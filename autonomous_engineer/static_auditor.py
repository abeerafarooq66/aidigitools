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

        # 8. Structured Data (JSON-LD)
        schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
        valid_schemas = 0
        for s in schemas:
            try:
                data = json.loads(s.strip())
                valid_schemas += 1
            except Exception as e:
                issues.append({
                    "severity": "CRITICAL",
                    "type": "invalid_json_ld",
                    "msg": f"Malformed JSON-LD schema: {str(e)}"
                })

        # 9. Tool page comparison table check
        if rel_path.startswith("tools/") and "<table" not in content.lower():
            issues.append({
                "severity": "WARNING",
                "type": "missing_comparison_table",
                "msg": f"Tool page {rel_path} lacks a semantic <table> comparison element.",
                "file": rel_path
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
            # Collect links
            hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
            pages[rel] = (anchors, hrefs)

        broken_links = []
        broken_anchors = []

        for source_page, (anchors, hrefs) in pages.items():
            for href in hrefs:
                if href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:")):
                    continue
                if href.startswith("#"):
                    # Local fragment on the same page
                    frag = href[1:]
                    if frag and frag not in anchors:
                        broken_anchors.append({
                            "source": source_page,
                            "target": href,
                            "anchor": frag
                        })
                    continue

                # Relative link
                link_clean = href.split("?")[0].split("#")[0]
                frag = href.split("#")[1] if "#" in href else None
                
                # Resolve relative path
                source_dir = Path(source_page).parent
                target_path = (source_dir / link_clean).resolve()
                try:
                    target_rel = target_path.relative_to(self.root.resolve()).as_posix()
                except ValueError:
                    broken_links.append({"source": source_page, "target": href, "error": "outside root"})
                    continue

                if target_rel not in pages and not (self.root / target_rel).exists():
                    broken_links.append({"source": source_page, "target": href, "resolved": target_rel})
                elif frag:
                    target_anchors = pages.get(target_rel, (set(), []))[0]
                    if frag not in target_anchors:
                        broken_anchors.append({
                            "source": source_page,
                            "target": href,
                            "target_page": target_rel,
                            "anchor": frag
                        })

        return {
            "total_pages_scanned": len(pages),
            "broken_links_count": len(broken_links),
            "broken_anchors_count": len(broken_anchors),
            "broken_links": broken_links,
            "broken_anchors": broken_anchors,
            "passed": (len(broken_links) == 0 and len(broken_anchors) == 0)
        }

    def run_static_audit(self) -> Dict[str, Any]:
        """Runs the complete static audit across all HTML documents, sitemaps, robots.txt, and link graph."""
        html_files = self.get_html_files()
        page_results = [self.audit_single_page(f) for f in html_files]
        sitemap_urls = self.get_sitemap_urls()
        robots_check = self.check_robots_txt()
        link_graph = self.check_link_graph()

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

        # Health score calculation (100 - penalties)
        score = 100
        score -= min(50, critical_count * 10)
        score -= min(30, warning_count * 2)
        score -= min(10, link_graph["broken_links_count"] * 5)
        score -= min(10, link_graph["broken_anchors_count"] * 3)
        score = max(0, score)

        return {
            "pages_scanned": len(html_files),
            "sitemap_urls_count": len(sitemap_urls),
            "missing_from_sitemap": missing_from_sitemap,
            "extra_in_sitemap": extra_in_sitemap,
            "robots_check": robots_check,
            "link_graph": link_graph,
            "health_score": score,
            "critical_count": critical_count,
            "warning_count": warning_count,
            "issues": all_issues,
            "page_results": page_results,
            "passed": (critical_count == 0 and link_graph["passed"] and robots_check["valid"])
        }
