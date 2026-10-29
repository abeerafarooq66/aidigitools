import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from .models import AuditIssue

class SchemaAuditor:
    """Validates Schema.org JSON-LD microdata across all pages."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()

    def audit_page_schemas(
        self,
        html_files: List[Path],
        timestamp: str
    ) -> Tuple[List[AuditIssue], Dict[str, Any]]:
        issues: List[AuditIssue] = []
        total_schemas_found = 0
        schema_types_count: Dict[str, int] = {}

        json_ld_pattern = re.compile(
            r'<script\s+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            re.IGNORECASE | re.DOTALL
        )

        for p in html_files:
            rel = p.relative_to(self.root).as_posix()
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue

            matches = json_ld_pattern.findall(content)
            for raw_json in matches:
                clean_json = raw_json.strip()
                if not clean_json:
                    continue

                total_schemas_found += 1
                try:
                    data = json.loads(clean_json)
                except Exception as e:
                    issues.append(AuditIssue(
                        id="MALFORMED_JSON_LD",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="STRUCTURED_DATA",
                        severity="CRITICAL",
                        confidence="CONFIRMED",
                        evidence=f"JSON-LD syntax error in {rel}: {str(e)}",
                        recommended_fix="Fix JSON syntax error (unescaped quotes, missing commas, or braces)."
                    ))
                    continue

                items = data if isinstance(data, list) else [data]
                for item in items:
                    stype = item.get("@type", "Unknown")
                    if isinstance(stype, list):
                        stype_str = "/".join(stype)
                    else:
                        stype_str = str(stype)
                    schema_types_count[stype_str] = schema_types_count.get(stype_str, 0) + 1

                    # 1. Product Schema Validation
                    if "Product" in stype_str:
                        # Check critical fields
                        for req_f in ["name", "description", "offers"]:
                            if req_f not in item:
                                issues.append(AuditIssue(
                                    id="PRODUCT_SCHEMA_MISSING_FIELD",
                                    timestamp=timestamp,
                                    tested_url=rel,
                                    category="STRUCTURED_DATA",
                                    severity="ERROR",
                                    confidence="CONFIRMED",
                                    evidence=f"Product schema in {rel} missing required field '{req_f}'.",
                                    recommended_fix=f"Add '{req_f}' property to Product JSON-LD."
                                ))
                        # Google Policy Compliance: Zero unverified aggregateRating
                        if "aggregateRating" in item:
                            issues.append(AuditIssue(
                                id="UNVERIFIED_AGGREGATE_RATING",
                                timestamp=timestamp,
                                tested_url=rel,
                                category="STRUCTURED_DATA",
                                severity="CRITICAL",
                                confidence="CONFIRMED",
                                evidence=f"Found 'aggregateRating' in {rel} without verified customer review backend.",
                                recommended_fix="Purge aggregateRating to comply with Google Search Essentials spam policies."
                            ))

                        # Offers Validation
                        offers = item.get("offers")
                        if isinstance(offers, dict):
                            if "price" not in offers or "priceCurrency" not in offers:
                                issues.append(AuditIssue(
                                    id="OFFER_SCHEMA_MISSING_PRICE",
                                    timestamp=timestamp,
                                    tested_url=rel,
                                    category="STRUCTURED_DATA",
                                    severity="ERROR",
                                    confidence="CONFIRMED",
                                    evidence=f"Offer schema in {rel} missing 'price' or 'priceCurrency'.",
                                    recommended_fix="Specify numeric price and ISO currency code (e.g. 'PKR')."
                                ))

                    # 2. BreadcrumbList Schema Validation
                    elif "BreadcrumbList" in stype_str:
                        elements = item.get("itemListElement")
                        if not elements or not isinstance(elements, list):
                            issues.append(AuditIssue(
                                id="BREADCRUMB_EMPTY",
                                timestamp=timestamp,
                                tested_url=rel,
                                category="STRUCTURED_DATA",
                                severity="ERROR",
                                confidence="CONFIRMED",
                                evidence=f"BreadcrumbList in {rel} has empty or missing 'itemListElement'.",
                                recommended_fix="Populate itemListElement with ordered ListItem objects."
                            ))
                        else:
                            for idx, elem in enumerate(elements, start=1):
                                if "item" not in elem or "name" not in elem:
                                    issues.append(AuditIssue(
                                        id="BREADCRUMB_ITEM_MISSING_PROPERTIES",
                                        timestamp=timestamp,
                                        tested_url=rel,
                                        category="STRUCTURED_DATA",
                                        severity="WARNING",
                                        confidence="CONFIRMED",
                                        evidence=f"Breadcrumb item {idx} in {rel} missing 'item' or 'name'.",
                                        recommended_fix="Add name and item URL to each breadcrumb element."
                                    ))

                    # 3. Organization Schema Validation
                    elif "Organization" in stype_str:
                        if "name" not in item or "url" not in item:
                            issues.append(AuditIssue(
                                id="ORGANIZATION_SCHEMA_INCOMPLETE",
                                timestamp=timestamp,
                                tested_url=rel,
                                category="STRUCTURED_DATA",
                                severity="WARNING",
                                confidence="CONFIRMED",
                                evidence=f"Organization schema in {rel} missing 'name' or 'url'.",
                                recommended_fix="Ensure Organization schema declares official name and url."
                            ))

                    # 4. FAQPage Schema Validation
                    elif "FAQPage" in stype_str:
                        entities = item.get("mainEntity", [])
                        if not entities or not isinstance(entities, list):
                            issues.append(AuditIssue(
                                id="FAQ_SCHEMA_EMPTY",
                                timestamp=timestamp,
                                tested_url=rel,
                                category="STRUCTURED_DATA",
                                severity="WARNING",
                                confidence="CONFIRMED",
                                evidence=f"FAQPage schema in {rel} has no mainEntity questions.",
                                recommended_fix="Add Question and acceptedAnswer pairs to FAQPage."
                            ))

        summary = {
            "total_schemas_found": total_schemas_found,
            "schema_types_count": schema_types_count
        }
        return issues, summary
