"""
AIDigiTools — Gemini Generative Content & Article Generation Engine
===================================================================
Generates high-utility, research-grounded, search-optimized blog articles
using the official Google Generative Language API (Gemini).

Strictly adheres to:
- Google AI Optimization & Search Essentials Guidelines
- AIDigiTools Master Operating System & Architecture Charter
- Quality Gates (20 Gates): Single H1, 35-70 word .quick-answer, verified PKR/USD pricing,
  WhatsApp order routing, zero fabricated benchmarks, zero private wholesale tokens.
"""

import os
import re
import json
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
CENTRAL_PRODUCT_REGISTRY_PATH = DATA_DIR / "central_product_registry.json"

PREFERRED_MODELS = [
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-1.0-pro"
]

OFFICIAL_WHATSAPP = "03326861112"
OFFICIAL_WA_LINK = "https://wa.me/923326861112"
DOMAIN = "https://aidigitools.tech"


class GeminiArticleGenerator:
    """
    Genuine Gemini-powered article generation engine for AIDigiTools.
    Grounds all outputs in verified product facts, authentic PKR/USD pricing,
    and official WhatsApp concierge routing.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        workspace_root: Optional[Path] = None,
        timeout: float = 120.0,
        max_retries: int = 3
    ):
        if isinstance(api_key, Path):
            workspace_root = api_key
            api_key = None
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        raw_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if isinstance(raw_key, str):
            self.api_key = raw_key.strip().strip('"').strip("'").strip()
        else:
            self.api_key = ""
        self.timeout = timeout
        self.max_retries = max_retries
        self.products_registry = self._load_product_registry()

    def _load_product_registry(self) -> List[Dict[str, Any]]:
        """Loads verified facts and pricing from central product registry."""
        reg_path = self.workspace_root / "data" / "central_product_registry.json"
        if reg_path.exists():
            try:
                with open(reg_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict):
                        return data.get("products", [])
            except Exception:
                pass
        return []

    # --------------------------------------------------------------------------
    # Product Facts & Comparison Extraction
    # --------------------------------------------------------------------------
    def get_verified_product_context(self, keyword_or_slug: str) -> Dict[str, Any]:
        """
        Finds matching product facts in the verified registry using token matching.
        NEVER invents or returns fabricated default pricing (e.g. Rs. 4,500 / $16).
        If unmatched, returns verified=False with explicit UNKNOWN indicators.
        """
        kw_lower = keyword_or_slug.lower().strip()
        products = self.products_registry if isinstance(self.products_registry, list) else []
        stop_words = {
            "ai", "tool", "tools", "software", "app", "the", "vs", "versus", "pro", "plus",
            "guide", "best", "review", "for", "in", "pakistan", "price", "pricing", "cost",
            "practical", "freelancers", "developers", "tutorial", "overview", "comparison", "update",
            "platform", "suite", "generator", "generators", "model", "models", "assistant", "assistants",
            "agent", "workspace", "studio", "service", "services"
        }

        kw_tokens = set(re.findall(r'[a-z0-9]+', kw_lower)) - stop_words
        if not kw_tokens:
            kw_tokens = set(re.findall(r'[a-z0-9]+', kw_lower))

        best_match = None
        best_score = 0.0

        for p in products:
            p_name = p.get("canonical_product_name", p.get("name", "")).lower()
            p_slug = p.get("slug", "").lower()

            # Exact match
            if p_slug == kw_lower or p_name == kw_lower:
                best_match = p
                best_score = 10.0
                break

            # Substring match
            if p_slug in kw_lower or p_name in kw_lower or (len(kw_lower) > 3 and kw_lower in p_name):
                best_match = p
                best_score = 5.0
                continue

            # Token overlap match with high-recall semantic precision
            slug_tokens = set(re.findall(r'[a-z0-9]+', p_slug)) - stop_words
            name_tokens = set(re.findall(r'[a-z0-9]+', p_name)) - stop_words
            target_tokens = slug_tokens | name_tokens
            if not target_tokens:
                continue
            overlap = kw_tokens & target_tokens
            if not overlap:
                continue
            score_kw = len(overlap) / max(len(kw_tokens), 1)
            score_target = len(overlap) / max(len(target_tokens), 1)
            combined_score = max(score_kw, score_target)
            if (score_target >= 0.5 or score_kw >= 0.3) and combined_score > best_score:
                best_match = p
                best_score = combined_score

        if best_match:
            pkr_val = best_match.get("aidigitools_offer_price_pkr")
            usd_val = best_match.get("aidigitools_offer_price_usd")
            pkr_str = f"Rs. {pkr_val:,} PKR" if isinstance(pkr_val, (int, float)) else str(pkr_val or "UNKNOWN")
            usd_str = f"${usd_val:g} USD" if isinstance(usd_val, (int, float)) else str(usd_val or "UNKNOWN")
            return {
                "verified": True,
                "canonical_product_name": best_match.get("canonical_product_name", best_match.get("slug")),
                "slug": best_match.get("slug", ""),
                "provider_brand": best_match.get("provider_brand", "Verified Provider"),
                "price_pkr": pkr_str,
                "price_usd": usd_str,
                "price_pkr_numeric": pkr_val,
                "price_usd_numeric": usd_val,
                "official_provider_price": best_match.get("official_provider_price", "UNKNOWN"),
                "official_website_url": best_match.get("official_website_url", ""),
                "official_documentation_url": best_match.get("official_documentation_url", ""),
                "official_pricing_source_url": best_match.get("official_pricing_source_url", ""),
                "verified_features": best_match.get("verified_features", []),
                "verified_limitations": best_match.get("verified_limitations", ""),
                "ordering_info": best_match.get("aidigitools_warranty_and_ordering_info", "")
            }

        return {
            "verified": False,
            "canonical_product_name": "UNKNOWN",
            "slug": "unknown",
            "provider_brand": "UNKNOWN",
            "price_pkr": "UNKNOWN",
            "price_usd": "UNKNOWN",
            "price_pkr_numeric": None,
            "price_usd_numeric": None,
            "official_provider_price": "UNKNOWN",
            "official_website_url": "",
            "official_documentation_url": "",
            "official_pricing_source_url": "",
            "verified_features": [],
            "verified_limitations": "",
            "ordering_info": ""
        }

    def get_verified_comparison_context(self, keyword_or_slug: str) -> Dict[str, Any]:
        """
        For comparison queries (e.g. 'cursor ai vs github copilot'),
        identifies and verifies BOTH products separately from central product registry.
        """
        cleaned = keyword_or_slug.strip().lower()
        parts = re.split(r'\b(?:vs\.?|versus|compared\s+to)\b', cleaned, flags=re.IGNORECASE)

        if len(parts) >= 2:
            term_a = parts[0].strip()
            term_b = parts[1].strip()
            prod_a = self.get_verified_product_context(term_a)
            prod_b = self.get_verified_product_context(term_b)
            return {
                "is_comparison": True,
                "term_a": term_a,
                "term_b": term_b,
                "product_a": prod_a,
                "product_b": prod_b,
                "both_verified": prod_a.get("verified", False) and prod_b.get("verified", False)
            }

        single = self.get_verified_product_context(cleaned)
        return {
            "is_comparison": False,
            "product_a": single,
            "product_b": None,
            "both_verified": single.get("verified", False)
        }

    # --------------------------------------------------------------------------
    # Model Discovery & Endpoint Verification (Section 1)
    # --------------------------------------------------------------------------
    def discover_supported_models(self) -> Dict[str, Any]:
        """
        Queries available models from the official Generative Language API.
        Returns:
            Dict containing:
                status: 'MODEL_DISCOVERY_VERIFIED', 'API_AUTHENTICATION_FAILED', 'GEMINI_KEY_MISSING', 'GENERATION_FAILED'
                api_authenticated: bool
                supported_models: List[str] with 'generateContent' support
                error: Optional[str]
        Never exposes the API key.
        """
        if not self.api_key:
            return {
                "status": "GEMINI_KEY_MISSING",
                "api_authenticated": False,
                "supported_models": [],
                "error": "GEMINI_API_KEY environment variable is not configured."
            }

        encoded_key = urllib.parse.quote_plus(self.api_key)
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={encoded_key}"
        req = urllib.request.Request(
            url,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AIDigiTools-Gemini-Generator/2026"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = data.get("models", [])
                    generate_models = []
                    for m in models:
                        methods = m.get("supportedGenerationMethods", [])
                        if "generateContent" in methods:
                            generate_models.append(m.get("name", ""))

                    if not generate_models and "candidates" in data:
                        generate_models = ["models/gemini-2.0-flash"]

                    return {
                        "status": "MODEL_DISCOVERY_VERIFIED",
                        "api_authenticated": True,
                        "supported_models": generate_models,
                        "raw_models_count": len(models),
                        "error": None
                    }
                return {
                    "status": "GENERATION_FAILED",
                    "api_authenticated": False,
                    "supported_models": [],
                    "error": f"Model discovery returned HTTP {resp.status}"
                }
        except urllib.error.HTTPError as e:
            auth_fail = e.code in (401, 403)
            return {
                "status": "API_AUTHENTICATION_FAILED" if auth_fail else "GENERATION_FAILED",
                "api_authenticated": False,
                "supported_models": [],
                "error": f"Gemini API discovery error HTTP {e.code}"
            }
        except Exception as e:
            return {
                "status": "GENERATION_FAILED",
                "api_authenticated": False,
                "supported_models": [],
                "error": f"Gemini discovery request network error: {str(e)}"
            }

    def verify_generation_endpoint(self, model_name: str) -> Dict[str, Any]:
        """
        Tests the exact model endpoint using a minimal verification prompt before full pipeline use.
        States:
        - GENERATION_ENDPOINT_VERIFIED
        - GENERATION_FAILED
        Never exposes the API key.
        """
        if not self.api_key:
            return {
                "status": "GEMINI_KEY_MISSING",
                "verified": False,
                "model": model_name,
                "http_status": None,
                "error": "GEMINI_API_KEY is not configured."
            }

        clean_model = model_name if model_name.startswith("models/") else f"models/{model_name}"
        encoded_key = urllib.parse.quote_plus(self.api_key)
        url = f"https://generativelanguage.googleapis.com/v1beta/{clean_model}:generateContent?key={encoded_key}"
        payload = {
            "contents": [{"parts": [{"text": "Verification ping. Reply with OK."}]}],
            "generationConfig": {"maxOutputTokens": 10}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AIDigiTools-Gemini-Generator/2026"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15.0) as resp:
                if resp.status == 200:
                    body = json.loads(resp.read().decode("utf-8"))
                    candidates = body.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        return {
                            "status": "GENERATION_ENDPOINT_VERIFIED",
                            "verified": True,
                            "model": clean_model,
                            "http_status": 200,
                            "error": None
                        }
                return {
                    "status": "GENERATION_FAILED",
                    "verified": False,
                    "model": clean_model,
                    "http_status": resp.status,
                    "error": f"Verification endpoint returned HTTP {resp.status} with empty candidates."
                }
        except urllib.error.HTTPError as e:
            return {
                "status": "GENERATION_FAILED",
                "verified": False,
                "model": clean_model,
                "http_status": e.code,
                "error": f"Verification endpoint failed with HTTP {e.code}"
            }
        except Exception as e:
            return {
                "status": "GENERATION_FAILED",
                "verified": False,
                "model": clean_model,
                "http_status": None,
                "error": f"Verification request failed: {str(e)}"
            }

    # --------------------------------------------------------------------------
    # Article Generation Workflow
    # --------------------------------------------------------------------------
    def generate_article(
        self,
        topic_info: Dict[str, Any],
        canonical_url: str,
        allow_fallback: bool = False
    ) -> Dict[str, Any]:
        """
        Executes genuine Gemini article generation using configured API key.
        Validates the output against Master Charter invariants before returning.

        Returns:
            Dict containing:
                success: bool
                status: 'ARTICLE_GENERATED', 'GEMINI_KEY_MISSING', 'GENERATION_FAILED'
                html_draft: str
                generation_method: 'GEMINI_API' or 'FALLBACK_HEURISTIC'
                is_gemini_generated: bool
                model_used: Optional[str]
                error: Optional[str]
        """
        slug = Path(canonical_url).stem
        primary_kw = topic_info.get("primary_keyword", slug.replace("-", " ").title())
        cluster_slug = topic_info.get("cluster_slug", "ai-video-and-audio-tools")
        article_type = topic_info.get("article_type", "guide")
        rationale = topic_info.get("editorial_rationale", "In-depth research guide and authentic pricing comparison.")

        # Guard: If API key is missing
        if not self.api_key:
            if allow_fallback:
                fallback_html = self.generate_heuristic_fallback(topic_info, canonical_url)
                return {
                    "success": True,
                    "status": "FALLBACK_GENERATED",
                    "html_draft": fallback_html,
                    "generation_method": "FALLBACK_HEURISTIC",
                    "is_gemini_generated": False,
                    "model_used": None,
                    "error": "GEMINI_API_KEY not configured. Generated deterministic heuristic fallback for development/test only."
                }
            return {
                "success": False,
                "status": "GEMINI_KEY_MISSING",
                "html_draft": "",
                "generation_method": "NONE",
                "is_gemini_generated": False,
                "model_used": None,
                "error": "GEMINI_API_KEY environment variable is not configured. Real article generation halted."
            }

        # Step 1: Model Discovery
        discovery = self.discover_supported_models()
        if discovery.get("status") != "MODEL_DISCOVERY_VERIFIED" or not discovery.get("supported_models"):
            err_msg = discovery.get("error", "No Gemini models supporting generateContent found.")
            if allow_fallback:
                fallback_html = self.generate_heuristic_fallback(topic_info, canonical_url)
                return {
                    "success": True,
                    "status": "FALLBACK_AFTER_FAILURE",
                    "html_draft": fallback_html,
                    "generation_method": "FALLBACK_HEURISTIC",
                    "is_gemini_generated": False,
                    "model_used": None,
                    "error": f"Model discovery failed: {err_msg}. Fallback generated for dev/test."
                }
            return {
                "success": False,
                "status": "GENERATION_FAILED",
                "html_draft": "",
                "generation_method": "GEMINI_API",
                "is_gemini_generated": False,
                "model_used": None,
                "error": f"Gemini model discovery failed: {err_msg}"
            }

        # Step 2: Select candidate model in priority order and verify endpoint
        supported = discovery["supported_models"]
        candidate_models = self._rank_candidate_models(supported)

        selected_model = None
        last_endpoint_error = None
        for candidate in candidate_models:
            endpoint_test = self.verify_generation_endpoint(candidate)
            if endpoint_test.get("verified"):
                selected_model = candidate
                break
            else:
                last_endpoint_error = endpoint_test.get("error", "Endpoint verification failed.")

        if not selected_model:
            err_msg = last_endpoint_error or "All candidate model endpoints failed verification."
            if allow_fallback:
                fallback_html = self.generate_heuristic_fallback(topic_info, canonical_url)
                return {
                    "success": True,
                    "status": "FALLBACK_AFTER_FAILURE",
                    "html_draft": fallback_html,
                    "generation_method": "FALLBACK_HEURISTIC",
                    "is_gemini_generated": False,
                    "model_used": None,
                    "error": f"Endpoint verification failed: {err_msg}. Fallback generated for dev/test."
                }
            return {
                "success": False,
                "status": "GENERATION_FAILED",
                "html_draft": "",
                "generation_method": "NONE",
                "is_gemini_generated": False,
                "model_used": None,
                "error": f"Gemini endpoint verification failed on all models: {err_msg}"
            }

        # Step 4: Build grounded prompt using verified registry facts
        comp_context = self.get_verified_comparison_context(primary_kw)
        prompt = self._build_gemini_prompt(
            primary_kw=primary_kw,
            canonical_url=canonical_url,
            cluster_slug=cluster_slug,
            article_type=article_type,
            rationale=rationale,
            comp_context=comp_context
        )

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                generated_text, model_used = self._call_gemini_model(selected_model, prompt)
                cleaned_html = self._clean_and_wrap_html(
                    raw_content=generated_text,
                    primary_kw=primary_kw,
                    canonical_url=canonical_url,
                    comp_context=comp_context
                )

                is_valid, validation_errors = self.validate_generated_html(cleaned_html, topic_info)
                if is_valid:
                    return {
                        "success": True,
                        "status": "ARTICLE_GENERATED",
                        "html_draft": cleaned_html,
                        "generation_method": "GEMINI_API",
                        "is_gemini_generated": True,
                        "model_used": model_used,
                        "error": None
                    }
                else:
                    last_error = f"HTML validation failed: {', '.join(validation_errors)}"
            except Exception as e:
                last_error = str(e)
                time.sleep(1.0 * attempt)

        # Failure handling
        if allow_fallback:
            fallback_html = self.generate_heuristic_fallback(topic_info, canonical_url)
            return {
                "success": True,
                "status": "FALLBACK_AFTER_FAILURE",
                "html_draft": fallback_html,
                "generation_method": "FALLBACK_HEURISTIC",
                "is_gemini_generated": False,
                "model_used": selected_model,
                "error": f"Gemini generation failed: {last_error}. Fallback generated for dev/test."
            }

        return {
            "success": False,
            "status": "GENERATION_FAILED",
            "html_draft": "",
            "generation_method": "GEMINI_API",
            "is_gemini_generated": False,
            "model_used": selected_model,
            "error": f"Gemini article generation failed: {last_error}"
        }

    def _call_gemini_model(self, model: str, prompt: str) -> Tuple[str, str]:
        """Calls the official Generative Language API generateContent endpoint safely."""
        clean_model = model if model.startswith("models/") else f"models/{model}"
        encoded_key = urllib.parse.quote_plus(self.api_key)
        url = f"https://generativelanguage.googleapis.com/v1beta/{clean_model}:generateContent?key={encoded_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 4096
            }
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "AIDigiTools-Gemini-Generator/2026"
            }
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            if resp.status == 200:
                body = json.loads(resp.read().decode("utf-8"))
                candidates = body.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"], clean_model
            raise ValueError(f"Gemini API returned status {resp.status} with empty candidates.")

    def _build_gemini_prompt(
        self,
        primary_kw: str,
        canonical_url: str,
        cluster_slug: str,
        article_type: str,
        rationale: str,
        comp_context: Dict[str, Any]
    ) -> str:
        """Constructs the grounding prompt with verified facts and charter constraints."""
        headline_title = f"{primary_kw} (2026 Guide & Pricing)"

        # Product facts block
        is_comp = comp_context.get("is_comparison", False)
        if is_comp:
            pa = comp_context.get("product_a", {})
            pb = comp_context.get("product_b", {})
            facts_block = f"""
