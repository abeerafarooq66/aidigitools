"""
AIDigiTools — Central Product Intelligence Engine
Strictly implements Section 2 of Master Architecture Charter:
CENTRAL PRODUCT INTELLIGENCE DATABASE
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
REGISTRY_PATH = ROOT_DIR / "data" / "central_product_registry.json"

PROHIBITED_TERMS = [
    r"\bshared\s+slot\b",
    r"\bcracked\b",
    r"\bprofile\s+pin\b",
    r"\bedu\s+pack\b",
    r"\bofficial\s+partner\b",
    r"\bauthorized\s+distributor\b",
    r"\bdirect\s+partnership\b",
    r"\bexclusive\s+access\b",
]

class ProductIntelligence:
    def __init__(self, registry_file: Optional[Path] = None):
        self.registry_path = registry_file or REGISTRY_PATH
        self._load_registry()

    def _load_registry(self):
        if not self.registry_path.exists():
            raise FileNotFoundError(f"Central product registry missing at: {self.registry_path}")
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.products: Dict[str, Dict[str, Any]] = {p["slug"]: p for p in data}

    def get_product(self, slug: str) -> Optional[Dict[str, Any]]:
        """Retrieve verified product fact record by slug."""
        return self.products.get(slug)

    def list_all_slugs(self) -> List[str]:
        """List all 49 canonical product slugs."""
        return list(self.products.keys())

    def is_cta_permitted(self, slug: str) -> bool:
        """
        Check if a direct purchase CTA is permitted.
        Returns False for Hold / Inquiry Only products.
        """
        product = self.get_product(slug)
        if not product:
            return False
        return bool(product.get("purchase_cta_permitted", False))

    def get_pricing_breakdown(self, slug: str) -> Dict[str, Any]:
        """
        Get strictly separated provider pricing and AIDigiTools offer pricing.
        Guarantees that official provider price and AIDigiTools offer are never combined.
        """
        product = self.get_product(slug)
        if not product:
            raise KeyError(f"Product slug not found: {slug}")
        return {
            "official_provider_price": product["official_provider_price"],
            "official_pricing_url": product["official_pricing_source_url"],
            "aidigitools_offer_price_pkr": product["aidigitools_offer_price_pkr"],
            "aidigitools_offer_price_usd": product["aidigitools_offer_price_usd"],
            "billing_period": product["billing_period"],
            "price_source_and_last_verified": product["price_source_and_last_verified"],
            "is_separate_concierge_offer": True
        }

    def validate_article_claims(self, text: str, primary_slug: Optional[str] = None) -> Tuple[bool, List[str]]:
        """
        Audit draft text for compliance with Section 2 invariants:
        1. Prohibited account-sharing or cracking buzzwords.
        2. Prohibited unverified partnership claims.
        3. Purchase CTA violations on Hold products.
        """
        violations = []
        text_lower = text.lower()

        # 1. Prohibited vocabulary check
        for pattern in PROHIBITED_TERMS:
            m = re.search(pattern, text_lower)
            if m:
                violations.append(f"Prohibited terminology detected: '{m.group(0)}' (pattern: {pattern})")

        # 2. Partnership / Official Reseller check
        if "official partner" in text_lower or "authorized reseller" in text_lower:
            violations.append("Violation: Article claims official partner or authorized reseller status without proof.")

        # 3. Hold product CTA check
        if primary_slug and not self.is_cta_permitted(primary_slug):
            cta_signals = ["buy now", "order now", "add to cart", "purchase now", "instant buy"]
            for sig in cta_signals:
                if sig in text_lower:
                    violations.append(
                        f"Violation: Product '{primary_slug}' is on HOLD / INQUIRY ONLY. "
                        f"Purchase CTA '{sig}' is strictly prohibited."
                    )

        # 4. WhatsApp payment reality check
        if "credit card gateway on website" in text_lower or "checkout directly on site" in text_lower:
            violations.append("Violation: Inaccurate claim about automated website gateway. Orders settle via WhatsApp.")

        is_valid = len(violations) == 0
        return is_valid, violations

if __name__ == "__main__":
    pi = ProductIntelligence()
    print(f"Loaded {len(pi.list_all_slugs())} products in ProductIntelligence registry.")
    print("Testing claim validator...")
    valid, viols = pi.validate_article_claims("Get a shared slot with profile pin")
    print(f"Result: {valid}, violations: {viols}")
    assert not valid
    print("Self-test passed!")
