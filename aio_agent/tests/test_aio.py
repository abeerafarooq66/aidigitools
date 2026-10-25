import unittest
import tempfile
import os
from pathlib import Path
from aio_agent.extractability import ExtractabilityAuditor
from aio_agent.query_fanout import QueryFanoutAuditor
from aio_agent.grounding_scorer import GroundingScorer
from aio_agent.llms_sync import LLMsSync

class TestAIOAgent(unittest.TestCase):

    def setUp(self):
        self.sample_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>ChatGPT Plus Pakistan | AIDigiTools</title>
    <meta name="description" content="Buy ChatGPT Plus in Pakistan with EasyPaisa, JazzCash, and SadaPay.">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "ChatGPT Plus Subscription",
        "offers": {
            "@type": "Offer",
            "price": "2300",
            "priceCurrency": "PKR"
        }
    }
    </script>
</head>
<body>
    <h1>ChatGPT Plus Pakistan Subscription & Pricing</h1>
    <p class="quick-answer">
        ChatGPT Plus in Pakistan costs Rs. 2,300 per month via AIDigiTools. You can pay instantly using EasyPaisa, JazzCash, SadaPay, or Raast without requiring an international credit card. Delivery takes just 15 minutes via direct WhatsApp support, accompanied by a 30-day replacement warranty for students, developers, and freelancers.
    </p>
    <div class="content">
        <h2>Features</h2>
        <p>Full access to GPT-4o, DALL-E, advanced voice mode, and custom GPTs.</p>
    </div>
</body>
</html>"""

    def test_01_extractability_single_h1_and_word_count(self):
        auditor = ExtractabilityAuditor(min_words=35, max_words=70)
        res = auditor.audit_content(self.sample_html)
        self.assertTrue(res["has_single_h1"])
        self.assertEqual(res["h1_text"], "ChatGPT Plus Pakistan Subscription & Pricing")
        self.assertTrue(res["is_valid_length"], f"Word count was {res['word_count']}")
        self.assertTrue(res["passed"])

    def test_02_query_fanout_5_branches(self):
        auditor = QueryFanoutAuditor()
        res = auditor.audit_content(self.sample_html)
        self.assertEqual(res["matched_branches"], 5)
        self.assertEqual(res["fanout_score"], 100.0)
        self.assertTrue(res["branches"]["pricing_pkr"])
        self.assertTrue(res["branches"]["local_payments"])
        self.assertTrue(res["branches"]["delivery_sla"])
        self.assertTrue(res["branches"]["warranty_support"])
        self.assertTrue(res["branches"]["target_audience"])

    def test_03_grounding_scorer_composite(self):
        scorer = GroundingScorer()
        with tempfile.NamedTemporaryFile("w+", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(self.sample_html)
            f_path = f.name

        try:
            res = scorer.score_file(f_path)
            self.assertGreaterEqual(res["grounding_score"], 80.0)
            self.assertEqual(res["status"], "PASS")
            self.assertIn("Product", res["structured_data"]["types_found"])
        finally:
            os.remove(f_path)

    def test_04_extractability_flags_invalid_word_count(self):
        invalid_html = "<h1>Short Title</h1><p class='quick-answer'>Too short.</p>"
        auditor = ExtractabilityAuditor(min_words=35, max_words=70)
        res = auditor.audit_content(invalid_html)
        self.assertFalse(res["is_valid_length"])
        self.assertFalse(res["passed"])

    def test_05_llms_sync_generates_markdown(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            tools_dir = tmppath / "tools"
            tools_dir.mkdir()
            (tools_dir / "chatgpt.html").write_text(self.sample_html, encoding="utf-8")

            syncer = LLMsSync(root_dir=tmpdir)
            sync_res = syncer.sync()

            self.assertEqual(sync_res["status"], "SUCCESS")
            llms_content = (tmppath / "llms.txt").read_text(encoding="utf-8")
            self.assertIn("AIDigiTools", llms_content)
            self.assertIn("ChatGPT Plus", llms_content)
            self.assertIn("Rs. 2,300", llms_content)

if __name__ == "__main__":
    unittest.main()
