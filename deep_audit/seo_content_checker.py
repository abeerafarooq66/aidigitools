import re
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any
from .models import AuditIssue

class SeoAndContentAuditor:
    """Audits on-page SEO, heading hierarchy, content thinness/duplication, and pricing consistency."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()
        self.merchant_prices = self._load_merchant_feed_prices()

    def _load_merchant_feed_prices(self) -> Dict[str, str]:
        """Loads product prices from merchant_feed.xml mapped by tool slug."""
        feed_path = self.root / "merchant_feed.xml"
        if not feed_path.exists():
            return {}
        try:
            tree = ET.parse(feed_path)
            root = tree.getroot()
            prices = {}
            for item in root.findall(".//item"):
                link_elem = item.find("link")
                if link_elem is None or not link_elem.text:
                    link_elem = item.find("{http://base.google.com/ns/1.0}link")
                
                price_elem = item.find("{http://base.google.com/ns/1.0}price")
                if link_elem is not None and link_elem.text and price_elem is not None and price_elem.text:
                    url = link_elem.text.strip()
                    slug = url.split("/")[-1].replace(".html", "")
                    # Extract numeric digits
                    raw_price = price_elem.text.strip().replace("PKR", "").strip()
                    prices[slug] = raw_price
            return prices
        except Exception:
            return {}

    def audit_pages(
        self,
        html_files: List[Path],
        sitemap_urls: List[str],
        timestamp: str
    ) -> List[AuditIssue]:
        issues: List[AuditIssue] = []

        seen_titles: Dict[str, List[str]] = {}
        seen_descriptions: Dict[str, List[str]] = {}
        sitemap_set = set(sitemap_urls)

        for p in html_files:
            rel = p.relative_to(self.root).as_posix()
            is_404 = (rel == "404.html")
            is_tool = rel.startswith("tools/")
            is_category = rel.startswith("categories/")
            is_guide = rel.startswith("guides/")

            try:
                content = p.read_text(encoding="utf-8")
            except Exception as e:
                issues.append(AuditIssue(
                    id="FILE_READ_ERROR",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="CRITICAL",
                    confidence="CONFIRMED",
                    evidence=f"Failed to read file: {str(e)}",
                    recommended_fix="Verify file encoding and permissions."
                ))
                continue

            # 1. Title Tag Inspection
            title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            title = title_m.group(1).strip() if title_m else ""
            if not title:
                issues.append(AuditIssue(
                    id="MISSING_TITLE_TAG",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="CRITICAL",
                    confidence="CONFIRMED",
                    evidence=f"No <title> tag found in {rel}.",
                    recommended_fix="Add a unique, descriptive <title> tag between 30 and 65 characters."
                ))
            else:
                if len(title) < 30 or len(title) > 65:
                    issues.append(AuditIssue(
                        id="TITLE_LENGTH_OUT_OF_BOUNDS",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ON_PAGE_SEO",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Title length is {len(title)} characters (expected 30-65): '{title}'.",
                        recommended_fix="Refine title tag to be within 30-65 characters (optimal 50-60 characters)."
                    ))
                seen_titles.setdefault(title, []).append(rel)

            # 2. Meta Description Inspection
            desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', content, re.IGNORECASE | re.DOTALL)
            desc = desc_m.group(2).strip() if desc_m else ""
            if not desc and not is_404:
                issues.append(AuditIssue(
                    id="MISSING_META_DESCRIPTION",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="CRITICAL",
                    confidence="CONFIRMED",
                    evidence=f"Missing meta description tag in {rel}.",
                    recommended_fix="Add a high-utility meta description between 70 and 165 characters."
                ))
            elif desc:
                if (len(desc) < 70 or len(desc) > 165) and not is_404:
                    issues.append(AuditIssue(
                        id="META_DESCRIPTION_LENGTH",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ON_PAGE_SEO",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Meta description length is {len(desc)} characters (expected 70-165).",
                        recommended_fix="Adjust meta description to 70-165 characters (optimal 140-160 characters)."
                    ))
                seen_descriptions.setdefault(desc, []).append(rel)

            # 3. Canonical URL
            canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
            canonical = canon_m.group(1).strip() if canon_m else ""
            if not canonical and not is_404:
                issues.append(AuditIssue(
                    id="MISSING_CANONICAL_TAG",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="ERROR",
                    confidence="CONFIRMED",
                    evidence=f"Missing rel='canonical' link tag in {rel}.",
                    recommended_fix="Add canonical link pointing to full HTTPS URL."
                ))
            elif canonical:
                expected_url = f"https://aidigitools.tech/{rel}"
                if rel == "index.html":
                    expected_url = "https://aidigitools.tech/"
                if canonical != expected_url:
                    issues.append(AuditIssue(
                        id="CANONICAL_URL_MISMATCH",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ON_PAGE_SEO",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Canonical href='{canonical}' does not match expected '{expected_url}'.",
                        recommended_fix="Align canonical link with primary indexable HTTPS URL."
                    ))

            # 4. Heading Structure & Hierarchy
            h1_matches = re.findall(r'<h1\b[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            if len(h1_matches) == 0:
                issues.append(AuditIssue(
                    id="MISSING_H1_HEADING",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="CRITICAL",
                    confidence="CONFIRMED",
                    evidence=f"No <h1> heading found in {rel}.",
                    recommended_fix="Add exactly one clear, descriptive <h1> heading to the page."
                ))
            elif len(h1_matches) > 1:
                issues.append(AuditIssue(
                    id="MULTIPLE_H1_HEADINGS",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="WARNING",
                    confidence="CONFIRMED",
                    evidence=f"Found {len(h1_matches)} <h1> headings in {rel}.",
                    recommended_fix="Consolidate page structure so there is strictly one <h1> per document."
                ))
            else:
                h1_text = re.sub(r'<[^>]+>', '', h1_matches[0]).strip()
                if not h1_text:
                    issues.append(AuditIssue(
                        id="EMPTY_H1_HEADING",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ON_PAGE_SEO",
                        severity="ERROR",
                        confidence="CONFIRMED",
                        evidence=f"The single <h1> in {rel} is empty or whitespace-only.",
                        recommended_fix="Populate <h1> with descriptive topic or entity name."
                    ))

            # 5. Robots Meta Directive
            if not is_404:
                robots_m = re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
                if robots_m:
                    robots_val = robots_m.group(1).lower()
                    if "noindex" in robots_val:
                        issues.append(AuditIssue(
                            id="ACCIDENTAL_NOINDEX",
                            timestamp=timestamp,
                            tested_url=rel,
                            category="ON_PAGE_SEO",
                            severity="CRITICAL",
                            confidence="CONFIRMED",
                            evidence=f"Canonical page contains 'noindex' in meta robots: '{robots_val}'.",
                            recommended_fix="Remove noindex directive to allow search engine indexing."
                        ))

            # 6. Content Quality & Thin Content Guard
            clean_body = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', content, flags=re.IGNORECASE | re.DOTALL)
            text_only = re.sub(r'<[^>]+>', ' ', clean_body)
            words = text_only.split()
            word_count = len(words)

            if word_count < 200 and not is_404:
                issues.append(AuditIssue(
                    id="THIN_CONTENT_WARNING",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="CONTENT_QUALITY",
                    severity="WARNING",
                    confidence="WARNING",
                    evidence=f"Page word count is {word_count} words (threshold: 200).",
                    recommended_fix="Expand page with substantive helpful information, specifications, and workflows."
                ))

            # Quick Answer Block Check on Content Pages
            if is_tool or is_category or is_guide or rel in {"deals.html", "about.html"}:
                qa_m = re.search(r'class=["\'][^"\']*\bquick-answer\b[^"\']*["\'][^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
                if not qa_m:
                    issues.append(AuditIssue(
                        id="MISSING_QUICK_ANSWER_CAPSULE",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="CONTENT_QUALITY",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Missing required .quick-answer capsule block in {rel}.",
                        recommended_fix="Add a 35-70 word .quick-answer summary block directly below the <h1>."
                    ))

            # Tool Page Depth Requirements
            if is_tool:
                # Comparison Table
                if "<table" not in content.lower():
                    issues.append(AuditIssue(
                        id="MISSING_COMPARISON_TABLE",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="CONTENT_QUALITY",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Tool page {rel} lacks a semantic <table> comparison element.",
                        recommended_fix="Add a structured comparison table with pricing, features, and alternatives."
                    ))
                # FAQ Accordion
                if "<details" not in content.lower() and "faq" not in content.lower():
                    issues.append(AuditIssue(
                        id="MISSING_FAQ_SECTION",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="CONTENT_QUALITY",
                        severity="NOTICE",
                        confidence="WARNING",
                        evidence=f"Tool page {rel} lacks visible FAQ details accordions.",
                        recommended_fix="Add a visible FAQ section answering common user questions."
                    ))

            # 7. Pricing Consistency Checks (Tool Pages)
            if is_tool:
                slug = rel.replace("tools/", "").replace(".html", "")
                merchant_price = self.merchant_prices.get(slug)
                
                # Check Schema offer price
                schema_price_m = re.search(r'"price":\s*["\']?(\d+)["\']?', content)
                schema_price = schema_price_m.group(1) if schema_price_m else None

                if merchant_price and schema_price:
                    if merchant_price != schema_price:
                        issues.append(AuditIssue(
                            id="INCONSISTENT_TOOL_PRICING",
                            timestamp=timestamp,
                            tested_url=rel,
                            category="PRICING_CONSISTENCY",
                            severity="ERROR",
                            confidence="CONFIRMED",
                            evidence=f"Price mismatch for {slug}: merchant_feed.xml lists {merchant_price} PKR but schema lists {schema_price} PKR.",
                            recommended_fix="Harmonize pricing between merchant_feed.xml and HTML schema offers."
                        ))

            # 8. Sitemap Coverage Consistency
            canonical_https = f"https://aidigitools.tech/{rel}" if rel != "index.html" else "https://aidigitools.tech/"
            if not is_404 and canonical_https not in sitemap_set:
                issues.append(AuditIssue(
                    id="SITEMAP_MISSING_PAGE",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ON_PAGE_SEO",
                    severity="WARNING",
                    confidence="CONFIRMED",
                    evidence=f"Page {rel} ({canonical_https}) is indexable but not present in sitemap.xml.",
                    recommended_fix="Add canonical page URL to sitemap.xml."
                ))

        # Check for Duplicate Titles Across Distinct Pages
        for title, pages in seen_titles.items():
            if len(pages) > 1:
                issues.append(AuditIssue(
                    id="DUPLICATE_TITLE_TAG",
                    timestamp=timestamp,
                    tested_url=", ".join(pages[:3]),
                    category="ON_PAGE_SEO",
                    severity="ERROR",
                    confidence="CONFIRMED",
                    evidence=f"Identical title '{title}' shared across {len(pages)} pages: {pages}.",
                    recommended_fix="Provide a distinct, unique title tag for each page."
                ))

        # Check for Duplicate Meta Descriptions
        for desc, pages in seen_descriptions.items():
            if len(pages) > 1:
                issues.append(AuditIssue(
                    id="DUPLICATE_META_DESCRIPTION",
                    timestamp=timestamp,
                    tested_url=", ".join(pages[:3]),
                    category="ON_PAGE_SEO",
                    severity="WARNING",
                    confidence="CONFIRMED",
                    evidence=f"Identical meta description shared across {len(pages)} pages: {pages}.",
                    recommended_fix="Provide customized meta descriptions reflecting each page's specific value proposition."
                ))

        return issues
