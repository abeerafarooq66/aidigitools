"""
AIDigiTools — Competitor Intelligence Engine
Strictly implements Section 4 of Master Architecture Charter:
COMPETITOR INTELLIGENCE ENGINE
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
COMPETITOR_DB_PATH = ROOT_DIR / "data" / "competitor_intelligence.json"

COMPETITOR_FORBIDDEN_PHRASES = [
    "ai tools pak",
    "aitoolspak",
    "ai tool gems",
    "aitoolgems",
    "according to competitor internal data",
    "competitor analytics reveal",
    "we hacked their traffic data",
    "private analytics show",
]

class CompetitorIntelligenceEngine:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or COMPETITOR_DB_PATH
        self._load_database()

    def _load_database(self):
        if not self.db_path.exists():
            raise FileNotFoundError(f"Competitor database missing at: {self.db_path}")
        with open(self.db_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.competitors = self.data.get("competitors", [])

    def list_competitors(self) -> List[str]:
        """List all tracked competitor names."""
        return [c["name"] for c in self.competitors]

    def get_competitor_profile(self, competitor_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve competitor profile by ID."""
        for c in self.competitors:
            if c["id"] == competitor_id:
                return c
        return None

    def analyze_topic_gaps(self, topic_keyword: str) -> Dict[str, Any]:
        """
        Analyze competitor weaknesses, missing information, and formulate
        the exact Information Gap AIDigiTools will satisfy with original research.
        """
        kw = topic_keyword.lower()
        aggregated_gaps = []
        unanswered_questions = []
        original_opportunities = []

        for c in self.competitors:
            # Check topic overlap
            overlap = any(kw in t.lower() or any(term in t.lower() for term in kw.split()) for t in c.get("primary_topics", []))
            if overlap or c["type"] in ["Regional AI Reseller & Marketplace", "Regional AI Tool Directory & Reseller"]:
                aggregated_gaps.extend(c.get("weaknesses_and_content_gaps", []))
                unanswered_questions.extend(c.get("unanswered_user_questions", []))
                original_opportunities.extend(c.get("aidigitools_original_research_opportunity", []))

        # Deduplicate while preserving order
        def dedup(lst):
            seen = set()
            return [x for x in lst if not (x in seen or seen.add(x))]

        gaps = dedup(aggregated_gaps)[:5]
        questions = dedup(unanswered_questions)[:4]
        opportunities = dedup(original_opportunities)[:5]

        return {
            "target_topic": topic_keyword,
            "competitor_weaknesses_identified": gaps,
            "missing_user_questions_to_answer": questions,
            "original_research_mandates": opportunities,
            "editorial_strategy": (
                "Do NOT duplicate competitor thin summaries. Satisfy reader intent by answering "
                f"unresolved questions with quantitative tables, transparent PKR pricing, and 30-day warranty backing."
            )
        }

    def verify_compliance_and_originality(self, text: str) -> Tuple[bool, List[str]]:
        """
        Enforce Section 4 Invariants:
        1. Never copy competitor distinctive branding or claim private competitor data.
        2. Strictly compliant research methods.
        """
        violations = []
        text_lower = text.lower()

        for phrase in COMPETITOR_FORBIDDEN_PHRASES:
            if phrase in text_lower:
                violations.append(
                    f"Compliance Violation: Detected competitor branding / fake private data claim: '{phrase}'"
                )

        # Check for claims of private competitor data
        data_claims = ["their private analytics", "competitor conversion rate is", "their internal traffic is"]
        for dc in data_claims:
            if dc in text_lower:
                violations.append(f"Violation: Claiming knowledge of competitor's private data ('{dc}') is prohibited.")

        is_valid = len(violations) == 0
        return is_valid, violations

if __name__ == "__main__":
    cie = CompetitorIntelligenceEngine()
    print("Tracked Competitors:", cie.list_competitors())
    gaps = cie.analyze_topic_gaps("ChatGPT Plus Pakistan")
    print(f"Topic Gaps for 'ChatGPT Plus Pakistan': {len(gaps['competitor_weaknesses_identified'])} gaps identified.")
    
    # Test compliance check
    valid, viols = cie.verify_compliance_and_originality("Our guide provides original research.")
    print(f"Clean text compliance: {valid}")
    assert valid
    
    valid_bad, viols_bad = cie.verify_compliance_and_originality("AI Tools Pak does not provide warranty.")
    print(f"Competitor mention check: {valid_bad}, violations: {viols_bad}")
    assert not valid_bad
    
    print("CompetitorIntelligenceEngine self-test PASSED!")
