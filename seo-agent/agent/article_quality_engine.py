"""
AIDigiTools — Article Quality & Structure Engine
Strictly implements Section 8 of Master Architecture Charter:
ARTICLE QUALITY AND STRUCTURE (Pure Python Standard Library — Zero Dependencies)
"""

import re
from typing import Dict, Any, List, Tuple, Optional

class ArticleQualityEngine:
    def __init__(self):
        pass

    def evaluate_article_html(self, html_content: str, target_slug: str, primary_keyword: str) -> Dict[str, Any]:
        """
        Comprehensive audit of an article's HTML structure, semantic tags,
        direct answer capsules, tables, FAQs, disclosures, and anti-filler rules.
        """
        checks = {}
        errors = []
        warnings = []

        # 1. Title Tag (30-65 chars, includes primary keyword & brand)
        title_m = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
        title_text = title_m.group(1).strip() if title_m else ""
        title_len = len(title_text)
        title_has_kw = any(term in title_text.lower() for term in primary_keyword.lower().split()[:2])
        title_has_brand = "aidigitools" in title_text.lower()
        title_valid = 30 <= title_len <= 65 and title_has_kw and title_has_brand
        checks["seo_title"] = {
            "value": title_text,
            "length": title_len,
            "valid": title_valid,
            "has_primary_keyword": title_has_kw,
            "has_brand": title_has_brand
        }
        if not title_valid:
            errors.append(f"Title tag invalid: length {title_len} (target 30-65), has_kw={title_has_kw}, has_brand={title_has_brand}")

        # 2. Meta Description (70-165 chars)
        desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html_content, re.IGNORECASE)
        if not desc_m:
            desc_m = re.search(r'<meta[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']', html_content, re.IGNORECASE)
        meta_desc = desc_m.group(1).strip() if desc_m else ""
        desc_len = len(meta_desc)
        desc_valid = 70 <= desc_len <= 165
        checks["meta_description"] = {
            "value": meta_desc,
            "length": desc_len,
            "valid": desc_valid
        }
        if not desc_valid:
            errors.append(f"Meta description invalid: length {desc_len} (target 70-165)")

        # 3. Canonical Tag
        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', html_content, re.IGNORECASE)
        canon_url = canon_m.group(1).strip() if canon_m else ""
        canon_valid = canon_url.startswith("https://aidigitools.tech/") and target_slug in canon_url
        checks["canonical_url"] = {
            "value": canon_url,
            "valid": canon_valid
        }
        if not canon_valid:
            errors.append(f"Canonical URL missing or malformed: '{canon_url}'")

        # 4. Single H1 Tag
        h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", html_content, re.IGNORECASE | re.DOTALL)
        h1_valid = len(h1_matches) == 1 and len(re.sub(r"<[^>]+>", "", h1_matches[0]).strip()) > 10
        checks["single_h1"] = {
            "count": len(h1_matches),
            "value": re.sub(r"<[^>]+>", "", h1_matches[0]).strip() if h1_matches else "",
            "valid": h1_valid
        }
        if not h1_valid:
            errors.append(f"Heading violation: expected exactly 1 H1, found {len(h1_matches)}")

        # 5. Direct Answer Capsule (.quick-answer, 35-70 words)
        qa_m = re.search(r'<p[^>]*class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</p>', html_content, re.IGNORECASE | re.DOTALL)
        qa_raw = qa_m.group(1).strip() if qa_m else ""
        qa_text = re.sub(r"<[^>]+>", "", qa_raw).strip()
        qa_words = len(qa_text.split())
        qa_valid = qa_m is not None and (35 <= qa_words <= 70)
        checks["quick_answer_capsule"] = {
            "present": qa_m is not None,
            "word_count": qa_words,
            "valid": qa_valid,
            "value": qa_text[:120] + "..." if qa_text else ""
        }
        if not qa_valid:
            errors.append(f"AEO Quick Answer capsule invalid: present={qa_m is not None}, word_count={qa_words} (target 35-70)")

        # 6. Heading Hierarchy (H2 count >= 2)
        h2_matches = re.findall(r"<h2[^>]*>(.*?)</h2>", html_content, re.IGNORECASE | re.DOTALL)
        h3_matches = re.findall(r"<h3[^>]*>(.*?)</h3>", html_content, re.IGNORECASE | re.DOTALL)
        headings_valid = len(h2_matches) >= 2 and all(len(re.sub(r"<[^>]+>", "", h).strip()) > 3 for h in h2_matches)
        checks["heading_hierarchy"] = {
            "h2_count": len(h2_matches),
            "h3_count": len(h3_matches),
            "valid": headings_valid
        }
        if not headings_valid:
            errors.append(f"Heading hierarchy weak: H2 count is {len(h2_matches)} (minimum 2 required)")

        # 7. Comparison Table (<table> with <thead>, <tbody>, <th>, <td>)
        has_table = "<table" in html_content.lower()
        has_thead = "<thead" in html_content.lower()
        has_tbody = "<tbody" in html_content.lower()
        th_count = len(re.findall(r"<th[^>]*>", html_content, re.IGNORECASE))
        td_count = len(re.findall(r"<td[^>]*>", html_content, re.IGNORECASE))
        table_valid = has_table and has_thead and has_tbody and th_count >= 3 and td_count >= 4
        checks["comparison_table"] = {
            "present": has_table,
            "semantic_valid": table_valid,
            "th_count": th_count,
            "td_count": td_count
        }
        if not table_valid:
            errors.append("Comparison table missing or lacks semantic structure (thead/tbody/th/td)")

        # 8. Genuine Pros and Cons / Limitations
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()
        has_pros = "pros" in clean_text or "advantages" in clean_text or "strengths" in clean_text
        has_limitations = "limitations" in clean_text or "cons" in clean_text or "drawbacks" in clean_text
        checks["pros_cons_limitations"] = {
            "has_pros": has_pros,
            "has_limitations": has_limitations,
            "valid": has_pros and has_limitations
        }
        if not (has_pros and has_limitations):
            errors.append(f"Balanced evaluation missing: has_pros={has_pros}, has_limitations={has_limitations}")

        # 9. FAQs (<details><summary> or faq block)
        details_count = len(re.findall(r"<details[^>]*>", html_content, re.IGNORECASE))
        summary_count = len(re.findall(r"<summary[^>]*>", html_content, re.IGNORECASE))
        faqs_valid = details_count >= 3 and details_count == summary_count
        checks["faq_section"] = {
            "faq_count": details_count,
            "valid": faqs_valid
        }
        if not faqs_valid:
            errors.append(f"FAQ section weak: found {details_count} <details> accordions (minimum 3 required)")

        # 10. Contextual Internal Links (>= 3 links)
        links = re.findall(r'href=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        internal_links = [
            l for l in links
            if l.startswith("/") or l.startswith("https://aidigitools.tech")
        ]
        int_valid = len(internal_links) >= 3
        checks["internal_links"] = {
            "count": len(internal_links),
            "valid": int_valid,
            "sample": internal_links[:4]
        }
        if not int_valid:
            errors.append(f"Internal linking insufficient: found {len(internal_links)} links (minimum 3 required)")

        # 11. External Reliable References
        external_links = [
            l for l in links
            if l.startswith("http") and "aidigitools.tech" not in l
        ]
        checks["external_references"] = {
            "count": len(external_links),
            "valid": len(external_links) >= 1
        }
        if len(external_links) == 0:
            warnings.append("No external official documentation references found.")

        # 12. Real Author & Editorial Governance
        has_author = (
            "abeera farooq" in clean_text or
            "editorial director" in clean_text or
            "editorial team" in clean_text
        )
        checks["author_attribution"] = {
            "has_author": has_author,
            "valid": has_author
        }
        if not has_author:
            errors.append("Author attribution missing; must reference real verified editorial author.")

        # 13. Reseller / Commercial Disclosure
        has_reseller_notice = (
            "independent reseller" in clean_text or
            "independent service desk" in clean_text or
            "trademark disclaimer" in clean_text or
            "not directly affiliated" in clean_text
        )
        checks["commercial_disclosure"] = {
            "has_reseller_notice": has_reseller_notice,
            "valid": has_reseller_notice
        }
        if not has_reseller_notice:
            errors.append("Mandatory Independent Reseller Disclosure notice missing.")

        # 14. Anti-Stuffing Guard (Density < 3.5%)
        words = clean_text.split()
        total_words = len(words)
        kw_count = clean_text.count(primary_keyword.lower())
        density = (kw_count * len(primary_keyword.split()) / max(total_words, 1)) * 100
        checks["keyword_density"] = {
            "total_words": total_words,
            "primary_keyword_count": kw_count,
            "density_pct": round(density, 2),
            "valid": density < 3.5 or total_words < 300
        }
        if total_words >= 300 and density >= 3.5:
            errors.append(f"Keyword stuffing alert: density is {density:.2f}% (hard limit 3.5%)")

        passed = len(errors) == 0
        return {
            "target_slug": target_slug,
            "overall_valid": passed,
            "checks": checks,
            "errors": errors,
            "warnings": warnings,
            "quality_grade": "A+" if passed and len(warnings) == 0 else ("A" if passed else "REJECT")
        }

