"""
AIDigiTools — Trust, Transparency & Editorial Governance Engine
Strictly implements Section 11 of Master Architecture Charter:
TRUST, TRANSPARENCY AND EDITORIAL GOVERNANCE
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
AUTHOR_REGISTRY_PATH = ROOT_DIR / "data" / "author_registry.json"

AFFILIATE_INDICATORS = [
    r"[?&](?:ref|aff|affiliate|partner|via|coupon|referral)=",
    r"shareasale\.com",
    r"impactradius\.com",
    r"awin1\.com",
    r"partnerize\.com",
    r"commission-junction\.com",
    r"cj\.com",
    r"linkshare\.com"
]

FABRICATED_CLAIM_PATTERNS = [
    r"\bofficially\s+endorsed\s+by\s+(?:openai|anthropic|google|microsoft)\b",
    r"\bvoted\s+#?1\s+(?:in\s+the\s+world|globally)\s+by\s+(?:mit|stanford|harvard)\b",
    r"\bexclusive\s+(?:partner|reseller)\s+authorized\s+by\s+(?:openai|anthropic)\b",
    r"\bdr\.\s+[a-z\s]+(?:phd|md)\s+confirmed\s+our\s+rankings\b"
]

class EditorialGovernanceEngine:
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or AUTHOR_REGISTRY_PATH
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if not self.registry_path.exists():
            return {"authors": []}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_registered_authors(self) -> Dict[str, Dict[str, Any]]:
        return {a["slug"]: a for a in self.registry.get("authors", [])}

    def validate_author(self, author_slug: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Verify author identity exists in official verified author registry."""
        authors = self.get_registered_authors()
        author = authors.get(author_slug)
        if author and author.get("verified_identity") and not author.get("is_fictional", False):
            return True, author
        return False, None

    def validate_human_review_claim(
        self,
        html_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[str]]:
        """
        Verify claims of human editorial review:
        - Do not claim human review unless actually reviewed by a registered human editor.
        - Check that reviewer ID is authentic.
        """
        violations = []
        metadata = metadata or {}
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()

        claims_human_review_in_copy = bool(re.search(
            r"\b(?:reviewed|edited|fact-checked)\s+by\s+(?:a\s+)?human\s+(?:editor|reviewer)\b",
            clean_text
        ))

        claims_review_metadata = metadata.get("human_reviewed", False)

        if claims_human_review_in_copy or claims_review_metadata:
            reviewer_slug = metadata.get("reviewed_by")
            if not reviewer_slug:
                violations.append(
                    "Human Review Violation: Article claims human editorial review, but no 'reviewed_by' author slug is provided."
                )
            else:
                is_valid, reviewer = self.validate_author(reviewer_slug)
                if not is_valid:
                    violations.append(
                        f"Human Review Violation: Reviewer '{reviewer_slug}' is not registered as a verified human editor in author_registry.json."
                    )
                elif not reviewer.get("is_human", False):
                    violations.append(
                        f"Human Review Violation: Reviewer '{reviewer_slug}' is not a human editor."
                    )

            review_date = metadata.get("review_date")
            if not review_date:
                violations.append(
                    "Human Review Violation: Article claims human review but lacks an authentic 'review_date' timestamp."
                )
            else:
                try:
                    datetime.fromisoformat(review_date)
                except ValueError:
                    violations.append(
                        f"Human Review Violation: Invalid review_date format '{review_date}'. Expected ISO format (YYYY-MM-DD)."
                    )

        return len(violations) == 0, violations

    def validate_ai_transparency(
        self,
        html_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[str]]:
        """
        Validate AI assistance transparency:
        - If article was generated or researched with AI assistance, disclose it transparently.
        """
        violations = []
        metadata = metadata or {}
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()

        ai_assisted = metadata.get("ai_assisted", False)
        if ai_assisted:
            # Check for visible transparency badge or note in HTML
            has_ai_badge = bool(re.search(
                r"\b(?:ai\s+assisted|ai-assisted|produced\s+with\s+(?:the\s+assistance\s+of\s+)?ai|synthesized\s+with\s+ai|ai\s+research\s+assistance)\b",
                clean_text
            ))
            if not has_ai_badge:
                violations.append(
                    "AI Transparency Violation: Article is metadata-flagged as AI-assisted, but lacks a visible transparency notice for readers."
                )

        return len(violations) == 0, violations

    def validate_affiliate_and_sponsored_links(
        self,
        html_content: str
    ) -> Tuple[bool, List[str]]:
        """
        Enforce rel="sponsored" on compensated/affiliate links per Google & FTC rules:
        - Outbound links containing affiliate query params or tracking platforms MUST have rel="sponsored".
        """
        violations = []
        # Find all <a> tags with href and rel attributes
        link_matches = re.finditer(r'<a\s+([^>]*?)href=["\']([^"\']+)["\']([^>]*?)>', html_content, re.IGNORECASE)

        for match in link_matches:
            before_attrs, href, after_attrs = match.groups()
            all_attrs = f"{before_attrs} {after_attrs}"

            # Check if this link is an affiliate link
            is_affiliate = False
            for pattern in AFFILIATE_INDICATORS:
                if re.search(pattern, href, re.IGNORECASE):
                    is_affiliate = True
                    break

            if is_affiliate:
                rel_match = re.search(r'rel=["\']([^"\']+)["\']', all_attrs, re.IGNORECASE)
                if not rel_match:
                    violations.append(
                        f"Affiliate Link Violation: Compensated link '{href}' is missing rel='sponsored'."
                    )
                else:
                    rel_val = rel_match.group(1).lower().split()
                    if "sponsored" not in rel_val:
                        violations.append(
                            f"Affiliate Link Violation: Compensated link '{href}' has rel='{rel_match.group(1)}' but is missing mandatory 'sponsored' token."
                        )

        return len(violations) == 0, violations

    def validate_no_fabricated_claims(
        self,
        html_content: str
    ) -> Tuple[bool, List[str]]:
        """
        Reject fake endorsements, invented expert rankings, or false official partnership claims.
        """
        violations = []
        clean_text = re.sub(r"<[^>]+>", " ", html_content).lower()

        for pattern in FABRICATED_CLAIM_PATTERNS:
            match = re.search(pattern, clean_text)
            if match:
                violations.append(
                    f"Fabricated Claim Violation: Prohibited claim detected matching pattern '{pattern}'."
                )

        return len(violations) == 0, violations

    def validate_editorial_policy_compliance(
        self,
        html_content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive Section 11 editorial governance audit.
        """
        metadata = metadata or {}
        errors = []

        # 1. Author check
        author_slug = metadata.get("author_slug")
        author_valid = True
        if author_slug:
            author_valid, _ = self.validate_author(author_slug)
            if not author_valid:
                errors.append(
                    f"Author Registry Violation: Author '{author_slug}' is not registered in official author_registry.json."
                )

        # 2. Human review claim check
        human_valid, human_errors = self.validate_human_review_claim(html_content, metadata)
        errors.extend(human_errors)

        # 3. AI assistance transparency check
        ai_valid, ai_errors = self.validate_ai_transparency(html_content, metadata)
        errors.extend(ai_errors)

        # 4. Sponsored link check
        sponsored_valid, sponsored_errors = self.validate_affiliate_and_sponsored_links(html_content)
        errors.extend(sponsored_errors)

        # 5. Fabricated claims check
        claims_valid, claims_errors = self.validate_no_fabricated_claims(html_content)
        errors.extend(claims_errors)

        overall_valid = len(errors) == 0

        return {
            "overall_valid": overall_valid,
            "author_valid": author_valid,
            "human_review_valid": human_valid,
            "ai_transparency_valid": ai_valid,
            "sponsored_links_valid": sponsored_valid,
            "claims_valid": claims_valid,
            "errors": errors
        }

if __name__ == "__main__":
    gov = EditorialGovernanceEngine()
    print("Testing EditorialGovernanceEngine...")

    # Test registered author
    ok, author = gov.validate_author("abeera-farooq")
    print(f"Author abeera-farooq: {ok}, {author['name']}")
    assert ok

    # Test fake author
    fake_ok, _ = gov.validate_author("fake-doctor-smith")
    print(f"Fake author rejected: {not fake_ok}")
    assert not fake_ok

    # Test false human review claim
    bad_html = "<p>Reviewed by a human editor with 10 years experience.</p>"
    ok_rev, errs_rev = gov.validate_human_review_claim(bad_html, metadata={})
    print(f"False human review claim caught: {not ok_rev}")
    assert not ok_rev

    # Test affiliate link missing rel="sponsored"
    aff_html = '<p>Check out <a href="https://vendor.com/?ref=aidigitools">Tool</a></p>'
    ok_aff, errs_aff = gov.validate_affiliate_and_sponsored_links(aff_html)
    print(f"Affiliate link missing sponsored caught: {not ok_aff}")
    assert not ok_aff

    # Test compliant affiliate link
    good_aff_html = '<p>Check out <a href="https://vendor.com/?ref=aidigitools" rel="nofollow sponsored">Tool</a></p>'
    ok_good_aff, _ = gov.validate_affiliate_and_sponsored_links(good_aff_html)
    print(f"Compliant affiliate link passed: {ok_good_aff}")
    assert ok_good_aff

    # Test fabricated claim
    fake_claim_html = "<p>AIDigiTools was officially endorsed by OpenAI in 2026.</p>"
    ok_claim, errs_claim = gov.validate_no_fabricated_claims(fake_claim_html)
    print(f"Fabricated endorsement caught: {not ok_claim}")
    assert not ok_claim

    print("EditorialGovernanceEngine self-test PASSED!")
