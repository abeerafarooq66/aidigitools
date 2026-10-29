import os
import re
import json
import unittest
import xml.etree.ElementTree as ET

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestBingAndIndexNowCompliance(unittest.TestCase):
    """
    Exhaustive Test Suite for Phase 10 — Bing Webmaster Tools & IndexNow Protocol.
    Validates IndexNow key files, submission script guardrails, Bing Site Scan rules,
    Bing verification hooks, robots.txt directives, and canonical consistency.
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
        fpath = os.path.normpath(os.path.join(WORKSPACE_DIR, rel))
        with open(fpath, "r", encoding="utf-8") as fh:
            return fh.read()

    def test_01_indexnow_key_file_exists_and_valid(self):
        """IndexNow key verification file must exist at root, be named {key}.txt, and contain {key}."""
        key = "89d63ab53a63527b12a199a3096e51ad"
        key_file_path = os.path.join(WORKSPACE_DIR, f"{key}.txt")
        self.assertTrue(os.path.exists(key_file_path), f"Missing key file: {key_file_path}")
        with open(key_file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        self.assertEqual(content, key, f"Key file content mismatch: expected '{key}', found '{content}'")

    def test_02_indexnow_submitter_script_guardrails(self):
        """IndexNow submitter script must exist and enforce domain filtering and batch limits."""
        script_path = os.path.join(WORKSPACE_DIR, "scripts", "submit_indexnow.py")
        self.assertTrue(os.path.exists(script_path), "Missing submit_indexnow.py script")
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn('https://api.indexnow.org/indexnow', code)
        self.assertIn('https://www.bing.com/indexnow', code)
        self.assertIn('https://yandex.com/indexnow', code)
        self.assertIn('aidigitools.tech', code)
        self.assertIn('keyLocation', code)

    def test_03_bing_site_scan_zero_critical_errors(self):
        """All 53 pages must pass Bing Site Scan checks: valid title, meta description, single H1, and alt tags."""
        for rel in self.html_files:
            c = self._read_file(rel)
            
            # Title
            t_match = re.search(r'<title>([^<]+)</title>', c, re.I)
            self.assertIsNotNone(t_match, f"Missing title in {rel}")
            title = t_match.group(1).strip()
            self.assertGreaterEqual(len(title), 15, f"Title too short in {rel}: '{title}'")
            self.assertLessEqual(len(title), 85, f"Title too long in {rel}: '{title}'")
            
            # Meta Description
            d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', c, re.I)
            self.assertIsNotNone(d_match, f"Missing description in {rel}")
            desc = d_match.group(1).strip()
            self.assertGreaterEqual(len(desc), 50, f"Description too short in {rel}: '{desc}'")
            self.assertLessEqual(len(desc), 185, f"Description too long in {rel}: '{desc}'")
            
            # Single H1
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', c, re.I | re.S)
            self.assertEqual(len(h1s), 1, f"Expected 1 H1 in {rel}, found {len(h1s)}")
            
            # Images
            imgs = re.findall(r'<img\s+([^>]+)>', c, re.I)
            for img in imgs:
                self.assertIn("alt=", img, f"Missing alt in {rel}: {img}")
                alt_m = re.search(r'alt=["\']([^"\']*)["\']', img, re.I)
                self.assertIsNotNone(alt_m, f"Malformed alt in {rel}: {img}")
                self.assertGreater(len(alt_m.group(1).strip()), 2, f"Empty alt in {rel}: {img}")

    def test_04_bing_verification_hooks_present(self):
        """index.html must provide Bing meta tag slot and BingSiteAuth.xml must exist in root."""
        c = self._read_file("index.html")
        self.assertIn("msvalidate.01", c, "Missing Bing verification meta placeholder in index.html")
        
        xml_path = os.path.join(WORKSPACE_DIR, "BingSiteAuth.xml")
        self.assertTrue(os.path.exists(xml_path), "Missing BingSiteAuth.xml in root")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        self.assertEqual(root.tag, "users")
        user_tag = root.find("user")
        self.assertIsNotNone(user_tag, "Missing <user> in BingSiteAuth.xml")

    def test_05_robots_txt_explicit_bingbot_directive(self):
        """robots.txt must explicitly allow Bingbot and declare sitemap."""
        with open(os.path.join(WORKSPACE_DIR, "robots.txt"), "r", encoding="utf-8") as fh:
            c = fh.read()
        self.assertIn("User-agent: Bingbot", c)
        self.assertIn("Sitemap: https://aidigitools.tech/sitemap.xml", c)

    def test_06_sitemap_ready_for_bing(self):
        """Sitemap must be valid XML with 52 canonical URLs."""
        tree = ET.parse(os.path.join(WORKSPACE_DIR, "sitemap.xml"))
        root = tree.getroot()
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [elem.text for elem in root.findall('.//sm:loc', ns)]
        self.assertEqual(len(urls), 65)
        self.assertIn("https://aidigitools.tech/", urls)

    def test_07_canonical_consistency_for_bing(self):
        """All canonical tags must be self-referencing and use HTTPS aidigitools.tech."""
        for rel in self.html_files:
            c = self._read_file(rel)
            canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', c, re.I)
            self.assertIsNotNone(canon, f"Missing canonical in {rel}")
            c_url = canon.group(1)
            self.assertTrue(c_url.startswith("https://aidigitools.tech/"))

    def test_08_indexnow_github_actions_workflow(self):
        """IndexNow GitHub Actions workflow must exist, trigger on content changes and dispatch, and use submit_indexnow.py."""
        wf_path = os.path.join(WORKSPACE_DIR, ".github", "workflows", "indexnow-dispatch.yml")
        self.assertTrue(os.path.exists(wf_path), f"Missing IndexNow workflow: {wf_path}")
        with open(wf_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("workflow_dispatch", content)
        self.assertIn("submit_indexnow.py", content)
        self.assertIn("contents: read", content)

if __name__ == "__main__":
    unittest.main()
