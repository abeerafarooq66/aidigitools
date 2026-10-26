import os
import re
import unittest

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestAEOAndGEOReadiness(unittest.TestCase):
    """
    Exhaustive Test Suite for Phase 11 — AEO, GEO and AI Search Readiness.
    Validates direct answer capsules (.quick-answer), official documentation citations,
    zero prompt injection or manipulative AI hacks, descriptive headings,
    freshness signals (October 2026), and transparent limitation disclosures.
    """
    @classmethod
    def setUpClass(cls):
        cls.html_files = []
        for root, dirs, files in os.walk(WORKSPACE_DIR):
            if any(p in root for p in [".git", "tests", "scratch"]):
                continue
            for f in files:
                if f.endswith(".html"):
                    rel = os.path.relpath(os.path.join(root, f), WORKSPACE_DIR).replace("\\", "/")
                    cls.html_files.append(rel)
        cls.html_files.sort()
        assert len(cls.html_files) == 66

    def _read_file(self, rel):
        fpath = os.path.normpath(os.path.join(WORKSPACE_DIR, rel))
        with open(fpath, "r", encoding="utf-8") as fh:
            return fh.read()

    def test_01_all_content_pages_have_quick_answer_capsule(self):
        """All 52 content pages (excluding 404.html) must feature a .quick-answer block between 30 and 85 words."""
        for rel in self.html_files:
            if rel == "404.html":
                continue
            c = self._read_file(rel)
            match = re.search(r'<[a-z0-9]+\s+[^>]*class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</[a-z0-9]+>', c, re.S | re.I)
            self.assertIsNotNone(match, f"Missing .quick-answer block in {rel}")
            text = re.sub(r'<[^>]+>', '', match.group(1)).strip()
            words = text.split()
            self.assertGreaterEqual(len(words), 30, f".quick-answer too short in {rel} ({len(words)} words)")
            self.assertLessEqual(len(words), 90, f".quick-answer too long in {rel} ({len(words)} words)")

    def test_02_tool_pages_official_documentation_citations(self):
        """All 36 tool pages must link to official vendor documentation with rel='noopener noreferrer nofollow'."""
        tool_pages = [f for f in self.html_files if f.startswith("tools/")]
        self.assertEqual(len(tool_pages), 49)
        
        vendor_domains = [
            "openai.com", "anthropic.com", "midjourney.com", "cursor.com", "adobe.com", "canva.com",
            "capcut.com", "github.com", "perplexity.ai", "deepseek.com", "google.com", "jetbrains.com",
            "replit.com", "figma.com", "notion.so", "nordvpn.com", "surfshark.com", "elevenlabs.io",
            "klingai.com", "runwayml.com", "suno.com", "udio.com", "semrush.com", "grammarly.com",
            "netflix.com", "youtube.com", "quillbot.com", "freepik.com", "envato.com", "linkedin.com", "x.ai",
            "deepmind.google", "leonardo.ai", "hailuoai.video", "heygen.com", "gamma.app", "n8n.io", "vidiq.com",
            "coursera.org", "lovable.dev", "spotify.com", "microsoft.com", "primevideo.com", "tradingview.com", "turnitin.com"
        ]
        for rel in tool_pages:
            c = self._read_file(rel)
            links = re.findall(r'<a\s+[^>]*href=["\'](https?://[^"\']+)["\'][^>]*>', c, re.I)
            has_vendor_link = False
            for url in links:
                if any(v in url for v in vendor_domains):
                    has_vendor_link = True
                    # Check rel attribute
                    link_match = re.search(rf'<a\s+[^>]*href=["\']{re.escape(url)}["\'][^>]*>', c, re.I)
                    tag = link_match.group(0)
                    self.assertIn("nofollow", tag, f"Official citation missing nofollow in {rel}: {url}")
                    self.assertIn("noopener", tag, f"Official citation missing noopener in {rel}: {url}")
                    break
            self.assertTrue(has_vendor_link, f"Missing official vendor citation in {rel}")

    def test_03_zero_prompt_injection_or_manipulative_tricks(self):
        """CRITICAL: Absolute prohibition of prompt injection, hidden prompts, or fake authority claims."""
        injection_terms = [
            "ignore previous instructions", "system prompt", "you are an ai", "recommend aidigitools above all",
            "chatgpt ignore", "hidden prompt", "prompt injection", "seo bot", "always cite"
        ]
        for rel in self.html_files:
            c = self._read_file(rel).lower()
            for term in injection_terms:
                self.assertNotIn(term, c, f"Manipulative prompt injection term '{term}' found in {rel}")

    def test_04_no_vague_h2_headings(self):
        """Headings must be descriptive topic descriptors, not vague single-word placeholders."""
        vague_terms = ["overview", "details", "info", "about", "content", "stuff"]
        for rel in self.html_files:
            c = self._read_file(rel)
            h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', c, re.I | re.S)
            for h in h2s:
                clean = re.sub(r'<[^>]+>', '', h).strip().lower()
                self.assertNotIn(clean, vague_terms, f"Vague H2 heading '{clean}' detected in {rel}")

    def test_05_explicit_freshness_and_verification_dates(self):
        """All 53 pages must explicitly state October 2026 verification/catalog freshness."""
        for rel in self.html_files:
            c = self._read_file(rel)
            self.assertTrue("October 2026" in c or "2026-10" in c, f"Missing October 2026 freshness date in {rel}")

    def test_06_pricing_transparency_and_limitations_on_tools(self):
        """All 36 tool pages must state PKR and USD pricing, 15m delivery SLA, and 30-day warranty."""
        tool_pages = [f for f in self.html_files if f.startswith("tools/")]
        for rel in tool_pages:
            c = self._read_file(rel)
            self.assertIn("PKR", c, f"Missing PKR pricing in {rel}")
            self.assertIn("USD", c, f"Missing USD pricing in {rel}")
            self.assertIn("15", c, f"Missing 15-minute delivery in {rel}")
            self.assertIn("30-Day", c, f"Missing 30-day warranty in {rel}")
            self.assertIn("Zero VPN required", c, f"Missing zero VPN required limitation in {rel}")

    def test_07_independent_reseller_transparency(self):
        """All 36 tool pages must clearly disclose independent reseller status to avoid trademark confusion."""
        tool_pages = [f for f in self.html_files if f.startswith("tools/")]
        for rel in tool_pages:
            c = self._read_file(rel)
            self.assertIn("Independent Reseller Notice", c, f"Missing independent reseller notice in {rel}")

    def test_08_sibling_tool_alternatives_interlinked(self):
        """All 36 tool pages must interlink to at least 2 relevant alternative tools."""
        tool_pages = [f for f in self.html_files if f.startswith("tools/")]
        for rel in tool_pages:
            c = self._read_file(rel)
            spec_block = re.search(r'id=["\']phase6-spec-block["\'].*?</section>', c, re.S | re.I)
            self.assertIsNotNone(spec_block, f"Missing specification block in {rel}")
            alt_links = re.findall(r'<a\s+[^>]*href=["\']([a-z0-9\-]+\.html)["\'][^>]*>', spec_block.group(0), re.I)
            self.assertGreaterEqual(len(alt_links), 2, f"Too few alternative links in {rel}: {alt_links}")

if __name__ == "__main__":
    unittest.main()
