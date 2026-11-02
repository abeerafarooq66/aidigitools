"""
AIDigiTools — Full Autonomous Publishing & Security Test Suite
==============================================================
Validates the complete autonomous publishing architecture:
1. Operational Phase: FULL_AUTONOMOUS active, 3-article barrier obsolete.
2. Direct Autonomous Publishing: Compliant articles publish without human approval.
3. Quality Gate Invariant: Failed quality gates strictly block publication.
4. High-Risk Triggers: Sensitive policy claims held for policy review.
5. Global Emergency Switch: Instantly halts all autonomous publishing.
6. Duplicate Protection: Duplicate slug, title, or canonical is rejected.
7. Content Rollback: Rollback workflow accurately marks status in ledger.
8. End-to-End Pipeline: Pipeline publishes, updates sitemap & IndexNow, and reports.
"""

import os
import sys
import json
import shutil
import hashlib
import tempfile
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

from agent.publishing_control import (
    PublishingControlEngine,
    FULL_AUTONOMOUS,
    PHASE_1_SUPERVISED,
    PHASE_2_AUTONOMOUS_LOW_RISK,
    QualityGateBypassProhibitedError,
    EmergencyPublishingDisabledError
)
from agent.automation_scheduler import AutomationScheduler, SchedulerDuplicateError


