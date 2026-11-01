"""
Unit tests for Original Research & Evidence System and Section 7 compliance invariants.
"""

import unittest
import sys
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.evidence_system import ResearchEvidenceSystem, VALID_CLASSIFICATIONS

class TestEvidenceSystem(unittest.TestCase):
    def setUp(self):
        self.res = ResearchEvidenceSystem()

    def test_01_first_evidence_file_exists_and_valid(self):
        """Verify TOPIC-001 evidence file exists and passes all validation checks."""
        filename = "TOPIC-001-cursor-vs-copilot.json"
        data = self.res.load_evidence_file(filename)
        self.assertEqual(data["evidence_file_id"], "EVID-TOPIC-001")
        is_valid, errors = self.res.validate_evidence_record(data)
        self.assertTrue(is_valid, f"Validation errors in {filename}: {errors}")
        self.assertEqual(len(errors), 0)

    def test_02_evidence_classification_strictly_controlled(self):
        """Verify classification must be one of A, B, or C."""
        valid_classifications = ["A. Hands-on tested", "B. Research-based", "C. Editorial analysis"]
        self.assertEqual(VALID_CLASSIFICATIONS, valid_classifications)

        bad_record = {
            "article_topic": "Test",
            "evidence_classification": "D. Speculative hearsay"
        }
        is_valid, errors = self.res.validate_evidence_record(bad_record)
        self.assertFalse(is_valid)
        self.assertTrue(any("Invalid evidence classification" in e for e in errors))

    def test_03_hands_on_classification_requires_environment(self):
        """Verify 'A. Hands-on tested' strictly requires hardware/testing environment specs."""
        hands_on_record = {
            "article_topic": "Hands-on Benchmark",
            "target_audience": "Developers",
            "search_intent": "Informational",
            "selected_keywords": ["test"],
            "competitor_gap_findings": "gap",
            "official_sources": ["docs"],
            "source_urls": ["https://example.com"],
            "source_publication_update_dates": "2026",
            "actual_verification_date": "2026",
            "product_versions": "1.0",
            "pricing_evidence": "$10",
            "research_methodology": "testing",
            "original_contribution": "data",
            "internal_links": ["/"],
            "claims_requiring_extra_verification": "none",
            "evidence_classification": "A. Hands-on tested"
            # Missing hands_on_testing_environment
        }
        is_valid, errors = self.res.validate_evidence_record(hands_on_record)
        self.assertFalse(is_valid)
        self.assertTrue(any("hands_on_testing_environment" in e for e in errors))

    def test_04_prohibited_fabrications_blocked(self):
        """Verify fake benchmarks and fake testimonials are strictly blocked."""
        fake_record = {
            "article_topic": "Fake Benchmark",
            "target_audience": "Developers",
            "search_intent": "Informational",
            "selected_keywords": ["test"],
            "competitor_gap_findings": "gap",
            "official_sources": ["docs"],
            "source_urls": ["https://example.com"],
            "source_publication_update_dates": "2026",
            "actual_verification_date": "2026",
            "product_versions": "1.0",
            "pricing_evidence": "$10",
            "research_methodology": "We tested this on 500 developers in our secret benchmark",
            "original_contribution": "data",
            "internal_links": ["/"],
            "claims_requiring_extra_verification": "none",
            "evidence_classification": "B. Research-based"
        }
        is_valid, errors = self.res.validate_evidence_record(fake_record)
        self.assertFalse(is_valid)
        self.assertTrue(any("Fabrication Violation" in e for e in errors))

    def test_05_distinction_guard_present(self):
        """Verify verified facts, estimates, and opinions are distinguished in sample evidence."""
        data = self.res.load_evidence_file("TOPIC-001-cursor-vs-copilot.json")
        distinction = data.get("distinction_guard", {})
        self.assertIn("verified_facts", distinction)
        self.assertIn("estimates", distinction)
        self.assertIn("expert_interpretation", distinction)
        self.assertIn("opinions", distinction)

if __name__ == "__main__":
    unittest.main()

