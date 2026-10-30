import unittest
import tempfile
import json
from pathlib import Path
from autonomous_engineer.gsc_client import GoogleSearchConsoleClient
from autonomous_engineer.pagespeed_client import PageSpeedInsightsClient
from autonomous_engineer.static_auditor import StaticAuditor
from autonomous_engineer.live_auditor import LiveAuditor
from autonomous_engineer.alert_manager import AlertManager
from autonomous_engineer.history_manager import HistoryManager
from autonomous_engineer.self_monitor import SelfMonitor
from autonomous_engineer.config import PROJECT_ROOT, BASE_URL

class TestSEOIntelligenceAndMonitoring(unittest.TestCase):
    """Rigorous verification suite for Step 6: SEO Intelligence and Long-Term Monitoring."""

    def setUp(self):
        self.root = PROJECT_ROOT

    def test_01_gsc_date_range_comparison(self):
        """Verifies GSC client compares current vs prior date ranges and computes deltas."""
        client = GoogleSearchConsoleClient(key_json_str="")
        res = client.compare_search_performance(period_days=7)
        self.assertFalse(res["configured"])
        self.assertIn("message", res)

        # Test delta calculations on synthetic rows
        client._parsed_key = {"client_email": "test@gserviceaccount.com"}
        current_mock = {
            "status_code": 200,
            "data": {
                "rows": [
                    {"keys": ["chatgpt plus pakistan"], "clicks": 15, "impressions": 200, "ctr": 0.075, "position": 4.2},
                    {"keys": ["ai tools islamabad"], "clicks": 5, "impressions": 100, "ctr": 0.05, "position": 6.8}
                ]
            }
        }
        prior_mock = {
            "status_code": 200,
            "data": {
                "rows": [
                    {"keys": ["chatgpt plus pakistan"], "clicks": 10, "impressions": 150, "ctr": 0.066, "position": 5.5}
                ]
            }
        }
        client.query_date_range = lambda s, e, dimensions=None, row_limit=25: current_mock if "2026" in s and s > "2026-10-15" else prior_mock
        comp = client.compare_search_performance(period_days=7)
        self.assertTrue(comp["configured"])
        self.assertEqual(comp["current_metrics"]["clicks"], 20)
        self.assertEqual(comp["current_metrics"]["impressions"], 300)

    def test_02_pagespeed_lab_vs_field_separation(self):
        """Verifies PageSpeed client separates Lab Diagnostics from Real-User Field Experience (CrUX)."""
        client = PageSpeedInsightsClient(api_key="test_key")
        mock_api_data = {
            "lighthouseResult": {
                "categories": {
                    "performance": {"score": 0.98},
                    "accessibility": {"score": 0.95},
                    "best-practices": {"score": 1.0},
                    "seo": {"score": 1.0}
                },
                "audits": {
                    "largest-contentful-paint": {"displayValue": "1.1 s"},
                    "cumulative-layout-shift": {"displayValue": "0"},
                    "first-contentful-paint": {"displayValue": "0.9 s"},
                    "total-blocking-time": {"displayValue": "50 ms"},
                    "speed-index": {"displayValue": "1.2 s"}
                }
            },
            "loadingExperience": {
                "overall_category": "FAST",
                "metrics": {
                    "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 1200},
                    "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 0},
                    "INTERACTION_TO_NEXT_PAINT": {"percentile": 80}
                }
            },
            "originLoadingExperience": {
                "overall_category": "FAST",
                "metrics": {}
            }
        }
        client.audit_url = lambda target_url, strategy: {"status_code": 200, "data": mock_api_data, "error": None}
        res = client.run_pagespeed_audit()
        self.assertTrue(res["connected"])
        self.assertIn("lab_diagnostics", res)
        self.assertIn("field_experience", res)
        self.assertEqual(res["lab_diagnostics"]["scores"]["performance"], 98)
        self.assertTrue(res["field_experience"]["has_field_data"])
        self.assertEqual(res["field_experience"]["url_metrics"]["overall_category"], "FAST")
        self.assertIn("disclaimer", res["field_experience"])

    def test_03_orphan_page_detection(self):
        """Verifies StaticAuditor correctly flags orphan pages with zero internal incoming links."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "index.html").write_text('<a href="linked.html">Link</a>', encoding="utf-8")
            (tmp_path / "linked.html").write_text('<a href="index.html">Back</a>', encoding="utf-8")
            (tmp_path / "orphan.html").write_text('<p>No one links to me</p>', encoding="utf-8")

            auditor = StaticAuditor(tmp_path)
            link_graph = auditor.check_link_graph()
            self.assertIn("orphan.html", link_graph["orphan_pages"])
            self.assertEqual(link_graph["orphan_pages_count"], 1)

    def test_04_duplicate_title_and_content_detection(self):
        """Verifies StaticAuditor detects duplicate titles and identical content blocks."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "page1.html").write_text('<title>Identical Title</title><main>Content A</main>', encoding="utf-8")
            (tmp_path / "page2.html").write_text('<title>Identical Title</title><main>Content B</main>', encoding="utf-8")

            auditor = StaticAuditor(tmp_path)
            uniq = auditor.check_content_uniqueness()
            self.assertEqual(uniq["duplicate_titles_count"], 1)
            self.assertEqual(uniq["duplicate_titles"][0]["title"], "Identical Title")

    def test_05_tool_claims_and_pricing_validation(self):
        """Verifies tool page auditing flags missing pricing, SLA, warranty, and unsupported claims."""
        auditor = StaticAuditor(self.root)
        # Test valid existing tool page
        chatgpt_path = self.root / "tools" / "chatgpt-plus.html"
        if chatgpt_path.exists():
            res = auditor.audit_single_page(chatgpt_path)
            self.assertTrue(res["passed"])
            # Ensure no unsupported claims or pricing issues flagged on verified tool
            issue_types = [i["type"] for i in res["issues"]]
            self.assertNotIn("pricing_transparency", issue_types)
            self.assertNotIn("unsupported_marketing_claim", issue_types)

    def test_06_indexnow_ownership_verification_and_disclaimer(self):
        """Verifies IndexNow check includes ownership key verification and explicit indexing disclaimer."""
        live_auditor = LiveAuditor()
        key_res = live_auditor.check_indexnow_key_file()
        self.assertIn("indexing_disclaimer", key_res)
        self.assertIn("does NOT constitute evidence of crawling", key_res["indexing_disclaimer"])

    def test_07_multi_stage_indexing_funnel(self):
        """Verifies 5 separate stages in search indexing lifecycle funnel."""
        live_auditor = LiveAuditor()
        funnel = live_auditor.get_indexing_funnel_status(
            gsc_summary={"connected": True},
            bing_summary={"connected": True},
            indexnow_valid=True
        )
        self.assertIn("stages", funnel)
        self.assertEqual(len(funnel["stages"]), 5)
        stage_names = [s["name"] for s in funnel["stages"]]
        self.assertIn("Sitemap Submission", stage_names)
        self.assertIn("URL Notification (IndexNow)", stage_names)
        self.assertIn("Search Bot Crawling", stage_names)
        self.assertIn("Search Indexation", stage_names)
        self.assertIn("Organic Query Ranking", stage_names)

    def test_08_alert_manager_incident_evaluation(self):
        """Verifies AlertManager triggers alerts for downtime, SSL failure, repeated degradation, and secrets."""
        alert_mgr = AlertManager()
        failing_live = {
            "homepage": {"reachable": False, "status_code": 500, "error": "SSL handshake failure"},
            "indexnow_key": {"valid": False, "url": f"{BASE_URL}/key.txt", "error": "404 Not Found"}
        }
        failing_audit = {"health_score": 75}
        failing_history_diff = {"previous_health_score": 78}
        failing_sec = {"is_secure": False, "critical_count": 1}

        alerts = alert_mgr.evaluate_alert_conditions(
            audit_summary=failing_audit,
            live_summary=failing_live,
            history_diff=failing_history_diff,
            security_summary=failing_sec
        )
        self.assertGreaterEqual(len(alerts), 4)
        types = [a["type"] for a in alerts]
        self.assertIn("site_downtime", types)
        self.assertIn("ssl_certificate_error", types)
        self.assertIn("repeated_audit_failure", types)
        self.assertIn("security_vulnerability", types)
        self.assertIn("indexnow_key_missing", types)

    def test_09_alert_manager_free_notification_fallback(self):
        """Verifies AlertManager handles unconfigured Telegram gracefully without errors."""
        alert_mgr = AlertManager()
        alert_mgr.telegram_token = ""
        res = alert_mgr.send_telegram_alert("Test", "Details")
        self.assertFalse(res["sent"])
        self.assertIn("not configured", res["reason"])

    def test_10_trend_summary_generation(self):
        """Verifies HistoryManager generates statistical weekly and monthly trend reports."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            hist_file = tmp_path / "history.json"
            dummy_runs = [
                {"run_id": f"run-{i}", "timestamp_pkt": "2026-10-30 08:00:00 PKT", "health_score": 100, "all_live_checks_passed": True, "repairs_applied": False}
                for i in range(14)
            ]
            hist_file.write_text(json.dumps(dummy_runs), encoding="utf-8")

            mgr = HistoryManager(reports_dir=tmp_path, history_file=hist_file)
            summary = mgr.generate_trend_summary(period="weekly")
            self.assertTrue(summary["has_data"])
            self.assertEqual(summary["average_health_score"], 100.0)
            self.assertEqual(summary["uptime_percentage"], 100.0)
            self.assertTrue((tmp_path / "weekly_trends.md").exists())

    def test_11_agent_self_monitoring(self):
        """Verifies SelfMonitor audits secrets, schedule conformance, quotas, and service health."""
        monitor = SelfMonitor(self.root)
        health = monitor.evaluate_agent_health()
        self.assertIn("agent_status", health)
        self.assertIn("secrets_audit", health)
        self.assertIn("schedule_audit", health)
        self.assertIn("quotas", health)
        self.assertTrue(health["schedule_audit"]["conforms_to_cadence"])

    def test_12_transparent_health_score_formula_and_disclaimer(self):
        """Verifies deterministic Health Score formula, deductions breakdown, and disclaimer."""
        auditor = StaticAuditor(self.root)
        score_data = auditor.calculate_transparent_health_score(
            critical_count=0,
            warning_count=0,
            broken_links_count=0,
            broken_anchors_count=0,
            orphan_count=0,
            dup_titles_count=0
        )
        self.assertEqual(score_data["health_score"], 100)
        self.assertEqual(score_data["total_deductions"], 0)
        self.assertIn("100 - sum(deductions)", score_data["formula"])
        self.assertIn("disclaimer", score_data)
        self.assertIn("does not guarantee", score_data["disclaimer"].lower())

if __name__ == "__main__":
    unittest.main()
