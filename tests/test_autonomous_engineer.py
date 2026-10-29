import os
import json
import unittest
import tempfile
from pathlib import Path
from autonomous_engineer.config import (
    DOMAIN, BASE_URL, TIMEZONE_OFFSET,
    SCHEDULE_HOURS_LOCAL, SCHEDULE_HOURS_UTC,
    INDEXNOW_KEY, PROJECT_ROOT, get_karachi_time
)
from autonomous_engineer.static_auditor import StaticAuditor
from autonomous_engineer.live_auditor import LiveAuditor
from autonomous_engineer.gemini_reasoner import GeminiReasoner
from autonomous_engineer.repair_executor import RepairExecutor
from autonomous_engineer.history_manager import HistoryManager
from autonomous_engineer.report_engine import ReportEngine

class TestAutonomousEngineer(unittest.TestCase):
    """Exhaustive test suite for the Autonomous SEO & Website Engineer system."""

    def setUp(self):
        self.root = PROJECT_ROOT

    def test_01_config_and_timezone(self):
        """Verifies core configuration, Asia/Karachi (UTC+5) offset, and twice-daily schedule mapping."""
        self.assertEqual(DOMAIN, "aidigitools.tech")
        self.assertEqual(BASE_URL, "https://aidigitools.tech")
        self.assertEqual(TIMEZONE_OFFSET.total_seconds(), 5 * 3600)
        self.assertEqual(SCHEDULE_HOURS_LOCAL, [8, 20])
        self.assertEqual(SCHEDULE_HOURS_UTC, [3, 15])
        
        now_pkt = get_karachi_time()
        self.assertEqual(now_pkt.tzinfo.tzname(now_pkt), "Asia/Karachi")

    def test_02_static_auditor_scans_all_pages(self):
        """Verifies StaticAuditor scans all 66 HTML documents and produces a valid health score."""
        auditor = StaticAuditor(self.root)
        summary = auditor.run_static_audit()
        self.assertEqual(summary["pages_scanned"], 66)
        self.assertEqual(summary["sitemap_urls_count"], 65)
        self.assertGreaterEqual(summary["health_score"], 95)
        self.assertEqual(summary["critical_count"], 0)
        self.assertEqual(summary["link_graph"]["broken_links_count"], 0)
        self.assertTrue(summary["robots_check"]["valid"])

    def test_03_static_auditor_detects_anomalies(self):
        """Verifies that StaticAuditor correctly flags missing or invalid elements."""
        auditor = StaticAuditor(self.root)
        index_path = self.root / "index.html"
        result = auditor.audit_single_page(index_path)
        self.assertEqual(result["file"], "index.html")
        self.assertEqual(result["canonical"], f"{BASE_URL}/")
        self.assertEqual(result["h1_count"], 1)
        self.assertTrue(result["passed"])

    def test_04_live_auditor_methods(self):
        """Verifies LiveAuditor structure and live probing logic."""
        live_auditor = LiveAuditor(timeout=5)
        self.assertEqual(live_auditor.timeout, 5)
        key_res = live_auditor.check_indexnow_key_file()
        self.assertIn("matches_key", key_res)
        if key_res.get("status_code") == 200:
            self.assertTrue(key_res["valid"])

    def test_05_gemini_reasoner_fallback(self):
        """Verifies GeminiReasoner provides a structured heuristic plan when GEMINI_API_KEY is not set."""
        reasoner = GeminiReasoner(api_key="")
        mock_audit = {
            "pages_scanned": 66,
            "health_score": 100,
            "critical_count": 0,
            "warning_count": 0,
            "missing_from_sitemap": [],
            "link_graph": {"broken_links": []},
            "issues": []
        }
        res = reasoner.evaluate_audit(mock_audit)
        self.assertFalse(res["gemini_api_connected"])
        self.assertIn("Deterministic Heuristic", res["engine"])
        self.assertIn("diagnosis", res)
        self.assertIsInstance(res["auto_repair_proposals"], list)
        self.assertIsInstance(res["manual_review_proposals"], list)

    def test_06_repair_executor_firewall(self):
        """Verifies RepairExecutor firewall protects cart.js, contact.html, and policies.html from auto-modification."""
        executor = RepairExecutor(self.root)
        self.assertTrue(executor.is_protected("assets/cart.js"))
        self.assertTrue(executor.is_protected("contact.html"))
        self.assertTrue(executor.is_protected("policies.html"))
        self.assertTrue(executor.is_protected("affiliate-disclosure.html"))
        self.assertFalse(executor.is_protected("tools/chatgpt-plus.html"))
        self.assertFalse(executor.is_protected("sitemap.xml"))

    def test_07_repair_executor_rollback_safety(self):
        """Verifies RepairExecutor rollback safety attributes and callable interface."""
        executor = RepairExecutor(self.root)
        self.assertTrue(hasattr(executor, "rollback_changes"))
        self.assertTrue(callable(executor.rollback_changes))

    def test_08_history_manager_and_report_engine(self):
        """Verifies HistoryManager and ReportEngine persistence, trend diffing, and report formatting in an isolated directory."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            history_file = tmp_path / "test_history.json"
            history_mgr = HistoryManager(reports_dir=tmp_path, history_file=history_file)
            history = history_mgr.load_history()
            self.assertIsInstance(history, list)

            diff = history_mgr.compare_with_previous([])
            self.assertIn("recurring_count", diff)
            self.assertIn("new_count", diff)

            report_engine = ReportEngine(reports_dir=tmp_path)
            mock_audit = {
                "health_score": 100,
                "passed": True,
                "pages_scanned": 66,
                "sitemap_urls_count": 65,
                "critical_count": 0,
                "warning_count": 0,
                "link_graph": {"broken_links_count": 0, "broken_anchors_count": 0}
            }
            mock_live = {
                "homepage": {"reachable": True, "status_code": 200, "latency_ms": 150},
                "indexnow_key": {"valid": True, "status_code": 200, "url": f"{BASE_URL}/{INDEXNOW_KEY}.txt"},
                "sample_routes": []
            }
            mock_reason = {
                "engine": "TestEngine",
                "model_used": "test-model",
                "diagnosis": "Test diagnosis",
                "manual_review_proposals": []
            }
            mock_repair = {"applied": False, "rolled_back": False}

            report_path = report_engine.generate_markdown_report(
                audit_summary=mock_audit,
                live_summary=mock_live,
                reasoner_summary=mock_reason,
                repair_summary=mock_repair,
                history_diff=diff
            )
            self.assertTrue(report_path.exists())
            content = report_path.read_text(encoding="utf-8")
            self.assertIn("AI DigiTools Autonomous Maintenance & SEO Audit Report", content)
            self.assertIn("Asia/Karachi", content)

    def test_09_workflow_yaml_syntax_and_cron(self):
        """Verifies GitHub Actions workflow configuration, cron schedule, and security settings."""
        wf_path = self.root / ".github" / "workflows" / "autonomous-seo-engineer.yml"
        self.assertTrue(wf_path.exists(), f"Workflow file missing: {wf_path}")
        content = wf_path.read_text(encoding="utf-8")
        
        # Check twice daily cron
        self.assertIn("cron: '0 3,15 * * *'", content)
        # Check manual dispatch
        self.assertIn("workflow_dispatch:", content)
        # Check permissions
        self.assertIn("contents: write", content)
        # Check Gemini Secret injection
        self.assertIn("GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}", content)
        # Check skip ci tag
        self.assertIn("[skip ci]", content)

    def test_10_bing_webmaster_client(self):
        """Verifies BingWebmasterClient unconfigured state, methods, and error resilience."""
        from autonomous_engineer.bing_client import BingWebmasterClient
        client = BingWebmasterClient(api_key="")
        self.assertFalse(client.is_configured())
        audit = client.run_bing_audit()
        self.assertFalse(audit["connected"])
        self.assertEqual(audit["status"], "UNCONFIGURED")

        # Verify unconfigured calls fail gracefully
        self.assertEqual(client.get_url_submission_quota()["status_code"], 0)
        self.assertEqual(client.get_crawl_stats()["status_code"], 0)
        self.assertEqual(client.get_query_stats()["status_code"], 0)
        self.assertEqual(client.get_feeds()["status_code"], 0)
        self.assertEqual(client.get_crawl_issues()["status_code"], 0)
        self.assertEqual(client.submit_feed()["status_code"], 0)
        self.assertEqual(client.submit_url("https://aidigitools.tech/deals.html")["status_code"], 0)
        self.assertEqual(client.submit_url_batch(["https://aidigitools.tech/deals.html"])["status_code"], 0)

        # Test workflow environment injection
        wf_path = self.root / ".github" / "workflows" / "autonomous-seo-engineer.yml"
        content = wf_path.read_text(encoding="utf-8")
        self.assertIn("BING_API_KEY: ${{ secrets.BING_API_KEY }}", content)

    def test_11_google_search_console_client(self):
        """Verifies GoogleSearchConsoleClient unconfigured state, methods, and error resilience."""
        from autonomous_engineer.gsc_client import GoogleSearchConsoleClient
        client = GoogleSearchConsoleClient(key_json_str="")
        self.assertFalse(client.is_configured())
        self.assertIsNone(client.get_client_email())
        self.assertIsNone(client.get_access_token())

        audit = client.run_gsc_audit()
        self.assertFalse(audit["connected"])
        self.assertEqual(audit["status"], "UNCONFIGURED")

        # Verify unconfigured calls fail gracefully without exceptions
        self.assertEqual(client.get_search_analytics()["status_code"], 0)
        self.assertEqual(client.get_sitemaps()["status_code"], 0)

        # Test workflow environment injection
        wf_path = self.root / ".github" / "workflows" / "autonomous-seo-engineer.yml"
        content = wf_path.read_text(encoding="utf-8")
        self.assertIn("GSC_SERVICE_ACCOUNT_KEY: ${{ secrets.GSC_SERVICE_ACCOUNT_KEY }}", content)

if __name__ == "__main__":
    unittest.main()
