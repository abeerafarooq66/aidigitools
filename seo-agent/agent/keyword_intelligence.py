"""
AIDigiTools — Keyword & Topic Intelligence Engine
Strictly implements Section 5 of Master Architecture Charter:
KEYWORD AND TOPIC INTELLIGENCE
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = ROOT_DIR / "data" / "topic_opportunity_registry.json"

SCORE_WEIGHTS = {
    "search_opportunity": 15,
    "gsc_bing_opportunity": 20,
    "audience_relevance": 15,
    "competitor_content_gap": 15,
    "trend_freshness": 10,
    "original_research_potential": 15,
    "business_relevance": 10
}
PREFERRED_THRESHOLD = 85

REQUIRED_ATTRIBUTES = [
    "primary_keyword",
    "secondary_keywords",
    "long_tail_queries",
    "question_based_queries",
    "related_entities",
    "search_intent",
    "language",
    "country_market_relevance",
    "existing_ranking_opportunities",
    "competitor_coverage",
    "product_category_relevance",
    "existing_target_urls",
    "cannibalization_risk"
]

class KeywordIntelligenceEngine:
    def __init__(self, registry_file: Optional[Path] = None):
        self.registry_path = registry_file or REGISTRY_PATH
        self._load_registry()
        self._load_existing_urls()

    def _load_registry(self):
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Topic registry missing at: {self.registry_path}")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.topics: List[Dict[str, Any]] = data.get("candidate_topics", [])

    def _load_existing_urls(self):
        """Scans the repository for all canonical HTML URLs."""
        self.existing_urls = []
        for p in ROOT_DIR.glob("**/*.html"):
            if any(part in p.parts for part in [".git", ".venv", "tests", "scratch"]):
                continue
            rel = p.relative_to(ROOT_DIR).as_posix()
            self.existing_urls.append(rel)

    def calculate_topic_score(self, breakdown: Dict[str, int]) -> Tuple[int, bool]:
        """
        Calculate the 7-dimension topic opportunity score out of 100.
        Returns: (total_score, passed_threshold)
        """
        total = 0
        for dim, max_pts in SCORE_WEIGHTS.items():
            pts = breakdown.get(dim, 0)
            capped_pts = max(0, min(pts, max_pts))
            total += capped_pts
        passed = total >= PREFERRED_THRESHOLD
        return total, passed

    def detect_cannibalization(self, primary_keyword: str, target_canonical_path: Optional[str] = None) -> Tuple[bool, List[str]]:
        """
        Check if the primary keyword or its exact search intent is already targeted
        by an existing canonical page in the repository.
        """
        kw_clean = primary_keyword.strip().lower()
        conflicts = []

        # If the target path already exists, it is an update, not a new page
        if target_canonical_path and target_canonical_path in self.existing_urls:
            return True, [target_canonical_path]

        is_comparison = " vs " in kw_clean or " compared to " in kw_clean

        for url in self.existing_urls:
            stem = Path(url).stem.lower().replace("-", " ")
            
            # Exact stem match
            if kw_clean == stem:
                conflicts.append(url)
                continue

            if is_comparison:
                # Comparison queries only conflict with dedicated comparison pages targeting both tools
                if "compare/" in url and (" vs " in stem or " versus " in stem):
                    # Check if entities in query overlap with existing comparison
                    parts = kw_clean.split(" vs ")
                    if len(parts) == 2 and parts[0].strip() in stem and parts[1].strip() in stem:
                        conflicts.append(url)
            else:
                # Non-comparison query: check if existing tool or guide targets this exact primary query
                if kw_clean in stem or stem in kw_clean:
                    # Single tool conflict
                    conflicts.append(url)

        is_risk = len(conflicts) > 0
        return is_risk, conflicts

    def evaluate_candidate_topic(self, topic: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate all 13 attributes, calculate the 7-part score, and determine
        recommended action (PUBLISH_NEW_ARTICLE vs UPDATE_EXISTING_PAGE vs SKIP_REJECT).
        """
        missing = [attr for attr in REQUIRED_ATTRIBUTES if attr not in topic or not topic[attr]]
        if missing:
            raise ValueError(f"Candidate topic missing required Section 5 attributes: {missing}")

        breakdown = topic.get("scoring_breakdown", {})
        score, passed = self.calculate_topic_score(breakdown)

        target_path = topic.get("target_canonical_path")
        cannibalization_risk, existing_matches = self.detect_cannibalization(
            topic["primary_keyword"],
            target_canonical_path=target_path
        )

        if not passed:
            action = "SKIP_REJECT"
            rationale = f"Opportunity score ({score}/100) is below the preferred threshold of {PREFERRED_THRESHOLD}/100."
        elif cannibalization_risk:
            action = "UPDATE_EXISTING_PAGE"
            rationale = (
                f"Opportunity score is strong ({score}/100), but existing page(s) "
                f"{existing_matches} already target this intent. Update existing page instead of creating a competing URL."
            )
        else:
            action = "PUBLISH_NEW_ARTICLE"
            rationale = f"Score ({score}/100) satisfies threshold and no competing URL targets this intent. Eligible for publication."

        return {
            "primary_keyword": topic["primary_keyword"],
            "total_score": score,
            "threshold_passed": passed,
            "cannibalization_risk": cannibalization_risk,
            "conflicting_existing_urls": existing_matches,
            "recommended_action": action,
            "editorial_rationale": rationale
        }

    def get_qualified_topics(self) -> List[Dict[str, Any]]:
        """
        Returns all candidate topics from the registry that meet or exceed
        the 85/100 threshold and are recommended for new publication.
        """
        qualified = []
        for t in self.topics:
            eval_res = self.evaluate_candidate_topic(t)
            if eval_res["recommended_action"] == "PUBLISH_NEW_ARTICLE":
                t_copy = dict(t)
                t_copy["evaluation"] = eval_res
                qualified.append(t_copy)
        return qualified

if __name__ == "__main__":
    kie = KeywordIntelligenceEngine()
    print(f"Loaded {len(kie.topics)} topics. Scanned {len(kie.existing_urls)} existing HTML URLs.")
    qualified = kie.get_qualified_topics()
    print(f"Qualified Topics for Publication (Score >= {PREFERRED_THRESHOLD}): {len(qualified)}")
    for q in qualified:
        print(f" -> {q['topic_id']}: '{q['primary_keyword']}' (Score: {q['total_opportunity_score']}/100)")
