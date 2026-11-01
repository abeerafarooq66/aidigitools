"""
Unit tests for Product Review & Comparison Methodology Engine and Section 9 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.comparison_methodology import ComparisonMethodologyEngine

class TestComparisonMethodology(unittest.TestCase):
    def setUp(self):
        self.engine = ComparisonMethodologyEngine()
        self.valid_html = """<!DOCTYPE html>
<html lang="en">
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

    def test_01_valid_comparison_passes_clean(self):
        """Verify full valid comparison passes Section 9 methodology checks."""
        res = self.engine.evaluate_review_or_comparison_html(self.valid_html)
        self.assertTrue(res["overall_valid"])
        self.assertEqual(len(res["errors"]), 0)
        self.assertEqual(res["methodology_status"], "APPROVED")

    def test_02_evaluation_criteria_enforced(self):
        """Verify missing evaluation criteria triggers rejection."""
        bad_html = self.valid_html.replace("<h2>Evaluation Criteria</h2>", "<h2>Overview</h2>")
        bad_html = bad_html.replace("four core criteria", "four things")
        res = self.engine.evaluate_review_or_comparison_html(bad_html)
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("evaluation criteria missing" in e.lower() for e in res["errors"]))

    def test_03_who_should_and_who_should_not_enforced(self):
        """Verify unbiased 'Who should / Who should not choose' matrix is required."""
        bad_html = self.valid_html.replace("Avoid this if (Who should not choose Cursor):", "Cursor is always great for everyone:")
        res = self.engine.evaluate_review_or_comparison_html(bad_html)
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("unbiased audience matrix missing" in e.lower() for e in res["errors"]))

    def test_04_methodology_evidence_badge_enforced(self):
        """Verify article must declare its evidence badge (Research-based or Hands-on tested)."""
        bad_html = self.valid_html.replace("Methodology: Research-based independent analysis", "")
        res = self.engine.evaluate_review_or_comparison_html(bad_html)
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("evidence badge" in e.lower() for e in res["errors"]))

    def test_05_anti_manufactured_hype_firewall(self):
        """Verify artificial hype and manufactured winner claims are rejected."""
        hype_html = self.valid_html + "<p>Cursor is the undisputed number 1 in the world and crushes all competition effortlessly!</p>"
        res = self.engine.evaluate_review_or_comparison_html(hype_html)
        self.assertFalse(res["overall_valid"])
        self.assertTrue(any("manufactured promotional hype" in e.lower() for e in res["errors"]))

if __name__ == "__main__":
    unittest.main()