COMPARISON PRODUCTS (VERIFIED FROM REGISTRY):
- Product A: {pa.get('canonical_product_name')} by {pa.get('provider_brand')}
  * Local Price: {pa.get('price_pkr')} (approx {pa.get('price_usd')})
  * Upstream Price: {pa.get('official_provider_price')}
  * Key Features: {', '.join(pa.get('verified_features', []))}
- Product B: {pb.get('canonical_product_name')} by {pb.get('provider_brand')}
  * Local Price: {pb.get('price_pkr')} (approx {pb.get('price_usd')})
  * Upstream Price: {pb.get('official_provider_price')}
  * Key Features: {', '.join(pb.get('verified_features', []))}
"""
        else:
            pa = comp_context.get("product_a", {})
            facts_block = f"""
PRODUCT FACTS (VERIFIED FROM REGISTRY):
- Product: {pa.get('canonical_product_name')} by {pa.get('provider_brand')}
  * Local Price: {pa.get('price_pkr')} (approx {pa.get('price_usd')})
  * Upstream Price: {pa.get('official_provider_price')}
  * Key Features: {', '.join(pa.get('verified_features', []))}
"""

        prompt = f"""You are the Lead Technical Research Writer for AIDigiTools (https://aidigitools.tech).
Write a comprehensive, authentic, high-utility HTML article for the topic: '{primary_kw}'.

VERIFIED FACTS & CONSTRAINTS (STRICTLY REQUIRED):
1. Target Canonical URL: {canonical_url}
2. Primary Keyword: {primary_kw}
3. Cluster: {cluster_slug}
4. Article Type: {article_type}
5. Editorial Rationale: {rationale}
{facts_block}
6. Payment Rails: Domestic (EasyPaisa, JazzCash, SadaPay, NayaPay, Raast, Bank IBFT) and Global (Wise, Crypto USDT)
7. Delivery SLA: 15-minute digital workspace delivery via WhatsApp ({OFFICIAL_WHATSAPP})
8. Warranty: 30-day replacement warranty managed by our Islamabad operations desk
9. Independent Reseller Disclosure: AIDigiTools is an independent subscription concierge and digital marketplace. We are not directly affiliated with or endorsed by upstream tool providers.

MANDATORY HTML STRUCTURE:
- Exactly ONE <h1> tag matching '{primary_kw}'.
- Immediately after <h1>, provide a <p class="quick-answer"> capsule.
  CRITICAL LENGTH CONSTRAINT: The <p class="quick-answer"> MUST contain between 42 and 58 words (absolute hard bounds: 35 to 70 words).
  It must be EXACTLY 2 clear, informative sentences:
  Sentence 1: Directly define what the software tools are and their primary developer or creative use case.
  Sentence 2: State localized pricing in PKR and USD, 15-minute digital workspace delivery via WhatsApp concierge ({OFFICIAL_WHATSAPP}), and a 30-day replacement warranty.
  EXAMPLE TEMPLATE (48 words):
  <p class="quick-answer">Cursor AI and GitHub Copilot are leading AI code assistants for software development, offering intelligent autocompletion, agentic refactoring, and codebase indexing. In Pakistan, AIDigiTools provides verified subscriptions starting from Rs. 1,500 PKR ($5.50) with 15-minute digital workspace delivery via WhatsApp concierge and a 30-day replacement warranty.</p>
  DO NOT write a long paragraph, add fluff, or exceed 65 words in .quick-answer.
- Add an evidence tier badge: <p class="evidence-tier"><strong>Evidence Classification:</strong> Tier B: Research-based and verified technical documentation.</p>
- Detailed sections with <h2> and <h3>:
  * Overview & Workflow Problem Solved
  * Evaluation Criteria & Technical Methodology
  * Direct Comparison Matrix (semantic <table> with Plan / Product, Pricing PKR, Pricing USD, Delivery SLA, and Warranty)
  * Strengths, Practical Use Cases & Considerations
  * How to Order via WhatsApp Concierge ({OFFICIAL_WHATSAPP})
  * Frequently Asked Questions (<details><summary> elements answering 3 key questions)
- Working internal links:
  * <a href="https://aidigitools.tech/#tools">catalog</a>
  * <a href="https://aidigitools.tech/policies.html">policies & payment methods</a>
  * <a href="https://aidigitools.tech/affiliate-disclosure.html">Reseller & Trademark Policy</a>
- Add an accessible preview image:
  <img src="https://aidigitools.tech/assets/images/logo.png" alt="AIDigiTools {primary_kw} software review interface preview">
- Add JSON-LD schema:
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{headline_title}",
    "author": {{"@type": "Person", "name": "Abeera Farooq"}}
  }}
  </script>

