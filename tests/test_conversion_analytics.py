"""
Unit tests for Conversion & Analytics Measurement Engine (Section 15 of Master Architecture Charter).
"""

import unittest
import sys
import json
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.conversion_analytics import ConversionAnalyticsEngine, APPROVED_GA4_EVENTS, VALID_PERIOD_DAYS

ROOT_DIR = Path(__file__).resolve().parent.parent

class TestConversionAnalytics(unittest.TestCase):
    def setUp(self):
        self.engine = ConversionAnalyticsEngine()

    def test_approved_ga4_events_validation(self):
        """All 6 authorized GA4 events must validate successfully with compliant parameters."""
        sample_payloads = {
            "blog_article_view": {"article_id": "ART-001", "article_title": "Claude vs ChatGPT", "cluster_slug": "ai-assistants-and-llms", "author_slug": "abeera-farooq"},
            "blog_to_product_click": {"source_article_id": "ART-001", "target_tool_slug": "cursor-pro", "cluster_slug": "ai-coding-and-development"},
            "comparison_click": {"comparison_id": "CMP-001", "tool_a": "cursor-pro", "tool_b": "github-copilot", "interaction_type": "table_toggle"},
            "quick_order_open": {"tool_slug": "cursor-pro", "plan_id": "PLAN-CURSOR-PRO-1M", "source_page": "/tools/cursor-pro.html"},
            "whatsapp_order_start": {"tool_slug": "cursor-pro", "plan_id": "PLAN-CURSOR-PRO-1M", "price_pkr": 3800, "payment_method": "EasyPaisa"},
            "confirmed_order": {"order_id": "ORD-2026-991", "tool_slug": "cursor-pro", "plan_id": "PLAN-CURSOR-PRO-1M", "value_pkr": 3800, "currency": "PKR", "verification_status": "VERIFIED"}
        }

        for ev_name, params in sample_payloads.items():
            ok, viols = self.engine.validate_ga4_event(ev_name, params)
            self.assertTrue(ok, f"Event '{ev_name}' failed validation: {viols}")
            self.assertEqual(len(viols), 0)

    def test_unapproved_events_rejected(self):
        """Unapproved or custom ad-hoc events must be rejected."""
        ok, viols = self.engine.validate_ga4_event("unapproved_custom_click", {"foo": "bar"})
        self.assertFalse(ok)
        self.assertTrue(any("Unapproved GA4 Event" in v for v in viols))

    def test_privacy_firewall_blocks_pii(self):
        """PII such as phone numbers, emails, and credentials must trigger privacy violations."""
        bad_payloads = [
            ("whatsapp_order_start", {"tool_slug": "cursor-pro", "customer_phone": "03326861112"}),
            ("whatsapp_order_start", {"tool_slug": "cursor-pro", "customer_phone": "+923326861112"}),
            ("quick_order_open", {"tool_slug": "cursor-pro", "customer_email": "customer@gmail.com"}),
            ("confirmed_order", {"order_id": "ORD-1", "tool_slug": "cursor-pro", "verification_status": "VERIFIED", "credit_card_last4": "1234"})
        ]

        for ev_name, params in bad_payloads:
            ok, viols = self.engine.validate_ga4_event(ev_name, params)
            self.assertFalse(ok, f"PII payload was not blocked: {params}")
            self.assertTrue(any("Privacy Violation" in v for v in viols))

    def test_order_separation_firewall(self):
        """confirmed_order events require genuine VERIFIED status and order_id."""
        # Unverified status
        bad_status = {
            "order_id": "ORD-123",
            "tool_slug": "cursor-pro",
            "verification_status": "CLICKED_WHATSAPP"
        }
        ok, viols = self.engine.validate_ga4_event("confirmed_order", bad_status)
        self.assertFalse(ok)
        self.assertTrue(any("Order Separation Violation" in v for v in viols))

        # Missing order_id
        missing_id = {
            "tool_slug": "cursor-pro",
            "verification_status": "VERIFIED"
        }
        ok_id, viols_id = self.engine.validate_ga4_event("confirmed_order", missing_id)
        self.assertFalse(ok_id)
        self.assertTrue(any("missing verified 'order_id'" in v for v in viols_id))

    def test_multi_period_reports_generation(self):
        """Reports must be generated across 7, 14, 28, and 56 days with all required metrics."""
        for period in VALID_PERIOD_DAYS:
            rep = self.engine.generate_performance_report(period)
            self.assertEqual(rep["report_period_days"], period)

            # Search Console metrics
            gsc = rep["search_console_metrics"]
            self.assertIn("organic_impressions", gsc)
            self.assertIn("organic_clicks", gsc)
            self.assertIn("average_ctr_percent", gsc)
            self.assertIn("average_position", gsc)
            self.assertIn("indexed_blog_urls", gsc)

            # Engagement metrics
            ga4 = rep["analytics_engagement_metrics"]
            self.assertIn("engaged_organic_sessions", ga4)
            self.assertIn("average_engagement_time_seconds", ga4)
            self.assertIn("bounce_rate_percent", ga4)

            # Funnel metrics
            funnel = rep["conversion_funnel"]
            self.assertIn("blog_article_views", funnel)
            self.assertIn("article_to_product_clicks", funnel)
            self.assertIn("quick_order_interactions", funnel)
            self.assertIn("whatsapp_order_starts", funnel)
            self.assertIn("confirmed_orders_verified", funnel)

            # Clusters & Declining pages
            self.assertIn("performance_by_topic_cluster", rep)
            self.assertIn("content_updates_and_declining_pages", rep)

            # Verify saved file
            path = ROOT_DIR / "data" / f"analytics_report_{period}d.json"
            self.assertTrue(path.exists())

    def test_business_success_reality_principle(self):
        """Reports must explicitly contain the principle warning against equating raw traffic with success."""
        rep = self.engine.generate_performance_report(28)
        principle = rep.get("business_reality_principle", "")
        self.assertIn("Traffic growth does not automatically equate to business success", principle)

if __name__ == "__main__":
    unittest.main()
