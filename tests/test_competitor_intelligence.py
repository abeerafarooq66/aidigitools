"""
Unit tests for Competitor Intelligence Engine and Section 4 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.competitor_intelligence import CompetitorIntelligenceEngine

class TestCompetitorIntelligence(unittest.TestCase):
    def setUp(self):
        self.cie = CompetitorIntelligenceEngine()

    def test_01_competitor_profiles_loaded(self):
        """Verify direct regional competitors and official hubs are tracked."""
        names = self.cie.list_competitors()
        self.assertIn("AI Tools Pak", names)
        self.assertIn("AI Tool Gems", names)
        self.assertIn("Official Provider Documentation", names)
        self.assertIn("Independent Tech Publications", names)

    def test_02_topic_gap_analysis_generates_mandates(self):
        """Verify gap analysis generates concrete research mandates."""
        gaps = self.cie.analyze_topic_gaps("Canva Pro")
        self.assertGreaterEqual(len(gaps["competitor_weaknesses_identified"]), 1)
        self.assertGreaterEqual(len(gaps["missing_user_questions_to_answer"]), 1)
        self.assertGreaterEqual(len(gaps["original_research_mandates"]), 1)

    def test_03_anti_plagiarism_and_forbidden_brand_names(self):
        """Verify competitor brand names and private data claims are blocked."""
        bad_text_1 = "Why buy from AI Tools Pak when you can buy from us?"
        valid_1, viols_1 = self.cie.verify_compliance_and_originality(bad_text_1)
        self.assertFalse(valid_1)
        self.assertTrue(any("ai tools pak" in v.lower() for v in viols_1))

        bad_text_2 = "Competitor analytics reveal their private conversion rate is 4%."
        valid_2, viols_2 = self.cie.verify_compliance_and_originality(bad_text_2)
        self.assertFalse(valid_2)

    def test_04_original_content_passes_clean(self):
        """Verify authentic original research passes compliance cleanly."""
        good_text = (
            "In our hands-on evaluation of Claude 3.5 Sonnet in Pakistan, we benchmarked "
            "token processing speeds across local ISPs and verified domestic EasyPaisa settlement."
        )
        valid, viols = self.cie.verify_compliance_and_originality(good_text)
        self.assertTrue(valid)
        self.assertEqual(len(viols), 0)

if __name__ == "__main__":
    unittest.main()

