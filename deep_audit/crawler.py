import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Set, Tuple

class DynamicCrawler:
    """Discovers all pages and sitemap entries dynamically without hardcoding assumptions."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()

    def discover_local_html_pages(self) -> List[Path]:
        """Discovers all published HTML pages in the repository dynamically."""
        discovered = []
        ignored_patterns = {".git", ".github", "tests", "scratch", "node_modules", "dist", "build"}
        
        for dirpath, dirnames, filenames in os.walk(self.root):
            # Prune ignored directory trees
            dirnames[:] = [d for d in dirnames if d not in ignored_patterns and not d.startswith(".")]
            for f in filenames:
                if f.endswith(".html"):
                    full_p = Path(dirpath) / f
                    discovered.append(full_p)
                    
        return sorted(discovered)

    def parse_sitemap_urls(self, sitemap_path: Path = None) -> List[str]:
        """Dynamically parses sitemap.xml and returns all declared URLs."""
        target = sitemap_path or (self.root / "sitemap.xml")
        if not target.exists():
            return []
            
        try:
            tree = ET.parse(target)
            root = tree.getroot()
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = []
            for elem in root.findall('.//sm:loc', ns):
                if elem.text and elem.text.strip():
                    urls.append(elem.text.strip())
            return sorted(urls)
        except Exception:
            return []

    def build_link_graph(self, html_files: List[Path]) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
        """
        Builds the directed link graph between all local pages.
        Returns (outbound_graph, inbound_graph).
        """
        outbound: Dict[str, Set[str]] = {}
        inbound: Dict[str, Set[str]] = {}

        for p in html_files:
            rel = p.relative_to(self.root).as_posix()
            outbound[rel] = set()
            if rel not in inbound:
                inbound[rel] = set()

        href_pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\']', re.IGNORECASE)

        for p in html_files:
            src_rel = p.relative_to(self.root).as_posix()
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue

            for m in href_pattern.finditer(content):
                raw_href = m.group(1).strip()
                # Skip external, javascript, mailto, tel
                if raw_href.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#")):
                    continue

                clean_href = raw_href.split("#")[0].split("?")[0]
                if not clean_href:
                    continue

                # Resolve relative path
                if clean_href.startswith("/"):
                    target_rel = clean_href.lstrip("/")
                else:
                    target_rel = (p.parent / clean_href).resolve().relative_to(self.root).as_posix()

                if target_rel.endswith("/") or target_rel == "":
                    target_rel += "index.html"

                outbound[src_rel].add(target_rel)
                if target_rel not in inbound:
                    inbound[target_rel] = set()
                inbound[target_rel].add(src_rel)

        return outbound, inbound

    def find_orphan_pages(self, html_files: List[Path], inbound_graph: Dict[str, Set[str]]) -> List[str]:
        """
        Identifies orphan pages that have 0 incoming internal links from other pages.
        (404.html and index.html are expected root/error pages).
        """
        orphans = []
        for p in html_files:
            rel = p.relative_to(self.root).as_posix()
            if rel in {"index.html", "404.html"}:
                continue
            inbound = inbound_graph.get(rel, set())
            # Filter out self-references
            external_inbound = [src for src in inbound if src != rel]
            if len(external_inbound) == 0:
                orphans.append(rel)
        return sorted(orphans)
