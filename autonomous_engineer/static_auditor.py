import os
import re
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple
from .config import (
    PROJECT_ROOT, DOMAIN, BASE_URL,
    TITLE_MIN_LEN, TITLE_MAX_LEN,
    DESC_MIN_LEN, DESC_MAX_LEN,
    QUICK_ANSWER_MIN_WORDS, QUICK_ANSWER_MAX_WORDS
)

class StaticAuditor:
    """Exhaustively inspects repository HTML files, sitemaps, robots.txt, schema, and link integrity."""

    def __init__(self, root_dir: Path = PROJECT_ROOT):
        self.root = Path(root_dir)

    def get_html_files(self) -> List[Path]:
        """Discovers all valid HTML files excluding tests, scratch, and git dirs."""
        html_files = []
        for root, dirs, files in os.walk(self.root):
            if any(p in root for p in [".git", "tests", "scratch", ".github"]):
                continue
            for f in files:
                if f.endswith(".html"):
                    html_files.append(Path(root) / f)
        return sorted(html_files)

    def get_sitemap_urls(self) -> List[str]:
        """Parses sitemap.xml and returns all declared URLs."""
        sitemap_path = self.root / "sitemap.xml"
        if not sitemap_path.exists():
            return []
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [elem.text.strip() for elem in root.findall('.//sm:loc', ns) if elem.text]
            return sorted(urls)
        except Exception:
            return []

    def check_robots_txt(self) -> Dict[str, Any]:
        """Verifies presence and correctness of robots.txt directives."""
        robots_path = self.root / "robots.txt"
        if not robots_path.exists():
            return {"exists": False, "valid": False, "error": "robots.txt missing"}
        content = robots_path.read_text(encoding="utf-8")
        has_sitemap = f"Sitemap: {BASE_URL}/sitemap.xml" in content
        has_googlebot = "Googlebot" in content
        has_bingbot = "Bingbot" in content
        has_disallow_crawl_traps = "Disallow: /*?*q=" in content
        
        valid = has_sitemap and has_googlebot and has_bingbot and has_disallow_crawl_traps
        return {
            "exists": True,
            "valid": valid,
            "has_sitemap": has_sitemap,
            "has_googlebot": has_googlebot,
            "has_bingbot": has_bingbot,
            "has_disallow_crawl_traps": has_disallow_crawl_traps,
            "error": None if valid else "robots.txt missing recommended directives"
        }

    def audit_single_page(self, file_path: Path) -> Dict[str, Any]:
        """Performs a comprehensive technical and SEO audit on a single HTML document."""
        rel_path = file_path.relative_to(self.root).as_posix()
        is_404 = (rel_path == "404.html")
        content = file_path.read_text(encoding="utf-8")
        issues = []

        # 1. Title Tag
        title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ""
        if not title:
            issues.append({"severity": "CRITICAL", "type": "missing_title", "msg": "Missing <title> tag"})
        elif not (TITLE_MIN_LEN <= len(title) <= TITLE_MAX_LEN):
            issues.append({
                "severity": "WARNING",
                "type": "title_length",
                "msg": f"Title length {len(title)} outside [{TITLE_MIN_LEN}, {TITLE_MAX_LEN}]"
            })

        # 2. Meta Description
        desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', content, re.IGNORECASE)
        desc = desc_m.group(2).strip() if desc_m else ""
        if not desc:
            issues.append({"severity": "CRITICAL", "type": "missing_meta_description", "msg": "Missing meta description"})
        elif not (DESC_MIN_LEN <= len(desc) <= DESC_MAX_LEN):
            issues.append({
                "severity": "WARNING",
                "type": "desc_length",
                "msg": f"Meta description length {len(desc)} outside [{DESC_MIN_LEN}, {DESC_MAX_LEN}]"
            })

        # 3. Canonical URL
        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
        canonical = canon_m.group(1).strip() if canon_m else ""
        expected_canonical = f"{BASE_URL}/" if rel_path == "index.html" else f"{BASE_URL}/{rel_path}"
        if not canonical:
            issues.append({"severity": "CRITICAL", "type": "missing_canonical", "msg": "Missing canonical URL tag"})
        elif canonical != expected_canonical and not is_404:
            issues.append({
                "severity": "WARNING",
                "type": "canonical_mismatch",
                "msg": f"Canonical mismatch: found '{canonical}', expected '{expected_canonical}'"
            })

        # 4. Viewport Meta
        vp_m = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
        if not (vp_m and "width=device-width" in vp_m.group(1)):
            issues.append({"severity": "CRITICAL", "type": "missing_viewport", "msg": "Missing mobile viewport meta tag"})

        # 5. Single H1
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if len(h1s) != 1:
            issues.append({
                "severity": "CRITICAL",
                "type": "h1_count",
                "msg": f"Expected exactly 1 <h1>, found {len(h1s)}"
            })

        # 6. Quick Answer block (AEO grounding)
        qa_words = 0
        if not is_404:
            qa_m = re.search(r'class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            if qa_m:
                text_clean = re.sub(r'<[^>]+>', ' ', qa_m.group(1)).strip()
                words = text_clean.split()
                qa_words = len(words)
                if not (QUICK_ANSWER_MIN_WORDS <= qa_words <= QUICK_ANSWER_MAX_WORDS):
                    issues.append({
                        "severity": "WARNING",
                        "type": "quick_answer_length",
                        "msg": f"Quick answer word count {qa_words} outside [{QUICK_ANSWER_MIN_WORDS}, {QUICK_ANSWER_MAX_WORDS}]"
                    })
            else:
                issues.append({"severity": "WARNING", "type": "missing_quick_answer", "msg": "Missing .quick-answer capsule"})

        # 7. Images alt text check
        imgs = re.findall(r'<img\s+([^>]+)>', content, re.IGNORECASE)
        for img in imgs:
            alt_m = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
            if not alt_m or len(alt_m.group(1).strip()) < 2:
                issues.append({
                    "severity": "WARNING",
                    "type": "image_alt_missing",
                    "msg": f"Image tag has missing or empty alt attribute: <img {img}>"
                })

        # 8. Structured Data Validation & Claim Verification
        schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
        valid_schemas = 0
        for s in schemas:
            try:
                data = json.loads(s.strip())
                valid_schemas += 1
                # Check for prohibited unverified ratings
                if isinstance(data, dict):
                    if "aggregateRating" in data and not data.get("review"):
                        issues.append({
                            "severity": "CRITICAL",
                            "type": "unverified_aggregate_rating",
                            "msg": f"Prohibited unverified aggregateRating without visible review in {rel_path}"
                        })
                    if data.get("@type") == "Product":
                        offers = data.get("offers", {})
                        if not offers.get("price") or offers.get("priceCurrency") != "PKR":
                            issues.append({
                                "severity": "WARNING",
                                "type": "schema_pricing_incomplete",
                                "msg": f"Product schema missing explicit PKR price in {rel_path}"
                            })
            except Exception as e:
                issues.append({
                    "severity": "CRITICAL",
                    "type": "invalid_json_ld",
                    "msg": f"Malformed JSON-LD schema: {str(e)}"
                })

        # 9. Tool page verification (Pricing, SLA, Warranty, Reseller Disclosure)
        if rel_path.startswith("tools/"):
            if "<table" not in content.lower():
                issues.append({
                    "severity": "WARNING",
                    "type": "missing_comparison_table",
                    "msg": f"Tool page {rel_path} lacks a semantic <table> comparison element.",
                    "file": rel_path
                })
            # Verify explicit PKR and USD pricing
            has_pkr = bool(re.search(r'\b(?:PKR|Rs\.?)\s*[\d,]+', content, re.IGNORECASE))
            has_usd = bool(re.search(r'\$\s*[\d,]+(?:\.\d+)?|\bUSD\b', content, re.IGNORECASE))
            if not (has_pkr and has_usd):
                issues.append({
                    "severity": "WARNING",
                    "type": "pricing_transparency",
                    "msg": f"Tool page {rel_path} must state both PKR and USD pricing figures."
                })
            # Verify Independent Reseller Disclosure
            if "independent" not in content.lower() or "reseller" not in content.lower():
                issues.append({
                    "severity": "WARNING",
                    "type": "reseller_disclosure_missing",
                    "msg": f"Tool page {rel_path} missing independent reseller transparency notice."
                })
            # Check for unsupported claims
            if re.search(r'\b(?:100% free forever|cheapest in the universe|zero risk guarantee 100% profit)\b', content, re.IGNORECASE):
                issues.append({
                    "severity": "WARNING",
                    "type": "unsupported_marketing_claim",
                    "msg": f"Unsupported or inaccurate marketing claim detected in {rel_path}"
                })

        return {
            "file": rel_path,
            "title": title,
            "meta_description": desc,
            "canonical": canonical,
            "h1_count": len(h1s),
            "quick_answer_words": qa_words,
            "json_ld_blocks": len(schemas),
            "valid_json_ld": valid_schemas,
            "issues": issues,
            "passed": (len([i for i in issues if i["severity"] == "CRITICAL"]) == 0)
        }

    def check_link_graph(self) -> Dict[str, Any]:
        """Validates all internal links and fragment anchors across the entire site."""
        html_files = self.get_html_files()
        pages: Dict[str, Tuple[Set[str], List[str]]] = {}
        
        for f in html_files:
            rel = f.relative_to(self.root).as_posix()
            content = f.read_text(encoding="utf-8")
            # Collect anchors (ids)
            anchors = set(re.findall(r'\bid=["\']([^"\']+)["\']', content))
            # Collect links from <a> tags
            hrefs = re.findall(r'<a\b[^>]*?\bhref=["\']([^"\']+)["\']', content, re.IGNORECASE)
            pages[rel] = (anchors, hrefs)

        broken_links = []
        broken_anchors = []
        incoming_map: Dict[str, Set[str]] = {p: set() for p in pages.keys()}

        for source_page, (anchors, hrefs) in pages.items():
            source_dir = Path(source_page).parent
            for href in hrefs:
                if href.startswith(("http://", "https://")):
                    if not (href.startswith("https://aidigitools.tech") or href.startswith("http://aidigitools.tech")):
                        continue
                    href_clean = href.replace("https://aidigitools.tech", "").replace("http://aidigitools.tech", "")
                    if not href_clean:
                        href_clean = "/"
                elif href.startswith(("mailto:", "tel:", "javascript:", "wa.me", "https://wa.me")):
                    continue
                else:
                    href_clean = href

                # Split path and fragment anchor
                if "#" in href_clean:
                    target_path_part, frag = href_clean.split("#", 1)
                else:
                    target_path_part, frag = href_clean, ""

                # Same page anchor link (e.g. #pricing)
                if not target_path_part:
                    target_rel = source_page
                elif target_path_part.startswith("/"):
                    target_rel = target_path_part.lstrip("/")
                    if not target_rel:
                        target_rel = "index.html"
                else:
                    combined = os.path.join(str(source_dir), target_path_part)
                    norm = os.path.normpath(combined).replace("\\", "/")
                    if norm == ".":
                        norm = "index.html"
                    elif norm.startswith("./"):
                        norm = norm[2:]
                    target_rel = norm

                # Clean up query params if present
                target_rel = target_rel.split("?")[0]

                # Check if target_rel exists in known pages
                if target_rel not in pages:
                    alt_rel = target_rel.rstrip("/") + "/index.html" if not target_rel.endswith(".html") else target_rel
                    if alt_rel in pages:
                        target_rel = alt_rel
                    elif (self.root / target_rel).is_file():
                        # Non-HTML static asset (e.g. image, css)
                        continue
                    else:
                        broken_links.append({"source": source_page, "target": href, "resolved": target_rel})
                        continue

                if target_rel in incoming_map and target_rel != source_page:
                    incoming_map[target_rel].add(source_page)

                if frag:
                    target_anchors = pages.get(target_rel, (set(), []))[0]
                    if frag not in target_anchors:
                        broken_anchors.append({
                            "source": source_page,
                            "target": href,
                            "target_page": target_rel,
                            "anchor": frag
                        })

        orphan_pages = [
            p for p, srcs in incoming_map.items()
            if len(srcs) == 0 and p not in ("index.html", "404.html")
        ]

        return {
            "total_pages_scanned": len(pages),
            "broken_links_count": len(broken_links),
            "broken_anchors_count": len(broken_anchors),
            "orphan_pages_count": len(orphan_pages),
            "broken_links": broken_links,
            "broken_anchors": broken_anchors,
            "orphan_pages": orphan_pages,
            "passed": (len(broken_links) == 0 and len(broken_anchors) == 0 and len(orphan_pages) == 0)
        }

    def check_content_uniqueness(self) -> Dict[str, Any]:
        """Detects duplicate titles and identical or near-duplicate body content across pages."""
        html_files = self.get_html_files()
        titles_map: Dict[str, List[str]] = {}
        content_hashes: Dict[str, List[str]] = {}

        for f in html_files:
            rel = f.relative_to(self.root).as_posix()
            content = f.read_text(encoding="utf-8")

            # Title extraction
            m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            t = m.group(1).strip() if m else ""
            if t:
                titles_map.setdefault(t, []).append(rel)

            # Body text simplification
            body_m = re.search(r'<main[^>]*>(.*?)</main>', content, re.IGNORECASE | re.DOTALL)
            main_text = re.sub(r'<[^>]+>', ' ', body_m.group(1) if body_m else content)
            normalized = " ".join(main_text.split())[:500]
            content_hashes.setdefault(normalized, []).append(rel)

        duplicate_titles = [
            {"title": t, "pages": pages}
            for t, pages in titles_map.items() if len(pages) > 1
        ]
        duplicate_content = [
            {"snippet": s[:80], "pages": pages}
            for s, pages in content_hashes.items() if len(pages) > 1 and len(s) > 100
        ]

        return {
            "duplicate_titles_count": len(duplicate_titles),
            "duplicate_titles": duplicate_titles,
            "duplicate_content_count": len(duplicate_content),
            "duplicate_content": duplicate_content,
            "passed": (len(duplicate_titles) == 0 and len(duplicate_content) == 0)
        }

    def calculate_transparent_health_score(
        self,
        critical_count: int,
        warning_count: int,
        broken_links_count: int,
        broken_anchors_count: int,
        orphan_count: int,
        dup_titles_count: int
    ) -> Dict[str, Any]:
        """Calculates transparent website health score based on published deterministic formula."""
        deductions = []
        total_deduction = 0

        if critical_count > 0:
            crit_pen = min(50, critical_count * 15)
            deductions.append({
                "category": "Critical Infrastructure & Errors",
                "points": crit_pen,
                "evidence": f"{critical_count} critical issue(s) detected (e.g., missing titles, broken canonicals, invalid JSON-LD)"
            })
            total_deduction += crit_pen

        if warning_count > 0:
            warn_pen = min(20, warning_count * 1)
            deductions.append({
                "category": "On-Page SEO Warnings",
                "points": warn_pen,
                "evidence": f"{warning_count} warning(s) detected (e.g., quick answer length, title length boundary)"
            })
            total_deduction += warn_pen

        if broken_links_count > 0:
            link_pen = min(15, broken_links_count * 5)
            deductions.append({
                "category": "Broken Internal Links",
                "points": link_pen,
                "evidence": f"{broken_links_count} broken internal link(s)"
            })
            total_deduction += link_pen

        if broken_anchors_count > 0:
            anc_pen = min(10, broken_anchors_count * 3)
            deductions.append({
                "category": "Broken Fragment Anchors",
                "points": anc_pen,
                "evidence": f"{broken_anchors_count} broken fragment anchor(s)"
            })
            total_deduction += anc_pen

        if orphan_count > 0:
            orph_pen = min(10, orphan_count * 3)
            deductions.append({
                "category": "Orphan Pages",
                "points": orph_pen,
                "evidence": f"{orphan_count} orphan page(s) with 0 incoming internal links"
            })
            total_deduction += orph_pen

        if dup_titles_count > 0:
            dup_pen = min(10, dup_titles_count * 3)
            deductions.append({
                "category": "Duplicate Title Tags",
                "points": dup_pen,
                "evidence": f"{dup_titles_count} duplicate title tag collision(s)"
            })
            total_deduction += dup_pen

        final_score = max(0, 100 - total_deduction)

        return {
            "health_score": final_score,
            "formula": "100 - sum(deductions) [bounded 0-100%]",
            "total_deductions": total_deduction,
            "deductions": deductions,
            "passed": (final_score >= 90 and critical_count == 0 and broken_links_count == 0),
            "disclaimer": "The Health Score measures internal technical compliance, crawlability, and code quality. It is NOT an algorithmic ranking factor and does not guarantee Google or Bing indexing, rankings, or organic traffic."
        }

    def run_static_audit(self) -> Dict[str, Any]:
        """Runs the complete static audit across all HTML documents, sitemaps, robots.txt, and link graph."""
        html_files = self.get_html_files()
        page_results = [self.audit_single_page(f) for f in html_files]
        sitemap_urls = self.get_sitemap_urls()
        robots_check = self.check_robots_txt()
        link_graph = self.check_link_graph()
        content_uniqueness = self.check_content_uniqueness()

        # Sitemap coverage check (excluding 404.html)
        expected_sitemap_urls = set(
            f"{BASE_URL}/" if p.relative_to(self.root).as_posix() == "index.html"
            else f"{BASE_URL}/{p.relative_to(self.root).as_posix()}"
            for p in html_files if p.name != "404.html"
        )
        sitemap_set = set(sitemap_urls)
        missing_from_sitemap = list(expected_sitemap_urls - sitemap_set)
        extra_in_sitemap = list(sitemap_set - expected_sitemap_urls)

        # Count total issues
        all_issues = []
        for r in page_results:
            for iss in r["issues"]:
                all_issues.append({"file": r["file"], **iss})

        critical_count = sum(1 for i in all_issues if i["severity"] == "CRITICAL")
        warning_count = sum(1 for i in all_issues if i["severity"] == "WARNING")

        health_breakdown = self.calculate_transparent_health_score(
            critical_count=critical_count,
            warning_count=warning_count,
            broken_links_count=link_graph["broken_links_count"],
            broken_anchors_count=link_graph["broken_anchors_count"],
            orphan_count=link_graph.get("orphan_pages_count", 0),
            dup_titles_count=content_uniqueness.get("duplicate_titles_count", 0)
        )
        score = health_breakdown["health_score"]

        return {
            "pages_scanned": len(html_files),
            "sitemap_urls_count": len(sitemap_urls),
            "missing_from_sitemap": missing_from_sitemap,
            "extra_in_sitemap": extra_in_sitemap,
            "robots_check": robots_check,
            "link_graph": link_graph,
            "content_uniqueness": content_uniqueness,
            "health_score": score,
            "health_breakdown": health_breakdown,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "issues": all_issues,
            "page_results": page_results,
            "passed": (critical_count == 0 and link_graph["passed"] and robots_check["valid"])
        }
