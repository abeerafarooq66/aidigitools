"""
Unit tests for Product Intelligence Registry & Section 2 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.product_intelligence import ProductIntelligence

class TestProductIntelligence(unittest.TestCase):
    def setUp(self):
        self.pi = ProductIntelligence()

    def test_01_all_49_products_registered(self):
        slugs = self.pi.list_all_slugs()
        self.assertEqual(len(slugs), 49, f"Expected 49 canonical products, found {len(slugs)}")

    def test_02_hold_products_strictly_block_purchase_ctas(self):
        hold_slugs = [
            "coursera-plus", "linkedin-premium", "netflix-premium",
            "spotify-premium", "turnitin-student"
        ]
        for slug in hold_slugs:
            self.assertFalse(
                self.pi.is_cta_permitted(slug),
                f"Hold product {slug} must NOT permit purchase CTA"
            )
            p = self.pi.get_product(slug)
            self.assertEqual(p["restricted_status"], "Hold / Inquiry Only")
            self.assertEqual(p["current_availability"], "InquiryOnly")

    def test_03_active_products_permit_purchase_ctas(self):
        active_slugs = ["adobe-creative-cloud", "claude-pro", "chatgpt-plus", "cursor-pro"]
        for slug in active_slugs:
            self.assertTrue(
                self.pi.is_cta_permitted(slug),
                f"Active product {slug} should permit purchase CTA"
            )
            p = self.pi.get_product(slug)
            self.assertEqual(p["restricted_status"], "Normal / Active")
            self.assertEqual(p["current_availability"], "InStock")

    def test_04_pricing_separation_invariant(self):
        """Verify provider price and AIDigiTools offer price are never combined."""
        pricing = self.pi.get_pricing_breakdown("claude-pro")
        self.assertIn("official_provider_price", pricing)
        self.assertIn("aidigitools_offer_price_pkr", pricing)
        self.assertTrue(pricing["is_separate_concierge_offer"])
        self.assertNotEqual(pricing["official_provider_price"], pricing["aidigitools_offer_price_pkr"])

    def test_05_prohibited_terminology_detector(self):
        """Verify prohibited account sharing and cracking terms are caught."""
        bad_text = "Get a shared slot with profile pin and cracked access."
        valid, violations = self.pi.validate_article_claims(bad_text)
        self.assertFalse(valid)
        self.assertTrue(any("shared slot" in v for v in violations))
        self.assertTrue(any("cracked" in v for v in violations))

    def test_06_unverified_reseller_claim_detector(self):
        """Verify false official partner claims are caught."""
        bad_text = "AIDigiTools is an official partner and authorized reseller of OpenAI."
        valid, violations = self.pi.validate_article_claims(bad_text)
        self.assertFalse(valid)
        self.assertTrue(any("official partner" in v.lower() for v in violations))

if __name__ == "__main__":
    unittest.main()
