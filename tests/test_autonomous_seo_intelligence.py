"""
AIDigiTools — Comprehensive Unit & Regression Test Battery for Autonomous SEO Intelligence.
==========================================================================================
Tests the following core engines:
1. PageDiscoveryEngine (Dynamic real page discovery, link graph, orphan detection, sitemap reconciliation)
2. CoreWebVitalsEngine (PageSpeed Insights v5 API parsing, CrUX field data, local invariant audits & healing)
3. DiagnosisEngine (Multi-tier root-cause analysis, risk/benefit evaluation, confidence scoring)
4. TechnicalKnowledgeBase (Authoritative knowledge registry validation)
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Workspace root setup
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SEO_AGENT_DIR = WORKSPACE_ROOT / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from agent.page_discovery_engine import PageDiscoveryEngine
from agent.core_web_vitals_engine import CoreWebVitalsEngine, CWV_THRESHOLDS
from agent.diagnosis_engine import DiagnosisEngine


class TestAutonomousSEOIntelligence(unittest.TestCase):

    def setUp(self):
        self.workspace_root = WORKSPACE_ROOT
        self.discovery_engine = PageDiscoveryEngine(self.workspace_root)
        self.cwv_engine = CoreWebVitalsEngine(self.workspace_root)
        self.diagnosis_engine = DiagnosisEngine(self.workspace_root)

    # =========================================================================
    # 1. PAGE DISCOVERY ENGINE TESTS
    # =========================================================================

    def test_01_discovery_finds_all_production_html_pages(self):
        """Verifies dynamic page discovery identifies user-facing HTML files and ignores excluded dirs."""
        files = self.discovery_engine.discover_local_html_files()
        self.assertGreaterEqual(len(files), 50, "Discovery must find at least 50 production HTML files")
        # Ensure no test or venv files are included
        for f in files:
            parts = f.parts
            self.assertNotIn(".venv", parts)
            self.assertNotIn("tests", parts)
            self.assertNotIn(".git", parts)

    def test_02_stable_id_is_deterministic_and_unique(self):
        """Verifies stable IDs are generated deterministically from canonical URLs."""
        url_a = "https://aidigitools.tech/about.html"
        url_b = "https://aidigitools.tech/contact.html"

        id_a1 = self.discovery_engine.generate_stable_id(url_a)
        id_a2 = self.discovery_engine.generate_stable_id(url_a)
        id_b = self.discovery_engine.generate_stable_id(url_b)

        self.assertEqual(id_a1, id_a2, "Identical URLs must yield identical stable IDs")
        self.assertNotEqual(id_a1, id_b, "Distinct URLs must yield distinct stable IDs")
        self.assertTrue(id_a1.startswith("PAGE-"))

    def test_03_discovery_reconciles_sitemap_and_zero_orphans(self):
        """Verifies full discovery runs cleanly with 0 orphan pages on current production site."""
        report = self.discovery_engine.run_full_discovery()
        self.assertEqual(report["status"], "SUCCESS")
        self.assertEqual(report["anomalies"]["orphan_pages_count"], 0, "Production site must have zero orphan pages")
        self.assertEqual(len(report["anomalies"]["duplicate_canonicals"]), 0, "Production site must have zero duplicate canonicals")
        self.assertEqual(len(report["anomalies"]["missing_sitemap_entries"]), 0, "Sitemap must match all production pages")

    def test_04_discovery_detects_mock_orphan_and_duplicate_canonical(self):
        """Verifies discovery engine correctly flags orphan pages and duplicate canonicals when present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # Create two pages that point to the exact same canonical
            p1 = tmppath / "page1.html"
            p2 = tmppath / "page2.html"
            orphan = tmppath / "orphan.html"

            p1.write_text('<link rel="canonical" href="https://aidigitools.tech/shared.html"><a href="page2.html">link</a>', encoding="utf-8")
            p2.write_text('<link rel="canonical" href="https://aidigitools.tech/shared.html">', encoding="utf-8")
            orphan.write_text('<link rel="canonical" href="https://aidigitools.tech/orphan.html">', encoding="utf-8")

            # Create dummy sitemap
            sm = tmppath / "sitemap.xml"
            sm.write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://aidigitools.tech/shared.html</loc></url></urlset>', encoding="utf-8")

            test_engine = PageDiscoveryEngine(tmppath)
            res = test_engine.run_full_discovery()

            self.assertEqual(len(res["anomalies"]["duplicate_canonicals"]), 1)
            self.assertIn("orphan.html", res["anomalies"]["orphan_pages"])
            self.assertIn("https://aidigitools.tech/orphan.html", res["anomalies"]["missing_sitemap_entries"])

    # =========================================================================
    # 2. CORE WEB VITALS & PAGESPEED ENGINE TESTS
    # =========================================================================

    def test_05_cwv_api_configuration_truthfulness(self):
        """Verifies CWV engine truthfully reports when API key is missing or present."""
        unconfigured = CoreWebVitalsEngine(self.workspace_root, api_key="")
        self.assertFalse(unconfigured.is_api_configured())

        configured = CoreWebVitalsEngine(self.workspace_root, api_key="AIzaSyD-FakeKeyForTesting1234567")
        self.assertTrue(configured.is_api_configured())

    def test_06_cwv_parses_lighthouse_and_crux_payload(self):
        """Verifies parser extracts lab metrics, scores, LCP elements, and CrUX field data."""
        mock_raw = {
            "lighthouseResult": {
                "categories": {
                    "performance": {"score": 0.95},
                    "accessibility": {"score": 1.0},
                    "best-practices": {"score": 1.0},
                    "seo": {"score": 1.0}
                },
                "audits": {
                    "first-contentful-paint": {"displayValue": "1.2 s"},
                    "largest-contentful-paint": {"displayValue": "1.8 s"},
                    "total-blocking-time": {"displayValue": "0 ms"},
                    "cumulative-layout-shift": {"displayValue": "0.01"},
                    "speed-index": {"displayValue": "1.5 s"},
                    "largest-contentful-paint-element": {
                        "details": {"items": [{"node": {"snippet": "<p class=\"quick-answer\">..."}}]}
                    },
                    "render-blocking-resources": {
                        "details": {"items": []}
                    },
                    "non-composited-animations": {
                        "details": {"items": []}
                    },
                    "color-contrast": {
                        "details": {"items": []}
                    },
                    "dom-size": {"displayValue": "250 elements"}
                }
            },
            "loadingExperience": {
                "overall_category": "FAST",
                "metrics": {
                    "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 2100},
                    "INTERACTION_TO_NEXT_PAINT": {"percentile": 85},
                    "CUMULATIVE_LAYOUT_SHIFT_SCORE": {"percentile": 0.02}
                }
            },
            "originLoadingExperience": {
                "overall_category": "FAST",
                "metrics": {
                    "LARGEST_CONTENTFUL_PAINT_MS": {"percentile": 2200}
                }
            }
        }

        parsed = self.cwv_engine._parse_pagespeed_response(mock_raw, "https://aidigitools.tech/", "mobile")
        self.assertTrue(parsed["success"])
        self.assertEqual(parsed["scores"]["performance"], 95)
        self.assertEqual(parsed["scores"]["accessibility"], 100)
        self.assertEqual(parsed["lab_metrics"]["largest_contentful_paint"], "1.8 s")
        self.assertEqual(parsed["diagnostics"]["lcp_element_snippet"], "<p class=\"quick-answer\">...")
        self.assertTrue(parsed["field_experience"]["url_crux"]["has_data"])
        self.assertEqual(parsed["field_experience"]["url_crux"]["lcp"], 2100)

    def test_07_local_pagespeed_invariants_pass_on_production_codebase(self):
        """Verifies local PageSpeed invariants pass cleanly on the current production codebase."""
        res = self.cwv_engine.audit_local_pagespeed_invariants()
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["total_issues"], 0, "Zero render-blocking scripts or low-contrast buttons on production codebase")

    def test_08_local_pagespeed_invariants_detects_and_heals_mock_issues(self):
        """Verifies local invariant checker catches render-blocking script and low contrast, and heals them."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            assets_dir = tmppath / "assets"
            assets_dir.mkdir()

            # HTML with un-deferred cart.js
            bad_html = tmppath / "test.html"
            bad_html.write_text('<html><body><script src="assets/cart.js?v=2.5"></script></body></html>', encoding="utf-8")

            # CSS with low-contrast button
            bad_css = assets_dir / "style.css"
            bad_css.write_text('.btn-whatsapp { background: #10B981; color: #FFFFFF; }', encoding="utf-8")

            test_cwv = CoreWebVitalsEngine(tmppath)
            audit_res = test_cwv.audit_local_pagespeed_invariants()
            self.assertEqual(audit_res["status"], "FAIL")
            self.assertEqual(audit_res["total_issues"], 2)

            # Execute healing
            heal_res = test_cwv.heal_pagespeed_issues()
            self.assertEqual(heal_res["status"], "HEALED")
            self.assertEqual(heal_res["total_files_repaired"], 2)

            # Verify healed files pass invariants
            post_audit = test_cwv.audit_local_pagespeed_invariants()
            self.assertEqual(post_audit["status"], "PASS")
            self.assertEqual(post_audit["total_issues"], 0)

    # =========================================================================
    # 3. DIAGNOSIS ENGINE TESTS
    # =========================================================================

    def test_09_diagnosis_engine_prioritizes_issues_by_severity(self):
        """Verifies DiagnosisEngine ranks issues: CRITICAL > HIGH > MEDIUM > LOW."""
        mock_discovery = {
            "anomalies": {
                "orphan_pages": ["blog/orphan-article.html"],
                "duplicate_canonicals": [{"canonical_url": "https://aidigitools.tech/test", "competing_files": ["a.html", "b.html"]}],
                "missing_sitemap_entries": ["https://aidigitools.tech/missing.html"]
            }
        }
        mock_cwv = {
            "issues": [
                {
                    "file": "test.html",
                    "type": "RENDER_BLOCKING_SCRIPT",
                    "severity": "HIGH",
                    "message": "Script lacks defer"
                }
            ]
        }
        mock_gsc = {
            "opportunities": [
                {
                    "query": "cursor ai vs copilot",
                    "page": "https://aidigitools.tech/compare/cursor-vs-copilot.html",
                    "impressions": 120,
                    "clicks": 1,
                    "ctr": 0.8,
                    "position": 8.5
                }
            ]
        }

        diag = self.diagnosis_engine.diagnose_all_systems(
            discovery_report=mock_discovery,
            cwv_local_report=mock_cwv,
            gsc_report=mock_gsc
        )

        self.assertEqual(diag["status"], "ACTION_REQUIRED")
        self.assertGreater(diag["summary"]["total_diagnosed_issues"], 0)
        issues = diag["issues"]
        # Verify first issue is HIGH (since no CRITICAL in mock)
        self.assertEqual(issues[0]["severity"], "HIGH")
        # Verify GSC issue has proposed solution and confidence score
        gsc_issues = [i for i in issues if i["category"] == "SEARCH_INTELLIGENCE"]
        self.assertEqual(len(gsc_issues), 1)
        self.assertEqual(gsc_issues[0]["confidence_score"], 90)
        self.assertTrue(gsc_issues[0]["proposed_solutions"][0]["recommended"])

    # =========================================================================
    # 4. TECHNICAL KNOWLEDGE BASE INTEGRITY
    # =========================================================================

    def test_10_technical_knowledge_base_exists_and_contains_core_sections(self):
        """Verifies docs/seo-agent/technical-knowledge-base.md exists with all required sections."""
        kb_path = self.workspace_root / "docs" / "seo-agent" / "technical-knowledge-base.md"
        self.assertTrue(kb_path.exists(), "Technical Knowledge Base must exist on disk")

        content = kb_path.read_text(encoding="utf-8")
        self.assertIn("System Architecture Map", content)
        self.assertIn("Core Modules, Responsibilities & Failure Handling", content)
        self.assertIn("Structured Technical Knowledge Registry", content)
        self.assertIn("Engineering Standards & Release Verification Checklist", content)
        self.assertIn("Render-Blocking Resources", content)
        self.assertIn("Color Contrast Inadequacy", content)
        self.assertIn("Non-Composited Animations", content)


if __name__ == "__main__":
    unittest.main()
