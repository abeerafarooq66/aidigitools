class CompetitorGapAnalyzer:
    """Analyzes keyword and tool gaps against rival Pakistani AI tool providers."""

    PRIMARY_COMPETITOR_BENCHMARKS = {
        "chatgpt-plus": {"target_price_pkr": 2300, "features": ["GPT-4o", "Voice Mode", "DALL-E 3", "Custom GPTs"]},
        "claude-pro": {"target_price_pkr": 2500, "features": ["Claude 3.5 Sonnet", "Artifacts", "Projects", "High Context"]},
        "canva-pro": {"target_price_pkr": 600, "features": ["Brand Kit", "Background Remover", "Magic Studio", "1TB Cloud"]},
        "midjourney": {"target_price_pkr": 2800, "features": ["Fast GPU Hours", "Discord Access", "Commercial License"]},
        "capcut-pro": {"target_price_pkr": 950, "features": ["Auto Captions", "Pro Effects", "4K Export", "Desktop & Mobile"]},
        "perplexity-pro": {"target_price_pkr": 2200, "features": ["Pro Search", "Claude & GPT-4o Models", "File Uploads"]}
    }

    PAKISTANI_MARKET_QUERIES = [
        "chatgpt plus easypaisa price in pakistan",
        "buy claude pro with jazzcash",
        "canva pro cheap subscription karachi lahore",
        "midjourney shared account pakistan sadapay",
        "capcut pro desktop lifetime rate pakistan",
        "perplexity pro subscription raast bank transfer"
    ]

    def analyze_catalog(self, existing_tools: list[str]) -> dict:
        existing_set = {t.lower().replace(" ", "-") for t in existing_tools}
        missing_tools = []
        covered_tools = []

        for tool_id, details in self.PRIMARY_COMPETITOR_BENCHMARKS.items():
            if tool_id in existing_set:
                covered_tools.append({"id": tool_id, "details": details})
            else:
                missing_tools.append({"id": tool_id, "details": details})

        coverage_ratio = len(covered_tools) / len(self.PRIMARY_COMPETITOR_BENCHMARKS)
        return {
            "total_benchmark_tools": len(self.PRIMARY_COMPETITOR_BENCHMARKS),
            "covered_tools": covered_tools,
            "missing_tools": missing_tools,
            "catalog_coverage_pct": round(coverage_ratio * 100, 1),
            "recommended_expansion": [m["id"] for m in missing_tools]
        }

    def generate_gap_queries(self, missing_tool_ids: list[str]) -> list[str]:
        gap_queries = []
        for tid in missing_tool_ids:
            clean_name = tid.replace("-", " ").title()
            gap_queries.append(f"buy {clean_name} pakistan easypaisa")
            gap_queries.append(f"{clean_name} price in pakistan jazzcash")
            gap_queries.append(f"how to buy {clean_name} in pakistan without credit card")
        return gap_queries
