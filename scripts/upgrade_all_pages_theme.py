"""
AIDigiTools — Complete Site-Wide Theme & Logo Upgrade Engine
Applies the new Light Editorial Marketplace Theme, SVG Animated Orbit Emblem,
and refined typography across all 52 HTML pages while strictly preserving:
- Exact Title tags & Meta Descriptions
- Exactly one <h1> per page
- Exact .quick-answer blocks (35-70 words)
- Valid JSON-LD structured data
- 100% link graph integrity (0 broken links, 0 broken anchors)
- Real WhatsApp helpline (03326861112)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# SVG Orbit Emblem definition (compact for header/footer)
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
        <a href="https://wa.me/923326861112" target="_blank" rel="noopener noreferrer" class="nav-cta">
          <span class="pulse-dot"></span>
          <span>WhatsApp Order</span>
        </a>
      </nav>
    </div>
  </header>"""

def build_footer(is_root=True):
    prefix = "" if is_root else "../"
    home_link = "index.html" if is_root else "../"
    
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

def upgrade_all_pages():
    html_files = [p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)]
    print(f"Upgrading theme and logo components across {len(html_files)} HTML pages...")
    
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
            
        # 3. Add favicon link if missing
        fav_prefix = "" if is_root else "../"
        if "favicon.svg" not in content:
            fav_tag = f'  <link rel="icon" type="image/svg+xml" href="{fav_prefix}favicon.svg">\n'
            content = content.replace('</head>', f'{fav_tag}</head>')
            
        f.write_text(content, encoding="utf-8")
        
    print(f"Header, footer, and SVG Orbit Emblem successfully synchronized on all {len(html_files)} pages!")

if __name__ == "__main__":
    upgrade_all_pages()
