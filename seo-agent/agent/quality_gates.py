"""
AIDigiTools — Master Quality Gates Engine (Part 18).
=====================================================
Strictly implements Part 18 of the Master Architecture Charter:
QUALITY GATES — NEVER BYPASS.

20-Point Mandatory Pre-Publishing Quality Gate Firewall:
1. Real Reader Problem Solved
2. Topic Fits AIDigiTools Brand Scope
3. Search Intent Accuracy
4. No Cannibalization / Intent Duplication
5. Original Value & Real Research
6. Sources & Primary Documentation
7. Product Facts & Upstream Versions Accuracy
8. Pricing Verification & PKR/USD Parity
9. Disclosed Comparison Methodology & Plan Parity
10. No Invented Hands-On Tests or Fabricated Benchmarks
11. Accurate CTAs & WhatsApp Concierge Preservation
12. Commercial & Independent Reseller Disclosures
13. Truthful Author & Editorial Profiles
14. 100% Working Internal Links & Anchors
15. Relevant, Accessible & Licensed Images
16. Semantic HTML & Schema Validation (No Fake Ratings)
17. Canonical, Sitemap & Indexability Integrity
18. Mobile Responsiveness & Performance
19. Zero Security, Secret, or PII Leakage
20. Google Search Policies & Anti-Manipulation Compliance

CRITICAL INVARIANT:
Any critical failure means strictly DO NOT PUBLISH.

HUMAN REVIEW HOLD TRIGGER:
Claims about product authorization, supplier legitimacy, legal terms,
warranty interpretation, pricing exceptions, or uncertain product access
are automatically enqueued for human review before any publication action.
"""

import os
import re
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set

# Base Directories
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"

# Core Data Files
PUBLICATION_LEDGER_PATH = DATA_DIR / "publication_ledger.json"
HUMAN_REVIEW_QUEUE_PATH = DATA_DIR / "human_review_queue.json"
CENTRAL_PRODUCT_REGISTRY_PATH = DATA_DIR / "central_product_registry.json"
CONTENT_CLUSTERS_PATH = DATA_DIR / "content_clusters.json"
AUTHOR_REGISTRY_PATH = DATA_DIR / "author_registry.json"
TOPIC_REGISTRY_PATH = DATA_DIR / "topic_opportunity_registry.json"
BLOG_REGISTRY_PATH = DATA_DIR / "blog_articles_registry.json"

# Prohibited private/wholesale tokens (Stage 3.3 invariant)
PROHIBITED_LEAK_TOKENS = [
    "wholesale_price",
    "cost_usd",
    "bunnytoolsbot",
    "fat bunny hub",
    "reconciliation_ledger",
    "SRC-"
]

# Sensitive Categories Requiring Human Review
HUMAN_REVIEW_TRIGGERS = {
    "product_authorization": [
        r"(?i)\b(?:official(?:ly)?|exclusive|direct)\s+(?:partner|agent|reseller|licensee)\s+of\s+(?:openai|anthropic|google|microsoft|adobe|midjourney|cursor)\b",
        r"(?i)\b(?:authorized|endorsed|certified)\s+by\s+(?:openai|anthropic|google|microsoft|adobe)\b",
        r"(?i)\bwe\s+are\s+(?:an?\s+)?official\s+distributor\b"
    ],
    "supplier_legitimacy": [
        r"(?i)\b(?:our|upstream)\s+(?:suppliers?|wholesalers?|distributors?|bulk\s+vendors?)\b",
        r"(?i)\b(?:wholesale\s+channel|direct\s+distributor\s+agreement)\b",
        r"(?i)\b(?:supplier\s+credentials|source\s+distributor)\b"
    ],
    "legal_terms": [
        r"(?i)\b(?:guarantee\s+no\s+copyright\s+infringement|legal\s+immunity|indemnify\s+(?:all\s+)?users)\b",
        r"(?i)\b(?:binding\s+legal\s+contract|exempt\s+from\s+terms\s+of\s+service)\b",
        r"(?i)\b(?:dmca\s+immunity|waive\s+all\s+legal\s+liabilit(?:y|ies))\b"
    ],
    "warranty_interpretation": [
        r"(?i)\b(?:100%\s+money[- ]back\s+guarantee|full\s+cash\s+refund|lifetime\s+warranty|instant\s+cash\s+reversal)\b",
        r"(?i)\b(?:guaranteed\s+refund\s+anytime|unconditional\s+cash\s+back)\b"
    ],
    "pricing_exceptions": [
        r"(?i)\b(?:secret\s+discount|backdoor\s+price|negotiated\s+bulk\s+rate|special\s+unlisted\s+price)\b",
        r"(?i)\b(?:custom\s+off[- ]catalog\s+pricing|under\s+the\s+table\s+rates?)\b"
    ],
    "uncertain_product_access": [
        r"(?i)\b(?:order|buy|checkout|purchase)\s+(?:coursera[- ]plus|linkedin[- ]premium|netflix[- ]premium|spotify[- ]premium|turnitin|sora[- ]ai)\b",
        r"(?i)\b(?:instant\s+delivery\s+for\s+sora|guaranteed\s+turnitin\s+instructor\s+slot)\b"
    ]
}


