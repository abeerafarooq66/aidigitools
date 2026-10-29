import unittest
from pathlib import Path
import tempfile
import json
import xml.etree.ElementTree as ET

from deep_audit.models import AuditIssue, DeepAuditSummary, LAB_VS_FIELD_DISCLAIMER
from deep_audit.crawler import DynamicCrawler
from deep_audit.link_checker import LinkAndAnchorAuditor
from deep_audit.seo_content_checker import SeoAndContentAuditor
from deep_audit.schema_checker import SchemaAuditor
from deep_audit.accessibility_checker import AccessibilityAuditor
from deep_audit.engine import DeepAuditEngine

class TestDeepAuditEngine(unittest.TestCase):
    """Regression test suite for Deep Audit Engine components and invariants."""

    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent

    def test_01_dynamic_discovery_no_hardcoded_assumptions(self):
        """Dynamic crawler must find all HTML pages without assuming fixed page count."""
        crawler = DynamicCrawler(self.project_root)
        pages = crawler.discover_local_html_pages()
        self.assertIsInstance(pages, list)
        self.assertGreater(len(pages), 30, "Should discover more than 30 pages dynamically")
        
        # Verify all discovered files actually exist
        for p in pages:
            self.assertTrue(p.exists())
            self.assertTrue(p.suffix == ".html")

    def test_02_dynamic_sitemap_parsing(self):
        """Sitemap parser must dynamically parse sitemap.xml without assuming fixed URL count."""
        crawler = DynamicCrawler(self.project_root)
        urls = crawler.parse_sitemap_urls()
        self.assertIsInstance(urls, list)
        self.assertGreater(len(urls), 30, "Should dynamically discover more than 30 sitemap URLs")
        for u in urls:
            self.assertTrue(u.startswith("https://aidigitools.tech"))

    def test_03_link_checker_detects_broken_links_and_anchors(self):
        """LinkAndAnchorAuditor must detect broken targets and anchors in a synthetic workspace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            p1 = tmp / "index.html"
            p1.write_text('<a href="missing.html">Broken Link</a><a href="target.html#nonexistent">Broken Anchor</a>', encoding="utf-8")
            p2 = tmp / "target.html"
            p2.write_text('<div id="valid-anchor">Content</div>', encoding="utf-8")

            auditor = LinkAndAnchorAuditor(tmp)
            issues, summary = auditor.audit_page_links([p1, p2], "2026-10-29T12:00:00Z")
            
            self.assertEqual(summary["broken_links_count"], 1)
            self.assertEqual(summary["broken_anchors_count"], 1)
            self.assertEqual(len(issues), 2)
            self.assertTrue(any(i.id == "BROKEN_INTERNAL_LINK" and i.severity == "ERROR" and i.confidence == "CONFIRMED" for i in issues))
            self.assertTrue(any(i.id == "BROKEN_FRAGMENT_ANCHOR" and i.severity == "ERROR" and i.confidence == "CONFIRMED" for i in issues))

    def test_04_schema_auditor_detects_unverified_ratings_and_malformed_json(self):
        """SchemaAuditor must flag unverified aggregateRating and malformed JSON as CONFIRMED blockers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            p1 = tmp / "tool.html"
            p1.write_text('''
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@type": "Product",
                "name": "Test Tool",
                "description": "Test description",
                "aggregateRating": {"ratingValue": "4.9", "reviewCount": "120"}
            }
            </script>
            <script type="application/ld+json">
            { malformed json without quotes: 123
            </script>
            ''', encoding="utf-8")

            auditor = SchemaAuditor(tmp)
            issues, summary = auditor.audit_page_schemas([p1], "2026-10-29T12:00:00Z")
            
            self.assertTrue(any(i.id == "UNVERIFIED_AGGREGATE_RATING" and i.severity == "CRITICAL" for i in issues))
            self.assertTrue(any(i.id == "MALFORMED_JSON_LD" and i.severity == "CRITICAL" for i in issues))

    def test_05_laboratory_performance_disclaimer_invariant(self):
        """Audit engine must enforce the explicit laboratory vs real-user Core Web Vitals disclaimer."""
        from datetime import datetime, timezone
        self.assertIn("Laboratory performance metrics", LAB_VS_FIELD_DISCLAIMER)
        self.assertIn("do NOT equate to real-user Core Web Vitals", LAB_VS_FIELD_DISCLAIMER)
        self.assertIn("CrUX field data", LAB_VS_FIELD_DISCLAIMER)

        engine = DeepAuditEngine(self.project_root)
        report = engine._generate_markdown_report({
            "summary": {
                "timestamp": "2026-10-29T12:00:00Z",
                "domain": "aidigitools.tech",
                "total_pages_discovered": 10,
                "sitemap_urls_count": 10,
                "orphan_pages_count": 0,
                "health_score": 100,
                "issues_by_severity": {"CRITICAL": 0, "ERROR": 0, "WARNING": 0, "NOTICE": 0},
                "issues_by_category": {},
            },
            "issues": []
        }, datetime.now(timezone.utc))
        
        self.assertIn("Scientific Performance Grounding & Disclaimer", report)
        self.assertIn(LAB_VS_FIELD_DISCLAIMER, report)

    def test_06_pricing_consistency_detection(self):
        """SeoAndContentAuditor must flag price discrepancies between merchant_feed and HTML schema."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            feed = tmp / "merchant_feed.xml"
            feed.write_text('''<?xml version="1.0" encoding="UTF-8"?>
            <rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
              <channel>
                <item>
                  <g:link>https://aidigitools.tech/tools/test-tool.html</g:link>
                  <g:price>1500 PKR</g:price>
                </item>
              </channel>
            </rss>''', encoding="utf-8")

            tool_dir = tmp / "tools"
            tool_dir.mkdir()
            tool = tool_dir / "test-tool.html"
            tool.write_text('''
            <title>Test Tool | AIDigiTools Pakistan</title>
            <meta name="description" content="Test tool meta description text that is long enough to satisfy requirements easily.">
            <link rel="canonical" href="https://aidigitools.tech/tools/test-tool.html">
            <h1>Test Tool</h1>
            <p class="quick-answer">Quick answer summary describing the tool with verified technical facts and pricing.</p>
            <table><tr><td>Feature</td></tr></table>
            <details><summary>FAQ</summary><p>Answer</p></details>
            <script type="application/ld+json">
            {
               "@context": "https://schema.org",
               "@type": "Product",
               "name": "Test Tool",
               "description": "Test description",
               "offers": { "price": "2500", "priceCurrency": "PKR" }
            }
            </script>
            ''', encoding="utf-8")

            auditor = SeoAndContentAuditor(tmp)
            issues = auditor.audit_pages([tool], ["https://aidigitools.tech/tools/test-tool.html"], "2026-10-29T12:00:00Z")
            
            pricing_issues = [i for i in issues if i.id == "INCONSISTENT_TOOL_PRICING"]
            self.assertEqual(len(pricing_issues), 1)
            self.assertEqual(pricing_issues[0].severity, "ERROR")
            self.assertEqual(pricing_issues[0].confidence, "CONFIRMED")
            self.assertIn("1500 PKR", pricing_issues[0].evidence)
            self.assertIn("2500 PKR", pricing_issues[0].evidence)

    def test_07_accessibility_auditor_flags_missing_viewport_and_alt(self):
        """AccessibilityAuditor must flag missing viewport and missing img alt attributes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            p = tmp / "index.html"
            p.write_text('<html><body><header></header><nav></nav><main><img src="test.png"></main><footer></footer></body></html>', encoding="utf-8")

            auditor = AccessibilityAuditor(tmp)
            issues, summary = auditor.audit_accessibility([p], "2026-10-29T12:00:00Z")

            self.assertTrue(any(i.id == "MISSING_MOBILE_VIEWPORT" and i.severity == "CRITICAL" for i in issues))
            self.assertTrue(any(i.id == "IMG_MISSING_ALT" and i.severity == "ERROR" for i in issues))

if __name__ == "__main__":
    unittest.main()
