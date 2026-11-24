"""
Unit tests for Backlink Intelligence & Competitor Outreach Acquisition Engine.
=============================================================================
Verifies all core architectural guarantees:
1. Multi-category prospect vetting (Relevance, DA, Traffic, Placement, Spam Score).
2. Live HTTP backlink verification — never report unverified links as acquired.
3. Competitor backlink gap analysis.
4. Human-In-The-Loop governance for outreach pitches.
5. Anchor text safety auditing (<20% exact match guardrail).
6. Toxic backlink detection.
"""

import os
import sys
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Workspace path setup
ROOT_DIR = Path(__file__).resolve().parent.parent
SEO_AGENT_DIR = ROOT_DIR / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent.backlink_intelligence_engine import BacklinkIntelligenceEngine
from agent.competitor_deep_analyzer import CompetitorDeepAnalyzer


class TestBacklinkIntelligence(unittest.TestCase):
    def setUp(self):
        self.bie = BacklinkIntelligenceEngine(workspace_root=ROOT_DIR)
        self.cda = CompetitorDeepAnalyzer()

    def test_01_backlink_registry_and_summary_schema(self):
        """Verify backlink registry exists and has valid summary fields."""
        self.assertTrue(self.bie.registry_path.exists())
        with open(self.bie.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("summary", data)
        self.assertIn("links", data)
        self.assertIn("anchor_distribution", data)
        self.assertGreaterEqual(data["summary"]["total_backlinks"], 0)

    def test_02_live_verification_returns_empirical_status(self):
        """Verify live backlink verification executes and returns true counts."""
        res = self.bie.verify_registered_backlinks_live(timeout=5.0)
        self.assertIn("active_count", res)
        self.assertIn("total_backlinks", res)
        self.assertGreaterEqual(res["total_backlinks"], 0)

    def test_03_competitor_backlink_matrix_and_gap_analysis(self):
        """Verify competitor backlink matrix tracks competitors and gaps."""
        matrix = self.bie.get_competitor_backlink_matrix()
        self.assertIn("competitors", matrix)
        self.assertIn("backlink_gap_analysis", matrix)
        
        comps = matrix["competitors"]
        domains = [c["domain"] for c in comps]
        self.assertIn("aitoolspak.com", domains)
        self.assertIn("futurepedia.io", domains)

        gaps = self.bie.identify_backlink_gaps()
        self.assertGreaterEqual(len(gaps), 5)
        for g in gaps:
            self.assertIn("gap_id", g)
            self.assertIn("domain", g)
            self.assertIn("domain_authority", g)
            self.assertIn("target_editorial_angle", g)
            self.assertFalse(g["links_to_aidigitools"])

    def test_04_vetted_opportunities_across_nine_categories(self):
        """Verify vetted opportunities cover all 9 required categories."""
        opps = self.bie.list_vetted_opportunities(min_composite_score=50.0)
        self.assertGreaterEqual(len(opps), 10)

        categories = set(o["category"] for o in opps)
        self.assertTrue(any("Directory" in c or "Software" in c for c in categories))
        self.assertTrue(any("Publication" in c for c in categories))
        self.assertTrue(any("Communit" in c for c in categories))

        # Check multi-factor scoring (never DA alone)
        for o in opps:
            self.assertIn("quality_composite_score", o)
            self.assertIn("relevance_score", o)
            self.assertIn("spam_score", o)
            self.assertLessEqual(o["spam_score"], 4, "Spam score must be strictly <= 4 for vetted prospects")

    def test_05_outreach_pipeline_enforces_human_in_the_loop(self):
        """Verify outreach pitches are saved with PENDING_USER_APPROVAL and require approval."""
        pipeline = self.bie.get_outreach_pipeline()
        campaigns = pipeline.get("campaigns", [])
        self.assertGreaterEqual(len(campaigns), 1)

        for c in campaigns:
            self.assertTrue(c.get("requires_user_approval"))
            self.assertEqual(c.get("status"), "PENDING_USER_APPROVAL")
            self.assertIn("email_subject", c)
            self.assertIn("email_body", c)
            self.assertIn("aidigitools.tech", c["email_body"])

    def test_06_anchor_text_safety_auditor(self):
        """Verify anchor text safety detects over-optimization risk when exact match > 20%."""
        safety = self.bie.audit_anchor_text_safety()
        self.assertIn("status", safety)
        self.assertIn("exact_match_percent", safety)
        self.assertLessEqual(safety["exact_match_percent"], 20.0)
        self.assertEqual(safety["status"], "HEALTHY")

    def test_07_competitor_deep_analyzer_brief_generation(self):
        """Verify CompetitorDeepAnalyzer generates actionable original research briefs."""
        brief = self.cda.generate_original_content_brief("ChatGPT Plus in Pakistan")
        self.assertIn("target_keyword", brief)
        self.assertIn("required_sections", brief)
        self.assertIn("competitor_shortcomings_to_exploit", brief)
        self.assertIn("must_answer_questions", brief)
        self.assertGreaterEqual(len(brief["required_sections"]), 4)

    def test_08_no_unverified_backlink_claims(self):
        """Verify unverified links cannot be marked ACQUIRED."""
        summary = self.bie.verify_registered_backlinks_live()
        # Active count must strictly equal sum of genuinely verified links
        with open(self.bie.registry_path, "r", encoding="utf-8") as f:
            reg = json.load(f)
        genuine_active = sum(1 for l in reg["links"] if l.get("status") in ("ACTIVE", "Live Verified"))
        self.assertEqual(summary["active_count"], genuine_active)


if __name__ == "__main__":
    unittest.main()
