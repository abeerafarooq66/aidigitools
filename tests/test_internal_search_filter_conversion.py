import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestInternalSearchFilterConversion(unittest.TestCase):
    """
    Automated compliance suite for Phase 13:
    Internal Search, Filtering, Sorting, Product Comparison, Conversion & Pre-Order Terms.
    """

    def setUp(self):
        self.index_path = os.path.join(REPO_ROOT, "index.html")
        self.cart_js_path = os.path.join(REPO_ROOT, "assets", "cart.js")
        self.robots_path = os.path.join(REPO_ROOT, "robots.txt")

        with open(self.index_path, "r", encoding="utf-8") as f:
            self.index_html = f.read()

        with open(self.cart_js_path, "r", encoding="utf-8") as f:
            self.cart_js = f.read()

        with open(self.robots_path, "r", encoding="utf-8") as f:
            self.robots_txt = f.read()

    def test_01_search_input_and_controls_present_and_accessible(self):
        """Verify search input exists with accessibility attributes and clear button."""
        self.assertIn('id="toolSearchInput"', self.index_html)
        self.assertIn('role="searchbox"', self.index_html)
        self.assertIn('aria-label=', self.index_html)
        self.assertIn('id="clearSearchBtn"', self.index_html)
        self.assertIn('onclick="clearSearchInput()"', self.index_html)

    def test_02_category_filter_pills_present_with_aria(self):
        """Verify category filter pills exist with aria-pressed attributes."""
        self.assertIn('class="category-filter-pills"', self.index_html)
        self.assertIn('role="group"', self.index_html)
        categories = ['coding', 'video', 'image', 'ai', 'vpn', 'productivity', 'streaming']
        for cat in categories:
            self.assertIn(f'data-cat="{cat}"', self.index_html, f"Missing category filter for '{cat}'")
            self.assertIn(f"filterCategory('{cat}')", self.index_html)
        self.assertIn('aria-pressed="true"', self.index_html)

    def test_03_sorting_and_price_filters_present(self):
        """Verify price range and sort dropdowns are present with useful options."""
        self.assertIn('id="priceFilter"', self.index_html)
        self.assertIn('id="sortSelect"', self.index_html)
        self.assertIn('id="searchCountBadge"', self.index_html)
        self.assertIn('aria-live="polite"', self.index_html)

        # Verify price options
        price_options = ['all', 'under-1000', '1000-2500', 'above-2500']
        for opt in price_options:
            self.assertIn(f'value="{opt}"', self.index_html, f"Missing price option '{opt}'")

        # Verify sort options
        sort_options = ['featured', 'price-asc', 'price-desc', 'name-asc', 'name-desc']
        for s_opt in sort_options:
            self.assertIn(f'value="{s_opt}"', self.index_html, f"Missing sort option '{s_opt}'")

    def test_04_all_36_cards_enriched_with_filter_attributes(self):
        """Verify all 36 tool cards in index.html are enriched with search and filter data attributes."""
        tool_cards = re.findall(r'<div class="card tool-card"[^>]*>', self.index_html)
        self.assertEqual(len(tool_cards), 49, f"Expected 36 parent tool cards, found {len(tool_cards)}")

        for i, card in enumerate(tool_cards):
            self.assertIn('data-tool="', card, f"Card {i} missing data-tool")
            self.assertIn('data-name="', card, f"Card {i} missing data-name")
            self.assertIn('data-price-pkr="', card, f"Card {i} missing data-price-pkr")
            self.assertIn('data-category="', card, f"Card {i} missing data-category")
            self.assertIn('data-vendor="', card, f"Card {i} missing data-vendor")
            self.assertIn('data-terms="', card, f"Card {i} missing data-terms")

    def test_05_clear_product_comparison_controls(self):
        """Verify product comparison buttons, floating dock, and modal exist."""
        compare_btns = re.findall(r'btn-tool-compare', self.index_html)
        self.assertEqual(len(compare_btns), 49, f"Expected 36 compare buttons, found {len(compare_btns)}")

        self.assertIn('id="compareDock"', self.index_html)
        self.assertIn('id="compareModalBackdrop"', self.index_html)
        self.assertIn('id="compareModalBody"', self.index_html)
        self.assertIn('openCompareModal()', self.index_html)
        self.assertIn('clearComparison()', self.index_html)

    def test_06_pre_order_transparency_terms_present(self):
        """Verify pre-order transparency terms are clearly stated before purchase."""
        self.assertIn('pre-order-terms-bar', self.index_html)
        self.assertIn('15–30 Min', self.index_html)
        self.assertIn('30-Day Replacement Warranty', self.index_html)
        self.assertIn('shared', self.index_html.lower())
        self.assertIn('EasyPaisa', self.index_html)

    def test_07_reliable_purchase_actions_and_no_fake_carts(self):
        """Verify purchase actions are authentic WhatsApp concierge links, and no fake payment forms exist."""
        self.assertIn('https://wa.me/923326861112', self.index_html)
        self.assertIn('openQuickOrderModal(', self.index_html)

        # Verify no deceptive fake checkout inputs (e.g. fake credit card inputs)
        fake_inputs = ['name="cc_number"', 'name="cvv"', 'name="card_number"', 'placeholder="Card number"']
        for fake in fake_inputs:
            self.assertNotIn(fake, self.index_html.lower(), f"Deceptive fake checkout input found: {fake}")

    def test_08_robots_txt_disallows_query_parameter_duplication(self):
        """Verify robots.txt disallows query parameters to prevent crawler duplicate indexing."""
        param_patterns = [
            'Disallow: /*?*q=',
            'Disallow: /*?*search=',
            'Disallow: /*?*sort=',
            'Disallow: /*?*filter=',
            'Disallow: /*?*category=',
            'Disallow: /*?*price='
        ]
        for pattern in param_patterns:
            self.assertIn(pattern, self.robots_txt, f"robots.txt missing parameter disallow directive: {pattern}")

    def test_09_cart_js_engine_functions_defined(self):
        """Verify assets/cart.js contains all required filtering, sorting, and comparison functions."""
        required_functions = [
            'window.applyFilters',
            'window.filterCategory',
            'window.toggleCompare',
            'window.openCompareModal',
            'window.closeCompareModal',
            'window.clearComparison',
            'window.resetAllFilters',
            'window.applyQuickSearch',
            'searchEmptyState',
            'history.replaceState'
        ]
        for func in required_functions:
            self.assertIn(func, self.cart_js, f"assets/cart.js missing required engine component: {func}")

if __name__ == "__main__":
    unittest.main()
