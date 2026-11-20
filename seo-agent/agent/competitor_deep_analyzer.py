"""
AIDigiTools — Competitor Deep SEO & Content Strategy Analyzer
=============================================================
Analyzes competitor organic traffic, ranking pages, content strategies,
internal linking models, topical authority, and information gaps to
formulate 10x more useful original research for AIDigiTools.

Strictly enforces Section 4 of Master Architecture Charter:
1. Zero plagiarism or copying of competitor text/titles.
2. Zero fabricated claims of competitor private analytics.
3. 100% original, empirical, helpful content.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
COMPETITOR_DB_PATH = ROOT_DIR / "data" / "competitor_intelligence.json"
COMPETITOR_MATRIX_PATH = ROOT_DIR / "data" / "competitor_backlink_matrix.json"


class CompetitorDeepAnalyzer:
    """Deep competitive search intelligence engine for AIDigiTools."""

    def __init__(
        self,
        db_path: Optional[Path] = None,
        matrix_path: Optional[Path] = None
    ):
        self.db_path = db_path or COMPETITOR_DB_PATH
        self.matrix_path = matrix_path or COMPETITOR_MATRIX_PATH
        self._load_data()

    def _load_data(self):
        if not self.db_path.exists():
            raise FileNotFoundError(f"Missing competitor DB at: {self.db_path}")
        with open(self.db_path, "r", encoding="utf-8") as f:
            self.competitor_info = json.load(f)

        if self.matrix_path.exists():
            with open(self.matrix_path, "r", encoding="utf-8") as f:
                self.matrix_info = json.load(f)
        else:
            self.matrix_info = {"competitors": [], "backlink_gap_analysis": []}

    def list_tracked_competitors(self) -> List[Dict[str, Any]]:
        """Returns consolidated profiles of all tracked competitors."""
        out = []
        for c in self.competitor_info.get("competitors", []):
            mat_match = next((m for m in self.matrix_info.get("competitors", []) if m.get("domain") in c.get("domain", "")), None)
            merged = dict(c)
            if mat_match:
                merged["estimated_referring_domains"] = mat_match.get("estimated_referring_domains", 0)
                merged["estimated_total_backlinks"] = mat_match.get("estimated_total_backlinks", 0)
                merged["domain_rating"] = mat_match.get("domain_rating", 0)
                merged["estimated_monthly_organic_traffic"] = mat_match.get("estimated_monthly_organic_traffic", 0)
                merged["top_linked_pages"] = mat_match.get("top_linked_pages", [])
                merged["strongest_referring_domains"] = mat_match.get("strongest_referring_domains", [])
            out.append(merged)
        return out

    def analyze_competitor_content_strategies(self) -> List[Dict[str, Any]]:
        """
        Extracts key architectural patterns, content weaknesses, and
        the exact differentiation strategy AIDigiTools uses to win search rankings.
        """
        strategies = []
        for c in self.competitor_info.get("competitors", []):
            cid = c.get("id")
            name = c.get("name")
            typ = c.get("type")
            weaknesses = c.get("weaknesses_and_content_gaps", [])
            unanswered = c.get("unanswered_user_questions", [])
            opportunities = c.get("aidigitools_original_research_opportunity", [])

            strategies.append({
                "competitor_id": cid,
                "competitor_name": name,
                "competitor_type": typ,
                "content_weaknesses": weaknesses[:4],
                "unanswered_questions": unanswered[:3],
                "aidigitools_counter_strategy": opportunities[:4]
            })
        return strategies

    def generate_original_content_brief(self, topic_keyword: str) -> Dict[str, Any]:
        """
        Formulates an empirical, anti-copying content brief for AIDigiTools
        to satisfy search intent better than any existing competitor page.
        """
        kw_lower = topic_keyword.lower()
        matched_gaps = []
        matched_questions = []

        for c in self.competitor_info.get("competitors", []):
            if any(term in kw_lower for term in ["pakistan", "price", "pkr", "easypaisa", "jazzcash", "video", "coding", "canva", "chatgpt", "midjourney"]):
                matched_gaps.extend(c.get("weaknesses_and_content_gaps", []))
                matched_questions.extend(c.get("unanswered_user_questions", []))

        # Deduplicate
        def dedup(seq):
            seen = set()
            return [x for x in seq if not (x in seen or seen.add(x))]

        final_gaps = dedup(matched_gaps)[:5]
        final_questions = dedup(matched_questions)[:4]

        return {
            "target_keyword": topic_keyword,
            "target_intent": "Commercial / Informational (Pakistan & International)",
            "required_sections": [
                {"name": "Quick Answer Capsule", "length": "35-70 words", "purpose": "Google AI Overview grounding & immediate clarity"},
                {"name": "Quantitative Comparison Table", "columns": ["Plan", "PKR Price", "USD Price", "Key Limitation", "SLA"], "purpose": "Satisfy comparison intent with verified data"},
                {"name": "Step-by-Step Payment Troubleshooting", "purpose": "Overcome 3D Secure & international card decline barriers"},
                {"name": "First-Hand Empirical Verification", "purpose": "Demonstrate authentic testing, latency, and credit burn rates"},
                {"name": "Interactive FAQ Accordion", "items_count": "4-6 questions", "purpose": "Answer PAA and high-intent long-tail questions"}
            ],
            "competitor_shortcomings_to_exploit": final_gaps,
            "must_answer_questions": final_questions,
            "anti_plagiarism_invariant": "Never copy competitor phrasing or claim private access. Ground all pricing strictly in central_product_registry.json."
        }

    def evaluate_featured_snippet_targets(self) -> List[Dict[str, Any]]:
        """Identifies search queries where AIDigiTools can win Google Featured Snippets."""
        return [
            {
                "query": "how to pay for midjourney in pakistan without credit card",
                "format": "Ordered List / Step-by-Step",
                "current_winner": "Thin forum posts & Reddit snippets",
                "aidigitools_advantage": "Dedicated verified guide with domestic EasyPaisa/JazzCash activation steps",
                "target_page": "blog/how-to-pay-for-midjourney-in-pakistan-without-credit-card.html"
            },
            {
                "query": "best ai video generators for youtube shorts in pakistan",
                "format": "Quantitative Comparison Table",
                "current_winner": "Generic US listicles lacking PKR rates",
                "aidigitools_advantage": "Full pricing, credit burn rate per minute, and local ISP latency tests",
                "target_page": "blog/best-ai-video-generators-youtube-shorts-pakistan.html"
            },
            {
                "query": "claude 3.5 sonnet vs chatgpt plus coding comparison",
                "format": "Paragraph Quick Answer + Benchmark Matrix",
                "current_winner": "Outdated comparison articles from early 2024",
                "aidigitools_advantage": "Fresh 2026 developer benchmark with real codebase refactoring results",
                "target_page": "blog/claude-3-5-sonnet-vs-chatgpt-plus-coding-benchmark.html"
            }
        ]
