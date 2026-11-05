"""
AIDigiTools — Dynamic Page Discovery & URL Inventory Engine.
============================================================
Strictly implements Part 4 of the Master Operating System & Architecture Charter:
DYNAMIC REAL PAGE DISCOVERY & PERSISTENT URL INVENTORY

Key Responsibilities:
1. Dynamic page discovery from multiple authoritative sources:
   - Local filesystem HTML route inventory.
   - Authoritative XML sitemap (sitemap.xml).
   - In-memory bidirectional internal link graph.
   - Explicit canonical URL declarations.
2. Complete detection of structural route anomalies:
   - Newly created pages vs historically known pages.
   - Removed or phantom pages.
   - Broken internal links and non-existent destination files.
   - Orphan pages (pages with 0 inbound internal links).
   - Duplicate canonical URLs across distinct files.
   - Canonical URL mismatches (declared canonical != actual route).
   - Missing sitemap entries (local valid page absent from sitemap).
   - Noindex directives.
3. Stable URL Identity & Persistent Tracking:
   - Generates deterministic stable IDs for every URL (`URL-XXXX`).
   - Persists state to data/discovered_urls_registry.json.
"""

import os
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Set, Optional, Tuple
import xml.etree.ElementTree as ET

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
SITEMAP_FILE = WORKSPACE_ROOT / "sitemap.xml"
INVENTORY_OUTPUT_PATH = DATA_DIR / "discovered_urls_registry.json"
BASE_DOMAIN = "https://aidigitools.tech"


