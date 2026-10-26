import os
import re
import json
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestStage33CatalogExpansion(unittest.TestCase):
    """
    Stage 3.3 Regression Test Suite:
    Validates competitor catalog expansion, popular products ranking,
    multi-layer catalog consistency, quarantine isolation, zero secret leaks,
    and commercial copy compliance across all 49 tools and 66 HTML routes.
    """

    @classmethod
    def setUpClass(cls):
        cls.catalog_path = os.path.join(REPO_ROOT, "scripts", "tools_catalog.json")
        with open(cls.catalog_path, "r", encoding="utf-8") as f:
            cls.catalog = json.load(f)

        cls.cart_js_path = os.path.join(REPO_ROOT, "assets", "cart.js")
        with open(cls.cart_js_path, "r", encoding="utf-8") as f:
            cls.cart_js = f.read()

        # Extract TOOLS_DATA from cart.js
        start_idx = cls.cart_js.find('TOOLS_DATA = {')
        brace_start = cls.cart_js.find('{', start_idx)
        brace_count = 0
        end_idx = -1
        for i in range(brace_start, len(cls.cart_js)):
            if cls.cart_js[i] == '{':
                brace_count += 1
            elif cls.cart_js[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break
        json_str = cls.cart_js[brace_start:end_idx]
        cls.cart_tools = json.loads(json_str)

        cls.index_path = os.path.join(REPO_ROOT, "index.html")
        with open(cls.index_path, "r", encoding="utf-8") as f:
            cls.index_html = f.read()

        cls.all_html_files = []
        for root, dirs, files in os.walk(REPO_ROOT):
            if any(p in root for p in [".git", "tests", "scratch"]):
                continue
            for file in files:
                if file.endswith(".html"):
                    cls.all_html_files.append(os.path.relpath(os.path.join(root, file), REPO_ROOT).replace("\\", "/"))
        cls.all_html_files.sort()

        cls.tool_files = [f for f in cls.all_html_files if f.startswith("tools/")]

    def test_01_catalog_and_cart_counts_match_49_tools(self):
        """Verify exactly 49 unique tool families in tools_catalog.json, cart.js, and tools/*.html."""
        self.assertEqual(len(self.catalog), 49, f"Expected 49 tools in tools_catalog.json, found {len(self.catalog)}")
        self.assertEqual(len(self.cart_tools), 49, f"Expected 49 tools in cart.js TOOLS_DATA, found {len(self.cart_tools)}")
        self.assertEqual(len(self.tool_files), 49, f"Expected 49 tool HTML pages, found {len(self.tool_files)}")
        self.assertEqual(len(self.all_html_files), 66, f"Expected 66 total HTML files, found {len(self.all_html_files)}")

        # Verify all slugs match 1-to-1
        catalog_slugs = set(self.catalog.keys())
        cart_slugs = set(self.cart_tools.keys())
        tool_page_slugs = {f.replace("tools/", "").replace(".html", "") for f in self.tool_files}

        self.assertEqual(catalog_slugs, cart_slugs, "Slug mismatch between tools_catalog.json and cart.js")
        self.assertEqual(catalog_slugs, tool_page_slugs, "Slug mismatch between tools_catalog.json and tools/*.html")

    def test_02_13_new_verified_tools_present(self):
        """Verify all 13 approved competitor expansion tools are present."""
        expected_new_tools = [
            "heygen-ai", "gamma-app", "n8n-automation", "vidiq-boost", "coursera-plus",
            "google-ai-ultra", "lovable-ai", "spotify-premium", "microsoft-office-365",
            "windows-11-pro", "prime-video", "tradingview-pro", "turnitin-student"
        ]
        for slug in expected_new_tools:
            self.assertIn(slug, self.catalog, f"Missing {slug} in tools_catalog.json")
            self.assertIn(slug, self.cart_tools, f"Missing {slug} in cart.js")
            tool_html_path = os.path.join(REPO_ROOT, "tools", f"{slug}.html")
            self.assertTrue(os.path.exists(tool_html_path), f"Missing HTML page for {slug}")

    def test_03_zero_price_discrepancies_across_catalog_and_pages(self):
        """Verify starting PKR price in catalog matches the detail page and cart."""
        for slug, data in self.catalog.items():
            pkr_price = data.get("starting_price_pkr")
            self.assertIsNotNone(pkr_price, f"{slug} missing starting_price_pkr in catalog")

            # Check cart.js starting price
            cart_item = self.cart_tools[slug]
            cart_pkr = cart_item.get("starting_price_pkr") or (cart_item.get("plans")[0]["price_pkr"] if cart_item.get("plans") else None)
            self.assertEqual(pkr_price, cart_pkr, f"Price mismatch for {slug}: catalog {pkr_price} vs cart {cart_pkr}")

            # Check tool detail page contains PKR price
            page_path = os.path.join(REPO_ROOT, "tools", f"{slug}.html")
            with open(page_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(f"Rs. {pkr_price:,}", content, f"Formatted price Rs. {pkr_price:,} missing from {slug}.html")

    def test_04_popularity_ranking_metadata_and_integrity(self):
        """Verify popularity scores (0-100), ranks (1-49), and top-ranked tools."""
        ranks_seen = set()
        for slug, data in self.catalog.items():
            score = data.get("popularity_score")
            rank = data.get("popularity_rank")
            self.assertIsNotNone(score, f"{slug} missing popularity_score")
            self.assertIsNotNone(rank, f"{slug} missing popularity_rank")
            self.assertTrue(0 <= score <= 100, f"{slug} popularity score out of range: {score}")
            self.assertTrue(1 <= rank <= 49, f"{slug} popularity rank out of range: {rank}")
            self.assertNotIn(rank, ranks_seen, f"Duplicate popularity rank: {rank}")
            ranks_seen.add(rank)

        self.assertEqual(len(ranks_seen), 49, "Every tool must have a distinct popularity rank from 1 to 49")

        # Top 3 should be high demand market leaders
        top_1 = [s for s, d in self.catalog.items() if d.get("popularity_rank") == 1][0]
        top_2 = [s for s, d in self.catalog.items() if d.get("popularity_rank") == 2][0]
        top_3 = [s for s, d in self.catalog.items() if d.get("popularity_rank") == 3][0]
        self.assertEqual(top_1, "chatgpt-plus")
        self.assertEqual(top_2, "claude-pro")
        self.assertEqual(top_3, "canva-pro")

    def test_05_quarantined_products_strictly_absent_from_public_site(self):
        """Verify unverified candidates (Ideogram, PlayHT, Jasper, etc.) are NOT in catalog or public pages."""
        quarantined_slugs = [
            "ideogram", "ideogram-ai", "playht", "play-ht", "jasper", "jasper-ai",
            "wordai", "word-ai", "dzine", "storyblocks", "helium-10", "helium10",
            "success-ai", "all-in-one-portal", "ai-portal"
        ]
        for q in quarantined_slugs:
            self.assertNotIn(q, self.catalog, f"Quarantined item '{q}' found in tools_catalog.json")
            self.assertNotIn(q, self.cart_tools, f"Quarantined item '{q}' found in cart.js")
            self.assertFalse(os.path.exists(os.path.join(REPO_ROOT, "tools", f"{q}.html")), f"Quarantined page exists: tools/{q}.html")

    def test_06_zero_wholesale_cost_or_supplier_leaks(self):
        """Ensure no USDT costs, supplier names, or private ledger keys exist in public files."""
        forbidden_strings = [
            "wholesale_price", "cost_usd", "bunnytoolsbot", "fat bunny hub",
            "reconciliation_ledger", "SRC-"
        ]
        public_exts = (".html", ".js", ".json", ".xml", ".txt")
        for root, dirs, files in os.walk(REPO_ROOT):
            if any(p in root for p in [".git", "tests", "scratch"]):
                continue
            for f in files:
                if f.endswith(public_exts):
                    path = os.path.join(root, f)
                    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read()
                    for s in forbidden_strings:
                        self.assertNotIn(s, content, f"Leak of private token '{s}' detected in public file: {path}")

    def test_07_commercial_policy_uniformity(self):
        """Verify 15-min delivery is a target, 30-day warranty is replacement-only, and no 24/7 support claims."""
        for tool_page in self.tool_files:
            path = os.path.join(REPO_ROOT, tool_page)
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()

            # Delivery target
            self.assertIn("15", c, f"Missing 15-minute target in {tool_page}")
            self.assertNotIn("15-minute delivery guarantee", c.lower(), f"Unsubstantiated guarantee in {tool_page}")
            self.assertNotIn("guaranteed 15 minute", c.lower(), f"Unsubstantiated guarantee in {tool_page}")

            # 30-day warranty
            self.assertIn("30-Day", c, f"Missing 30-day warranty in {tool_page}")
            self.assertIn("Replacement Warranty", c, f"Warranty must be replacement-only in {tool_page}")

            # Variable WhatsApp
            self.assertNotIn("24/7 live support", c.lower(), f"24/7 claim found in {tool_page}")
            self.assertNotIn("24/7 support", c.lower(), f"24/7 claim found in {tool_page}")

            # Independent reseller notice
            self.assertIn("Independent Reseller Notice", c, f"Missing reseller notice in {tool_page}")

    def test_08_feeds_and_sitemap_sync(self):
        """Verify sitemap (65 URLs) and feeds (49 items each) are fully synchronized and valid XML."""
        # Sitemap
        sitemap_tree = ET.parse(os.path.join(REPO_ROOT, "sitemap.xml"))
        sitemap_locs = [e.text for e in sitemap_tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        self.assertEqual(len(sitemap_locs), 65, f"Expected 65 URLs in sitemap, found {len(sitemap_locs)}")

        # RSS feed
        feed_tree = ET.parse(os.path.join(REPO_ROOT, "feed.xml"))
        feed_items = feed_tree.findall(".//item")
        self.assertEqual(len(feed_items), 49, f"Expected 49 items in feed.xml, found {len(feed_items)}")

        # Merchant feed
        merchant_tree = ET.parse(os.path.join(REPO_ROOT, "merchant_feed.xml"))
        merchant_items = merchant_tree.findall(".//item")
        self.assertEqual(len(merchant_items), 49, f"Expected 49 items in merchant_feed.xml, found {len(merchant_items)}")

if __name__ == "__main__":
    unittest.main()