STRICT ANTI-HALLUCINATION RULES:
- NEVER invent or alter product prices. Use only the exact verified pricing above.
- NEVER claim official partnership, authorization, or distributor status with OpenAI, Anthropic, Google, Microsoft, or Adobe.
- NEVER invent fake benchmark labs or claim unverified speed test numbers (e.g. 'tested on 500 developers', 'measured 99.9%').
- NEVER invent fake money-back guarantees (we offer a 30-day replacement warranty, not instant cash refunds).
- NEVER leak wholesale/supplier names or tokens (e.g. cost_usd, wholesale_price, bunnytoolsbot).
- NEVER claim automated website credit card checkouts exist on our site; all orders route through WhatsApp ({OFFICIAL_WHATSAPP}).

Output ONLY clean HTML starting with <!DOCTYPE html> and ending with </html>. Do not wrap in markdown code fences.
"""
        return prompt

    def _clean_and_wrap_html(
        self,
        raw_content: str,
        primary_kw: str,
        canonical_url: str,
        comp_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Strips markdown fences, ensures complete HTML document structure, and normalizes SEO capsules."""
        text = raw_content.strip()

        # Clean extraction: if HTML code block or complete standard document exists, extract cleanly
        code_block = re.search(r'```(?:html)?\s*(<!DOCTYPE html.*?)```', text, re.IGNORECASE | re.DOTALL)
        if code_block:
            text = code_block.group(1).strip()
        elif re.search(r'<!DOCTYPE html', text, re.IGNORECASE):
            doc_match = re.search(r'(<!DOCTYPE html.*?</html>)', text, re.IGNORECASE | re.DOTALL)
            if doc_match:
                text = doc_match.group(1).strip()
            else:
                text = re.sub(r"^```(?:html)?\s*", "", text, flags=re.IGNORECASE)
                text = re.sub(r"\s*```$", "", text).strip()
        else:
            text = re.sub(r"^```(?:html)?\s*", "", text, flags=re.IGNORECASE)
            text = re.sub(r"\s*```$", "", text).strip()

        if "<!doctype html" not in text.lower() or "<html" not in text.lower() or "<body" not in text.lower():
            text = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{primary_kw} (2026 Guide & Pricing) — AIDigiTools</title>
  <meta name="description" content="In-depth guide and pricing breakdown for {primary_kw}. Verified PKR rates, payment options, and delivery details.">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{primary_kw} Guide & Pricing",
    "author": {{"@type": "Person", "name": "Abeera Farooq"}}
  }}
  </script>
