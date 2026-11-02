"""
AIDigiTools — Gemini Generation & Quality Gate Regression Test Suite
=====================================================================
Covers 10 mandatory production regression invariants:
1. Gemini HTTP 404 stops production generation (allow_fallback=False returns failure).
2. Fallback article cannot receive APPROVED status (fails Gate 5).
3. Missing registry matches never create default prices (returns UNKNOWN or omitted).
4. Unverified benchmark claims fail Gate 10.
5. Evidence verification actually evaluates article claims and rejects unsupported statements.
6. Cursor Pro pricing matches registry (Rs. 3,800 / $14.0).
7. Comparison article contains real comparison information for both products.
8. No article is published before human approval (Phase 1 Supervised Mode lock).
9. Preview file paths are correctly persisted as repository-relative (data/previews/...).
10. Failed generation does not create a pending approval preview.
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

from agent.gemini_generator import GeminiArticleGenerator
from agent.quality_gates import QualityGateEngine
from agent.evidence_system import ResearchEvidenceSystem
from agent.publishing_control import PublishingControlEngine, PHASE_1_SUPERVISED
from agent.automation_scheduler import AutomationScheduler


class TestGeminiGenerationQualityGateRegression(unittest.TestCase):
    def setUp(self):
        self.workspace_root = ROOT_DIR
        self.gemini_gen = GeminiArticleGenerator(workspace_root=self.workspace_root)
        self.gate_engine = QualityGateEngine(self.workspace_root)
        self.evidence_sys = ResearchEvidenceSystem(self.workspace_root / "data" / "research_evidence")
        self.pub_control = PublishingControlEngine(self.workspace_root)
        self.scheduler = AutomationScheduler(self.workspace_root)

    def tearDown(self):
        # Clean up test previews if created
        for p in (self.workspace_root / "data" / "previews").glob("test-*.html"):
            try:
                p.unlink()
            except Exception:
                pass
        for e in (self.workspace_root / "data" / "research_evidence").glob("EVID-test-*.json"):
            try:
                e.unlink()
            except Exception:
                pass

    def test_01_gemini_http_404_stops_production_generation(self):
        """
        Invariant 1: When Gemini API returns HTTP 404, and allow_fallback=False,
        generation halts with status GENERATION_FAILED and never returns heuristic fallback.
        """
        gen_with_key = GeminiArticleGenerator(api_key="mock-test-key", workspace_root=self.workspace_root)
        mock_discovery = {
            "status": "MODEL_DISCOVERY_VERIFIED",
            "supported_models": ["models/gemini-2.0-flash"],
            "primary_model": "models/gemini-2.0-flash",
            "http_status": 200
        }
        mock_endpoint = {
            "status": "GENERATION_FAILED",
            "verified": False,
            "model": "models/gemini-2.0-flash",
            "http_status": 404,
            "error": "HTTP 404: Model not found"
        }
        with patch.object(gen_with_key, "discover_supported_models", return_value=mock_discovery), \
             patch.object(gen_with_key, "verify_generation_endpoint", return_value=mock_endpoint):
            result = gen_with_key.generate_article(
                topic_info={
                    "topic_id": "test-topic-1",
                    "title": "Cursor AI vs GitHub Copilot Comparison",
                    "primary_keyword": "cursor ai vs github copilot",
                    "article_type": "comparison"
                },
                canonical_url="https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html",
                allow_fallback=False
            )
            self.assertFalse(result["success"])
            self.assertFalse(result["is_gemini_generated"])
            self.assertEqual(result["status"], "GENERATION_FAILED")
            self.assertFalse(result["html_draft"])
            self.assertIn("404", result["error"])

    def test_02_fallback_article_cannot_receive_approved_status(self):
        """
        Invariant 2: A fallback heuristic article can NEVER receive APPROVED status
        under Quality Gate 5 (Originality & Value-Add).
        """
        html_fallback = self.gemini_gen.generate_heuristic_fallback(
            topic_info={
                "title": "Cursor AI vs GitHub Copilot Comparison",
                "primary_keyword": "cursor ai vs github copilot",
                "slug": "cursor-ai-vs-github-copilot-comparison",
                "article_type": "comparison"
            },
            canonical_url="https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html"
        )
        self.assertIsInstance(html_fallback, str)

        eval_result = self.gate_engine.evaluate_article(
            html_content=html_fallback,
            metadata={
                "slug": "cursor-ai-vs-github-copilot-comparison",
                "title": "Cursor AI vs GitHub Copilot Comparison",
                "primary_keyword": "cursor ai vs github copilot",
                "canonical_url": "https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html",
                "article_type": "comparison",
                "is_fallback": True,
                "generation_method": "FALLBACK_HEURISTIC",
                "is_gemini_generated": False
            }
        )
        self.assertNotEqual(eval_result["decision"], "APPROVED")
        self.assertTrue(eval_result["failed_gates_count"] > 0)
        self.assertTrue(any("GATE_05" in failure for failure in eval_result["critical_failures"]))

    def test_03_missing_registry_matches_never_create_default_prices(self):
        """
        Invariant 3: Missing registry products must never invent default prices
        (such as Rs. 4,500 or $16) and must return UNKNOWN or unverified.
        """
        context = self.gemini_gen.get_verified_product_context("completely-unknown-ai-tool-xyz-999")
        self.assertFalse(context["verified"])
        self.assertEqual(context["price_pkr"], "UNKNOWN")
        self.assertNotIn("4,500", str(context))
        self.assertNotIn("4500", str(context))

        comp_context = self.gemini_gen.get_verified_comparison_context("non-existent-tool-a vs non-existent-tool-b")
        self.assertFalse(comp_context["product_a"]["verified"])
        self.assertFalse(comp_context["product_b"]["verified"])
        self.assertEqual(comp_context["product_a"]["price_pkr"], "UNKNOWN")
        self.assertEqual(comp_context["product_b"]["price_pkr"], "UNKNOWN")

    def test_04_unverified_benchmark_claims_fail_gate_10(self):
        """
        Invariant 4: Fabricated benchmark claims (e.g. 'tested on 500 developers',
        'secret benchmark', 'measured 99.9%', 'in our hardware cluster') must fail Gate 10.
        """
        fabricated_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head><title>Fabricated Article</title></head>
        <body>
        <main>
        <h1>Cursor AI vs GitHub Copilot Comparison</h1>
        <p class="quick-answer">In our rigorous testing tested on 500 developers across Pakistan, we measured 99.9% productivity boost in our hardware cluster using a secret benchmark.</p>
        <table class="comparison-table">
          <thead><tr><th>Feature</th><th>Cursor</th><th>Copilot</th></tr></thead>
          <tbody>
            <tr><td>Speed</td><td>10x faster</td><td>Normal</td></tr>
            <tr><td>Price</td><td>Rs. 3,800</td><td>Rs. 1,500</td></tr>
            <tr><td>Guarantee</td><td>100% money-back guarantee</td><td>Standard</td></tr>
          </tbody>
        </table>
        </main>
        </body>
        </html>
        """
        eval_result = self.gate_engine.evaluate_article(
            html_content=fabricated_html,
            metadata={
                "slug": "test-fabricated-claims",
                "title": "Cursor AI vs GitHub Copilot Comparison",
                "primary_keyword": "cursor ai vs github copilot",
                "canonical_url": "https://aidigitools.tech/blog/test-fabricated-claims.html",
                "article_type": "comparison"
            }
        )
        self.assertNotEqual(eval_result["decision"], "APPROVED")
        self.assertFalse(eval_result["gate_results"]["GATE_10_NO_INVENTED_TESTS"]["passed"])
        self.assertTrue(any("GATE_10" in f for f in eval_result["critical_failures"]))

    def test_05_evidence_verification_actually_evaluates_article_claims(self):
        """
        Invariant 5: ResearchEvidenceSystem.verify_article_evidence rejects unsupported claims,
        fabricated prices (Rs. 4,500 for Cursor), or missing primary vendor links.
        """
        bad_html = """
        <html><body>
        <h1>Cursor AI vs GitHub Copilot</h1>
        <p>Tested on 500 developers. Cursor Pro is available at Rs. 4,500 PKR.</p>
        </body></html>
        """
        res_bad = self.evidence_sys.verify_article_evidence(
            html_content=bad_html,
            metadata={
                "slug": "cursor-ai-vs-github-copilot-comparison",
                "primary_keyword": "cursor ai vs github copilot",
                "title": "Cursor AI vs GitHub Copilot",
                "article_type": "comparison"
            }
        )
        self.assertFalse(res_bad["verified"])
        self.assertEqual(res_bad["status"], "EVIDENCE_UNAVAILABLE")
        self.assertTrue(len(res_bad["errors"]) > 0)
        self.assertTrue(any("4,500" in err for err in res_bad["errors"]))

    def test_06_cursor_pro_pricing_matches_registry(self):
        """
        Invariant 6: Verified pricing for Cursor Pro must be exactly Rs. 3,800 / $14.0
        and reject legacy placeholder Rs. 4,500 or fake Rs. 8,500 multi-seat.
        """
        context = self.gemini_gen.get_verified_product_context("cursor-pro")
        self.assertTrue(context["verified"])
        self.assertIn("3,800", context["price_pkr"])
        self.assertIn("14", context["price_usd"])

        # Gate 8 verification: article with Rs. 4,500 or 8,500 for Cursor must fail Gate 8
        bad_price_html = """
        <html><head><title>Cursor Pro Pricing</title></head><body>
        <h1>Cursor Pro Pakistan Price Review</h1>
        <p class="quick-answer">Cursor Pro costs Rs. 4,500 PKR while Pro Multi-Seat costs Rs. 8,500 PKR.</p>
        </body></html>
        """
        eval_result = self.gate_engine.evaluate_article(
            html_content=bad_price_html,
            metadata={
                "slug": "cursor-pro-pakistan-price-review",
                "primary_keyword": "cursor pro",
                "title": "Cursor Pro Pakistan Price Review",
                "canonical_url": "https://aidigitools.tech/blog/cursor-pro-pakistan-price-review.html"
            }
        )
        self.assertTrue(any("GATE_08" in fail for fail in eval_result["critical_failures"]))

    def test_07_comparison_article_contains_real_comparison_for_both_products(self):
        """
        Invariant 7: Comparison articles must contain real dual-entity comparison
        and at least 3 concrete comparison rows in an HTML table.
        """
        one_entity_html = """
        <html><head><title>Cursor AI vs GitHub Copilot</title></head><body>
        <h1>Cursor AI vs GitHub Copilot</h1>
        <p class="quick-answer">Cursor AI is a great tool for coding with AI in Pakistan.</p>
        <p>No table or Copilot details here.</p>
        </body></html>
        """
        eval_result = self.gate_engine.evaluate_article(
            html_content=one_entity_html,
            metadata={
                "slug": "cursor-ai-vs-github-copilot-comparison",
                "primary_keyword": "cursor ai vs github copilot",
                "title": "Cursor AI vs GitHub Copilot",
                "canonical_url": "https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html",
                "article_type": "comparison"
            }
        )
        self.assertFalse(eval_result["gate_results"]["GATE_03_SEARCH_INTENT_ACCURACY"]["passed"])
        self.assertTrue(any("GATE_03" in fail for fail in eval_result["critical_failures"]))

    def test_08_no_article_published_before_human_approval(self):
        """
        Invariant 8: Under Phase 1 Supervised Mode (0/3 threshold),
        no article can ever be published automatically to /blog/ or added to sitemap.xml.
        """
        status = self.pub_control.get_operational_status()
        self.assertEqual(status["current_phase"], PHASE_1_SUPERVISED)
        self.assertEqual(status["approved_supervised_publications_count"], 0)
        self.assertFalse(status["phase_2_unlocked"])

        # Attempting to approve non-existent preview raises KeyError; missing reviewer raises ValueError
        with self.assertRaises(ValueError):
            self.pub_control.human_approve_preview(preview_id_or_slug="any-preview", reviewer_name="", reviewer_notes="")
        with self.assertRaises(KeyError):
            self.pub_control.human_approve_preview(preview_id_or_slug="non-existent-preview", reviewer_name="Abeera Farooq", reviewer_notes="Approved")

    def test_09_preview_file_paths_persisted_as_repository_relative(self):
        """
        Invariant 9: Generated previews must persist repository-relative paths
        (e.g. data/previews/{slug}.html) across ledger and reports, avoiding machine-specific absolute paths.
        """
        preview_record = self.pub_control.prepare_article_preview(
            slug="test-relative-preview-slug",
            title="Test Relative Preview Title",
            html_content="<html><body><h1>Test Content</h1></body></html>",
            metadata={
                "canonical_url": "https://aidigitools.tech/blog/test-relative-preview-slug.html",
                "primary_keyword": "test keyword"
            },
            quality_gate_report={"decision": "NEEDS_IMPROVEMENT"}
        )
        self.assertEqual(preview_record["preview_path"], "data/previews/test-relative-preview-slug.html")
        self.assertFalse(preview_record["preview_path"].startswith("/"))
        self.assertFalse(":" in preview_record["preview_path"])  # No Windows drive letter

    def test_10_failed_generation_does_not_create_pending_approval_preview(self):
        """
        Invariant 10: When Gemini generation fails (or is mock-failed),
        execute_full_content_pipeline immediately halts with GENERATION_FAILED,
        article_generated=False, and zero previews enqueued.
        """
        mock_generator_instance = MagicMock()
        mock_generator_instance.generate_article.return_value = {
            "success": False,
            "is_gemini_generated": False,
            "status": "GENERATION_FAILED",
            "error": "HTTP 404: Model not found",
            "html_draft": None
        }

        with patch("agent.gemini_generator.GeminiArticleGenerator", return_value=mock_generator_instance):
            result = self.scheduler.execute_full_content_pipeline()
            self.assertEqual(result["pipeline_status"], "GENERATION_FAILED")
            self.assertFalse(result["article_generated"])
            self.assertFalse(result.get("preview_created", False))
            self.assertIsNone(result.get("preview_id"))

    def test_11_quick_answer_normalization_enforces_word_count_limits(self):
        """
        Invariant 11: When Gemini generates an over-length quick-answer (e.g. 150+ words),
        or under-length (< 35 words), post-processing normalizes it to strictly between
        35 and 70 words (optimal target 40-60 words), satisfying Gate 1 and check_seo_metrics.py.
        """
        gen = GeminiArticleGenerator(workspace_root=self.workspace_root)
        comp_context = gen.get_verified_comparison_context("cursor ai vs github copilot")

        # Case 1: 150-word verbose text from LLM
        verbose_text = """<!DOCTYPE html><html><head><title>Test Title That Fits Correct Length Bounds Here</title>
<meta name="description" content="In-depth guide and pricing breakdown for Cursor AI vs GitHub Copilot in Pakistan with verified details.">
</head><body><h1>Cursor AI vs GitHub Copilot</h1>
<p class="quick-answer">Cursor AI and GitHub Copilot are two premier AI-powered coding assistants designed for modern software developers, offering deep IDE integrations, automated multi-file edits, and intelligent codebase comprehension across complex repositories. Cursor provides native agentic editing and specialized background refactoring starting from Rs. 3,800 PKR per month, while GitHub Copilot offers broad multi-editor autocompletion starting from Rs. 1,500 PKR. In Pakistan, AIDigiTools provides verified workspace seats for both tools with fast 15-minute digital delivery via WhatsApp and a 30-day replacement warranty. Software engineers across Islamabad, Lahore, Karachi, and global freelance hubs require reliable access without international credit card restrictions. This in-depth comparison covers everything you need to make an informed decision for your workflow, including benchmark analysis, response latency, supported models such as Claude 3.5 Sonnet and GPT-4o, and pricing plans with complete transparency.</p>
</body></html>"""

        normalized = gen._clean_and_wrap_html(
            raw_content=verbose_text,
            primary_kw="cursor ai vs github copilot",
            canonical_url="https://aidigitools.tech/blog/cursor-ai-vs-github-copilot-comparison.html",
            comp_context=comp_context
        )

        import re
        qa_match = re.search(r'<p[^>]*class=["\']quick-answer["\'][^>]*>(.*?)</p>', normalized, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(qa_match)
        words = len(re.sub(r'<[^>]+>', ' ', qa_match.group(1)).split())
        self.assertGreaterEqual(words, 35)
        self.assertLessEqual(words, 70)

        # Gate 1 evaluation must pass on normalized output
        gate_res = self.gate_engine.evaluate_article(
            html_content=normalized,
            metadata={"slug": "cursor-ai-vs-github-copilot-comparison", "title": "Cursor AI vs GitHub Copilot"}
        )
        self.assertTrue(gate_res["gate_results"]["GATE_01_REAL_READER_PROBLEM"]["passed"])


if __name__ == "__main__":
    unittest.main()
