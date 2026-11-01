"""
Unit tests for Trust, Transparency & Editorial Governance Engine (Section 11 of Master Architecture Charter).
"""

import unittest
import sys
import re
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.editorial_governance import EditorialGovernanceEngine

ROOT_DIR = Path(__file__).resolve().parent.parent

class TestEditorialGovernance(unittest.TestCase):
    def setUp(self):
        self.engine = EditorialGovernanceEngine()

    def test_registered_authors_authenticity(self):
        """All authors in author_registry.json must be verified human identities."""
        authors = self.engine.get_registered_authors()
        self.assertGreaterEqual(len(authors), 2)
        
        for slug, author in authors.items():
            self.assertTrue(author.get("verified_identity"), f"Author {slug} must have verified_identity=True")
            self.assertTrue(author.get("is_human"), f"Author {slug} must be a real human (is_human=True)")
            self.assertFalse(author.get("is_fictional", False), f"Author {slug} must not be fictional")
            self.assertIn("Islamabad", author.get("location", ""))
            self.assertTrue(len(author.get("bio", "")) > 30, f"Author {slug} must have a detailed bio")

    def test_author_validation_valid_and_invalid(self):
        """Valid registered authors must pass, while unknown/invented personas must fail."""
        # Valid author
        ok, author = self.engine.validate_author("abeera-farooq")
        self.assertTrue(ok)
        self.assertEqual(author["name"], "Abeera Farooq")

        # Desk author
        ok_desk, desk = self.engine.validate_author("aidigitools-editorial")
        self.assertTrue(ok_desk)
        self.assertEqual(desk["name"], "AIDigiTools Technical Editorial Desk")

        # Fake / unverified author
        ok_fake, fake = self.engine.validate_author("invented-expert-phd")
        self.assertFalse(ok_fake)
        self.assertIsNone(fake)

    def test_human_review_claim_enforcement(self):
        """Claiming human editorial review requires a registered human reviewer and valid ISO review date."""
        # Uncredited human review claim in text
        uncredited_html = "<p>This guide was reviewed by a human editor for accuracy.</p>"
        valid, viols = self.engine.validate_human_review_claim(uncredited_html, metadata={})
        self.assertFalse(valid)
        self.assertTrue(any("no 'reviewed_by' author slug" in v for v in viols))

        # Human review with invalid reviewer
        invalid_reviewer_meta = {
            "human_reviewed": True,
            "reviewed_by": "unregistered-reviewer-x",
            "review_date": "2026-11-01"
        }
        valid, viols = self.engine.validate_human_review_claim("<p>Test content</p>", metadata=invalid_reviewer_meta)
        self.assertFalse(valid)
        self.assertTrue(any("not registered as a verified human editor" in v for v in viols))

        # Compliant human review
        compliant_meta = {
            "human_reviewed": True,
            "reviewed_by": "abeera-farooq",
            "review_date": "2026-11-01"
        }
        valid, viols = self.engine.validate_human_review_claim("<p>Reviewed by a human editor.</p>", metadata=compliant_meta)
        self.assertTrue(valid)
        self.assertEqual(len(viols), 0)

    def test_ai_assistance_transparency_enforcement(self):
        """If content is flagged as AI-assisted, a visible transparency notice must be present."""
        # AI assisted but no notice in HTML
        ai_meta = {"ai_assisted": True}
        html_without_notice = "<p>Here is an in-depth breakdown of Claude vs ChatGPT.</p>"
        valid, viols = self.engine.validate_ai_transparency(html_without_notice, metadata=ai_meta)
        self.assertFalse(valid)
        self.assertTrue(any("lacks a visible transparency notice" in v for v in viols))

        # AI assisted with compliant notice
        html_with_notice = """
        <div class="ai-transparency-badge">
            <p>Transparency: Synthesized with AI research assistance and verified by our editorial desk.</p>
        </div>
        <p>Here is an in-depth breakdown of Claude vs ChatGPT.</p>
        """
        valid, viols = self.engine.validate_ai_transparency(html_with_notice, metadata=ai_meta)
        self.assertTrue(valid)
        self.assertEqual(len(viols), 0)

    def test_rel_sponsored_on_affiliate_links(self):
        """Affiliate and compensated links must have rel='sponsored' per Google Search guidelines."""
        # Missing rel="sponsored"
        bad_link_html = '<p>Check out <a href="https://vendor.com/?ref=aidigitools_pk">Vendor Tool</a></p>'
        valid, viols = self.engine.validate_affiliate_and_sponsored_links(bad_link_html)
        self.assertFalse(valid)
        self.assertTrue(any("missing rel='sponsored'" in v for v in viols))

        # With rel="nofollow" only (missing sponsored)
        bad_rel_html = '<p>Check out <a href="https://shareasale.com/r.cfm?b=123" rel="nofollow">Vendor</a></p>'
        valid, viols = self.engine.validate_affiliate_and_sponsored_links(bad_rel_html)
        self.assertFalse(valid)
        self.assertTrue(any("missing mandatory 'sponsored' token" in v for v in viols))

        # Compliant link with rel="nofollow sponsored"
        compliant_link_html = '<p>Check out <a href="https://vendor.com/?ref=aidigitools_pk" rel="nofollow sponsored">Vendor Tool</a></p>'
        valid, viols = self.engine.validate_affiliate_and_sponsored_links(compliant_link_html)
        self.assertTrue(valid)
        self.assertEqual(len(viols), 0)

    def test_fabricated_claims_and_endorsements_blocked(self):
        """Reject fabricated endorsements, fake rankings, or false partnership claims."""
        bad_claims = [
            "<p>AIDigiTools was officially endorsed by OpenAI in 2026.</p>",
            "<p>We were voted #1 in the world by MIT for subscription brokering.</p>",
            "<p>AIDigiTools is the exclusive partner authorized by Anthropic in Pakistan.</p>"
        ]
        for bad_html in bad_claims:
            valid, viols = self.engine.validate_no_fabricated_claims(bad_html)
            self.assertFalse(valid)
            self.assertTrue(any("Fabricated Claim Violation" in v for v in viols))

    def test_editorial_guidelines_page_integrity(self):
        """Verify the public about.html page complies with all on-page SEO & Section 11 editorial governance standards."""
        page_path = ROOT_DIR / "about.html"
        self.assertTrue(page_path.exists(), "about.html must exist")

        with open(page_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Title check (30-65 chars)
        title_match = re.search(r"<title>(.*?)</title>", html)
        self.assertIsNotNone(title_match)
        title = title_match.group(1).replace("&amp;", "&")
        self.assertTrue(30 <= len(title) <= 65, f"Title length {len(title)} not in [30, 65]")

        # Meta description check (70-165 chars)
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.I)
        self.assertIsNotNone(desc_match)
        desc = desc_match.group(1).replace("&amp;", "&")
        self.assertTrue(70 <= len(desc) <= 165, f"Meta desc length {len(desc)} not in [70, 165]")

        # Single H1 check
        h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I)
        self.assertEqual(len(h1_matches), 1, "Exactly one <h1> tag required")

        # Quick answer block check (35-70 words)
        qa_match = re.search(r'<p\s+class=["\']quick-answer["\']>(.*?)</p>', html, re.DOTALL)
        self.assertIsNotNone(qa_match)
        qa_text = re.sub(r"<[^>]+>", " ", qa_match.group(1)).strip()
        words = len(qa_text.split())
        self.assertTrue(35 <= words <= 70, f"Quick answer word count {words} not in [35, 70]")

        # Mandatory Section 11 topics check
        required_topics = [
            "About the Editorial Team",
            "Editorial Guidelines",
            "Testing Methodology",
            "Fact-Checking Policy",
            "Content Corrections",
            "Commercial & Affiliate Disclosure",
            "AI Assistance Transparency",
            "Human Editorial Review Standard",
            "Contact & Support Operations Desk"
        ]
        html_decoded = html.replace("&amp;", "&").lower()
        for topic in required_topics:
            self.assertIn(topic.lower(), html_decoded, f"Missing mandatory Section 11 topic: {topic}")

        # Author and contact mentions
        self.assertIn("Abeera Farooq", html)
        self.assertIn("03326861112", html)
        self.assertIn("support@aidigitools.tech", html)
        self.assertIn("rel=\"canonical\" href=\"https://aidigitools.tech/about.html\"", html)

if __name__ == "__main__":
    unittest.main()
