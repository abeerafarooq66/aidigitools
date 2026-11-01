"""
Unit tests for Content Cluster & Product Mapping and Section 6 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.cluster_mapper import ClusterMapper

class TestClusterMapping(unittest.TestCase):
    def setUp(self):
        self.cm = ClusterMapper()

    def test_01_all_10_clusters_present(self):
        """Verify all 10 clusters specified in Section 6 exist."""
        clusters = self.cm.list_all_clusters()
        self.assertEqual(len(clusters), 10)
        slugs = [c["slug"] for c in clusters]
        expected_slugs = [
            "ai-assistants-and-llms",
            "ai-coding-and-development",
            "ai-image-and-design-tools",
            "ai-video-and-audio-tools",
            "writing-and-productivity",
            "digital-marketing-and-seo",
            "developer-apis-and-automation",
            "freelancers-and-small-businesses",
            "pricing-plans-and-cost-comparisons",
            "privacy-security-and-responsible-use"
        ]
        for es in expected_slugs:
            self.assertIn(es, slugs, f"Expected cluster '{es}' missing")

    def test_02_product_to_cluster_resolution(self):
        """Verify products map to their rightful category and cluster."""
        cursor_cluster = self.cm.find_cluster_for_product("cursor-pro")
        self.assertIsNotNone(cursor_cluster)
        self.assertEqual(cursor_cluster["slug"], "ai-coding-and-development")

        runway_cluster = self.cm.find_cluster_for_product("runway-gen3")
        self.assertIsNotNone(runway_cluster)
        self.assertEqual(runway_cluster["slug"], "ai-video-and-audio-tools")

    def test_03_internal_link_graph_prevents_orphan_pages(self):
        """Verify that resolved link graph returns >= 3 contextual links."""
        graph = self.cm.resolve_internal_link_graph("midjourney prompt guide", primary_product_slug="midjourney")
        self.assertGreaterEqual(graph["total_contextual_links_available"], 3)
        self.assertIn("categories/image.html", graph["category_hub_link"])
        self.assertTrue(any("midjourney.html" in u for u in graph["supporting_product_links"]))

    def test_04_informational_vs_commercial_cta_guard(self):
        """Verify that informational intent blocks hard-sell buy now language."""
        bad_informational = "In this article we explain AI. Buy now for only Rs. 2,000!"
        valid, viols = self.cm.validate_article_cta_rules("Informational", bad_informational)
        self.assertFalse(valid)
        self.assertTrue(any("buy now for only" in v for v in viols))

        good_informational = "In this guide we explain how Claude works. Explore the Claude Pro profile for full plan specs."
        valid_good, viols_good = self.cm.validate_article_cta_rules("Informational", good_informational)
        self.assertTrue(valid_good)
        self.assertEqual(len(viols_good), 0)

if __name__ == "__main__":
    unittest.main()

