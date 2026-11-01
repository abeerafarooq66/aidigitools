"""
Live Empirical Verification for:
- Part 5: KEYWORD AND TOPIC INTELLIGENCE
- Part 6: CONTENT CLUSTER AND PRODUCT MAPPING
"""

import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SEO_AGENT_DIR = ROOT_DIR / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.keyword_intelligence import KeywordIntelligenceEngine, PREFERRED_THRESHOLD, REQUIRED_ATTRIBUTES, SCORE_WEIGHTS
from agent.cluster_mapper import ClusterMapper

def verify_part5_keyword_intelligence():
    print("=" * 70)
    print("VERIFYING PART 5: KEYWORD AND TOPIC INTELLIGENCE")
    print("=" * 70)
    kie = KeywordIntelligenceEngine()
    print(f"1. Topics loaded from registry: {len(kie.topics)}")
    print(f"2. Existing HTML URLs scanned: {len(kie.existing_urls)}")
    
    # Check all 13 attributes on each topic
    for t in kie.topics:
        tid = t.get("topic_id")
        for attr in REQUIRED_ATTRIBUTES:
            assert attr in t and t[attr], f"Topic {tid} missing {attr}"
    print("   -> ALL 13 Section 5 mandatory attributes present across all topics [VERIFIED]")

    # Check 7 scoring dimensions
    print("3. Scoring Dimensions Verification:")
    for dim, max_pts in SCORE_WEIGHTS.items():
        print(f"   - {dim:<30}: max {max_pts} pts")
    assert sum(SCORE_WEIGHTS.values()) == 100
    print(f"   -> Total weight = 100 pts, Preferred Threshold = {PREFERRED_THRESHOLD}/100 [VERIFIED]")

    # Evaluate all candidate topics
    print("4. Live Candidate Topic Evaluation:")
    for t in kie.topics:
        eval_res = kie.evaluate_candidate_topic(t)
        tid = t["topic_id"]
        kw = t["primary_keyword"]
        score = eval_res["total_score"]
        action = eval_res["recommended_action"]
        risk = eval_res["cannibalization_risk"]
        print(f"   [{tid}] '{kw}' | Score: {score}/100 | Passed: {eval_res['threshold_passed']} | Cannibalization Risk: {risk} | Action: {action}")
        
        # Verify Invariants
        if score >= PREFERRED_THRESHOLD and not risk:
            assert action == "PUBLISH_NEW_ARTICLE"
        elif risk:
            assert action == "UPDATE_EXISTING_PAGE"
        else:
            assert action in ["SKIP_REJECT", "UPDATE_EXISTING_PAGE"]
    print("   -> Scoring gating & Cannibalization decision logic [VERIFIED]")

    # Qualified topics
    qualified = kie.get_qualified_topics()
    print(f"5. Qualified Topics Ready for Publication (Score >= {PREFERRED_THRESHOLD}): {len(qualified)}")
    for q in qualified:
        print(f"   * {q['topic_id']}: '{q['primary_keyword']}' -> {q['target_canonical_path']}")
    print("PART 5 VERIFICATION COMPLETE: ALL GATES GREEN\n")

def verify_part6_content_cluster_mapping():
    print("=" * 70)
    print("VERIFYING PART 6: CONTENT CLUSTER AND PRODUCT MAPPING")
    print("=" * 70)
    cm = ClusterMapper()
    clusters = cm.list_all_clusters()
    print(f"1. Total Content Clusters Loaded: {len(clusters)}")
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
    loaded_slugs = [c["slug"] for c in clusters]
    for es in expected_slugs:
        assert es in loaded_slugs, f"Missing cluster {es}"
        c_detail = cm.get_cluster_by_slug(es)
        print(f"   - Cluster: {c_detail['name']:<45} | Slug: {es}")
    print("   -> ALL 10 official clusters mapped [VERIFIED]")

    print("2. Product-to-Cluster Association Check:")
    test_products = [
        ("cursor-pro", "ai-coding-and-development"),
        ("chatgpt-plus", "ai-assistants-and-llms"),
        ("midjourney", "ai-image-and-design-tools"),
        ("runway-gen3", "ai-video-and-audio-tools"),
        ("nordvpn", "privacy-security-and-responsible-use")
    ]
    for p_slug, expected_cluster in test_products:
        c = cm.find_cluster_for_product(p_slug)
        assert c is not None and c["slug"] == expected_cluster
        print(f"   * Product '{p_slug}' successfully mapped to '{c['name']}'")
    print("   -> Product-to-cluster mappings [VERIFIED]")

    print("3. Internal Linking Graph & Zero-Orphan Page Invariant:")
    sample_queries = [
        ("cursor vs copilot", "cursor-pro"),
        ("claude artifacts tutorial", "claude-pro"),
        ("runway gen 3 video editing", "runway-gen3")
    ]
    for q, p in sample_queries:
        graph = cm.resolve_internal_link_graph(q, primary_product_slug=p)
        total_links = graph["total_contextual_links_available"]
        assert total_links >= 3, "Must have at least 3 contextual links"
        print(f"   * Query '{q}': {total_links} contextual links mapped (Hub: {graph['category_hub_link']})")
    print("   -> Zero-orphan page internal linking guarantee [VERIFIED]")

    print("4. Informational Intent vs. Hard-Sell CTA Rule:")
    # Clean educational CTA
    clean_text = "In this guide we explain how Claude Artifacts work. Explore the Claude Pro tool profile for plan specifications."
    valid_clean, _ = cm.validate_article_cta_rules("Informational", clean_text)
    assert valid_clean
    print("   * Educational CTA in Informational article: ACCEPTED [VERIFIED]")

    # Aggressive hard sell CTA in informational article
    bad_text = "In this guide we explain AI. Buy now for only Rs. 2,000! Grab your account now!"
    valid_bad, viols = cm.validate_article_cta_rules("Informational", bad_text)
    assert not valid_bad
    print(f"   * Aggressive hard sell in Informational article: BLOCKED [VERIFIED] (Violations: {len(viols)})")
    print("PART 6 VERIFICATION COMPLETE: ALL GATES GREEN\n")

if __name__ == "__main__":
    verify_part5_keyword_intelligence()
    verify_part6_content_cluster_mapping()
    print("=" * 70)
    print("ALL VERIFICATIONS FOR PART 5 & PART 6 PASSED 100% GREEN!")
    print("=" * 70)
