import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List
from .config import DEFAULT_GEMINI_MODEL, FALLBACK_GEMINI_MODEL

class GeminiReasoner:
    """Leverages Gemini Flash to analyze site audit telemetry, diagnose root causes, and plan safe repairs."""

    def __init__(self, api_key: str = None, model: str = DEFAULT_GEMINI_MODEL):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
        self.model = model

    def _call_gemini_rest_api(self, prompt: str) -> str:
        """Invokes the official Google Generative Language API directly over HTTPS without external dependencies."""
        models_to_try = [self.model]
        if FALLBACK_GEMINI_MODEL not in models_to_try:
            models_to_try.append(FALLBACK_GEMINI_MODEL)
        if "gemini-2.0-flash" not in models_to_try:
            models_to_try.append("gemini-2.0-flash")
        if "gemini-1.5-flash" not in models_to_try:
            models_to_try.append("gemini-1.5-flash")

        last_error = None
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 2048,
                    "responseMimeType": "application/json"
                }
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=35) as resp:
                    resp_json = json.loads(resp.read().decode("utf-8"))
                    candidates = resp_json.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            self.model = model
                            return parts[0]["text"]
                    return "{}"
            except Exception as e:
                last_error = e
                print(f"[REASONER] Model {model} attempt encountered: {e}. Trying next model...")
                continue

        if last_error:
            raise last_error
        return "{}"

    def _deterministic_heuristic_plan(self, audit_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Provides deterministic, rule-based diagnostic and repair planning when GEMINI_API_KEY is not configured."""
        auto_repairs = []
        manual_reviews = []

        # Analyze missing or extra sitemap entries
        missing_sm = audit_summary.get("missing_from_sitemap", [])
        if missing_sm:
            auto_repairs.append({
                "id": "repair-sitemap-sync",
                "risk": "LOW",
                "action": "Sync sitemap.xml with existing published HTML pages",
                "details": f"Add {len(missing_sm)} missing public pages to sitemap.xml",
                "affected_items": missing_sm
            })

        # Analyze canonical URL mismatches
        for iss in audit_summary.get("issues", []):
            if iss.get("type") == "canonical_mismatch":
                auto_repairs.append({
                    "id": f"repair-canonical-{iss.get('file')}",
                    "risk": "LOW",
                    "action": f"Correct canonical URL in {iss.get('file')}",
                    "details": iss.get("msg"),
                    "file": iss.get("file")
                })
            elif iss.get("type") == "image_alt_missing":
                auto_repairs.append({
                    "id": f"repair-alt-{iss.get('file')}",
                    "risk": "LOW",
                    "action": f"Provide descriptive alt attribute in {iss.get('file')}",
                    "details": iss.get("msg"),
                    "file": iss.get("file")
                })
            elif iss.get("type") == "missing_comparison_table":
                auto_repairs.append({
                    "id": f"repair-table-{iss.get('file')}",
                    "risk": "LOW",
                    "action": f"Inject structured comparison table into {iss.get('file')}",
                    "details": iss.get("msg"),
                    "file": iss.get("file")
                })
            elif iss.get("severity") == "CRITICAL":
                manual_reviews.append({
                    "id": f"review-critical-{iss.get('file')}",
                    "risk": "HIGH",
                    "action": f"Manual investigation required for {iss.get('file')}",
                    "details": iss.get("msg"),
                    "file": iss.get("file")
                })

        # Link graph issues
        broken_links = audit_summary.get("link_graph", {}).get("broken_links", [])
        if broken_links:
            manual_reviews.append({
                "id": "review-broken-links",
                "risk": "HIGH",
                "action": "Review and repair broken internal hyperlinks",
                "details": f"Found {len(broken_links)} broken internal links",
                "affected_items": broken_links[:5]
            })

        diagnosis = (
            f"Static audit scanned {audit_summary.get('pages_scanned', 0)} pages with health score "
            f"{audit_summary.get('health_score', 0)}%. "
            f"Detected {audit_summary.get('critical_count', 0)} critical issues, "
            f"{audit_summary.get('warning_count', 0)} warnings, and "
            f"{len(broken_links)} broken links. "
            f"{len(auto_repairs)} low-risk automated repair tasks identified; "
            f"{len(manual_reviews)} items flagged for engineer review."
        )

        return {
            "gemini_api_connected": False,
            "engine": "Deterministic Heuristic Diagnostic Engine",
            "model_used": "none (deterministic fallback)",
            "status_note": "GEMINI_API_KEY not configured in environment. Using reliable built-in heuristic reasoning.",
            "diagnosis": diagnosis,
            "auto_repair_proposals": auto_repairs,
            "manual_review_proposals": manual_reviews
        }

    def evaluate_audit(self, audit_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates audit findings using Gemini Flash if API key is present, otherwise uses deterministic heuristic engine."""
        if not self.api_key:
            return self._deterministic_heuristic_plan(audit_summary)

        # Build prompt for Gemini Flash
        clean_summary = {
            "pages_scanned": audit_summary.get("pages_scanned"),
            "health_score": audit_summary.get("health_score"),
            "critical_count": audit_summary.get("critical_count"),
            "warning_count": audit_summary.get("warning_count"),
            "missing_from_sitemap": audit_summary.get("missing_from_sitemap", []),
            "broken_links_count": audit_summary.get("link_graph", {}).get("broken_links_count", 0),
            "sample_issues": audit_summary.get("issues", [])[:15]
        }

        prompt = f"""
        You are the Senior Technical SEO & Reliability Architect for AIDigiTools (aidigitools.tech).
        Analyze the following technical audit findings and output a strict JSON evaluation:
        
        {json.dumps(clean_summary, indent=2)}

        Format your response as a valid JSON object matching this schema:
        {{
          "gemini_api_connected": true,
          "model_used": "{self.model}",
          "diagnosis": "Comprehensive diagnostic summary of site health",
          "auto_repair_proposals": [
            {{
              "id": "repair-id",
              "risk": "LOW",
              "action": "Description of low-risk safe autonomous repair",
              "details": "Technical rationale grounded in Google/Bing official SEO standards",
              "file": "path/to/file.html"
            }}
          ],
          "manual_review_proposals": [
            {{
              "id": "review-id",
              "risk": "HIGH",
              "action": "Description of high-impact item requiring human approval",
              "details": "Rationale why automated change is unsafe",
              "file": "path/to/file.html"
            }}
          ]
        }}
        """

        try:
            raw_response = self._call_gemini_rest_api(prompt)
            data = json.loads(raw_response)
            data["gemini_api_connected"] = True
            data["model_used"] = self.model
            return data
        except Exception as e:
            fallback = self._deterministic_heuristic_plan(audit_summary)
            fallback["gemini_error"] = str(e)
            fallback["status_note"] = f"Gemini API attempt encountered notice ({str(e)}). Gracefully fell back to deterministic heuristic planner."
            return fallback
