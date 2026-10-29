import os
import urllib.request
import urllib.parse
import json
from typing import Dict, Any, List, Tuple, Optional
from .models import AuditIssue, LAB_VS_FIELD_DISCLAIMER

class LighthouseAuditor:
    """Retrieves synthetic laboratory Lighthouse diagnostics and Core Web Vitals telemetry."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("PAGESPEED_API_KEY", "")
        self.endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def run_audit(self, target_url: str, timestamp: str) -> Tuple[List[AuditIssue], Dict[str, Any]]:
        """Queries Lighthouse diagnostics via PageSpeed API (Mobile strategy)."""
        issues: List[AuditIssue] = []
        summary: Dict[str, Any] = {
            "strategy": "mobile",
            "laboratory_disclaimer": LAB_VS_FIELD_DISCLAIMER,
            "connected": False,
            "scores": {},
            "metrics": {}
        }

        params = {
            "url": target_url,
            "strategy": "mobile",
            "category": ["performance", "accessibility", "best-practices", "seo"]
        }
        if self.api_key:
            params["key"] = self.api_key

        query_str = urllib.parse.urlencode(params, doseq=True)
        req_url = f"{self.endpoint}?{query_str}"

        try:
            req = urllib.request.Request(
                req_url,
                headers={"User-Agent": "AIDigiTools-DeepAudit-Engine/1.0"}
            )
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                lh = data.get("lighthouseResult", {})
                cats = lh.get("categories", {})
                audits = lh.get("audits", {})

                scores = {
                    "performance": int((cats.get("performance", {}).get("score") or 0) * 100),
                    "accessibility": int((cats.get("accessibility", {}).get("score") or 0) * 100),
                    "best_practices": int((cats.get("best-practices", {}).get("score") or 0) * 100),
                    "seo": int((cats.get("seo", {}).get("score") or 0) * 100)
                }
                metrics = {
                    "largest_contentful_paint": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
                    "cumulative_layout_shift": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
                    "first_contentful_paint": audits.get("first-contentful-paint", {}).get("displayValue", "N/A"),
                    "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue", "N/A"),
                    "speed_index": audits.get("speed-index", {}).get("displayValue", "N/A")
                }

                summary["connected"] = True
                summary["scores"] = scores
                summary["metrics"] = metrics

                # Flag scores below minimum quality bar
                if scores["performance"] < 80:
                    issues.append(AuditIssue(
                        id="LH_PERFORMANCE_SCORE_LOW",
                        timestamp=timestamp,
                        tested_url=target_url,
                        category="LIGHTHOUSE",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Laboratory performance score is {scores['performance']}/100. (Note: Lab score does not equal CrUX field CWV).",
                        recommended_fix="Optimize critical render path, compress static assets, and defer third-party scripts."
                    ))

                if scores["accessibility"] < 90:
                    issues.append(AuditIssue(
                        id="LH_ACCESSIBILITY_SCORE_LOW",
                        timestamp=timestamp,
                        tested_url=target_url,
                        category="LIGHTHOUSE",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Laboratory accessibility score is {scores['accessibility']}/100.",
                        recommended_fix="Remediate color contrast, missing button text, and ARIA landmarks."
                    ))

        except Exception as e:
            summary["error"] = str(e)
            issues.append(AuditIssue(
                id="LIGHTHOUSE_API_UNAVAILABLE",
                timestamp=timestamp,
                tested_url=target_url,
                category="LIGHTHOUSE",
                severity="NOTICE",
                confidence="UNCERTAIN",
                evidence=f"Could not retrieve PageSpeed / Lighthouse API data: {str(e)}",
                recommended_fix="Check PAGESPEED_API_KEY quota or run Lighthouse locally via @lhci/cli."
            ))

        return issues, summary
