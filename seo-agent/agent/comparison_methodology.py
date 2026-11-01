"""
AIDigiTools — Product Review & Comparison Methodology Engine
Strictly implements Section 9 of Master Architecture Charter:
PRODUCT REVIEW AND COMPARISON METHODOLOGY
"""

import re
from typing import Dict, Any, List, Tuple, Optional

REQUIRED_METHODOLOGY_ELEMENTS = [
    "evaluation_criteria",
    "intended_use_case",
    "verified_product_versions",
    "comparable_plans_compared",
    "limitations_and_tradeoffs",
    "free_or_budget_alternatives",
    "pricing_and_credits_verified",
    "pricing_separation_enforced",
    "regional_availability_explained",
    "who_should_choose_matrix",
    "who_should_not_choose_matrix",
    "primary_documentation_linked",
    "methodology_evidence_badge"
]

class ComparisonMethodologyEngine:
    def __init__(self):
        pass

    def evaluate_review_or_comparison_html(
        self,
        html_content: str,
        article_type: str = "comparison",
        evidence_classification: str = "B. Research-based"
    ) -> Dict[str, Any]:
        """
        Validates that product reviews, head-to-head comparisons, and best-of articles
        strictly adhere to the 14-point Section 9 methodology.
        """
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()
        checks = {}
        errors = []
        warnings = []

        # 1. Evaluation Criteria Disclosed
        has_criteria = (
            "evaluation criteria" in clean_text or
            "how we evaluated" in clean_text or
            "comparison criteria" in clean_text or
            "benchmark criteria" in clean_text
        )
        checks["evaluation_criteria"] = has_criteria
        if not has_criteria:
            errors.append("Section 9 Violation: Disclosed evaluation criteria missing.")

        # 2. Intended Use Case Explained
        has_use_case = (
            "use case" in clean_text or
            "ideal for" in clean_text or
            "target workflow" in clean_text or
            "best suited for" in clean_text
        )
        checks["intended_use_case"] = has_use_case
        if not has_use_case:
            errors.append("Section 9 Violation: Intended use case explanation missing.")

        # 3. Verified Product Versions
        has_versions = bool(re.search(r"\b(v\d+|\d+\.\d+|version|release|2024|2025|2026)\b", clean_text))
        checks["verified_product_versions"] = has_versions
        if not has_versions:
            warnings.append("Specific software version numbers or release milestones not clearly stated.")

        # 4. Genuinely Comparable Plans
        has_plans = "plan" in clean_text or "subscription" in clean_text or "tier" in clean_text
        checks["comparable_plans_compared"] = has_plans
        if not has_plans:
            errors.append("Section 9 Violation: Plan tier comparison missing.")

        # 5. Limitations and Trade-Offs
        has_limitations = (
            "limitation" in clean_text or
            "drawback" in clean_text or
            "trade-off" in clean_text or
            "throttling" in clean_text or
            "context limit" in clean_text
        )
        checks["limitations_and_tradeoffs"] = has_limitations
        if not has_limitations:
            errors.append("Section 9 Violation: Explicit limitations and trade-offs missing.")

        # 6. Free or Budget Alternatives
        has_alternatives = (
            "alternative" in clean_text or
            "free tier" in clean_text or
            "open source" in clean_text or
            "budget option" in clean_text
        )
        checks["free_or_budget_alternatives"] = has_alternatives
        if not has_alternatives:
            warnings.append("Consider mentioning free or budget-friendly alternative tools.")

        # 7. Pricing, Credits & Billing Conditions
        has_pricing = bool(re.search(r"(\$|\brs\.?|\bpkr\b|\busd\b)", clean_text))
        has_credits = "credit" in clean_text or "token" in clean_text or "request" in clean_text or "hour" in clean_text
        checks["pricing_and_credits_verified"] = has_pricing and has_credits
        if not (has_pricing and has_credits):
            errors.append(f"Section 9 Violation: Pricing or usage credit terms missing: has_pricing={has_pricing}, has_credits={has_credits}")

        # 8. Separate Official Provider Price from AIDigiTools Concierge Price
        has_provider_price = "$" in html_content or "usd" in clean_text
        has_concierge_price = "pkr" in clean_text or "rs." in clean_text or "rupees" in clean_text
        checks["pricing_separation_enforced"] = has_provider_price and has_concierge_price
        if not (has_provider_price and has_concierge_price):
            errors.append("Section 9 Invariant Violation: Both official vendor USD price and AIDigiTools PKR price must be presented with clear separation.")

        # 9. Regional Availability & Provider Restrictions
        has_regional = (
            "pakistan" in clean_text or
            "forex" in clean_text or
            "card decline" in clean_text or
            "easypaisa" in clean_text or
            "jazzcash" in clean_text or
            "sadapay" in clean_text
        )
        checks["regional_availability_explained"] = has_regional
        if not has_regional:
            errors.append("Section 9 Violation: Regional availability and domestic payment context missing.")

        # 10. "Who Should Choose" vs "Who Should NOT Choose" Matrix
        has_who_should = "who should choose" in clean_text or "best for" in clean_text or "choose this if" in clean_text
        has_who_not = "who should not choose" in clean_text or "avoid this if" in clean_text or "not recommended if" in clean_text
        checks["who_should_choose_matrix"] = has_who_should
        checks["who_should_not_choose_matrix"] = has_who_not
        if not (has_who_should and has_who_not):
            errors.append(f"Section 9 Violation: Unbiased audience matrix missing: has_who_should={has_who_should}, has_who_not={has_who_not}")

        # 11. Links to Primary Official Documentation
        links = re.findall(r'href=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        has_official_docs = any(
            any(vendor in l.lower() for vendor in ["docs.", "help.", "openai.com", "anthropic.com", "cursor.com", "github.com", "adobe.com"])
            for l in links
        )
        checks["primary_documentation_linked"] = has_official_docs
        if not has_official_docs:
            errors.append("Section 9 Violation: Direct link to official upstream documentation missing.")

        # 12. Methodology & Evidence Badge
        has_badge = (
            "research-based" in clean_text or
            "hands-on tested" in clean_text or
            "editorial analysis" in clean_text
        )
        checks["methodology_evidence_badge"] = has_badge
        if not has_badge:
            errors.append("Section 9 Invariant Violation: Article must display a transparent evidence badge ('Research-based' or 'Hands-on tested').")

        # 13. Anti-Biased Ranking / Anti-Manufactured Winner Check
        has_manufactured_hype = (
            "undisputed number 1 in the world" in clean_text or
            "crushes all competition effortlessly" in clean_text or
            "the only tool you will ever need" in clean_text
        )
        checks["anti_manufactured_bias"] = not has_manufactured_hype
        if has_manufactured_hype:
            errors.append("Section 9 Invariant Violation: Detected manufactured promotional hype / biased artificial winner claim.")

        passed = len(errors) == 0
        return {
            "article_type": article_type,
            "overall_valid": passed,
            "checks": checks,
            "errors": errors,
            "warnings": warnings,
            "methodology_status": "APPROVED" if passed else "REJECTED"
        }

