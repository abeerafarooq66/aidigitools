"""
AIDigiTools — Production Verification & Regression Test Battery
================================================================
Verifies all 15 mandatory production invariants:
1. QualityGateEngine.evaluate_article() receives structured metadata & never crashes with TypeError.
2. Gemini generation request uses configured API client and model payload.
3. Static placeholder templates cannot be reported as Gemini-generated content.
4. Missing Gemini credentials do not result in fabricated article success.
5. Local HTML with live HTTP 404 is not marked healthy.
6. Skipped HTTP checks never count as live verified.
7. 64 skipped URLs cannot produce a 65-healthy live audit.
8. GSC read access does not imply sitemap write permission.
9. Google Ads credentials alone do not produce VERIFIED.
10. CrUX authenticated-but-no-data is recorded accurately.
11. Integration status is genuinely persisted and exported.
12. Topic selection is not counted as article generation.
13. Phase 1 never publishes without approval.
14. Successful deployment triggers discovery exactly once.
15. Indexing submissions never imply guaranteed indexing.
"""

import os
import sys
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Workspace path setup
ROOT_DIR = Path(__file__).resolve().parent.parent
SEO_AGENT_DIR = ROOT_DIR / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from agent.indexing_notifier import (
    IndexingNotifierEngine,
    NO_INDEXING_GUARANTEE_DISCLAIMER
)
from agent.automation_scheduler import AutomationScheduler
from agent.publishing_control import (
    PublishingControlEngine,
    PHASE_1_SUPERVISED
)
from agent.quality_gates import QualityGateEngine
from agent.gemini_generator import GeminiArticleGenerator
import scripts.credentials_preflight as preflight


class TestProductionVerificationRegression(unittest.TestCase):
    def setUp(self):
        self.workspace_root = ROOT_DIR
        self.notifier = IndexingNotifierEngine(self.workspace_root)
        self.scheduler = AutomationScheduler(self.workspace_root)
        self.pub_control = PublishingControlEngine(self.workspace_root)
        self.gate_engine = QualityGateEngine(self.workspace_root)

    def tearDown(self):
        # Clean up any test preview or live files
        for f in (self.workspace_root / "data" / "previews").glob("test-*.html"):
            try:
                f.unlink()
            except Exception:
                pass
        for f in (self.workspace_root / "blog").glob("test-*.html"):
            try:
                f.unlink()
            except Exception:
                pass
        # Clean up pending test previews from ledger
        try:
            with open(self.pub_control.control_ledger_path, "r", encoding="utf-8") as f:
                c_data = json.load(f)
            c_data["pending_previews"] = [p for p in c_data.get("pending_previews", []) if not p.get("slug", "").startswith("test-")]
            with open(self.pub_control.control_ledger_path, "w", encoding="utf-8") as f:
                json.dump(c_data, f, indent=2)
        except Exception:
            pass

    # --------------------------------------------------------------------------
    # 1. QualityGateEngine.evaluate_article() Invocation & Metadata
    # --------------------------------------------------------------------------
    def test_01_quality_gates_evaluate_article_invocation_and_metadata(self):
        html_sample = """<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Test</h1></body></html>"""
        metadata = {
            "slug": "test-cursor-article",
            "title": "Cursor AI Developer Guide (2026)",
            "primary_keyword": "cursor ai developer guide",
            "canonical_url": "https://aidigitools.tech/blog/test-cursor-article.html",
            "cluster_slug": "ai-coding-and-development",
            "article_type": "guide",
            "author_slug": "abeera-farooq"
        }

        # Must accept metadata dictionary without TypeError
        result1 = self.gate_engine.evaluate_article(html_content=html_sample, metadata=metadata)
        self.assertIn("decision", result1)
        self.assertIn("passed_gates_count", result1)

        # Must also accept kwargs without TypeError (backward compatibility safeguard)
        result2 = self.gate_engine.evaluate_article(
            html_content=html_sample,
            slug="test-cursor-article",
            title="Cursor AI Developer Guide (2026)",
            primary_keyword="cursor ai developer guide"
        )
        self.assertIn("decision", result2)

        # Incomplete HTML must fail quality gates and yield DO NOT PUBLISH
        self.assertEqual(result1["decision"], "DO NOT PUBLISH")
        self.assertGreater(result1["failed_gates_count"], 0)

    # --------------------------------------------------------------------------
    # 2. Gemini generation request uses configured API client
    # --------------------------------------------------------------------------
    def test_02_gemini_generation_request_uses_configured_api(self):
        generator = GeminiArticleGenerator(
            api_key="AIzaSyD-FakeGeminiTestKeyForMockingOnly12345",
            workspace_root=self.workspace_root
        )
        topic_info = {
            "primary_keyword": "Claude 3.5 Sonnet Coding Workflow",
            "cluster_slug": "ai-coding-and-development",
            "article_type": "guide",
            "editorial_rationale": "Developer workflows with Claude 3.5 Sonnet."
        }
        canonical_url = "https://aidigitools.tech/blog/claude-coding-workflow.html"

        mock_gemini_response = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Claude 3.5 Sonnet Coding Workflow — AIDigiTools</title>
  <meta name="description" content="Guide for Claude 3.5 Sonnet coding. Authentic pricing in PKR and USD, payment options via EasyPaisa and JazzCash, delivery SLA, and full comparison.">
  <link rel="canonical" href="https://aidigitools.tech/blog/claude-coding-workflow.html">
  <meta name="robots" content="index, follow">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "Claude 3.5 Sonnet Coding Workflow",
    "author": {"@type": "Person", "name": "Abeera Farooq"}
  }
  </script>
