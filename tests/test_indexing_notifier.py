"""
Unit Tests for Indexing & Search Engine Notification Engine (Part 19).
======================================================================
Strictly tests Part 19 of Master Architecture Charter:
INDEXING AND SEARCH ENGINE NOTIFICATIONS.

Validates:
1. Accurate sitemap updates with verified lastmod values.
2. IndexNow Bing notifications with key verification.
3. Strict prohibition firewall against using Google Indexing API for blog posts.
4. Technical indexing problem detection (canonical mismatch, noindex, missing tags).
5. Ledger persistence of URL status and last checked date in PKT.
6. Search engine autonomy disclaimer (no guarantee of indexing or ranking).
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

        # Create dummy HTML files
        (self.workspace / "index.html").write_text(
            '<!DOCTYPE html><html><head><link rel="canonical" href="https://aidigitools.tech/"><meta name="robots" content="index, follow"></head><body>Home</body></html>',
            encoding="utf-8"
        )
        (self.workspace / "deals.html").write_text(
            '<!DOCTYPE html><html><head><link rel="canonical" href="https://aidigitools.tech/deals.html"><meta name="robots" content="index, follow"></head><body>Deals</body></html>',
            encoding="utf-8"
        )
        (self.workspace / "tools").mkdir(parents=True, exist_ok=True)
        (self.workspace / "tools" / "chatgpt-plus.html").write_text(
            '<!DOCTYPE html><html><head><link rel="canonical" href="https://aidigitools.tech/tools/chatgpt-plus.html"><meta name="robots" content="index, follow"></head><body>ChatGPT Plus</body></html>',
            encoding="utf-8"
        )

        self.engine = IndexingNotifierEngine(workspace_root=self.workspace)

    def tearDown(self):
        """Clean up isolated directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_accurate_sitemap_synchronization_and_lastmod(self):
        """Sitemap must be generated with accurate lastmod, loc, priority, and XML structure."""
        res = self.engine.sync_sitemap(dry_run=False)
        self.assertEqual(res["total_urls"], 3)
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
        res = self.engine.notify_indexnow(urls=urls, dry_run=True)
        self.assertTrue(res["success"])
        self.assertTrue(res["key_file_exists_locally"])
        self.assertEqual(res["submitted_count"], 2)
        self.assertEqual(res["key"], "89d63ab53a63527b12a199a3096e51ad")
        self.assertIn("guarantees", res["disclaimer"].lower())
        self.assertIn("neither sitemap submission", res["disclaimer"].lower())

    def test_technical_indexing_audit_and_ledger_persistence(self):
        """Technical indexing audit must record URL status, HTTP status, and last checked date in PKT."""
        audit_res = self.engine.run_technical_indexing_audit()
        self.assertEqual(audit_res["total_urls_audited"], 3)
        self.assertEqual(audit_res["total_healthy"], 3)
        self.assertEqual(audit_res["total_issues"], 0)

        # Verify persistence to disk
        self.assertTrue(self.engine.indexing_ledger_path.exists())
        with open(self.engine.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        self.assertEqual(ledger["total_monitored_urls"], 3)
        self.assertEqual(ledger["total_healthy_urls"], 3)
        self.assertIn("https://aidigitools.tech/", ledger["urls"])
        home_record = ledger["urls"]["https://aidigitools.tech/"]
        self.assertEqual(home_record["status"], "HEALTHY")
        self.assertEqual(home_record["http_status"], 200)
        self.assertTrue(home_record["last_checked_date_pkt"].endswith(" PKT"))

    def test_canonical_and_robots_issue_detection(self):
        """Audit must accurately flag missing canonical tags, canonical mismatches, and noindex directives."""
        # Case A: Missing canonical tag
        html_missing_canon = "<html><head></head><body>No canon</body></html>"
        res_a = self.engine.audit_canonical_and_robots(html_missing_canon, "https://aidigitools.tech/page.html")
        self.assertFalse(res_a["is_valid"])
        self.assertIn("Missing <link rel='canonical'> tag", res_a["issues"][0])

        # Case B: Canonical mismatch
        html_mismatch = '<html><head><link rel="canonical" href="http://wrong-domain.com/page.html"></head></html>'
        res_b = self.engine.audit_canonical_and_robots(html_mismatch, "https://aidigitools.tech/page.html")
        self.assertFalse(res_b["is_valid"])
        self.assertIn("Canonical mismatch", res_b["issues"][0])

        # Case C: Blocking noindex tag
        html_noindex = '<html><head><link rel="canonical" href="https://aidigitools.tech/page.html"><meta name="robots" content="noindex, follow"></head></html>'
        res_c = self.engine.audit_canonical_and_robots(html_noindex, "https://aidigitools.tech/page.html")
        self.assertFalse(res_c["is_valid"])
        self.assertIn("blocking robots meta directive", res_c["issues"][0])

    def test_no_ranking_or_indexing_guarantee_disclaimer(self):
        """All outputs and ledger metadata must include the mandatory search engine autonomy disclaimer."""
        self.assertIn("Neither sitemap submission", NO_INDEXING_GUARANTEE_DISCLAIMER)
        self.assertIn("guarantees", NO_INDEXING_GUARANTEE_DISCLAIMER.lower())

        with open(self.engine.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        self.assertEqual(ledger["disclaimer"], NO_INDEXING_GUARANTEE_DISCLAIMER)


if __name__ == "__main__":
    unittest.main()
