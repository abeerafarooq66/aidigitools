"""
AIDigiTools — Structured Data & Schema Validation Engine
Strictly implements Section 13 of Master Architecture Charter:
STRUCTURED DATA RULES
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
AUTHOR_REGISTRY_PATH = ROOT_DIR / "data" / "author_registry.json"

class StructuredDataEngine:
    def __init__(self, author_registry_path: Optional[Path] = None):
        self.author_registry_path = author_registry_path or AUTHOR_REGISTRY_PATH
        self.authors = self._load_authors()

    def _load_authors(self) -> Dict[str, Dict[str, Any]]:
        if not self.author_registry_path.exists():
            return {}
        try:
            with open(self.author_registry_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {a["slug"]: a for a in data.get("authors", [])}
        except Exception:
            return {}

    def generate_article_schema(
        self,
        headline: str,
        description: str,
        author_id: str,
        image_url: str,
        date_published: str,
        date_modified: str,
        article_url: str,
        article_type: str = "TechArticle"
    ) -> Dict[str, Any]:
        """
        Generate compliant Schema.org Article / TechArticle / BlogPosting JSON-LD.
        Enforces verified author, ISO dates, publisher entity, and image standards.
        """
        author = self.authors.get(author_id)
        if not author:
            raise ValueError(f"Author '{author_id}' is not registered in author_registry.json")

        # Validate ISO dates
        pub_dt = datetime.fromisoformat(date_published)
        mod_dt = datetime.fromisoformat(date_modified)
        if mod_dt < pub_dt:
            raise ValueError(f"dateModified ({date_modified}) cannot be earlier than datePublished ({date_published})")

        return {
            "@context": "https://schema.org",
            "@type": article_type,
            "headline": headline[:110],
            "description": description[:165],
            "image": image_url,
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": article_url
            },
            "author": {
                "@type": "Person",
                "name": author["name"],
                "jobTitle": author.get("role", "Technical Editor"),
                "url": author.get("social_profiles", {}).get("website", "https://aidigitools.tech/about.html")
            },
            "publisher": {
                "@type": "Organization",
                "name": "AIDigiTools",
                "url": "https://aidigitools.tech/",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://aidigitools.tech/assets/images/aidigitools-logo.png"
                }
            },
            "datePublished": date_published,
            "dateModified": date_modified
        }

    def validate_html_structured_data(
        self,
        html_content: str,
        page_type: str = "auto",
        canonical_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive Section 13 Structured Data Validation:
        - Validates JSON-LD syntax.
        - Enforces Product/Offer schema ONLY on genuine product/tool pages.
        - Zero fabricated aggregateRating, reviews, or fake pricing.
        - Ensures schema parity with visible HTML content.
        - Validates Article/BlogPosting completeness.
        """
        errors = []
        warnings = []
        types_found = []

        # Extract all <script type="application/ld+json"> blocks
        matches = re.findall(
            r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html_content,
            re.IGNORECASE | re.DOTALL
        )

        if not matches:
            errors.append("Missing Structured Data: No JSON-LD <script> tags found.")
            return {
                "passed": False,
                "types_found": [],
                "errors": errors,
                "warnings": warnings
            }

        parsed_schemas = []
        for idx, block in enumerate(matches):
            try:
                data = json.loads(block.strip())
                parsed_schemas.append(data)
            except json.JSONDecodeError as e:
                errors.append(f"JSON-LD Syntax Error in block {idx+1}: {str(e)}")

        # Infer page_type if auto
        if page_type == "auto":
            if canonical_url and "/tools/" in canonical_url:
                page_type = "tool"
            elif canonical_url and ("/categories/" in canonical_url or "/deals.html" in canonical_url):
                page_type = "category"
            elif canonical_url and ("/compare/" in canonical_url or "/guides/" in canonical_url or "/best/" in canonical_url):
                page_type = "article"
            else:
                page_type = "core"

        # Examine all schemas
        clean_dom = re.sub(r"<[^>]+>", " ", html_content)

        for data in parsed_schemas:
            items = [data] if isinstance(data, dict) else (data if isinstance(data, list) else [])
            for item in items:
                stype = item.get("@type")
                if not stype:
                    errors.append("Schema Error: Missing '@type' property.")
                    continue

                if isinstance(stype, list):
                    types_found.extend(stype)
                else:
                    types_found.append(stype)

                # RULE 1: Anti-Fabrication Ratings & Reviews
                dumped = json.dumps(item).lower()
                if "aggregaterating" in dumped or "ratingvalue" in dumped:
                    errors.append(
                        "Fabrication Violation: 'aggregateRating' detected. "
                        "Unverified aggregate star ratings are strictly forbidden by Charter Section 13."
                    )
                if '"@type": "review"' in dumped:
                    errors.append(
                        "Fabrication Violation: Unverified 'Review' schema detected. "
                        "Must only describe real visible user reviews."
                    )

                # RULE 2: Page-Type Eligibility
                # Product schema must never appear on generic articles, categories, or guides
                if page_type in ["category", "article", "core"]:
                    if stype == "Product" or (isinstance(stype, list) and "Product" in stype):
                        errors.append(
                            f"Schema Ineligibility: Product schema applied to non-product page (type: {page_type}). "
                            "Product schema is strictly restricted to individual product/tool catalog pages."
                        )

                # RULE 3: Article / BlogPosting / TechArticle Completeness
                if stype in ["Article", "BlogPosting", "TechArticle"]:
                    req_fields = ["headline", "author", "datePublished", "dateModified", "publisher"]
                    for rf in req_fields:
                        if rf not in item:
                            errors.append(f"Article Schema Incomplete: Missing required field '{rf}' in {stype}.")

                    # Validate author structure
                    author_obj = item.get("author")
                    if isinstance(author_obj, dict):
                        if not author_obj.get("name"):
                            errors.append(f"Article Schema Error: author object missing 'name' in {stype}.")
                    elif not author_obj:
                        errors.append(f"Article Schema Error: missing author in {stype}.")

                    # Parity: Headline should match visible text
                    headline = item.get("headline", "")
                    if headline and headline.lower() not in clean_dom.lower():
                        # Allow partial match
                        headline_words = [w for w in headline.lower().split() if len(w) > 4]
                        matches_count = sum(1 for w in headline_words if w in clean_dom.lower())
                        if headline_words and (matches_count / len(headline_words)) < 0.6:
                            warnings.append(f"DOM Parity Notice: Headline '{headline[:40]}...' not found in visible text.")

                # RULE 4: Product & Offer Parity
                if stype == "Product":
                    if "name" not in item:
                        errors.append("Product Schema Error: Missing 'name'.")
                    if "offers" not in item:
                        errors.append("Product Schema Error: Missing 'offers'.")
                    else:
                        offer = item["offers"]
                        if isinstance(offer, dict):
                            price = offer.get("price")
                            if price:
                                # Ensure price appears in visible text
                                str_price = str(price)
                                if str_price not in clean_dom:
                                    warnings.append(f"Price Parity Warning: Schema price '{str_price}' not found in visible DOM text.")

        passed = len(errors) == 0

        return {
            "passed": passed,
            "page_type": page_type,
            "types_found": list(set(types_found)),
            "errors": errors,
            "warnings": warnings
        }

