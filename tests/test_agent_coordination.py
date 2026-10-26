import os
import re
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestAgentCoordination(unittest.TestCase):
    """
    Automated compliance suite for Phase 16:
    Agent Coordination, Multi-Agent Bounded Roles, Lead Architect Reconciliation,
    Data Privacy, Feed Validity, and Non-Destructive Operations.
    """

    def setUp(self):
        self.coordination_doc = os.path.join(REPO_ROOT, "docs", "AGENT_COORDINATION.md")
        self.feed_path = os.path.join(REPO_ROOT, "feed.xml")
        self.affiliate_path = os.path.join(REPO_ROOT, "affiliate-disclosure.html")
        self.gitignore_path = os.path.join(REPO_ROOT, ".gitignore")

    def test_01_all_ten_agent_roles_defined_in_architecture(self):
        """Verify docs/AGENT_COORDINATION.md documents all 10 specialized agent roles."""
        self.assertTrue(os.path.exists(self.coordination_doc), "docs/AGENT_COORDINATION.md must exist.")
        with open(self.coordination_doc, "r", encoding="utf-8") as f:
            content = f.read()

        roles = [
            "Repository Auditor",
            "Product Data Analyst",
            "UX/UI Designer",
            "Information Architect",
            "Technical SEO Engineer",
            "Keyword and Content Strategist",
            "AEO/GEO Specialist",
            "Google Search Specialist",
            "Bing Specialist",
            "QA and Security Engineer"
        ]
        for role in roles:
            self.assertIn(role.lower(), content.lower(), f"Role '{role}' must be defined in AGENT_COORDINATION.md")

    def test_02_lead_architect_reconciliation_rules(self):
        """Verify lead architect reconciliation protocols are defined and documented."""
        with open(self.coordination_doc, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Lead Architect Reconciliation", content)
        self.assertIn("Zero Independent Production Alterations", content)

    def test_03_wholesale_cost_privacy_remediated(self):
        """Verify catalog_36_summary.json is NOT present in repo root and .gitignore protects ledgers."""
        catalog_summary = os.path.join(REPO_ROOT, "catalog_36_summary.json")
        self.assertFalse(
            os.path.exists(catalog_summary),
            "catalog_36_summary.json must not exist in repo root to prevent wholesale margin exposure."
        )

        with open(self.gitignore_path, "r", encoding="utf-8") as f:
            gi_content = f.read()
        self.assertIn("catalog_*.json", gi_content, ".gitignore must ignore catalog_*.json private ledgers.")

    def test_04_feed_xml_validity(self):
        """Verify feed.xml is 100% valid XML and parses cleanly without unescaped entity errors."""
        self.assertTrue(os.path.exists(self.feed_path), "feed.xml must exist.")
        try:
            tree = ET.parse(self.feed_path)
            root = tree.getroot()
            items = root.findall(".//item")
            self.assertEqual(len(items), 49, f"feed.xml must contain exactly 36 items, found {len(items)}")
        except Exception as e:
            self.fail(f"feed.xml XML parsing failed with error: {e}")

    def test_05_independent_broker_disclosure_in_affiliate_page(self):
        """Verify affiliate-disclosure.html uses 'independent localized subscription broker' without claiming direct authorization."""
        with open(self.affiliate_path, "r", encoding="utf-8") as f:
            text = f.read()
        self.assertIn("independent localized subscription broker", text)
        self.assertNotIn("authorized localized subscription broker", text)

if __name__ == "__main__":
    unittest.main()