if __name__ == "__main__":
    engine = ComparisonMethodologyEngine()
    sample_comparison_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Cursor AI vs GitHub Copilot (2026) — Review | AIDigiTools</title>
</head>
<body>
    <article>
        <div class="evidence-badge">Methodology: Research-based independent analysis</div>
        <h1>Cursor AI vs GitHub Copilot: 2026 Developer Comparison</h1>
        
        <h2>Evaluation Criteria</h2>
        <p>We evaluated both tools across four core criteria: multi-file code refactoring, context window retention, pricing in USD vs PKR, and regional Pakistani banking compatibility.</p>
        
        <h2>Intended Use Case & Plan Tier</h2>
        <p>This comparison examines the Pro subscription tier for both tools: Cursor Pro ($20/mo) and GitHub Copilot Individual ($10/mo), tailored for full-stack developers.</p>
        
        <h2>Pricing and Usage Credits</h2>
        <p>Cursor Pro costs $20 USD/month (or Rs. 3,800 PKR on AIDigiTools), granting 500 fast Claude 3.5 Sonnet requests. Copilot Individual costs $10 USD/month (Rs. 1,600 PKR on AIDigiTools) with unlimited completions.</p>
        
        <h2>Limitations and Trade-offs</h2>
        <p>Cursor's primary limitation is the 500 fast-request quota, after which requests queue. Copilot's limitation is weaker whole-repository contextual understanding.</p>
        
        <h2>Free and Open Source Alternatives</h2>
        <p>Developers on a strict budget can evaluate Continue.dev with local Ollama models as a free alternative.</p>
        
        <h2>Regional Availability & Pakistan Payment</h2>
        <p>Direct billing via international credit cards often fails due to Pakistani bank forex restrictions. AIDigiTools provides local settlement via EasyPaisa and JazzCash with 15-minute delivery and 30-day warranty.</p>
        
        <h2>Who Should Choose Which Tool?</h2>
        <p><strong>Choose this if (Who should choose Cursor):</strong> You build complex full-stack apps and need multi-file Composer refactoring.</p>
        <p><strong>Avoid this if (Who should not choose Cursor):</strong> You only need simple inline autocomplete inside JetBrains or Visual Studio; Copilot is lighter and cheaper.</p>
        
        <footer>
            <p>Official Sources: <a href="https://docs.cursor.com/">Cursor Official Documentation</a> and <a href="https://docs.github.com/en/copilot">GitHub Copilot Documentation</a>.</p>
        </footer>
    </article>
</body>
</html>"""
    res = engine.evaluate_review_or_comparison_html(sample_comparison_html)
    print(f"Sample Comparison Valid: {res['overall_valid']}, Status: {res['methodology_status']}")
    print(f"Errors: {res['errors']}")
    assert res["overall_valid"]
    print("ComparisonMethodologyEngine self-test PASSED!")

