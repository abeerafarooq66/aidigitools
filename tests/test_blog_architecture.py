"""
Unit tests for Blog Website Architecture Engine (Section 14 of Master Architecture Charter).
"""

import unittest
import sys
import json
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.blog_architecture import BlogArchitectureEngine

ROOT_DIR = Path(__file__).resolve().parent.parent

class TestBlogArchitecture(unittest.TestCase):
    def setUp(self):
        self.engine = BlogArchitectureEngine()

    def test_clean_evergreen_urls_enforcement(self):
        """Enforce clean evergreen URLs and reject date-stamped or messy URLs."""
        # Clean evergreen URL
        valid_url = "https://aidigitools.tech/compare/chatgpt-vs-claude.html"
        ok, viols = self.engine.validate_article_url(valid_url)
        self.assertTrue(ok)
        self.assertEqual(len(viols), 0)

        # Date-stamped URL
        date_url = "https://aidigitools.tech/2026/11/01/chatgpt-vs-claude/"
        bad_ok, bad_viols = self.engine.validate_article_url(date_url)
        self.assertFalse(bad_ok)
        self.assertTrue(any("date-based" in v for v in bad_viols))

        # Uppercase in URL
        upper_url = "https://aidigitools.tech/compare/ChatGPT-vs-Claude.html"
        up_ok, up_viols = self.engine.validate_article_url(upper_url)
        self.assertFalse(up_ok)
        self.assertTrue(any("lowercase" in v for v in up_viols))

        # Query parameter in URL
        query_url = "https://aidigitools.tech/compare/chatgpt-vs-claude.html?ref=twitter"
        q_ok, q_viols = self.engine.validate_article_url(query_url)
        self.assertFalse(q_ok)
        self.assertTrue(any("query parameters" in v for v in q_viols))

    def test_thin_tag_pages_prohibited(self):
        """Thin tag, archive, and duplicate pagination URLs must be rejected."""
        prohibited_urls = [
            "https://aidigitools.tech/tags/ai-video/",
            "https://aidigitools.tech/tag/chatgpt/",
            "https://aidigitools.tech/archives/2026/",
            "https://aidigitools.tech/date/2026/10/"
        ]
        for url in prohibited_urls:
            ok, viols = self.engine.validate_article_url(url)
            self.assertFalse(ok, f"Thin tag URL '{url}' was not rejected")
            self.assertTrue(any("thin tag" in v for v in viols))

    def test_breadcrumb_hierarchy_validation(self):
        """Breadcrumbs must begin with Home, have at least 2 levels, and valid names/URLs."""
        valid_breadcrumbs = [
            {"name": "Home", "url": "https://aidigitools.tech/"},
            {"name": "Comparisons", "url": "https://aidigitools.tech/#products"},
            {"name": "ChatGPT vs Claude", "url": "https://aidigitools.tech/compare/chatgpt-vs-claude.html"}
        ]
        ok, viols = self.engine.validate_breadcrumbs(valid_breadcrumbs)
        self.assertTrue(ok)
        self.assertEqual(len(viols), 0)

        # Missing Home root
        no_home = [
            {"name": "Comparisons", "url": "https://aidigitools.tech/#products"},
            {"name": "ChatGPT vs Claude", "url": "https://aidigitools.tech/compare/chatgpt-vs-claude.html"}
        ]
        bad_ok, bad_viols = self.engine.validate_breadcrumbs(no_home)
        self.assertFalse(bad_ok)
        self.assertTrue(any("Root item must be 'Home'" in v for v in bad_viols))

        # Too short (< 2 levels)
        one_level = [{"name": "Home", "url": "https://aidigitools.tech/"}]
        short_ok, short_viols = self.engine.validate_breadcrumbs(one_level)
        self.assertFalse(short_ok)
        self.assertTrue(any("at least 2 levels" in v for v in short_viols))

    def test_related_entities_requirement(self):
        """Every article must declare at least 2 related tools and 2 related articles."""
        valid_article = {
            "related_tools": ["chatgpt-plus", "claude-pro"],
            "related_articles": ["guides/chatgpt-vs-claude.html", "best/best-ai-coding-tools.html"]
        }
        ok, viols = self.engine.validate_related_entities(valid_article)
        self.assertTrue(ok)
        self.assertEqual(len(viols), 0)

        # Insufficient tools
        bad_tools = {
            "related_tools": ["chatgpt-plus"],
            "related_articles": ["guides/chatgpt-vs-claude.html", "best/best-ai-coding-tools.html"]
        }
        b_ok, b_viols = self.engine.validate_related_entities(bad_tools)
        self.assertFalse(b_ok)
        self.assertTrue(any("related tools" in v for v in b_viols))

        # Insufficient articles
        bad_arts = {
            "related_tools": ["chatgpt-plus", "claude-pro"],
            "related_articles": ["guides/chatgpt-vs-claude.html"]
        }
        ba_ok, ba_viols = self.engine.validate_related_entities(bad_arts)
        self.assertFalse(ba_ok)
        self.assertTrue(any("related articles" in v for v in ba_viols))

    def test_rss_feed_item_generation(self):
        """Verify RSS item generator generates valid RSS 2.0 XML."""
        item_xml = self.engine.generate_rss_item({
            "title": "Cursor AI vs GitHub Copilot",
            "canonical_url": "https://aidigitools.tech/compare/cursor-vs-copilot.html",
            "description": "2026 Developer shootout.",
            "date_published": "2026-10-25T12:00:00+05:00"
        })
        self.assertIn("<item>", item_xml)
        self.assertIn("<title>Cursor AI vs GitHub Copilot</title>", item_xml)
        self.assertIn("<link>https://aidigitools.tech/compare/cursor-vs-copilot.html</link>", item_xml)
        self.assertIn("<guid>https://aidigitools.tech/compare/cursor-vs-copilot.html</guid>", item_xml)
        self.assertIn("<pubDate>", item_xml)

    def test_published_articles_registry_validity(self):
        """Verify all articles in blog_articles_registry.json pass architectural rules."""
        articles = self.engine.registry.get("articles", [])
        self.assertGreaterEqual(len(articles), 5)
        for art in articles:
            # URL check
            url_ok, url_viols = self.engine.validate_article_url(art["canonical_url"])
            self.assertTrue(url_ok, f"Article {art['id']} has invalid URL: {url_viols}")

            # Breadcrumbs check
            crumb_ok, crumb_viols = self.engine.validate_breadcrumbs(art["breadcrumbs"])
            self.assertTrue(crumb_ok, f"Article {art['id']} has invalid breadcrumbs: {crumb_viols}")

            # Related entities check
            rel_ok, rel_viols = self.engine.validate_related_entities(art)
            self.assertTrue(rel_ok, f"Article {art['id']} has invalid related entities: {rel_viols}")

    def test_real_article_pages_architecture(self):
        """Verify published article pages have semantic breadcrumbs, canonicals, and viewport."""
        sample_articles = [
            "compare/chatgpt-vs-claude.html",
            "compare/runway-vs-pika.html",
            "best/best-ai-coding-tools.html"
        ]
        for rel in sample_articles:
            path = ROOT_DIR / rel
            self.assertTrue(path.exists())
            with open(path, "r", encoding="utf-8") as f:
                html = f.read()
            res = self.engine.validate_article_architecture_compliance(html)
            self.assertTrue(res["passed"], f"Article {rel} failed architecture check: {res['violations']}")

if __name__ == "__main__":
    unittest.main()
