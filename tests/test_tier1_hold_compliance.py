import os
import re
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class TestTier1HoldCompliance(unittest.TestCase):
    TIER1_SLUGS = [
        'turnitin-student',
        'linkedin-premium',
        'netflix-premium',
        'spotify-premium',
        'coursera-plus'
    ]

    def test_tier1_files_exist_and_retain_canonicals(self):
        """Assert all 5 products exist and retain valid canonical tags and titles."""
        for slug in self.TIER1_SLUGS:
            file_path = os.path.join(REPO_ROOT, 'tools', f"{slug}.html")
            self.assertTrue(os.path.exists(file_path), f"File missing: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            expected_canonical = f'<link rel="canonical" href="https://aidigitools.tech/tools/{slug}.html">'
            self.assertIn(expected_canonical, content, f"Canonical tag missing or incorrect in {slug}.html")

            # Check title exists
            self.assertRegex(content, r'<title>[^<]+</title>', f"Title tag missing in {slug}.html")

    def test_tier1_direct_orders_active_on_tool_pages(self):
        """Assert all 5 products have active direct ordering modal triggers and no hold banners."""
        for slug in self.TIER1_SLUGS:
            file_path = os.path.join(REPO_ROOT, 'tools', f"{slug}.html")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Quick order button for this slug must be present
            has_quick_order = f"openQuickOrderModal('{slug}')" in content or f'openQuickOrderModal("{slug}")' in content
            self.assertTrue(has_quick_order, f"openQuickOrderModal missing for {slug} in {slug}.html")

            # On-hold banner must NOT be present
            self.assertNotIn("Direct Orders Currently On Hold", content, f"Hold banner still present in {slug}.html")

            # Active orders accepted badge must be present
            has_accepted_badge = ("🟢 Orders Accepted" in content) or ('<span class="status-dot"></span> Orders Accepted' in content)
            self.assertTrue(has_accepted_badge, f"Orders accepted badge missing in {slug}.html")

            # Inquiry-only button must NOT be present
            self.assertNotIn("Inquire on WhatsApp for Current Availability", content, f"Inquiry button still present in {slug}.html")

    def test_tier1_index_html_direct_orders_active(self):
        """Assert index.html exposes direct quick-order triggers for all 5 products."""
        index_path = os.path.join(REPO_ROOT, 'index.html')
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for slug in self.TIER1_SLUGS:
            has_quick_order = f"openQuickOrderModal('{slug}')" in content or f'openQuickOrderModal("{slug}")' in content
            self.assertTrue(has_quick_order, f"Direct order button for {slug} missing in index.html")

    def test_cart_js_active_products_not_held(self):
        """Assert assets/cart.js does not block active products under HELD_PRODUCTS."""
        cart_path = os.path.join(REPO_ROOT, 'assets', 'cart.js')
        with open(cart_path, 'r', encoding='utf-8') as f:
            content = f.read()

        for slug in self.TIER1_SLUGS:
            # Match in HELD_PRODUCTS array specifically
            held_match = re.search(r'var HELD_PRODUCTS = \[(.*?)\];', content, re.DOTALL)
            if held_match:
                held_array_content = held_match.group(1)
                self.assertNotIn(f'"{slug}"', held_array_content, f"Active slug {slug} still held in cart.js")
                self.assertNotIn(f"'{slug}'", held_array_content, f"Active slug {slug} still held in cart.js")

    def test_sitemap_urls_count_and_retention(self):
        """Assert sitemap.xml retains at least 65 canonical URLs including all 5 active tools."""
        sitemap_path = os.path.join(REPO_ROOT, 'sitemap.xml')
        self.assertTrue(os.path.exists(sitemap_path), "sitemap.xml missing")

        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        urls = [elem.text.strip() for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]

        self.assertGreaterEqual(len(urls), 65, f"Expected at least 65 sitemap URLs, got {len(urls)}")
        for slug in self.TIER1_SLUGS:
            expected_url = f"https://aidigitools.tech/tools/{slug}.html"
            self.assertIn(expected_url, urls, f"Tool {expected_url} missing from sitemap.xml")

    def test_inflation_claims_purged_across_catalog(self):
        """Assert unverified inflation claims are purged across all tool pages."""
        tools_dir = os.path.join(REPO_ROOT, 'tools')
        banned_phrases = [
            'unconditional 30-day',
            'instant 15-minute delivery',
            'verified SLA terms',
            '365-day replacement guarantee',
            '365-day replacement warranty'
        ]

        for fname in os.listdir(tools_dir):
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(tools_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            for phrase in banned_phrases:
                self.assertNotIn(phrase.lower(), content, f"Banned phrase '{phrase}' found in {fname}")

    def test_reseller_notices_harmonized_across_all_tools(self):
        """Assert all 49 tools have harmonized reseller notice stating authorization is unverified."""
        tools_dir = os.path.join(REPO_ROOT, 'tools')
        tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]
        self.assertEqual(len(tool_files), 49, f"Expected 49 tools, found {len(tool_files)}")

        for fname in tool_files:
            fpath = os.path.join(tools_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            self.assertIn("Direct official resale authorization", content, f"Reseller notice missing in {fname}")
            self.assertIn("is unverified", content, f"Unverified clause missing in {fname}")

if __name__ == '__main__':
    unittest.main()
