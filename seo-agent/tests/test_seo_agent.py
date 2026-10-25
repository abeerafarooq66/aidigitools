import unittest
import tempfile
import os
import sys
from pathlib import Path

# Add seo-agent directory to sys.path for direct imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agent.audit_engine import TechnicalAuditEngine
from agent.decision_engine import GrowthDecisionEngine
from agent.deployment_verifier import DeploymentVerifier

class TestSEOAgent(unittest.TestCase):

    def setUp(self):
        self.perfect_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>AIDigiTools — AI Software Marketplace Pakistan</title>
    <meta name="description" content="Buy premium AI tools in Pakistan with EasyPaisa, JazzCash, and SadaPay. Fast activation and 30-day warranty.">
    <link rel="canonical" href="https://aidigitools.tech/">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:title" content="AIDigiTools — AI Software Marketplace Pakistan">
    <meta property="og:description" content="Buy premium AI tools in Pakistan with EasyPaisa, JazzCash, and SadaPay.">
    <meta property="og:url" content="https://aidigitools.tech/">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="AIDigiTools — AI Tools Pakistan">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "AIDigiTools",
        "url": "https://aidigitools.tech/"
    }
    </script>
</head>
<body>
    <h1>AIDigiTools Pakistan — Premium AI Tools Marketplace</h1>
    <img src="assets/banner.webp" alt="AIDigiTools AI Marketplace Banner">
</body>
</html>"""

    # --- 10 Technical Audit Steps (1-10) ---
    def test_01_step_title_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["title"]["passed"])
            self.assertGreaterEqual(res["checks"]["title"]["length"], 30)
            self.assertLessEqual(res["checks"]["title"]["length"], 65)
        finally:
            os.remove(f_path)

    def test_02_step_meta_description_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["meta_description"]["passed"])
            self.assertGreaterEqual(res["checks"]["meta_description"]["length"], 70)
        finally:
            os.remove(f_path)

    def test_03_step_canonical_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["canonical"]["passed"])
            self.assertIn("https://aidigitools.tech", res["checks"]["canonical"]["value"])
        finally:
            os.remove(f_path)

    def test_04_step_viewport_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["viewport"]["passed"])
        finally:
            os.remove(f_path)

    def test_05_step_single_h1_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["single_h1"]["passed"])
            self.assertEqual(res["checks"]["single_h1"]["count"], 1)
        finally:
            os.remove(f_path)

    def test_06_step_opengraph_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["opengraph"]["passed"])
        finally:
            os.remove(f_path)

    def test_07_step_twitter_card_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["twitter_card"]["passed"])
        finally:
            os.remove(f_path)

    def test_08_step_json_ld_schema_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["json_ld"]["passed"])
        finally:
            os.remove(f_path)

    def test_09_step_image_alt_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["image_alt"]["passed"])
            self.assertEqual(res["checks"]["image_alt"]["missing_alt"], 0)
        finally:
            os.remove(f_path)

    def test_10_step_html_lang_valid(self):
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertTrue(res["checks"]["html_lang"]["passed"])
            self.assertEqual(res["checks"]["html_lang"]["value"], "en")
        finally:
            os.remove(f_path)

    # --- Edge Cases & Failures ---
    def test_11_multiple_h1_fails(self):
        html = self.perfect_html.replace("</body>", "<h1>Second H1</h1></body>")
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertFalse(res["checks"]["single_h1"]["passed"])
            self.assertEqual(res["checks"]["single_h1"]["count"], 2)
        finally:
            os.remove(f_path)

    def test_12_missing_alt_attribute_fails(self):
        html = self.perfect_html.replace('alt="AIDigiTools AI Marketplace Banner"', '')
        engine = TechnicalAuditEngine()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            f_path = Path(f.name)
        try:
            res = engine.audit_page(f_path)
            self.assertFalse(res["checks"]["image_alt"]["passed"])
            self.assertEqual(res["checks"]["image_alt"]["missing_alt"], 1)
        finally:
            os.remove(f_path)

    def test_13_audit_site_overall_score(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "index.html").write_text(self.perfect_html, encoding="utf-8")
            (tmppath / "robots.txt").write_text("User-agent: *\nAllow: /", encoding="utf-8")
            (tmppath / "sitemap.xml").write_text("<urlset></urlset>", encoding="utf-8")

            engine = TechnicalAuditEngine(root_dir=tmpdir)
            site_rep = engine.audit_site()
            self.assertEqual(site_rep["pages_scanned"], 1)
            self.assertEqual(site_rep["average_seo_score"], 100.0)
            self.assertTrue(site_rep["all_passed"])

    def test_14_decision_engine_proposes_fixes(self):
        decision = GrowthDecisionEngine()
        dummy_audit = {
            "robots_txt_exists": False,
            "sitemap_xml_exists": False,
            "results": [
                {
                    "file": "test.html",
                    "checks": {
                        "single_h1": {"passed": False, "count": 0},
                        "title": {"passed": False, "length": 15},
                        "meta_description": {"passed": False, "length": 30},
                        "canonical": {"passed": False}
                    }
                }
            ]
        }
        proposals = decision.evaluate_audit(dummy_audit)
        self.assertEqual(len(proposals), 6)
        p0_types = [p["type"] for p in proposals if p["priority"] == "P0"]
        self.assertIn("CRITICAL_FIX", p0_types)
        self.assertIn("HEADING_HIERARCHY_FIX", p0_types)
        self.assertIn("CANONICAL_FIX", p0_types)

    def test_15_deployment_verifier_local_file(self):
        verifier = DeploymentVerifier()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.perfect_html)
            f_path = Path(f.name)
        try:
            res = verifier.verify_local_file(f_path)
            self.assertEqual(res["status"], 200)
            self.assertTrue(res["valid"])
        finally:
            os.remove(f_path)

    def test_16_deployment_verifier_missing_file(self):
        verifier = DeploymentVerifier()
        res = verifier.verify_local_file("non_existent_file.html")
        self.assertEqual(res["status"], 404)
        self.assertFalse(res["valid"])

if __name__ == "__main__":
    unittest.main()
