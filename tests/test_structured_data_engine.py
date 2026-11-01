"""
Unit tests for Structured Data Engine (Section 13 of Master Architecture Charter).
"""

import unittest
import sys
import json
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.structured_data_engine import StructuredDataEngine

ROOT_DIR = Path(__file__).resolve().parent.parent

class TestStructuredDataEngine(unittest.TestCase):
    def setUp(self):
        self.engine = StructuredDataEngine()

    def test_generate_article_schema_valid_and_invalid_author(self):
        """Article schema generation requires verified author from author_registry.json."""
        # Valid author
        schema = self.engine.generate_article_schema(
            headline="Cursor vs Copilot Benchmark 2026",
            description="Comparing AI coding tools in Pakistan.",
            author_id="abeera-farooq",
            image_url="https://aidigitools.tech/assets/images/cursor-pro.png",
            date_published="2026-10-15T00:00:00+05:00",
            date_modified="2026-11-01T00:00:00+05:00",
            article_url="https://aidigitools.tech/compare/cursor-vs-copilot.html"
        )
        self.assertEqual(schema["@type"], "TechArticle")
        self.assertEqual(schema["author"]["name"], "Abeera Farooq")
        self.assertEqual(schema["publisher"]["name"], "AIDigiTools")

        # Invalid author
        with self.assertRaises(ValueError):
            self.engine.generate_article_schema(
                headline="Test",
                description="Test",
                author_id="fake-unregistered-author",
                image_url="https://aidigitools.tech/img.png",
                date_published="2026-10-15T00:00:00+05:00",
                date_modified="2026-11-01T00:00:00+05:00",
                article_url="https://aidigitools.tech/test.html"
            )

    def test_generate_article_schema_date_invariants(self):
        """dateModified cannot precede datePublished."""
        with self.assertRaises(ValueError):
            self.engine.generate_article_schema(
                headline="Test",
                description="Test",
                author_id="abeera-farooq",
                image_url="https://aidigitools.tech/img.png",
                date_published="2026-11-01T00:00:00+05:00",
                date_modified="2026-10-01T00:00:00+05:00",  # earlier than published
                article_url="https://aidigitools.tech/test.html"
            )

    def test_prohibited_aggregaterating_rejection(self):
        """AggregateRating is strictly forbidden and must fail validation."""
        fake_rating_json = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "ChatGPT Plus",
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.9",
                "reviewCount": "500"
            },
            "offers": {"@type": "Offer", "price": "2300"}
        }
        html = f'<script type="application/ld+json">{json.dumps(fake_rating_json)}</script>'
        res = self.engine.validate_html_structured_data(html, page_type="tool")
        self.assertFalse(res["passed"])
        self.assertTrue(any("Fabrication Violation" in e for e in res["errors"]))

    def test_prohibited_product_schema_on_non_product_pages(self):
        """Product schema must never be applied to generic categories or guide articles."""
        category_with_product_schema = """
        <script type="application/ld+json">
        {"@context": "https://schema.org", "@type": "Product", "name": "Best AI Tools"}
        </script>
        """
        res = self.engine.validate_html_structured_data(category_with_product_schema, page_type="category")
        self.assertFalse(res["passed"])
        self.assertTrue(any("Schema Ineligibility" in e for e in res["errors"]))

    def test_real_catalog_tool_pages_validation(self):
        """Verify real tool pages pass structured data validation with 0 errors."""
        sample_tools = ["tools/cursor-pro.html", "tools/chatgpt-plus.html", "tools/claude-pro.html"]
        for rel in sample_tools:
            path = ROOT_DIR / rel
            self.assertTrue(path.exists(), f"Missing {rel}")
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            res = self.engine.validate_html_structured_data(html, page_type="tool", canonical_url=f"https://aidigitools.tech/{rel}")
            self.assertTrue(res["passed"], f"Tool page {rel} failed schema validation: {res['errors']}")
            self.assertIn("Product", res["types_found"])

    def test_real_guide_and_comparison_pages_validation(self):
        """Verify real guide/comparison pages use Article/TechArticle schema without Product schema."""
        sample_articles = ["compare/chatgpt-vs-claude.html", "guides/chatgpt-vs-claude.html"]
        for rel in sample_articles:
            path = ROOT_DIR / rel
            self.assertTrue(path.exists(), f"Missing {rel}")
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            res = self.engine.validate_html_structured_data(html, page_type="article", canonical_url=f"https://aidigitools.tech/{rel}")
            self.assertTrue(res["passed"], f"Article page {rel} failed schema validation: {res['errors']}")
            self.assertNotIn("Product", res["types_found"])

if __name__ == "__main__":
    unittest.main()