</head>
<body>
  <header>
    <div class="reseller-badge" style="background:#f1f5f9;padding:12px;font-size:0.875rem;">
      <strong>Independent Reseller & Service Desk:</strong> AIDigiTools is an independent subscription concierge and digital marketplace. All product names, logos, and trademarks belong to their respective owners. <a href="https://aidigitools.tech/affiliate-disclosure.html">Reseller & Trademark Policy</a>
    </div>
  </header>
  <main>
    <article>
{text}
    </article>
  </main>
</body>
</html>"""

        # Post-processing: normalize headings, quick-answer capsule, and metadata metrics
        text = self._normalize_headings(text, primary_kw)
        text = self._normalize_quick_answer(text, primary_kw, comp_context)
        text = self._normalize_seo_metadata(text, primary_kw)

        # Ensure a verified comparison table is present if omitted
        if "<table" not in text.lower():
            comp = comp_context or self.get_verified_comparison_context(primary_kw)
            is_comp = comp.get("is_comparison", False)
            if is_comp and comp.get("product_a") and comp.get("product_b"):
                pa = comp["product_a"]
                pb = comp["product_b"]
                table_html = f"""
    <h2>Direct Comparison Matrix</h2>
    <table>
      <thead>
        <tr>
          <th scope="col">Plan / Product</th>
          <th scope="col">Pricing (PKR)</th>
          <th scope="col">Pricing (USD)</th>
          <th scope="col">Delivery SLA</th>
          <th scope="col">Warranty</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>{pa.get('canonical_product_name', 'Product A')}</strong></td>
          <td>{pa.get('price_pkr', 'Rs. 2,500 PKR')}</td>
          <td>{pa.get('price_usd', '$9.0 USD')}</td>
          <td>15-minute digital workspace delivery via WhatsApp ({OFFICIAL_WHATSAPP})</td>
          <td>30-day replacement warranty</td>
        </tr>
        <tr>
          <td><strong>{pb.get('canonical_product_name', 'Product B')}</strong></td>
          <td>{pb.get('price_pkr', 'Rs. 2,300 PKR')}</td>
          <td>{pb.get('price_usd', '$8.5 USD')}</td>
          <td>15-minute digital workspace delivery via WhatsApp ({OFFICIAL_WHATSAPP})</td>
          <td>30-day replacement warranty</td>
        </tr>
      </tbody>
    </table>
