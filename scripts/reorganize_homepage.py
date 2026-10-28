import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INDEX_PATH = os.path.join(REPO_ROOT, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    orig_html = f.read()

# 1. toolsGrid
grid_start = orig_html.find('<div class="grid" id="toolsGrid">')
grid_end = orig_html.find('</section>', grid_start)
tools_grid_html = orig_html[grid_start:grid_end].strip()

# 2. showcase
showcase_start = orig_html.find('id="showcase"')
showcase_box_start = orig_html.rfind('<div class="authkit-widget-wrapper', 0, showcase_start)
actions_pos = orig_html.find('class="authkit-showcase-actions"', showcase_start)
showcase_end = orig_html.find('<!-- Category Hub Navigation -->', actions_pos)
if showcase_end == -1:
    showcase_end = orig_html.find('<section', actions_pos)
showcase_html = orig_html[showcase_box_start:showcase_end].strip()

# 3. search bar
search_start = orig_html.find('<!-- Live Search & Filter Bar -->')
search_end = orig_html.find('<section id="products"', search_start)
search_bar_html = orig_html[search_start:search_end].strip()

# 4. pricing table
pricing_start = orig_html.find('<div class="table-responsive">')
pricing_end = orig_html.find('</div>', orig_html.find('</table>', pricing_start)) + 6
pricing_table_html = orig_html[pricing_start:pricing_end].strip()

# 5. drawers and modals
drawer_start = orig_html.find('<div class="cart-drawer-backdrop"')
drawer_end = orig_html.find('</body>', drawer_start)
drawers_html = orig_html[drawer_start:drawer_end].strip()

tool_cards = re.findall(r'<div class="card tool-card"[^>]*>', tools_grid_html)
print(f"Extracted toolsGrid with {len(tool_cards)} tool cards.")
assert len(tool_cards) == 49, f"Expected 49 tool cards, found {len(tool_cards)}"

# Define new FAQ questions & answers matching both DOM and JSON-LD
faqs = [
    {
        "q": "Are direct subscription purchases currently available on AIDigiTools?",
        "a": "Direct paid orders are currently paused while supplier licensing and resale permissions undergo verification. Visitors may use WhatsApp for non-binding informational inquiries regarding availability and workflows."
    },
    {
        "q": "How are reference prices determined and should I verify them?",
        "a": "Prices displayed in PKR and USD are informational benchmarks based on prevailing marketplace rates and domestic payment rails. Current retail prices should always be confirmed directly on the official tool provider's website."
    },
    {
        "q": "Is AIDigiTools affiliated with OpenAI, Anthropic, or other tool providers?",
        "a": "No. AIDigiTools is an independent directory and software concierge desk. All product names, logos, and trademarks belong exclusively to their respective owners."
    },
    {
        "q": "Where can I find in-depth tool comparisons and guides?",
        "a": "Visit our Guides and Comparisons section to read head-to-head shootouts such as ChatGPT vs Claude and Runway vs Pika, or browse our Best AI Coding Tools and Best AI Video Generators rankings."
    },
    {
        "q": "How do I report outdated pricing or request a new tool review?",
        "a": "You can reach our team via WhatsApp at 03326861112 or email support@aidigitools.tech to submit updates, report discrepancies, or request editorial coverage."
    }
]

faq_jsonld_items = []
for item in faqs:
    faq_jsonld_items.append(f"""      {{
        "@type": "Question",
        "name": "{item['q']}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{item['a']}"
        }}
      }}""")
faq_jsonld_str = ",\n".join(faq_jsonld_items)

faq_cards_html = []
for item in faqs:
    faq_cards_html.append(f"""        <div class="card">
          <h2>{item['q']}</h2>
          <p>{item['a']}</p>
        </div>""")
faq_cards_str = "\n".join(faq_cards_html)

new_index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AIDigiTools — AI Tools Directory, Comparisons &amp; Guides</title>
  <meta name="description" content="Discover 49 verified AI tools, coding assistants, creative video suites, and benchmark guides. Compare features and reference prices on AIDigiTools.">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <!-- Google Search Console Verification: Insert token from GSC below when connecting property -->
  <!-- <meta name="google-site-verification" content="YOUR_GSC_VERIFICATION_TOKEN"> -->
  <!-- Bing Webmaster Tools Verification: Insert token from Bing below when connecting property -->
  <!-- <meta name="msvalidate.01" content="YOUR_BING_VERIFICATION_TOKEN"> -->
  <link rel="canonical" href="https://aidigitools.tech/">
  <link rel="alternate" hreflang="x-default" href="https://aidigitools.tech/">
  <link rel="alternate" hreflang="en" href="https://aidigitools.tech/">
  <link rel="alternate" hreflang="en-PK" href="https://aidigitools.tech/">
  <link rel="stylesheet" href="assets/style.css">
  <meta property="og:site_name" content="AI DigiTools">
  <meta property="og:type" content="website">
  <meta property="og:title" content="AIDigiTools — AI Tools Directory, Comparisons &amp; Guides">
  <meta property="og:description" content="Discover 49 verified AI tools, coding assistants, creative video suites, and benchmark guides with transparent reference pricing.">
  <meta property="og:url" content="https://aidigitools.tech/">
  <meta property="og:image" content="https://aidigitools.tech/assets/images/aidigitools-orbit-emblem.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="AI DigiTools — Verified AI Software Directory &amp; Guides">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@aidigitools">
  <meta name="twitter:title" content="AIDigiTools — AI Tools Directory, Comparisons &amp; Guides">
  <meta name="twitter:description" content="Discover 49 verified AI tools, coding assistants, creative video suites, and benchmark guides with transparent reference pricing.">
  <meta name="twitter:image" content="https://aidigitools.tech/assets/images/aidigitools-orbit-emblem.png">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "AIDigiTools",
    "url": "https://aidigitools.tech/",
    "potentialAction": {{
      "@type": "SearchAction",
      "target": "https://aidigitools.tech/#products",
      "query-input": "required name=search_term_string"
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{faq_jsonld_str}
    ]
  }}
  </script>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "AIDigiTools",
    "url": "https://aidigitools.tech/",
    "logo": "https://aidigitools.tech/assets/images/aidigitools-logo.svg",
    "description": "Premier verified AI software subscription marketplace and digital tools concierge serving Pakistan and worldwide.",
    "email": "support@aidigitools.tech",
    "telephone": "+92-332-6861112",
    "contactPoint": [
      {{
        "@type": "ContactPoint",
        "telephone": "+92-332-6861112",
        "contactType": "customer service",
        "contactOption": "TollFree",
        "areaServed": ["PK", "Worldwide"],
        "availableLanguage": ["en", "ur"]
      }}
    ],
    "sameAs": [
      "https://github.com/abeerafarooq66/aidigitools"
    ]
  }}
  </script>
