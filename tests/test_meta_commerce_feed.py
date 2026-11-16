"""
AIDigiTools — Meta Commerce & WhatsApp Business Feed Test Suite
==============================================================
Validates XML integrity, product counts, stock partitioning, and parity
for Meta Commerce Manager and WhatsApp Business Catalog integration.
"""

import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META_FEED_PATH = ROOT / "meta-product-feed.xml"
MERCHANT_FEED_PATH = ROOT / "merchant_feed.xml"
TOOLS_DIR = ROOT / "tools"
IMAGES_DIR = ROOT / "assets" / "images"

HELD_SLUGS = {
    "turnitin-student",
    "linkedin-premium",
    "netflix-premium",
    "spotify-premium",
    "coursera-plus",
    "claude-artifacts",
    "deepseek-pro"
}

class TestMetaCommerceFeed(unittest.TestCase):

    def setUp(self):
        self.assertTrue(META_FEED_PATH.exists(), "meta-product-feed.xml must exist")
        self.assertTrue(MERCHANT_FEED_PATH.exists(), "merchant_feed.xml must exist")
        self.meta_tree = ET.parse(META_FEED_PATH)
        self.merchant_tree = ET.parse(MERCHANT_FEED_PATH)
        self.ns = {"g": "http://base.google.com/ns/1.0"}

    def test_01_xml_validity_and_namespaces(self):
        """Verify XML is well-formed with standard Google/Meta namespace."""
        root = self.meta_tree.getroot()
        self.assertEqual(root.tag, "rss")
        self.assertEqual(root.get("version"), "2.0")
        channel = root.find("channel")
        self.assertIsNotNone(channel)
        self.assertIn("AIDigiTools", channel.find("title").text)
        self.assertEqual(channel.find("link").text, "https://aidigitools.tech")

    def test_02_total_product_count_matches_master_database(self):
        """Verify exactly 49 products exist in the Meta feed."""
        items = self.meta_tree.findall(".//item")
        self.assertEqual(len(items), 49, f"Expected 49 products in Meta feed, found {len(items)}")

    def test_03_stock_partitioning_policy_enforcement(self):
        """
        Verify that 42 active products are 'in_stock' and the 7 policy-held
        products are strictly designated as 'out_of_stock'.
        """
        items = self.meta_tree.findall(".//item")
        in_stock_count = 0
        out_of_stock_count = 0

        for item in items:
            item_id = item.find("g:id", self.ns).text
            avail = item.find("g:availability", self.ns).text
            slug = item_id.replace("aidigitools-", "")

            if slug in HELD_SLUGS:
                self.assertEqual(avail, "out_of_stock", f"Held product '{slug}' must be 'out_of_stock'")
                out_of_stock_count += 1
            else:
                self.assertEqual(avail, "in_stock", f"Active product '{slug}' must be 'in_stock'")
                in_stock_count += 1

        self.assertEqual(in_stock_count, 42)
        self.assertEqual(out_of_stock_count, 7)

    def test_04_mandatory_attributes_presence_and_format(self):
        """Verify all mandatory Meta Commerce attributes exist and are non-empty."""
        items = self.meta_tree.findall(".//item")
        for item in items:
            item_id = item.find("g:id", self.ns).text
            self.assertTrue(item_id.startswith("aidigitools-"))

            title = item.find("g:title", self.ns).text
            self.assertTrue(len(title) > 5)
            self.assertTrue("Plan in Pakistan" in title or "Subscription" in title)

            desc = item.find("g:description", self.ns).text
            self.assertTrue(len(desc) > 20)

            link = item.find("g:link", self.ns).text
            self.assertTrue(link.startswith("https://aidigitools.tech/tools/"))

            img = item.find("g:image_link", self.ns).text
            self.assertTrue(img.startswith("https://aidigitools.tech/assets/images/"))

            price = item.find("g:price", self.ns).text
            self.assertTrue(price.endswith(" PKR"))
            num_part = price.replace(" PKR", "")
            self.assertTrue(num_part.isdigit(), f"Price '{price}' must contain integer PKR amount")

            brand = item.find("g:brand", self.ns).text
            self.assertTrue(len(brand) > 0)

            condition = item.find("g:condition", self.ns).text
            self.assertEqual(condition, "new")

    def test_05_landing_pages_and_images_exist_locally(self):
        """Verify that every link and image_link resolves to an existing file in the repo."""
        items = self.meta_tree.findall(".//item")
        for item in items:
            slug = item.find("g:id", self.ns).text.replace("aidigitools-", "")

            # Tool landing page check
            tool_html = TOOLS_DIR / f"{slug}.html"
            self.assertTrue(tool_html.exists(), f"Landing page missing for slug: {slug}")

            # Product preview image check
            tool_img = IMAGES_DIR / f"{slug}.png"
            self.assertTrue(tool_img.exists(), f"Product image missing for slug: {slug}")

    def test_06_feed_parity_between_meta_and_merchant(self):
        """Verify parity between meta-product-feed.xml and merchant_feed.xml."""
        meta_items = self.meta_tree.findall(".//item")
        merchant_items = self.merchant_tree.findall(".//item")
        self.assertEqual(len(meta_items), len(merchant_items))

        meta_ids = [i.find("g:id", self.ns).text for i in meta_items]
        merchant_ids = [i.find("g:id", self.ns).text for i in merchant_items]
        self.assertEqual(meta_ids, merchant_ids)

if __name__ == "__main__":
    unittest.main()
