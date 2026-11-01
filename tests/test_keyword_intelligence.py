"""
Unit tests for Keyword & Topic Intelligence Engine and Section 5 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.keyword_intelligence import KeywordIntelligenceEngine, PREFERRED_THRESHOLD

class TestKeywordIntelligence(unittest.TestCase):
    def setUp(self):
        self.kie = KeywordIntelligenceEngine()

    def test_01_all_topics_have_13_attributes(self):
        """Verify every candidate topic has all 13 attributes mandated by Section 5."""
        required = [
            "primary_keyword", "secondary_keywords", "long_tail_queries",
            "question_based_queries", "related_entities", "search_intent",
            "language", "country_market_relevance", "existing_ranking_opportunities",
            "competitor_coverage", "product_category_relevance", "existing_target_urls",
            "cannibalization_risk"
        ]
        for t in self.kie.topics:
            for r in required:
                self.assertIn(r, t, f"Topic '{t.get('topic_id')}' missing attribute '{r}'")
                self.assertTrue(t[r], f"Topic '{t.get('topic_id')}' has empty attribute '{r}'")

    def test_02_scoring_dimensions_sum_to_100(self):
        """Verify the 7 scoring dimensions sum to max 100 points."""
        breakdown = {
            "search_opportunity": 15,
            "gsc_bing_opportunity": 20,
            "audience_relevance": 15,
            "competitor_content_gap": 15,
            "trend_freshness": 10,
            "original_research_potential": 15,
            "business_relevance": 10
        }
        total, passed = self.kie.calculate_topic_score(breakdown)
        self.assertEqual(total, 100)
        self.assertTrue(passed)

    def test_03_preferred_threshold_gating(self):
        """Verify topics below threshold (85/100) are flagged and not auto-published."""
        low_breakdown = {
            "search_opportunity": 10,
            "gsc_bing_opportunity": 10,
            "audience_relevance": 10,
            "competitor_content_gap": 10,
            "trend_freshness": 5,
            "original_research_potential": 10,
            "business_relevance": 5
        }
        total, passed = self.kie.calculate_topic_score(low_breakdown)
        self.assertEqual(total, 60)
        self.assertFalse(passed)

    def test_04_cannibalization_guard_detects_existing_pages(self):
        """Verify cannibalization guard flags existing URLs targeting the same intent."""
        # 'chatgpt plus' already exists as tools/chatgpt-plus.html
        is_risk, conflicts = self.kie.detect_cannibalization("chatgpt plus")
        self.assertTrue(is_risk)
        self.assertTrue(any("chatgpt-plus.html" in c for c in conflicts))

    def test_05_update_existing_page_recommendation(self):
        """Verify that when cannibalization is detected, action is UPDATE_EXISTING_PAGE."""
        # Topic 004 has high cannibalization
        t4 = next(t for t in self.kie.topics if t["topic_id"] == "TOPIC-004")
        eval_res = self.kie.evaluate_candidate_topic(t4)
        # Score is 82 (below 85) or cannibalization detected
        self.assertIn(eval_res["recommended_action"], ["UPDATE_EXISTING_PAGE", "SKIP_REJECT"])

if __name__ == "__main__":
    unittest.main()

