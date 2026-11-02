"""
Unit Tests for Indexing & Search Engine Notification Engine (Part 19).
======================================================================
Strictly tests Part 19 of Master Architecture Charter:
INDEXING AND SEARCH ENGINE NOTIFICATIONS.

Validates:
1. Accurate sitemap updates with verified lastmod values and XML validity.
2. IndexNow Bing notifications with key verification, retry handling, and duplicate control.
3. Strict prohibition firewall against using Google Indexing API for blog posts.
4. Technical indexability pre-flight checks (8 points).
5. Google Search Console sitemap submission & URL Inspection API handling.
6. Strictly separated indexing lifecycle status tracking.
7. Post-publication automated discovery pipeline.
8. Search engine autonomy disclaimer (no guarantee of indexing or ranking).
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

from agent.indexing_notifier import (
    IndexingNotifierEngine,
    GoogleIndexingApiViolationError,
    TechnicalIndexabilityError,
    NO_INDEXING_GUARANTEE_DISCLAIMER
)


class TestIndexingNotifier(unittest.TestCase):

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
            "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /private/\nSitemap: https://aidigitools.tech/sitemap.xml\n",
            encoding="utf-8"
        )

        # Create dummy HTML files
        (self.workspace / "index.html").write_text(
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="canonical" href="https://aidigitools.tech/"><meta name="robots" content="index, follow"><script type="application/ld+json">{"@type":"WebSite","name":"AIDigiTools"}</script></head><body><a href="/deals.html">Deals</a><a href="/tools/chatgpt-plus.html">ChatGPT</a></body></html>',
            encoding="utf-8"
        )
        (self.workspace / "deals.html").write_text(
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="canonical" href="https://aidigitools.tech/deals.html"><meta name="robots" content="index, follow"><script type="application/ld+json">{"@type":"CollectionPage","name":"Deals"}</script></head><body><a href="/">Home</a><a href="/tools/chatgpt-plus.html">ChatGPT</a></body></html>',
            encoding="utf-8"
        )
        (self.workspace / "tools").mkdir(parents=True, exist_ok=True)
        (self.workspace / "tools" / "chatgpt-plus.html").write_text(
            '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="canonical" href="https://aidigitools.tech/tools/chatgpt-plus.html"><meta name="robots" content="index, follow"><script type="application/ld+json">{"@type":"Product","name":"ChatGPT Plus"}</script></head><body><a href="/">Home</a><a href="/deals.html">Deals</a></body></html>',
            encoding="utf-8"
        )

        self.engine = IndexingNotifierEngine(workspace_root=self.workspace)

    def tearDown(self):
        """Clean up isolated directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_accurate_sitemap_synchronization_and_lastmod(self):
        """Sitemap must be generated with accurate lastmod, loc, priority, valid XML, and robots.txt reference."""
        res = self.engine.sync_sitemap(dry_run=False)
        self.assertEqual(res["total_urls"], 3)
        self.assertTrue(res["xml_valid"])
        self.assertTrue(res["robots_txt_sitemap_referenced"])
        self.assertTrue(Path(res["sitemap_path"]).exists())

        sitemap_content = Path(res["sitemap_path"]).read_text(encoding="utf-8")
        self.assertIn('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">', sitemap_content)
        self.assertIn("<loc>https://aidigitools.tech/</loc>", sitemap_content)
        self.assertIn("<loc>https://aidigitools.tech/deals.html</loc>", sitemap_content)
        self.assertIn("<loc>https://aidigitools.tech/tools/chatgpt-plus.html</loc>", sitemap_content)
        self.assertIn("<lastmod>", sitemap_content)

    def test_google_indexing_api_prohibition_firewall(self):
        """Calling Google Indexing API for ordinary blog/product pages must be strictly blocked with an error."""
        with self.assertRaises(GoogleIndexingApiViolationError) as ctx:
            self.engine.request_google_indexing_api("https://aidigitools.tech/compare/chatgpt-vs-claude.html")

        self.assertIn("strictly reserved for pages with JobPosting or BroadcastEvent", str(ctx.exception))
        self.assertIn("violates Google Search Central policies", str(ctx.exception))

    def test_indexnow_notification_and_key_validation(self):
        """IndexNow submissions must validate key existence and format payloads correctly."""
        urls = [
            "https://aidigitools.tech/compare/chatgpt-vs-claude.html",
            "https://aidigitools.tech/tools/cursor-pro.html"
        ]
        res = self.engine.notify_indexnow_with_retry(urls=urls, dry_run=True, force=True)
        self.assertTrue(res["success"])
        self.assertTrue(res["key_file_exists_locally"])
        self.assertEqual(res["submitted_count"], 2)
        self.assertEqual(res["key"], "89d63ab53a63527b12a199a3096e51ad")
        self.assertIn("guarantees", res["disclaimer"].lower())
        self.assertIn("neither sitemap submission", res["disclaimer"].lower())

    def test_indexnow_retry_and_duplicate_control(self):
        """IndexNow duplicate control must skip URLs submitted within the cooldown window."""
        urls = ["https://aidigitools.tech/tools/chatgpt-plus.html"]
        # First submission
        res1 = self.engine.notify_indexnow_with_retry(urls=urls, dry_run=True, force=True)
        self.assertEqual(res1["submitted_count"], 1)

        # Immediate second submission without force should be skipped by duplicate control
        res2 = self.engine.notify_indexnow_with_retry(urls=urls, dry_run=True, force=False)
        self.assertEqual(res2["submitted_count"], 0)
        self.assertEqual(res2["duplicate_skipped_count"], 1)
        self.assertIn("Duplicate submission control active", res2["message"])

    def test_technical_indexability_preflight_checks(self):
        """Pre-flight indexability check must audit all 8 criteria and catch violations."""
        self.engine.sync_sitemap(dry_run=False)

        # 1. Compliant page should pass
        res = self.engine.verify_technical_indexability("https://aidigitools.tech/tools/chatgpt-plus.html")
        self.assertTrue(res["passed"], f"Expected pass, got violations: {res['violations']}")
        self.assertTrue(res["checks"]["http_200"])
        self.assertTrue(res["checks"]["canonical_url"])
        self.assertTrue(res["checks"]["noindex_directive"])
        self.assertTrue(res["checks"]["robots_txt_allowed"])
        self.assertTrue(res["checks"]["sitemap_included"])
        self.assertTrue(res["checks"]["mobile_accessible"])
        self.assertTrue(res["checks"]["structured_data_valid"])

        # 2. Defective page with noindex and fake aggregateRating should fail
        defective_html = """<!DOCTYPE html><html><head>
        <meta name="robots" content="noindex, follow">
        <link rel="canonical" href="https://aidigitools.tech/bad.html">
        <script type="application/ld+json">{"@type":"Product","name":"Bad","aggregateRating":{"ratingValue":5}}</script>
        </head><body><p>No links, no viewport</p></body></html>"""
        res_bad = self.engine.verify_technical_indexability(
            "https://aidigitools.tech/bad.html",
            html_content=defective_html,
            verify_sitemap=False
        )
        self.assertFalse(res_bad["passed"])
        self.assertTrue(any("Accidental noindex" in v for v in res_bad["violations"]))
        self.assertTrue(any("Fabricated schema" in v for v in res_bad["violations"]))
        self.assertTrue(any("Missing responsive viewport" in v for v in res_bad["violations"]))

    def test_google_sitemap_submit_and_url_inspection(self):
        """Google Search Console sitemap submission and URL inspection must report truthful status."""
        # Unconfigured environment
        gsc_sub = self.engine.submit_google_sitemap(dry_run=False)
        self.assertEqual(gsc_sub["status"], "NOT_CONFIGURED")
        self.assertFalse(gsc_sub["submitted"])

        gsc_inspect = self.engine.inspect_google_url("https://aidigitools.tech/tools/chatgpt-plus.html", dry_run=False)
        self.assertEqual(gsc_inspect["status"], "NOT_CONFIGURED")
        self.assertEqual(gsc_inspect["indexing_state"], "UNKNOWN")

        # Dry-run execution
        dry_sub = self.engine.submit_google_sitemap(dry_run=True)
        self.assertEqual(dry_sub["status"], "GOOGLE_SITEMAP_SUBMITTED")
        self.assertTrue(dry_sub["submitted"])

        dry_inspect = self.engine.inspect_google_url("https://aidigitools.tech/tools/chatgpt-plus.html", dry_run=True)
        self.assertEqual(dry_inspect["status"], "GOOGLE_INDEX_STATUS_CHECKED")
        self.assertEqual(dry_inspect["indexing_state"], "UNKNOWN")  # Never call indexed without proof

    def test_separated_indexing_status_tracking(self):
        """Status tracking must separate PUBLISHED, DEPLOYED, SITEMAP, GOOGLE, and BING states."""
        audit_res = self.engine.run_technical_indexing_audit()
        self.assertEqual(audit_res["total_urls_audited"], 3)
        self.assertEqual(audit_res["total_healthy"], 3)

        with open(self.engine.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        home_record = ledger["urls"]["https://aidigitools.tech/"]
        breakdown = home_record["status_breakdown"]

        self.assertEqual(breakdown["publication_status"], "PUBLISHED")
        self.assertEqual(breakdown["deployment_status"], "DEPLOYED")
        self.assertEqual(breakdown["sitemap_status"], "SITEMAP_UPDATED")
        self.assertIn(breakdown["google_sitemap_status"], ["NOT_CONFIGURED", "GOOGLE_SITEMAP_SUBMITTED"])
        self.assertIn(breakdown["google_inspection_status"], ["NOT_CONFIGURED", "GOOGLE_INDEX_STATUS_CHECKED"])
        self.assertEqual(breakdown["google_indexing_state"], "UNKNOWN")  # Never claim indexed without evidence!
        self.assertIn(breakdown["indexnow_status"], ["INDEXNOW_SUBMITTED", "PENDING"])
        self.assertIn(breakdown["bing_status"], ["BING_STATUS_VERIFIED", "PENDING"])

    def test_post_publication_discovery_pipeline(self):
        """Post-publication pipeline must orchestrate pre-flight, sitemap sync, GSC submit, URL inspect, and IndexNow."""
        target_url = "https://aidigitools.tech/tools/chatgpt-plus.html"
        res = self.engine.execute_post_publication_discovery(
            url=target_url,
            is_deployed=True,
            dry_run=True
        )

        self.assertTrue(res["passed"])
        self.assertEqual(res["url"], target_url)

        breakdown = res["status_breakdown"]
        self.assertEqual(breakdown["publication_status"], "PUBLISHED")
        self.assertEqual(breakdown["deployment_status"], "DEPLOYED")
        self.assertEqual(breakdown["sitemap_status"], "SITEMAP_UPDATED")
        self.assertEqual(breakdown["google_sitemap_status"], "GOOGLE_SITEMAP_SUBMITTED")
        self.assertEqual(breakdown["google_inspection_status"], "GOOGLE_INDEX_STATUS_CHECKED")
        self.assertEqual(breakdown["google_indexing_state"], "UNKNOWN")  # Autonomous discipline: not indexed yet
        self.assertEqual(breakdown["indexnow_status"], "INDEXNOW_SUBMITTED")
        self.assertEqual(breakdown["bing_status"], "BING_STATUS_VERIFIED")

        # Verify entry in ledger
        with open(self.engine.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        saved = ledger["urls"][target_url]
        self.assertEqual(saved["status_breakdown"], breakdown)

    def test_no_ranking_or_indexing_guarantee_disclaimer(self):
        """All outputs and ledger metadata must include the mandatory search engine autonomy disclaimer."""
        self.assertIn("Neither sitemap submission", NO_INDEXING_GUARANTEE_DISCLAIMER)
        self.assertIn("guarantees", NO_INDEXING_GUARANTEE_DISCLAIMER.lower())

        with open(self.engine.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        self.assertEqual(ledger["disclaimer"], NO_INDEXING_GUARANTEE_DISCLAIMER)


if __name__ == "__main__":
    unittest.main()
