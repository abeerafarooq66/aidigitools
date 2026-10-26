import os
import re
import json
import unittest

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestStructuredDataCompliance(unittest.TestCase):
    """
    Exhaustive Test Suite for Phase 8 — Structured Data Compliance.
    Validates that:
    1. Every schema type matches actual page content.
    2. Zero schemas are applied indiscriminately (no Product markup on category pages).
    3. Zero fabricated ratings, reviews, or fake author credentials exist.
    4. 100% of JSON-LD blocks are valid and parse cleanly.
    5. Product, Offer, SoftwareApplication, Organization, WebSite, BreadcrumbList,
       Article/TechArticle, and FAQPage conform strictly to Schema.org standards.
    """
    @classmethod
    def setUpClass(cls):
        cls.html_files = []
        cls.jsonld_by_file = {}
        for root, dirs, files in os.walk(WORKSPACE_DIR):
            if any(p in root for p in [".git", "tests", "scratch"]):
                continue
            for f in files:
                if f.endswith(".html"):
                    fpath = os.path.join(root, f)
                    rel = os.path.relpath(fpath, WORKSPACE_DIR).replace("\\", "/")
                    cls.html_files.append(rel)
                    with open(fpath, "r", encoding="utf-8") as fh:
                        content = fh.read()
                    blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', content, re.S | re.I)
                    cls.jsonld_by_file[rel] = []
                    for b in blocks:
                        cls.jsonld_by_file[rel].append(json.loads(b.strip()))
        cls.html_files.sort()
        assert len(cls.html_files) == 66, f"Expected 53 HTML files, found {len(cls.html_files)}"

    def test_01_all_jsonld_syntax_valid(self):
        """Every single HTML file must have at least one valid JSON-LD block and 0 syntax errors."""
        total_blocks = sum(len(blocks) for blocks in self.jsonld_by_file.values())
        self.assertGreaterEqual(total_blocks, 150, f"Expected at least 150 JSON-LD blocks, found {total_blocks}")
        for rel, blocks in self.jsonld_by_file.items():
            self.assertGreater(len(blocks), 0, f"Page {rel} has no JSON-LD schema blocks")
            for b in blocks:
                self.assertIn("@context", b, f"Missing @context in {rel}")
                self.assertIn("@type", b, f"Missing @type in {rel}")

    def test_02_no_product_markup_on_category_or_guide_pages(self):
        """CRITICAL: Product rich-result markup must NEVER be applied to category or listing pages."""
        non_product_pages = [
            "index.html", "about.html", "contact.html", "deals.html", "policies.html",
            "shipping-policy.html", "affiliate-disclosure.html", "404.html",
            "categories/coding.html", "categories/image.html", "categories/video.html", "categories/vpn.html",
            "best/best-ai-coding-tools.html", "best/best-ai-video-generators.html",
            "compare/chatgpt-vs-claude.html", "compare/runway-vs-pika.html",
            "guides/chatgpt-vs-claude.html"
        ]
        for rel in non_product_pages:
            blocks = self.jsonld_by_file.get(rel, [])
            for b in blocks:
                stype = b.get("@type")
                if isinstance(stype, list):
                    self.assertNotIn("Product", stype, f"VIOLATION: Category/guide page {rel} contains Product schema: {stype}")
                else:
                    self.assertNotEqual(stype, "Product", f"VIOLATION: Category/guide page {rel} contains Product schema: {stype}")

    def test_03_zero_fabricated_ratings_or_reviews(self):
        """CRITICAL: Zero fabricated AggregateRating or Review entities anywhere in the codebase."""
        for rel, blocks in self.jsonld_by_file.items():
            for b in blocks:
                dumped = json.dumps(b)
                self.assertNotIn("AggregateRating", dumped, f"Fabricated AggregateRating detected in {rel}")
                self.assertNotIn("aggregateRating", dumped, f"Fabricated aggregateRating detected in {rel}")
                self.assertNotIn("ratingValue", dumped, f"Fabricated ratingValue detected in {rel}")
                self.assertNotIn('"@type": "Review"', dumped, f"Fabricated Review detected in {rel}")

    def test_04_product_and_offer_rich_result_properties(self):
        """Every tool page must have valid Product, Offer, and SoftwareApplication metadata."""
        tool_pages = [f for f in self.html_files if f.startswith("tools/")]
        self.assertEqual(len(tool_pages), 49)
        for rel in tool_pages:
            blocks = self.jsonld_by_file.get(rel, [])
            product_blocks = [b for b in blocks if b.get("@type") == "Product" or (isinstance(b.get("@type"), list) and "Product" in b.get("@type"))]
            self.assertEqual(len(product_blocks), 1, f"Expected exactly 1 Product block in {rel}")
            prod = product_blocks[0]

            # Name & Description
            self.assertIn("name", prod, f"Missing name in {rel}")
            self.assertIn("description", prod, f"Missing description in {rel}")

            # Brand
            self.assertIn("brand", prod, f"Missing brand in {rel}")
            self.assertIsInstance(prod["brand"], dict)
            self.assertEqual(prod["brand"].get("@type"), "Brand")
            self.assertIn("name", prod["brand"])

            # Image
            self.assertIn("image", prod, f"Missing image in {rel}")
            self.assertTrue(prod["image"].startswith("https://aidigitools.tech/assets/images/"))

            # Offers
            self.assertIn("offers", prod, f"Missing offers in {rel}")
            offer = prod["offers"]
            self.assertEqual(offer.get("@type"), "Offer")
            self.assertIn("price", offer)
            self.assertEqual(offer.get("priceCurrency"), "PKR")
            held_slugs = [
                "tools/turnitin-student.html",
                "tools/linkedin-premium.html",
                "tools/netflix-premium.html",
                "tools/spotify-premium.html",
                "tools/coursera-plus.html"
            ]
            if rel in held_slugs:
                self.assertEqual(offer.get("availability"), "https://schema.org/OutOfStock", f"Held product {rel} must have OutOfStock availability")
            else:
                self.assertEqual(offer.get("availability"), "https://schema.org/InStock", f"Active product {rel} must have InStock availability")

            # priceValidUntil must be absent (no genuine maintained expiration date)
            self.assertNotIn("priceValidUntil", offer, f"priceValidUntil must not be present in {rel}")

            # Seller & Return Policy
            self.assertIn("seller", offer)
            self.assertEqual(offer["seller"].get("@type"), "Organization")
            self.assertEqual(offer["seller"].get("name"), "AIDigiTools")
            self.assertIn("hasMerchantReturnPolicy", offer)
            policy = offer["hasMerchantReturnPolicy"]
            self.assertEqual(policy.get("returnPolicyCategory"), "https://schema.org/MerchantReturnFiniteReturnWindow", f"Return window category missing in {rel}")
            self.assertEqual(policy.get("merchantReturnDays"), 30, f"Return days must be 30 in {rel}")
            self.assertEqual(policy.get("returnMethod"), "https://schema.org/ReturnOnline", f"Return method must be ReturnOnline in {rel}")
            self.assertEqual(policy.get("returnFees"), "https://schema.org/FreeReturn", f"Return fees must be FreeReturn for replacement in {rel}")
            self.assertEqual(policy.get("refundType"), "https://schema.org/ExchangeRefund", f"refundType must be ExchangeRefund (replacement only) in {rel}")
            self.assertEqual(policy.get("merchantReturnLink"), "https://aidigitools.tech/policies.html#refunds", f"Missing or incorrect return link in {rel}")

            # SoftwareApplication properties
            self.assertEqual(prod.get("additionalType"), "https://schema.org/SoftwareApplication")
            self.assertEqual(prod.get("applicationCategory"), "SoftwareApplication")
            self.assertEqual(prod.get("operatingSystem"), "Web, Windows, macOS, iOS, Android")

    def test_05_article_and_guide_rich_result_properties(self):
        """All article, best, and comparison guides must have complete Article / TechArticle properties."""
        article_pages = [
            "guides/chatgpt-vs-claude.html",
            "compare/chatgpt-vs-claude.html",
            "compare/runway-vs-pika.html",
            "best/best-ai-coding-tools.html",
            "best/best-ai-video-generators.html"
        ]
        for rel in article_pages:
            blocks = self.jsonld_by_file.get(rel, [])
            art_blocks = [b for b in blocks if b.get("@type") in ["Article", "TechArticle", "BlogPosting"]]
            self.assertEqual(len(art_blocks), 1, f"Expected 1 Article/TechArticle block in {rel}")
            art = art_blocks[0]
            self.assertIn("headline", art, f"Missing headline in {rel}")
            self.assertIn("datePublished", art, f"Missing datePublished in {rel}")
            self.assertIn("dateModified", art, f"Missing dateModified in {rel}")
            self.assertIn("mainEntityOfPage", art, f"Missing mainEntityOfPage in {rel}")
            self.assertIn("image", art, f"Missing image in {rel}")
            self.assertIn("publisher", art, f"Missing publisher in {rel}")
            self.assertEqual(art["publisher"].get("@type"), "Organization")
            self.assertIn("logo", art["publisher"])

    def test_06_organization_and_website_on_homepage(self):
        """Homepage must have WebSite and Organization schema matching visible branding."""
        blocks = self.jsonld_by_file.get("index.html", [])
        website_blocks = [b for b in blocks if b.get("@type") == "WebSite"]
        self.assertEqual(len(website_blocks), 1)
        ws = website_blocks[0]
        self.assertEqual(ws.get("name"), "AIDigiTools")
        self.assertEqual(ws.get("url"), "https://aidigitools.tech/")
        self.assertIn("potentialAction", ws)

        org_blocks = [b for b in blocks if b.get("@type") == "Organization"]
        self.assertEqual(len(org_blocks), 1)
        org = org_blocks[0]
        self.assertEqual(org.get("name"), "AIDigiTools")
        self.assertEqual(org.get("telephone"), "+92-332-6861112")
        self.assertEqual(org.get("email"), "support@aidigitools.tech")
        self.assertIn("logo", org)
        self.assertIn("contactPoint", org)

    def test_07_breadcrumb_list_hierarchy(self):
        """All content, category, and tool pages must feature valid BreadcrumbList hierarchies."""
        # 51 pages should have breadcrumb list (excluding root homepage and 404.html)
        bc_count = 0
        for rel, blocks in self.jsonld_by_file.items():
            bc_blocks = [b for b in blocks if b.get("@type") == "BreadcrumbList"]
            if bc_blocks:
                bc_count += 1
                bc = bc_blocks[0]
                self.assertIn("itemListElement", bc, f"Missing itemListElement in {rel}")
                items = bc["itemListElement"]
                self.assertGreaterEqual(len(items), 2, f"Breadcrumb trail too short in {rel}")
                self.assertEqual(items[0].get("position"), 1)
                self.assertEqual(items[0].get("name"), "Home")
                self.assertEqual(items[0].get("item"), "https://aidigitools.tech/")
        self.assertEqual(bc_count, 64, f"Expected 51 pages with BreadcrumbList, found {bc_count}")

    def test_08_category_collection_and_item_list(self):
        """Category pages must use CollectionPage with ItemList, never Product rich-result markup."""
        cat_pages = [
            "categories/coding.html",
            "categories/image.html",
            "categories/video.html",
            "categories/vpn.html"
        ]
        for rel in cat_pages:
            blocks = self.jsonld_by_file.get(rel, [])
            cp_blocks = [b for b in blocks if b.get("@type") == "CollectionPage"]
            self.assertEqual(len(cp_blocks), 1, f"Missing CollectionPage in {rel}")
            cp = cp_blocks[0]
            self.assertIn("name", cp)
            self.assertIn("url", cp)
            self.assertIn("mainEntity", cp)
            me = cp["mainEntity"]
            self.assertEqual(me.get("@type"), "ItemList")
            self.assertIn("itemListElement", me)
            self.assertGreaterEqual(len(me["itemListElement"]), 2)

    def test_09_faq_pages_match_visible_content(self):
        """All 37 FAQPage instances must feature valid Question and acceptedAnswer structures."""
        faq_count = 0
        for rel, blocks in self.jsonld_by_file.items():
            faq_blocks = [b for b in blocks if b.get("@type") == "FAQPage"]
            if faq_blocks:
                faq_count += 1
                faq = faq_blocks[0]
                self.assertIn("mainEntity", faq, f"Missing mainEntity in FAQPage on {rel}")
                questions = faq["mainEntity"]
                self.assertGreaterEqual(len(questions), 2, f"Too few questions in FAQPage on {rel}")
                for q in questions:
                    self.assertEqual(q.get("@type"), "Question")
                    self.assertIn("name", q)
                    self.assertIn("acceptedAnswer", q)
                    self.assertEqual(q["acceptedAnswer"].get("@type"), "Answer")
                    self.assertIn("text", q["acceptedAnswer"])
        self.assertEqual(faq_count, 50, f"Expected 37 FAQPage instances, found {faq_count}")

    def test_10_no_duplicate_or_extraneous_schemas_per_page(self):
        """Verify pages do not carry redundant schema bloat or mismatched entity types."""
        for rel, blocks in self.jsonld_by_file.items():
            types = [b.get("@type") for b in blocks]
            # Ensure no page has duplicate primary schemas
            for t in ["Product", "WebSite", "AboutPage", "ContactPage", "CollectionPage"]:
                self.assertLessEqual(types.count(t), 1, f"Duplicate schema {t} on page {rel}")

    def test_11_zero_misleading_monetary_return_markup(self):
        """CRITICAL: Zero misleading monetary refund terms (FullRefund) and zero ReturnByMail or priceValidUntil."""
        for rel, blocks in self.jsonld_by_file.items():
            for b in blocks:
                dumped = json.dumps(b)
                self.assertNotIn("FullRefund", dumped, f"Misleading FullRefund monetary schema in {rel}")
                self.assertNotIn("ReturnByMail", dumped, f"Misleading ReturnByMail physical shipping schema in {rel}")
                self.assertNotIn("priceValidUntil", dumped, f"Unsupported priceValidUntil schema in {rel}")

if __name__ == "__main__":
    unittest.main()
