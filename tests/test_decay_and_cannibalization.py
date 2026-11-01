"""
Unit tests for Content Decay and Cannibalization Management Engine (Section 16 of Master Architecture Charter).
"""

import unittest
import sys
import json
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.decay_and_cannibalization import DecayAndCannibalizationEngine, REPORT_OUTPUT_PATH

ROOT_DIR = Path(__file__).resolve().parent.parent

class TestDecayAndCannibalization(unittest.TestCase):
    def setUp(self):
        self.engine = DecayAndCannibalizationEngine()

    def test_duplicate_intent_and_cannibalization_detection(self):
        """Overlapping queries for published articles must trigger UPDATE_EXISTING_PAGE."""
        # Query that overlaps with compare/chatgpt-vs-claude.html
        res = self.engine.detect_duplicate_intent_and_cannibalization(
            candidate_keyword="chatgpt plus vs claude pro comparison",
            candidate_intent="commercial comparison"
        )
        self.assertTrue(res["cannibalization_risk"])
        self.assertEqual(res["recommendation"], "UPDATE_EXISTING_PAGE")
        self.assertIn("chatgpt-vs-claude", res["competing_url"])

        # Commercial query that overlaps with tool page
        res_tool = self.engine.detect_duplicate_intent_and_cannibalization(
            candidate_keyword="buy cursor pro",
            candidate_intent="transactional"
        )
        self.assertTrue(res_tool["cannibalization_risk"])
        self.assertEqual(res_tool["recommendation"], "UPDATE_EXISTING_PAGE")
        self.assertIn("tools/cursor-pro.html", res_tool["competing_url"])

    def test_distinct_intent_allowed(self):
        """Distinct search intent with no competing URL must be approved for new article creation."""
        res = self.engine.detect_duplicate_intent_and_cannibalization(
            candidate_keyword="how to fine-tune deepseek r1 locally with ollama",
            candidate_intent="informational tutorial"
        )
        self.assertFalse(res["cannibalization_risk"])
        self.assertEqual(res["recommendation"], "CREATE_NEW_ARTICLE")

    def test_performance_decay_thresholds(self):
        """Drops in clicks >= 15% or impressions >= 20% must be flagged as decay."""
        mock_data = {
            "https://aidigitools.tech/stable-page.html": {
                "current_28d": {"clicks": 500, "impressions": 8000},
                "previous_28d": {"clicks": 510, "impressions": 8100}
            },
            "https://aidigitools.tech/decaying-page.html": {
                "current_28d": {"clicks": 400, "impressions": 6000},
                "previous_28d": {"clicks": 500, "impressions": 8000}  # 20% clicks drop, 25% impr drop
            }
        }
        decaying = self.engine.detect_performance_decay(mock_data)
        self.assertEqual(len(decaying), 1)
        self.assertEqual(decaying[0]["url"], "https://aidigitools.tech/decaying-page.html")
        self.assertEqual(decaying[0]["status"], "DECAY_DETECTED")
        self.assertGreaterEqual(decaying[0]["clicks_drop_percent"], 15.0)

    def test_meaningful_date_modified_enforcement(self):
        """Only change dateModified when a meaningful update has actually occurred."""
        orig_html = "<article><h1>AI Video Tools</h1><p>Here is an introduction to video generators.</p></article>"

        # Trivial update (only whitespace or tiny typo)
        trivial_html = "<article><h1>AI Video Tools</h1><p>Here is an introduction to video generators. </p></article>"
        ok_triv, viols_triv = self.engine.validate_meaningful_date_modified(
            orig_html, trivial_html, "2026-10-15", "2026-11-01"
        )
        self.assertFalse(ok_triv)
        self.assertTrue(any("Trivial Update Violation" in v for v in viols_triv))

        # Substantial update (new paragraphs, benchmark numbers, fresh facts)
        substantial_html = """
        <article>
            <h1>AI Video Tools</h1>
            <p>Here is an introduction to video generators. In our latest October 2026 benchmark, Runway Gen-3 Alpha rendered 720p 10-second clips in 84 seconds, while Kling 1.5 achieved superior temporal stability in complex camera pans.</p>
        </article>
        """
        ok_sub, viols_sub = self.engine.validate_meaningful_date_modified(
            orig_html, substantial_html, "2026-10-15", "2026-11-01"
        )
        self.assertTrue(ok_sub)
        self.assertEqual(len(viols_sub), 0)

    def test_page_retirement_rules(self):
        """Active pages cannot be retired without 301 redirects, and high-value pages must be retained."""
        # High value page
        res_high = self.engine.evaluate_page_retirement(
            "/tools/cursor-pro.html", traffic_30d=520, inbound_links=5, business_purpose="Primary tool landing page"
        )
        self.assertEqual(res_high["decision"], "RETAIN_AND_IMPROVE")

        # Low traffic page with active visitors
        res_low = self.engine.evaluate_page_retirement(
            "/legacy-guide.html", traffic_30d=12, inbound_links=1, business_purpose="Old guide"
        )
        self.assertEqual(res_low["decision"], "CONSOLIDATE_AND_301_REDIRECT")

        # Zero traffic and no purpose
        res_zero = self.engine.evaluate_page_retirement(
            "/temp-test.html", traffic_30d=0, inbound_links=0, business_purpose="None"
        )
        self.assertEqual(res_zero["decision"], "RETIRE_OR_NOINDEX")

    def test_pricing_and_version_drift_detection(self):
        """Discrepancies between mentioned pricing and central registry must be flagged."""
        # Tool cursor-pro verified price is 3,800 PKR
        outdated_html = "<p>Cursor Pro is currently available for Rs. 2,000 PKR on our site.</p>"
        drifts = self.engine.check_pricing_and_version_drift(outdated_html, "cursor-pro")
        self.assertGreater(len(drifts), 0)
        self.assertEqual(drifts[0]["type"], "PRICE_DRIFT_PKR")
        self.assertEqual(drifts[0]["mentioned_pkr"], 2000)

    def test_scheduled_decay_cycle_generates_valid_report(self):
        """Scheduled decay cycle executes and outputs valid report to disk."""
        rep = self.engine.run_scheduled_decay_cycle()
        self.assertIn("last_cycle_run", rep)
        self.assertIn("outdated_articles_count", rep)
        self.assertIn("performance_decay_detected", rep)
        self.assertIn("orphan_pages_count", rep)
        self.assertEqual(rep["scheduled_cycle_status"], "CYCLE_COMPLETED")
        self.assertTrue(REPORT_OUTPUT_PATH.exists())

if __name__ == "__main__":
    unittest.main()

