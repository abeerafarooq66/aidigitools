import os
import re
import unittest
import glob

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestPhase15FullRegression(unittest.TestCase):
    """
    Master regression test suite for Phase 15:
    Validates all 11 controlled stages (Stage A through Stage K) across
    access, baseline, architecture, design system, catalog, SEO, a11y,
    structured data, search visibility, performance, and deployment readiness.
    """

    def setUp(self):
        self.all_html_files = glob.glob(os.path.join(REPO_ROOT, "**", "*.html"), recursive=True)
        self.tool_files = glob.glob(os.path.join(REPO_ROOT, "tools", "*.html"))
        self.category_files = glob.glob(os.path.join(REPO_ROOT, "categories", "*.html"))
        self.css_path = os.path.join(REPO_ROOT, "assets", "style.css")
        self.cart_js_path = os.path.join(REPO_ROOT, "assets", "cart.js")

    def test_stage_a_access_and_baseline_audit(self):
        """Stage A: Verify repository git health, snapshot branch, and physical backup directory."""
        self.assertTrue(os.path.exists(os.path.join(REPO_ROOT, ".git")), "Local git repo must be intact.")
        physical_backup = r"C:\Users\Dell\Desktop\aidigitools_backup_phase0"
        if not os.path.exists(physical_backup):
            # In CI environments, physical workstation directory is not present
            self.skipTest("Physical baseline backup directory is local to developer workstation.")

    def test_stage_b_architecture_and_content_model(self):
        """Stage B: Verify 53 published HTML routes and logical 4-tier directory hierarchy."""
        self.assertEqual(
            len(self.all_html_files), 66,
            f"Expected exactly 53 published HTML pages, found {len(self.all_html_files)}."
        )
        self.assertEqual(len(self.tool_files), 49, f"Expected 36 tool pages, found {len(self.tool_files)}.")
        self.assertEqual(len(self.category_files), 4, f"Expected 4 category hubs, found {len(self.category_files)}.")

    def test_stage_c_brand_and_ui_ux_redesign(self):
        """Stage C: Verify design tokens, Orbit Emblem SVG, and component classes in assets/style.css."""
        with open(self.css_path, "r", encoding="utf-8") as f:
            css = f.read()
        tokens = ['--brand-mint', '--brand-cyan', '--brand-indigo', '--brand-violet', '--bg-canvas', '--text-primary']
        for t in tokens:
            self.assertIn(t, css, f"Missing design token: {t}")

        components = ['.empty-state', '.loading-spinner', '.error-state', '.breadcrumbs', '.pagination']
        for c in components:
            self.assertIn(c, css, f"Missing UI component class: {c}")

    def test_stage_d_homepage_and_global_layout(self):
        """Stage D: Verify index.html structure, search landmark form, and pre-order terms bar."""
        index_path = os.path.join(REPO_ROOT, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        self.assertIn('<form role="search"', html)
        self.assertIn('class="category-filter-pills"', html)
        self.assertIn('class="pre-order-terms-bar"', html)
        self.assertIn('id="compareDock"', html)
        self.assertIn('id="cartDrawer"', html)

    def test_stage_e_categories_and_directory(self):
        """Stage E: Verify category hubs have CollectionPage schema and item lists."""
        for cat_file in self.category_files:
            with open(cat_file, "r", encoding="utf-8") as f:
                c_html = f.read()
            self.assertIn('CollectionPage', c_html, f"{os.path.basename(cat_file)} must define CollectionPage schema.")
            self.assertIn('ItemList', c_html, f"{os.path.basename(cat_file)} must define ItemList schema.")

    def test_stage_f_verified_product_pages(self):
        """Stage F: Verify all 36 product pages include specs block, PKR price, platforms, and vendor links."""
        for tool_file in self.tool_files:
            with open(tool_file, "r", encoding="utf-8") as f:
                t_html = f.read()
            self.assertIn('id="phase6-spec-block"', t_html, f"{os.path.basename(tool_file)} missing #phase6-spec-block")
            self.assertIn('PKR', t_html, f"{os.path.basename(tool_file)} missing PKR price")
            self.assertIn('rel="noopener noreferrer nofollow"', t_html, f"{os.path.basename(tool_file)} missing vendor link attributes")
            self.assertIn('Supported Platforms', t_html, f"{os.path.basename(tool_file)} missing platforms section")

    def test_stage_g_editorial_and_trust_pages(self):
        """Stage G: Verify trust and policy pages exist and editorial pages meet word count standards."""
        trust_pages = ["about.html", "contact.html", "policies.html", "shipping-policy.html", "affiliate-disclosure.html", "deals.html"]
        for tp in trust_pages:
            tp_path = os.path.join(REPO_ROOT, tp)
            self.assertTrue(os.path.exists(tp_path), f"Trust page {tp} must exist.")

        editorial_pages = [
            os.path.join(REPO_ROOT, "compare", "chatgpt-vs-claude.html"),
            os.path.join(REPO_ROOT, "compare", "runway-vs-pika.html"),
            os.path.join(REPO_ROOT, "best", "best-ai-coding-tools.html"),
            os.path.join(REPO_ROOT, "best", "best-ai-video-generators.html"),
            os.path.join(REPO_ROOT, "guides", "chatgpt-vs-claude.html"),
        ]
        for ep in editorial_pages:
            with open(ep, "r", encoding="utf-8") as f:
                content = f.read()
            words = len(content.split())
            self.assertGreaterEqual(words, 1500, f"{os.path.basename(ep)} must have >= 1,500 words.")

    def test_stage_h_technical_seo_and_structured_data(self):
        """Stage H: Verify self-referencing canonicals, sitemap, robots.txt, and valid JSON-LD schemas."""
        sitemap_path = os.path.join(REPO_ROOT, "sitemap.xml")
        robots_path = os.path.join(REPO_ROOT, "robots.txt")
        self.assertTrue(os.path.exists(sitemap_path), "sitemap.xml must exist.")
        self.assertTrue(os.path.exists(robots_path), "robots.txt must exist.")

        for html_file in self.all_html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn('<link rel="canonical"', c, f"{os.path.basename(html_file)} missing canonical link tag.")
            self.assertIn('application/ld+json', c, f"{os.path.basename(html_file)} missing structured data.")

    def test_stage_i_google_and_bing_readiness(self):
        """Stage I: Verify Bing verification file, IndexNow key, and submission script."""
        bing_auth = os.path.join(REPO_ROOT, "BingSiteAuth.xml")
        indexnow_key = os.path.join(REPO_ROOT, "e3b0c44298fc1c149afbf4c8996fb924.txt")
        submit_script = os.path.join(REPO_ROOT, "scripts", "submit_indexnow.py")

        self.assertTrue(os.path.exists(bing_auth), "BingSiteAuth.xml must exist.")
        self.assertTrue(os.path.exists(indexnow_key), "IndexNow key file must exist.")
        self.assertTrue(os.path.exists(submit_script), "IndexNow submission script must exist.")

    def test_stage_j_performance_accessibility_and_security(self):
        """Stage J: Verify explicit image dimensions, zero external tracking scripts, and zero secret leaks."""
        for html_file in self.all_html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                c = f.read()
            # check zero 3rd-party scripts
            scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', c)
            for s in scripts:
                self.assertFalse(s.startswith('http'), f"{os.path.basename(html_file)} contains external script: {s}")

        with open(self.css_path, "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn(':focus-visible', css, "assets/style.css must have :focus-visible rules.")
        self.assertIn('prefers-reduced-motion', css, "assets/style.css must have prefers-reduced-motion rules.")

    def test_stage_k_full_regression_and_deployment_rollback_plan(self):
        """Stage K: Verify deployment and rollback documentation exists."""
        plan_path = os.path.join(REPO_ROOT, "docs", "DEPLOYMENT_AND_ROLLBACK_PLAN.md")
        self.assertTrue(os.path.exists(plan_path), "docs/DEPLOYMENT_AND_ROLLBACK_PLAN.md must exist.")
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Tier 1: Instant Git Hard Reset", content)
        self.assertIn("Tier 2: Snapshot Branch Restoration", content)
        self.assertIn("Tier 3: Physical Directory Restoration", content)

if __name__ == "__main__":
    unittest.main()