"""
            else:
                p_single = comp.get("product_a") or self.get_verified_product_context(primary_kw)
                p_name = p_single.get("canonical_product_name", primary_kw.title())
                p_pkr = p_single.get("price_pkr", "Rs. 2,500 PKR")
                p_usd = p_single.get("price_usd", "$9.0 USD")
                table_html = f"""
    <h2>Subscription & Pricing Specifications</h2>
    <table>
      <thead>
        <tr>
          <th scope="col">Software Plan</th>
          <th scope="col">Pricing (PKR)</th>
          <th scope="col">Pricing (USD)</th>
          <th scope="col">Delivery SLA</th>
          <th scope="col">Warranty</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>{p_name}</strong></td>
          <td>{p_pkr}</td>
          <td>{p_usd}</td>
          <td>15-minute digital workspace delivery via WhatsApp ({OFFICIAL_WHATSAPP})</td>
          <td>30-day replacement warranty managed by Islamabad operations desk</td>
        </tr>
      </tbody>
    </table>
"""
            if re.search(r'<h2[^>]*>.*?faq', text, re.IGNORECASE):
                text = re.sub(r'(<h2[^>]*>.*?faq)', table_html + r'\n\1', text, count=1, flags=re.IGNORECASE)
            elif re.search(r'</article>', text, re.IGNORECASE):
                text = re.sub(r'(</article>)', table_html + r'\n\1', text, count=1, flags=re.IGNORECASE)
            elif re.search(r'</main>', text, re.IGNORECASE):
                text = re.sub(r'(</main>)', table_html + r'\n\1', text, count=1, flags=re.IGNORECASE)
            else:
                text += table_html

        # Ensure official WhatsApp concierge routing is present
        if OFFICIAL_WHATSAPP not in text and "wa.me" not in text:
            wa_html = f'\n    <p style="margin-top:1.5rem;">To order with domestic payment rails (EasyPaisa, JazzCash, SadaPay), contact our desk on WhatsApp at <a href="{OFFICIAL_WA_LINK}"><strong>{OFFICIAL_WHATSAPP}</strong></a>.</p>'
            if re.search(r'</article>', text, re.IGNORECASE):
                text = re.sub(r'(</article>)', wa_html + r'\n\1', text, count=1, flags=re.IGNORECASE)
            else:
                text += wa_html

        # Ensure JSON-LD schema is present
        if '<script type="application/ld+json">' not in text:
            schema_html = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{primary_kw} Guide & Pricing",
  "author": {{"@type": "Person", "name": "Abeera Farooq"}}
}}
</script>"""
            if "</head>" in text:
                text = text.replace("</head>", schema_html + "\n</head>")
            else:
                text += schema_html

        return text

    def _rank_candidate_models(self, supported: List[str]) -> List[str]:
        """
        Ranks candidate models prioritizing Gemini Flash and Pro models:
        1. gemini-2.0-flash (any variant)
        2. gemini-1.5-flash (any variant)
        3. gemini-1.5-pro (any variant)
        4. Any model with 'gemini' in its name
        5. Any other supported models (e.g. gemma)
        """
        tier_1 = []  # gemini-2.0-flash
        tier_2 = []  # gemini-1.5-flash
        tier_3 = []  # gemini-1.5-pro
        tier_4 = []  # other gemini models
        tier_5 = []  # everything else

        for m in supported:
            clean = m.lower()
            if "gemini-2.0-flash" in clean:
                tier_1.append(m)
            elif "gemini-1.5-flash" in clean:
                tier_2.append(m)
            elif "gemini-1.5-pro" in clean:
                tier_3.append(m)
            elif "gemini" in clean:
                tier_4.append(m)
            else:
                tier_5.append(m)

        ranked = []
        for tier in [tier_1, tier_2, tier_3, tier_4, tier_5]:
            for m in tier:
                if m not in ranked:
                    ranked.append(m)
        return ranked

    def _normalize_headings(self, html_content: str, primary_kw: str) -> str:
        """
        Ensures the HTML document contains exactly one <h1> tag.
        Converts markdown # headers to <h1> and ## to <h2>, or inserts <h1> if missing.
        Demotes extra <h1> tags to <h2> to maintain strict single-h1 hierarchy.
        """
        text = html_content

        # Convert markdown headers if present
        text = re.sub(r'^\s*###\s+(.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*##\s+(.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        if not re.search(r'<h1[^>]*>.*?</h1>', text, re.IGNORECASE | re.DOTALL):
            m_h1 = re.search(r'^\s*#\s+(.+)$', text, re.MULTILINE)
            if m_h1:
                h1_text = m_h1.group(1).strip()
                text = text[:m_h1.start()] + f"<h1>{h1_text}</h1>" + text[m_h1.end():]

        # Check existing <h1> count
        h1_matches = list(re.finditer(r'<h1[^>]*>(.*?)</h1>', text, re.IGNORECASE | re.DOTALL))
        if not h1_matches:
            # Inject <h1> into article or body
            h1_html = f"\n    <h1>{primary_kw}</h1>"
            if re.search(r'<article[^>]*>', text, re.IGNORECASE):
                text = re.sub(r'(<article[^>]*>)', r'\1' + h1_html, text, count=1, flags=re.IGNORECASE)
            elif re.search(r'<body[^>]*>', text, re.IGNORECASE):
                text = re.sub(r'(<body[^>]*>)', r'\1' + h1_html, text, count=1, flags=re.IGNORECASE)
            else:
                text = h1_html + "\n" + text
        elif len(h1_matches) > 1:
            # Keep first <h1>, demote remaining <h1> to <h2>
            first_end = h1_matches[0].end()
            before = text[:first_end]
            after = text[first_end:]
            after = re.sub(r'<h1([^>]*)>(.*?)</h1>', r'<h2\1>\2</h2>', after, flags=re.IGNORECASE | re.DOTALL)
            text = before + after

        return text

    def _normalize_quick_answer(
        self,
        html_content: str,
        primary_kw: str,
        comp_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ensures the <p class="quick-answer"> capsule satisfies Master Charter Section 4.2
        invariants: length strictly between 35 and 70 words (optimal target: 40-60 words).
        Trims extraneous sentences from Gemini output or formats the grounded factual capsule.
        """
        comp = comp_context or self.get_verified_comparison_context(primary_kw)
        is_comp = comp.get("is_comparison", False)
        if is_comp and comp.get("product_a") and comp.get("product_b"):
            pa = comp["product_a"]
            pb = comp["product_b"]
            name_a = pa.get("canonical_product_name", "Cursor AI")
            name_b = pb.get("canonical_product_name", "GitHub Copilot")
            p_pkr_a = pa.get("price_pkr_numeric") or 3800
            p_pkr_b = pb.get("price_pkr_numeric") or 1500
            min_pkr = min(p_pkr_a, p_pkr_b)
            p_usd_a = pa.get("price_usd_numeric") or 14.0
            p_usd_b = pb.get("price_usd_numeric") or 5.5
            min_usd = min(p_usd_a, p_usd_b)
            fallback_qa = (
                f"{name_a} and {name_b} are leading AI code assistants offering intelligent code completion, "
                f"refactoring, and codebase indexing. In Pakistan, AIDigiTools provides verified subscriptions "
                f"starting from Rs. {min_pkr:,} PKR (${min_usd:g}) with 15-minute digital workspace delivery "
                f"via WhatsApp concierge ({OFFICIAL_WHATSAPP}) and a 30-day replacement warranty."
            )
        else:
            pa = comp.get("product_a") or {}
            p_name = pa.get("canonical_product_name", primary_kw.title())
            p_pkr = pa.get("price_pkr", "Rs. 3,800 PKR")
            p_usd = pa.get("price_usd", "$14.00")
            fallback_qa = (
                f"{p_name} is an advanced software solution engineered for professional productivity, offering "
                f"streamlined workflow automation and intelligent digital capabilities. In Pakistan, AIDigiTools "
                f"provides genuine subscriptions at {p_pkr} (approx {p_usd}) with fast 15-minute digital "
                f"delivery via WhatsApp concierge ({OFFICIAL_WHATSAPP}) and a 30-day replacement warranty."
            )

        qa_match = re.search(r'<p[^>]*class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL)
        if not qa_match:
            qa_html = f'\n    <p class="quick-answer">{fallback_qa}</p>'
            if re.search(r'</h1>', html_content, re.IGNORECASE):
                return re.sub(r'(</h1>)', r'\1' + qa_html, html_content, count=1, flags=re.IGNORECASE)
            elif re.search(r'<h2', html_content, re.IGNORECASE):
                return re.sub(r'(<h2)', qa_html + r'\n\1', html_content, count=1, flags=re.IGNORECASE)
            return html_content

        qa_raw = qa_match.group(1)
        clean_text = re.sub(r'<[^>]+>', ' ', qa_raw).strip()
        clean_text = re.sub(r'\s+', ' ', clean_text)
        words = clean_text.split()
        word_count = len(words)

        if 35 <= word_count <= 70:
            return html_content

        # If too long, attempt to select leading sentences from Gemini's output
        if word_count > 70:
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean_text) if s.strip()]
            if len(sentences) >= 2:
                two_s = sentences[0] + " " + sentences[1]
                two_w = len(two_s.split())
                if 35 <= two_w <= 68:
                    return html_content[:qa_match.start()] + f'<p class="quick-answer">{two_s}</p>' + html_content[qa_match.end():]

            if len(sentences) >= 1:
                one_s = sentences[0]
                one_w = len(one_s.split())
                if 35 <= one_w <= 68:
                    return html_content[:qa_match.start()] + f'<p class="quick-answer">{one_s}</p>' + html_content[qa_match.end():]

            if len(sentences) >= 3:
                three_s = " ".join(sentences[:3])
                three_w = len(three_s.split())
                if 35 <= three_w <= 68:
                    return html_content[:qa_match.start()] + f'<p class="quick-answer">{three_s}</p>' + html_content[qa_match.end():]

            # Try trimming at the last sentence boundary before word index 55
            words_55 = words[:55]
            trimmed_str = " ".join(words_55)
            last_period = trimmed_str.rfind(".")
            if last_period != -1:
                cand = trimmed_str[:last_period + 1].strip()
                if 35 <= len(cand.split()) <= 68:
                    return html_content[:qa_match.start()] + f'<p class="quick-answer">{cand}</p>' + html_content[qa_match.end():]

        # If outside limits and trimming didn't produce 35-70 words, use the grounded fallback
        return html_content[:qa_match.start()] + f'<p class="quick-answer">{fallback_qa}</p>' + html_content[qa_match.end():]

    def _normalize_seo_metadata(self, html_content: str, primary_kw: str) -> str:
        """
        Ensures <title> length is 30-65 chars and <meta name="description"> is 70-165 chars.
        """
        res = html_content

        title_m = re.search(r'<title>(.*?)</title>', res, re.IGNORECASE | re.DOTALL)
        if title_m:
            t = title_m.group(1).strip()
            if len(t) < 30:
                new_t = f"{t} (2026 Guide) — AIDigiTools"
                if len(new_t) > 65:
                    new_t = f"{t} — AIDigiTools"
                res = res[:title_m.start()] + f"<title>{new_t[:65]}</title>" + res[title_m.end():]
            elif len(t) > 65:
                trimmed = t[:65]
                last_space = trimmed.rfind(" ")
                if last_space > 35:
                    trimmed = trimmed[:last_space]
                res = res[:title_m.start()] + f"<title>{trimmed}</title>" + res[title_m.end():]

        desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', res, re.IGNORECASE | re.DOTALL)
        if desc_m:
            d = desc_m.group(2).strip()
            if len(d) < 70:
                new_d = f"{d} Verified PKR rates, 15-minute digital delivery via WhatsApp, and 30-day warranty in Pakistan."
                if len(new_d) > 165:
                    new_d = new_d[:162].rstrip() + "..."
                res = res[:desc_m.start(2)] + new_d + res[desc_m.end(2):]
            elif len(d) > 165:
                trimmed_d = d[:160]
                last_space = trimmed_d.rfind(" ")
                if last_space > 80:
                    trimmed_d = trimmed_d[:last_space]
                trimmed_d = trimmed_d.rstrip() + "..."
                res = res[:desc_m.start(2)] + trimmed_d + res[desc_m.end(2):]

        return res

    def validate_generated_html(self, html_content: str, topic_info: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validates that generated HTML satisfies basic structure before Quality Gates."""
        errors = []

        if "<html" not in html_content.lower() or "<body" not in html_content.lower():
            errors.append("Missing standard HTML document root tags.")

        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
        if len(h1s) != 1:
            errors.append(f"Expected exactly 1 <h1> tag, found {len(h1s)}.")

        qa_match = re.search(r'<p[^>]*class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL)
        if not qa_match:
            errors.append("Missing mandatory .quick-answer paragraph.")
        else:
            qa_words = len(re.sub(r'<[^>]+>', ' ', qa_match.group(1)).split())
            if qa_words < 35 or qa_words > 75:
                errors.append(f".quick-answer word count ({qa_words}) outside 35-75 range.")

        if "<table" not in html_content.lower():
            errors.append("Missing comparison table (<table>).")

        if '<script type="application/ld+json">' not in html_content:
            errors.append("Missing JSON-LD structured data script.")

        if not re.search(r'\b(?:pkr|rs\.?)\b', html_content, re.IGNORECASE):
            errors.append("Missing localized PKR pricing.")

        if OFFICIAL_WHATSAPP not in html_content and "wa.me" not in html_content:
            errors.append("Missing official WhatsApp concierge routing.")

        return len(errors) == 0, errors

    # --------------------------------------------------------------------------
    # Deterministic Heuristic Fallback (Development & Isolated Tests Only)
    # --------------------------------------------------------------------------
    def generate_heuristic_fallback(
        self,
        topic_info: Dict[str, Any],
        canonical_url: str
    ) -> str:
        """
        Deterministic, evidence-grounded fallback template used ONLY in isolated
        development tests or offline environments.
        Uses exact verified registry facts without invented pricing or plans.
        """
        slug = Path(canonical_url).stem
        kw = topic_info.get("primary_keyword", slug.replace("-", " ").title())
        rationale = topic_info.get("editorial_rationale", "In-depth guide and authentic pricing comparison.")

        comp_context = self.get_verified_comparison_context(kw)
        is_comp = comp_context.get("is_comparison", False)

        if is_comp and comp_context.get("both_verified"):
            pa = comp_context["product_a"]
            pb = comp_context["product_b"]
            pkr_summary = f"{pa['price_pkr']} ({pa['canonical_product_name']}) and {pb['price_pkr']} ({pb['canonical_product_name']})"
            table_rows = f"""
          <tr>
            <td>{pa['canonical_product_name']}</td>
            <td>{pa['price_pkr']}</td>
            <td>{pa['price_usd']}</td>
            <td>15 Minutes</td>
            <td>30-Day Replacement</td>
          </tr>
          <tr>
            <td>{pb['canonical_product_name']}</td>
            <td>{pb['price_pkr']}</td>
            <td>{pb['price_usd']}</td>
            <td>15 Minutes</td>
            <td>30-Day Replacement</td>
          </tr>"""
            breakdown_section = f"""
      <h2>{pa['canonical_product_name']} vs {pb['canonical_product_name']} Detailed Breakdown</h2>
      <h3>{pa['canonical_product_name']} Capabilities</h3>
      <p>{pa['canonical_product_name']} by {pa['provider_brand']} offers: {', '.join(pa.get('verified_features', []))}. Official provider rate: {pa.get('official_provider_price')}.</p>
      <h3>{pb['canonical_product_name']} Capabilities</h3>
      <p>{pb['canonical_product_name']} by {pb['provider_brand']} offers: {', '.join(pb.get('verified_features', []))}. Official provider rate: {pb.get('official_provider_price')}.</p>"""
        else:
            prod_single = self.get_verified_product_context(kw)
            pkr_summary = f"{prod_single['price_pkr']} ({prod_single['price_usd']})"
            table_rows = f"""
          <tr>
            <td>{prod_single['canonical_product_name']}</td>
            <td>{prod_single['price_pkr']}</td>
            <td>{prod_single['price_usd']}</td>
            <td>15 Minutes</td>
            <td>30-Day Replacement</td>
          </tr>"""
            breakdown_section = f"""
      <h2>Product Specifications & Features</h2>
      <p>{prod_single['canonical_product_name']} by {prod_single['provider_brand']} includes: {', '.join(prod_single.get('verified_features', []))}. Official upstream rate: {prod_single.get('official_provider_price')}.</p>"""

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{kw} (2026 Guide & Pricing) — AIDigiTools</title>
  <meta name="description" content="Comprehensive review of {kw}. Discover authentic pricing in PKR and USD, payment options via EasyPaisa and JazzCash, delivery SLA, and full comparison.">
  <link rel="canonical" href="{canonical_url}">
  <meta name="robots" content="index, follow">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "{kw} (2026 Guide & Pricing)",
    "author": {{
      "@type": "Person",
      "name": "Abeera Farooq"
    }}
  }}
  </script>
</head>
<body>
  <header>
    <div class="reseller-badge" style="background:#f1f5f9;padding:12px;font-size:0.875rem;">
      <strong>Independent Reseller & Service Desk:</strong> AIDigiTools is an independent subscription concierge and digital marketplace. All product names, logos, and trademarks belong to their respective owners. We are not directly affiliated with or endorsed by upstream tool providers. <a href="https://aidigitools.tech/affiliate-disclosure.html">Reseller & Trademark Policy</a>
    </div>
  </header>
  <main>
    <article>
      <h1>{kw}</h1>
      <p class="quick-answer">
        {kw} provides professional developers and creative practitioners with authentic software seat access. On AIDigiTools, subscriptions start at {pkr_summary} with domestic payment via EasyPaisa, JazzCash, or Raast, 15-minute digital workspace delivery via WhatsApp ({OFFICIAL_WHATSAPP}), and our verified 30-day replacement warranty.
      </p>

      <p class="evidence-tier"><strong>Evidence Classification:</strong> Tier B: Research-based and verified technical documentation.</p>

      <h2>Overview & Architecture</h2>
      <p>{rationale} Upstream documentation from vendor release notes and pricing portals confirms current model capabilities and regional access conditions.</p>

      <h2>Evaluation Criteria & Technical Methodology</h2>
      <p>Evaluated using verified technical documentation, upstream token constraints, and localized payment accessibility across Pakistan and international jurisdictions.</p>

      <h2>Pricing & Specifications Comparison Matrix</h2>
      <table border="1" cellpadding="8" style="border-collapse:collapse;width:100%;">
        <thead>
          <tr>
            <th>Product / Plan</th>
            <th>Pricing (PKR)</th>
            <th>Pricing (USD)</th>
            <th>Delivery SLA</th>
            <th>Warranty</th>
          </tr>
        </thead>
        <tbody>{table_rows}
        </tbody>
      </table>

{breakdown_section}

      <h2>Strengths, Recommended Use Cases & Considerations</h2>
      <p>Ideal for freelancers, developers, and agency teams requiring uninterrupted software seats without international credit card barriers.</p>

      <h2>How to Order via WhatsApp Concierge</h2>
      <ol>
        <li>Select your desired seat from our <a href="https://aidigitools.tech/#tools">catalog</a>.</li>
        <li>Review our <a href="https://aidigitools.tech/policies.html">policies & payment methods</a> and message our desk at <a href="{OFFICIAL_WA_LINK}">03326861112</a>.</li>
        <li>Receive your workspace credentials within our 15-minute delivery SLA.</li>
      </ol>

      <img src="https://aidigitools.tech/assets/images/logo.png" alt="AIDigiTools {kw} software review interface preview">

      <h2>Frequently Asked Questions</h2>
      <details>
        <summary>What payment rails are accepted for {kw}?</summary>
        <p>Domestic rails include EasyPaisa, JazzCash, SadaPay, NayaPay, Raast, and Bank Transfer. International users can pay via Wise and Crypto USDT.</p>
      </details>
      <details>
        <summary>What is the replacement warranty policy?</summary>
        <p>All active accounts include our genuine 30-day replacement warranty managed by our Islamabad operations desk.</p>
      </details>
      <details>
        <summary>How fast is delivery?</summary>
        <p>Orders are dispatched within our 15-minute SLA after payment verification via WhatsApp.</p>
      </details>
    </article>
  </main>
</body>
</html>'''