</head>
<body>
  <header>
    <div class="reseller-badge"><strong>Independent Reseller & Service Desk:</strong> AIDigiTools is an independent concierge. <a href="https://aidigitools.tech/affiliate-disclosure.html">Reseller & Trademark Policy</a></div>
  </header>
  <main>
    <article>
      <h1>Claude 3.5 Sonnet Coding Workflow</h1>
      <p class="quick-answer">Claude 3.5 Sonnet coding workflow delivers premier reasoning for software engineering. On AIDigiTools, seats cost Rs. 4,500 PKR ($16 USD) with activation via WhatsApp within 15 minutes, local payments through EasyPaisa, JazzCash, or Raast, and our verified 30-day replacement warranty.</p>
      <p class="evidence-tier"><strong>Evidence Classification:</strong> Tier B: Research-based and verified technical releases tested by AIDigiTools engineers.</p>
      <h2>Overview & Architecture</h2>
      <p>Tested by AIDigiTools engineers based on verified technical releases from Anthropic.</p>
      <h2>Direct Comparison Matrix</h2>
      <table>
        <thead><tr><th>Plan</th><th>Price (PKR)</th><th>Price (USD)</th></tr></thead>
        <tbody><tr><td>Pro Seat</td><td>Rs. 4,500 PKR</td><td>$16 USD</td></tr></tbody>
      </table>
      <h2>How to Order via WhatsApp Concierge</h2>
      <p>Order at <a href="https://wa.me/923326861112">03326861112</a> via <a href="https://aidigitools.tech/policies/payment-methods.html">payment methods</a> or view our <a href="https://aidigitools.tech/#tools">catalog</a>.</p>
      <img src="https://aidigitools.tech/assets/images/logo.png" alt="Claude coding preview">
      <details><summary>Payment methods?</summary><p>EasyPaisa and JazzCash.</p></details>
      <details><summary>Warranty?</summary><p>30 days replacement.</p></details>
      <details><summary>Delivery SLA?</summary><p>15 minutes via WhatsApp.</p></details>
    </article>
  </main>
