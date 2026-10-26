"""
Apply full AIDigiTools redesign across all 52 pages:
1. Header: Animated SVG Orbit Emblem + clean navigation without WhatsApp CTA (Quick Order drawer trigger).
2. Footer: Clean, modern footer.
3. Dynamic Floating WhatsApp Concierge widget at bottom-right before </body>.
4. Universal Slide-Over Quick Order / Cart Drawer before </body>.
5. Inclusion of assets/cart.js.
6. Official brand SVG logos in all tool pages and deals bundles.
7. 100% Link graph & SEO / AEO integrity preserved.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "scripts" / "tools_catalog.json"
catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

SVG_EMBLEM_HEADER = """<svg class="logo-brand-icon" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <defs>
            <linearGradient id="navTeal" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#00E5A3"/>
              <stop offset="50%" stop-color="#05D5A6"/>
              <stop offset="100%" stop-color="#00B4D8"/>
            </linearGradient>
            <linearGradient id="navPurple" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0077B6"/>
              <stop offset="35%" stop-color="#4361EE"/>
              <stop offset="70%" stop-color="#7209B7"/>
              <stop offset="100%" stop-color="#8B5CF6"/>
            </linearGradient>
            <linearGradient id="navOrbit" x1="0%" y1="50%" x2="100%" y2="50%">
              <stop offset="0%" stop-color="#00E5A3"/>
              <stop offset="50%" stop-color="#00B4D8"/>
              <stop offset="100%" stop-color="#8B5CF6"/>
            </linearGradient>
          </defs>
          <path class="orbit-back" d="M 12 62 C 12 36, 126 18, 134 38" stroke="url(#navOrbit)" stroke-width="3.5" stroke-linecap="round" fill="none" opacity="0.65"/>
          <path class="sparkle-star" d="M 8 36 Q 8 41 3 41 Q 8 41 8 46 Q 8 41 13 41 Q 8 41 8 36 Z" fill="#00E5A3"/>
          <path class="sparkle-star" d="M 128 78 Q 128 82 124 82 Q 128 82 128 86 Q 128 82 132 82 Q 128 82 128 78 Z" fill="#8B5CF6"/>
          <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" fill="url(#navTeal)"/>
          <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" fill="url(#navPurple)"/>
          <path d="M 46 64 C 52 58, 66 56, 80 62 L 72 74 C 62 70, 52 72, 46 76 Z" fill="url(#navTeal)" opacity="0.95"/>
          <path class="orbit-front" d="M 134 38 C 142 58, 38 88, 16 66" stroke="url(#navOrbit)" stroke-width="4" stroke-linecap="round" fill="none"/>
          <circle class="orbit-node" cx="124" cy="34" r="5.5" fill="#4361EE"/>
          <circle cx="122.5" cy="32.5" r="1.8" fill="#FFFFFF" opacity="0.8"/>
        </svg>"""

def build_header(is_root=True):
    prefix = "" if is_root else "../"
    home_link = "index.html" if is_root else "../index.html"
    products_link = "index.html#products" if is_root else "../index.html#products"
    
    return f"""<header>
    <div class="container nav-wrapper">
      <a href="{home_link}" class="logo" aria-label="AIDigiTools Home">
        {SVG_EMBLEM_HEADER}
        <span class="logo-text-wrap">
          <span class="logo-brand-name"><span class="ai-prefix">AI</span> DigiTools</span>
          <span class="tagline">SMART TOOLS • BIGGER POSSIBILITIES</span>
        </span>
      </a>
      <nav>
        <a href="{products_link}">Products</a>
        <a href="{prefix}deals.html">Deals</a>
        <a href="{prefix}categories/video.html">Video</a>
        <a href="{prefix}categories/coding.html">Coding</a>
        <a href="{prefix}categories/vpn.html">VPN</a>
        <a href="{prefix}categories/image.html">Image</a>
        <a href="{prefix}shipping-policy.html">Delivery</a>
        <a href="{prefix}policies.html#payments">Payments</a>
        <a href="{prefix}contact.html">Contact</a>
        <button type="button" onclick="openQuickOrderModal('chatgpt-plus')" class="nav-cta" style="border:none; cursor:pointer;" aria-label="Open Quick Order">
          <span>🛒 Quick Order</span>
        </button>
      </nav>
    </div>
  </header>"""

def build_footer(is_root=True):
    prefix = "" if is_root else "../"
    home_link = "index.html" if is_root else "../index.html"
    
    return f"""<footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="{home_link}" class="logo" style="margin-bottom:0.75rem;" aria-label="AIDigiTools Home">
            {SVG_EMBLEM_HEADER}
            <span class="logo-text-wrap">
              <span class="logo-brand-name"><span class="ai-prefix">AI</span> DigiTools</span>
              <span class="tagline">SMART TOOLS • BIGGER POSSIBILITIES</span>
            </span>
          </a>
          <p style="font-size:0.88rem; color:var(--text-secondary); margin-top:0.75rem; line-height:1.55;">
            Premier localized AI software intelligence hub and subscription concierge serving Pakistan and worldwide customers with transparent PKR &amp; USD pricing and domestic rails.
          </p>
          <div style="margin-top:1rem;">
            <a href="https://wa.me/923326861112" target="_blank" rel="noopener noreferrer" class="btn-whatsapp" style="padding:0.5rem 1rem; font-size:0.85rem;">
              <span>💬 03326861112 (WhatsApp Desk)</span>
            </a>
          </div>
        </div>
        <div class="footer-col">
          <h4>Categories</h4>
          <ul>
            <li><a href="{prefix}categories/video.html">AI Video &amp; Animation</a></li>
            <li><a href="{prefix}categories/coding.html">Coding &amp; LLM Assistants</a></li>
            <li><a href="{prefix}categories/vpn.html">VPN &amp; Security Services</a></li>
            <li><a href="{prefix}categories/image.html">Image &amp; Graphic Suites</a></li>
            <li><a href="{prefix}deals.html">Bundle Deals &amp; Discounts</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Comparisons &amp; Guides</h4>
          <ul>
            <li><a href="{prefix}compare/chatgpt-vs-claude.html">ChatGPT vs Claude</a></li>
            <li><a href="{prefix}compare/runway-vs-pika.html">Runway vs Pika</a></li>
            <li><a href="{prefix}best/best-ai-video-generators.html">Best Video AI (2026)</a></li>
            <li><a href="{prefix}best/best-ai-coding-tools.html">Best Coding AI (2026)</a></li>
            <li><a href="{prefix}guides/chatgpt-vs-claude.html">AI Models Guide</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Policies &amp; Verification</h4>
          <ul>
            <li><a href="{prefix}policies.html#payments">Payment Rails (PKR &amp; USD)</a></li>
            <li><a href="{prefix}policies.html#refunds">30-Day Replacement Warranty</a></li>
            <li><a href="{prefix}shipping-policy.html">15-Minute Delivery SLA</a></li>
            <li><a href="{prefix}affiliate-disclosure.html">Reseller &amp; Trademark Policy</a></li>
            <li><a href="{prefix}contact.html">Support Operations Desk</a></li>
            <li><a href="{prefix}about.html">About AIDigiTools</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 AIDigiTools (aidigitools.tech). All rights reserved. Independent software subscription concierge desk.</p>
        <p style="margin-top:0.35rem; font-size:0.8rem; color:var(--text-muted);">
          Verified Rails: EasyPaisa • JazzCash • SadaPay • NayaPay • Raast • Bank IBFT • Wise • Binance Pay (USDT)
        </p>
      </div>
    </div>
  </footer>"""

def build_bottom_widgets(is_root=True):
    prefix = "" if is_root else "../"
    return f"""  <!-- ========================================================
       UNIVERSAL SLIDE-OVER QUICK ORDER / CART DRAWER
       ======================================================== -->
  <div class="cart-drawer-backdrop" id="cartBackdrop" onclick="closeQuickOrderModal()"></div>
  <aside class="cart-drawer" id="cartDrawer" aria-label="Quick Order Checkout">
    <div class="cart-drawer-header">
      <div class="cart-drawer-title">
        <span>🛒</span>
        <span>Quick Order Checkout</span>
      </div>
      <button type="button" class="cart-drawer-close" onclick="closeQuickOrderModal()" aria-label="Close Drawer">&times;</button>
    </div>
    
    <div class="cart-drawer-body">
      <!-- Item Info Box -->
      <div class="cart-item-preview">
        <img id="drawerItemIcon" src="{prefix}assets/images/icons/chatgpt-plus.svg" alt="Tool Icon" width="48" height="48" class="cart-item-icon">
        <div>
          <div class="cart-item-name" id="drawerItemName">ChatGPT Plus</div>
          <div class="cart-item-vendor" id="drawerItemVendor">OpenAI Enterprise Systems</div>
        </div>
      </div>

      <!-- Plan Duration Selection -->
      <div>
        <div class="cart-section-title">Select Subscription Duration:</div>
        <div class="duration-pills-grid">
          <div class="duration-pill active" data-months="1" onclick="selectCartDuration(1, 0)">
            <div>1 Month</div>
            <span class="duration-discount-tag">Standard</span>
          </div>
          <div class="duration-pill" data-months="3" onclick="selectCartDuration(3, 5)">
            <div>3 Months</div>
            <span class="duration-discount-tag">Save 5%</span>
          </div>
          <div class="duration-pill" data-months="12" onclick="selectCartDuration(12, 15)">
            <div>12 Months</div>
            <span class="duration-discount-tag">Save 15%</span>
          </div>
        </div>
      </div>

      <!-- Payment Rails Selection -->
      <div>
        <div class="cart-section-title">Select Payment Method:</div>
        <div class="payment-rails-selector">
          <div class="rail-option active" data-rail="EasyPaisa" onclick="selectCartRail('EasyPaisa')">
            <span>🟢</span><span>EasyPaisa</span>
          </div>
          <div class="rail-option" data-rail="JazzCash" onclick="selectCartRail('JazzCash')">
            <span>🔴</span><span>JazzCash</span>
          </div>
          <div class="rail-option" data-rail="SadaPay" onclick="selectCartRail('SadaPay')">
            <span>🟠</span><span>SadaPay</span>
          </div>
          <div class="rail-option" data-rail="Wise / Crypto" onclick="selectCartRail('Wise / Crypto')">
            <span>🌐</span><span>Wise / Crypto</span>
          </div>
        </div>
      </div>

      <!-- Live Price Calculation -->
      <div class="cart-summary-box">
        <div class="cart-summary-row">
          <span>Base Subtotal:</span>
          <span id="drawerSubtotal" style="font-weight:600;">Rs. 2,300 PKR</span>
        </div>
        <div class="cart-summary-row" id="drawerDiscountRow" style="display:none; color:#059669;">
          <span>Plan Discount:</span>
          <span id="drawerDiscount" style="font-weight:600;">- Rs. 0 PKR</span>
        </div>
        <div class="cart-total-row">
          <div>
            <div>Total Amount:</div>
            <div id="drawerTotalUsd" style="font-size:0.8rem; color:var(--text-muted); font-weight:normal;">(~$8.00 USD)</div>
          </div>
          <div class="cart-total-pkr" id="drawerTotalPkr">Rs. 2,300 PKR</div>
        </div>
      </div>

      <!-- SLA Guarantee Box -->
      <div class="cart-sla-box">
        <div><strong>⚡ Guaranteed 15-Minute Delivery:</strong> Credentials delivered directly to your WhatsApp with dedicated account configuration.</div>
        <div style="margin-top:0.35rem;"><strong>🛡️ 30-Day Full Replacement Warranty:</strong> Complete peace of mind with instant customer support.</div>
      </div>

      <!-- Checkout CTA -->
      <a id="drawerCheckoutBtn" href="https://wa.me/923326861112" target="_blank" rel="noopener noreferrer" class="cart-checkout-btn">
        <span>Proceed to WhatsApp Checkout &rarr;</span>
      </a>
      <div style="text-align:center; font-size:0.75rem; color:var(--text-muted);">
        Encrypted direct communication with official AIDigiTools Concierge (03326861112)
      </div>
    </div>
  </aside>

  <!-- ========================================================
       DYNAMIC FLOATING WHATSAPP CONCIERGE WIDGET
       ======================================================== -->
  <aside class="floating-wa-container" aria-label="Customer Support Concierge">
    <div class="floating-wa-badge">
      <span class="floating-wa-pulse"></span>
      <span class="floating-wa-status">🟢 Online • 15m Delivery</span>
    </div>
    <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20have%20a%20question%20about%20your%20verified%20software%20subscriptions." target="_blank" rel="noopener noreferrer" class="floating-wa-btn" aria-label="Chat with AIDigiTools on WhatsApp">
      <svg viewBox="0 0 32 32" width="28" height="28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path d="M16 2.5C8.54 2.5 2.5 8.54 2.5 16c0 2.61.74 5.05 2.02 7.12L2.6 29.4l6.45-1.89A13.43 13.43 0 0016 29.5c7.46 0 13.5-6.04 13.5-13.5S23.46 2.5 16 2.5zm6.83 19.22c-.28.81-1.65 1.56-2.32 1.62-.61.06-1.39.09-4.48-1.19-3.71-1.53-6.08-5.3-6.27-5.54-.18-.25-1.51-2-1.51-3.82s.95-2.7 1.29-3.07c.34-.36.74-.45 1-.45.24 0 .5 0 .71.01.24.01.56-.09.87.67.33.77 1.11 2.7 1.21 2.9.1.2.16.44.03.71-.13.26-.2.41-.39.64-.2.23-.41.5-.58.67-.2.19-.4.39-.17.79.23.39 1 1.65 2.15 2.67 1.48 1.32 2.73 1.73 3.12 1.93.39.19.61.16.84-.1.23-.26.98-1.14 1.24-1.54.27-.39.53-.33.9-.19.36.13 2.29 1.08 2.69 1.28.39.2.65.3.75.46.1.17.1.98-.18 1.79z" fill="#FFFFFF"/>
      </svg>
      <span class="floating-wa-label">WhatsApp Concierge</span>
    </a>
  </aside>

  <script src="{prefix}assets/cart.js"></script>"""

def upgrade_all_pages():
    html_files = sorted([p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)])
    print(f"Applying comprehensive redesign to {len(html_files)} HTML pages...")

    for f in html_files:
        is_root = (f.parent == ROOT)
        content = f.read_text(encoding="utf-8")

        # 1. Update header
        header_pattern = r"<header>.*?</header>"
        new_header = build_header(is_root)
        if re.search(header_pattern, content, re.DOTALL):
            content = re.sub(header_pattern, new_header, content, flags=re.DOTALL)

        # 2. Update footer
        footer_pattern = r"<footer>.*?</footer>"
        new_footer = build_footer(is_root)
        if re.search(footer_pattern, content, re.DOTALL):
            content = re.sub(footer_pattern, new_footer, content, flags=re.DOTALL)

        # 3. Clean any existing bottom widgets / scripts before </body> and reinsert fresh
        content = re.sub(r'<!-- =+\s*UNIVERSAL SLIDE-OVER QUICK ORDER.*?</body>', '</body>', content, flags=re.DOTALL)
        content = re.sub(r'<aside class="floating-wa-container".*?</body>', '</body>', content, flags=re.DOTALL)
        content = re.sub(r'<script src="[^"]*assets/cart\.js"></script>\s*</body>', '</body>', content, flags=re.DOTALL)
        
        # Insert fresh widgets before </body>
        bottom_markup = build_bottom_widgets(is_root)
        content = content.replace('</body>', f"{bottom_markup}\n</body>")

        # 4. For individual tool pages: enhance hero CTA with official brand icon and quick order button
        if f.parent.name == "tools":
            slug = f.stem
            if slug in catalog:
                tool = catalog[slug]
                # If brand icon not in hero, prepend brand icon
                if f'assets/images/icons/{slug}.svg' not in content:
                    hero_icon_tag = f'<div style="text-align:center; margin-bottom:1rem;"><img src="../assets/images/icons/{slug}.svg" alt="{tool["name"]} Logo" width="64" height="64" style="border-radius:14px; box-shadow:0 4px 14px rgba(15,23,42,0.08);"></div>\n      <h1>'
                    content = content.replace('<h1>', hero_icon_tag, 1)

                # Add quick order button next to btn-whatsapp if not present
                if 'openQuickOrderModal' not in content:
                    quick_btn = f'<div style="display:flex; justify-content:center; gap:0.75rem; flex-wrap:wrap; margin-top:1.25rem;"><button type="button" class="btn-primary" onclick="openQuickOrderModal(\'{slug}\')">⚡ Quick Order / Select Duration</button> '
                    content = re.sub(r'<a href="https://wa\.me/923326861112\?text=[^"]*" class="btn-whatsapp">', quick_btn + r'<a href="https://wa.me/923326861112" class="btn-whatsapp" target="_blank" rel="noopener noreferrer">', content)
                    if quick_btn in content:
                        content = re.sub(r'(class="btn-whatsapp"[^>]*>.*?</a>)', r'\1</div>', content)

        f.write_text(content, encoding="utf-8")

    print(f"Redesign successfully applied across all {len(html_files)} pages!")

if __name__ == "__main__":
    upgrade_all_pages()
