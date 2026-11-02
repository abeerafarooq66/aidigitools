"""
AIDigiTools — Production Verification & Regression Test Battery
Verifies all 9 mandatory invariants:
1. A local file with live HTTP 404 is not marked healthy.
2. A skipped live HTTP check never becomes HTTP 200.
3. GSC read access does not imply sitemap write permission.
4. Google Ads credentials alone do not produce VERIFIED.
5. CrUX authenticated-but-no-data is recorded accurately.
6. A selected topic is not counted as a generated article.
7. No article is published before approval in Phase 1.
8. A successful deployment triggers discovery exactly once.
9. Indexing submissions never imply guaranteed indexing.
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

from agent.indexing_notifier import (
    IndexingNotifierEngine,
    NO_INDEXING_GUARANTEE_DISCLAIMER
)
from agent.automation_scheduler import AutomationScheduler
from agent.publishing_control import (
    PublishingControlEngine,
    PHASE_1_SUPERVISED
)
import scripts.credentials_preflight as preflight


class TestProductionVerificationRegression(unittest.TestCase):
    def setUp(self):
        self.workspace_root = ROOT_DIR
        self.notifier = IndexingNotifierEngine(self.workspace_root)
        self.scheduler = AutomationScheduler(self.workspace_root)
        self.pub_control = PublishingControlEngine(self.workspace_root)

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
    # 1. Local file with live HTTP 404 is NOT marked healthy
    # --------------------------------------------------------------------------
    def test_local_file_with_live_http_404_not_marked_healthy(self):
        url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        mock_live_failed = {
            "status": "LIVE_HTTP_FAILED",
            "http_code": 404,
            "final_url": url,
            "live_canonical": url,
            "issues": ["HTTP status code is 404 (expected 200)."]
        }

        # Check technical indexability
        res = self.notifier.verify_technical_indexability(
            url,
            check_live_http=True,
            live_http_mock=mock_live_failed
        )
        self.assertFalse(res["passed"], "Preflight must fail when live HTTP status is 404")
        self.assertFalse(res["checks"]["http_200"], "http_200 must be False when live HTTP is 404")
        self.assertEqual(res["checks"]["live_http_status"], "LIVE_HTTP_FAILED")

        # Check full audit record
        audit_res = self.notifier.run_technical_indexing_audit(
            check_live_http=True,
            verify_live_sitemap=False,
            live_http_mock=mock_live_failed
        )
        record = audit_res["urls"].get(url)
        self.assertIsNotNone(record)
        self.assertNotEqual(record["status"], "HEALTHY", "URL with HTTP 404 must not be marked HEALTHY")
        self.assertEqual(record["status"], "TECHNICAL_ISSUE")
        self.assertEqual(record["http_status"], 404)
        self.assertEqual(record["status_breakdown"]["deployment_status"], "LIVE_HTTP_FAILED")

    # --------------------------------------------------------------------------
    # 2. Skipped live HTTP check never becomes HTTP 200
    # --------------------------------------------------------------------------
    def test_skipped_live_http_check_never_becomes_http_200(self):
        url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        res = self.notifier.verify_technical_indexability(url, check_live_http=False)

        self.assertEqual(res["checks"]["live_http_status"], "SKIPPED")
        self.assertEqual(res["checks"]["http_200"], "SKIPPED", "Skipped live HTTP must remain 'SKIPPED', never True or 200")

        # In full technical audit
        audit_res = self.notifier.run_technical_indexing_audit(check_live_http=False, verify_live_sitemap=False)
        record = audit_res["urls"].get(url)
        self.assertIsNotNone(record)
        self.assertEqual(record["http_status"], "SKIPPED")
        self.assertEqual(record["status_breakdown"]["deployment_status"], "UNKNOWN", "Skipping live HTTP must produce deployment_status UNKNOWN")

    # --------------------------------------------------------------------------
    # 3. GSC read access does not imply sitemap write permission
    # --------------------------------------------------------------------------
    def test_gsc_read_access_does_not_imply_sitemap_write_permission(self):
        # Mock sys.modules for google.oauth2 so tests run cleanly in any environment
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
                # Request read-only token
                token_ro = self.notifier._get_gsc_access_token(write_scope=False)
                mock_sa.Credentials.from_service_account_info.assert_called_with(
                    {"client_email": "test@test.iam.gserviceaccount.com"},
                    scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
                )

                # Request write token
                token_w = self.notifier._get_gsc_access_token(write_scope=True)
                mock_sa.Credentials.from_service_account_info.assert_called_with(
                    {"client_email": "test@test.iam.gserviceaccount.com"},
                    scopes=["https://www.googleapis.com/auth/webmasters"]
                )

        # Calling submit_google_sitemap without write token must fail
        with patch.object(self.notifier, "_get_gsc_access_token", return_value=None):
            submit_res = self.notifier.submit_google_sitemap(dry_run=False)
            self.assertFalse(submit_res["submitted"])
            self.assertEqual(submit_res["status"], "NOT_CONFIGURED")

    # --------------------------------------------------------------------------
    # 4. Google Ads credentials alone do not produce VERIFIED
    # --------------------------------------------------------------------------
    def test_google_ads_credentials_alone_do_not_produce_verified(self):
        env_vars = {
            "GOOGLE_ADS_CUSTOMER_ID": "2913849282",
            "GOOGLE_ADS_MANAGER_ID": "1826247360",
            "GOOGLE_ADS_DEVELOPER_TOKEN": "test_developer_token_xyz"
        }
        with patch.dict(os.environ, env_vars, clear=False):
            if "GOOGLE_ADS_OAUTH_TOKEN" in os.environ:
                del os.environ["GOOGLE_ADS_OAUTH_TOKEN"]

            # Static mode
            st_static, msg_static = preflight.check_google_ads(test_live=False)
            self.assertEqual(st_static, preflight.STATUS_CONFIGURED_NOT_TESTED)
            self.assertNotEqual(st_static, preflight.STATUS_VERIFIED)

            # Live test mode without real authorized query
            st_live, msg_live = preflight.check_google_ads(test_live=True)
            self.assertEqual(st_live, preflight.STATUS_CONFIGURED_NOT_TESTED)
            self.assertNotEqual(st_live, preflight.STATUS_VERIFIED)
            self.assertIn("CONFIGURED_NOT_TESTED", msg_live)

    # --------------------------------------------------------------------------
    # 5. CrUX authenticated-but-no-data is recorded accurately
    # --------------------------------------------------------------------------
    def test_crux_authenticated_no_data_recorded_accurately(self):
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
                self.assertIn("unavailable", msg)

    # --------------------------------------------------------------------------
    # 6. Selected topic is not counted as a generated article
    # --------------------------------------------------------------------------
    def test_selected_topic_not_counted_as_generated_article(self):
        # Read baseline publication count
        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger_before = json.load(f)
        count_before = len(ledger_before.get("publications", []))

        # Run evaluate_daily_research_check
        eval_report = self.scheduler.evaluate_daily_research_check(force_cadence=True)
        
        # Decision must be TOPIC_SELECTED, not APPROVED_FOR_PUBLICATION or PUBLISHED
        if eval_report.get("decision") != "SKIP":
            self.assertEqual(eval_report["decision"], "TOPIC_SELECTED")
            self.assertEqual(eval_report["reason_code"], "TOPIC_QUALIFIED")

        # Verify publications count in ledger has NOT changed
        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger_after = json.load(f)
        count_after = len(ledger_after.get("publications", []))
        self.assertEqual(count_before, count_after, "Topic selection must never increment publication records count")

    # --------------------------------------------------------------------------
    # 7. No article is published before approval in Phase 1
    # --------------------------------------------------------------------------
    def test_no_article_published_before_approval_in_phase_1(self):
        op_status = self.pub_control.get_operational_status()
        self.assertEqual(op_status["current_phase"], PHASE_1_SUPERVISED)
        self.assertLess(op_status["approved_supervised_publications_count"], 3)

        # Prepare a mock preview under Phase 1
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

        self.assertTrue(preview_record["approval_required"])
        self.assertEqual(preview_record["decision"], "HELD_FOR_HUMAN_APPROVAL")
        self.assertEqual(preview_record["status"], "PENDING")
        self.assertFalse(target_live_file.exists(), "Article must NOT be published to blog/ directory before human approval in Phase 1")

    # --------------------------------------------------------------------------
    # 8. Successful deployment triggers discovery exactly once
    # --------------------------------------------------------------------------
    def test_successful_deployment_triggers_discovery_exactly_once(self):
        url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        
        with patch.object(self.notifier, "submit_google_sitemap", return_value={"submitted": True, "http_status": 200}):
            res1 = self.notifier.execute_post_publication_discovery(
                url,
                verify_live_deployment=False,
                dry_run=True
            )
            self.assertTrue(res1["passed"])
            self.assertEqual(res1["status_breakdown"]["deployment_status"], "DEPLOYED")

            # Subsequent dispatch for already submitted URL without force skips duplicate
            res2 = self.notifier.notify_indexnow_with_retry([url], dry_run=True, force=False)
            self.assertEqual(res2.get("submitted_count"), 0)
            self.assertEqual(res2.get("duplicate_skipped_count"), 1)

    # --------------------------------------------------------------------------
    # 9. Indexing submissions never imply guaranteed indexing
    # --------------------------------------------------------------------------
    def test_indexing_submissions_never_imply_guaranteed_indexing(self):
        # 1. Sitemap submit response contains mandatory disclaimer
        sitemap_res = self.notifier.submit_google_sitemap(dry_run=True)
        self.assertIn("disclaimer", sitemap_res)
        self.assertIn("guarantees", sitemap_res["disclaimer"].lower())
        self.assertIn("neither sitemap submission", sitemap_res["disclaimer"].lower())

        # 2. IndexNow response contains mandatory disclaimer
        indexnow_res = self.notifier.notify_indexnow(
            ["https://aidigitools.tech/tools/chatgpt-plus.html"],
            dry_run=True
        )
        self.assertIn("disclaimer", indexnow_res)
        self.assertIn("guarantees", indexnow_res["disclaimer"].lower())

        # 3. NO_INDEXING_GUARANTEE_DISCLAIMER is exact charter text
        self.assertIn("neither sitemap submission", NO_INDEXING_GUARANTEE_DISCLAIMER.lower())
        self.assertIn("guarantees", NO_INDEXING_GUARANTEE_DISCLAIMER.lower())


if __name__ == "__main__":
    unittest.main()
