"""
AIDigiTools — Content Cluster & Product Relationship Mapper
Strictly implements Section 6 of Master Architecture Charter:
CONTENT CLUSTER AND PRODUCT MAPPING
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CLUSTERS_PATH = ROOT_DIR / "data" / "content_clusters.json"

class ClusterMapper:
    def __init__(self, clusters_file: Optional[Path] = None):
        self.clusters_path = clusters_file or CLUSTERS_PATH
        self._load_clusters()

    def _load_clusters(self):
        if not self.clusters_path.exists():
            raise FileNotFoundError(f"Content clusters file missing at: {self.clusters_path}")
        with open(self.clusters_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.clusters: List[Dict[str, Any]] = data.get("clusters", [])
        self.cluster_by_slug = {c["slug"]: c for c in self.clusters}

    def list_all_clusters(self) -> List[Dict[str, str]]:
        """List all 10 content clusters with id and name."""
        return [{"id": c["cluster_id"], "slug": c["slug"], "name": c["name"]} for c in self.clusters]

    def get_cluster_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        return self.cluster_by_slug.get(slug)

    def find_cluster_for_product(self, product_slug: str) -> Optional[Dict[str, Any]]:
        """Find the primary topic cluster for a specific tool."""
        for c in self.clusters:
            if product_slug in c.get("associated_products", []):
                return c
        return None

    def resolve_internal_link_graph(self, topic_keyword: str, primary_product_slug: Optional[str] = None) -> Dict[str, Any]:
        """
        Build a contextual internal linking graph for an article to prevent orphan pages:
        1. Category Hub link
        2. Supporting Product Profile link(s)
        3. Relevant Comparison or Guide link(s)
        4. Sibling planned article link(s)
        """
        kw = topic_keyword.lower()
        matched_cluster = None

        if primary_product_slug:
            matched_cluster = self.find_cluster_for_product(primary_product_slug)

        if not matched_cluster:
            for c in self.clusters:
                if any(term in kw for term in c["slug"].split("-")):
                    matched_cluster = c
                    break

        if not matched_cluster:
            matched_cluster = self.clusters[0]  # default to AI Assistants

        category_url = matched_cluster.get("primary_category_url", "https://aidigitools.tech/categories/coding.html")
        product_slugs = matched_cluster.get("associated_products", [])[:3]
        product_urls = [f"https://aidigitools.tech/tools/{p}.html" for p in product_slugs]
        guides = matched_cluster.get("supporting_comparisons_and_guides", [])
        siblings = matched_cluster.get("planned_blog_topics", [])

        link_graph = {
            "cluster_slug": matched_cluster["slug"],
            "cluster_name": matched_cluster["name"],
            "category_hub_link": category_url,
            "supporting_product_links": product_urls,
            "comparison_and_guide_links": guides,
            "sibling_article_links": siblings,
            "total_contextual_links_available": 1 + len(product_urls) + len(guides) + len(siblings)
        }
        return link_graph

    def validate_article_cta_rules(self, search_intent: str, draft_text: str) -> Tuple[bool, List[str]]:
        """
        Enforce Section 6 Invariant:
        Informational articles MUST NOT be turned into aggressive sales pages.
        Direct purchase CTAs belong on product pages; informational articles should use
        educational exploration CTAs.
        """
        violations = []
        text_lower = draft_text.lower()

        if search_intent.lower() == "informational":
            aggressive_signals = [
                "buy now for only",
                "limited time discount",
                "order immediately",
                "purchase this instantly to save",
                "grab your account now"
            ]
            for sig in aggressive_signals:
                if sig in text_lower:
                    violations.append(
                        f"Intent Mismatch Violation: Informational article contains aggressive sales pitch: '{sig}'. "
                        "Informational content must educate readers and use soft contextual discovery CTAs."
                    )

        is_valid = len(violations) == 0
        return is_valid, violations

if __name__ == "__main__":
    cm = ClusterMapper()
    print(f"Loaded {len(cm.list_all_clusters())} content clusters.")
    graph = cm.resolve_internal_link_graph("cursor vs copilot", primary_product_slug="cursor-pro")
    print(f"Link Graph for 'cursor vs copilot': {graph['cluster_name']} ({graph['total_contextual_links_available']} links)")
    
    # Test CTA rule
    valid, viols = cm.validate_article_cta_rules(
        "Informational",
        "In this guide we explain how Claude Artifacts work. Explore the Claude Pro tool profile to learn more."
    )
    print(f"Informational CTA test: valid={valid}")
    assert valid
    
    valid_bad, viols_bad = cm.validate_article_cta_rules(
        "Informational",
        "Buy now for only Rs. 2,000! Grab your account now!"
    )
    print(f"Aggressive CTA test: valid={valid_bad}, violations={viols_bad}")
    assert not valid_bad
    
    print("ClusterMapper self-test PASSED!")
