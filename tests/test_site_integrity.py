import unittest
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from scripts.link_graph_checker import check_link_graph

ROOT = Path(__file__).resolve().parent.parent

class TestSiteIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.html_files = sorted([p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts) and p.name != "404.html"])
        cls.tool_files = sorted(list(ROOT.glob("tools/*.html")))
        cls.guide_files = sorted(list(ROOT.glob("guides/*.html")) + list(ROOT.glob("compare/*.html")) + list(ROOT.glob("best/*.html")))

    # --- Sitemap & Robots Integrity (1-5) ---
    def test_01_robots_txt_exists(self):
        robots = ROOT / "robots.txt"
        self.assertTrue(robots.is_file())
        content = robots.read_text(encoding="utf-8")
        self.assertIn("User-agent: *", content)
        self.assertIn("Sitemap: https://aidigitools.tech/sitemap.xml", content)

    def test_02_robots_allows_ai_crawlers(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("GPTBot", robots)
        self.assertIn("ClaudeBot", robots)
        self.assertIn("PerplexityBot", robots)

    def test_03_sitemap_xml_exists(self):
        sitemap = ROOT / "sitemap.xml"
        self.assertTrue(sitemap.is_file())

    def test_04_sitemap_xml_valid_syntax(self):
        sitemap = ROOT / "sitemap.xml"
        tree = ET.parse(sitemap)
        root = tree.getroot()
        self.assertIn("urlset", root.tag)

    def test_05_sitemap_contains_all_pages(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for hf in self.html_files:
            rel = hf.relative_to(ROOT).as_posix()
            if rel == "index.html":
                self.assertIn("https://aidigitools.tech/</loc>", sitemap)
            else:
                self.assertIn(f"https://aidigitools.tech/{rel}</loc>", sitemap)

    # --- LLMs.txt & Machine Knowledge (6-8) ---
    def test_06_llms_txt_exists(self):
        llms = ROOT / "llms.txt"
        self.assertTrue(llms.is_file())
        content = llms.read_text(encoding="utf-8")
        self.assertIn("AIDigiTools", content)
        self.assertIn("EasyPaisa", content)

    def test_07_llms_full_txt_exists(self):
        llms_full = ROOT / "llms-full.txt"
        self.assertTrue(llms_full.is_file())
        self.assertGreater(llms_full.stat().st_size, 500)

    def test_08_llms_txt_contains_all_tools(self):
        content = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("ChatGPT Plus", content)
        self.assertIn("Claude Pro", content)
        self.assertIn("Canva Pro", content)

    # --- Strict Link Graph & Anchors (9-10) ---
    def test_09_zero_broken_internal_links(self):
        res = check_link_graph(ROOT, strict=False)
        self.assertEqual(len(res["broken_links"]), 0, f"Broken links: {res['broken_links']}")

    def test_10_zero_broken_anchors(self):
        res = check_link_graph(ROOT, strict=False)
        self.assertEqual(len(res["broken_anchors"]), 0, f"Broken anchors: {res['broken_anchors']}")

    # --- Title & Meta Description Tags (11-16) ---
    def test_11_all_pages_have_title_tag(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            self.assertIsNotNone(title_m, f"Missing title in {hf}")

    def test_12_title_tag_lengths_within_bounds(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            title = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE).group(1).strip()
            self.assertGreaterEqual(len(title), 30, f"Title too short in {hf}: '{title}' ({len(title)} chars)")
            self.assertLessEqual(len(title), 65, f"Title too long in {hf}: '{title}' ({len(title)} chars)")

    def test_13_all_pages_have_meta_description(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', content, re.IGNORECASE)
            self.assertIsNotNone(desc_m, f"Missing meta description in {hf}")

    def test_14_meta_description_lengths_within_bounds(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', content, re.IGNORECASE)
            self.assertIsNotNone(desc_m, f"Missing meta description in {hf}")
            desc = desc_m.group(2).strip()
            self.assertGreaterEqual(len(desc), 70, f"Meta desc too short in {hf}: '{desc}' ({len(desc)} chars)")
            self.assertLessEqual(len(desc), 165, f"Meta desc too long in {hf}: '{desc}' ({len(desc)} chars)")

    def test_15_canonical_urls_present_on_all_pages(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
            self.assertIsNotNone(canon_m, f"Missing canonical in {hf}")
            self.assertTrue(canon_m.group(1).startswith("https://aidigitools.tech"), f"Invalid canonical {canon_m.group(1)} in {hf}")

    def test_16_html_lang_attribute_set_to_en(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            lang_m = re.search(r'<html[^>]*lang=["\']en["\']', content, re.IGNORECASE)
            self.assertIsNotNone(lang_m, f"Missing or non-en lang attribute in {hf}")

    # --- Mobile Responsive & Social Tags (17-20) ---
    def test_17_viewport_tag_present(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            self.assertIn("viewport", content.lower())
            self.assertIn("width=device-width", content.lower())

    def test_18_opengraph_title_and_description(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            self.assertIn('property="og:title"', content)
            self.assertIn('property="og:description"', content)
            self.assertIn('property="og:url"', content)

    def test_19_twitter_card_meta_present(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            self.assertIn('name="twitter:card"', content)
            self.assertIn('name="twitter:title"', content)

    def test_20_image_alt_attributes_never_empty(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            imgs = re.findall(r'<img\s+([^>]+)>', content, re.IGNORECASE)
            for img in imgs:
                alt_m = re.search(r'alt=["\'](.*?)["\']', img, re.IGNORECASE)
                self.assertIsNotNone(alt_m, f"Image missing alt in {hf}: {img}")
                self.assertGreater(len(alt_m.group(1).strip()), 0, f"Empty alt tag in {hf}")

    # --- Heading Hierarchy & AEO Standards (21-25) ---
    def test_21_exactly_one_h1_per_page(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            self.assertEqual(len(h1s), 1, f"Found {len(h1s)} H1 tags in {hf}")

    def test_22_quick_answer_block_present(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            self.assertIn('class="quick-answer"', content, f"Missing quick-answer block in {hf}")

    def test_23_quick_answer_word_count_35_to_70(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            qa_m = re.search(r'<p[^>]*class=["\']quick-answer["\'][^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            self.assertIsNotNone(qa_m, f"Could not extract quick-answer in {hf}")
            clean_text = re.sub(r'<[^>]+>', '', qa_m.group(1)).strip()
            words = clean_text.split()
            self.assertGreaterEqual(len(words), 35, f"Quick answer too short in {hf} ({len(words)} words)")
            self.assertLessEqual(len(words), 70, f"Quick answer too long in {hf} ({len(words)} words)")

    def test_24_no_empty_h2_tags(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.IGNORECASE | re.DOTALL)
            for h in h2s:
                self.assertGreater(len(re.sub(r'<[^>]+>', '', h).strip()), 0)

    def test_25_no_empty_paragraphs(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            ps = re.findall(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
            for p in ps:
                clean = re.sub(r'<[^>]+>', '', p).strip()
                self.assertGreater(len(clean), 0, f"Empty <p> in {hf}")

    # --- Structured Data JSON-LD (26-30) ---
    def test_26_valid_json_ld_syntax_on_all_pages(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
            self.assertGreater(len(schemas), 0, f"No JSON-LD schema found in {hf}")
            for s in schemas:
                try:
                    json.loads(s)
                except json.JSONDecodeError as e:
                    self.fail(f"Invalid JSON-LD in {hf}: {e}")

    def test_27_product_pages_have_product_schema(self):
        for tf in self.tool_files:
            content = tf.read_text(encoding="utf-8")
            self.assertIn('"@type": "Product"', content, f"Missing Product schema in {tf}")

    def test_28_product_pages_have_offer_pkr(self):
        for tf in self.tool_files:
            content = tf.read_text(encoding="utf-8")
            self.assertIn('"@type": "Offer"', content, f"Missing Offer in {tf}")
            self.assertIn('"priceCurrency": "PKR"', content, f"priceCurrency is not PKR in {tf}")

    def test_29_product_pages_have_breadcrumbs(self):
        for tf in self.tool_files:
            content = tf.read_text(encoding="utf-8")
            self.assertIn('"@type": "BreadcrumbList"', content, f"Missing Breadcrumbs in {tf}")

    def test_30_guide_pages_have_article_schema(self):
        for gf in self.guide_files:
            content = gf.read_text(encoding="utf-8")
            self.assertTrue('"@type": "TechArticle"' in content or '"@type": "Article"' in content, f"Missing Article schema in {gf}")

    # --- Pricing & Local Rails Fan-out (31-35) ---
    def test_31_chatgpt_pricing_pkr(self):
        content = (ROOT / "tools/chatgpt-plus.html").read_text(encoding="utf-8")
        self.assertIn("2,300", content)
        self.assertIn("EasyPaisa", content)

    def test_32_claude_pricing_pkr(self):
        content = (ROOT / "tools/claude-pro.html").read_text(encoding="utf-8")
        self.assertIn("2,500", content)
        self.assertIn("JazzCash", content)

    def test_33_canva_pricing_pkr(self):
        content = (ROOT / "tools/canva-pro.html").read_text(encoding="utf-8")
        self.assertIn("600", content)
        self.assertIn("EasyPaisa", content)

    def test_34_local_payment_rails_mentioned(self):
        for tf in self.tool_files:
            content = tf.read_text(encoding="utf-8").lower()
            self.assertTrue("easypaisa" in content or "jazzcash" in content or "sadapay" in content)

    def test_35_delivery_sla_mentioned(self):
        for tf in self.tool_files:
            content = tf.read_text(encoding="utf-8").lower()
            self.assertTrue("15 minutes" in content or "instant" in content)

    # --- Safety & Anti-Hallucination Firewalls (36-40) ---
    def test_36_no_unintegrated_stripe_gateway_forms(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8").lower()
            self.assertNotIn("action=\"https://api.stripe.com", content)
            self.assertNotIn("stripe-element", content)

    def test_37_no_unintegrated_paypal_checkout_buttons(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8").lower()
            self.assertNotIn("www.paypal.com/cgi-bin/webscr", content)
            self.assertNotIn("paypal-button-container", content)

    def test_38_whatsapp_links_format(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            wa_links = re.findall(r'href=["\'](https://wa\.me/[^"\']+)["\']', content)
            for wl in wa_links:
                self.assertTrue(wl.startswith("https://wa.me/92"))

    def test_39_replacement_warranty_on_all_tools(self):
        for tf in self.tool_files:
            content = tf.read_text(encoding="utf-8").lower()
            self.assertTrue("warranty" in content or "guarantee" in content)

    def test_40_distinct_tool_slugs(self):
        slugs = [tf.stem for tf in self.tool_files]
        self.assertEqual(len(slugs), len(set(slugs)))

    # --- CSS & Design Assets (41-45) ---
    def test_41_stylesheet_exists(self):
        css_file = ROOT / "assets/style.css"
        self.assertTrue(css_file.is_file())
        self.assertGreater(css_file.stat().st_size, 500)

    def test_42_css_has_css_variables(self):
        css_text = (ROOT / "assets/style.css").read_text(encoding="utf-8")
        self.assertIn(":root", css_text)
        self.assertIn("--accent-gold", css_text)

    def test_43_all_pages_reference_stylesheet(self):
        for hf in self.html_files:
            content = hf.read_text(encoding="utf-8")
            self.assertIn("style.css", content)

    def test_44_no_broken_css_imports(self):
        css_text = (ROOT / "assets/style.css").read_text(encoding="utf-8")
        self.assertNotIn("@import", css_text)

    def test_45_policies_has_payment_rails_anchor(self):
        policies = (ROOT / "policies.html").read_text(encoding="utf-8")
        self.assertIn('id="payments"', policies)
        self.assertIn('id="refunds"', policies)

    # --- Agent Invariants & System Files (46-50) ---
    def test_46_agents_md_exists(self):
        agents_md = ROOT / "AGENTS.md"
        self.assertTrue(agents_md.is_file())
        content = agents_md.read_text(encoding="utf-8")
        self.assertIn("AIDigiTools", content)
        self.assertIn("aidigitools.tech", content)

    def test_47_geo_aeo_invariants_rule_exists(self):
        rule = ROOT / ".agents/rules/geo-aeo-invariants.md"
        self.assertTrue(rule.is_file())

    def test_48_geo_aeo_skill_exists(self):
        skill = ROOT / ".agents/skills/geo-aeo-optimizer/SKILL.md"
        self.assertTrue(skill.is_file())

    def test_49_seoranking_workflow_exists(self):
        wf = ROOT / ".agents/workflows/seoranking.md"
        self.assertTrue(wf.is_file())

    def test_50_master_link_graph_integrity_flag(self):
        res = check_link_graph(ROOT, strict=True)
        self.assertTrue(res["passed"])

    def test_51_custom_404_page_integrity(self):
        page_404 = ROOT / "404.html"
        self.assertTrue(page_404.is_file(), "Custom 404.html must exist")
        content = page_404.read_text(encoding="utf-8")
        self.assertIn("noindex", content, "404 page must be marked noindex")
        self.assertIn("assets/style.css", content)
        self.assertIn("03326861112", content)
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.I)
        self.assertEqual(len(h1s), 1, "404 page must have exactly one H1")

if __name__ == "__main__":
    unittest.main()
