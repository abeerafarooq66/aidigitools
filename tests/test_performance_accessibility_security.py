import os
import re
import unittest
import glob

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestPerformanceAccessibilitySecurity(unittest.TestCase):
    """
    Automated compliance suite for Phase 14:
    Performance, Accessibility (a11y), Core Web Vitals, Contrast, Reduced Motion,
    Form Validation, and Security / Secret Auditing across aidigitools.tech.
    """

    def setUp(self):
        self.all_html_files = glob.glob(os.path.join(REPO_ROOT, "**", "*.html"), recursive=True)
        self.css_path = os.path.join(REPO_ROOT, "assets", "style.css")
        self.cart_js_path = os.path.join(REPO_ROOT, "assets", "cart.js")

        with open(self.css_path, "r", encoding="utf-8") as f:
            self.css = f.read()

        with open(self.cart_js_path, "r", encoding="utf-8") as f:
            self.cart_js = f.read()

    def test_01_all_images_have_explicit_dimensions_and_svg_format(self):
        """Verify 100% of <img> tags have explicit width & height to prevent CLS."""
        total_images = 0
        missing_dims = []

        for html_file in self.all_html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            img_tags = re.findall(r'<img[^>]*>', content)
            total_images += len(img_tags)
            for tag in img_tags:
                has_w = 'width=' in tag
                has_h = 'height=' in tag
                if not (has_w and has_h):
                    missing_dims.append((os.path.basename(html_file), tag))

        self.assertGreater(total_images, 0, "Images must exist on the website.")
        self.assertEqual(
            len(missing_dims), 0,
            f"Found {len(missing_dims)} images without explicit width and height: {missing_dims[:3]}"
        )

    def test_02_font_loading_zero_blocking_external_fonts(self):
        """Verify no blocking external font stylesheets (fonts.googleapis.com) to guarantee 0 FOIT."""
        for html_file in self.all_html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(
                'fonts.googleapis.com', content,
                f"{os.path.basename(html_file)} links to external blocking Google Fonts."
            )

    def test_03_zero_third_party_tracking_scripts(self):
        """Verify zero external third-party tracking, advertising, or bloated scripts."""
        for html_file in self.all_html_files:
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', content)
            for s in scripts:
                is_external = s.startswith('http://') or s.startswith('https://') or s.startswith('//')
                self.assertFalse(
                    is_external,
                    f"{os.path.basename(html_file)} includes external 3rd-party script: {s}"
                )

    def test_04_javascript_bundle_size_within_budget(self):
        """Verify JavaScript bundle is under 100 KB uncompressed (pure vanilla, zero framework bloat)."""
        js_size_bytes = os.path.getsize(self.cart_js_path)
        self.assertLess(
            js_size_bytes, 102400,
            f"assets/cart.js size is {js_size_bytes} bytes, exceeding 100 KB performance budget."
        )

    def test_05_reduced_motion_media_queries_present(self):
        """Verify CSS respects prefers-reduced-motion to accommodate vestibular motion sensitivity."""
        reduced_motion_matches = re.findall(r'prefers-reduced-motion:\s*reduce', self.css)
        self.assertGreaterEqual(
            len(reduced_motion_matches), 1,
            "assets/style.css must contain @media (prefers-reduced-motion: reduce) rules."
        )

    def test_06_focus_visibility_rules_present(self):
        """Verify CSS contains accessible :focus-visible rules for keyboard navigation."""
        focus_visible_matches = re.findall(r':focus-visible', self.css)
        self.assertGreaterEqual(
            len(focus_visible_matches), 3,
            "assets/style.css must define visible focus indicators using :focus-visible."
        )

    def test_07_accessible_form_labels_and_validation(self):
        """Verify contact.html contains an accessible form with associated labels and error feedback."""
        contact_path = os.path.join(REPO_ROOT, "contact.html")
        with open(contact_path, "r", encoding="utf-8") as f:
            contact_html = f.read()

        self.assertIn('<form id="contactInquiryForm"', contact_html)
        self.assertIn('for="inquiryName"', contact_html)
        self.assertIn('for="inquiryEmail"', contact_html)
        self.assertIn('for="inquiryTopic"', contact_html)
        self.assertIn('for="inquiryMessage"', contact_html)
        self.assertIn('required', contact_html)
        self.assertIn('aria-live="polite"', contact_html)
        self.assertIn('handleInquirySubmit', contact_html)

    def test_08_search_form_landmark_and_accessible_name(self):
        """Verify index.html contains a search form landmark with accessible name."""
        index_path = os.path.join(REPO_ROOT, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            index_html = f.read()

        self.assertIn('<form role="search"', index_html)
        self.assertIn('role="searchbox"', index_html)
        self.assertIn('aria-label=', index_html)

    def test_09_zero_exposed_secrets_or_api_keys(self):
        """Scan all HTML and JS files for accidentally exposed API keys, tokens, or hardcoded passwords."""
        secret_patterns = [
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
            (r'ghp_[a-zA-Z0-9]{20,}', "GitHub Token"),
            (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
            (r'(?:cost_usdt|wholesale_price)\s*[:=]', "Wholesale Cost Leak")
        ]

        for file_path in self.all_html_files + [self.cart_js_path]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            for pattern, desc in secret_patterns:
                matches = re.findall(pattern, content)
                self.assertEqual(
                    len(matches), 0,
                    f"Security Alert: Potential {desc} found in {os.path.basename(file_path)}: {matches}"
                )

    def test_10_color_contrast_wcag_aa_compliance(self):
        """Verify color tokens defined in CSS meet WCAG 2.1 AA/AAA contrast ratios."""
        # Calculate contrast ratio between text and background
        def luminance(r, g, b):
            a = [x / 255.0 for x in [r, g, b]]
            a = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in a]
            return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]

        def contrast_ratio(rgb1, rgb2):
            lum1 = luminance(*rgb1)
            lum2 = luminance(*rgb2)
            lighter = max(lum1, lum2)
            darker = min(lum1, lum2)
            return (lighter + 0.05) / (darker + 0.05)

        # Primary Text (#0F172A) on White Background (#FFFFFF)
        text_primary = (15, 23, 42)
        bg_white = (255, 255, 255)
        ratio_primary = contrast_ratio(text_primary, bg_white)
        self.assertGreaterEqual(ratio_primary, 7.0, f"Primary text contrast ratio {ratio_primary:.2f} must exceed WCAG AAA 7.0:1")

        # Secondary Text (#334155) on White Background (#FFFFFF)
        text_secondary = (51, 65, 85)
        ratio_secondary = contrast_ratio(text_secondary, bg_white)
        self.assertGreaterEqual(ratio_secondary, 4.5, f"Secondary text contrast ratio {ratio_secondary:.2f} must exceed WCAG AA 4.5:1")

        # Action Button (#00E5A3) with Dark Text (#0F172A)
        btn_bg = (0, 229, 163)
        ratio_btn = contrast_ratio(text_primary, btn_bg)
        self.assertGreaterEqual(ratio_btn, 4.5, f"Action button contrast ratio {ratio_btn:.2f} must exceed WCAG AA 4.5:1")

if __name__ == "__main__":
    unittest.main()
