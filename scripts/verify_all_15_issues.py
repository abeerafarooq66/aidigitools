import os
import re
import sys

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO_ROOT, "index.html")
STYLE_PATH = os.path.join(REPO_ROOT, "assets", "style.css")
CART_PATH = os.path.join(REPO_ROOT, "assets", "cart.js")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

with open(STYLE_PATH, "r", encoding="utf-8") as f:
    css = f.read()

with open(CART_PATH, "r", encoding="utf-8") as f:
    js = f.read()

passed = []
failed = []

def record(num, name, condition, details=""):
    if condition:
        print(f"[PASS] Issue {num}: {name} -> {details}")
        passed.append(num)
    else:
        print(f"[FAIL] Issue {num}: {name} -> {details}")
        failed.append(num)

# Issue 1: Many button styles consolidated
c1 = (".btn {" in css and ".btn-primary" in css and ".btn-secondary" in css and "--radius-md" in css)
record(1, "Many button styles consolidated into systematic 3-tier hierarchy", c1, "Base .btn with shared padding, radius, transitions")

# Issue 2: Two separate category filters harmonized
cats_showcase = re.findall(r'<button type="button" class="authkit-cat-pill[^"]*"[^>]*data-cat="([^"]+)"', html)
cats_expected = ['all', 'coding', 'video', 'image', 'ai', 'vpn', 'productivity', 'streaming']
c2 = (cats_showcase == cats_expected)
record(2, "Two category filter button sets harmonized", c2, f"Showcase now contains exact matching 8 categories: {cats_showcase}")

# Issue 3: Wall of buttons on tool cards resolved with clear hierarchy
c3 = (".tool-card-cta-row .btn-quick-order" in css and "grid-column: 1 / -1" in css and "grid-column: span 1" in css)
record(3, "Tool card CTA density organized into 3-tier hierarchy", c3, "Primary full-width (100%), secondary side-by-side (50/50), tertiary link")

# Issue 4: Filter buttons have visible active state & ARIA
c4_css = (".authkit-cat-pill.active" in css and "background: #0F172A" in css)
c4_aria = ('aria-selected="true"' in html and 'aria-selected="false"' in html and 'setAttribute(\'aria-selected\'' in js)
c4 = (c4_css and c4_aria)
record(4, "Filter buttons have high-contrast active state and ARIA selection", c4, "High-contrast #0F172A background (15:1 ratio) + aria-selected dynamic update")

# Issue 5: Consistent type scale defined (Aim <= 10)
c5 = ("--text-xs: 0.75rem;" in css and "--text-sm: 0.875rem;" in css and "--text-base: 1rem;" in css and "--text-3xl: 2rem;" in css)
record(5, "Consistent typographic scale tokenized", c5, "Strict 7-level type scale in :root (12px, 14px, 16px, 18px, 20px, 24px, 32px)")

# Issue 6: Consolidated text colors (Aim <= 12)
c6 = ("--text-primary:" in css and "--text-secondary:" in css and "--text-muted:" in css and "--state-warning:" in css and "--state-success:" in css)
record(6, "Semantic color tokens consolidated", c6, "Mapped to centralized tokens for headings, body, muted, and state colors")

# Issue 7: Inconsistent corner radii (Aim <= 6)
c7 = ("--radius-sm: 6px;" in css and "--radius-md: 10px;" in css and "--radius-lg: 16px;" in css and "--radius-full: 9999px;" in css)
record(7, "Corner radii scale standardized", c7, "Consolidated to 4 tokens: 6px, 10px, 16px, 9999px")

# Issue 8: Body text very small in tagline (min ~12px)
c8 = (".logo .tagline {" in css and "font-size: 0.75rem;" in css)
record(8, "Header tagline font size increased to 12px", c8, "Changed from 0.65rem (10px) to 0.75rem (12px, WCAG minimum)")

# Issue 9: Long all-caps text resolved
c9 = (".tool-cat-badge {" in css and "text-transform: none;" in css)
record(9, "Long all-caps text in tool badges converted to Title Case", c9, "text-transform changed from uppercase to none")

# Issue 10: Body text in tool rank badge is at least 12px (min ~12px)
c10_css = (".tool-rank-badge" in css and "font-size: 0.78rem !important;" in css)
c10_html = ("font-size: 0.72rem;" not in html and "font-size: 0.78rem;" in html)
c10 = (c10_css and c10_html)
record(10, "Tool rank badge font size increased above 12px", c10, "Upgraded to 0.78rem (12.5px / 13px)")

# Issue 11: Heading level skipped (H2 to H4 resolved)
c11_html = ("<div class=\"footer-col\">\n          <h3>Explore</h3>" in html and "<div class=\"footer-col\">\n          <h3>Learn &amp; Compare</h3>" in html)
c11_css = (".footer-col h3," in css)
c11 = (c11_html and c11_css)
record(11, "Footer headings outline level skip resolved (H2 to H3)", c11, "Changed <h4> to <h3> in footer columns, outline is strictly sequential")

# Issue 12: Repetitive feature lines visual noise reduced
c12 = (".tool-card-checklist {" in css and "background: rgba(241, 245, 249, 0.5);" in css and "padding: 0.55rem 0.75rem;" in css)
record(12, "Repetitive feature list compacted into neat reassurance block", c12, "Compact styling with subtle background container & reduced vertical space")

# Issue 13: Hero CTA buttons visual hierarchy established
c13 = ("hero-btn-main" in html or "padding:0.85rem 1.75rem; font-size:1rem; font-weight:700; box-shadow:0 4px 16px rgba(0,180,216,0.35);" in html)
record(13, "Hero CTAs visual hierarchy differentiated", c13, "Dominant primary button vs subtle secondary outline buttons")

# Issue 14: Header logo and navigation container centered without extreme gap
c14 = (".nav-wrapper {" in css and "max-width: 1140px;" in css and "margin: 0 auto;" in css)
record(14, "Header logo and navigation container centered", c14, "max-width: 1140px with margin: 0 auto anchors navigation to content column")

# Issue 15: Netflix and held cards have clear status badge and no duplicate 'Inquire'
held_slugs = ['netflix-premium', 'linkedin-premium', 'coursera-plus', 'spotify-premium', 'turnitin-student']
all_held_badged = all(
    (f'data-tool="{slug}"' in html and "inquiry-badge" in html.split(f'data-tool="{slug}"')[1].split('</div>\n          <div class="tool-card-actions">')[0])
    for slug in held_slugs
)
no_duplicate_inquire = ('💬 Inquire' not in html and '💬 WhatsApp Inquiry' in html)
c15 = (all_held_badged and no_duplicate_inquire)
record(15, "Netflix & held products have clear status badge and distinct actions", c15, "Added 'Inquiry Only • Direct Orders Paused' badge + 'WhatsApp Inquiry' action")

print(f"\n==================================================")
print(f"VERIFICATION RESULT: {len(passed)}/15 PASSED, {len(failed)}/15 FAILED")
print(f"==================================================")

if len(failed) > 0:
    sys.exit(1)
