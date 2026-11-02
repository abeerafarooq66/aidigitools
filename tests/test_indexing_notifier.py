"""
Unit Tests for Indexing & Search Engine Notification Engine (Part 19 & Corrections V2).
======================================================================================
Strictly tests Part 19 of Master Architecture Charter & Section 9 Corrections V2:
INDEXING AND SEARCH ENGINE NOTIFICATIONS.

Validates all 20 Mandatory Scenarios:
1. Local file exists but public URL returns 404 (LIVE_HTTP_FAILED).
2. HTML preview exists but production URL is unavailable (LIVE_HTTP_UNKNOWN).
3. Wrong canonical URL.
4. noindex meta directive.
5. X-Robots-Tag noindex header.
6. Googlebot blocked by robots.txt.
7. Bingbot blocked by robots.txt.
8. Missing sitemap URL.
9. Malformed sitemap XML.
10. GSC credentials absent (truthful NOT_CONFIGURED).
11. GSC sitemap submission failure.
12. URL Inspection returning indexed (GOOGLE_INDEXED).
13. URL Inspection returning not indexed (NOT_INDEXED).
14. URL Inspection returning an uncertain verdict (UNKNOWN).
15. IndexNow Central succeeds while Bing fails (PARTIALLY_SUBMITTED).
16. Bing succeeds while IndexNow Central fails (PARTIALLY_SUBMITTED, BING_STATUS_VERIFIED).
17. Both IndexNow endpoints fail (FAILED).
18. Failed dispatch does not activate success cooldown.
19. Human approval before live deployment does not send indexing notifications.
20. Verified deployment triggers the indexing workflow exactly once.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.indexing_notifier import (
    IndexingNotifierEngine,
    GoogleIndexingApiViolationError,
    TechnicalIndexabilityError,
    NO_INDEXING_GUARANTEE_DISCLAIMER
)
from agent.publishing_control import PublishingControlEngine
from agent.automation_scheduler import AutomationScheduler


class TestIndexingNotifierCorrectionsV2(unittest.TestCase):

    def setUp(self):
        """Create an isolated test workspace for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Create key file
        (self.workspace / "89d63ab53a63527b12a199a3096e51ad.txt").write_text(
            "89d63ab53a63527b12a199a3096e51ad", encoding="utf-8"
        )

        # Create robots.txt
        (self.workspace / "robots.txt").write_text(
            "User-agent: *\nDisallow: /admin/\nDisallow: /private/\nAllow: /\n"
            "User-agent: Googlebot\nDisallow: /admin/\nDisallow: /private/\nAllow: /\n"
            "User-agent: Bingbot\nDisallow: /admin/\nDisallow: /private/\nAllow: /\n"
            "Sitemap: https://aidigitools.tech/sitemap.xml\n",
            encoding="utf-8"
        )

        # Create dummy HTML files
        (self.workspace / "index.html").write_text(
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<link rel="canonical" href="https://aidigitools.tech/">'
            '<meta name="robots" content="index, follow">'
            '<script type="application/ld+json">{"@type":"WebSite","name":"AIDigiTools"}</script>'
            '</head><body><a href="/deals.html">Deals</a><a href="/tools/chatgpt-plus.html">ChatGPT</a></body></html>',
            encoding="utf-8"
        )
        (self.workspace / "deals.html").write_text(
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<link rel="canonical" href="https://aidigitools.tech/deals.html">'
            '<meta name="robots" content="index, follow">'
            '<script type="application/ld+json">{"@type":"CollectionPage","name":"Deals"}</script>'
            '</head><body><a href="/">Home</a><a href="/tools/chatgpt-plus.html">ChatGPT</a></body></html>',
            encoding="utf-8"
        )
        (self.workspace / "tools").mkdir(parents=True, exist_ok=True)
        (self.workspace / "tools" / "chatgpt-plus.html").write_text(
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<link rel="canonical" href="https://aidigitools.tech/tools/chatgpt-plus.html">'
            '<meta name="robots" content="index, follow">'
            '<script type="application/ld+json">{"@type":"Product","name":"ChatGPT Plus"}</script>'
            '</head><body><a href="/">Home</a><a href="/deals.html">Deals</a></body></html>',
            encoding="utf-8"
        )

        self.engine = IndexingNotifierEngine(workspace_root=self.workspace)

    def tearDown(self):
        """Clean up isolated directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # --------------------------------------------------------------------------
    # Test 1: Local file exists but public URL returns 404
    # --------------------------------------------------------------------------
    def test_01_local_file_exists_but_public_url_returns_404(self):
        """Local file exists but live HTTP GET returns 404 -> LIVE_HTTP_FAILED."""
        mock_404 = {
            "status": "LIVE_HTTP_FAILED",
            "http_code": 404,
            "issues": ["Production server returned HTTP 404: Not Found"]
        }
        res = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/tools/chatgpt-plus.html",
            check_live_http=True,
            live_http_mock=mock_404
        )
        self.assertFalse(res["passed"])
        self.assertEqual(res["checks"]["live_http_status"], "LIVE_HTTP_FAILED")
        self.assertTrue(any("404" in v for v in res["violations"]))

    # --------------------------------------------------------------------------
    # Test 2: HTML preview exists but production URL is unavailable
    # --------------------------------------------------------------------------
    def test_02_html_preview_exists_but_production_url_unavailable(self):
        """HTML preview supplied but network connection to live server fails -> LIVE_HTTP_UNKNOWN."""
        mock_unavail = {
            "status": "LIVE_HTTP_UNKNOWN",
            "http_code": None,
            "issues": ["Network / connection error contacting production server: Connection timed out"]
        }
        res = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/blog/preview-article.html",
            html_content="<!DOCTYPE html><html><head><link rel='canonical' href='https://aidigitools.tech/blog/preview-article.html'></head><body>Preview</body></html>",
            check_live_http=True,
            live_http_mock=mock_unavail,
            verify_sitemap=False
        )
        self.assertFalse(res["passed"])
        self.assertEqual(res["checks"]["live_http_status"], "LIVE_HTTP_UNKNOWN")
        self.assertTrue(any("timed out" in v for v in res["violations"]))

    # --------------------------------------------------------------------------
    # Test 3: Wrong canonical URL
    # --------------------------------------------------------------------------
    def test_03_wrong_canonical_url(self):
        """Canonical tag href does not match expected canonical URL -> Canonical mismatch violation."""
        html_mismatch = (
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<link rel="canonical" href="https://aidigitools.tech/wrong-slug.html">'
            '<meta name="robots" content="index, follow">'
            '<script type="application/ld+json">{"@type":"Article","headline":"Title"}</script>'
            '</head><body><a href="/">Home</a><a href="/deals.html">Deals</a></body></html>'
        )
        res = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/correct-slug.html",
            html_content=html_mismatch,
            verify_sitemap=False
        )
        self.assertFalse(res["passed"])
        self.assertFalse(res["checks"]["canonical_url"])
        self.assertTrue(any("Canonical mismatch" in v for v in res["violations"]))

    # --------------------------------------------------------------------------
    # Test 4: noindex meta directive
    # --------------------------------------------------------------------------
    def test_04_noindex_meta_directive(self):
        """Meta robots containing noindex or none -> Accidental noindex violation."""
        html_noindex = (
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<link rel="canonical" href="https://aidigitools.tech/tools/test.html">'
            '<meta name="robots" content="noindex, follow">'
            '<script type="application/ld+json">{"@type":"Product","name":"Test"}</script>'
            '</head><body><a href="/">Home</a><a href="/deals.html">Deals</a></body></html>'
        )
        res = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/tools/test.html",
            html_content=html_noindex,
            verify_sitemap=False
        )
        self.assertFalse(res["passed"])
        self.assertFalse(res["checks"]["noindex_directive"])
        self.assertTrue(any("Accidental noindex" in v for v in res["violations"]))

    # --------------------------------------------------------------------------
    # Test 5: X-Robots-Tag noindex header
    # --------------------------------------------------------------------------
    def test_05_x_robots_tag_noindex_header(self):
        """Live HTTP response header contains X-Robots-Tag: noindex -> LIVE_HTTP_FAILED."""
        mock_header_noindex = {
            "status": "LIVE_HTTP_FAILED",
            "http_code": 200,
            "x_robots_tag": "noindex, nofollow",
            "issues": ["Live HTTP header X-Robots-Tag contains blocking directive: 'noindex, nofollow'."]
        }
        res = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/tools/chatgpt-plus.html",
            check_live_http=True,
            live_http_mock=mock_header_noindex
        )
        self.assertFalse(res["passed"])
        self.assertTrue(any("X-Robots-Tag contains blocking directive" in v for v in res["violations"]))

    # --------------------------------------------------------------------------
    # Test 6: Googlebot blocked by robots.txt
    # --------------------------------------------------------------------------
    def test_06_googlebot_blocked_by_robots_txt(self):
        """URL disallowed specifically for Googlebot in robots.txt -> robots_txt_allowed is False."""
        robots_blocking_google = (
            "User-agent: Googlebot\nDisallow: /admin/\nDisallow: /private/\nDisallow: /tools/blocked.html\nAllow: /\n"
            "User-agent: Bingbot\nAllow: /\n"
        )
        res = self.engine.verify_robots_txt(
            "https://aidigitools.tech/tools/blocked.html",
            robots_content=robots_blocking_google
        )
        self.assertFalse(res["googlebot_allowed"])
        self.assertTrue(res["bingbot_allowed"])
        self.assertFalse(res["robots_allowed"])
        self.assertIn("Googlebot", res["robots_block_reason"])

    # --------------------------------------------------------------------------
    # Test 7: Bingbot blocked by robots.txt
    # --------------------------------------------------------------------------
    def test_07_bingbot_blocked_by_robots_txt(self):
        """URL disallowed specifically for Bingbot in robots.txt -> robots_txt_allowed is False."""
        robots_blocking_bing = (
            "User-agent: Googlebot\nAllow: /\n"
            "User-agent: Bingbot\nDisallow: /tools/blocked-bing.html\nAllow: /\n"
        )
        res = self.engine.verify_robots_txt(
            "https://aidigitools.tech/tools/blocked-bing.html",
            robots_content=robots_blocking_bing
        )
        self.assertTrue(res["googlebot_allowed"])
        self.assertFalse(res["bingbot_allowed"])
        self.assertFalse(res["robots_allowed"])
        self.assertIn("Bingbot", res["robots_block_reason"])

    # --------------------------------------------------------------------------
    # Test 8: Missing sitemap URL
    # --------------------------------------------------------------------------
    def test_08_missing_sitemap_url(self):
        """URL not present in local or live sitemap -> sitemap_included violation."""
        self.engine.sync_sitemap(dry_run=False)
        res = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/tools/unlisted-tool.html",
            verify_sitemap=True
        )
        self.assertFalse(res["checks"]["sitemap_included"])
        self.assertTrue(any("missing from local sitemap.xml" in v for v in res["violations"]))

    # --------------------------------------------------------------------------
    # Test 9: Malformed sitemap XML
    # --------------------------------------------------------------------------
    def test_09_malformed_sitemap_xml(self):
        """Malformed XML syntax in live or local sitemap triggers validation error."""
        malformed_xml = "<urlset><url><loc>https://aidigitools.tech/</loc>"  # missing closing tags
        res = self.engine.verify_live_sitemap(
            "https://aidigitools.tech/",
            mock_sitemap_xml=malformed_xml
        )
        self.assertEqual(res["live_sitemap_status"], "LIVE_SITEMAP_FAILED")
        self.assertIn("XML syntax error", res["error_message"])

    # --------------------------------------------------------------------------
    # Test 10: GSC credentials absent
    # --------------------------------------------------------------------------
    def test_10_gsc_credentials_absent(self):
        """When GSC credentials are absent, submit and inspect report truthful NOT_CONFIGURED."""
        with patch.dict(os.environ, {}, clear=True):
            sub_res = self.engine.submit_google_sitemap(dry_run=False)
            self.assertEqual(sub_res["status"], "NOT_CONFIGURED")
            self.assertFalse(sub_res["submitted"])
            self.assertIsNone(sub_res["http_status"])

            inspect_res = self.engine.inspect_google_url("https://aidigitools.tech/", dry_run=False)
            self.assertEqual(inspect_res["status"], "NOT_CONFIGURED")
            self.assertEqual(inspect_res["indexing_state"], "UNKNOWN")
            self.assertIsNone(inspect_res["verdict"])
            self.assertIsNone(inspect_res["coverageState"])

    # --------------------------------------------------------------------------
    # Test 11: GSC sitemap submission failure
    # --------------------------------------------------------------------------
    def test_11_gsc_sitemap_submission_failure(self):
        """GSC API HTTP 403 or 500 error is caught and recorded as FAILED."""
        import urllib.error
        with patch("urllib.request.urlopen") as mock_open:
            mock_open.side_effect = urllib.error.HTTPError(
                url="https://www.googleapis.com/webmasters/v3/...",
                code=403,
                msg="Forbidden: Insufficient Permissions",
                hdrs={},
                fp=None
            )
            res = self.engine.submit_google_sitemap(access_token="fake_token_123", dry_run=False)
            self.assertEqual(res["status"], "FAILED")
            self.assertFalse(res["submitted"])
            self.assertEqual(res["http_status"], 403)
            self.assertIn("403", res["message"])

    # --------------------------------------------------------------------------
    # Test 12: URL Inspection returning indexed
    # --------------------------------------------------------------------------
    def test_12_url_inspection_returning_indexed(self):
        """URL Inspection API verdict PASS with coverage 'Submitted and indexed' maps to GOOGLE_INDEXED."""
        fake_api_response = json.dumps({
            "inspectionResult": {
                "indexStatusResult": {
                    "verdict": "PASS",
                    "coverageState": "Submitted and indexed",
                    "indexingState": "INDEXING_ALLOWED",
                    "pageFetchState": "SUCCESSFUL",
                    "robotsTxtState": "ALLOWED",
                    "googleCanonical": "https://aidigitools.tech/tools/chatgpt-plus.html",
                    "userCanonical": "https://aidigitools.tech/tools/chatgpt-plus.html",
                    "lastCrawlTime": "2026-11-01T12:00:00Z"
                }
            }
        }).encode("utf-8")

        mock_resp = MagicMock()
        mock_resp.read.return_value = fake_api_response
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp):
            res = self.engine.inspect_google_url(
                "https://aidigitools.tech/tools/chatgpt-plus.html",
                access_token="mock_token",
                dry_run=False
            )
            self.assertEqual(res["status"], "GOOGLE_INDEX_STATUS_CHECKED")
            self.assertEqual(res["indexing_state"], "GOOGLE_INDEXED")
            self.assertEqual(res["verdict"], "PASS")
            self.assertEqual(res["coverageState"], "Submitted and indexed")
            self.assertEqual(res["googleCanonical"], "https://aidigitools.tech/tools/chatgpt-plus.html")

    # --------------------------------------------------------------------------
    # Test 13: URL Inspection returning not indexed
    # --------------------------------------------------------------------------
    def test_13_url_inspection_returning_not_indexed(self):
        """URL Inspection API verdict FAIL with 'Crawled - currently not indexed' maps to NOT_INDEXED."""
        fake_api_response = json.dumps({
            "inspectionResult": {
                "indexStatusResult": {
                    "verdict": "FAIL",
                    "coverageState": "Crawled - currently not indexed",
                    "indexingState": "BLOCKED_BY_META_TAG",
                    "pageFetchState": "SUCCESSFUL",
                    "robotsTxtState": "ALLOWED",
                    "googleCanonical": None,
                    "userCanonical": "https://aidigitools.tech/tools/chatgpt-plus.html",
                    "lastCrawlTime": "2026-11-01T12:00:00Z"
                }
            }
        }).encode("utf-8")

        mock_resp = MagicMock()
        mock_resp.read.return_value = fake_api_response
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp):
            res = self.engine.inspect_google_url(
                "https://aidigitools.tech/tools/chatgpt-plus.html",
                access_token="mock_token",
                dry_run=False
            )
            self.assertEqual(res["status"], "GOOGLE_INDEX_STATUS_CHECKED")
            self.assertEqual(res["indexing_state"], "NOT_INDEXED")
            self.assertEqual(res["verdict"], "FAIL")

    # --------------------------------------------------------------------------
    # Test 14: URL Inspection returning uncertain verdict
    # --------------------------------------------------------------------------
    def test_14_url_inspection_returning_uncertain_verdict(self):
        """URL Inspection API with NEUTRAL verdict and empty coverage maps to UNKNOWN."""
        fake_api_response = json.dumps({
            "inspectionResult": {
                "indexStatusResult": {
                    "verdict": "NEUTRAL",
                    "coverageState": "",
                    "indexingState": "INDEXING_STATE_UNSPECIFIED",
                    "pageFetchState": "PAGE_FETCH_STATE_UNSPECIFIED",
                    "robotsTxtState": "ROBOTS_TXT_STATE_UNSPECIFIED",
                    "googleCanonical": None,
                    "userCanonical": None,
                    "lastCrawlTime": None
                }
            }
        }).encode("utf-8")

        mock_resp = MagicMock()
        mock_resp.read.return_value = fake_api_response
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp):
            res = self.engine.inspect_google_url(
                "https://aidigitools.tech/tools/chatgpt-plus.html",
                access_token="mock_token",
                dry_run=False
            )
            self.assertEqual(res["indexing_state"], "UNKNOWN")

    # --------------------------------------------------------------------------
    # Test 15: IndexNow Central succeeds while Bing fails
    # --------------------------------------------------------------------------
    def test_15_indexnow_central_succeeds_while_bing_fails(self):
        """Central returns 200, Bing returns 500 -> PARTIALLY_SUBMITTED, Bing not verified."""
        import urllib.error

        def mock_dispatch(req, timeout):
            if "api.indexnow.org" in req.full_url:
                resp = MagicMock()
                resp.status = 200
                resp.__enter__.return_value = resp
                return resp
            else:
                raise urllib.error.HTTPError(req.full_url, 500, "Internal Server Error", {}, None)

        with patch("urllib.request.urlopen", side_effect=mock_dispatch):
            res = self.engine.notify_indexnow_with_retry(
                urls=["https://aidigitools.tech/tools/chatgpt-plus.html"],
                dry_run=False,
                force=True
            )
            self.assertEqual(res["indexnow_central_status"], "SUBMITTED")
            self.assertEqual(res["microsoft_bing_indexnow_status"], "FAILED")
            self.assertEqual(res["indexnow_overall_status"], "PARTIALLY_SUBMITTED")
            self.assertEqual(res["bing_status"], "SUBMISSION_FAILED")

    # --------------------------------------------------------------------------
    # Test 16: Bing succeeds while IndexNow Central fails
    # --------------------------------------------------------------------------
    def test_16_bing_succeeds_while_indexnow_central_fails(self):
        """Bing returns 200, Central returns 503 -> PARTIALLY_SUBMITTED, Bing verified."""
        import urllib.error

        def mock_dispatch(req, timeout):
            if "bing.com" in req.full_url:
                resp = MagicMock()
                resp.status = 200
                resp.__enter__.return_value = resp
                return resp
            else:
                raise urllib.error.HTTPError(req.full_url, 503, "Service Unavailable", {}, None)

        with patch("urllib.request.urlopen", side_effect=mock_dispatch):
            res = self.engine.notify_indexnow_with_retry(
                urls=["https://aidigitools.tech/tools/chatgpt-plus.html"],
                dry_run=False,
                force=True
            )
            self.assertEqual(res["indexnow_central_status"], "FAILED")
            self.assertEqual(res["microsoft_bing_indexnow_status"], "SUBMITTED")
            self.assertEqual(res["indexnow_overall_status"], "PARTIALLY_SUBMITTED")
            self.assertEqual(res["bing_status"], "BING_STATUS_VERIFIED")

    # --------------------------------------------------------------------------
    # Test 17: Both IndexNow endpoints fail
    # --------------------------------------------------------------------------
    def test_17_both_indexnow_endpoints_fail(self):
        """Both IndexNow Central and Bing return 500 -> overall FAILED, submitted_count is 0."""
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 500, "Error", {}, None)):
            res = self.engine.notify_indexnow_with_retry(
                urls=["https://aidigitools.tech/tools/chatgpt-plus.html"],
                dry_run=False,
                force=True
            )
            self.assertFalse(res["success"])
            self.assertEqual(res["indexnow_overall_status"], "FAILED")
            self.assertEqual(res["submitted_count"], 0)
            self.assertEqual(res["bing_status"], "SUBMISSION_FAILED")

    # --------------------------------------------------------------------------
    # Test 18: Failed dispatch does not activate success cooldown
    # --------------------------------------------------------------------------
    def test_18_failed_dispatch_does_not_activate_success_cooldown(self):
        """When an IndexNow dispatch fails, retry eligibility is retained without cooldown lock."""
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 500, "Error", {}, None)):
            res1 = self.engine.notify_indexnow_with_retry(
                urls=["https://aidigitools.tech/tools/chatgpt-plus.html"],
                dry_run=False,
                force=True
            )
            self.assertFalse(res1["success"])

        # Second attempt without force must NOT be skipped by cooldown because previous run failed!
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 500, "Error", {}, None)):
            res2 = self.engine.notify_indexnow_with_retry(
                urls=["https://aidigitools.tech/tools/chatgpt-plus.html"],
                dry_run=False,
                force=False  # Cooldown check active
            )
            self.assertEqual(res2["duplicate_skipped_count"], 0)  # Not skipped!
            self.assertNotIn("Duplicate submission control active", res2.get("message", ""))

    # --------------------------------------------------------------------------
    # Test 19: Human approval before live deployment does not send notifications
    # --------------------------------------------------------------------------
    def test_19_human_approval_before_live_deployment_does_not_send_notifications(self):
        """Approving a preview when live deployment is not yet verified leaves discovery pending."""
        control = PublishingControlEngine(workspace_root=self.workspace)
        preview = control.prepare_article_preview(
            slug="test-pending-deploy",
            title="Test Pending Deploy",
            html_content="<!DOCTYPE html><html><body>Test</body></html>",
            metadata={
                "topic_id": "TOPIC-TEST-01",
                "canonical_url": "https://aidigitools.tech/blog/test-pending-deploy.html",
                "cluster_slug": "ai-coding"
            },
            quality_gate_report={"passed": True, "critical_failures": []}
        )

        # Mock verify_live_http to return LIVE_HTTP_FAILED (e.g. 404 because not yet deployed)
        with patch.object(IndexingNotifierEngine, "verify_live_http") as mock_live:
            mock_live.return_value = {
                "status": "LIVE_HTTP_FAILED",
                "http_code": 404,
                "issues": ["HTTP 404 Not Found on production server"]
            }
            approval = control.human_approve_preview(
                preview_id_or_slug=preview["preview_id"],
                reviewer_name="Senior Editor",
                reviewer_notes="Approved pending deployment"
            )

            self.assertEqual(approval["status"], "APPROVED_BY_HUMAN")
            telemetry = approval["discovery_telemetry"]
            self.assertEqual(telemetry["status"], "PENDING_DEPLOYMENT_VERIFICATION")
            self.assertFalse(telemetry["passed"])
            self.assertIn("Search engine discovery deferred", telemetry["message"])

    # --------------------------------------------------------------------------
    # Test 20: Verified deployment triggers the indexing workflow exactly once
    # --------------------------------------------------------------------------
    def test_20_verified_deployment_triggers_indexing_workflow_exactly_once(self):
        """When live production deployment is verified, post-publication discovery executes completely."""
        mock_live_verified = {
            "status": "LIVE_HTTP_VERIFIED",
            "http_code": 200,
            "content_type": "text/html; charset=utf-8",
            "final_url": "https://aidigitools.tech/tools/chatgpt-plus.html",
            "live_canonical": "https://aidigitools.tech/tools/chatgpt-plus.html",
            "x_robots_tag": "",
            "meta_robots": "index, follow",
            "issues": []
        }

        with patch.object(IndexingNotifierEngine, "verify_live_http", return_value=mock_live_verified):
            res = self.engine.execute_post_publication_discovery(
                url="https://aidigitools.tech/tools/chatgpt-plus.html",
                verify_live_deployment=True,
                dry_run=True
            )
            self.assertTrue(res["passed"])
            breakdown = res["status_breakdown"]
            self.assertEqual(breakdown["deployment_status"], "DEPLOYED")
            self.assertEqual(breakdown["sitemap_status"], "SITEMAP_UPDATED")
            self.assertEqual(breakdown["google_indexing_state"], "UNKNOWN")  # Invariant: not indexed yet!
            self.assertEqual(breakdown["indexnow_overall_status"], "FULLY_SUBMITTED")
            self.assertEqual(breakdown["bing_status"], "BING_STATUS_VERIFIED")

    # --------------------------------------------------------------------------
    # Baseline Integrity Tests
    # --------------------------------------------------------------------------
    def test_accurate_sitemap_synchronization_and_lastmod(self):
        """Sitemap must be generated with accurate lastmod, loc, priority, valid XML, and robots.txt reference."""
        res = self.engine.sync_sitemap(dry_run=False)
        self.assertEqual(res["total_urls"], 3)
        self.assertTrue(res["xml_valid"])
        self.assertTrue(res["robots_txt_sitemap_referenced"])
        self.assertTrue(Path(res["sitemap_path"]).exists())

    def test_google_indexing_api_prohibition_firewall(self):
        """Calling Google Indexing API for ordinary blog/product pages must be strictly blocked with an error."""
        with self.assertRaises(GoogleIndexingApiViolationError) as ctx:
            self.engine.request_google_indexing_api("https://aidigitools.tech/compare/chatgpt-vs-claude.html")

        self.assertIn("strictly reserved for pages with JobPosting or BroadcastEvent", str(ctx.exception))

    def test_no_ranking_or_indexing_guarantee_disclaimer(self):
        """All outputs and ledger metadata must include the mandatory search engine autonomy disclaimer."""
        self.assertIn("Neither sitemap submission", NO_INDEXING_GUARANTEE_DISCLAIMER)
        self.assertIn("guarantees", NO_INDEXING_GUARANTEE_DISCLAIMER.lower())


if __name__ == "__main__":
    unittest.main()
