import os
import re
import unittest
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestTechnicalSEOCompliance(unittest.TestCase):
    """
    Exhaustive Test Suite for Phase 7 — Technical SEO Compliance.
    Validates all search engine specifications, indexability controls,
    canonical rules, Open Graph, Twitter cards, sitemap, robots.txt,
    semantic HTML, mobile tags, and image attributes.
    """
    @classmethod
    def setUpClass(cls):
        cls.html_files = []
        for root, dirs, files in os.walk(WORKSPACE_DIR):
            if any(p in root for p in [".git", "tests", "scratch"]):
                continue
            for f in files:
                if f.endswith(".html"):
                    cls.html_files.append(os.path.join(root, f))
        cls.html_files.sort()
        assert len(cls.html_files) == 53, f"Expected 53 HTML files, found {len(cls.html_files)}"

    def _read_file(self, fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            return f.read()

    def test_01_canonical_tags_presence_and_format(self):
        """Every page must have a canonical tag using https://aidigitools.tech/."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content, re.I)
            if not match:
                match = re.search(r'<link\s+href=["\']([^"\']+)["\']\s+rel=["\']canonical["\']', content, re.I)
            self.assertIsNotNone(match, f"Missing canonical tag in {rel}")
            canon_url = match.group(1)
            self.assertTrue(canon_url.startswith("https://aidigitools.tech/"),
                            f"Canonical in {rel} does not start with https://aidigitools.tech/: {canon_url}")

    def test_02_strict_rule_no_unrelated_canonical_points_to_homepage(self):
        """CRITICAL: Do not use canonical tags to point unrelated pages to the homepage."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content, re.I)
            if not match:
                match = re.search(r'<link\s+href=["\']([^"\']+)["\']\s+rel=["\']canonical["\']', content, re.I)
            canon_url = match.group(1)
            if canon_url in ["https://aidigitools.tech/", "https://aidigitools.tech/index.html"]:
                self.assertEqual(rel, "index.html",
                                 f"VIOLATION: Unrelated page {rel} points canonical to homepage ({canon_url})")

    def test_03_canonical_self_referencing_integrity(self):
        """Every canonical tag must self-reference the exact page URL."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content, re.I)
            if not match:
                match = re.search(r'<link\s+href=["\']([^"\']+)["\']\s+rel=["\']canonical["\']', content, re.I)
            canon_url = match.group(1)
            if rel == "index.html":
                self.assertIn(canon_url, ["https://aidigitools.tech/", "https://aidigitools.tech/index.html"])
            else:
                expected = f"https://aidigitools.tech/{rel}"
                self.assertEqual(canon_url, expected, f"Mismatched canonical in {rel}: expected {expected}, got {canon_url}")

    def test_04_robots_meta_tags_indexability_controls(self):
        """Content pages must have index, follow; 404 must have noindex, follow."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            match = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)["\']', content, re.I)
            self.assertIsNotNone(match, f"Missing robots meta tag in {rel}")
            robots_val = match.group(1).lower()
            if rel == "404.html":
                self.assertIn("noindex", robots_val, f"404.html must have noindex, got: {robots_val}")
                self.assertIn("follow", robots_val, f"404.html must have follow, got: {robots_val}")
            else:
                self.assertIn("index", robots_val, f"Content page {rel} must have index, got: {robots_val}")
                self.assertIn("follow", robots_val, f"Content page {rel} must have follow, got: {robots_val}")
                self.assertNotIn("noindex", robots_val, f"Content page {rel} must NOT have noindex, got: {robots_val}")

    def test_05_single_primary_h1_per_page(self):
        """Every page must have exactly one primary <h1> heading."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.I | re.S)
            self.assertEqual(len(h1s), 1, f"Page {rel} has {len(h1s)} <h1> tags; expected exactly 1")

    def test_06_unique_titles_across_all_pages(self):
        """All 53 pages must have unique titles with reasonable lengths."""
        titles = {}
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            match = re.search(r'<title>([^<]+)</title>', content, re.I)
            self.assertIsNotNone(match, f"Missing title in {rel}")
            title = match.group(1).strip()
            self.assertGreaterEqual(len(title), 20, f"Title too short in {rel}: '{title}'")
            self.assertLessEqual(len(title), 85, f"Title too long in {rel}: '{title}'")
            self.assertNotIn(title, titles, f"Duplicate title found in {rel} and {titles.get(title)}: '{title}'")
            titles[title] = rel
        self.assertEqual(len(titles), 53)

    def test_07_unique_meta_descriptions_across_all_pages(self):
        """All 53 pages must have unique meta descriptions with reasonable lengths."""
        descriptions = {}
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content, re.I)
            self.assertIsNotNone(match, f"Missing meta description in {rel}")
            desc = match.group(1).strip()
            self.assertGreaterEqual(len(desc), 50, f"Meta description too short in {rel}: '{desc}'")
            self.assertLessEqual(len(desc), 180, f"Meta description too long in {rel}: '{desc}'")
            self.assertNotIn(desc, descriptions, f"Duplicate meta description in {rel} and {descriptions.get(desc)}: '{desc}'")
            descriptions[desc] = rel
        self.assertEqual(len(descriptions), 53)

    def test_08_open_graph_metadata_completeness(self):
        """All pages must have complete Open Graph social card tags."""
        required_og = ["og:site_name", "og:type", "og:title", "og:description", "og:url", "og:image"]
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            for prop in required_og:
                self.assertTrue(re.search(rf'<meta\s+property=["\']{prop}["\']\s+content=["\'][^"\']+["\']', content, re.I),
                                f"Missing {prop} in {rel}")

    def test_09_twitter_card_metadata_completeness(self):
        """All pages must have complete Twitter Card tags."""
        required_tw = ["twitter:card", "twitter:site", "twitter:title", "twitter:description", "twitter:image"]
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            for name in required_tw:
                self.assertTrue(re.search(rf'<meta\s+name=["\']{name}["\']\s+content=["\'][^"\']+["\']', content, re.I),
                                f"Missing {name} in {rel}")

    def test_10_image_optimization_and_alt_attributes(self):
        """All images must have non-empty alt, explicit width and height, and loading attribute."""
        total_imgs = 0
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            imgs = re.findall(r'<img\s+([^>]+)>', content, re.I)
            total_imgs += len(imgs)
            for img in imgs:
                # Alt attribute
                self.assertIn('alt=', img, f"Missing alt attribute in {rel}: {img}")
                alt_match = re.search(r'alt=["\']([^"\']*)["\']', img, re.I)
                self.assertIsNotNone(alt_match, f"Invalid alt format in {rel}: {img}")
                self.assertGreater(len(alt_match.group(1).strip()), 2, f"Empty or too short alt text in {rel}: {img}")
                # Width and height
                self.assertIn('width=', img, f"Missing width in {rel}: {img}")
                self.assertIn('height=', img, f"Missing height in {rel}: {img}")
                # Loading attribute
                self.assertIn('loading=', img, f"Missing loading attribute in {rel}: {img}")
        self.assertGreaterEqual(total_imgs, 140, f"Expected at least 140 images, found {total_imgs}")

    def test_11_sitemap_xml_standards_and_coverage(self):
        """Sitemap must be valid XML with exactly 52 indexable URLs, excluding 404."""
        sitemap_path = os.path.join(WORKSPACE_DIR, "sitemap.xml")
        self.assertTrue(os.path.exists(sitemap_path), "sitemap.xml missing from root")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall('.//sm:loc', ns)]
        self.assertEqual(len(urls), 52, f"Expected 52 URLs in sitemap, found {len(urls)}")
        
        # Verify 404 is excluded
        self.assertFalse(any("404" in u for u in urls), "404.html must NOT be in sitemap.xml")
        
        # Verify homepage is included
        self.assertIn("https://aidigitools.tech/", urls, "Homepage missing from sitemap.xml")
        
        # Verify each URL maps to a real file
        for u in urls:
            path = urlparse(u).path.lstrip("/")
            local_file = os.path.join(WORKSPACE_DIR, "index.html") if not path else os.path.join(WORKSPACE_DIR, path.replace("/", "\\"))
            self.assertTrue(os.path.exists(local_file), f"Sitemap URL {u} does not exist on disk at {local_file}")

    def test_12_robots_txt_specifications_and_safety(self):
        """robots.txt must exist, allow main bots & AI bots, specify sitemap, and not block essential paths."""
        robots_path = os.path.join(WORKSPACE_DIR, "robots.txt")
        self.assertTrue(os.path.exists(robots_path), "robots.txt missing from root")
        with open(robots_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Sitemap: https://aidigitools.tech/sitemap.xml", content)
        self.assertIn("User-agent: Googlebot", content)
        self.assertIn("User-agent: Bingbot", content)
        self.assertIn("User-agent: Google-Extended", content)
        self.assertIn("User-agent: GPTBot", content)
        self.assertIn("User-agent: ClaudeBot", content)
        self.assertIn("User-agent: PerplexityBot", content)
        # Ensure it does not disallow css, js, assets, or tools
        for blocked in ["/css", "/js", "/assets", "/tools", "/categories"]:
            self.assertNotIn(f"Disallow: {blocked}", content, f"Robots.txt accidentally blocks {blocked}")

    def test_13_semantic_html_structure(self):
        """Every page must have semantic <header>, <nav>, <main>, and <footer> tags."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            for tag in ["<header", "<nav", "<main", "<footer"]:
                self.assertIn(tag, content, f"Missing semantic {tag} in {rel}")

    def test_14_mobile_viewport_meta_tag(self):
        """Every page must have the responsive viewport meta tag."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            self.assertTrue(
                re.search(r'<meta\s+name=["\']viewport["\']\s+content=["\']width=device-width,\s*initial-scale=1\.0["\']', content, re.I),
                f"Missing or malformed viewport meta tag in {rel}"
            )

    def test_15_language_and_i18n_declaration(self):
        """Every page must explicitly declare lang='en'."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            self.assertTrue(
                re.search(r'<html\s+[^>]*lang=["\']en["\']', content, re.I),
                f"Missing lang='en' in {rel}"
            )

    def test_16_no_query_param_crawl_traps(self):
        """No internal links should have query parameters that could trap crawlers."""
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            hrefs = re.findall(r'href=["\']([^"\']+)["\']', content, re.I)
            for h in hrefs:
                if h.startswith("http") and "aidigitools.tech" not in h:
                    continue
                if h.startswith("mailto:") or h.startswith("tel:") or h.startswith("https://wa.me"):
                    continue
                self.assertNotIn("?page=", h, f"Crawl trap query parameter in {rel}: {h}")
                self.assertNotIn("?sort=", h, f"Crawl trap query parameter in {rel}: {h}")
                self.assertNotIn("?filter=", h, f"Crawl trap query parameter in {rel}: {h}")

    def test_17_cname_and_https_integrity(self):
        """CNAME must be aidigitools.tech and all internal references must use HTTPS."""
        cname_path = os.path.join(WORKSPACE_DIR, "CNAME")
        self.assertTrue(os.path.exists(cname_path), "CNAME file missing")
        with open(cname_path, "r", encoding="utf-8") as f:
            cname = f.read().strip()
        self.assertEqual(cname, "aidigitools.tech")
        
        # Check that no internal canonical or Open Graph tag uses insecure http://aidigitools.tech
        for fpath in self.html_files:
            rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
            content = self._read_file(fpath)
            self.assertNotIn("http://aidigitools.tech", content, f"Insecure HTTP link found in {rel}")

if __name__ == "__main__":
    unittest.main()