</head>
<body class="homepage-theme">
  <header>
    <div class="container nav-wrapper">
      <a href="index.html" class="logo" aria-label="AIDigiTools Home">
        <svg class="logo-brand-icon" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
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
        </svg>
        <span class="logo-text-wrap">
          <span class="logo-brand-name"><span class="ai-prefix">AI</span> DigiTools</span>
          <span class="tagline">SMART TOOLS • BIGGER POSSIBILITIES</span>
        </span>
      </a>
      <nav>
        <a href="index.html#products">Directory</a>
        <a href="#categories">Categories</a>
        <a href="#pricing">Pricing</a>
        <a href="#guides">Guides</a>
        <a href="deals.html">Deals</a>
        <a href="shipping-policy.html">Delivery</a>
        <a href="policies.html#payments">Payments</a>
        <a href="contact.html">Contact</a>
        <button type="button" onclick="openQuickOrderModal('chatgpt-plus')" class="nav-cta" style="border:none; cursor:pointer;" aria-label="Open Quick Inquiry">
          <span>🛒 Quick Order</span>
        </button>
      </nav>
    </div>
  </header>

  <main class="container">
    <!-- ========================================================
         SECTION A: HERO
         ======================================================== -->
    <section class="hero">
      <h1>AIDigiTools — AI Tools Directory, Comparisons &amp; Guides</h1>
      <p class="quick-answer">
        AIDigiTools is an independent AI software directory and tools resource hub. Browse curated profiles, feature comparisons, and benchmark guides across 49 popular AI assistants, coding engines, and creative video generators with transparent informational reference pricing and verified domestic PKR payment workflows.
      </p>
      <div class="badges-row">
        <span class="badge">🇵🇰 EasyPaisa &amp; JazzCash</span>
        <span class="badge">🌍 Wise &amp; Crypto USDT</span>
        <span class="badge">SadaPay &amp; Raast</span>
        <span class="badge emerald">15-Min Delivery Target</span>
        <span class="badge">30-Day Replacement Warranty</span>
      </div>
      <div style="display:flex; justify-content:center; align-items:center; gap:0.75rem; flex-wrap:wrap; margin-top:1.5rem; position:relative; z-index:1;">
        <a href="#products" class="btn btn-primary" style="text-decoration:none; display:inline-flex; align-items:center; gap:0.4rem; padding:0.65rem 1.35rem; font-weight:700;">
          <span>🔍 Explore 49 AI Tools</span>
        </a>
        <a href="#categories" class="btn btn-secondary" style="text-decoration:none; display:inline-flex; align-items:center; gap:0.4rem; padding:0.65rem 1.25rem; font-weight:600; background:#FFFFFF; border:1.5px solid #CBD5E1; color:#0F172A;">
          <span>📂 Browse Categories</span>
        </a>
        <a href="#guides" class="btn btn-secondary" style="text-decoration:none; display:inline-flex; align-items:center; gap:0.4rem; padding:0.65rem 1.25rem; font-weight:600; background:#FFFFFF; border:1.5px solid #CBD5E1; color:#0F172A;">
          <span>📖 Benchmark Guides</span>
        </a>
      </div>
    </section>

    <!-- ========================================================
         SECTION B: EXPLORE CATEGORIES
         ======================================================== -->
    <section id="categories" style="margin-top: 3.5rem; margin-bottom: 2.5rem;">
      <div style="text-align:center; max-width:760px; margin:0 auto 1.75rem;">
        <span class="badge" style="background:#E0F2FE; color:#0284C7; border:1px solid #BAE6FD; font-weight:700;">📂 Specialized Hubs</span>
        <h2 style="font-size:1.85rem; font-weight:800; letter-spacing:-0.03em; color:#0F172A; margin:0.45rem 0 0.35rem;">Explore AI Tool Categories</h2>
        <p style="font-size:0.95rem; color:#475569; margin:0;">Targeted directories built for engineers, creators, digital agencies, and researchers.</p>
      </div>

      <div class="category-cards-grid">
        <a href="categories/coding.html" class="category-card">
          <div>
            <div class="category-card-icon">💻</div>
            <h3 class="category-card-title">AI Coding &amp; Dev Tools</h3>
            <p class="category-card-desc">Frontier code generation, SWE-bench reasoning, and IDE assistants including Claude Pro, Cursor, Copilot, Lovable, and JetBrains.</p>
          </div>
          <span class="category-card-link">Explore 18 Coding Tools &rarr;</span>
        </a>

        <a href="categories/video.html" class="category-card">
          <div>
            <div class="category-card-icon">🎬</div>
            <h3 class="category-card-title">AI Video &amp; Motion Studios</h3>
            <p class="category-card-desc">Cinematic video synthesis, multilingual voice dubbing, and automated editing tools like Runway Gen-3, Kling AI, HeyGen, and CapCut.</p>
          </div>
          <span class="category-card-link">Explore 10 Video Tools &rarr;</span>
        </a>

        <a href="categories/image.html" class="category-card">
          <div>
            <div class="category-card-icon">🎨</div>
            <h3 class="category-card-title">Design, Image &amp; Creative</h3>
            <p class="category-card-desc">Photorealistic generative art, vector design, and stock visual platforms including Midjourney, Canva Pro, Figma Pro, and Adobe CC.</p>
          </div>
          <span class="category-card-link">Explore 7 Image Tools &rarr;</span>
        </a>

        <a href="categories/vpn.html" class="category-card">
          <div>
            <div class="category-card-icon">🔒</div>
            <h3 class="category-card-title">VPN &amp; Workstation Privacy</h3>
            <p class="category-card-desc">High-speed encrypted tunnels, dedicated IP routing, and zero-log streaming security powered by NordVPN and Surfshark VPN.</p>
          </div>
          <span class="category-card-link">Explore Privacy Tools &rarr;</span>
        </a>
      </div>

      <!-- Quick Route to Deals & Full Directory -->
      <div style="display:flex; justify-content:center; align-items:center; gap:1rem; flex-wrap:wrap; margin-top:1.25rem;">
        <a href="deals.html" class="badge emerald" style="text-decoration:none; padding:0.5rem 1rem; font-size:0.88rem; font-weight:700;">
          🔥 View Curated Software Bundles &amp; Deals &rarr;
        </a>
        <a href="#products" class="badge" style="text-decoration:none; padding:0.5rem 1rem; font-size:0.88rem; font-weight:600; background:#FFFFFF; border:1.5px solid #CBD5E1; color:#0F172A;">
          📋 Jump to All 49 Tool Profiles &darr;
        </a>
      </div>
    </section>

    <!-- ========================================================
         SECTION C: TOOL SEARCH AND DIRECTORY
         ======================================================== -->
    <section id="directory" style="margin-top: 3.5rem;">
      <div style="text-align:center; max-width:760px; margin:0 auto 1.5rem;">
        <span class="badge" style="background:#E0F2FE; color:#0284C7; border:1px solid #BAE6FD; font-weight:700;">⚡ Interactive Directory</span>
        <h2 style="font-size:1.85rem; font-weight:800; letter-spacing:-0.03em; color:#0F172A; margin:0.45rem 0 0.35rem;">Search &amp; Discover AI Tools</h2>
        <p style="font-size:0.95rem; color:#475569; margin:0;">Filter across 49 verified software profiles by technology stack, technical capability, or reference pricing.</p>
      </div>

      <!-- Interactive Living Console Centerpiece -->
      {showcase_html}

      <!-- Live Search & Category Filter Controls -->
      {search_bar_html}

      <!-- Full 49 Tools Catalog Grid -->
      <section id="products" style="margin-top: 3.5rem;">
        <div style="display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:0.5rem; margin-bottom:1.5rem;">
          <div>
            <h2 class="section-title" style="margin-bottom:0.25rem;">AI Software Tool Profiles (49 Tools Catalog)</h2>
            <p class="section-subtitle" style="margin-bottom:0;">Technical specifications, capability reviews, and informational reference rates.</p>
          </div>
          <span style="font-size:0.85rem; color:#64748B; font-weight:600;">Updated: October 2026</span>
        </div>

        {tools_grid_html}
      </section>
    </section>

    <!-- ========================================================
         SECTION D: PRICING AND LICENSING TRANSPARENCY
         ======================================================== -->
    <section id="pricing" style="margin-top: 4.5rem;">
      <div style="text-align:center; max-width:780px; margin:0 auto 1.75rem;">
        <span class="badge" style="background:#FEF3C7; color:#B45309; border:1px solid #FDE68A; font-weight:700;">⚖️ Consumer Transparency</span>
        <h2 class="section-title" style="margin:0.45rem 0 0.35rem;">Pricing &amp; Licensing Transparency</h2>
        <p class="section-subtitle" style="margin:0;">Informational benchmarks in Pakistani Rupees (PKR) and US Dollars (USD) with zero hidden forex surcharges.</p>
      </div>

      <div class="transparency-callout">
        <strong>Direct Order Status Notice:</strong> Direct paid subscription checkout is currently paused while supplier licensing and resale authorizations undergo standard legal verification. Prices displayed below represent historical and prevailing reference benchmarks. Visitors are advised to confirm current pricing, features, and licensing terms directly on the tool provider's official website. WhatsApp communication remains active for non-binding inquiries only.
      </div>

      <!-- Pre-Order Transparency Terms Bar -->
      <div class="pre-order-terms-bar" role="note" aria-label="Pre-Order Transparency Notice" style="margin-bottom:2rem;">
        <div class="term-item"><span>⚡</span> <div><strong>15-Minute Delivery Target (15–30 Min):</strong> Login credentials sent via WhatsApp after payment confirmation.</div></div>
        <div class="term-item"><span>🛡️</span> <div><strong>30-Day Replacement Warranty:</strong> Account replacement provided if access is disrupted during the 30-day term.</div></div>
        <div class="term-item"><span>🏢</span> <div><strong>Transparent Account Models:</strong> Distinctly labeled shared team workspaces and private email seats. Zero stolen or trial accounts.</div></div>
        <div class="term-item"><span>💳</span> <div><strong>Zero FX Friction:</strong> Pay in Pakistani Rupees (PKR) via EasyPaisa, JazzCash, Raast, or SadaPay with no bank international surcharges.</div></div>
      </div>

      {pricing_table_html}
    </section>

    <!-- ========================================================
         SECTION E: GUIDES AND COMPARISONS
         ======================================================== -->
    <section id="guides" style="margin-top: 4.5rem;">
      <div style="text-align:center; max-width:780px; margin:0 auto 2rem;">
        <span class="badge" style="background:#EEF2FF; color:#4361EE; border:1px solid #C7D2FE; font-weight:700;">📖 Editorial Research</span>
        <h2 class="section-title" style="margin:0.45rem 0 0.35rem;">Guides, Comparisons &amp; Best-Of Lists</h2>
        <p class="section-subtitle" style="margin:0;">In-depth technical shootouts, side-by-side benchmark evaluations, and ranked tool recommendations.</p>
      </div>

      <div class="grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1.25rem;">
        <div class="card">
          <span class="badge" style="background:#F0FDF4; color:#15803D; border:1px solid #BBF7D0; font-size:0.75rem; align-self:flex-start; margin-bottom:0.75rem;">⚖️ Head-to-Head Shootout</span>
          <h3 style="font-size:1.15rem; font-weight:750; color:#0F172A; margin:0 0 0.5rem;">ChatGPT Plus vs Claude Pro</h3>
          <p style="font-size:0.9rem; color:#475569; line-height:1.55; margin:0 0 1.25rem;">Comprehensive analysis comparing coding benchmarks, 200K token context windows, Artifacts visual canvas, and Advanced Voice Mode.</p>
          <a href="compare/chatgpt-vs-claude.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem;">Read Full Comparison &rarr;</a>
        </div>

        <div class="card">
          <span class="badge" style="background:#EFF6FF; color:#1D4ED8; border:1px solid #BFDBFE; font-size:0.75rem; align-self:flex-start; margin-bottom:0.75rem;">🎬 Video AI Shootout</span>
          <h3 style="font-size:1.15rem; font-weight:750; color:#0F172A; margin:0 0 0.5rem;">Runway Gen-3 vs Pika 2.0</h3>
          <p style="font-size:0.9rem; color:#475569; line-height:1.55; margin:0 0 1.25rem;">Cinematic motion fidelity, prompt consistency, and viral creative physics evaluated side by side for video creators.</p>
          <a href="compare/runway-vs-pika.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem;">Read Video Shootout &rarr;</a>
        </div>

        <div class="card">
          <span class="badge" style="background:#FAF5FF; color:#7E22CE; border:1px solid #E9D5FF; font-size:0.75rem; align-self:flex-start; margin-bottom:0.75rem;">💻 Developer Rankings</span>
          <h3 style="font-size:1.15rem; font-weight:750; color:#0F172A; margin:0 0 0.5rem;">Best AI Coding Tools (2026)</h3>
          <p style="font-size:0.9rem; color:#475569; line-height:1.55; margin:0 0 1.25rem;">Ranked benchmarks of GitHub Copilot, Cursor Pro, Claude 3.5 Sonnet, Lovable, and JetBrains with verified SWE-bench scores.</p>
          <a href="best/best-ai-coding-tools.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem;">View Developer Rankings &rarr;</a>
        </div>

        <div class="card">
          <span class="badge" style="background:#FFF1F2; color:#BE123C; border:1px solid #FECDD3; font-size:0.75rem; align-self:flex-start; margin-bottom:0.75rem;">🎬 Video Rankings</span>
          <h3 style="font-size:1.15rem; font-weight:750; color:#0F172A; margin:0 0 0.5rem;">Best AI Video Generators (2026)</h3>
          <p style="font-size:0.9rem; color:#475569; line-height:1.55; margin:0 0 1.25rem;">Shortlist of top generative video engines for social media, YouTube production, and commercial advertising in Pakistan.</p>
          <a href="best/best-ai-video-generators.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem;">View Video Rankings &rarr;</a>
        </div>

        <div class="card">
          <span class="badge" style="background:#FEF3C7; color:#B45309; border:1px solid #FDE68A; font-size:0.75rem; align-self:flex-start; margin-bottom:0.75rem;">🧠 Architecture Guide</span>
          <h3 style="font-size:1.15rem; font-weight:750; color:#0F172A; margin:0 0 0.5rem;">Frontier AI Models &amp; Architecture</h3>
          <p style="font-size:0.9rem; color:#475569; line-height:1.55; margin:0 0 1.25rem;">Practical guide to understanding frontier LLMs, token pricing, reasoning trade-offs, and choosing between open and proprietary weights.</p>
          <a href="guides/chatgpt-vs-claude.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem;">Read LLM Guide &rarr;</a>
        </div>
      </div>
    </section>

    <!-- ========================================================
         SECTION F: FREQUENTLY ASKED QUESTIONS
         ======================================================== -->
    <section id="faq" style="margin-top: 4.5rem;">
      <div style="text-align:center; max-width:780px; margin:0 auto 2rem;">
        <span class="badge" style="background:#F1F5F9; color:#475569; border:1px solid #CBD5E1; font-weight:700;">❓ Knowledge Base</span>
        <h2 class="section-title" style="margin:0.45rem 0 0.35rem;">Frequently Asked Questions</h2>
        <p class="section-subtitle" style="margin:0;">Clear answers on catalog operations, reference pricing, and vendor independence.</p>
      </div>
      <div style="display:flex; flex-direction:column; gap:1.25rem; max-width:850px; margin:0 auto;">
{faq_cards_str}
      </div>
    </section>

    <!-- ========================================================
         SECTION G: TRUST AND SUPPORT
         ======================================================== -->
    <section id="features" style="margin-top: 4.5rem;">
      <div style="text-align:center; max-width:780px; margin:0 auto 2rem;">
        <span class="badge" style="background:#ECFDF5; color:#047857; border:1px solid #A7F3D0; font-weight:700;">🛡️ Verified Operations</span>
        <h2 class="section-title" style="margin:0.45rem 0 0.35rem;">Trust, Operations &amp; Consumer Support</h2>
        <p class="section-subtitle" style="margin:0;">Independent digital concierge desk based in Islamabad, Pakistan, serving domestic and international users.</p>
      </div>
      <div class="grid" style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1.25rem;">
        <div class="card">
          <h2>1. Independent Directory &amp; Help Desk</h2>
          <p>AIDigiTools operates as an independent software guide and subscription concierge desk. We assist customers with setup workflows, domestic PKR settlement guidance, and technical tool comparison.</p>
          <a href="about.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem; margin-top:auto;">Learn About Our Operations &rarr;</a>
        </div>
        <div class="card">
          <h2>2. Responsive WhatsApp Help Desk</h2>
          <p>Real human assistance available on WhatsApp at 03326861112 for plan inquiries, account setup instructions, and prompt responses during operational business hours.</p>
          <a href="contact.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem; margin-top:auto;">Contact Support Desk &rarr;</a>
        </div>
        <div class="card">
          <h2>3. Reseller &amp; Trademark Disclosures</h2>
          <p>We are not directly affiliated with or endorsed by OpenAI, Anthropic, Midjourney, or Adobe. All brand names and trademarks belong to their respective corporate copyright holders.</p>
          <a href="affiliate-disclosure.html" style="color:#0284C7; font-weight:700; text-decoration:none; font-size:0.88rem; margin-top:auto;">Read Trademark Policy &rarr;</a>
        </div>
      </div>
    </section>

    <!-- Payment Rails Section with Anchor -->
    <section id="payments" style="margin-top: 3.5rem; text-align:center;">
      <h2 class="section-title" style="font-size:1.35rem;">Supported Domestic &amp; Global Payment Rails</h2>
      <p style="color:#475569; font-size:0.95rem;">EasyPaisa, JazzCash, SadaPay, NayaPay, Raast, local Bank IBFT, Wise, and Binance Pay (USDT).</p>
      <p style="margin-top:0.75rem;"><a href="policies.html#payments" style="color:#0284C7; font-weight:700; text-decoration:none;">Read complete payment details in our policies &rarr;</a></p>
    </section>
  </main>

  <!-- ========================================================
       SECTION H: FOOTER
       ======================================================== -->
  <footer>
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="index.html" class="logo" style="margin-bottom:0.75rem;" aria-label="AIDigiTools Home">
            <svg class="logo-brand-icon" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <defs>
                <linearGradient id="footerNavTeal" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#00E5A3"/>
                  <stop offset="50%" stop-color="#05D5A6"/>
                  <stop offset="100%" stop-color="#00B4D8"/>
                </linearGradient>
                <linearGradient id="footerNavPurple" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#0077B6"/>
                  <stop offset="35%" stop-color="#4361EE"/>
                  <stop offset="70%" stop-color="#7209B7"/>
                  <stop offset="100%" stop-color="#8B5CF6"/>
                </linearGradient>
                <linearGradient id="footerNavOrbit" x1="0%" y1="50%" x2="100%" y2="50%">
                  <stop offset="0%" stop-color="#00E5A3"/>
                  <stop offset="50%" stop-color="#00B4D8"/>
                  <stop offset="100%" stop-color="#8B5CF6"/>
                </linearGradient>
              </defs>
              <path class="orbit-back" d="M 12 62 C 12 36, 126 18, 134 38" stroke="url(#footerNavOrbit)" stroke-width="3.5" stroke-linecap="round" fill="none" opacity="0.65"/>
              <path class="sparkle-star" d="M 8 36 Q 8 41 3 41 Q 8 41 8 46 Q 8 41 13 41 Q 8 41 8 36 Z" fill="#00E5A3"/>
              <path class="sparkle-star" d="M 128 78 Q 128 82 124 82 Q 128 82 128 86 Q 128 82 132 82 Q 128 82 128 78 Z" fill="#8B5CF6"/>
              <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" fill="url(#footerNavTeal)"/>
              <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" fill="url(#footerNavPurple)"/>
              <path d="M 46 64 C 52 58, 66 56, 80 62 L 72 74 C 62 70, 52 72, 46 76 Z" fill="url(#footerNavTeal)" opacity="0.95"/>
              <path class="orbit-front" d="M 134 38 C 142 58, 38 88, 16 66" stroke="url(#footerNavOrbit)" stroke-width="4" stroke-linecap="round" fill="none"/>
              <circle class="orbit-node" cx="124" cy="34" r="5.5" fill="#4361EE"/>
              <circle cx="122.5" cy="32.5" r="1.8" fill="#FFFFFF" opacity="0.8"/>
            </svg>
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
          <h4>Explore</h4>
          <ul>
            <li><a href="categories/coding.html">Coding &amp; LLM Assistants</a></li>
            <li><a href="categories/video.html">AI Video &amp; Animation</a></li>
            <li><a href="categories/image.html">Image &amp; Graphic Suites</a></li>
            <li><a href="categories/vpn.html">VPN &amp; Security Services</a></li>
            <li><a href="deals.html">Bundle Deals &amp; Discounts</a></li>
            <li><a href="index.html#products">Full 49 Tools Catalog</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Learn &amp; Compare</h4>
          <ul>
            <li><a href="compare/chatgpt-vs-claude.html">ChatGPT vs Claude</a></li>
            <li><a href="compare/runway-vs-pika.html">Runway vs Pika</a></li>
            <li><a href="best/best-ai-video-generators.html">Best Video AI (2026)</a></li>
            <li><a href="best/best-ai-coding-tools.html">Best Coding AI (2026)</a></li>
            <li><a href="guides/chatgpt-vs-claude.html">Frontier Models Guide</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Trust &amp; Support</h4>
          <ul>
            <li><a href="about.html">About AIDigiTools</a></li>
            <li><a href="contact.html">Support Operations Desk</a></li>
            <li><a href="affiliate-disclosure.html">Reseller &amp; Trademark Policy</a></li>
            <li><a href="policies.html">Consumer Terms &amp; Policies</a></li>
            <li><a href="shipping-policy.html">15-Minute Delivery Target</a></li>
            <li><a href="policies.html#payments">Payment Rails (PKR &amp; USD)</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 AIDigiTools (aidigitools.tech). All rights reserved. Independent software subscription concierge desk.</p>
        <p style="margin-top:0.35rem; font-size:0.8rem; color:var(--text-muted);">
          Verified Rails: EasyPaisa • JazzCash • SadaPay • NayaPay • Raast • Bank IBFT • Wise • Binance Pay (USDT) • Catalog Freshness: October 2026
        </p>
      </div>
    </div>
  </footer>

  {drawers_html}
</body>
</html>
"""

# Write reorganized index.html
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(new_index_html)

print("index.html reorganized successfully!")
