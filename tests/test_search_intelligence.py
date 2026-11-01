"""
Unit tests for Search Intelligence Aggregator and Section 3 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.search_intelligence import SearchIntelligenceAggregator

class TestSearchIntelligence(unittest.TestCase):
    def setUp(self):
        self.agg = SearchIntelligenceAggregator()

    def test_01_provenance_metadata_enforced(self):
        """Verify every imported source stores rigorous data provenance fields."""
        report = self.agg.generate_unified_intelligence_report()
        sources = ["google_search_console", "google_analytics_4", "bing_webmaster", "predictive_trends", "pagespeed_and_crux"]
        
        required_prov_keys = ["source", "fetch_timestamp", "metric_type", "status", "limitations"]
        for s in sources:
            self.assertIn(s, report, f"Source '{s}' missing in unified report")
            prov = report[s].get("provenance", {})
            for rk in required_prov_keys:
                self.assertIn(rk, prov, f"Provenance key '{rk}' missing in source '{s}'")

    def test_02_predictive_trends_discovery_active(self):
        """Verify real-time Google search trends returns live queries without API keys."""
        trends = self.agg.fetch_trending_search_queries(["best ai tools", "claude vs chatgpt"])
        self.assertEqual(trends["provenance"]["metric_type"], "inferred_trend_interest")
        self.assertGreaterEqual(trends["total_trending_queries_discovered"], 2)
        self.assertIn("best ai tools", trends["trends_by_seed"])

    def test_03_zero_data_invention_on_missing_credentials(self):
        """Verify that missing credentials return UNAVAILABLE without fabricating fake data."""
        # Unset keys for this test
        old_gsc = self.agg.gsc_key
        self.agg.gsc_key = ""
        gsc = self.agg.fetch_gsc_intelligence()
        self.assertEqual(gsc["provenance"]["status"], "UNAVAILABLE")
        self.assertEqual(len(gsc["opportunities"]), 0)
        self.agg.gsc_key = old_gsc

    def test_04_ga4_whatsapp_inquiry_invariant(self):
        """Verify GA4 limitations explicitly declare WhatsApp clicks as inquiries, not sales."""
        ga4 = self.agg.fetch_ga4_intelligence()
        limitations = ga4["provenance"]["limitations"].lower()
        self.assertIn("not confirmed purchases", limitations)

if __name__ == "__main__":
    unittest.main()