</body>
</html>"""
                            }
                        ]
                    }
                }
            ]
        }

        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_resp = MagicMock()
            mock_resp.status = 200
            mock_resp.read.return_value = json.dumps(mock_gemini_response).encode("utf-8")
            mock_urlopen.return_value.__enter__.return_value = mock_resp

            result = generator.generate_article(topic_info, canonical_url)
            self.assertTrue(result["success"])
            self.assertEqual(result["status"], "ARTICLE_GENERATED")
            self.assertEqual(result["generation_method"], "GEMINI_API")
            self.assertTrue(result["is_gemini_generated"])
            self.assertIsNotNone(result["model_used"])
            self.assertIn("Claude 3.5 Sonnet Coding Workflow", result["html_draft"])

    # --------------------------------------------------------------------------
    # 3. Static placeholder templates cannot be reported as Gemini-generated
    # --------------------------------------------------------------------------
    def test_03_static_placeholder_cannot_be_reported_as_gemini(self):
        generator = GeminiArticleGenerator(api_key=None, workspace_root=self.workspace_root)
        fallback_html = generator.generate_heuristic_fallback(
            topic_info={"primary_keyword": "Fallback Testing"},
            canonical_url="https://aidigitools.tech/blog/fallback.html"
        )
        self.assertIsInstance(fallback_html, str)

        # Running generation with allow_fallback=True returns FALLBACK_HEURISTIC, NOT GEMINI_API
        res = generator.generate_article(
            topic_info={"primary_keyword": "Fallback Testing"},
            canonical_url="https://aidigitools.tech/blog/fallback.html",
            allow_fallback=True
        )
        self.assertFalse(res["is_gemini_generated"], "Heuristic fallback MUST NOT claim is_gemini_generated=True")
        self.assertEqual(res["generation_method"], "FALLBACK_HEURISTIC")
        self.assertNotEqual(res["generation_method"], "GEMINI_API")

    # --------------------------------------------------------------------------
    # 4. Missing Gemini credentials do not result in fabricated article success
    # --------------------------------------------------------------------------
    def test_04_missing_gemini_credentials_reports_missing_key(self):
        generator = GeminiArticleGenerator(api_key="", workspace_root=self.workspace_root)
        res = generator.generate_article(
            topic_info={"primary_keyword": "Uncredentialed Topic"},
            canonical_url="https://aidigitools.tech/blog/uncredentialed.html",
            allow_fallback=False
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["status"], "GEMINI_KEY_MISSING")
        self.assertFalse(res["is_gemini_generated"])
        self.assertEqual(res["html_draft"], "")

    # --------------------------------------------------------------------------
    # 5. Local HTML with live HTTP 404 is NOT healthy
    # --------------------------------------------------------------------------
    def test_05_local_html_with_live_http_404_is_not_healthy(self):
        url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        mock_live_failed = {
            "status": "LIVE_HTTP_FAILED",
            "http_code": 404,
            "final_url": url,
            "live_canonical": url,
            "issues": ["HTTP status code is 404 (expected 200)."]
        }

        audit_res = self.notifier.run_technical_indexing_audit(
            check_live_http=True,
            verify_live_sitemap=False,
            live_http_mock=mock_live_failed
        )
        record = audit_res["urls"].get(url)
        self.assertIsNotNone(record)
        self.assertNotEqual(record["status"], "HEALTHY", "URL with live HTTP 404 must not be HEALTHY")
        self.assertEqual(record["status"], "LIVE_HTTP_FAILED")
        self.assertEqual(record["http_status"], 404)
        self.assertGreater(audit_res["total_issues"], 0)

    # --------------------------------------------------------------------------
    # 6. Skipped HTTP checks never count as live verified
    # --------------------------------------------------------------------------
    def test_06_skipped_http_checks_never_count_as_live_verified(self):
        url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        res = self.notifier.verify_technical_indexability(url, check_live_http=False)

        self.assertEqual(res["checks"]["live_http_status"], "SKIPPED")
        self.assertEqual(res["checks"]["http_200"], "SKIPPED")

        audit_res = self.notifier.run_technical_indexing_audit(check_live_http=False, verify_live_sitemap=False)
        record = audit_res["urls"].get(url)
        self.assertEqual(record["http_status"], "SKIPPED")
        self.assertEqual(record["live_http_status"], "SKIPPED")
        self.assertEqual(record["status"], "LOCAL_VALID_LIVE_SKIPPED")
        self.assertNotEqual(record["status"], "HEALTHY")

    # --------------------------------------------------------------------------
    # 7. 64 skipped URLs cannot produce a 65-healthy live audit
    # --------------------------------------------------------------------------
    def test_07_64_skipped_urls_cannot_produce_65_healthy_audit(self):
        audit_res = self.notifier.run_technical_indexing_audit(
            check_live_http=False,
            verify_live_sitemap=False,
            save_ledger=False
        )
        self.assertEqual(audit_res["total_healthy"], 0, "When live HTTP is skipped, total_healthy must be 0, never 65")
        self.assertEqual(audit_res["total_skipped"], audit_res["total_urls_audited"])
        self.assertEqual(audit_res["audit_mode"], "LOCAL_PREFLIGHT_ONLY_LIVE_SKIPPED")

    # --------------------------------------------------------------------------
    # 8. GSC read access does not imply sitemap write permission
    # --------------------------------------------------------------------------
    def test_08_gsc_read_access_does_not_imply_sitemap_write_permission(self):
        mock_sa = MagicMock()
        mock_creds = MagicMock()
        mock_creds.token = "mock_gsc_token"
        mock_sa.Credentials.from_service_account_info.return_value = mock_creds

        mock_google = MagicMock()
        mock_google.oauth2 = MagicMock(service_account=mock_sa)
        mock_google.oauth2.service_account = mock_sa
        mock_google.auth = MagicMock()
        mock_google.auth.transport = MagicMock()
        mock_google.auth.transport.requests = MagicMock()

        modules_patch = {
            "google": mock_google,
            "google.oauth2": mock_google.oauth2,
            "google.oauth2.service_account": mock_sa,
            "google.auth": mock_google.auth,
            "google.auth.transport": mock_google.auth.transport,
            "google.auth.transport.requests": mock_google.auth.transport.requests
        }

        with patch.dict(sys.modules, modules_patch):
            with patch.dict(os.environ, {"GSC_SERVICE_ACCOUNT_KEY": '{"client_email": "test@test.iam.gserviceaccount.com"}'}):
                self.notifier._get_gsc_access_token(write_scope=False)
                mock_sa.Credentials.from_service_account_info.assert_called_with(
                    {"client_email": "test@test.iam.gserviceaccount.com"},
                    scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
                )

                self.notifier._get_gsc_access_token(write_scope=True)
                mock_sa.Credentials.from_service_account_info.assert_called_with(
                    {"client_email": "test@test.iam.gserviceaccount.com"},
                    scopes=["https://www.googleapis.com/auth/webmasters"]
                )

    # --------------------------------------------------------------------------
    # 9. Google Ads credentials alone do not produce VERIFIED
    # --------------------------------------------------------------------------
    def test_09_google_ads_credentials_alone_do_not_produce_verified(self):
        env_vars = {
            "GOOGLE_ADS_CUSTOMER_ID": "2913849282",
            "GOOGLE_ADS_MANAGER_ID": "1826247360",
            "GOOGLE_ADS_DEVELOPER_TOKEN": "test_developer_token_xyz"
        }
        with patch.dict(os.environ, env_vars, clear=False):
            if "GOOGLE_ADS_OAUTH_TOKEN" in os.environ:
                del os.environ["GOOGLE_ADS_OAUTH_TOKEN"]

            st_static, msg_static = preflight.check_google_ads(test_live=False)
            self.assertEqual(st_static, preflight.STATUS_CONFIGURED_NOT_TESTED)
            self.assertNotEqual(st_static, preflight.STATUS_VERIFIED)

            st_live, msg_live = preflight.check_google_ads(test_live=True)
            self.assertEqual(st_live, preflight.STATUS_CONFIGURED_NOT_TESTED)
            self.assertNotEqual(st_live, preflight.STATUS_VERIFIED)

    # --------------------------------------------------------------------------
    # 10. CrUX authenticated-but-no-data is recorded accurately
    # --------------------------------------------------------------------------
    def test_10_crux_authenticated_no_data_recorded_accurately(self):
        with patch.dict(os.environ, {"CRUX_API_KEY": "AIzaSyD-TestKeyWithTwentyFiveCharsMin"}):
            with patch("urllib.request.urlopen") as mock_url:
                import urllib.error
                mock_url.side_effect = urllib.error.HTTPError(
                    url="https://chromeuxreport.googleapis.com",
                    code=404,
                    msg="Not Found",
                    hdrs={},
                    fp=None
                )
                st, msg = preflight.check_crux(test_live=True)
                self.assertEqual(st, preflight.STATUS_AUTHENTICATED_NO_DATA)
                self.assertIn("insufficient 28-day traffic density", msg)

    # --------------------------------------------------------------------------
    # 11. Integration status is genuinely persisted and exported
    # --------------------------------------------------------------------------
    def test_11_integration_status_genuinely_persisted_and_exported(self):
        results = [
            ("IndexNow Protocol", (preflight.STATUS_VERIFIED, "Live HTTPS file verified and matching key")),
            ("Google Search Console API", (preflight.STATUS_VERIFIED, "Service Account verified. Property https://aidigitools.tech/ accessible (Inspection API: VERIFIED_200). Note: Read access does not imply sitemap submitted.")),
            ("Google Gemini API", (preflight.STATUS_VERIFIED, "API authenticated (50 models discovered)")),
            ("Chrome UX Report (CrUX) API", (preflight.STATUS_AUTHENTICATED_NO_DATA, "CrUX API authenticated; Origin has insufficient 28-day traffic density for CrUX (origin traffic data unavailable, not zero)"))
        ]
        preflight.sync_api_integrations_status(results, test_live=True)

        status_path = self.workspace_root / "data" / "api_integrations_status.json"
        self.assertTrue(status_path.exists())
        with open(status_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        integrations = data.get("integrations", {})
        self.assertIn("indexnow", integrations)
        self.assertIn("google_search_console", integrations)
        self.assertIn("gemini_api", integrations)
        self.assertIn("crux_api", integrations)

        # Check GSC separate capabilities
        gsc = integrations["google_search_console"]
        self.assertIn("read_property_access", gsc)
        self.assertIn("sitemap_submission_scope", gsc)
        self.assertIn("indexing_api_policy", gsc)

    # --------------------------------------------------------------------------
    # 12. Topic selection is not counted as article generation
    # --------------------------------------------------------------------------
    def test_12_topic_selection_is_not_counted_as_article_generation(self):
        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger_before = json.load(f)
        count_before = len(ledger_before.get("publications", []))

        eval_report = self.scheduler.evaluate_daily_research_check(force_cadence=True)
        if eval_report.get("decision") != "SKIP":
            self.assertEqual(eval_report["decision"], "TOPIC_SELECTED")
            self.assertEqual(eval_report["reason_code"], "TOPIC_QUALIFIED")

        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger_after = json.load(f)
        count_after = len(ledger_after.get("publications", []))
        self.assertEqual(count_before, count_after)

    # --------------------------------------------------------------------------
    # 13. Phase 1 never publishes without approval
    # --------------------------------------------------------------------------
    def test_13_phase_1_never_publishes_without_approval(self):
        op_status = self.pub_control.get_operational_status()
        self.assertIn(op_status["current_phase"], ["FULL_AUTONOMOUS", PHASE_1_SUPERVISED])
        self.assertLess(op_status["approved_supervised_publications_count"], 3)

        test_slug = "test-phase1-supervision-sample"
        target_live_file = self.workspace_root / "blog" / f"{test_slug}.html"
        if target_live_file.exists():
            target_live_file.unlink()

        preview_record = self.pub_control.prepare_article_preview(
            slug=test_slug,
            title="Phase 1 Test Article",
            html_content="<!DOCTYPE html><html><body><h1>Phase 1 Test</h1></body></html>",
            metadata={"canonical_url": f"https://aidigitools.tech/blog/{test_slug}.html"}
        )

        self.assertEqual(preview_record["approval_required"], op_status["current_phase"] == PHASE_1_SUPERVISED)
        self.assertEqual(preview_record["decision"], "HELD_FOR_HUMAN_APPROVAL" if op_status["current_phase"] == PHASE_1_SUPERVISED else "APPROVED_FOR_AUTO_PUBLICATION")
        self.assertFalse(target_live_file.exists())

    # --------------------------------------------------------------------------
    # 14. Successful deployment triggers discovery exactly once
    # --------------------------------------------------------------------------
    def test_14_successful_deployment_triggers_discovery_only_once(self):
        url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        with patch.object(self.notifier, "submit_google_sitemap", return_value={"submitted": True, "http_status": 200}):
            res1 = self.notifier.execute_post_publication_discovery(
                url,
                verify_live_deployment=False,
                dry_run=True
            )
            self.assertTrue(res1["passed"])
            self.assertEqual(res1["status_breakdown"]["deployment_status"], "DEPLOYED")

            res2 = self.notifier.notify_indexnow_with_retry([url], dry_run=True, force=False)
            self.assertEqual(res2.get("submitted_count"), 0)
            self.assertEqual(res2.get("duplicate_skipped_count"), 1)

    # --------------------------------------------------------------------------
    # 15. Indexing submissions never imply guaranteed indexing
    # --------------------------------------------------------------------------
    def test_15_indexing_submissions_never_imply_guaranteed_indexing(self):
        sitemap_res = self.notifier.submit_google_sitemap(dry_run=True)
        self.assertIn("disclaimer", sitemap_res)
        self.assertIn("guarantees", sitemap_res["disclaimer"].lower())
        self.assertIn("neither sitemap submission", sitemap_res["disclaimer"].lower())

        indexnow_res = self.notifier.notify_indexnow(
            ["https://aidigitools.tech/tools/chatgpt-plus.html"],
            dry_run=True
        )
        self.assertIn("disclaimer", indexnow_res)
        self.assertIn("guarantees", indexnow_res["disclaimer"].lower())
        self.assertIn("neither sitemap submission", NO_INDEXING_GUARANTEE_DISCLAIMER.lower())


if __name__ == "__main__":
    unittest.main()
