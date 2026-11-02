"""
AIDigiTools Autonomous Content Intelligence & SEO Growth Agent V2
Master Charter Implementation Test Suite (Stages 0 to 7)

Validates complete implementation of the 23-part Master Operating System & Architecture Charter.
"""

import os
import sys
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "seo-agent"))
sys.path.insert(0, str(ROOT))

class TestCharterImplementation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = ROOT
        cls.data_dir = ROOT / "data"

    # --------------------------------------------------------------------------
    # STAGE 0: Repository, Catalog, Website Pages & Baseline SEO
    # --------------------------------------------------------------------------
    def test_stage_0_catalog_and_inventory(self):
        html_files = [p for p in self.root.glob("**/*.html") if not any(part in ("data", "tests", "scratch") or part.startswith((".", "venv", "node_modules")) for part in p.parts)]
        self.assertEqual(len(html_files), 66, f"Expected 66 HTML templates, found {len(html_files)}")

        tool_pages = list((self.root / "tools").glob("*.html"))
        self.assertEqual(len(tool_pages), 49, f"Expected 49 tool pages, found {len(tool_pages)}")

        sitemap_path = self.root / "sitemap.xml"
        self.assertTrue(sitemap_path.exists(), "sitemap.xml missing")
        tree = ET.parse(sitemap_path)
        urls = [elem.text for elem in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(len(urls), 65, f"Expected 65 sitemap URLs, found {len(urls)}")

        tools_cat = self.root / "data" / "tools_catalog.json"
        if not tools_cat.exists():
            tools_cat = self.root / "scripts" / "tools_catalog.json"
        cat_data = json.loads(tools_cat.read_text(encoding="utf-8"))
        self.assertEqual(len(cat_data), 49, f"Expected 49 catalog items, found {len(cat_data)}")

    # --------------------------------------------------------------------------
    # STAGE 1: Product Facts Registry, Editorial Governance & Data Architecture
    # --------------------------------------------------------------------------
    def test_stage_1_registries_and_governance(self):
        prod_path = self.data_dir / "central_product_registry.json"
        self.assertTrue(prod_path.exists(), "central_product_registry.json missing")
        products = json.loads(prod_path.read_text(encoding="utf-8"))
        self.assertEqual(len(products), 49, f"Expected 49 products in registry, found {len(products)}")

        author_path = self.data_dir / "author_registry.json"
        self.assertTrue(author_path.exists(), "author_registry.json missing")
        author_data = json.loads(author_path.read_text(encoding="utf-8"))
        authors = author_data.get("authors", [])
        slugs = [a.get("slug") or a.get("id") for a in authors]
        self.assertIn("abeera-farooq", slugs, "Abeera Farooq must be registered")

        clusters_path = self.data_dir / "content_clusters.json"
        self.assertTrue(clusters_path.exists(), "content_clusters.json missing")
        clusters_data = json.loads(clusters_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(clusters_data.get("clusters", {})), 8)

        topic_path = self.data_dir / "topic_opportunity_registry.json"
        self.assertTrue(topic_path.exists(), "topic_opportunity_registry.json missing")
        topic_data = json.loads(topic_path.read_text(encoding="utf-8"))
        topics = topic_data.get("candidate_topics", [])
        self.assertGreaterEqual(len(topics), 4)

        for t in topics:
            if t.get("recommended_action") == "PUBLISH_NEW_ARTICLE":
                self.assertGreaterEqual(t.get("total_opportunity_score", 0), 85)
                self.assertTrue(t.get("score_threshold_passed"))

    # --------------------------------------------------------------------------
    # STAGE 2: Multi-Source Search Intelligence & API Fallbacks
    # --------------------------------------------------------------------------
    def test_stage_2_search_intelligence_and_api_security(self):
        indexnow_file = self.root / "89d63ab53a63527b12a199a3096e51ad.txt"
        self.assertTrue(indexnow_file.exists(), "IndexNow key file missing")
        self.assertEqual(indexnow_file.read_text(encoding="utf-8").strip(), "89d63ab53a63527b12a199a3096e51ad")

        from agent.security_access_manager import SecurityAccessManager
        mgr = SecurityAccessManager()
        # Verify IndexNow reports CONNECTED
        idx_status = mgr.verify_integration("indexnow")
        self.assertEqual(idx_status.get("status"), "CONNECTED")

        # Verify unconfigured API reports truthful NOT_CONFIGURED (never faked)
        gsc_status = mgr.verify_integration("google_search_console")
        self.assertIn(gsc_status.get("status"), ["NOT_CONFIGURED", "CONNECTED"])

        from agent.search_intelligence import SearchIntelligenceAggregator
        sia = SearchIntelligenceAggregator()
        trends = sia.fetch_trending_search_queries()
        self.assertIn("trends_by_seed", trends)
        self.assertEqual(trends.get("provenance", {}).get("status"), "CONNECTED")

    # --------------------------------------------------------------------------
    # STAGE 3: Competitor Research & Cannibalization Prevention
    # --------------------------------------------------------------------------
    def test_stage_3_competitor_and_cannibalization(self):
        from agent.competitor_intelligence import CompetitorIntelligenceEngine
        cie = CompetitorIntelligenceEngine()
        gaps = cie.analyze_topic_gaps("cursor ai vs github copilot")
        self.assertIn("competitor_weaknesses_identified", gaps)
        self.assertIn("original_research_mandates", gaps)

        from agent.decay_and_cannibalization import DecayAndCannibalizationEngine
        dce = DecayAndCannibalizationEngine()
        orphans = dce.find_orphan_pages()
        self.assertEqual(len(orphans), 0, f"Orphan pages found: {orphans}")

        cannibal_check = dce.detect_duplicate_intent_and_cannibalization(
            candidate_keyword="chatgpt plus price in pakistan",
            candidate_intent="Transactional"
        )
        self.assertTrue(cannibal_check.get("cannibalization_risk"))
        self.assertEqual(cannibal_check.get("recommendation"), "UPDATE_EXISTING_PAGE")

    # --------------------------------------------------------------------------
    # STAGE 4: Research Evidence System & Fact Checking
    # --------------------------------------------------------------------------
    def test_stage_4_evidence_system_and_methodology(self):
        from agent.evidence_system import ResearchEvidenceSystem
        res = ResearchEvidenceSystem()
        ev_file = self.data_dir / "research_evidence" / "TOPIC-001-cursor-vs-copilot.json"
        self.assertTrue(ev_file.exists(), "Sample evidence file missing")
        ev_data = json.loads(ev_file.read_text(encoding="utf-8"))
        is_valid, errors = res.validate_evidence_record(ev_data)
        self.assertTrue(is_valid, f"Evidence validation errors: {errors}")

        # Test fabrication rejection
        fabricated_data = dict(ev_data)
        fabricated_data["research_methodology"] = "we tested this on 500 developers in our secret benchmark"
        is_valid_fab, errors_fab = res.validate_evidence_record(fabricated_data)
        self.assertFalse(is_valid_fab)
        self.assertTrue(any("Fabrication Violation" in e for e in errors_fab))

        from agent.comparison_methodology import ComparisonMethodologyEngine
        cme = ComparisonMethodologyEngine()
        compliant_snippet = """<!DOCTYPE html>
<html><body>
<div class="badge">Research-based</div>
<h1>Cursor vs Copilot</h1>
<h2>Plan Comparison & Pro Tier Subscription</h2>
<p>In our comparison criteria we tested version 2026 releases ideal for full-stack developers.</p>
<h2>Pricing Separation and Credits</h2>
<p>Official USD price is $20 per month for the Pro subscription plan; AIDigiTools local concierge price is 4,500 PKR monthly with 1,000 credits.</p>
<p>In Pakistan, credit cards often decline. EasyPaisa is supported.</p>
<h2>Who Should Choose vs Who Should Not Choose</h2>
<p>Who should choose Cursor: multi-file editors. Who should not choose Cursor: single-file developers.</p>
<p>Drawbacks and limitations include rate limits. Open source alternative is Continue.dev.</p>
<p><a href="https://docs.cursor.com">Cursor Documentation</a></p>
</body></html>"""
        eval_res = cme.evaluate_review_or_comparison_html(compliant_snippet)
        self.assertTrue(eval_res.get("overall_valid"), f"Methodology violations: {eval_res.get('errors')}")

    # --------------------------------------------------------------------------
    # STAGE 5: Blog Architecture & Structured Data Standards
    # --------------------------------------------------------------------------
    def test_stage_5_blog_architecture_and_schema(self):
        from agent.blog_architecture import BlogArchitectureEngine
        bae = BlogArchitectureEngine()
        is_valid, url_errs = bae.validate_article_url("https://aidigitools.tech/blog/cursor-vs-copilot.html")
        self.assertTrue(is_valid)

        # Ensure date-based URLs are rejected
        is_date_valid, date_errs = bae.validate_article_url("https://aidigitools.tech/blog/2026/11/01/cursor.html")
        self.assertFalse(is_date_valid)

        from agent.structured_data_engine import StructuredDataEngine
        sde = StructuredDataEngine()
        fake_rating_html = """<html><head>
        <script type="application/ld+json">
        {"@type": "Product", "name": "Fake Tool", "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9"}}
        </script></head><body><h1>Fake Tool</h1></body></html>"""
        audit = sde.validate_html_structured_data(fake_rating_html, page_type="tool", canonical_url="https://aidigitools.tech/tools/fake.html")
        self.assertFalse(audit.get("passed"))
        self.assertTrue(any("aggregateRating" in err for err in audit.get("errors", [])))

    # --------------------------------------------------------------------------
    # STAGE 6: Automation, 48h Cadence, Quality Gates & Rollback
    # --------------------------------------------------------------------------
    def test_stage_6_automation_scheduler_and_quality_gates(self):
        wf_path = self.root / ".github" / "workflows" / "content_intelligence_scheduler.yml"
        self.assertTrue(wf_path.exists())
        wf_text = wf_path.read_text(encoding="utf-8")
        self.assertIn("0 4 * * *", wf_text)  # 09:00 PKT daily cloud runner

        from agent.automation_scheduler import AutomationScheduler
        sched = AutomationScheduler()
        can_pub, hours, msg = sched.check_publication_cadence()
        self.assertIsInstance(can_pub, bool)

        from agent.quality_gates import QualityGateEngine
        qge = QualityGateEngine()
        # Verify 20 Quality Gates reject thin, broken content
        bad_meta = {"slug": "bad-art", "title": "Short"}
        bad_html = "<html><body><h1>Short</h1><p>Thin text.</p></body></html>"
        res = qge.evaluate_article(bad_html, metadata=bad_meta)
        self.assertFalse(res.get("passed"))
        self.assertGreater(len(res.get("critical_failures", [])), 0)

    # --------------------------------------------------------------------------
    # STAGE 7: Indexing Monitoring, GA4 Conversion & Publishing Control
    # --------------------------------------------------------------------------
    def test_stage_7_indexing_analytics_and_publishing_control(self):
        from agent.indexing_notifier import IndexingNotifierEngine, GoogleIndexingApiViolationError
        notifier = IndexingNotifierEngine()
        with self.assertRaises(GoogleIndexingApiViolationError):
            notifier.request_google_indexing_api("https://aidigitools.tech/blog/cursor-vs-copilot.html")

        from agent.conversion_analytics import ConversionAnalyticsEngine
        cae = ConversionAnalyticsEngine()
        is_valid, violations = cae.validate_ga4_event("whatsapp_order_start", {"phone": "03326861112"})
        self.assertFalse(is_valid)
        self.assertTrue(any("Privacy Violation" in v for v in violations))

        from agent.publishing_control import PublishingControlEngine
        pce = PublishingControlEngine()
        status = pce.get_operational_status()
        self.assertIn(status.get("current_phase"), ["FULL_AUTONOMOUS", "PHASE_1_SUPERVISED", "PHASE_2_AUTONOMOUS_LOW_RISK"])

        from agent.content_reporter import ContentReporterEngine
        cr = ContentReporterEngine()
        report_data = cr.generate_cycle_report(
            cycle_id="CYCLE-UNIT-TEST",
            data_sources_accessed=["Google Trends Fallback", "IndexNow"],
            data_sources_unavailable=["GSC"],
            search_opportunity_findings={"score": 92},
            selected_topic={"topic_id": "TOPIC-001", "primary_keyword": "cursor ai vs github copilot"},
            primary_keyword="cursor ai vs github copilot",
            secondary_keywords=["cursor vs copilot"],
            search_intent="Commercial Investigation",
            competitor_gap="No quantitative comparison tables or PKR rates",
            relevant_products=["cursor-pro", "github-copilot"],
            research_sources=["https://cursor.com"],
            evidence_status={"classification": "B. Research-based", "verified": True},
            quality_gate_results={"passed": True, "critical_failures": []},
            decision="APPROVED",
            decision_reason="Passed all 20 Quality Gates in Phase 1 Supervised Mode."
        )
        self.assertIn("business_timezone", report_data)
        self.assertIn("PKT", report_data["business_timezone"])

if __name__ == "__main__":
    unittest.main()