if __name__ == "__main__":
    engine = ArticleQualityEngine()
    sample_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Cursor AI vs GitHub Copilot (2026) — Review | AIDigiTools</title>
    <meta name="description" content="Detailed 2026 comparison of Cursor AI vs GitHub Copilot for developers in Pakistan. Benchmark features, Composer IDE, and PKR pricing with 15m WhatsApp setup.">
    <link rel="canonical" href="https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html">
</head>
<body>
    <header><p class="reseller-notice">AIDigiTools is an independent reseller and digital service desk.</p></header>
    <main>
        <h1>Cursor AI vs GitHub Copilot: 2026 Developer Comparison & Pricing</h1>
        <p class="quick-answer">Cursor AI and GitHub Copilot are industry-leading AI coding assistants. While Copilot provides fast inline code completions as an extension for existing IDEs, Cursor is a dedicated VS Code fork with Composer for multi-file agentic editing. In Pakistan, AIDigiTools provides local PKR settlement for both tools with 15-minute delivery and a 30-day warranty.</p>
        <h2>Key Architectural Differences</h2>
        <p>Cursor indexes entire repositories locally to provide full context reasoning. It builds a semantic map of your code so that multi-file refactoring runs accurately.</p>
        <h3>Composer vs Copilot Workspace</h3>
        <p>Composer allows parallel diff reviews across multiple files in a unified canvas, while Copilot relies heavily on single-file suggestions.</p>
        <h2>Quantitative Specification Comparison</h2>
        <table>
            <thead><tr><th>Plan Feature</th><th>Cursor Pro</th><th>GitHub Copilot</th></tr></thead>
            <tbody>
                <tr><td>Price (PKR)</td><td>Rs. 3,800/mo</td><td>Rs. 1,600/mo</td></tr>
                <tr><td>Primary Model</td><td>Claude 3.5 Sonnet</td><td>GPT-4o</td></tr>
            </tbody>
        </table>
        <h2>Pros and Cons Analysis</h2>
        <p>Cursor pros include deep refactoring. Limitations include a 500 fast-request monthly cap on Claude 3.5 Sonnet.</p>
        <h2>Frequently Asked Questions</h2>
        <details><summary>Is Cursor Pro better than GitHub Copilot?</summary><p>Yes, for multi-file edits.</p></details>
        <details><summary>Can I pay in PKR?</summary><p>Yes, via EasyPaisa or JazzCash on AIDigiTools.</p></details>
        <details><summary>What is the delivery time?</summary><p>Digital activation completes within 15 minutes.</p></details>
        <footer>
            <p>Written by Abeera Farooq, Chief Editorial Director at AIDigiTools.</p>
            <p><a href="/categories/coding.html">Coding Category</a> | <a href="/tools/cursor-pro.html">Cursor Pro Profile</a> | <a href="/tools/github-copilot.html">Copilot Profile</a></p>
            <p><a href="https://docs.cursor.com/">Cursor Official Documentation</a></p>
        </footer>
    </main>
</body>
</html>"""
    res = engine.evaluate_article_html(sample_html, "cursor-ai-vs-github-copilot", "cursor ai vs github copilot")
    print(f"Sample Article Quality Valid: {res['overall_valid']}, Grade: {res['quality_grade']}")
    print(f"Errors: {res['errors']}")
    assert res["overall_valid"]
    print("ArticleQualityEngine self-test PASSED (Zero External Dependencies)!")