class TestFullAutonomousPublishing(unittest.TestCase):

    def setUp(self):
        """Create an isolated test workspace for every test."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.previews_dir = self.data_dir / "previews"
        self.previews_dir.mkdir(parents=True, exist_ok=True)
        self.audit_dir = self.workspace / "audit_reports"
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Initialize control ledger in FULL_AUTONOMOUS mode
        self.control_ledger_path = self.data_dir / "publishing_control_ledger.json"
        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump({
                "ledger_version": "2.0.0",
                "business_timezone": "PKT (UTC+5)",
                "current_phase": FULL_AUTONOMOUS,
                "autonomous_publishing_authorized": True,
                "emergency_publishing_disabled": False,
                "approved_supervised_publications_count": 0,
                "phase_2_threshold": 0,
                "pending_previews": [],
                "approved_history": [],
                "rejected_history": [],
                "published_history": [],
                "last_updated_pkt": "2026-11-02 18:00:00 PKT"
            }, f, indent=2)

        # Initialize publication ledger
        self.pub_ledger_path = self.data_dir / "publication_ledger.json"
        with open(self.pub_ledger_path, "w", encoding="utf-8") as f:
            json.dump({
                "ledger_version": "1.0.0",
                "business_timezone": "PKT (UTC+5)",
                "min_cadence_hours": 48.0,
                "last_updated_pkt": "2026-10-31 09:00:00 PKT",
                "publications": [
                    {
                        "article_id": "ART-001",
                        "slug": "existing-test-article",
                        "title": "Existing Test Article",
                        "canonical_url": "https://aidigitools.tech/blog/existing-test-article.html",
                        "relative_url": "blog/existing-test-article.html",
                        "published_at_pkt": "2026-10-31 09:00:00 PKT",
                        "status": "PUBLISHED"
                    }
                ]
            }, f, indent=2)

        self.engine = PublishingControlEngine(workspace_root=self.workspace)

        # Valid compliant sample article HTML
        self.sample_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Cursor AI vs GitHub Copilot Comparison (2026) | AIDigiTools</title>
  <meta name="description" content="Cursor AI vs GitHub Copilot comparison for developers. Real PKR pricing, EasyPaisa and JazzCash payment rails, 15-minute delivery, and 30-day warranty.">
  <link rel="canonical" href="https://aidigitools.tech/blog/cursor-ai-vs-github-copilot.html">
</head>
<body>
  <h1>Cursor AI vs GitHub Copilot Comparison</h1>
  <p class="quick-answer">Cursor Pro costs Rs. 3,800 PKR per month while GitHub Copilot costs Rs. 2,900 PKR on AIDigiTools with 15-minute WhatsApp activation and verified payment rails.</p>
</body>
</html>"""

        self.sample_meta = {
            "slug": "cursor-ai-vs-github-copilot",
            "title": "Cursor AI vs GitHub Copilot Comparison",
            "canonical_url": "https://aidigitools.tech/blog/cursor-ai-vs-github-copilot.html",
            "target_canonical_path": "blog/cursor-ai-vs-github-copilot.html",
            "relative_url": "blog/cursor-ai-vs-github-copilot.html"
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # --------------------------------------------------------------------------
    # 1. Operational Status Verification
    # --------------------------------------------------------------------------
    def test_01_full_autonomous_mode_unlocked_and_active(self):
        """FULL_AUTONOMOUS phase must be active and autonomous publishing enabled."""
        status = self.engine.get_operational_status()
        self.assertEqual(status["current_phase"], FULL_AUTONOMOUS)
        self.assertTrue(status["is_autonomous"])
        self.assertTrue(status["autonomous_publishing_authorized"])
        self.assertFalse(status["emergency_publishing_disabled"])
        self.assertEqual(status["approved_supervised_publications_count"], 0)

    # --------------------------------------------------------------------------
    # 2. Direct Autonomous Publishing (No Human Approval)
    # --------------------------------------------------------------------------
    def test_02_eligible_article_publishes_autonomously_without_human_approval(self):
        """A compliant article passing quality gates must be approved and published autonomously."""
        preview = self.engine.prepare_article_preview(
            slug=self.sample_meta["slug"],
            title=self.sample_meta["title"],
            html_content=self.sample_html,
            metadata=self.sample_meta,
            quality_gate_report={"decision": "APPROVED", "failed_gates_count": 0}
        )

        # In Full Autonomous mode, approval is NOT required!
        self.assertFalse(preview["approval_required"])
        self.assertEqual(preview["decision"], "APPROVED_FOR_AUTO_PUBLICATION")
        self.assertEqual(preview["status"], "READY_TO_PUBLISH")

        # Execute verified production publication
        pub_res = self.engine.publish_verified_article(
            slug=self.sample_meta["slug"],
            title=self.sample_meta["title"],
            html_content=self.sample_html,
            canonical_url=self.sample_meta["canonical_url"],
            metadata=self.sample_meta,
            dry_run=False
        )

        # Verify article written to target file
        published_file = self.workspace / "blog" / "cursor-ai-vs-github-copilot.html"
        self.assertTrue(published_file.exists())
        self.assertIn("Cursor AI vs GitHub Copilot Comparison", published_file.read_text(encoding="utf-8"))

        # Verify SHA-256 content hash
        expected_hash = hashlib.sha256(self.sample_html.encode("utf-8")).hexdigest()
        self.assertEqual(pub_res["content_hash"], expected_hash)
        self.assertEqual(pub_res["status"], "PUBLISHED_AUTONOMOUSLY")

        # Verify control ledger updated
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            c_ledger = json.load(f)
        self.assertEqual(len(c_ledger["published_history"]), 1)
        self.assertEqual(c_ledger["published_history"][0]["slug"], self.sample_meta["slug"])

    # --------------------------------------------------------------------------
    # 3. Quality Gate Failure Rejection Invariant
    # --------------------------------------------------------------------------
    def test_03_quality_gate_failure_blocks_autonomous_publication(self):
        """Failed quality gates must strictly block publication and never be bypassed."""
        failed_gate_report = {
            "decision": "DO NOT PUBLISH",
            "failed_gates_count": 2,
            "critical_failures": ["GATE_02_ONE_H1", "GATE_04_ACCURATE_PRICING"]
        }

        with self.assertRaises(QualityGateBypassProhibitedError) as ctx:
            self.engine.prepare_article_preview(
                slug="failing-article",
                title="Failing Article",
                html_content=self.sample_html,
                metadata={"slug": "failing-article"},
                quality_gate_report=failed_gate_report
            )
        self.assertIn("Never bypass a failed quality gate", str(ctx.exception))

        # Ensure no file is published
        failing_file = self.workspace / "blog" / "failing-article.html"
        self.assertFalse(failing_file.exists())

    # --------------------------------------------------------------------------
    # 4. Persistent High-Risk Triggers Held for Policy Review
    # --------------------------------------------------------------------------
    def test_04_persistent_high_risk_triggers_block_autonomous_publishing(self):
        """Content containing high-risk claims must be held for policy review, not auto-published."""
        tampered_html = self.sample_html + "<p>Special access model with shared slot and profile PIN.</p>"
        prev = self.engine.prepare_article_preview(
            slug="risky-article",
            title="Risky Article",
            html_content=tampered_html,
            metadata={"slug": "risky-article"}
        )

        self.assertTrue(prev["approval_required"])
        self.assertEqual(prev["decision"], "HELD_FOR_POLICY_REVIEW")
        self.assertEqual(prev["status"], "PENDING")

        # Verify enqueued in pending previews
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            c_ledger = json.load(f)
        self.assertTrue(any(p["slug"] == "risky-article" for p in c_ledger["pending_previews"]))

    # --------------------------------------------------------------------------
    # 5. Global Emergency Publishing Disable Switch
    # --------------------------------------------------------------------------
    def test_05_emergency_switch_instantly_suspends_publishing(self):
        """Activating the emergency disable switch must instantly halt autonomous publishing."""
        # Activate emergency switch
        res = self.engine.set_emergency_switch(disabled=True)
        self.assertTrue(res["emergency_publishing_disabled"])
        self.assertTrue(self.engine.is_emergency_disabled())

        status = self.engine.get_operational_status()
        self.assertFalse(status["is_autonomous"])

        preview = self.engine.prepare_article_preview(
            slug=self.sample_meta["slug"],
            title=self.sample_meta["title"],
            html_content=self.sample_html,
            metadata=self.sample_meta
        )
        self.assertTrue(preview["approval_required"])
        self.assertEqual(preview["decision"], "BLOCKED_EMERGENCY_DISABLED")

        # Direct publish attempt raises EmergencyPublishingDisabledError
        with self.assertRaises(EmergencyPublishingDisabledError):
            self.engine.publish_verified_article(
                slug=self.sample_meta["slug"],
                title=self.sample_meta["title"],
                html_content=self.sample_html,
                canonical_url=self.sample_meta["canonical_url"]
            )

        # Deactivate emergency switch resumes autonomous operation
        self.engine.set_emergency_switch(disabled=False)
        self.assertFalse(self.engine.is_emergency_disabled())
        status_resumed = self.engine.get_operational_status()
        self.assertTrue(status_resumed["is_autonomous"])

    # --------------------------------------------------------------------------
    # 6. Duplicate Protection
    # --------------------------------------------------------------------------
    def test_06_duplicate_publication_protection(self):
        """Attempting to publish an article matching an existing publication must be rejected."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        is_dup, reason = scheduler.check_duplicate_publication(
            slug="existing-test-article",
            canonical_url="https://aidigitools.tech/blog/existing-test-article.html",
            title="Existing Test Article"
        )
        self.assertTrue(is_dup)
        self.assertIn("already published", reason)

        # Attempting to record publication raises SchedulerDuplicateError
        with self.assertRaises(SchedulerDuplicateError):
            scheduler.record_publication(
                slug="existing-test-article",
                title="Existing Test Article",
                canonical_url="https://aidigitools.tech/blog/existing-test-article.html",
                cluster_slug="ai-tools",
                article_type="blog",
                author_slug="abeera-farooq",
                primary_keyword="test",
                quality_gate_passed=True
            )

    # --------------------------------------------------------------------------
    # 7. Content Rollback Support
    # --------------------------------------------------------------------------
    def test_07_content_rollback_marks_ledger_and_records_reason(self):
        """Rollback accurately marks the article as ROLLED_BACK in the publication ledger."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        rollback_res = scheduler.rollback_article(
            article_id_or_slug="existing-test-article",
            rollback_reason="Discovered pricing discrepancy in vendor tier."
        )
        self.assertEqual(rollback_res["status"], "ROLLED_BACK")
        self.assertEqual(rollback_res["slug"], "existing-test-article")

        with open(self.pub_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        pub = next(p for p in ledger["publications"] if p["slug"] == "existing-test-article")
        self.assertEqual(pub["status"], "ROLLED_BACK")
        self.assertEqual(pub["rollback_reason"], "Discovered pricing discrepancy in vendor tier.")

    # --------------------------------------------------------------------------
    # 8. End-to-End Pipeline Autonomous Publishing Execution
    # --------------------------------------------------------------------------
    def test_08_end_to_end_pipeline_autonomous_publishing(self):
        """Full pipeline execution autonomously publishes an eligible article without human review."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)

        mock_topic = {
            "topic_id": "TOPIC-AUTO-999",
            "primary_keyword": "cursor pro vs copilot pro 2026",
            "target_canonical_path": "blog/cursor-pro-vs-copilot-pro-2026.html",
            "cluster_slug": "ai-coding-and-development",
            "article_type": "comparison",
            "author_slug": "abeera-farooq"
        }

        mock_research_report = {
            "decision": "TOPIC_SELECTED",
            "reason_code": "TOPIC_QUALIFIED",
            "selected_topic": mock_topic
        }

        mock_gemini_res = {
            "success": True,
            "status": "ARTICLE_GENERATED",
            "generation_method": "GEMINI_API",
            "is_gemini_generated": True,
            "model_used": "models/gemini-2.0-flash",
            "html_draft": self.sample_html
        }

        with patch.object(scheduler, "evaluate_daily_research_check", return_value=mock_research_report), \
             patch("agent.gemini_generator.GeminiArticleGenerator.generate_article", return_value=mock_gemini_res), \
             patch("agent.evidence_system.ResearchEvidenceSystem.verify_article_evidence", return_value={"verified": True, "critical_failures": []}), \
             patch("agent.quality_gates.QualityGateEngine.evaluate_article", return_value={"decision": "APPROVED", "passed_gates_count": 20, "failed_gates_count": 0, "critical_failures": []}):

            pipeline_result = scheduler.execute_full_content_pipeline(force_cadence=True)

            self.assertEqual(pipeline_result["pipeline_status"], "PUBLISHED_AUTONOMOUSLY")
            self.assertTrue(pipeline_result["published"])
            self.assertIn("cursor-pro-vs-copilot-pro-2026.html", pipeline_result["published_url"])
            self.assertIsNotNone(pipeline_result.get("content_hash"))
            self.assertIsNotNone(pipeline_result.get("article_id"))

            # Verify published file on disk
            pub_path = self.workspace / "blog" / "cursor-pro-vs-copilot-pro-2026.html"
            self.assertTrue(pub_path.exists())

            # Verify report generated in audit_reports/
            latest_report = self.workspace / "audit_reports" / "AUTONOMOUS_PUBLISHER_LATEST.md"
            self.assertTrue(latest_report.exists())
            report_text = latest_report.read_text(encoding="utf-8")
            self.assertIn("PUBLISHED_AUTONOMOUSLY", report_text)
            self.assertIn("cursor-pro-vs-copilot-pro-2026.html", report_text)


    # --------------------------------------------------------------------------
    # 9. Regression: Missing API Key Halts Pipeline with GENERATION_FAILED
    # --------------------------------------------------------------------------
    def test_09_missing_api_key_halts_production_pipeline_with_generation_failed(self):
        """Missing GEMINI_API_KEY must return GENERATION_FAILED, creating no article or ledger entry."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        mock_topic = {
            "topic_id": "TOPIC-KEY-MISSING",
            "primary_keyword": "uncredentialed gemini topic",
            "target_canonical_path": "blog/uncredentialed-gemini-topic.html"
        }
        mock_research = {
            "decision": "TOPIC_SELECTED",
            "reason_code": "TOPIC_QUALIFIED",
            "selected_topic": mock_topic
        }
        mock_missing_key_res = {
            "success": False,
            "status": "GEMINI_KEY_MISSING",
            "generation_method": "NONE",
            "is_gemini_generated": False,
            "model_used": None,
            "html_draft": "",
            "error": "GEMINI_API_KEY environment variable is not configured. Real article generation halted."
        }

        with patch.object(scheduler, "evaluate_daily_research_check", return_value=mock_research), \
             patch("agent.gemini_generator.GeminiArticleGenerator.generate_article", return_value=mock_missing_key_res):

            pipeline_result = scheduler.execute_full_content_pipeline(force_cadence=True)

            self.assertEqual(pipeline_result["pipeline_status"], "GENERATION_FAILED")
            self.assertFalse(pipeline_result["article_generated"])
            self.assertFalse(pipeline_result.get("published", False))
            self.assertIn("CRITICAL INVARIANT", pipeline_result["explanation"])

            # Verify no article written to production
            pub_file = self.workspace / "blog" / "uncredentialed-gemini-topic.html"
            self.assertFalse(pub_file.exists())

            # Verify publication ledger unchanged
            with open(self.pub_ledger_path, "r", encoding="utf-8") as f:
                pub_ledger = json.load(f)
            self.assertEqual(len(pub_ledger["publications"]), 1)

            # Verify control ledger published_history empty
            with open(self.control_ledger_path, "r", encoding="utf-8") as f:
                ctrl_ledger = json.load(f)
            self.assertEqual(len(ctrl_ledger["published_history"]), 0)

            # Verify report in audit_reports/ records failure reason
            latest_report = self.workspace / "audit_reports" / "AUTONOMOUS_PUBLISHER_LATEST.md"
            self.assertTrue(latest_report.exists())
            report_text = latest_report.read_text(encoding="utf-8")
            self.assertIn("GENERATION_FAILED", report_text)
            self.assertIn("GEMINI_API_KEY environment variable is not configured", report_text)

    # --------------------------------------------------------------------------
    # 10. Regression: API Failure Halts Pipeline with GENERATION_FAILED
    # --------------------------------------------------------------------------
    def test_10_api_failure_halts_production_pipeline_with_generation_failed(self):
        """Gemini API failure (e.g. HTTP 500) returns GENERATION_FAILED and stops publication."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        mock_topic = {
            "topic_id": "TOPIC-API-FAIL",
            "primary_keyword": "api failure test topic",
            "target_canonical_path": "blog/api-failure-test-topic.html"
        }
        mock_research = {
            "decision": "TOPIC_SELECTED",
            "reason_code": "TOPIC_QUALIFIED",
            "selected_topic": mock_topic
        }
        mock_api_fail_res = {
            "success": False,
            "status": "GENERATION_FAILED",
            "generation_method": "GEMINI_API",
            "is_gemini_generated": False,
            "model_used": "models/gemini-2.0-flash",
            "html_draft": "",
            "error": "HTTP 500: Internal Server Error from Generative Language API"
        }

        with patch.object(scheduler, "evaluate_daily_research_check", return_value=mock_research), \
             patch("agent.gemini_generator.GeminiArticleGenerator.generate_article", return_value=mock_api_fail_res):

            pipeline_result = scheduler.execute_full_content_pipeline(force_cadence=True)

            self.assertEqual(pipeline_result["pipeline_status"], "GENERATION_FAILED")
            self.assertFalse(pipeline_result["article_generated"])
            self.assertFalse(pipeline_result.get("published", False))

            # Verify no file written and ledgers untouched
            pub_file = self.workspace / "blog" / "api-failure-test-topic.html"
            self.assertFalse(pub_file.exists())

            with open(self.pub_ledger_path, "r", encoding="utf-8") as f:
                pub_ledger = json.load(f)
            self.assertEqual(len(pub_ledger["publications"]), 1)

            with open(self.control_ledger_path, "r", encoding="utf-8") as f:
                ctrl_ledger = json.load(f)
            self.assertEqual(len(ctrl_ledger["published_history"]), 0)

    # --------------------------------------------------------------------------
    # 11. Regression: Model Discovery Failure Halts Production Pipeline
    # --------------------------------------------------------------------------
    def test_11_model_discovery_failure_halts_production_pipeline(self):
        """Model discovery failure must halt the pipeline with GENERATION_FAILED."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        mock_topic = {
            "topic_id": "TOPIC-DISCOVERY-FAIL",
            "primary_keyword": "model discovery fail topic",
            "target_canonical_path": "blog/model-discovery-fail-topic.html"
        }
        mock_research = {
            "decision": "TOPIC_SELECTED",
            "reason_code": "TOPIC_QUALIFIED",
            "selected_topic": mock_topic
        }
        mock_discovery_fail_res = {
            "success": False,
            "status": "GENERATION_FAILED",
            "generation_method": "GEMINI_API",
            "is_gemini_generated": False,
            "model_used": None,
            "html_draft": "",
            "error": "Gemini model discovery failed: No Gemini models supporting generateContent found."
        }

        with patch.object(scheduler, "evaluate_daily_research_check", return_value=mock_research), \
             patch("agent.gemini_generator.GeminiArticleGenerator.generate_article", return_value=mock_discovery_fail_res):

            pipeline_result = scheduler.execute_full_content_pipeline(force_cadence=True)

            self.assertEqual(pipeline_result["pipeline_status"], "GENERATION_FAILED")
            self.assertFalse(pipeline_result["article_generated"])
            self.assertFalse(pipeline_result.get("published", False))

            pub_file = self.workspace / "blog" / "model-discovery-fail-topic.html"
            self.assertFalse(pub_file.exists())

    # --------------------------------------------------------------------------
    # 12. Regression: Heuristic Fallback Strictly Rejected Everywhere
    # --------------------------------------------------------------------------
    def test_12_heuristic_fallback_strictly_rejected_from_autonomous_publishing(self):
        """Heuristic fallback content must NEVER be approved or published to production."""
        fallback_meta = {
            "slug": "fallback-test-article",
            "title": "Fallback Test Article",
            "canonical_url": "https://aidigitools.tech/blog/fallback-test-article.html",
            "is_fallback": True,
            "generation_method": "FALLBACK_HEURISTIC",
            "is_gemini_generated": False
        }

        # 1. prepare_article_preview must raise QualityGateBypassProhibitedError
        with self.assertRaises(QualityGateBypassProhibitedError) as ctx1:
            self.engine.prepare_article_preview(
                slug=fallback_meta["slug"],
                title=fallback_meta["title"],
                html_content=self.sample_html,
                metadata=fallback_meta,
                quality_gate_report={"decision": "APPROVED", "failed_gates_count": 0}
            )
        self.assertIn("heuristic fallback", str(ctx1.exception).lower())

        # 2. publish_verified_article must raise QualityGateBypassProhibitedError
        with self.assertRaises(QualityGateBypassProhibitedError) as ctx2:
            self.engine.publish_verified_article(
                slug=fallback_meta["slug"],
                title=fallback_meta["title"],
                html_content=self.sample_html,
                canonical_url=fallback_meta["canonical_url"],
                metadata=fallback_meta,
                dry_run=False
            )
        self.assertIn("heuristic fallback", str(ctx2.exception).lower())

        # 3. Pipeline execution with fallback generation result halts with GENERATION_FAILED
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        mock_topic = {
            "topic_id": "TOPIC-FALLBACK",
            "primary_keyword": "fallback test topic",
            "target_canonical_path": "blog/fallback-test-article.html"
        }
        mock_research = {
            "decision": "TOPIC_SELECTED",
            "reason_code": "TOPIC_QUALIFIED",
            "selected_topic": mock_topic
        }
        mock_fallback_gen_res = {
            "success": True,
            "status": "FALLBACK_AFTER_FAILURE",
            "generation_method": "FALLBACK_HEURISTIC",
            "is_gemini_generated": False,
            "is_fallback": True,
            "model_used": None,
            "html_draft": self.sample_html,
            "error": "Gemini generation failed: Model endpoint error. Fallback generated for dev/test."
        }

        with patch.object(scheduler, "evaluate_daily_research_check", return_value=mock_research), \
             patch("agent.gemini_generator.GeminiArticleGenerator.generate_article", return_value=mock_fallback_gen_res):

            pipeline_result = scheduler.execute_full_content_pipeline(force_cadence=True)

            self.assertEqual(pipeline_result["pipeline_status"], "GENERATION_FAILED")
            self.assertFalse(pipeline_result["article_generated"])
            self.assertFalse(pipeline_result.get("published", False))

            pub_file = self.workspace / "blog" / "fallback-test-article.html"
            self.assertFalse(pub_file.exists())

            with open(self.pub_ledger_path, "r", encoding="utf-8") as f:
                pub_ledger = json.load(f)
            self.assertEqual(len(pub_ledger["publications"]), 1)

    # --------------------------------------------------------------------------
    # 13. Regression: _generate_compliant_article_draft Prohibits Fallback
    # --------------------------------------------------------------------------
    def test_13_generate_compliant_article_draft_disallows_fallback(self):
        """_generate_compliant_article_draft passes allow_fallback=False and raises on failure."""
        scheduler = AutomationScheduler(workspace_root=self.workspace)
        mock_failed_res = {
            "success": False,
            "status": "GENERATION_FAILED",
            "generation_method": "NONE",
            "is_gemini_generated": False,
            "html_draft": "",
            "error": "Model failure"
        }

        with patch("agent.gemini_generator.GeminiArticleGenerator.generate_article", return_value=mock_failed_res) as mock_gen:
            with self.assertRaises(RuntimeError) as ctx:
                scheduler._generate_compliant_article_draft(
                    slug="test-slug",
                    title="Test Title",
                    canonical_url="https://aidigitools.tech/blog/test-slug.html",
                    topic_info={"primary_keyword": "test"}
                )
            mock_gen.assert_called_once_with(
                topic_info={"primary_keyword": "test"},
                canonical_url="https://aidigitools.tech/blog/test-slug.html",
                allow_fallback=False
            )
            self.assertIn("Heuristic fallback content is strictly prohibited", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
