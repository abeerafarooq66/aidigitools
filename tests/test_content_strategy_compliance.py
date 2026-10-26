import os
import re
import unittest
import glob

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestContentStrategyCompliance(unittest.TestCase):
    """
    Automated compliance suite for Phase 12 - Content Strategy & Editorial Review.
    Validates content planning, quality guardrails, word counts, FAQ limits,
    disclosures, and anti-spam standards across all editorial and repository assets.
    """

    def setUp(self):
        self.strategy_doc_path = os.path.join(REPO_ROOT, "docs", "CONTENT_STRATEGY.md")
        self.editorial_pages = [
            os.path.join(REPO_ROOT, "compare", "chatgpt-vs-claude.html"),
            os.path.join(REPO_ROOT, "compare", "runway-vs-pika.html"),
            os.path.join(REPO_ROOT, "best", "best-ai-coding-tools.html"),
            os.path.join(REPO_ROOT, "best", "best-ai-video-generators.html"),
            os.path.join(REPO_ROOT, "guides", "chatgpt-vs-claude.html"),
        ]

    def test_01_editorial_content_strategy_document_exists(self):
        """Verify docs/CONTENT_STRATEGY.md exists and covers all required themes and criteria."""
        self.assertTrue(os.path.exists(self.strategy_doc_path), "docs/CONTENT_STRATEGY.md must exist in the repo.")
        with open(self.strategy_doc_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for 8 editorial themes
        required_themes = [
            "AI Tool Comparisons",
            "Use-Case Guides",
            "Tool Alternatives",
            "Beginner Tutorials",
            "Feature Explanations",
            "Pricing and Plan Comparisons",
            "Responsible Buying and Account-Safety",
            "Updates When Products or Offers Genuinely Change"
        ]
        for theme in required_themes:
            self.assertIn(theme.lower(), content.lower(), f"Theme '{theme}' must be defined in CONTENT_STRATEGY.md")

        # Check for 6 mandatory dimensions
        required_criteria = [
            "Audience",
            "Search Intent",
            "Factual Sources",
            "Original Contribution",
            "Internal Links",
            "Review Requirements"
        ]
        for criteria in required_criteria:
            self.assertIn(criteria.lower(), content.lower(), f"Dimension '{criteria}' must be defined in CONTENT_STRATEGY.md")

        # Check for 4 review pillars
        review_pillars = [
            "Factual Accuracy",
            "Product Eligibility",
            "Licensing",
            "Pricing"
        ]
        for pillar in review_pillars:
            self.assertIn(pillar.lower(), content.lower(), f"Review pillar '{pillar}' must be defined in CONTENT_STRATEGY.md")

    def test_02_existing_editorial_pages_meet_word_count_standard(self):
        """Verify all existing editorial pages meet the anti-thin content minimum (>= 1,500 words)."""
        for page_path in self.editorial_pages:
            self.assertTrue(os.path.exists(page_path), f"Editorial page {page_path} must exist.")
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read()
                words = len(html.split())
                self.assertGreaterEqual(
                    words, 1500,
                    f"Editorial page {os.path.basename(page_path)} has {words} words, must be >= 1,500 words to prevent thin content."
                )

    def test_03_existing_editorial_pages_faq_guardrail(self):
        """Verify editorial pages do not have excessive FAQs (maximum 5 FAQs allowed per page)."""
        for page_path in self.editorial_pages:
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read()
                faq_details = len(re.findall(r"<details", html))
                faq_classes = len(re.findall(r'class="[^"]*faq-item', html))
                faqs = max(faq_details, faq_classes)
                self.assertLessEqual(
                    faqs, 5,
                    f"Editorial page {os.path.basename(page_path)} has {faqs} FAQs. Max allowed is 5 to prevent excessive filler FAQs."
                )

    def test_04_editorial_pages_pkr_pricing_transparency(self):
        """Verify editorial pages visibly state pricing in Pakistani Rupees (PKR)."""
        for page_path in self.editorial_pages:
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read()
                has_pkr = "PKR" in html or "Rs." in html
                self.assertTrue(
                    has_pkr,
                    f"Editorial page {os.path.basename(page_path)} must include transparent PKR pricing."
                )

    def test_05_editorial_pages_licensing_and_access_disclosures(self):
        """Verify editorial pages include clear licensing/access model disclosures (shared workspace vs private seat)."""
        for page_path in self.editorial_pages:
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read().lower()
                has_disclosure = "shared" in html or "workspace" in html or "reseller" in html or "account" in html
                self.assertTrue(
                    has_disclosure,
                    f"Editorial page {os.path.basename(page_path)} must disclose account access model or reseller status."
                )

    def test_06_editorial_pages_no_unsupported_exaggerated_claims(self):
        """Verify editorial pages contain zero unsupported hyperbolic marketing claims."""
        banned_phrases = [
            "100% bug-free",
            "100% bug free",
            "100% error-free",
            "100% error free",
            "magic ai",
            "magical results",
            "replace all developers",
            "replace all humans",
            "guaranteed wealth",
            "instant millionaire"
        ]
        for page_path in self.editorial_pages:
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read().lower()
                for phrase in banned_phrases:
                    self.assertNotIn(
                        phrase, html,
                        f"Editorial page {os.path.basename(page_path)} contains banned unsupported claim '{phrase}'."
                    )

    def test_07_editorial_pages_have_citations_and_canonical_links(self):
        """Verify editorial pages include canonical links, internal catalog links, and schema markup."""
        for page_path in self.editorial_pages:
            with open(page_path, "r", encoding="utf-8") as f:
                html = f.read()
                # Check canonical link
                self.assertIn('<link rel="canonical"', html, f"{os.path.basename(page_path)} must have a canonical tag.")
                # Check schema
                self.assertIn('application/ld+json', html, f"{os.path.basename(page_path)} must have JSON-LD structured data.")
                # Check internal links to catalog tools
                self.assertTrue(
                    'href="../tools/' in html or 'href="tools/' in html or 'href="/tools/' in html,
                    f"{os.path.basename(page_path)} must link internally to catalog tools."
                )

    def test_08_no_programmatic_doorway_keyword_pages(self):
        """Verify repository contains zero city-stuffed programmatic doorway pages."""
        all_html_files = glob.glob(os.path.join(REPO_ROOT, "**", "*.html"), recursive=True)
        city_keywords = ["lahore", "karachi", "islamabad", "rawalpindi", "faisalabad", "peshawar", "multan"]
        
        for file_path in all_html_files:
            filename = os.path.basename(file_path).lower()
            for city in city_keywords:
                self.assertNotIn(
                    city, filename,
                    f"Doorway page detected: {file_path} contains city keyword '{city}'."
                )

if __name__ == "__main__":
    unittest.main()
