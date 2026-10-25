"""
Upgrade index.html for AIDigiTools:
1. Pic 1: Centerpiece Living Showcase Console with all 36 tools, categorized select, brand icon, specs link, and dual action buttons.
2. Pic 2: #toolsGrid with 36 cards featuring official SVG brand logos, soft typography, clean category badges, and workable buttons.
3. Pic 3: #pricing table with clean columns (Brand + Tool, Price PKR/USD, Payment Rails, 15m SLA & Warranty, Action Buttons).
4. Dynamic Floating WhatsApp Concierge at bottom-right (removed from top nav).
5. Universal Slide-Over Quick Order / Cart Drawer.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "index.html"
CATALOG_PATH = ROOT / "scripts" / "tools_catalog.json"

catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

# Group tools by category for showcase optgroups and pills
CATEGORIES_ORDER = [
    ("ai", "⭐ Featured AI Assistants", ["chatgpt-plus", "claude-pro", "gemini-advanced", "perplexity-pro", "grok-ai"]),
    ("coding", "💻 AI Coding & Developer Tools", ["cursor-pro", "github-copilot", "deepseek-pro", "jetbrains-all", "replit-core", "chatgpt-codex", "claude-artifacts"]),
    ("video", "🎬 AI Video & Audio Engines", ["capcut-pro", "runway-gen3", "kling-ai", "google-veo", "minimax-ai", "elevenlabs-creator", "suno-ai", "udio-ai"]),
    ("image", "🎨 Design, Image & Creative Studios", ["midjourney", "canva-pro", "adobe-creative-cloud", "figma-pro", "freepik-premium", "envato-elements", "leonardo-ai"]),
    ("vpn", "🔒 VPN & Workstation Privacy", ["nordvpn", "surfshark-vpn"]),
    ("productivity", "⚡ Productivity, SEO & Enterprise", ["semrush-guru", "notion-business", "linkedin-premium", "grammarly-pro", "quillbot-premium"]),
    ("streaming", "📺 Streaming & Entertainment", ["netflix-premium", "youtube-premium"])
]

def build_showcase_markup():
    # Options for dropdown
    options_html = []
    for cat_key, cat_title, slugs in CATEGORIES_ORDER:
        options_html.append(f'              <optgroup label="{cat_title}" data-cat="{cat_key}">')
        for slug in slugs:
            if slug in catalog:
                tool = catalog[slug]
                selected = ' selected' if slug == 'chatgpt-plus' else ''
                options_html.append(f'                <option value="{slug}"{selected}>{tool["name"]} — Rs. {int(tool["price_pkr"]):,} PKR / ${tool["price_usd"]} USD</option>')
        options_html.append('              </optgroup>')
    select_options = "\n".join(options_html)

    return f"""    <!-- ========================================================
         AUTHKIT LIVING COMPONENT WIDGET (CENTERPIECE)
         Featuring Traveling Laser Border-Beam & All 36 Tools
         ======================================================== -->
    <div class="authkit-widget-wrapper border-beam-card" id="showcase">
      <div class="authkit-widget-card">
        <!-- Interactive Category Switcher Pills -->
        <div class="authkit-cat-filter-pills" role="tablist" aria-label="Tool Categories">
          <button type="button" class="authkit-cat-pill active" onclick="filterShowcaseCategory('all', this)">⭐ All 36 Tools</button>
          <button type="button" class="authkit-cat-pill" onclick="filterShowcaseCategory('ai', this)">🤖 AI Assistants</button>
          <button type="button" class="authkit-cat-pill" onclick="filterShowcaseCategory('coding', this)">💻 AI Coding</button>
          <button type="button" class="authkit-cat-pill" onclick="filterShowcaseCategory('video', this)">🎬 AI Video &amp; Audio</button>
          <button type="button" class="authkit-cat-pill" onclick="filterShowcaseCategory('image', this)">🎨 Design &amp; Image</button>
          <button type="button" class="authkit-cat-pill" onclick="filterShowcaseCategory('vpn', this)">🔒 VPN &amp; Privacy</button>
          <button type="button" class="authkit-cat-pill" onclick="filterShowcaseCategory('productivity', this)">⚡ Productivity &amp; SEO</button>
        </div>

        <!-- Quick Select Dropdown for all 36 tools -->
        <div style="margin-bottom: 1.25rem;">
          <label for="showcaseToolSelect" style="display:block; font-size:0.82rem; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; color:var(--text-secondary); margin-bottom:0.4rem;">Select Any Software Tool to Test Live Pricing &amp; Rails:</label>
          <select id="showcaseToolSelect" class="authkit-tool-select" onchange="setMasterTool(this.value)">
{select_options}
          </select>
        </div>

        <!-- Dynamic Tool Interactive Grid -->
        <div class="authkit-widget-grid">
          <div>
            <div class="authkit-showcase-header">
              <img id="mToolIcon" src="assets/images/icons/chatgpt-plus.svg" alt="ChatGPT Plus Official Logo" width="56" height="56" class="authkit-brand-icon">
              <div>
                <div class="authkit-vendor-pill" id="mToolVendor">OpenAI Enterprise Systems</div>
                <h3 class="authkit-tool-title" id="mToolTitle" style="margin:0; font-size:1.4rem;">ChatGPT Plus Subscription</h3>
              </div>
            </div>
            
            <p class="authkit-tool-desc" id="mToolDesc" style="margin-top:0.75rem;">Full access to GPT-4o, Custom GPTs, Advanced Voice Mode, and DALL-E 3 image generation without foreign cards.</p>
            
            <div class="authkit-price-row" style="margin:1rem 0;">
              <span class="authkit-price-val" id="mToolPrice" style="color:#0284C7; font-weight:700;">Rs. 2,300</span>
              <span class="authkit-price-sub" id="mToolPriceSub">PKR (~$8.00 USD) / month</span>
            </div>

            <ul class="authkit-features-list">
              <li><span class="check">✓</span><span>15-Minute Instant WhatsApp Delivery SLA</span></li>
              <li><span class="check">✓</span><span>30-Day Guaranteed Replacement Warranty</span></li>
              <li><span class="check">✓</span><span>Settled in Domestic PKR or USD (Zero Forex Surcharges)</span></li>
            </ul>

            <div style="margin-top:1rem;">
              <a id="mSpecsLink" href="tools/chatgpt-plus.html" style="font-size:0.88rem; font-weight:600; color:#0284C7; text-decoration:none;">View Full Specs &amp; Benchmarks for ChatGPT Plus →</a>
            </div>
          </div>

          <!-- Instant Order Simulator Box -->
          <div class="authkit-simulator-box">
            <div>
              <div class="authkit-rails-title">Supported Rails (Domestic &amp; Global):</div>
              <div class="authkit-rails-grid">
                <div class="authkit-rail-item">EasyPaisa</div>
                <div class="authkit-rail-item">JazzCash</div>
                <div class="authkit-rail-item">SadaPay</div>
                <div class="authkit-rail-item">Wise &amp; Crypto</div>
              </div>
              <div class="authkit-badge-nofx">⚡ Serving Pakistan &amp; Worldwide (PKR / USD)</div>
            </div>
            
            <div class="authkit-showcase-actions">
              <a id="mWaLink" href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20ChatGPT%20Plus%20for%20Rs%202300%20PKR%20/%20$8.00%20USD." target="_blank" rel="noopener noreferrer" class="btn-primary" style="width: 100%; display: flex; align-items: center; justify-content: center; gap: 0.5rem; text-decoration: none;">
                <span>Instant Order on WhatsApp &rarr;</span>
              </a>
              <button type="button" onclick="openQuickOrderModal(document.getElementById('showcaseToolSelect').value)" class="btn-quick-order" style="width: 100%;">
                <span>🛒 Open Quick Order Drawer (1 / 3 / 12 Mo)</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>"""

def build_tools_grid_markup():
    cards = []
    for slug, tool in catalog.items():
        cat_key = tool["category_key"]
        cat_label = tool["category_label"]
        pkr_str = f"{int(tool['price_pkr']):,}"
        usd_str = tool["price_usd"]
        
        wa_text = f"Hi AIDigiTools, I want to order {tool['name']} for Rs {tool['price_pkr']} PKR / ${usd_str} USD"
        wa_url = f"https://wa.me/923326861112?text={wa_text.replace(' ', '%20')}"
        
        card_html = f"""        <div class="card tool-card" data-category="{cat_key} {cat_label.lower()}">
          <div>
            <div class="tool-card-header">
              <img src="{tool['icon']}" alt="{tool['name']} Official Logo" width="46" height="46" class="tool-brand-logo" loading="lazy">
              <span class="tool-cat-badge">{cat_label}</span>
            </div>
            <h3 class="tool-card-title">{tool['name']}</h3>
            <span class="tool-card-vendor">{tool['vendor']}</span>
            <p class="tool-card-desc">{tool['description']}</p>
            <div class="price-tag"><span class="price-amount">Rs. {pkr_str} PKR</span> <span class="price-period">(~${usd_str} USD) / month</span></div>
            <ul class="tool-card-checklist">
              <li><span class="check-icon">✓</span> 15-Minute Instant WhatsApp Delivery SLA</li>
              <li><span class="check-icon">✓</span> 30-Day Guaranteed Replacement Warranty</li>
              <li><span class="check-icon">✓</span> EasyPaisa, JazzCash, SadaPay, Wise &amp; Crypto</li>
            </ul>
          </div>
          <div class="tool-card-actions">
            <div class="tool-card-cta-row">
              <button type="button" class="btn-quick-order" onclick="openQuickOrderModal('{slug}')">⚡ Quick Order</button>
              <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="btn-wa-subtle">WhatsApp</a>
            </div>
            <a href="{tool['url']}" class="tool-specs-link">View Full Specs &amp; Benchmark Data →</a>
          </div>
        </div>"""
        cards.append(card_html)
    return "\n\n".join(cards)

def build_pricing_table_markup():
    rows = []
    for slug, tool in catalog.items():
        pkr_str = f"{int(tool['price_pkr']):,}"
        usd_str = tool["price_usd"]
        wa_text = f"Hi AIDigiTools, I want to order {tool['name']} for Rs {tool['price_pkr']} PKR / ${usd_str} USD"
        wa_url = f"https://wa.me/923326861112?text={wa_text.replace(' ', '%20')}"

        row_html = f"""          <tr>
            <td>
              <div class="pricing-tool-cell">
                <img src="{tool['icon']}" alt="{tool['name']} Icon" width="34" height="34" class="pricing-tool-icon" loading="lazy">
                <div class="pricing-tool-info">
                  <span class="pricing-tool-name">{tool['name']}</span>
                  <span class="pricing-tool-vendor">{tool['vendor']}</span>
                </div>
              </div>
            </td>
            <td>
              <div class="pricing-pkr-val">Rs. {pkr_str} PKR</div>
              <div class="pricing-usd-val">~${usd_str} USD / mo</div>
            </td>
            <td>EasyPaisa, JazzCash, SadaPay, Wise, Crypto</td>
            <td>
              <span class="pricing-sla-badge">✓ 15-Minute SLA</span><br>
              <span style="font-size:0.78rem; color:var(--text-muted);">30-Day Replacement Guarantee</span>
            </td>
            <td>
              <div class="pricing-table-actions">
                <button type="button" class="btn-table-order" onclick="openQuickOrderModal('{slug}')">Quick Order</button>
                <a href="{tool['url']}" class="btn-table-specs">Specs →</a>
              </div>
            </td>
          </tr>"""
        rows.append(row_html)
    
    rows_markup = "\n".join(rows)

    return f"""    <section id="pricing" style="margin-top: 4.5rem;">
      <h2 class="section-title">Transparent Domestic &amp; Worldwide Pricing</h2>
      <p class="section-subtitle">Real numbers with zero hidden exchange conversion surcharges across all 36 tools.</p>
      
      <div class="table-responsive">
        <table>
          <thead>
            <tr>
              <th>Tool &amp; Platform</th>
              <th>Monthly Price (PKR / USD)</th>
              <th>Payment Methods</th>
              <th>Delivery SLA &amp; Warranty</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
{rows_markup}
          </tbody>
        </table>
      </div>
    </section>"""

def build_cart_drawer_and_floating_wa():
    return """  <!-- ========================================================
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
        <img id="drawerItemIcon" src="assets/images/icons/chatgpt-plus.svg" alt="Tool Icon" width="48" height="48" class="cart-item-icon">
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
  
  <script src="assets/cart.js"></script>"""

def main():
    content = INDEX_PATH.read_text(encoding="utf-8")

    # 1. Replace Showcase Console
    showcase_pattern = re.compile(
        r'<!-- =+\s*AUTHKIT LIVING COMPONENT WIDGET.*?<!-- Category Hub Navigation -->',
        re.DOTALL
    )
    if not showcase_pattern.search(content):
        # Alternative pattern
        showcase_pattern = re.compile(
            r'<div class="authkit-widget-wrapper border-beam-card">.*?<!-- Category Hub Navigation -->',
            re.DOTALL
        )
    
    new_showcase = build_showcase_markup() + "\n\n    <!-- Category Hub Navigation -->"
    content = showcase_pattern.sub(new_showcase, content, count=1)

    # 2. Replace #toolsGrid
    grid_pattern = re.compile(r'<div class="grid" id="toolsGrid">.*?</div>\s*</section>\s*<section id="pricing"', re.DOTALL)
    new_grid = f'<div class="grid" id="toolsGrid">\n{build_tools_grid_markup()}\n      </div>\n    </section>\n\n    <section id="pricing"'
    content = grid_pattern.sub(new_grid, content, count=1)

    # 3. Replace #pricing section
    pricing_pattern = re.compile(r'<section id="pricing".*?</section>\s*<section style="margin-top: 4.5rem;">\s*<h2 class="section-title">Frequently Asked Questions</h2>', re.DOTALL)
    new_pricing = build_pricing_table_markup() + '\n\n    <section style="margin-top: 4.5rem;">\n      <h2 class="section-title">Frequently Asked Questions</h2>'
    content = pricing_pattern.sub(new_pricing, content, count=1)

    # 4. Remove WhatsApp button from top nav in index.html
    # Replace nav-cta in header
    content = re.sub(
        r'<a href="https://wa\.me/923326861112"[^>]*class="nav-cta"[^>]*>.*?</a>',
        '<button type="button" onclick="openQuickOrderModal(\'chatgpt-plus\')" class="nav-cta" style="border:none; cursor:pointer;"><span>🛒 Quick Order</span></button>',
        content,
        flags=re.DOTALL
    )

    # 5. Add Cart Drawer and Floating WhatsApp widget before </body>
    # First remove any old scripts and existing drawer/widget if present
    content = re.sub(r'<!-- =+\s*UNIVERSAL SLIDE-OVER QUICK ORDER.*?</body>', '</body>', content, flags=re.DOTALL)
    content = re.sub(r'<aside class="floating-wa-container".*?</body>', '</body>', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*var mData = \{.*?</script>\s*</body>', '</body>', content, flags=re.DOTALL)

    content = content.replace('</body>', build_cart_drawer_and_floating_wa() + '\n</body>')

    INDEX_PATH.write_text(content, encoding="utf-8")
    print(f"Successfully upgraded {INDEX_PATH} with Living Showcase (all 36 tools), #toolsGrid, #pricing table, and drawer!")

if __name__ == "__main__":
    main()