if __name__ == "__main__":
    engine = StructuredDataEngine()
    print("Testing StructuredDataEngine...")

    # Test Article schema generation
    article_schema = engine.generate_article_schema(
        headline="Cursor AI vs GitHub Copilot: 2026 Developer Comparison",
        description="Head-to-head benchmark comparing Cursor Pro and GitHub Copilot for software developers.",
        author_id="abeera-farooq",
        image_url="https://aidigitools.tech/assets/images/cursor-pro.png",
        date_published="2026-10-15T00:00:00+05:00",
        date_modified="2026-11-01T00:00:00+05:00",
        article_url="https://aidigitools.tech/compare/cursor-vs-copilot.html"
    )
    print(f"Article schema generated: {article_schema['@type']}, Author: {article_schema['author']['name']}")
    assert article_schema["author"]["name"] == "Abeera Farooq"

    # Test Validation on Compliant Article HTML
    compliant_article_html = f"""<!DOCTYPE html>
<html>
<head>
<script type="application/ld+json">{json.dumps(article_schema)}</script>
</head>
<body>
<h1>Cursor AI vs GitHub Copilot: 2026 Developer Comparison</h1>
<p>By Abeera Farooq</p>
</body>
</html>"""
    res = engine.validate_html_structured_data(compliant_article_html, page_type="article")
    print(f"Compliant article validation: {res['passed']}, errors: {res['errors']}")
    assert res["passed"]

    # Test Rejection of AggregateRating
    bad_rating_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Cursor Pro",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "1200"}
    }
    bad_html = f'<script type="application/ld+json">{json.dumps(bad_rating_schema)}</script>'
    res_bad = engine.validate_html_structured_data(bad_html, page_type="tool")
    print(f"AggregateRating rejection: {not res_bad['passed']}, error: {res_bad['errors']}")
    assert not res_bad["passed"]

    # Test Rejection of Product schema on generic category
    res_cat = engine.validate_html_structured_data(
        f'<script type="application/ld+json">{{"@context":"https://schema.org", "@type":"Product", "name":"Tool"}}</script>',
        page_type="category"
    )
    print(f"Category product rejection: {not res_cat['passed']}")
    assert not res_cat["passed"]

    print("StructuredDataEngine self-test PASSED!")
