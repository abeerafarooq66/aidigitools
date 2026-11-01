"""
Unit tests for Article Quality and Structure Engine and Section 8 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.article_quality_engine import ArticleQualityEngine

class TestArticleQuality(unittest.TestCase):
    def setUp(self):
        self.engine = ArticleQualityEngine()
        self.valid_html = """<!DOCTYPE html>
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

    def test_01_valid_article_passes_clean(self):
        """Verify full valid article passes with grade A+."""
        res = self.engine.evaluate_article_html(
            self.valid_html,
            "cursor-ai-vs-github-copilot",
            "cursor ai vs github copilot"
        )
        self.assertTrue(res["overall_valid"])
        self.assertEqual(len(res["errors"]), 0)
        self.assertIn(res["quality_grade"], ["A", "A+"])

    def test_02_heading_invariants_strictly_enforced(self):
        """Verify missing H1 or multiple H1s are caught."""
        # Multiple H1s
        bad_h1 = self.valid_html.replace("<h2>Key Architectural Differences</h2>", "<h1>Key Architectural Differences</h1>")
        res = self.engine.evaluate_article_html(bad_h1, "cursor-ai-vs-github-copilot", "cursor ai")
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("Heading violation" in e for e in res["errors"]))

    def test_03_quick_answer_word_count_guard(self):
        """Verify quick answer capsule must be between 35 and 70 words."""
        # Too short (10 words)
        bad_qa = self.valid_html.replace(
            'class="quick-answer">Cursor AI and GitHub Copilot are industry-leading AI coding assistants. While Copilot provides fast inline code completions as an extension for existing IDEs, Cursor is a dedicated VS Code fork with Composer for multi-file agentic editing. In Pakistan, AIDigiTools provides local PKR settlement for both tools with 15-minute delivery and a 30-day warranty.',
            'class="quick-answer">Cursor and Copilot are AI tools. Buy them today in Pakistan.'
        )
        res = self.engine.evaluate_article_html(bad_qa, "cursor-ai-vs-github-copilot", "cursor ai")
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("AEO Quick Answer capsule invalid" in e for e in res["errors"]))

    def test_04_comparison_table_enforced(self):
        """Verify missing comparison table triggers failure."""
        no_table = self.valid_html.replace("<table>", "<!--").replace("</table>", "-->")
        res = self.engine.evaluate_article_html(no_table, "cursor-ai-vs-github-copilot", "cursor ai")
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("Comparison table missing" in e for e in res["errors"]))

    def test_05_reseller_disclosure_enforced(self):
        """Verify missing independent reseller disclosure triggers failure."""
        no_reseller = self.valid_html.replace("AIDigiTools is an independent reseller and digital service desk.", "")
        res = self.engine.evaluate_article_html(no_reseller, "cursor-ai-vs-github-copilot", "cursor ai")
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("Independent Reseller Disclosure" in e for e in res["errors"]))

if __name__ == "__main__":
    unittest.main()

