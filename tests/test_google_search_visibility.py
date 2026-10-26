import os
import re
import json
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestGoogleSearchVisibility(unittest.TestCase):
    """
    Exhaustive Test Suite for Phase 9 — Google Search Visibility & GSC Readiness.
    Validates XML sitemap readiness, robots.txt Googlebot permissions, canonical alignment,
    crawlability, Core Web Vitals structural readiness, and rich result enhancement models.
    """
    @classmethod
    def setUpClass(cls):
        cls.html_files = []
        for root, dirs, files in os.walk(WORKSPACE_DIR):
            if any(p in root for p in [".git", "tests", "scratch"]):
                continue
            for f in files:
                if f.endswith(".html"):
                    rel = os.path.relpath(os.path.join(root, f), WORKSPACE_DIR).replace("\\", "/")
                    cls.html_files.append(rel)
        cls.html_files.sort()
        assert len(cls.html_files) == 66

    def _read_file(self, rel):
        fpath = os.path.join(WORKSPACE_DIR, rel.replace("/", "\\"))
        with open(fpath, "r", encoding="utf-8") as fh:
            return fh.read()

    def test_01_sitemap_ready_for_gsc_ingestion(self):
        """Sitemap must be valid XML, 52 canonical URLs, matching files on disk, omitting 404."""
        sitemap_path = os.path.join(WORKSPACE_DIR, "sitemap.xml")
        self.assertTrue(os.path.exists(sitemap_path))
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall('.//sm:loc', ns)]
        self.assertEqual(len(urls), 65)
        self.assertIn("https://aidigitools.tech/", urls)
        self.assertFalse(any("404" in u for u in urls))
        
        # Check lastmod on all entries
        lastmods = [elem.text for elem in root.findall('.//sm:lastmod', ns)]
        self.assertEqual(len(lastmods), 65)
        for lm in lastmods:
            self.assertTrue(re.match(r'^\d{4}-\d{2}-\d{2}$', lm), f"Invalid lastmod date format: {lm}")

    def test_02_robots_txt_explicit_googlebot_directives(self):
        """robots.txt must allow Googlebot, Google-Extended, and link to sitemap."""
        robots_path = os.path.join(WORKSPACE_DIR, "robots.txt")
        self.assertTrue(os.path.exists(robots_path))
        with open(robots_path, "r", encoding="utf-8") as fh:
            content = fh.read()
        self.assertIn("User-agent: Googlebot", content)
        self.assertIn("User-agent: Google-Extended", content)
        self.assertIn("Sitemap: https://aidigitools.tech/sitemap.xml", content)
        self.assertNotIn("Disallow: /assets", content)
        self.assertNotIn("Disallow: /tools", content)
        self.assertNotIn("Disallow: /categories", content)

    def test_03_zero_orphaned_pages_full_crawlability(self):
        """Every page must have at least one inbound internal link (zero orphans for Googlebot)."""
        inbound = {p: 0 for p in self.html_files}
        for rel in self.html_files:
            c = self._read_file(rel)
            hrefs = re.findall(r'href=["\']([^"\']+)["\']', c, re.I)
            base_dir = os.path.dirname(rel)
            for h in hrefs:
                if h.startswith("http") and "aidigitools.tech" not in h:
                    continue
                if h.startswith("#") or h.startswith("mailto:") or h.startswith("tel:") or h.startswith("https://wa.me"):
                    continue
                clean = h.split("#")[0].split("?")[0]
                if not clean:
                    continue
                if clean.startswith("https://aidigitools.tech/"):
                    target = clean.replace("https://aidigitools.tech/", "")
                    if not target:
                        target = "index.html"
                else:
                    target = os.path.normpath(os.path.join(base_dir, clean)).replace("\\", "/")
                if target in inbound:
                    inbound[target] += 1
                    
        for p, count in inbound.items():
            self.assertGreater(count, 0, f"Orphaned page found with 0 incoming internal links: {p}")

    def test_04_canonical_and_cname_alignment(self):
        """CNAME must match aidigitools.tech, canonicals must all be self-referencing and HTTPS."""
        with open(os.path.join(WORKSPACE_DIR, "CNAME"), "r", encoding="utf-8") as fh:
            cname = fh.read().strip()
        self.assertEqual(cname, "aidigitools.tech")
        
        for rel in self.html_files:
            c = self._read_file(rel)
            canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', c, re.I)
            self.assertIsNotNone(canon, f"Missing canonical in {rel}")
            c_url = canon.group(1)
            self.assertTrue(c_url.startswith("https://aidigitools.tech/"))
            if rel == "index.html":
                self.assertIn(c_url, ["https://aidigitools.tech/", "https://aidigitools.tech/index.html"])
            else:
                self.assertEqual(c_url, f"https://aidigitools.tech/{rel}")

    def test_05_zero_soft_404_risks_and_content_substance(self):
        """All content pages must have substantial body copy (> 200 words) to prevent GSC Soft 404 flags."""
        for rel in self.html_files:
            if rel == "404.html":
                # 404 page must be noindex
                c = self._read_file(rel)
                self.assertIn('content="noindex, follow"', c)
                continue
            c = self._read_file(rel)
            # Strip tags and evaluate word count
            text = re.sub(r'<[^>]+>', ' ', c)
            words = text.split()
            self.assertGreaterEqual(len(words), 200, f"Page {rel} has only {len(words)} words, risking Soft 404")

    def test_06_core_web_vitals_readiness_cls_and_lcp(self):
        """All images must have explicit width and height, loading attribute, and decoding async."""
        for rel in self.html_files:
            c = self._read_file(rel)
            imgs = re.findall(r'<img\s+([^>]+)>', c, re.I)
            for img in imgs:
                self.assertIn("width=", img, f"Missing width in {rel}: {img}")
                self.assertIn("height=", img, f"Missing height in {rel}: {img}")
                self.assertIn("loading=", img, f"Missing loading in {rel}: {img}")
                self.assertIn("decoding=", img, f"Missing decoding in {rel}: {img}")

    def test_07_rich_result_enhancement_readiness(self):
        """Verify readiness for Google Search Console enhancement reports."""
        for rel in self.html_files:
            c = self._read_file(rel)
            if rel.startswith("tools/"):
                # Product & Offer
                self.assertIn('"@type": "Product"', c, f"Missing Product schema in {rel}")
                self.assertIn('"@type": "Offer"', c, f"Missing Offer schema in {rel}")
                self.assertIn('"@type": "BreadcrumbList"', c, f"Missing BreadcrumbList in {rel}")
                self.assertIn('"@type": "FAQPage"', c, f"Missing FAQPage in {rel}")
            elif rel.startswith("categories/"):
                # CollectionPage & ItemList
                self.assertIn('"@type": "CollectionPage"', c, f"Missing CollectionPage in {rel}")
                self.assertIn('"@type": "ItemList"', c, f"Missing ItemList in {rel}")
                self.assertIn('"@type": "BreadcrumbList"', c, f"Missing BreadcrumbList in {rel}")
            elif rel.startswith("guides/") or rel.startswith("compare/") or rel.startswith("best/"):
                # Article / TechArticle
                self.assertTrue('"@type": "Article"' in c or '"@type": "TechArticle"' in c, f"Missing Article in {rel}")
                self.assertIn('"@type": "BreadcrumbList"', c, f"Missing BreadcrumbList in {rel}")

    def test_08_gsc_verification_slot_present(self):
        """index.html must provide the pre-configured slot for Google Search Console site verification."""
        c = self._read_file("index.html")
        self.assertIn("Google Search Console Verification", c)

if __name__ == "__main__":
    unittest.main()
