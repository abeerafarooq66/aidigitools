# scripts/generate_candidate_tool_pages.py
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, "scripts", "tools_catalog.json")

with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

CANDIDATE_SLUGS = ["spotify-premium", "duolingo-super", "discord-nitro", "zoom-workplace"]

template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Buy {name} in Pakistan & Worldwide | Pricing & Plans</title>
  <meta name="description" content="Buy {name} in Pakistan and worldwide from Rs. {min_pkr:,} PKR (~${min_usd:.2f} USD). 15-minute delivery, EasyPaisa, JazzCash, 30-day warranty.">
  <link rel="canonical" href="https://aidigitools.tech/tools/{slug}.html">
  <link rel="alternate" hreflang="x-default" href="https://aidigitools.tech/tools/{slug}.html">
  <link rel="alternate" hreflang="en" href="https://aidigitools.tech/tools/{slug}.html">
  <link rel="alternate" hreflang="en-PK" href="https://aidigitools.tech/tools/{slug}.html">
  <link rel="stylesheet" href="../assets/style.css">
  <meta property="og:title" content="Buy {name} in Pakistan & Worldwide | Pricing & Plans">
  <meta property="og:description" content="Buy {name} in Pakistan and worldwide from Rs. {min_pkr:,} PKR (~${min_usd:.2f} USD). 15-minute delivery, EasyPaisa, JazzCash, 30-day warranty.">
  <meta property="og:url" content="https://aidigitools.tech/tools/{slug}.html">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{name} Pakistan & Worldwide — AIDigiTools">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "{name} Subscription",
    "description": "{desc}",
    "brand": {{
      "@type": "Brand",
      "name": "{brand}"
    }},
    "offers": {{
      "@type": "AggregateOffer",
      "lowPrice": "{min_pkr}",
      "priceCurrency": "PKR",
      "offerCount": "{num_plans}",
      "availability": "https://schema.org/InStock",
      "url": "https://aidigitools.tech/tools/{slug}.html"
    }},
    "image": "https://aidigitools.tech/assets/product-logos/{slug}.svg"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://aidigitools.tech/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "Tools",
        "item": "https://aidigitools.tech/#products"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{name}",
        "item": "https://aidigitools.tech/tools/{slug}.html"
      }}
    ]
  }}
  </script>
  <link rel="icon" type="image/svg+xml" href="../favicon.svg">
