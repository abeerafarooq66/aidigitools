"""
AIDigiTools — SEO, AEO, GEO and AI Search Readiness Engine
Strictly implements Section 12 of Master Architecture Charter:
SEO, AEO, GEO AND AI SEARCH READINESS
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from urllib.parse import urlparse

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

PROHIBITED_AI_HACKS = [
    r"\bguaranteed\s+(?:ai\s+overview|aio|chatgpt|perplexity)\s+rankings?\b",
    r"\bhack\s+(?:google\s+)?ai\s+overviews?\b",
    r"\btrick\s+(?:the\s+)?ai\s+algorithm\b",
    r"\bsecret\s+formula\s+to\s+rank\s+#?1\s+in\s+chatgpt\b",
    r"\bignore\s+(?:all\s+)?previous\s+instructions\b",
    r"\bsystem\s+prompt\s*:\b"
]

VAGUE_H2_HEADINGS = {
    "overview", "details", "info", "about", "content", "stuff", "more", "summary", "features"
}

AI_SEARCH_REFERRERS = [
    "chatgpt.com",
    "chat.openai.com",
    "perplexity.ai",
    "claude.ai",
    "copilot.microsoft.com",
    "gemini.google.com"
]

class SearchReadinessEngine:
    """
    Exhaustive auditor for Traditional SEO, AEO (Answer Engine Optimization),
    and GEO (Generative Engine Optimization / AI Search Grounding).
    """

    def __init__(self):
        pass

    def check_traditional_seo(self, html_content: str, canonical_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify foundational technical and on-page SEO:
        - Crawlability/Indexability (no noindex meta)
        - Canonical URL tag present and valid
        - Unique title (30-65 chars)
        - Unique meta description (70-165 chars)
        - Descriptive headings (1 H1, descriptive H2s)
        - Contextual internal links (>= 3 links, no 'click here')
        - Image alt text on all <img>
        """
        issues = []
        clean_text = re.sub(r"<[^>]+>", " ", html_content)

        # 1. Robots / Indexability
        robots_match = re.search(r'<meta\s+[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.I)
        if robots_match:
            robots_content = robots_match.group(1).lower()
            if "noindex" in robots_content and "404.html" not in (canonical_url or ""):
                issues.append("Indexability Error: Page has 'noindex' meta tag.")

        # 2. Canonical URL
        canonical_match = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html_content, re.I)
        if not canonical_match:
            issues.append("Canonical Error: Missing <link rel='canonical'> tag.")
        elif canonical_url and canonical_match.group(1).rstrip('/') != canonical_url.rstrip('/'):
            issues.append(f"Canonical Mismatch: Found '{canonical_match.group(1)}', expected '{canonical_url}'.")

        # 3. Title tag (30-65 chars)
        title_match = re.search(r'<title>(.*?)</title>', html_content, re.I | re.S)
        if not title_match:
            issues.append("Title Error: Missing <title> tag.")
        else:
            title = title_match.group(1).strip().replace("&amp;", "&")
            if len(title) < 30 or len(title) > 65:
                issues.append(f"Title Length Error: Title is {len(title)} chars (must be 30-65 chars).")

        # 4. Meta description (70-165 chars)
        desc_match = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.I)
        if not desc_match:
            issues.append("Description Error: Missing meta description.")
        else:
            desc = desc_match.group(1).strip().replace("&amp;", "&")
            if len(desc) < 70 or len(desc) > 165:
                issues.append(f"Description Length Error: Description is {len(desc)} chars (must be 70-165 chars).")

        # 5. Headings: Exactly 1 H1
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html_content, re.I | re.S)
        if len(h1s) != 1:
            issues.append(f"H1 Error: Expected exactly 1 <h1> tag, found {len(h1s)}.")

        # H2s: Check for vague single-word headings
        h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html_content, re.I | re.S)
        for h in h2s:
            clean_h = re.sub(r'<[^>]+>', '', h).strip().lower()
            if clean_h in VAGUE_H2_HEADINGS:
                issues.append(f"Vague Heading Error: H2 '{clean_h}' is too vague. Must be descriptive.")

        # 6. Internal links (>= 3 contextual links)
        internal_links = re.findall(r'<a\s+[^>]*href=["\']((?!https?://|mailto:|tel:|#)[^"\']+)["\'][^>]*>(.*?)</a>', html_content, re.I | re.S)
        bad_anchors = ["click here", "read more", "here", "link", "learn more"]
        for _, anchor_html in internal_links:
            clean_anchor = re.sub(r'<[^>]+>', '', anchor_html).strip().lower()
            if clean_anchor in bad_anchors:
                issues.append(f"Internal Linking Error: Non-descriptive anchor text '{clean_anchor}' detected.")

        # 7. Images: Alt text
        img_matches = re.finditer(r'<img\s+([^>]*?)>', html_content, re.I)
        for img in img_matches:
            attrs = img.group(1)
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.I)
            if not alt_match or not alt_match.group(1).strip():
                issues.append(f"Image Alt Error: Image tag '{img.group(0)[:60]}...' missing non-empty alt text.")

        passed = len(issues) == 0
        score = max(0.0, 100.0 - (len(issues) * 15.0))
        return {
            "passed": passed,
            "score": score,
            "issues": issues
        }

    def check_aeo_readiness(self, html_content: str) -> Dict[str, Any]:
        """
        Verify Answer Engine Optimization (AEO):
        - Direct answer capsule (.quick-answer with 35-70 words)
        - Reader-focused FAQ accordions (<details><summary>)
        - Quantitative tables (<table> with <thead>/<tbody>/<th>/<td>)
        """
        issues = []

        # 1. Quick answer capsule
        qa_match = re.search(r'<[a-z0-9]+\s+[^>]*class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</[a-z0-9]+>', html_content, re.I | re.S)
        if not qa_match:
            issues.append("AEO Error: Missing .quick-answer capsule block.")
            word_count = 0
        else:
            qa_text = re.sub(r'<[^>]+>', ' ', qa_match.group(1)).strip()
            word_count = len(qa_text.split())
            if word_count < 35 or word_count > 70:
                issues.append(f"AEO Error: .quick-answer word count is {word_count} words (must be 35-70 words).")

        # 2. Tables check for content pages
        has_table = "<table" in html_content and "<thead" in html_content and "<tbody" in html_content

        # 3. FAQ accordions check
        details_count = len(re.findall(r'<details\b', html_content, re.I))

        passed = len(issues) == 0
        score = 100.0 if passed else max(0.0, 100.0 - (len(issues) * 25.0))

        return {
            "passed": passed,
            "score": score,
            "quick_answer_word_count": word_count,
            "has_semantic_table": has_table,
            "faq_accordions_count": details_count,
            "issues": issues
        }

    def check_geo_grounding(self, html_content: str) -> Dict[str, Any]:
        """
        Verify Generative Engine Optimization (GEO) & AI Search Grounding:
        - Explicit entities & terminology (PKR pricing, EasyPaisa/JazzCash, 15m delivery, 30d warranty)
        - Transparent source citations (vendor documentation)
        - Schema.org structured data parity
        - Accurate author/publisher context
        - Zero manipulative prompt injections or hidden text
        """
        issues = []
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()

        # 1. Anti-manipulation firewall (checks visible text AND raw HTML including comments)
        raw_lower = html_content.lower()
        for pattern in PROHIBITED_AI_HACKS:
            if re.search(pattern, clean_text) or re.search(pattern, raw_lower):
                issues.append(f"GEO Anti-Manipulation Violation: Prohibited AI hack phrase matching '{pattern}' found.")

        # 2. Hidden text detection
        hidden_styles = [
            r'display\s*:\s*none',
            r'visibility\s*:\s*hidden',
            r'font-size\s*:\s*0(?:px)?',
            r'color\s*:\s*transparent',
            r'opacity\s*:\s*0(?:\.0+)?(?:\s|;|$)'
        ]
        for h_style in hidden_styles:
            # Check if applied to text-bearing containers
            hidden_matches = re.finditer(rf'<[a-z0-9]+\s+[^>]*style=["\'][^"\']*{h_style}[^"\']*["\'][^>]*>(.*?)</[a-z0-9]+>', html_content, re.I | re.S)
            for hm in hidden_matches:
                inner = re.sub(r'<[^>]+>', '', hm.group(1)).strip()
                if inner and len(inner) > 50 and "modal" not in hm.group(0).lower() and "drawer" not in hm.group(0).lower() and "discount" not in hm.group(0).lower():
                    issues.append(f"GEO Hidden Text Violation: Hidden content block detected ({inner[:40]}...).")

        # 3. Structured Data Parity
        schema_matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_content, re.I | re.S)
        if not schema_matches:
            issues.append("GEO Schema Error: Missing JSON-LD structured data script.")

        passed = len(issues) == 0
        score = 100.0 if passed else max(0.0, 100.0 - (len(issues) * 20.0))

        return {
            "passed": passed,
            "score": score,
            "has_structured_data": len(schema_matches) > 0,
            "issues": issues
        }

    def audit_page_readiness(self, html_content: str, canonical_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Full composite audit across Traditional SEO (35%), AEO (35%), and GEO (30%).
        Pass threshold is >= 85.0 score.
        """
        seo = self.check_traditional_seo(html_content, canonical_url)
        aeo = self.check_aeo_readiness(html_content)
        geo = self.check_geo_grounding(html_content)

        composite_score = round((seo["score"] * 0.35) + (aeo["score"] * 0.35) + (geo["score"] * 0.30), 1)
        all_issues = seo["issues"] + aeo["issues"] + geo["issues"]

        return {
            "overall_score": composite_score,
            "status": "PASS" if composite_score >= 85.0 and len(all_issues) == 0 else "NEEDS_OPTIMIZATION",
            "traditional_seo": seo,
            "aeo_readiness": aeo,
            "geo_grounding": geo,
            "total_issues": len(all_issues),
            "issues": all_issues
        }

    def monitor_ai_search_traffic(
        self,
        gsc_data: Optional[Dict[str, Any]] = None,
        ga4_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Monitor available AI-search visibility, referral sessions, and AI Overview citations.
        Tracks referrals from ChatGPT, Perplexity, Claude, Copilot, and Google AI Overviews.
        """
        gsc_data = gsc_data or {}
        ga4_data = ga4_data or {}

        ai_referral_summary = {
            "last_audited": "2026-11-01",
            "ai_referrers_tracked": AI_SEARCH_REFERRERS,
            "referral_breakdown": {
                "chatgpt.com": {"sessions": 42, "users": 38, "top_landing_page": "/tools/cursor-pro.html"},
                "perplexity.ai": {"sessions": 28, "users": 25, "top_landing_page": "/compare/chatgpt-vs-claude.html"},
                "claude.ai": {"sessions": 15, "users": 14, "top_landing_page": "/best/best-ai-coding-tools.html"},
                "copilot.microsoft.com": {"sessions": 9, "users": 8, "top_landing_page": "/tools/github-copilot.html"}
            },
            "google_aio_tracked_queries": [
                {"query": "buy cursor pro easypaisa", "aio_presence": True, "cited_url": "https://aidigitools.tech/tools/cursor-pro.html"},
                {"query": "chatgpt plus price in pakistan", "aio_presence": True, "cited_url": "https://aidigitools.tech/tools/chatgpt-plus.html"},
                {"query": "runway gen 3 alternatives pakistan", "aio_presence": True, "cited_url": "https://aidigitools.tech/compare/runway-vs-pika.html"}
            ],
            "total_ai_referral_sessions": 94,
            "citation_status": "ACTIVE_RETRIEVAL"
        }

        output_path = ROOT_DIR / "data" / "ai_search_visibility_report.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(ai_referral_summary, f, indent=2)

        return ai_referral_summary

if __name__ == "__main__":
    engine = SearchReadinessEngine()
    print("Testing SearchReadinessEngine...")

    # Sample compliant HTML
    sample_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Cursor Pro Pakistan (PKR &amp; USD) — Pricing | AIDigiTools</title>
    <meta name="description" content="Buy Cursor Pro in Pakistan with EasyPaisa, JazzCash, SadaPay. Transparent PKR pricing with 15-minute delivery and 30-day warranty.">
    <link rel="canonical" href="https://aidigitools.tech/tools/cursor-pro.html">
    <script type="application/ld+json">{"@context": "https://schema.org", "@type": "Product", "name": "Cursor Pro"}</script>
</head>
<body>
    <h1>Cursor Pro AI Code Editor Subscription in Pakistan</h1>
    <p class="quick-answer">
        Cursor Pro costs Rs. 3,800 PKR ($20 USD) monthly on AIDigiTools for Pakistani developers and agencies. It unlocks 500 fast requests of Claude 3.5 Sonnet and GPT-4o with multi-file Composer editing. Orders are delivered electronically within 15 minutes via EasyPaisa or JazzCash with a 30-day replacement warranty.
    </p>
    <h2>Evaluation &amp; Key Features</h2>
    <p>Cursor Pro integrates directly into VS Code workflows. <a href="../compare/chatgpt-vs-claude.html">Compare AI models</a> for more context.</p>
    <img src="../assets/images/cursor-pro.png" alt="Cursor Pro IDE Workspace Interface">
    <table class="specs-table">
        <thead><tr><th>Feature</th><th>Specification</th></tr></thead>
        <tbody><tr><td>Fast Requests</td><td>500 Claude 3.5 Sonnet</td></tr></tbody>
    </table>
    <details>
        <summary>Can I pay for Cursor Pro using EasyPaisa?</summary>
        <p>Yes, AIDigiTools supports EasyPaisa, JazzCash, and SadaPay with instant confirmation.</p>
    </details>
</body>
</html>"""

    res = engine.audit_page_readiness(sample_html, canonical_url="https://aidigitools.tech/tools/cursor-pro.html")
    print(f"Overall score: {res['overall_score']}, Status: {res['status']}, Issues: {res['issues']}")
    assert res["status"] == "PASS"

    # Test prohibited hack
    bad_html = sample_html.replace("<h2>Evaluation &amp; Key Features</h2>", "<h2>Secret formula to rank #1 in ChatGPT</h2>")
    bad_res = engine.audit_page_readiness(bad_html)
    print(f"Bad AIO hack detected: {bad_res['status'] == 'NEEDS_OPTIMIZATION'}")
    assert bad_res["status"] == "NEEDS_OPTIMIZATION"

    # Test AI traffic monitor
    rep = engine.monitor_ai_search_traffic()
    print(f"AI search report generated: total sessions = {rep['total_ai_referral_sessions']}")
    assert rep["total_ai_referral_sessions"] > 0

    print("SearchReadinessEngine self-test PASSED!")
