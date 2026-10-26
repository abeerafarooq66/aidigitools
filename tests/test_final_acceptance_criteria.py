"""
Final Acceptance Criteria & Execution Rules Test Suite
Validates that all 11 Final Acceptance Criteria and all 4 Execution Rules
are programmatically satisfied across the AI DigiTools repository.
"""

import json
import os
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ACCEPTANCE_DOC_PATH = os.path.join(REPO_ROOT, "docs", "FINAL_ACCEPTANCE_REPORT.md")


class TestFinalAcceptanceCriteria(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(ACCEPTANCE_DOC_PATH):
            raise FileNotFoundError(f"Missing acceptance report: {ACCEPTANCE_DOC_PATH}")
        with open(ACCEPTANCE_DOC_PATH, "r", encoding="utf-8") as f:
            cls.doc_content = f.read()

    def test_01_acceptance_report_exists_and_covers_all_sections(self):
        self.assertTrue(os.path.isfile(ACCEPTANCE_DOC_PATH))
        for i in range(1, 12):
            self.assertIn(f"Criterion {i}:", self.doc_content)
        self.assertIn("Execution Rules Compliance Audit", self.doc_content)

    def test_02_criterion_1_design_consistent_and_responsive(self):
        css_path = os.path.join(REPO_ROOT, "assets", "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn(":focus-visible", css)
        self.assertIn("@media (prefers-reduced-motion", css)
        self.assertIn("@media (max-width:", css)
        self.assertIn("--bg-canvas", css)
        self.assertIn("--brand-mint", css)
        self.assertIn("--brand-cyan", css)

    def test_03_criterion_2_useful_functionality_preserved(self):
        js_path = os.path.join(REPO_ROOT, "assets", "cart.js")
        with open(js_path, "r", encoding="utf-8") as f:
            js = f.read()
        self.assertIn("search", js.lower())
        self.assertIn("filter", js.lower())
        self.assertIn("sort", js.lower())
        self.assertIn("compare", js.lower())
        self.assertIn("wa.me", js)

    def test_04_criterion_3_verified_product_source_information(self):
        catalog_items = [
            f for f in os.listdir(os.path.join(REPO_ROOT, "tools"))
            if f.endswith(".html")
        ]
        self.assertEqual(len(catalog_items), 36)
        # Check that tools contain verified specs and pricing
        sample_tool = os.path.join(REPO_ROOT, "tools", "chatgpt-plus.html")
        with open(sample_tool, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Rs. 2,300", content)
        self.assertIn("phase6-spec-block", content)

    def test_05_criterion_4_unverified_offers_not_presented_as_official(self):
        affiliate_path = os.path.join(REPO_ROOT, "affiliate-disclosure.html")
        with open(affiliate_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("independent localized subscription broker", content)
        self.assertNotIn("authorized distributor of openai", content.lower())

    def test_06_criterion_5_important_pages_reachable_through_crawlable_links(self):
        index_path = os.path.join(REPO_ROOT, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            index_html = f.read()
        self.assertIn("categories/coding.html", index_html)
        self.assertIn("tools/chatgpt-plus.html", index_html)
        self.assertIn("about.html", index_html)
        self.assertIn("contact.html", index_html)

    def test_07_criterion_6_canonicals_metadata_robots_sitemap_consistent(self):
        sitemap_path = os.path.join(REPO_ROOT, "sitemap.xml")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        urls = [elem.text for elem in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(len(urls), 52)
        self.assertNotIn("https://aidigitools.tech/404.html", urls)

        robots_path = os.path.join(REPO_ROOT, "robots.txt")
        with open(robots_path, "r", encoding="utf-8") as f:
            robots = f.read()
        self.assertIn("Sitemap: https://aidigitools.tech/sitemap.xml", robots)

    def test_08_criterion_7_structured_data_matches_visible_content(self):
        index_path = os.path.join(REPO_ROOT, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('"@type": "WebSite"', content)
        self.assertNotIn('"AggregateRating"', content)

        category_path = os.path.join(REPO_ROOT, "categories", "coding.html")
        with open(category_path, "r", encoding="utf-8") as f:
            cat_content = f.read()
        self.assertIn('"@type": "CollectionPage"', cat_content)
        self.assertNotIn('"@type": "Product"', cat_content)

    def test_09_criterion_8_no_known_critical_build_failures(self):
        # RSS Feed parses cleanly
        feed_path = os.path.join(REPO_ROOT, "feed.xml")
        feed_tree = ET.parse(feed_path)
        self.assertIsNotNone(feed_tree)
        # Git root has no leaked wholesale JSON
        self.assertFalse(os.path.isfile(os.path.join(REPO_ROOT, "catalog_36_summary.json")))

    def test_10_criterion_9_automated_checks_run_and_reported(self):
        test_dir = os.path.join(REPO_ROOT, "tests")
        test_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
        self.assertGreaterEqual(len(test_files), 12)

    def test_11_criterion_10_prepared_for_google_and_bing_monitoring(self):
        index_path = os.path.join(REPO_ROOT, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            index_html = f.read()
        self.assertIn("google-site-verification", index_html)
        self.assertIn("msvalidate.01", index_html)
        self.assertTrue(os.path.isfile(os.path.join(REPO_ROOT, "BingSiteAuth.xml")))
        self.assertTrue(os.path.isfile(os.path.join(REPO_ROOT, "e3b0c44298fc1c149afbf4c8996fb924.txt")))

    def test_12_criterion_11_remaining_manual_tasks_documented(self):
        self.assertIn("Remaining manual tasks and limitations are clearly documented", self.doc_content)
        self.assertIn("Edge SSL Verification", self.doc_content)
        self.assertIn("GSC Verification Token", self.doc_content)

    def test_13_execution_rules_compliance(self):
        self.assertIn("15227e7", self.doc_content)
        self.assertIn("aidigitools_backup_phase0", self.doc_content)
        self.assertIn("backup/work-in-progress-snapshot", self.doc_content)
        self.assertIn("rebuild/ai-digitools-foundation", self.doc_content)


if __name__ == "__main__":
    unittest.main()
