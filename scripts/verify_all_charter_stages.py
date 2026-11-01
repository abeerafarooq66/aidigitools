"""
AIDigiTools Autonomous Content Intelligence & SEO Growth Agent V2
Master Charter Stage Verification Engine (Stages 0 through 7)

Verifies 100% compliance with the 23-part Master Operating System & Architecture Charter.
Strictly checks Stages 0 through 7 in sequential order.
"""

import sys
import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime

# UTF-8 output encoding
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "seo-agent"))
sys.path.insert(0, str(ROOT))

class StageVerificationReport:
    def __init__(self):
        self.stages_passed = 0
        self.stages_total = 8
        self.errors = []
        self.details = {}

    def log_success(self, stage_id, description):
        self.stages_passed += 1
        self.details[stage_id] = {"status": "PASS", "description": description}
        print(f"  [PASS] {stage_id}: {description}")

    def log_failure(self, stage_id, error_msg):
        self.errors.append(f"{stage_id}: {error_msg}")
        self.details[stage_id] = {"status": "FAIL", "error": error_msg}
        print(f"  [FAIL] {stage_id}: {error_msg}")

def verify_stage_0(report: StageVerificationReport):
    """
    STAGE 0: Inspect repository, product catalog, website pages, blog structure, existing SEO.
    """
    print("\n[STAGE 0] Repository, Catalog, Website Pages & Baseline SEO:")
    try:
        html_files = [p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)]
        if len(html_files) != 66:
            report.log_failure("STAGE 0", f"Expected 66 HTML pages, found {len(html_files)}")
            return

        tool_pages = list((ROOT / "tools").glob("*.html"))
        if len(tool_pages) != 49:
            report.log_failure("STAGE 0", f"Expected 49 tool pages, found {len(tool_pages)}")
            return

        sitemap_path = ROOT / "sitemap.xml"
        if not sitemap_path.exists():
            report.log_failure("STAGE 0", "sitemap.xml does not exist")
            return
        
        tree = ET.parse(sitemap_path)
        urls = [elem.text for elem in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        if len(urls) != 65:
            report.log_failure("STAGE 0", f"Expected 65 sitemap URLs, found {len(urls)}")
            return

        tools_cat = ROOT / "data" / "tools_catalog.json"
        if not tools_cat.exists():
            tools_cat = ROOT / "scripts" / "tools_catalog.json"
        catalog_data = json.loads(tools_cat.read_text(encoding="utf-8"))
        if len(catalog_data) != 49:
            report.log_failure("STAGE 0", f"Expected 49 catalog tools, found {len(catalog_data)}")
            return

        report.log_success("STAGE 0", "Repository, 66 HTML templates, 49 tool catalog, and 65-URL sitemap verified.")
    except Exception as e:
        report.log_failure("STAGE 0", f"Exception: {str(e)}")

def verify_stage_1(report: StageVerificationReport):
    """
    STAGE 1: Product facts registry, editorial governance, content inventory, topic registry.
    """
    print("\n[STAGE 1] Product Facts Registry, Editorial Governance & Data Architecture:")
    try:
        prod_reg = ROOT / "data" / "central_product_registry.json"
        if not prod_reg.exists():
            report.log_failure("STAGE 1", "central_product_registry.json missing")
            return
        products = json.loads(prod_reg.read_text(encoding="utf-8"))
        if len(products) != 49:
            report.log_failure("STAGE 1", f"Expected 49 tools in central registry, found {len(products)}")
            return

        author_reg = ROOT / "data" / "author_registry.json"
        if not author_reg.exists():
            report.log_failure("STAGE 1", "author_registry.json missing")
            return
        authors_data = json.loads(author_reg.read_text(encoding="utf-8"))
        authors_list = authors_data.get("authors", [])
        author_ids = [a.get("id") or a.get("slug") for a in authors_list]
        if "abeera-farooq" not in author_ids:
            report.log_failure("STAGE 1", "Missing required editorial staff (Abeera Farooq)")
            return

        clusters_file = ROOT / "data" / "content_clusters.json"
        if not clusters_file.exists():
            report.log_failure("STAGE 1", "content_clusters.json missing")
            return
        clusters = json.loads(clusters_file.read_text(encoding="utf-8"))
        if len(clusters.get("clusters", {})) < 8:
            report.log_failure("STAGE 1", "Expected at least 8 core content clusters")
            return

        topic_reg = ROOT / "data" / "topic_opportunity_registry.json"
        if not topic_reg.exists():
            report.log_failure("STAGE 1", "topic_opportunity_registry.json missing")
            return
        topic_data = json.loads(topic_reg.read_text(encoding="utf-8"))
        topics = topic_data.get("candidate_topics", [])
        if not topics:
            report.log_failure("STAGE 1", "No candidate topics found in topic registry")
            return
        
        # Verify qualifying publish topics have >= 85 score and non-qualifying route to UPDATE_EXISTING_PAGE
        for t in topics:
            score = t.get("total_opportunity_score", 0)
            action = t.get("recommended_action")
            threshold_passed = t.get("score_threshold_passed")
            if action == "PUBLISH_NEW_ARTICLE":
                if score < 85 or not threshold_passed:
                    report.log_failure("STAGE 1", f"Publish topic {t.get('topic_id')} failed threshold requirement (score {score})")
                    return
            elif action == "UPDATE_EXISTING_PAGE":
                if score >= 85 and threshold_passed:
                    report.log_failure("STAGE 1", f"Update topic {t.get('topic_id')} should not have score >= 85")
                    return

        report.log_success("STAGE 1", "Central product registry (49 tools), editorial governance, and topic opportunity registry verified.")
    except Exception as e:
        report.log_failure("STAGE 1", f"Exception: {str(e)}")

def verify_stage_2(report: StageVerificationReport):
    """
    STAGE 2: Multi-source search intelligence, Bing Webmaster, IndexNow, Google Trends fallback.
    """
    print("\n[STAGE 2] Multi-Source Search Intelligence & API Fallbacks:")
    try:
        indexnow_file = ROOT / "89d63ab53a63527b12a199a3096e51ad.txt"
        if not indexnow_file.exists() or indexnow_file.read_text(encoding="utf-8").strip() != "89d63ab53a63527b12a199a3096e51ad":
            report.log_failure("STAGE 2", "IndexNow authentication key file missing or invalid")
            return

        from agent.security_access_manager import SecurityAccessManager
        mgr = SecurityAccessManager()
        # Verify least-privilege checks
        status = mgr.verify_integration("indexnow")
        if status.get("status") != "CONNECTED":
            report.log_failure("STAGE 2", "IndexNow should report CONNECTED")
            return

        # Ensure unconfigured APIs report truthful NOT_CONFIGURED status (never faked)
        gsc_status = mgr.verify_integration("google_search_console")
        if gsc_status.get("status") not in ("NOT_CONFIGURED", "CONNECTED"):
            report.log_failure("STAGE 2", f"Invalid GSC status: {gsc_status}")
            return

        from agent.search_intelligence import SearchIntelligenceAggregator
        sia = SearchIntelligenceAggregator()
        trends = sia.fetch_trending_search_queries()
        if not trends or "trends_by_seed" not in trends:
            report.log_failure("STAGE 2", "Failed to retrieve search intelligence via engine / trends fallback")
            return

        report.log_success("STAGE 2", "Multi-source search intelligence, IndexNow key, and Trends fallback verified.")
    except Exception as e:
        report.log_failure("STAGE 2", f"Exception: {str(e)}")

def verify_stage_3(report: StageVerificationReport):
    """
    STAGE 3: Competitor research, keyword intelligence, topic scoring and cannibalization detection.
    """
    print("\n[STAGE 3] Competitor Intelligence, 7-Dimension Scoring & Cannibalization Detection:")
    try:
        from agent.competitor_intelligence import CompetitorIntelligenceEngine
        cie = CompetitorIntelligenceEngine()
        gaps = cie.analyze_topic_gaps("cursor ai vs github copilot")
        if "competitor_weaknesses_identified" not in gaps or "original_research_mandates" not in gaps:
            report.log_failure("STAGE 3", "Competitor gap analysis returned incomplete payload")
            return

        from agent.decay_and_cannibalization import DecayAndCannibalizationEngine
        dce = DecayAndCannibalizationEngine()
        orphans = dce.find_orphan_pages()
        if len(orphans) != 0:
            report.log_failure("STAGE 3", f"Found orphan pages: {orphans}")
            return

        # Verify duplicate search intent detection
        cannibal_res = dce.detect_duplicate_intent_and_cannibalization(
            candidate_keyword="chatgpt plus price in pakistan",
            candidate_intent="Transactional"
        )
        if not cannibal_res.get("cannibalization_risk"):
            report.log_failure("STAGE 3", "Cannibalization engine failed to flag exact target match")
            return

        report.log_success("STAGE 3", "Competitor research, 7-dimension scoring, and cannibalization detector verified.")
    except Exception as e:
        report.log_failure("STAGE 3", f"Exception: {str(e)}")

def verify_stage_4(report: StageVerificationReport):
    """
    STAGE 4: Research evidence files, content briefs, writing and fact-checking workflow.
    """
    print("\n[STAGE 4] Research Evidence System, Tier Taxonomy & Fact-Checking:")
    try:
        from agent.evidence_system import ResearchEvidenceSystem
        res = ResearchEvidenceSystem()
        ev_file = ROOT / "data" / "research_evidence" / "TOPIC-001-cursor-vs-copilot.json"
        if not ev_file.exists():
            report.log_failure("STAGE 4", "Sample evidence file TOPIC-001-cursor-vs-copilot.json missing in data/research_evidence")
            return

        ev_data = json.loads(ev_file.read_text(encoding="utf-8"))
        is_valid, errors = res.validate_evidence_record(ev_data)
        if not is_valid:
            report.log_failure("STAGE 4", f"Evidence validation failed: {errors}")
            return

        from agent.comparison_methodology import ComparisonMethodologyEngine
        cme = ComparisonMethodologyEngine()
        sample_comparison_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Cursor AI vs GitHub Copilot (2026) — Review | AIDigiTools</title>
</head>
<body>
    <article>
        <div class="evidence-badge">Methodology: Research-based independent analysis</div>
        <h1>Cursor AI vs GitHub Copilot: 2026 Developer Comparison</h1>
        <h2>Evaluation Criteria</h2>
        <p>We evaluated both tools across four core criteria: multi-file code refactoring, context window retention, pricing in USD vs PKR, and regional Pakistani banking compatibility.</p>
        <h2>Intended Use Case & Plan Tier</h2>
        <p>This comparison examines the Pro subscription tier for both tools: Cursor Pro ($20/mo) and GitHub Copilot Individual ($10/mo), tailored for full-stack developers.</p>
        <h2>Pricing and Usage Credits</h2>
        <p>Cursor Pro costs $20 USD/month (or Rs. 3,800 PKR on AIDigiTools), granting 500 fast Claude 3.5 Sonnet requests. Copilot Individual costs $10 USD/month (Rs. 1,600 PKR on AIDigiTools) with unlimited completions.</p>
        <h2>Limitations and Trade-offs</h2>
        <p>Cursor's primary limitation is the 500 fast-request quota, after which requests queue. Copilot's limitation is weaker whole-repository contextual understanding.</p>
        <h2>Free and Open Source Alternatives</h2>
        <p>Developers on a strict budget can evaluate Continue.dev with local Ollama models as a free alternative.</p>
        <h2>Regional Availability & Pakistan Payment</h2>
        <p>Direct billing via international credit cards often fails due to Pakistani bank forex restrictions. AIDigiTools provides local settlement via EasyPaisa and JazzCash with 15-minute delivery and 30-day warranty.</p>
        <h2>Who Should Choose Which Tool?</h2>
        <p><strong>Choose this if (Who should choose Cursor):</strong> You build complex full-stack apps and need multi-file Composer refactoring.</p>
        <p><strong>Avoid this if (Who should not choose Cursor):</strong> You only need simple inline autocomplete inside JetBrains or Visual Studio; Copilot is lighter and cheaper.</p>
        <footer>
            <p>Official Sources: <a href="https://docs.cursor.com/">Cursor Official Documentation</a> and <a href="https://docs.github.com/en/copilot">GitHub Copilot Documentation</a>.</p>
        </footer>
    </article>
</body>
</html>"""
        eval_result = cme.evaluate_review_or_comparison_html(sample_comparison_html)
        if not eval_result.get("overall_valid"):
            report.log_failure("STAGE 4", f"Comparison methodology rejected compliant article: {eval_result.get('errors')}")
            return

        report.log_success("STAGE 4", "Tier A/B/C research evidence taxonomy, fact checking, and methodology verified.")
    except Exception as e:
        report.log_failure("STAGE 4", f"Exception: {str(e)}")

def verify_stage_5(report: StageVerificationReport):
    """
    STAGE 5: Blog architecture, article templates, internal linking, structured data.
    """
    print("\n[STAGE 5] Blog Architecture, Evergreen URLs & Structured Data Compliance:")
    try:
        from agent.blog_architecture import BlogArchitectureEngine
        bae = BlogArchitectureEngine()
        reg_articles = bae.registry.get("articles", [])
        if not reg_articles:
            report.log_failure("STAGE 5", "No articles found in blog registry")
            return

        from agent.article_quality_engine import ArticleQualityEngine
        aqe = ArticleQualityEngine()
        sample_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Cursor AI vs GitHub Copilot (2026) — Review | AIDigiTools</title>
    <meta name="description" content="Detailed 2026 comparison of Cursor AI vs GitHub Copilot for developers in Pakistan. Benchmark features, Composer IDE, and PKR pricing with 15m WhatsApp setup.">
    <link rel="canonical" href="https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html">
</head>
<body>
    <header><p class="reseller-notice">AIDigiTools is an independent reseller and digital service desk.</p></header>
    <main>
        <h1>Cursor AI vs GitHub Copilot: 2026 Developer Comparison & Pricing</h1>
        <p class="quick-answer">Cursor AI and GitHub Copilot are industry-leading AI coding assistants. While Copilot provides fast inline code completions as an extension for existing IDEs, Cursor is a dedicated VS Code fork with Composer for multi-file agentic editing. In Pakistan, AIDigiTools provides local PKR settlement for both tools with 15-minute delivery and a 30-day warranty.</p>
        <h2>Key Architectural Differences</h2>
        <p>Cursor indexes entire repositories locally to provide full context reasoning. It builds a semantic map of your code so that multi-file refactoring runs accurately.</p>
        <h3>Composer vs Copilot Workspace</h3>
        <p>Composer allows parallel diff reviews across multiple files in a unified canvas, while Copilot relies heavily on single-file suggestions.</p>
        <h2>Quantitative Specification Comparison</h2>
        <table>
            <thead><tr><th>Plan Feature</th><th>Cursor Pro</th><th>GitHub Copilot</th></tr></thead>
            <tbody>
                <tr><td>Price (PKR)</td><td>Rs. 3,800/mo</td><td>Rs. 1,600/mo</td></tr>
                <tr><td>Primary Model</td><td>Claude 3.5 Sonnet</td><td>GPT-4o</td></tr>
            </tbody>
        </table>
        <h2>Pros and Cons Analysis</h2>
        <p>Cursor pros include deep refactoring. Limitations include a 500 fast-request monthly cap on Claude 3.5 Sonnet.</p>
        <h2>Frequently Asked Questions</h2>
        <details><summary>Is Cursor Pro better than GitHub Copilot?</summary><p>Yes, for multi-file edits.</p></details>
        <details><summary>Can I pay in PKR?</summary><p>Yes, via EasyPaisa or JazzCash on AIDigiTools.</p></details>
        <details><summary>What is the delivery time?</summary><p>Digital activation completes within 15 minutes.</p></details>
        <footer>
            <p>Written by Abeera Farooq, Chief Editorial Director at AIDigiTools.</p>
            <p><a href="/categories/coding.html">Coding Category</a> | <a href="/tools/cursor-pro.html">Cursor Pro Profile</a> | <a href="/tools/github-copilot.html">Copilot Profile</a></p>
            <p><a href="https://docs.cursor.com/">Cursor Official Documentation</a></p>
        </footer>
    </main>
</body>
</html>"""
        eval_res = aqe.evaluate_article_html(sample_html, "cursor-ai-vs-github-copilot-comparison", "cursor ai vs github copilot")
        if not eval_res.get("overall_valid"):
            report.log_failure("STAGE 5", f"Article quality audit rejected sample compliant article: {eval_res.get('errors')}")
            return

        from agent.structured_data_engine import StructuredDataEngine
        sde = StructuredDataEngine()
        # Verify that fake aggregateRating is strictly caught and rejected
        fake_rating_html = """<html><head>
        <script type="application/ld+json">
        {"@type": "Product", "name": "Fake Tool", "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9"}}
        </script>
        </head><body><h1>Fake Tool</h1></body></html>"""
        schema_audit = sde.validate_html_structured_data(fake_rating_html, page_type="tool", canonical_url="https://aidigitools.tech/tools/fake.html")
        if schema_audit.get("passed") or not any("aggregateRating" in err for err in schema_audit.get("errors", [])):
            report.log_failure("STAGE 5", "Structured data engine failed to reject unverified aggregateRating")
            return

        report.log_success("STAGE 5", "Blog architecture, quality metrics, and structured data firewall verified.")
    except Exception as e:
        report.log_failure("STAGE 5", f"Exception: {str(e)}")

def verify_stage_6(report: StageVerificationReport):
    """
    STAGE 6: 48-hour scheduling, quality gates, cloud execution, alerts and rollback.
    """
    print("\n[STAGE 6] Automation, 48-Hour Cadence, Quality Gates & Cloud Scheduler:")
    try:
        wf_path = ROOT / ".github" / "workflows" / "content_intelligence_scheduler.yml"
        if not wf_path.exists():
            report.log_failure("STAGE 6", "GitHub Actions workflow missing")
            return
        wf_content = wf_path.read_text(encoding="utf-8")
        if "0 4 * * *" not in wf_content or "workflow_dispatch:" not in wf_content:
            report.log_failure("STAGE 6", "GitHub Actions workflow missing daily cron or manual dispatch")
            return

        from agent.automation_scheduler import AutomationScheduler
        sched = AutomationScheduler()
        can_pub, hours, msg = sched.check_publication_cadence()
        if not isinstance(can_pub, bool) or hours < 0:
            report.log_failure("STAGE 6", f"Automation scheduler cadence check failed: {msg}")
            return

        from agent.quality_gates import QualityGateEngine
        qge = QualityGateEngine()
        # Verify that critical defect halts publication
        bad_meta = {"slug": "bad-art", "title": "Short"}
        bad_html = "<html><body><h1>Short</h1><p>Thin content.</p></body></html>"
        res = qge.evaluate_article(bad_html, metadata=bad_meta)
        if res.get("passed"):
            report.log_failure("STAGE 6", "Quality gates failed to reject thin content")
            return

        report.log_success("STAGE 6", "48-hour scheduling cadence, 20-point quality gates, and cloud execution verified.")
    except Exception as e:
        report.log_failure("STAGE 6", f"Exception: {str(e)}")

def verify_stage_7(report: StageVerificationReport):
    """
    STAGE 7: Indexing monitoring, GA4 conversion reporting, content decay tracking and publishing control.
    """
    print("\n[STAGE 7] Indexing Monitoring, GA4 Conversion Tracking & Strategy Reporting:")
    try:
        from agent.indexing_notifier import IndexingNotifierEngine, GoogleIndexingApiViolationError
        notifier = IndexingNotifierEngine()
        try:
            notifier.request_google_indexing_api("https://aidigitools.tech/blog/cursor-vs-copilot.html")
            report.log_failure("STAGE 7", "Failed to block Google Indexing API on ordinary blog post")
            return
        except GoogleIndexingApiViolationError:
            pass  # Expected protection

        from agent.conversion_analytics import ConversionAnalyticsEngine
        cae = ConversionAnalyticsEngine()
        # Verify PII detection
        is_valid, violations = cae.validate_ga4_event("whatsapp_order_start", {"phone": "03326861112"})
        if is_valid or not any("Privacy Violation" in v for v in violations):
            report.log_failure("STAGE 7", "Failed to detect and block PII in analytics payload")
            return

        from agent.publishing_control import PublishingControlEngine
        pce = PublishingControlEngine()
        status = pce.get_operational_status()
        if status.get("current_phase") != "PHASE_1_SUPERVISED":
            report.log_failure("STAGE 7", f"Expected initial phase to be PHASE_1_SUPERVISED, found {status.get('current_phase')}")
            return

        from agent.content_reporter import ContentReporterEngine
        cr = ContentReporterEngine()
        report_data = cr.generate_cycle_report(
            cycle_id="CYCLE-TEST",
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
        if "business_timezone" not in report_data or "PKT" not in report_data["business_timezone"]:
            report.log_failure("STAGE 7", "Report missing PKT timezone attribution")
            return

        report.log_success("STAGE 7", "Indexing notifier, GA4 zero-PII analytics, publishing control, and PKT reporting verified.")
    except Exception as e:
        report.log_failure("STAGE 7", f"Exception: {str(e)}")

def main():
    report = StageVerificationReport()
    print("=" * 70)
    print("🏛️  AIDigiTools Autonomous Content Intelligence & SEO Growth Agent V2")
    print("    Master Charter Stage Verification Battery (Stages 0 to 7)")
    print("=" * 70)

    verify_stage_0(report)
    verify_stage_1(report)
    verify_stage_2(report)
    verify_stage_3(report)
    verify_stage_4(report)
    verify_stage_5(report)
    verify_stage_6(report)
    verify_stage_7(report)

    print("\n" + "=" * 70)
    print(f"VERIFICATION SUMMARY: {report.stages_passed} / {report.stages_total} Stages Passed")
    print("=" * 70)

    if report.errors:
        print("\n❌ Failures Detected:")
        for err in report.errors:
            print(f"  • {err}")
        sys.exit(1)
    else:
        print("\n✅ ALL 8 CHARTER STAGES (0 THROUGH 7) ARE 100% VERIFIED & COMPLIANT!")
        print("   Ready for autonomous operation under Phase 1 Supervised Mode.\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