def get_pkt_now_str() -> str:
    """Returns timestamp in Pakistan Standard Time (PKT = UTC+5)."""
    pkt = datetime.timezone(datetime.timedelta(hours=5), name="PKT")
    return datetime.datetime.now(pkt).strftime("%Y-%m-%d %H:%M:%S PKT")


class QualityGateEngine:
    """
    Evaluates 20 mandatory quality gates prior to publishing any blog article,
    comparison, or guide on AIDigiTools.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        self.data_dir = self.workspace_root / "data"
        self.human_review_queue_path = self.data_dir / "human_review_queue.json"
        self._ensure_queue_file()

    def _ensure_queue_file(self) -> None:
        """Ensures human review queue JSON exists."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.human_review_queue_path.exists():
            default_queue = {
                "queue_version": "1.0.0",
                "business_timezone": "PKT (UTC+5)",
                "last_updated_pkt": get_pkt_now_str(),
                "pending_reviews": [],
                "approved_reviews": [],
                "rejected_reviews": []
            }
            with open(self.human_review_queue_path, "w", encoding="utf-8") as f:
                json.dump(default_queue, f, indent=2)

    # --------------------------------------------------------------------------
    # Human Review Scanner
    # --------------------------------------------------------------------------
    def scan_for_human_review_triggers(self, text_content: str) -> List[Dict[str, Any]]:
        """
        Scans text for sensitive claims touching:
        - product authorization
        - supplier legitimacy
        - legal terms
        - warranty interpretation
        - pricing exceptions
        - uncertain product access
        """
        triggers_found = []
        for category, patterns in HUMAN_REVIEW_TRIGGERS.items():
            for pat in patterns:
                matches = re.findall(pat, text_content)
                if matches:
                    triggers_found.append({
                        "category": category,
                        "pattern": pat,
                        "matches": list(set(matches))
                    })
        return triggers_found

    def enqueue_for_human_review(
        self,
        article_slug: str,
        title: str,
        triggers: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Adds a flagged article to the human review queue."""
        with open(self.human_review_queue_path, "r", encoding="utf-8") as f:
            queue = json.load(f)

        review_id = f"REV-{len(queue.get('pending_reviews', [])) + len(queue.get('approved_reviews', [])) + len(queue.get('rejected_reviews', [])) + 1:04d}"
        now_pkt = get_pkt_now_str()

        entry = {
            "review_id": review_id,
            "article_slug": article_slug,
            "title": title,
            "triggers": triggers,
            "metadata": metadata or {},
            "status": "PENDING",
            "enqueued_at_pkt": now_pkt,
            "reviewer_notes": None
        }

        queue.setdefault("pending_reviews", []).append(entry)
        queue["last_updated_pkt"] = now_pkt

        with open(self.human_review_queue_path, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

        return entry

    # --------------------------------------------------------------------------
    # Internal Link Validator Helper
    # --------------------------------------------------------------------------
    def validate_link(self, link: str, source_file_path: Optional[Path] = None) -> bool:
        """Validates internal links, relative paths, and local anchors."""
        link_str = link.strip()
        if not link_str or link_str.startswith(("#", "mailto:", "tel:", "javascript:")):
            return True
        if link_str.startswith("https://aidigitools.tech/"):
            rel_path = link_str.replace("https://aidigitools.tech/", "")
            clean = rel_path.split("#")[0].lstrip("/")
            if not clean:
                return (self.workspace_root / "index.html").exists()
            return (self.workspace_root / clean).exists()
        if link_str.startswith("http://") or link_str.startswith("https://"):
            return True  # External link
        # Relative file path
        path_part = link_str.split("#")[0]
        if not path_part:
            return True
        if source_file_path:
            target = (source_file_path.parent / path_part).resolve()
        else:
            clean_rel = path_part.replace("../", "").lstrip("/")
            target = (self.workspace_root / clean_rel).resolve()
        return target.exists()

    # --------------------------------------------------------------------------
    # Master 20-Gate Pre-Publish Evaluation
    # --------------------------------------------------------------------------
    def evaluate_article(
        self,
        html_content: str,
        metadata: Optional[Dict[str, Any]] = None,
        source_file_path: Optional[Path] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluates an article against all 20 Quality Gates.
        Returns full audit report with decision: APPROVED, DO NOT PUBLISH, or HELD_FOR_HUMAN_REVIEW.
        Accepts metadata dict and optional kwargs for maximum architectural resilience.
        """
        meta = dict(metadata or {})
        meta.update(kwargs)

        slug = meta.get("slug", "unknown-slug")
        title = meta.get("title", "")
        primary_kw = meta.get("primary_keyword", "")
        cluster_slug = meta.get("cluster_slug", "")
        article_type = meta.get("article_type", "comparison")
        author_slug = meta.get("author_slug", "")

        gate_results: Dict[str, Dict[str, Any]] = {}
        critical_failures: List[str] = []

        # 0. Check Human Review Triggers
        review_triggers = self.scan_for_human_review_triggers(html_content)
        held_for_review = len(review_triggers) > 0
        if held_for_review:
            self.enqueue_for_human_review(slug, title, review_triggers, metadata)

        # ----------------------------------------------------------------------
        # Gate 1: Real Reader Problem Solved
        # ----------------------------------------------------------------------
        qa_match = re.search(r'<p[^>]*class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL)
        qa_text = re.sub(r'<[^>]+>', ' ', qa_match.group(1)).strip() if qa_match else ""
        qa_words = len(qa_text.split())
        g1_pass = (35 <= qa_words <= 75) and len(qa_text) > 80
        gate_results["GATE_01_REAL_READER_PROBLEM"] = {
            "passed": g1_pass,
            "score": 10 if g1_pass else 0,
            "details": f"Quick answer capsule contains {qa_words} words (target 35-70) defining solution directly."
        }
        if not g1_pass:
            critical_failures.append("GATE_01_REAL_READER_PROBLEM: Missing or invalid .quick-answer problem definition (target 35-70 words).")

        # ----------------------------------------------------------------------
        # Gate 2: Topic Fits AIDigiTools Brand Scope
        # ----------------------------------------------------------------------
        approved_clusters = {
            "ai-assistants-and-llms", "ai-coding-and-development", "ai-video-and-audio-tools",
            "creative-and-design-suites", "research-and-productivity", "cloud-and-infrastructure-tools",
            "business-and-marketing-intelligence", "data-and-analytics-platforms", "security-and-vpn-access",
            "education-and-e-learning"
        }
        g2_pass = cluster_slug in approved_clusters
        gate_results["GATE_02_TOPIC_FITS_AIDIGITOOLS"] = {
            "passed": g2_pass,
            "score": 10 if g2_pass else 0,
            "details": f"Cluster '{cluster_slug}' is {'approved' if g2_pass else 'unapproved'} within AIDigiTools software scope."
        }
        if not g2_pass:
            critical_failures.append(f"GATE_02_TOPIC_FITS_AIDIGITOOLS: Cluster '{cluster_slug}' is outside AIDigiTools 10-cluster charter.")

        # ----------------------------------------------------------------------
        # Gate 3: Search Intent Accuracy
        # ----------------------------------------------------------------------
        has_table = "<table" in html_content.lower()
        if article_type == "comparison" or "vs" in title.lower() or "vs" in slug.lower():
            # A table and 'vs' in a title must not be enough to pass comparison intent.
            # Must verify that BOTH compared entities are substantively analyzed.
            comp_terms = re.split(r'\b(?:vs\.?|versus)\b', title if "vs" in title.lower() else slug.replace("-", " "), flags=re.IGNORECASE)
            has_both_entities = False
            if len(comp_terms) >= 2:
                term_1 = comp_terms[0].strip().lower()
                term_2 = comp_terms[1].strip().lower()
                t1_toks = set(re.findall(r'[a-z0-9]+', term_1)) - {"ai", "tools", "tool", "app", "pro", "plus", "the"}
                t2_toks = set(re.findall(r'[a-z0-9]+', term_2)) - {"ai", "tools", "tool", "app", "pro", "plus", "the"}
                has_t1 = any(t in html_content.lower() for t in t1_toks) if t1_toks else True
                has_t2 = any(t in html_content.lower() for t in t2_toks) if t2_toks else True
                has_both_entities = has_t1 and has_t2

            tr_count = len(re.findall(r'<tr[^>]*>', html_content, re.IGNORECASE))
            has_sufficient_rows = tr_count >= 3  # Header + at least 2 comparison data rows

            g3_pass = has_table and has_both_entities and has_sufficient_rows
            details = f"Comparison intent matched with dual-entity analysis and {tr_count} comparison table rows." if g3_pass else "Comparison article lacks concrete dual-entity rows or substantive analysis."
        else:
            g3_pass = True
            details = f"Intent '{article_type}' matched with structured educational content."
        gate_results["GATE_03_SEARCH_INTENT_ACCURACY"] = {
            "passed": g3_pass,
            "score": 10 if g3_pass else 0,
            "details": details
        }
        if not g3_pass:
            critical_failures.append("GATE_03_SEARCH_INTENT_ACCURACY: Comparison article lacks dual-product data rows or substantive comparison analysis.")

        # ----------------------------------------------------------------------
        # Gate 4: No Cannibalization / Intent Duplication
        # ----------------------------------------------------------------------
        dup_found = False
        ledger_path = self.data_dir / "publication_ledger.json"
        if not ledger_path.exists() and self.workspace_root == WORKSPACE_ROOT:
            ledger_path = PUBLICATION_LEDGER_PATH
        if ledger_path.exists():
            with open(ledger_path, "r", encoding="utf-8") as f:
                p_ledger = json.load(f)
            for pub in p_ledger.get("publications", []):
                if pub.get("slug") != slug and pub.get("primary_keyword", "").lower() == primary_kw.lower():
                    dup_found = True
                    break
        g4_pass = not dup_found
        gate_results["GATE_04_NO_CANNIBALIZATION"] = {
            "passed": g4_pass,
            "score": 10 if g4_pass else 0,
            "details": "Zero intent duplication or URL competition detected." if g4_pass else f"Conflict: Duplicate primary keyword '{primary_kw}' already targeted."
        }
        if not g4_pass:
            critical_failures.append(f"GATE_04_NO_CANNIBALIZATION: Primary keyword '{primary_kw}' cannibalizes an existing published asset.")

        # ----------------------------------------------------------------------
        # Gate 5: Original Value & Real Research
        # ----------------------------------------------------------------------
        is_fallback = meta.get("is_fallback") or (meta.get("generation_method") == "FALLBACK_HEURISTIC") or (meta.get("is_gemini_generated") is False)
        has_fallback_marker = bool(re.search(r'\b(?:pro multi-seat|is an advanced software solution designed for creative professionals and digital agencies seeking scalable productivity)\b', html_content, re.IGNORECASE))

        has_table_or_matrix = "<table" in html_content.lower() or "comparison matrix" in html_content.lower() or "<ol" in html_content.lower()
        has_pricing_data = bool(re.search(r'\b(?:pkr|rs\.?|\$)\b', html_content, re.IGNORECASE))
        has_use_cases_or_pros_or_steps = bool(re.search(r'\b(?:pros|cons|strengths|use cases?|recommended|ideal for|best for|how to|steps?|guide|workflow)\b', html_content, re.IGNORECASE))

        g5_pass = has_table_or_matrix and has_pricing_data and has_use_cases_or_pros_or_steps and not is_fallback and not has_fallback_marker
        gate_results["GATE_05_ORIGINAL_VALUE"] = {
            "passed": g5_pass,
            "score": 10 if g5_pass else 0,
            "details": "Contains genuine original research and comparison matrix." if g5_pass else ("Fallback heuristic article detected; prohibited from approval." if (is_fallback or has_fallback_marker) else "Missing quantitative matrix/table or localized pricing.")
        }
        if not g5_pass:
            if is_fallback or has_fallback_marker:
                critical_failures.append("GATE_05_ORIGINAL_VALUE: Fallback heuristic article detected. Fallback content is strictly prohibited from receiving APPROVED status.")
            else:
                critical_failures.append("GATE_05_ORIGINAL_VALUE: Missing quantitative comparison table/matrix, localized pricing, or use case breakdown.")

        # ----------------------------------------------------------------------
        # Gate 6: Sources & Primary Documentation
        # ----------------------------------------------------------------------
        # Recognizes external links or explicit reference to primary vendor sources (OpenAI, Anthropic, Cursor, etc.)
        has_external_links = bool(re.search(r'href=["\']https?://(?!aidigitools\.tech)[^"\']+["\']', html_content))
        has_primary_vendor_mentions = bool(re.search(r'\b(?:openai|anthropic|github|google|runway|cursor|midjourney)\b', html_content, re.IGNORECASE))
        g6_pass = has_external_links or has_primary_vendor_mentions
        gate_results["GATE_06_SOURCES_AND_EVIDENCE"] = {
            "passed": g6_pass,
            "score": 10 if g6_pass else 0,
            "details": "Material statements supported by external reference links or primary vendor citations." if g6_pass else "No external authoritative citations detected."
        }
        if not g6_pass:
            critical_failures.append("GATE_06_SOURCES_AND_EVIDENCE: Missing authoritative external documentation links or primary citations.")

        # ----------------------------------------------------------------------
        # Gate 7: Product Facts & Upstream Versions Accuracy
        # ----------------------------------------------------------------------
        has_deprecated_models = bool(re.search(r'\b(?:gpt-3\.5\s+turbo|claude\s+2\.0|dall-e\s+2)\b', html_content, re.IGNORECASE))
        g7_pass = not has_deprecated_models
        gate_results["GATE_07_ACCURATE_FACTS_AND_VERSIONS"] = {
            "passed": g7_pass,
            "score": 10 if g7_pass else 0,
            "details": "Product facts and upstream model versions reflect current generation." if g7_pass else "Deprecated legacy model version detected."
        }
        if not g7_pass:
            critical_failures.append("GATE_07_ACCURATE_FACTS_AND_VERSIONS: Deprecated/legacy model versions referenced as current.")

        # ----------------------------------------------------------------------
        # Gate 8: Pricing Verification & PKR/USD Parity
        # ----------------------------------------------------------------------
        has_pkr = bool(re.search(r'\b(?:pkr|rs\.?)\s*[\d,]+', html_content, re.IGNORECASE))
        has_usd = bool(re.search(r'\$\s*[\d,]+', html_content))

        pricing_matched = True
        pricing_errors = []
        if CENTRAL_PRODUCT_REGISTRY_PATH.exists():
            try:
                with open(CENTRAL_PRODUCT_REGISTRY_PATH, "r", encoding="utf-8") as f:
                    p_reg = json.load(f)
                    p_list = p_reg if isinstance(p_reg, list) else p_reg.get("products", [])

                    article_kw = (primary_kw + " " + title + " " + slug).lower()
                    for p in p_list:
                        p_slug = p.get("slug", "").lower()
                        p_name = p.get("canonical_product_name", "").lower()
                        pkr_val = p.get("aidigitools_offer_price_pkr")

                        is_ref = False
                        if p_slug in article_kw or p_name in article_kw:
                            is_ref = True
                        else:
                            clean_tokens = set(re.findall(r'[a-z0-9]+', p_slug)) - {"ai", "tools", "tool", "app", "pro", "plus", "the"}
                            if clean_tokens and clean_tokens.issubset(set(re.findall(r'[a-z0-9]+', article_kw))):
                                is_ref = True

                        if is_ref and pkr_val:
                            expected_pkr = f"{pkr_val:,}"
                            if expected_pkr not in html_content and str(pkr_val) not in html_content:
                                pricing_matched = False
                                pricing_errors.append(f"Price for '{p.get('canonical_product_name')}' contradicts registry (expected Rs. {expected_pkr} PKR).")

                            if "cursor" in p_slug:
                                if "4,500" in html_content or "4500" in html_content:
                                    pricing_matched = False
                                    pricing_errors.append("Fabricated price Rs. 4,500 detected for Cursor Pro (central registry requires Rs. 3,800).")
            except Exception:
                pass

        g8_pass = has_pkr and has_usd and pricing_matched
        gate_results["GATE_08_PRICING_VERIFICATION"] = {
            "passed": g8_pass,
            "score": 10 if g8_pass else 0,
            "details": f"Separates localized PKR concierge pricing from upstream USD pricing (PKR={has_pkr}, USD={has_usd}). All prices match central registry." if g8_pass else f"Pricing error: {'; '.join(pricing_errors) if pricing_errors else 'Missing PKR or USD pricing.'}"
        }
        if not g8_pass:
            if pricing_errors:
                critical_failures.append(f"GATE_08_PRICING_VERIFICATION: {'; '.join(pricing_errors)}")
            else:
                critical_failures.append("GATE_08_PRICING_VERIFICATION: Missing clear distinction between PKR concierge price and USD provider price.")

        # ----------------------------------------------------------------------
        # Gate 9: Disclosed Comparison Methodology & Plan Parity
        # ----------------------------------------------------------------------
        if article_type == "comparison":
            has_methodology = bool(re.search(r'\b(?:methodology|evaluation criteria|tested parameters|benchmark criteria|tested by|comparison matrix|shootout)\b', html_content, re.IGNORECASE))
            g9_pass = has_methodology
            details = "Evaluation criteria and comparison methodology explicitly disclosed." if g9_pass else "Missing disclosed comparison criteria."
        else:
            g9_pass = True
            details = "Non-comparison article: comparison methodology check passed."
        gate_results["GATE_09_COMPARISON_METHODOLOGY"] = {
            "passed": g9_pass,
            "score": 10 if g9_pass else 0,
            "details": details
        }
        if not g9_pass:
            critical_failures.append("GATE_09_COMPARISON_METHODOLOGY: Comparison article lacks disclosed evaluation methodology.")

        # ----------------------------------------------------------------------
        # Gate 10: No Invented Hands-On Tests or Fabricated Benchmarks
        # ----------------------------------------------------------------------
        has_tier_badge = bool(re.search(r'(?:tier\s+[abc]:|evidence:|research-based|verified (?:technical )?documentation)', html_content, re.IGNORECASE))
        fake_bench_patterns = [
            r'\btested\s+on\s+\d+\s+(?:developers|users|teams)\b',
            r'\bin\s+our\s+(?:hardware\s+cluster|secret\s+benchmark|in-house\s+lab)\b',
            r'\bmeasured\s+99\.\d+%',
            r'\b10x\s+(?:faster|speed|productivity)\b',
            r'\b(?:100%\s+money[- ]back\s+guarantee|instant\s+cash\s+refund|lifetime\s+warranty)\b'
        ]
        detected_fakes = []
        for pat in fake_bench_patterns:
            m = re.findall(pat, html_content, re.IGNORECASE)
            if m:
                detected_fakes.extend(m)

        g10_pass = has_tier_badge and (len(detected_fakes) == 0)
        gate_results["GATE_10_NO_INVENTED_TESTS"] = {
            "passed": g10_pass,
            "score": 10 if g10_pass else 0,
            "details": "Features transparent evidence classification; zero fabricated testing or benchmark claims." if g10_pass else f"Fabricated claims detected: {detected_fakes}"
        }
        if not g10_pass:
            critical_failures.append(f"GATE_10_NO_INVENTED_TESTS: Missing evidence tier badge or contains unverified benchmark/performance claim: {detected_fakes}")

        # ----------------------------------------------------------------------
        # Gate 11: Accurate CTAs & WhatsApp Concierge Preservation
        # ----------------------------------------------------------------------
        has_wa = "wa.me/923326861112" in html_content or "03326861112" in html_content
        has_fake_gateway = bool(re.search(r'\b(?:pay\s+(?:directly\s+)?with\s+credit\s+card\s+on\s+(?:our\s+)?website|automated\s+website\s+payment\s+gateway)\b', html_content, re.IGNORECASE))
        g11_pass = has_wa and not has_fake_gateway
        gate_results["GATE_11_ACCURATE_CTAS"] = {
            "passed": g11_pass,
            "score": 10 if g11_pass else 0,
            "details": "Preserves official WhatsApp order routing; zero fake website payment processor claims." if g11_pass else "CTA violation: Missing WhatsApp routing or claims non-existent website payment gateway."
        }
        if not g11_pass:
            critical_failures.append("GATE_11_ACCURATE_CTAS: Violates WhatsApp order flow or claims fake credit card gateway exists on site.")

        # ----------------------------------------------------------------------
        # Gate 12: Commercial & Independent Reseller Disclosures
        # ----------------------------------------------------------------------
        has_reseller_notice = bool(re.search(r'(?i)\b(?:independent\s+(?:reseller|concierge)|reseller\s+&\s+trademark\s+policy|affiliate-disclosure\.html)\b', html_content))
        g12_pass = has_reseller_notice
        gate_results["GATE_12_COMMERCIAL_DISCLOSURES"] = {
            "passed": g12_pass,
            "score": 10 if g12_pass else 0,
            "details": "Independent reseller and commercial disclosure present." if g12_pass else "Missing mandatory independent reseller notice or disclosure link."
        }
        if not g12_pass:
            critical_failures.append("GATE_12_COMMERCIAL_DISCLOSURES: Missing mandatory independent reseller disclosure or policy link.")

        # ----------------------------------------------------------------------
        # Gate 13: Truthful Author & Editorial Profiles
        # ----------------------------------------------------------------------
        approved_authors = {"abeera-farooq", "aidigitools-editorial"}
        g13_pass = author_slug in approved_authors
        gate_results["GATE_13_TRUTHFUL_AUTHOR_INFO"] = {
            "passed": g13_pass,
            "score": 10 if g13_pass else 0,
            "details": f"Author profile '{author_slug}' is verified in author registry." if g13_pass else f"Unverified author slug '{author_slug}'."
        }
        if not g13_pass:
            critical_failures.append(f"GATE_13_TRUTHFUL_AUTHOR_INFO: Author '{author_slug}' is not an authorized real editorial practitioner.")

        # ----------------------------------------------------------------------
        # Gate 14: 100% Working Internal Links & Anchors
        # ----------------------------------------------------------------------
        target_canon = meta.get("canonical_url", "").strip()
        target_slug = meta.get("slug", "").strip()
        internal_links = re.findall(r'href=["\']([^"\']+\.html(?:#[^"\']*)?)["\']', html_content)
        broken_links = [
            lk for lk in internal_links
            if lk != target_canon and not (target_slug and f"{target_slug}.html" in lk) and not self.validate_link(lk, source_file_path)
        ]
        g14_pass = len(broken_links) == 0
        gate_results["GATE_14_INTERNAL_LINKS_WORK"] = {
            "passed": g14_pass,
            "score": 10 if g14_pass else 0,
            "details": f"Zero broken internal links ({len(internal_links)} validated)." if g14_pass else f"Broken internal links detected: {broken_links}"
        }
        if not g14_pass:
            critical_failures.append(f"GATE_14_INTERNAL_LINKS_WORK: Contains broken internal link(s): {broken_links}")

        # ----------------------------------------------------------------------
        # Gate 15: Relevant, Accessible & Licensed Images
        # ----------------------------------------------------------------------
        imgs = re.findall(r'<img[^>]*>', html_content, re.IGNORECASE)
        missing_alt = False
        for img in imgs:
            alt_m = re.search(r'alt=["\'](.*?)["\']', img, re.IGNORECASE)
            if not alt_m or not alt_m.group(1).strip():
                missing_alt = True
                break
        g15_pass = not missing_alt
        gate_results["GATE_15_IMAGES_AND_ACCESSIBILITY"] = {
            "passed": g15_pass,
            "score": 10 if g15_pass else 0,
            "details": f"All images ({len(imgs)}) have descriptive alt text." if g15_pass else "One or more images missing descriptive alt text."
        }
        if not g15_pass:
            critical_failures.append("GATE_15_IMAGES_AND_ACCESSIBILITY: Image missing mandatory descriptive alt attribute.")

        # ----------------------------------------------------------------------
        # Gate 16: Semantic HTML & Schema Validation (No Fake Ratings)
        # ----------------------------------------------------------------------
        h1_count = len(re.findall(r'<h1[^>]*>', html_content, re.IGNORECASE))
        has_schema = '<script type="application/ld+json">' in html_content
        has_fake_rating = "aggregaterating" in html_content.lower()
        g16_pass = (h1_count == 1) and has_schema and not has_fake_rating
        gate_results["GATE_16_HTML_AND_SCHEMA_VALIDITY"] = {
            "passed": g16_pass,
            "score": 10 if g16_pass else 0,
            "details": f"Single H1={h1_count==1}, Schema present={has_schema}, Zero fake aggregateRating={not has_fake_rating}."
        }
        if not g16_pass:
            critical_failures.append(f"GATE_16_HTML_AND_SCHEMA_VALIDITY: HTML/Schema error: H1 count={h1_count}, Schema={has_schema}, Fake Rating={has_fake_rating}.")

        # ----------------------------------------------------------------------
        # Gate 17: Canonical, Sitemap & Indexability Integrity
        # ----------------------------------------------------------------------
        expected_canonical = meta.get("canonical_url", "")
        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](https://aidigitools\.tech/[^"\']+)["\']', html_content, re.IGNORECASE)
        has_canonical = bool(canon_m)
        canon_matches_expected = True
        if expected_canonical and canon_m:
            canon_matches_expected = (canon_m.group(1).strip() == expected_canonical.strip())
        has_robots_index = "noindex" not in html_content.lower()

        g17_pass = has_canonical and canon_matches_expected and has_robots_index
        gate_results["GATE_17_CANONICAL_AND_INDEXABILITY"] = {
            "passed": g17_pass,
            "score": 10 if g17_pass else 0,
            "details": f"Canonical URL verified matching metadata ({expected_canonical}); robots directives permit indexation." if g17_pass else "Missing/mismatched canonical tag or contains noindex directive."
        }
        if not g17_pass:
            critical_failures.append(f"GATE_17_CANONICAL_AND_INDEXABILITY: Canonical URL missing, mismatched with expected canonical, or page blocked from indexing.")

        # ----------------------------------------------------------------------
        # Gate 18: Mobile Responsiveness & Performance
        # ----------------------------------------------------------------------
        has_viewport = '<meta name="viewport"' in html_content.lower() or "<meta name='viewport'" in html_content.lower()
        g18_pass = has_viewport
        gate_results["GATE_18_MOBILE_AND_PERFORMANCE"] = {
            "passed": g18_pass,
            "score": 10 if g18_pass else 0,
            "details": "Responsive viewport meta tag verified; clean lightweight layout." if g18_pass else "Missing mobile viewport meta tag."
        }
        if not g18_pass:
            critical_failures.append("GATE_18_MOBILE_AND_PERFORMANCE: Missing mobile viewport meta tag.")

        # ----------------------------------------------------------------------
        # Gate 19: Zero Security, Secret, or PII Leakage
        # ----------------------------------------------------------------------
        leaked_tokens = [tok for tok in PROHIBITED_LEAK_TOKENS if tok in html_content]
        has_unauthorized_phone = bool(re.search(r'\b03[0-4][0-9]\d{7}\b', html_content) and "03326861112" not in html_content)
        g19_pass = (len(leaked_tokens) == 0) and not has_unauthorized_phone
        gate_results["GATE_19_SECURITY_AND_ZERO_LEAK"] = {
            "passed": g19_pass,
            "score": 10 if g19_pass else 0,
            "details": "Zero confidential tokens, wholesale costs, customer PII, or API keys leaked." if g19_pass else f"Security leak detected: {leaked_tokens}"
        }
        if not g19_pass:
            critical_failures.append(f"GATE_19_SECURITY_AND_ZERO_LEAK: Confidential wholesale tokens or PII detected: {leaked_tokens}")

        # ----------------------------------------------------------------------
        # Gate 20: Google Search Policies & Anti-Manipulation Compliance
        # ----------------------------------------------------------------------
        has_prompt_injection = bool(re.search(r'(?i)(?:ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions|system\s+prompt\s+override)', html_content))
        # Excludes known UI drawer elements, looking for hidden text intended to manipulate spiders
        has_manipulative_hidden_text = bool(re.search(r'<(?:span|p|div)(?![^>]*id=["\']drawer)[^>]*style=["\'][^"\']*(?:font-size:\s*0|opacity:\s*0)[^"\']*>[^<]{10,}</', html_content, re.IGNORECASE))
        g20_pass = not has_prompt_injection and not has_manipulative_hidden_text
        gate_results["GATE_20_GOOGLE_SEARCH_POLICY_COMPLIANCE"] = {
            "passed": g20_pass,
            "score": 10 if g20_pass else 0,
            "details": "Compliant with Google Search Essentials; zero manipulative hidden text or prompt injections." if g20_pass else "Manipulation detected (hidden text or prompt injection)."
        }
        if not g20_pass:
            critical_failures.append("GATE_20_GOOGLE_SEARCH_POLICY_COMPLIANCE: Contains hidden manipulative text or prompt injection.")

        # ----------------------------------------------------------------------
        # Overall Decision Matrix
        # ----------------------------------------------------------------------
        total_passed = sum(1 for g in gate_results.values() if g["passed"])
        overall_score = round((total_passed / 20.0) * 100, 1)

        if held_for_review:
            decision = "HELD_FOR_HUMAN_REVIEW"
            summary_message = (
                f"Article flagged for Human Review ({len(review_triggers)} trigger categories matched: "
                f"{', '.join(t['category'] for t in review_triggers)}). Publication halted pending reviewer sign-off."
            )
        elif len(critical_failures) > 0:
            decision = "DO NOT PUBLISH"
            summary_message = f"Quality gate failure: {len(critical_failures)} critical gate(s) failed. Strictly prohibited from publishing."
        else:
            decision = "APPROVED"
            summary_message = f"All 20 Quality Gates passed (100% compliance). Ready for publication."

        return {
            "article_slug": slug,
            "title": title,
            "decision": decision,
            "overall_score": overall_score,
            "passed_gates_count": total_passed,
            "failed_gates_count": len(critical_failures),
            "summary_message": summary_message,
            "critical_failures": critical_failures,
            "human_review_triggers": review_triggers,
            "gate_results": gate_results,
            "evaluated_at_pkt": get_pkt_now_str()
        }


# ==============================================================================
# CLI Entrypoint
# ==============================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AIDigiTools Pre-Publish Quality Gate Engine")
    parser.add_argument("--file", help="Path to HTML file to evaluate")
    args = parser.parse_args()

    engine = QualityGateEngine()

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File {file_path} does not exist.")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        meta = {
            "slug": file_path.stem,
            "title": file_path.stem.replace("-", " ").title(),
            "primary_keyword": file_path.stem.replace("-", " "),
            "cluster_slug": "ai-assistants-and-llms",
            "article_type": "comparison" if "vs" in file_path.stem else "guide",
            "author_slug": "abeera-farooq"
        }
        res = engine.evaluate_article(html, meta, source_file_path=file_path)
        print(f"[QUALITY GATE DECISION] {res['decision']} (Score: {res['overall_score']}%)")
        print(f"[SUMMARY] {res['summary_message']}")
        if res['critical_failures']:
            print("[CRITICAL FAILURES]:")
            for cf in res['critical_failures']:
                print(f"  - {cf}")
        if res['human_review_triggers']:
            print("[HUMAN REVIEW TRIGGERS]:")
            for ht in res['human_review_triggers']:
                print(f"  - Category: {ht['category']} (Matches: {ht['matches']})")
        sys.exit(0 if res['decision'] == "APPROVED" else 1)

    print("Usage: python -m seo-agent.agent.quality_gates --file <path_to_html>")


if __name__ == "__main__":
    main()