</head>
<body>
  <header>
    <div class="container nav-wrapper">
      <a href="../index.html" class="logo" aria-label="AIDigiTools Home">
        <svg class="logo-brand-icon" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <defs>
            <linearGradient id="navTeal" x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#00E5A3"/>
              <stop offset="100%" stop-color="#00B4D8"/>
            </linearGradient>
            <linearGradient id="navPurple" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#0077B6"/>
              <stop offset="50%" stop-color="#4361EE"/>
              <stop offset="100%" stop-color="#8B5CF6"/>
            </linearGradient>
            <linearGradient id="navOrbit" x1="0%" y1="50%" x2="100%" y2="50%">
              <stop offset="0%" stop-color="#00E5A3"/>
              <stop offset="50%" stop-color="#00B4D8"/>
              <stop offset="100%" stop-color="#8B5CF6"/>
            </linearGradient>
          </defs>
          <path class="orbit-back" d="M 12 62 C 12 36, 126 18, 134 38" stroke="url(#navOrbit)" stroke-width="3.5" stroke-linecap="round" fill="none" opacity="0.65"/>
          <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" fill="url(#navTeal)"/>
          <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" fill="url(#navPurple)"/>
          <path d="M 46 64 C 52 58, 66 56, 80 62 L 72 74 C 62 70, 52 72, 46 76 Z" fill="url(#navTeal)" opacity="0.95"/>
          <path class="orbit-front" d="M 134 38 C 142 58, 38 88, 16 66" stroke="url(#navOrbit)" stroke-width="4" stroke-linecap="round" fill="none"/>
          <circle cx="124" cy="34" r="5.5" fill="#4361EE"/>
        </svg>
        <span class="logo-text-wrap">
          <span class="logo-brand-name"><span class="ai-prefix">AI</span> DigiTools</span>
          <span class="tagline">SMART TOOLS • BIGGER POSSIBILITIES</span>
        </span>
      </a>
      <nav>
        <a href="../index.html#products">Products</a>
        <a href="../deals.html">Deals</a>
        <a href="../categories/video.html">Video</a>
        <a href="../categories/coding.html">Coding</a>
        <a href="../categories/vpn.html">VPN</a>
        <a href="../categories/image.html">Image</a>
        <a href="../shipping-policy.html">Delivery</a>
        <a href="../policies.html#payments">Payments</a>
        <a href="../contact.html">Contact</a>
        <button type="button" onclick="openQuickOrderModal('{slug}')" class="nav-cta" style="border:none; cursor:pointer;" aria-label="Open Quick Order">
          <span>⚡ Quick Order</span>
        </button>
      </nav>
    </div>
  </header>

  <main class="container">
    <section class="hero">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol>
          <li><a href="../index.html">Home</a></li>
          <li><a href="../index.html#products">Tools</a></li>
          <li><span aria-current="page">{name}</span></li>
        </ol>
      </nav>

      <div class="reseller-notice" style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:8px; padding:0.6rem 1rem; font-size:0.82rem; color:var(--text-muted); margin-bottom:1.5rem; text-align:center;">
        <strong>Official Reseller Notice:</strong> AIDigiTools is an independent software subscription aggregator. All brand names, registered trademarks, and logos belong to their respective copyright holders.
      </div>

      <div style="text-align:center; margin-bottom:1rem;">
        <img src="../assets/product-logos/{slug}.svg" alt="{name} Official Logo" width="64" height="64" style="border-radius:14px; box-shadow:0 4px 14px rgba(15,23,42,0.08);">
      </div>

      <h1>{name} in Pakistan & Worldwide — Pricing & Verified Plans</h1>
      <p class="quick-answer">
        {desc} Available on AIDigiTools starting from Rs. {min_pkr:,} PKR (~${min_usd:.2f} USD). Pay seamlessly with EasyPaisa, JazzCash, SadaPay, or Crypto. Guaranteed 15-minute electronic delivery via WhatsApp backed by our 30-day replacement warranty.
      </p>

      <div class="price-tag">Starting from Rs. {min_pkr:,} PKR <span class="period">(~${min_usd:.2f} USD)</span></div>
      <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20{name}%20for%20Rs%20{min_pkr}%20PKR" class="btn-whatsapp">Order {name} on WhatsApp</a>
      <a href="#compare-plans" class="btn-secondary" style="margin-left:0.6rem; display:inline-flex; align-items:center; gap:0.4rem; padding:0.85rem 1.4rem; border-radius:12px; font-weight:700; text-decoration:none; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-color); vertical-align:middle;">Compare {num_plans} Plans ↓</a>
    </section>

    <!-- Canonical Plan Comparison Section -->
    <section class="plans-comparison-section" id="compare-plans">
      <h2 class="section-title">Compare Verified {name} Plans</h2>
      <p class="section-subtitle">Genuinely distinct official plan variants with transparent Pakistani pricing and verified SLA terms.</p>
      <div class="plans-grid">
{plan_cards}
      </div>
    </section>

    <section style="margin-top: 3.5rem;">
      <h2 class="section-title">{name} Technical Specifications & Performance</h2>
      <p class="section-subtitle">Verified operational limits and platform attributes.</p>
      <table>
        <thead>
          <tr>
            <th>System Parameter</th>
            <th>Technical Specification</th>
            <th>Verification Standard</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Platform Compatibility</strong></td>
            <td>Web, Windows, macOS, Android, iOS</td>
            <td>Full Cross-Device Cloud Sync</td>
          </tr>
          <tr>
            <td><strong>Delivery SLA</strong></td>
            <td>Guaranteed within 15 minutes</td>
            <td>WhatsApp Electronic Dispatch</td>
          </tr>
          <tr>
            <td><strong>Payment Options</strong></td>
            <td>EasyPaisa, JazzCash, SadaPay, Wise, Crypto</td>
            <td>Zero Forex Conversion Surcharges</td>
          </tr>
          <tr>
            <td><strong>Warranty Guarantee</strong></td>
            <td>30-Day Full Replacement Protection</td>
            <td>Direct Helpline Resolution</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>

  <!-- Slide-Over Quick Order / Cart Drawer -->
  <div class="cart-drawer-backdrop" id="cartBackdrop" onclick="closeQuickOrderModal()"></div>
  <aside class="cart-drawer" id="cartDrawer" aria-label="Quick Order Checkout">
    <div class="cart-drawer-header">
      <div class="cart-drawer-title">
        <span>⚡</span>
        <span>Quick Order Checkout</span>
      </div>
      <button type="button" class="cart-drawer-close" onclick="closeQuickOrderModal()" aria-label="Close Drawer">&times;</button>
    </div>
    <div class="cart-drawer-body">
      <div class="cart-item-preview">
        <img id="drawerItemIcon" src="../assets/product-logos/{slug}.svg" alt="Tool Icon" width="48" height="48" class="cart-item-icon">
        <div>
          <div class="cart-item-name" id="drawerItemName">{name}</div>
          <div class="cart-item-vendor" id="drawerItemVendor">{brand}</div>
        </div>
      </div>
      <div id="drawerPlanSelectorContainer" style="margin-bottom: 1.25rem;"></div>
      <div class="cart-section-title">Select Payment Method:</div>
      <div class="payment-rails-grid">
        <button type="button" class="rail-option active" data-rail="EasyPaisa" onclick="selectCartRail('EasyPaisa')">EasyPaisa</button>
        <button type="button" class="rail-option" data-rail="JazzCash" onclick="selectCartRail('JazzCash')">JazzCash</button>
        <button type="button" class="rail-option" data-rail="SadaPay" onclick="selectCartRail('SadaPay')">SadaPay</button>
        <button type="button" class="rail-option" data-rail="Bank IBFT" onclick="selectCartRail('Bank IBFT')">Bank Transfer</button>
      </div>
    </div>
    <div class="cart-drawer-footer">
      <div class="cart-drawer-total">
        <span>Total:</span>
        <span id="drawerTotalPkr">Rs. {min_pkr:,} PKR</span>
      </div>
      <a href="#" id="drawerCheckoutBtn" class="btn-checkout" target="_blank" rel="noopener noreferrer">Proceed to WhatsApp Order</a>
    </div>
  </aside>

  <script src="../assets/cart.js"></script>
</body>
</html>
'''

for slug in CANDIDATE_SLUGS:
    tool = catalog.get(slug)
    if not tool:
        continue
    
    plans = tool["plans"]
    min_pkr = min(p["price_pkr"] for p in plans)
    min_usd = min(p["price_usd"] for p in plans)
    
    plan_cards = []
    for plan in plans:
        badge = f'<div class="plan-badge-top">{plan["badge"]}</div>' if plan.get("badge") else ""
        feats = "\n".join([f'          <li class="plan-feature-item"><span class="plan-feature-check">✓</span><span>{f}</span></li>' for f in plan.get("features", [])])
        card = f'''      <div class="plan-card" id="plan-{plan['plan_id']}">
        {badge}
        <div class="plan-tier-label">{plan.get('plan_type', 'Tier')}</div>
        <h3 class="plan-title">{plan['name']}</h3>
        <div class="plan-price-wrap">
          <span class="plan-price-pkr">Rs. {plan['price_pkr']:,}</span>
          <span class="plan-price-sub">PKR (~${plan['price_usd']:.2f} USD) / {plan['duration']}</span>
        </div>
        <div class="plan-meta-row">
          <span class="plan-pill">⏱ {plan['duration']}</span>
          <span class="plan-pill">👤 {plan['seats']}</span>
        </div>
        <ul class="plan-features-list">
{feats}
        </ul>
        <div class="plan-terms-note">
          <strong>Terms:</strong> {plan['limits']}
        </div>
        <button type="button" class="btn-choose-plan" onclick="openQuickOrderModal('{slug}', '{plan['plan_id']}')">
          <span>Choose {plan['name']}</span>
          <span>→</span>
        </button>
      </div>'''
        plan_cards.append(card)

    cards_joined = "\n".join(plan_cards)
    page_html = template.format(
        slug=slug,
        name=tool["name"],
        desc=tool["description"],
        brand=tool.get("brand", "Official Platform"),
        min_pkr=min_pkr,
        min_usd=min_usd,
        num_plans=len(plans),
        plan_cards=cards_joined
    )

    dest_path = os.path.join(BASE_DIR, "tools", f"{slug}.html")
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"Created candidate tool page: {dest_path}")

print("Candidate pages creation complete!")