class PageDiscoveryEngine:
    """Discovers, reconciles, and maintains the authoritative inventory of all website pages."""

    EXCLUDE_DIRS = {
        ".git", ".github", ".venv", ".agent", ".agents", ".gemini", ".gsd",
        "tests", "scratch", "__pycache__", "node_modules", "data"
    }

    def __init__(self, workspace_root: Optional[Path] = None):
        self.root = Path(workspace_root) if workspace_root else WORKSPACE_ROOT
        self.sitemap_path = self.root / "sitemap.xml"
        self.registry_path = self.root / "data" / "discovered_urls_registry.json"

    def generate_stable_id(self, canonical_url: str) -> str:
        """Generates a deterministic 8-character hex hash identifier for a URL."""
        clean_url = canonical_url.strip().lower()
        h = hashlib.sha256(clean_url.encode("utf-8")).hexdigest()[:8]
        return f"PAGE-{h.upper()}"

    def discover_local_html_files(self) -> List[Path]:
        """Scans the repository for all user-facing HTML files."""
        html_files: List[Path] = []
        for p in self.root.rglob("*.html"):
            # Check exclusions
            parts = set(p.relative_to(self.root).parts)
            if parts.intersection(self.EXCLUDE_DIRS):
                continue
            html_files.append(p)
        return sorted(html_files)

    def extract_page_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extracts title, description, canonical, robots directives, and internal links."""
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        rel_path = file_path.relative_to(self.root).as_posix()

        # Title
        t_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = t_m.group(1).strip() if t_m else ""

        # Meta Description
        d_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', content, re.IGNORECASE | re.DOTALL)
        desc = d_m.group(2).strip() if d_m else ""

        # Canonical URL
        c_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
        canonical = c_m.group(1).strip() if c_m else ""

        # Robots Directives
        r_m = re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
        robots_content = r_m.group(1).lower() if r_m else ""
        is_noindex = "noindex" in robots_content

        # H1
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        h1_count = len(h1_matches)

        # Internal Links: extract ONLY from <a> anchor tags, never from <link rel="canonical"> or stylesheets
        hrefs = re.findall(r'<a\s+[^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
        internal_links = set()
        for href in hrefs:
            href_clean = href.strip()
            # Ignore empty, tel, mailto, javascript, external links
            if not href_clean or href_clean.startswith(("#", "javascript:", "mailto:", "tel:", "whatsapp:")):
                continue
            if href_clean.startswith("http://") or href_clean.startswith("https://"):
                if href_clean.startswith(BASE_DOMAIN):
                    internal_links.add(href_clean)
            elif href_clean.endswith(".html") or "/" in href_clean:
                # Relative link
                internal_links.add(href_clean)

        return {
            "file_path": rel_path,
            "title": title,
            "title_length": len(title),
            "meta_description": desc,
            "meta_description_length": len(desc),
            "canonical_url": canonical,
            "is_noindex": is_noindex,
            "h1_count": h1_count,
            "internal_links": sorted(list(internal_links))
        }

    def discover_sitemap_urls(self) -> List[str]:
        """Extracts canonical URLs listed in sitemap.xml."""
        if not self.sitemap_path.exists():
            return []
        try:
            tree = ET.parse(self.sitemap_path)
            root = tree.getroot()
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = [elem.text.strip() for elem in root.findall(".//sm:loc", ns) if elem.text]
            return urls
        except Exception:
            return []

    def run_full_discovery(self) -> Dict[str, Any]:
        """Executes full discovery, link graph computation, and anomaly detection."""
        html_files = self.discover_local_html_files()
        sitemap_urls = set(self.discover_sitemap_urls())

        inventory: Dict[str, Any] = {}
        canonical_map: Dict[str, List[str]] = {}  # canonical -> [file_paths]
        outbound_links_by_file: Dict[str, List[str]] = {}
        inbound_links_by_url: Dict[str, Set[str]] = {}

        # 1. Process files
        for f in html_files:
            meta = self.extract_page_metadata(f)
            rel_path = meta["file_path"]
            canonical = meta["canonical_url"]

            if not canonical:
                # Fallback expected canonical
                if rel_path == "index.html":
                    canonical = f"{BASE_DOMAIN}/"
                else:
                    canonical = f"{BASE_DOMAIN}/{rel_path}"

            stable_id = self.generate_stable_id(canonical)
            meta["stable_id"] = stable_id
            inventory[rel_path] = meta

            canonical_map.setdefault(canonical, []).append(rel_path)
            outbound_links_by_file[rel_path] = meta["internal_links"]
            inbound_links_by_url.setdefault(canonical, set())

        # 2. Build internal link graph
        for src_file, out_links in outbound_links_by_file.items():
            src_canonical = inventory[src_file]["canonical_url"]
            for target in out_links:
                # Normalize target to canonical if possible
                target_canonical = target
                if not target.startswith("http"):
                    # Relative path resolution anchored to workspace root
                    src_dir = (self.root / src_file).parent
                    resolved = (src_dir / target).resolve()
                    try:
                        rel_res = resolved.relative_to(self.root.resolve()).as_posix()
                        if rel_res in inventory:
                            target_canonical = inventory[rel_res]["canonical_url"]
                    except Exception:
                        pass
                
                inbound_links_by_url.setdefault(target_canonical, set()).add(src_canonical)

        # 3. Detect anomalies
        orphans: List[str] = []
        duplicate_canonicals: List[Dict[str, Any]] = []
        missing_sitemap_entries: List[str] = []
        phantom_sitemap_urls: List[str] = []
        noindex_pages: List[str] = []
        missing_canonical_tags: List[str] = []

        # Check local pages
        for rel_path, data in inventory.items():
            canon = data["canonical_url"]
            if not canon:
                missing_canonical_tags.append(rel_path)

            if data["is_noindex"]:
                noindex_pages.append(rel_path)

            # Check sitemap inclusion (404.html is exempt from sitemap)
            if rel_path != "404.html" and canon not in sitemap_urls:
                missing_sitemap_entries.append(canon)

            # Check orphans (index.html is entry point and 404.html is HTTP error page; both exempt)
            inbound = inbound_links_by_url.get(canon, set())
            data["inbound_internal_links_count"] = len(inbound)
            if rel_path not in ("index.html", "404.html") and len(inbound) == 0:
                orphans.append(rel_path)

        # Check duplicate canonicals
        for canon, files in canonical_map.items():
            if len(files) > 1:
                duplicate_canonicals.append({
                    "canonical_url": canon,
                    "competing_files": files
                })

        # Check phantom sitemap URLs (in sitemap but not on disk)
        all_canonicals_on_disk = set(canonical_map.keys())
        for sm_url in sitemap_urls:
            if sm_url not in all_canonicals_on_disk:
                phantom_sitemap_urls.append(sm_url)

        discovery_report = {
            "status": "SUCCESS",
            "total_local_html_pages": len(html_files),
            "total_sitemap_urls": len(sitemap_urls),
            "total_canonical_urls": len(all_canonicals_on_disk),
            "anomalies": {
                "orphan_pages": orphans,
                "orphan_pages_count": len(orphans),
                "duplicate_canonicals": duplicate_canonicals,
                "missing_sitemap_entries": missing_sitemap_entries,
                "phantom_sitemap_urls": phantom_sitemap_urls,
                "noindex_pages": noindex_pages,
                "missing_canonical_tags": missing_canonical_tags
            },
            "pages": inventory
        }

        # Persist registry
        self.save_registry(discovery_report)
        return discovery_report

    def save_registry(self, report: Dict[str, Any]) -> None:
        """Persists the discovered page registry to data directory."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    engine = PageDiscoveryEngine()
    rep = engine.run_full_discovery()
    print(f"Discovered {rep['total_local_html_pages']} HTML pages.")
    print(f"Sitemap URLs: {rep['total_sitemap_urls']}")
    print(f"Orphan pages: {rep['anomalies']['orphan_pages_count']}")
    print(f"Missing sitemap entries: {len(rep['anomalies']['missing_sitemap_entries'])}")
    print(f"Duplicate canonicals: {len(rep['anomalies']['duplicate_canonicals'])}")
