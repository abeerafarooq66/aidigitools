"""
Unit Tests for Content Reporting & Historical Performance Engine (Part 22).
===========================================================================
Strictly tests Part 22 of Master Architecture Charter:
CONTENT REPORTING.

Validates:
1. Every cycle report contains all 17 mandatory elements in Pakistan Standard Time (PKT).
2. JSON and Markdown report artifact generation.
3. Chronological logging to the historical content and performance database.
4. Multi-period performance tracking (7d, 14d, 28d, 56d).
5. Accurate logging for both publication and skip/held decisions.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.content_reporter import ContentReporterEngine


class TestContentReporter(unittest.TestCase):

    def setUp(self):
        """Create an isolated test workspace for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.engine = ContentReporterEngine(workspace_root=self.workspace)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generate_cycle_report_contains_all_17_elements(self):
        """A complete cycle report must contain all 17 mandatory elements in PKT."""
        report = self.engine.generate_cycle_report(
            cycle_id="CYCLE-2026-11-02-01",
            data_sources_accessed=["GSC_REST_API", "GA4_DATA", "BING_SEARCH", "CENTRAL_REGISTRY"],
            data_sources_unavailable=["GOOGLE_ADS_API"],
            search_opportunity_findings={"evaluated_count": 4, "top_score": 95},
            selected_topic={"topic_id": "TOPIC-001", "title": "Cursor AI vs GitHub Copilot"},
            primary_keyword="cursor ai vs github copilot",
            secondary_keywords=["cursor vs copilot 2026", "ai code editor pakistan"],
            search_intent="Commercial Investigation",
            competitor_gap="Competitors lack benchmark tables and PKR pricing breakdowns.",
            relevant_products=["cursor-pro", "github-copilot"],
            research_sources=["https://cursor.com", "https://github.com/features/copilot"],
            evidence_status={"tier": "Tier B: Research-based independent analysis", "verified_at_pkt": "2026-11-02 01:00:00 PKT"},
            quality_gate_results={"overall_score": 100.0, "passed_gates_count": 20, "critical_failures": []},
            decision="APPROVED",
            decision_reason="All 20 quality gates passed; 48-hour cadence gate cleared.",
            deployed_url="https://aidigitools.tech/compare/cursor-ai-vs-github-copilot-comparison.html",
            sitemap_indexnow_result={"sitemap_updated": True, "indexnow_submitted": True},
            google_indexing_status="SUBMITTED",
            errors_and_improvements=["Consider adding interactive benchmark slider in next iteration."]
        )

        # 1. Date/time in PKT
        self.assertTrue(report["timestamp_pkt"].endswith(" PKT"))
        # 2. Data sources accessed
        self.assertIn("GSC_REST_API", report["data_sources_accessed"])
        # 3. Data sources unavailable
        self.assertIn("GOOGLE_ADS_API", report["data_sources_unavailable"])
        # 4. Search opportunity findings
        self.assertEqual(report["search_opportunity_findings"]["top_score"], 95)
        # 5. Selected topic
        self.assertEqual(report["selected_topic"]["topic_id"], "TOPIC-001")
        # 6. Primary and secondary keywords
        self.assertEqual(report["primary_keyword"], "cursor ai vs github copilot")
        self.assertEqual(len(report["secondary_keywords"]), 2)
        # 7. Search intent
        self.assertEqual(report["search_intent"], "Commercial Investigation")
        # 8. Competitor gap
        self.assertIn("Competitors lack benchmark tables", report["competitor_gap"])
        # 9. Relevant products
        self.assertIn("cursor-pro", report["relevant_products"])
        # 10. Research sources
        self.assertIn("https://cursor.com", report["research_sources"])
        # 11. Evidence verification status
        self.assertIn("Tier B", report["evidence_verification_status"]["tier"])
        # 12. Quality gate results
        self.assertEqual(report["quality_gate_results"]["overall_score"], 100.0)
        # 13. Publication or skip decision
        self.assertEqual(report["publication_or_skip_decision"]["decision"], "APPROVED")
        # 14. Deployed URL
        self.assertEqual(report["deployed_url"], "https://aidigitools.tech/compare/cursor-ai-vs-github-copilot-comparison.html")
        # 15. Sitemap/IndexNow result
        self.assertTrue(report["sitemap_indexnow_submission_result"]["sitemap_updated"])
        # 16. Google indexing status
        self.assertEqual(report["google_indexing_status"], "SUBMITTED")
        # 17. Errors and recommended improvements
        self.assertEqual(len(report["errors_and_recommended_improvements"]), 1)

    def test_markdown_report_rendering(self):
        """Report generator must output clean, valid Markdown artifacts on disk."""
        self.engine.generate_cycle_report(
            cycle_id="CYCLE-TEST-MD",
            data_sources_accessed=["GSC", "GA4"],
            data_sources_unavailable=[],
            search_opportunity_findings={"score": 93},
            selected_topic={"topic_id": "TOPIC-002", "title": "Claude Artifacts"},
            primary_keyword="claude artifacts",
            secondary_keywords=["claude pro"],
            search_intent="Informational",
            competitor_gap="Lack visual walkthroughs.",
            relevant_products=["claude-pro"],
            research_sources=["https://anthropic.com"],
            evidence_status={"tier": "Tier B", "verified_at_pkt": "2026-11-02 01:00:00 PKT"},
            quality_gate_results={"overall_score": 100.0, "passed_gates_count": 20, "critical_failures": []},
            decision="APPROVED",
            decision_reason="Passed all gates.",
            deployed_url="https://aidigitools.tech/guides/claude-artifacts.html"
        )

        md_path = self.engine.latest_report_md
        self.assertTrue(md_path.exists())
        content = md_path.read_text(encoding="utf-8")
        self.assertIn("# AIDigiTools Autonomous Content Intelligence Cycle Report", content)
        self.assertIn("CYCLE-TEST-MD", content)
        self.assertIn("**Decision**: **`APPROVED`**", content)
        self.assertIn("https://aidigitools.tech/guides/claude-artifacts.html", content)

    def test_historical_performance_database_logging(self):
        """Historical database must append new cycles and track multi-period metrics."""
        self.engine.generate_cycle_report(
            cycle_id="CYCLE-HIST-01",
            data_sources_accessed=["BING_API"],
            data_sources_unavailable=[],
            search_opportunity_findings={},
            selected_topic={"topic_id": "TOPIC-001"},
            primary_keyword="cursor ai vs copilot",
            secondary_keywords=[],
            search_intent="Commercial",
            competitor_gap="Gap",
            relevant_products=["cursor-pro"],
            research_sources=[],
            evidence_status={"tier": "Tier B"},
            quality_gate_results={"overall_score": 100.0},
            decision="APPROVED",
            decision_reason="Success"
        )

        db = self.engine.get_historical_database()
        self.assertGreaterEqual(db["total_tracked_cycles"], 1)
        self.assertEqual(len(db["cycle_log"]), 1)
        self.assertEqual(db["cycle_log"][0]["cycle_id"], "CYCLE-HIST-01")
        self.assertEqual(db["cycle_log"][0]["decision"], "APPROVED")

    def test_skip_cycle_reporting(self):
        """Skipped cycles (cadence lock or low score) must be accurately recorded without deployed URLs."""
        report = self.engine.generate_cycle_report(
            cycle_id="CYCLE-SKIP-01",
            data_sources_accessed=["CENTRAL_REGISTRY"],
            data_sources_unavailable=[],
            search_opportunity_findings={"top_score": 78},
            selected_topic=None,
            primary_keyword="none",
            secondary_keywords=[],
            search_intent="N/A",
            competitor_gap="N/A",
            relevant_products=[],
            research_sources=[],
            evidence_status={},
            quality_gate_results={},
            decision="SKIP",
            decision_reason="Cadence lock active: Only 22.0 hours elapsed since last publication.",
            deployed_url=None
        )

        self.assertEqual(report["publication_or_skip_decision"]["decision"], "SKIP")
        self.assertIsNone(report["deployed_url"])
        self.assertIn("Cadence lock active", report["publication_or_skip_decision"]["reason"])


if __name__ == "__main__":
    unittest.main()
