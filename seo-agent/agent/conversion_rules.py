"""
AIDigiTools — Product Conversion & CTA Governance Engine
Strictly implements Section 10 of Master Architecture Charter:
AIDIGITOOLS PRODUCT CONVERSION RULES
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APPROVED_CONTEXTUAL_CTAS = [
    "Explore Full Tool Details",
    "Compare Available Plans",
    "Check Product Availability",
    "View the Relevant Tool Profile",
    "Contact AIDigiTools on WhatsApp"
]

HOLD_PRODUCTS = {
    "coursera-plus",
    "linkedin-premium",
    "netflix-premium",
    "spotify-premium",
    "turnitin-student"
}

PROHIBITED_GATEWAY_CLAIMS = [
    r"\bpay\s+(?:directly\s+)?with\s+credit\s+card\s+on\s+(?:our\s+)?website\b",
    r"\bcheckout\s+(?:directly\s+)?on\s+(?:the\s+)?website\b",
    r"\bautomated\s+website\s+payment\s+gateway\b",
    r"\bonline\s+credit\s+card\s+processor\s+on\s+site\b",
    r"\benter\s+your\s+card\s+details\s+at\s+checkout\b"
]

class ConversionEngine:
    def __init__(self):
        self.official_wa_number = "03326861112"
        self.official_wa_intl = "+92 332 6861112"

    def is_purchase_cta_permitted(self, product_slug: str) -> bool:
        """Only products not on hold permit direct purchasing CTAs."""
        return product_slug.lower() not in HOLD_PRODUCTS

    def generate_contextual_cta(self, product_slug: str, cta_text: Optional[str] = None) -> Dict[str, str]:
        """
        Generate a compliant, contextual CTA button/link matching Section 10 rules:
        - If product is on Hold: generates inquiry-only CTA to WhatsApp.
        - If product is Active: links to canonical tool profile or WhatsApp concierge.
        """
        slug = product_slug.lower()
        is_hold = slug in HOLD_PRODUCTS

        if is_hold:
            text = cta_text or "Check Product Availability on WhatsApp"
            href = f"https://wa.me/923326861112?text=Hi%20AIDigiTools%2C%20I%20would%20like%20to%20inquire%20about%20{slug}%20availability"
            cta_type = "INQUIRY_ONLY"
        else:
            text = cta_text or "Explore Full Tool Details & Pricing"
            href = f"https://aidigitools.tech/tools/{slug}.html"
            cta_type = "CONTEXTUAL_PROFILE"

        return {
            "product_slug": slug,
            "cta_text": text,
            "cta_href": href,
            "cta_type": cta_type,
            "purchase_permitted": not is_hold
        }

    def validate_article_conversion_compliance(
        self,
        html_content: str,
        cluster_slug: Optional[str] = None,
        primary_product_slug: Optional[str] = None
    ) -> Tuple[bool, List[str]]:
        """
        Audit article for Section 10 compliance:
        1. Zero fake website payment gateway claims.
        2. Zero direct purchase CTAs on Hold products.
        3. Delivery SLA (15m) and Warranty (30d) alignment.
        4. No unrelated product injection.
        """
        violations = []
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()

        # 1. Fake payment gateway check
        for pattern in PROHIBITED_GATEWAY_CLAIMS:
            if re.search(pattern, clean_text):
                violations.append(
                    f"Payment Gateway Violation: Article claims automated website checkout matching '{pattern}'. "
                    "Actual payment completes via WhatsApp concierge with domestic/global rails."
                )

        # 2. Hold product direct buy CTA check
        for hold_slug in HOLD_PRODUCTS:
            name_variant = hold_slug.replace('-', ' ')
            if hold_slug in clean_text or name_variant in clean_text or hold_slug in html_content:
                # Check if there is an aggressive buy CTA targeting this hold product
                hold_buy_pattern = rf"\b(?:buy|order|purchase)\s+(?:now\s+)?(?:{hold_slug}|{name_variant})\b"
                if re.search(hold_buy_pattern, clean_text):
                    violations.append(
                        f"Hold Product Violation: Product '{hold_slug}' is on HOLD / INQUIRY ONLY. "
                        "Direct purchase CTA is strictly prohibited. Must use inquiry-only CTA."
                    )

        # 3. Policy alignment check (Warranty and Delivery)
        if "warranty" in clean_text:
            if "30-day" not in clean_text and "30 day" not in clean_text and "30 days" not in clean_text:
                violations.append("Policy Mismatch: Warranty mentioned but fails to state standard '30-day replacement warranty'.")

        if "delivery" in clean_text:
            if "15-minute" not in clean_text and "15 minute" not in clean_text and "15m" not in clean_text:
                violations.append("Policy Mismatch: Delivery mentioned but fails to state standard '15-minute digital delivery SLA'.")

        # 4. Irrelevant Product Injection Guard
        # If writing in AI coding cluster, ensure we haven't injected entertainment streaming tools like netflix or prime
        if cluster_slug in ["ai-coding-and-development", "ai-assistants-and-llms"]:
            irrelevant_tools = ["netflix-premium", "prime-video", "spotify-premium"]
            for irr in irrelevant_tools:
                if f"/tools/{irr}.html" in html_content or irr.replace("-", " ") in clean_text:
                    violations.append(
                        f"Topic Relevance Violation: Irrelevant product '{irr}' injected into technical coding/LLM article."
                    )

        is_valid = len(violations) == 0
        return is_valid, violations

if __name__ == "__main__":
    ce = ConversionEngine()
    print("Testing ConversionEngine...")
    
    # Test Active product CTA
    active_cta = ce.generate_contextual_cta("cursor-pro")
    print(f"Active CTA: {active_cta}")
    assert active_cta["cta_type"] == "CONTEXTUAL_PROFILE"
    assert active_cta["purchase_permitted"]
    
    # Test Hold product CTA
    hold_cta = ce.generate_contextual_cta("coursera-plus")
    print(f"Hold CTA: {hold_cta}")
    assert hold_cta["cta_type"] == "INQUIRY_ONLY"
    assert not hold_cta["purchase_permitted"]
    assert "inquire" in hold_cta["cta_href"].lower()
    
    # Test Gateway Claim Violation
    bad_html = "<p>You can pay directly with credit card on our website checkout.</p>"
    valid, viols = ce.validate_article_conversion_compliance(bad_html)
    print(f"Gateway violation detected: {not valid}, errors: {viols}")
    assert not valid
    
    # Test Irrelevant injection
    irrelevant_html = '<p>Check out our coding IDE and also <a href="/tools/netflix-premium.html">Netflix</a>.</p>'
    valid_irr, viols_irr = ce.validate_article_conversion_compliance(irrelevant_html, cluster_slug="ai-coding-and-development")
    print(f"Irrelevant injection detected: {not valid_irr}, errors: {viols_irr}")
    assert not valid_irr
    
    print("ConversionEngine self-test PASSED!")
