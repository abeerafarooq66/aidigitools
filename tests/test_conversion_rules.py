"""
Unit tests for Product Conversion & CTA Governance Engine (Section 10 of Master Architecture Charter).
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.conversion_rules import ConversionEngine, HOLD_PRODUCTS, APPROVED_CONTEXTUAL_CTAS

class TestConversionRules(unittest.TestCase):
    def setUp(self):
        self.engine = ConversionEngine()

    def test_approved_contextual_ctas_list(self):
        """Verify standard approved contextual CTAs are defined."""
        expected_ctas = [
            "Explore Full Tool Details",
            "Compare Available Plans",
            "Check Product Availability",
            "View the Relevant Tool Profile",
            "Contact AIDigiTools on WhatsApp"
        ]
        for cta in expected_ctas:
            self.assertIn(cta, APPROVED_CONTEXTUAL_CTAS)

    def test_active_product_cta_generation(self):
        """Active products should generate contextual tool profile link with purchase permitted."""
        cta = self.engine.generate_contextual_cta("cursor-pro")
        self.assertEqual(cta["product_slug"], "cursor-pro")
        self.assertEqual(cta["cta_type"], "CONTEXTUAL_PROFILE")
        self.assertTrue(cta["purchase_permitted"])
        self.assertIn("https://aidigitools.tech/tools/cursor-pro.html", cta["cta_href"])

    def test_hold_product_cta_generation(self):
        """Hold products must generate inquiry-only WhatsApp CTAs with purchase prohibited."""
        for slug in HOLD_PRODUCTS:
            cta = self.engine.generate_contextual_cta(slug)
            self.assertEqual(cta["product_slug"], slug)
            self.assertEqual(cta["cta_type"], "INQUIRY_ONLY")
            self.assertFalse(cta["purchase_permitted"])
            self.assertIn("wa.me/923326861112", cta["cta_href"])
            self.assertIn("inquire", cta["cta_href"].lower())

    def test_prohibited_gateway_claims_detection(self):
        """Articles claiming a website payment gateway must fail conversion validation."""
        bad_html_samples = [
            "<p>You can pay directly with credit card on our website checkout.</p>",
            "<p>Please checkout directly on the website using our payment portal.</p>",
            "<p>We have integrated an automated website payment gateway for all transactions.</p>",
            "<p>Enter your card details at checkout to complete the order.</p>"
        ]
        for bad_html in bad_html_samples:
            valid, violations = self.engine.validate_article_conversion_compliance(bad_html)
            self.assertFalse(valid)
            self.assertTrue(any("Payment Gateway Violation" in v for v in violations))

    def test_hold_product_direct_purchase_block(self):
        """Direct purchase CTAs on hold products in article HTML must be flagged as violations."""
        bad_html = "<p>Ready to get started? <a href='#'>Buy now Coursera Plus</a> at discounted rates!</p>"
        valid, violations = self.engine.validate_article_conversion_compliance(bad_html)
        self.assertFalse(valid)
        self.assertTrue(any("Hold Product Violation" in v for v in violations))

    def test_policy_alignment_delivery_and_warranty(self):
        """Delivery and warranty mentions must align with 15-minute SLA and 30-day replacement warranty."""
        # Missing 15-minute SLA
        bad_delivery_html = "<p>We offer instant delivery within 2 hours of payment.</p>"
        valid, violations = self.engine.validate_article_conversion_compliance(bad_delivery_html)
        self.assertFalse(valid)
        self.assertTrue(any("Delivery" in v for v in violations))

        # Missing 30-day warranty
        bad_warranty_html = "<p>All accounts come with a 7-day warranty period.</p>"
        valid, violations = self.engine.validate_article_conversion_compliance(bad_warranty_html)
        self.assertFalse(valid)
        self.assertTrue(any("Warranty" in v for v in violations))

        # Compliant HTML
        compliant_html = """
        <p>Orders are backed by our 15-minute digital delivery SLA and a full 30-day replacement warranty.</p>
        <p><a href="https://aidigitools.tech/tools/cursor-pro.html">Explore Full Tool Details</a></p>
        """
        valid, violations = self.engine.validate_article_conversion_compliance(compliant_html)
        self.assertTrue(valid)
        self.assertEqual(len(violations), 0)

    def test_irrelevant_product_injection_guard(self):
        """Prevent injecting unrelated products into technical/coding articles."""
        coding_article_with_entertainment = """
        <h2>Top AI Coding Tools</h2>
        <p>Cursor is great for code editing. If you need a break, watch movies with <a href="/tools/netflix-premium.html">Netflix</a>.</p>
        """
        valid, violations = self.engine.validate_article_conversion_compliance(
            coding_article_with_entertainment,
            cluster_slug="ai-coding-and-development"
        )
        self.assertFalse(valid)
        self.assertTrue(any("Topic Relevance Violation" in v for v in violations))

if __name__ == "__main__":
    unittest.main()
