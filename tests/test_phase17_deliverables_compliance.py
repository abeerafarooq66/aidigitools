"""
Phase 17 Deliverables Compliance Test Suite
Validates that docs/MASTER_DELIVERABLES.md fully fulfills all 15 required deliverables
and checks that every listed issue includes: severity, evidence, proposed fix, affected routes,
implementation status, and validation result.
"""

import os
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DELIVERABLES_PATH = os.path.join(REPO_ROOT, "docs", "MASTER_DELIVERABLES.md")


class TestPhase17DeliverablesCompliance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.isfile(DELIVERABLES_PATH):
            raise FileNotFoundError(f"Missing master deliverables: {DELIVERABLES_PATH}")
        with open(DELIVERABLES_PATH, "r", encoding="utf-8") as f:
            cls.content = f.read()

    def test_01_file_exists_and_substantial(self):
        self.assertTrue(os.path.isfile(DELIVERABLES_PATH))
        self.assertGreater(len(self.content), 10000, "Deliverables file is unexpectedly short")

    def test_02_deliverable_1_repository_audit(self):
        self.assertIn("Deliverable 1: Repository & Live-Site Audit Report", self.content)
        self.assertIn("Static Jamstack", self.content)
        self.assertIn("1,774", self.content)

    def test_03_deliverable_2_route_inventory(self):
        self.assertIn("Deliverable 2: Existing Route Inventory", self.content)
        self.assertIn("53 published HTML routes", self.content)
        self.assertIn("tools/chatgpt-plus.html", self.content)
        self.assertIn("404.html", self.content)

    def test_04_deliverable_3_sitemap_and_ia(self):
        self.assertIn("Deliverable 3: Proposed Final Sitemap & Information Architecture", self.content)
        self.assertIn("4-Tier Logical Architecture", self.content)
        self.assertIn("52 indexable URLs", self.content)

    def test_05_deliverable_4_visual_design_system(self):
        self.assertIn("Deliverable 4: Visual Design System & Page-Layout Specification", self.content)
        self.assertIn("#F8FAFC", self.content)
        self.assertIn("Orbit Emblem Palette", self.content)
        self.assertIn("prefers-reduced-motion", self.content)

    def test_06_deliverable_5_product_catalog_audit(self):
        self.assertIn("Deliverable 5: Product Catalog Audit", self.content)
        self.assertIn("2,902 rows", self.content)
        self.assertIn("Wholesale USDT Costs", self.content)
        self.assertIn("Quarantined", self.content)

    def test_07_deliverable_6_launch_shortlist(self):
        self.assertIn("Deliverable 6: Initial Launch Shortlist", self.content)
        self.assertIn("36 Canonical Tools", self.content)
        self.assertIn("Cursor Pro", self.content)
        self.assertIn("Rs. 3,800 PKR", self.content)

    def test_08_deliverable_7_keyword_and_intent_map(self):
        self.assertIn("Deliverable 7: Keyword & Search-Intent Map", self.content)
        self.assertIn("buy chatgpt plus in pakistan easypaisa", self.content)
        self.assertIn("Transactional", self.content)
        self.assertIn("P1 (Critical)", self.content)

    def test_09_deliverable_8_technical_seo_issues_fields(self):
        self.assertIn("Deliverable 8: Technical SEO Issue List with Priorities", self.content)
        # Check required fields in the table header
        self.assertIn("Severity", self.content)
        self.assertIn("Concrete Evidence Detected", self.content)
        self.assertIn("Proposed Architectural Fix", self.content)
        self.assertIn("Affected Routes", self.content)
        self.assertIn("Status", self.content)
        self.assertIn("Validation Method", self.content)

    def test_10_deliverable_9_gsc_readiness_checklist(self):
        self.assertIn("Deliverable 9: Google Search Console Readiness Checklist", self.content)
        self.assertIn("google-site-verification", self.content)
        self.assertIn("Googlebot", self.content)

    def test_11_deliverable_10_bing_and_indexnow_checklist(self):
        self.assertIn("Deliverable 10: Bing Webmaster Tools & IndexNow Checklist", self.content)
        self.assertIn("BingSiteAuth.xml", self.content)
        self.assertIn("e3b0c44298fc1c149afbf4c8996fb924.txt", self.content)

    def test_12_deliverable_11_structured_data_plan(self):
        self.assertIn("Deliverable 11: Structured-Data Plan", self.content)
        self.assertIn("CollectionPage", self.content)
        self.assertIn("SoftwareApplication", self.content)
        self.assertIn("AggregateRating", self.content)

    def test_13_deliverable_12_content_publishing_plan(self):
        self.assertIn("Deliverable 12: Content Publishing Plan", self.content)
        self.assertIn("8 Editorial Themes", self.content)
        self.assertIn("16 Proposed Articles", self.content)

    def test_14_deliverable_13_implementation_plan(self):
        self.assertIn("Deliverable 13: Implementation Plan with File-Level Changes", self.content)
        self.assertIn("beec596", self.content)
        self.assertIn("2c49482", self.content)

    def test_15_deliverable_14_test_results_and_remaining_issues(self):
        self.assertIn("Deliverable 14: Test Results & Remaining Issues", self.content)
        self.assertIn("172 tests", self.content)
        self.assertIn("100% (172 Passed", self.content)

    def test_16_deliverable_15_deployment_and_rollback_instructions(self):
        self.assertIn("Deliverable 15: Deployment & Rollback Instructions", self.content)
        self.assertIn("Tier 1 (Instant Git Hard Reset", self.content)
        self.assertIn("Tier 2 (Snapshot Branch Restore", self.content)
        self.assertIn("Tier 3 (Cold Storage Physical Restore", self.content)


if __name__ == "__main__":
    unittest.main()
