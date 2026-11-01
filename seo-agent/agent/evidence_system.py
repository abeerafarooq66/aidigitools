"""
AIDigiTools — Original Research & Evidence System
Strictly implements Section 7 of Master Architecture Charter:
ORIGINAL RESEARCH AND EVIDENCE SYSTEM
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCE_DIR = ROOT_DIR / "data" / "research_evidence"

VALID_CLASSIFICATIONS = [
    "A. Hands-on tested",
    "B. Research-based",
    "C. Editorial analysis"
]

REQUIRED_EVIDENCE_FIELDS = [
    "article_topic",
    "target_audience",
    "search_intent",
    "selected_keywords",
    "competitor_gap_findings",
    "official_sources",
    "source_urls",
    "source_publication_update_dates",
    "actual_verification_date",
    "product_versions",
    "pricing_evidence",
    "research_methodology",
    "original_contribution",
    "internal_links",
    "claims_requiring_extra_verification",
    "evidence_classification"
]

PROHIBITED_FABRICATIONS = [
    "we tested this on 500 developers",
    "our in-house lab measured 99.9%",
    "in our secret benchmark",
    "our hands-on lab confirmed",
    "anonymous customer review:",
    "john doe from karachi said:",
]

class ResearchEvidenceSystem:
    def __init__(self, evidence_dir: Optional[Path] = None):
        self.evidence_dir = evidence_dir or EVIDENCE_DIR
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def validate_evidence_record(self, record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that an evidence record contains all 15 required fields,
        carries a valid classification, and contains zero fabricated claims.
        """
        errors = []

        # 1. Required fields check
        for field in REQUIRED_EVIDENCE_FIELDS:
            if field not in record or not record[field]:
                errors.append(f"Missing mandatory evidence field: '{field}'")

        # 2. Classification validation
        classification = record.get("evidence_classification", "")
        if classification not in VALID_CLASSIFICATIONS:
            errors.append(
                f"Invalid evidence classification: '{classification}'. "
                f"Must be one of: {VALID_CLASSIFICATIONS}"
            )

        # 3. Hands-on claim invariant:
        # If classified as "A. Hands-on tested", it MUST have an explicit tested_hardware or environment field
        if classification == "A. Hands-on tested":
            if not record.get("hands_on_testing_environment"):
                errors.append("Evidence claims 'A. Hands-on tested' but lacks explicit 'hands_on_testing_environment' specifications.")

        # 4. Prohibited fabrication scans
        record_str = json.dumps(record).lower()
        for fab in PROHIBITED_FABRICATIONS:
            if fab in record_str:
                errors.append(f"Fabrication Violation: Detected unverified benchmark or testimonial phrase: '{fab}'")

        is_valid = len(errors) == 0
        return is_valid, errors

    def save_evidence_file(self, filename: str, record: Dict[str, Any]) -> Path:
        """
        Validates and writes an evidence file to data/research_evidence/.
        """
        is_valid, errors = self.validate_evidence_record(record)
        if not is_valid:
            raise ValueError(f"Cannot save invalid evidence file '{filename}': {errors}")

        target_path = self.evidence_dir / filename
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        return target_path

    def load_evidence_file(self, filename: str) -> Dict[str, Any]:
        """
        Loads an existing evidence file.
        """
        target_path = self.evidence_dir / filename
        if not target_path.exists():
            raise FileNotFoundError(f"Evidence file missing: {target_path}")
        with open(target_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_all_evidence_files(self) -> List[str]:
        return [f.name for f in self.evidence_dir.glob("*.json")]

if __name__ == "__main__":
    res = ResearchEvidenceSystem()
    print(f"Research Evidence System initialized. Storage directory: {res.evidence_dir}")
    print(f"Total evidence files: {len(res.list_all_evidence_files())}")

