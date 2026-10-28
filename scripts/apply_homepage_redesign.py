import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_PATH = os.path.join(REPO_ROOT, "assets", "style.css")
INDEX_PATH = os.path.join(REPO_ROOT, "index.html")

print("Applying Premium Modern AI-Tech Design System to assets/style.css...")

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update :root variables
root_pattern = r":root\s*\{[^}]+\}"
new_root = """:root {
  /* ========================================================
     AIDigiTools Premium Modern AI-Tech Design System
     Palette: Midnight Navy (#111827), Deep Slate (#1F2937),
              Warm Ivory (#F5F3EE), Pure White (#FFFFFF),
              Muted Teal (#2CB6A5), Soft Violet (#8B83D7),
              Slate Text (#344054), Muted Text (#98A2B3)
     ======================================================== */
  
  /* Primary Design System Tokens */
  --color-midnight-navy: #111827;  /* Hero, premium header, dark sections */
  --color-deep-slate: #1F2937;     /* Cards & dark UI surfaces */
  --color-warm-ivory: #F5F3EE;     /* Main page background & breathing space */
  --color-pure-white: #FFFFFF;     /* Selected content cards & readable surfaces */
  --color-muted-teal: #2CB6A5;     /* Primary accents, active states, key icons */
  --color-soft-violet: #8B83D7;    /* Restrained secondary accents for AI highlights */
  --color-slate-text: #344054;     /* Body text on light backgrounds */
  --color-muted-text: #98A2B3;     /* Muted text on dark surfaces */

  /* Canvas & Background Surfaces */
  --bg-dark: #111827;              /* Midnight Navy Dark Surface */
  --bg-canvas: #F5F3EE;            /* Warm Ivory Breathing Space */
  --bg-surface: #FFFFFF;           /* Pure White Surface */
  --bg-card: #FFFFFF;              /* Crisp Elevated Card */
  --bg-card-hover: #FFFFFF;
  --bg-card-secondary: #F3F1EC;    /* Warm Ivory Tint */
  --bg-subtle: #F3F1EC;
  
  /* Text Contrast Hierarchy */
  --text-primary: #111827;         /* Midnight Navy (High Contrast WCAG AAA) */
  --text-color: #111827;
  --text-secondary: #344054;       /* Slate Text (High Contrast WCAG AA/AAA) */
  --text-muted: #667085;           /* Refined Slate Gray */
  
  /* Brand Orbit Palette */
  --brand-mint: #2CB6A5;           /* Muted Teal */
  --brand-teal: #2CB6A5;           /* Muted Teal */
  --brand-cyan: #2CB6A5;           /* Muted Teal */
  --brand-blue: #4361EE;           /* Accent Blue */
  --brand-indigo: #4361EE;
  --brand-purple: #8B83D7;         /* Soft Violet */
  --brand-violet: #8B83D7;         /* Soft Violet */
  --brand-gradient: linear-gradient(135deg, #2CB6A5 0%, #4361EE 50%, #8B83D7 100%);
  --brand-gradient-hover: linear-gradient(135deg, #259D8E 0%, #3B54D4 50%, #7A72C8 100%);
  
  /* Compatibility with existing test suite */
  --accent-gold: #2CB6A5;          /* Mapped to brand muted teal */
  --accent-gold-light: #E6F8F5;
  --accent-gold-glow: rgba(44, 182, 165, 0.2);
  --accent-emerald: #10B981;
  --accent-emerald-light: #D1FAE5;
  --accent-violet: #8B83D7;
  --accent-cyan: #2CB6A5;
  --accent-rose: #E11D48;
  
  /* Precision Hairline Borders */
  --border-color: #E2E8F0;         /* Soft Slate 200 */
  --border-subtle: #E2E8F0;
  --border-subtle-hover: #CBD5E1;
  --border-highlight: #2CB6A5;
  --border-emerald: #10B981;
  
  /* Modern Typography Stack */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
  
  /* Refined Elevation & Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(17, 24, 39, 0.05);
  --shadow-card: 0 1px 3px 0 rgba(17, 24, 39, 0.06), 0 1px 2px -1px rgba(17, 24, 39, 0.04);
  --shadow-card-hover: 0 14px 30px -6px rgba(17, 24, 39, 0.1), 0 4px 10px -3px rgba(17, 24, 39, 0.04), 0 0 0 1px rgba(44, 182, 165, 0.28);
  --shadow-glow: 0 4px 20px -2px rgba(44, 182, 165, 0.2);
  --shadow-lg: 0 12px 28px -5px rgba(17, 24, 39, 0.12), 0 8px 10px -6px rgba(17, 24, 39, 0.04);
}"""

css = re.sub(root_pattern, new_root, css, count=1)

# 2. Update Body Background
body_pattern = r"body\s*\{[^}]+\}"
new_body = """body {
  font-family: var(--font-sans);
  background-color: var(--bg-canvas); /* Warm Ivory #F5F3EE */
  color: var(--text-primary);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  background-image: 
    radial-gradient(ellipse 60% 40% at 50% 0%, rgba(44, 182, 165, 0.04) 0%, transparent 65%),
    radial-gradient(rgba(17, 24, 39, 0.02) 1px, transparent 1px);
  background-size: 100% 100%, 28px 28px;
  background-attachment: fixed;
  min-height: 100vh;
}"""
css = re.sub(body_pattern, new_body, css, count=1)

# 3. Header Styling: Midnight Navy with refined glassmorphism
header_pattern = r"header\s*\{[^}]+\}"
new_header = """header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(17, 24, 39, 0.95); /* Midnight Navy Translucent */
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.25s ease;
}"""
css = re.sub(header_pattern, new_header, css, count=1)

# 4. Logo & Nav Links inside Header
logo_name_pattern = r"\.logo-brand-name\s*\{[^}]+\}"
new_logo_name = """.logo-brand-name {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: #F9FAFB;
}"""
css = re.sub(logo_name_pattern, new_logo_name, css, count=1)

logo_prefix_pattern = r"\.logo-brand-name\s+\.ai-prefix\s*\{[^}]+\}"
new_logo_prefix = """.logo-brand-name .ai-prefix {
  background: linear-gradient(135deg, #2CB6A5 0%, #8B83D7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 900;
}"""
css = re.sub(logo_prefix_pattern, new_logo_prefix, css, count=1)

logo_tagline_pattern = r"\.logo\s+\.tagline\s*\{[^}]+\}"
new_logo_tagline = """.logo .tagline {
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  color: #98A2B3;
  text-transform: uppercase;
  margin-top: 2px;
}"""
css = re.sub(logo_tagline_pattern, new_logo_tagline, css, count=1)

nav_a_pattern = r"nav\s+a\s*\{[^}]+\}"
new_nav_a = """nav a {
  text-decoration: none;
  color: #D1D5DB;
  font-size: 0.92rem;
  font-weight: 500;
  padding: 0.45rem 0.75rem;
  border-radius: 8px;
  transition: all 0.18s ease;
}"""
css = re.sub(nav_a_pattern, new_nav_a, css, count=1)

nav_a_hover_pattern = r"nav\s+a:hover\s*\{[^}]+\}"
new_nav_a_hover = """nav a:hover {
  color: #FFFFFF;
  background: rgba(255, 255, 255, 0.08);
}"""
css = re.sub(nav_a_hover_pattern, new_nav_a_hover, css, count=1)

nav_cta_pattern = r"\.nav-cta\s*\{[^}]+\}"
new_nav_cta = """.nav-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #2CB6A5 0%, #1E9E8F 100%);
  color: #FFFFFF !important;
  font-weight: 600;
  font-size: 0.88rem;
  padding: 0.45rem 1rem !important;
  border-radius: 9999px;
  box-shadow: 0 2px 10px rgba(44, 182, 165, 0.35);
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}"""
css = re.sub(nav_cta_pattern, new_nav_cta, css, count=1)

# 5. Hero Section
hero_pattern = r"\.hero\s*\{[^}]+\}"
new_hero = """.hero {
  padding: 3.75rem 2rem 3.25rem;
  text-align: center;
  max-width: 980px;
  margin: 1.5rem auto 2.5rem;
  background: radial-gradient(ellipse 80% 60% at 50% -10%, rgba(44, 182, 165, 0.18) 0%, transparent 70%),
              radial-gradient(ellipse 60% 40% at 85% 20%, rgba(139, 131, 215, 0.14) 0%, transparent 60%),
              #111827; /* Midnight Navy */
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  box-shadow: 0 20px 40px -15px rgba(17, 24, 39, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.05);
  position: relative;
  overflow: hidden;
}

.hero::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(rgba(255, 255, 255, 0.035) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
}

.hero h1 {
  font-size: clamp(1.9rem, 3.6vw, 2.5rem);
  font-weight: 750;
  line-height: 1.25;
  letter-spacing: -0.025em;
  color: #FFFFFF;
  margin-bottom: 1.25rem;
  position: relative;
  z-index: 1;
}

.hero .quick-answer {
  background: rgba(31, 41, 55, 0.85); /* Deep Slate */
  border: 1px solid rgba(44, 182, 165, 0.35);
  border-left: 4px solid #2CB6A5; /* Muted Teal */
  border-radius: 14px;
  padding: 1.35rem 1.65rem;
  font-size: 1.02rem;
  line-height: 1.65;
  color: #E5E7EB;
  text-align: left;
  box-shadow: 0 12px 28px -6px rgba(0, 0, 0, 0.35);
  margin: 1.25rem auto 1.75rem;
  max-width: 840px;
  position: relative;
  z-index: 1;
}

.hero .badges-row {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin: 1.25rem 0 0.5rem;
  position: relative;
  z-index: 1;
}

.hero .badge {
  background: rgba(31, 41, 55, 0.88); /* Deep Slate */
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #E5E7EB;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.82rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.hero .badge:hover {
  border-color: #2CB6A5;
  color: #FFFFFF;
  background: rgba(44, 182, 165, 0.2);
  transform: translateY(-1px);
}

.hero .badge.emerald {
  background: rgba(44, 182, 165, 0.15);
  border-color: rgba(44, 182, 165, 0.4);
  color: #2CB6A5;
}"""
css = re.sub(hero_pattern, new_hero, css, count=1)

# 6. Showcase / AuthKit Console Widget: Deep Slate Surface
border_beam_pattern = r"\.border-beam-card\s*\{[^}]+\}"
new_border_beam = """.border-beam-card {
  position: relative;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(44, 182, 165, 0.4), rgba(139, 131, 215, 0.3), rgba(44, 182, 165, 0.2));
  padding: 1px;
  box-shadow: 0 20px 45px -10px rgba(17, 24, 39, 0.2), 0 4px 12px -2px rgba(17, 24, 39, 0.08);
}"""
css = re.sub(border_beam_pattern, new_border_beam, css, count=1)

authkit_card_pattern = r"\.authkit-widget-card\s*\{[^}]+\}"
new_authkit_card = """.authkit-widget-card {
  background: #1F2937; /* Deep Slate */
  border-radius: 19px;
  overflow: hidden;
  color: #F9FAFB;
}

.authkit-cat-filter-pills {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 1rem 1.25rem;
  background: rgba(17, 24, 39, 0.7); /* Midnight Navy wash */
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.authkit-cat-pill {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #D1D5DB;
  font-size: 0.84rem;
  font-weight: 600;
  padding: 0.4rem 0.85rem;
  border-radius: 9999px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.authkit-cat-pill:hover {
  background: rgba(255, 255, 255, 0.12);
  color: #FFFFFF;
}

.authkit-cat-pill.active {
  background: #2CB6A5;
  color: #FFFFFF;
  border-color: #2CB6A5;
  box-shadow: 0 2px 8px rgba(44, 182, 165, 0.35);
}

.authkit-tool-select {
  width: 100%;
  padding: 0.65rem 0.95rem;
  background: #111827;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #FFFFFF;
  font-size: 0.92rem;
  font-weight: 500;
  outline: none;
  cursor: pointer;
}

.authkit-tool-select:focus {
  border-color: #2CB6A5;
  box-shadow: 0 0 0 3px rgba(44, 182, 165, 0.25);
}

.authkit-vendor-pill {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #2CB6A5;
  background: rgba(44, 182, 165, 0.14);
  border: 1px solid rgba(44, 182, 165, 0.3);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  margin-bottom: 0.65rem;
}

.authkit-tool-title {
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #FFFFFF;
  margin-bottom: 0.5rem;
}

.authkit-tool-desc {
  font-size: 0.95rem;
  color: #98A2B3;
  line-height: 1.55;
  margin-bottom: 1.25rem;
}

.authkit-price-row {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  margin-bottom: 1.25rem;
}

.authkit-price-val {
  font-size: 1.9rem;
  font-weight: 800;
  color: #2CB6A5;
  letter-spacing: -0.03em;
}

.authkit-price-sub {
  font-size: 0.9rem;
  color: #98A2B3;
  font-weight: 500;
}

.authkit-features-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.authkit-features-list li {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.92rem;
  color: #E5E7EB;
}

.authkit-features-list .check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: rgba(44, 182, 165, 0.2);
  color: #2CB6A5;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 800;
  flex-shrink: 0;
}

.authkit-simulator-box {
  background: #111827; /* Midnight Navy */
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1.25rem;
}

.authkit-rails-title {
  font-size: 0.82rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #98A2B3;
  margin-bottom: 0.65rem;
}

.authkit-rail-item {
  background: #1F2937;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 8px;
  padding: 0.5rem;
  text-align: center;
  font-size: 0.82rem;
  font-weight: 600;
  color: #F3F4F6;
}

.authkit-badge-nofx {
  font-size: 0.78rem;
  font-weight: 600;
  color: #2CB6A5;
  text-align: center;
  background: rgba(44, 182, 165, 0.12);
  border: 1px solid rgba(44, 182, 165, 0.25);
  padding: 0.4rem;
  border-radius: 6px;
}"""
css = re.sub(authkit_card_pattern, new_authkit_card, css, count=1)

# 7. Card & Tool-Card Styling: Pure White with slate borders & Muted Teal accents
card_pattern = r"\.card,\s*\.tool-card\s*\{[^}]+\}"
new_card = """.card, .tool-card {
  background: #FFFFFF; /* Pure White Card on Warm Ivory canvas */
  border: 1.5px solid #E2E8F0;
  border-radius: 20px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 16px -2px rgba(17, 24, 39, 0.04);
  transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}"""
css = re.sub(card_pattern, new_card, css, count=1)

card_before_pattern = r"\.card::before,\s*\.tool-card::before\s*\{[^}]+\}"
new_card_before = """.card::before, .tool-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3.5px;
  background: linear-gradient(90deg, #2CB6A5 0%, #4361EE 50%, #8B83D7 100%);
  opacity: 0.9;
  transition: height 0.25s ease, opacity 0.25s ease;
}"""
css = re.sub(card_before_pattern, new_card_before, css, count=1)

# 8. Popular Card: Mint/Teal Accent
popular_card_pattern = r"\.popular-card\s*\{[^}]+\}"
new_popular_card = """.popular-card {
  background: #FFFFFF !important;
  border: 1.5px solid rgba(44, 182, 165, 0.5) !important;
  box-shadow: 0 4px 18px rgba(44, 182, 165, 0.08) !important;
}"""
if re.search(popular_card_pattern, css):
    css = re.sub(popular_card_pattern, new_popular_card, css, count=1)

# 9. Tool Brand Logo Elevated Container
logo_container_pattern = r"\.tool-brand-logo\s*\{[^}]+\}"
new_logo_container = """.tool-brand-logo {
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  box-shadow: 0 3px 8px rgba(17, 24, 39, 0.05);
  border-radius: 12px;
  padding: 4px;
}"""
if re.search(logo_container_pattern, css):
    css = re.sub(logo_container_pattern, new_logo_container, css, count=1)
else:
    css += "\n" + new_logo_container

# 10. Price Tag Styling: Muted Teal Wash + Crisp Tabular Typography
price_tag_pattern = r"\.price-tag\s*\{[^}]+\}"
new_price_tag = """.price-tag {
  font-size: 1.35rem;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.025em;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.35rem 0.6rem;
  margin: 0.95rem 0;
  line-height: 1.35;
  background: linear-gradient(135deg, rgba(44, 182, 165, 0.07) 0%, rgba(139, 131, 215, 0.06) 100%);
  border: 1px solid rgba(44, 182, 165, 0.25);
  border-radius: 12px;
  padding: 0.65rem 0.95rem;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 2px 6px rgba(17, 24, 39, 0.02);
}"""
css = re.sub(price_tag_pattern, new_price_tag, css, count=1)

# 11. Feature Panels & Supporting Sections (Deep Slate Variation for #features)
features_css = """
/* ========================================================
   DELIBERATE SURFACE VARIATION: DARK FEATURE PANELS (#features)
   ======================================================== */
#features .card {
  background: #1F2937 !important; /* Deep Slate feature panel */
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 18px;
  color: #F9FAFB !important;
  box-shadow: 0 10px 25px -5px rgba(17, 24, 39, 0.15) !important;
  padding: 2rem;
}

#features .card::before {
  background: linear-gradient(90deg, #2CB6A5 0%, #8B83D7 100%) !important;
}

#features .card h2 {
  color: #FFFFFF !important;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

#features .card p {
  color: #98A2B3 !important;
  font-size: 0.94rem;
  line-height: 1.6;
}

/* Accessible Categories & Filter Controls */
.cat-pill-btn {
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  color: #344054;
  padding: 0.45rem 0.95rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.84rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-pill-btn:hover {
  background: #E5E7EB;
  color: #111827;
}

.cat-pill-btn.active {
  background: #2CB6A5 !important;
  border-color: #2CB6A5 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(44, 182, 165, 0.35);
}

.search-input-field:focus {
  border-color: #2CB6A5 !important;
  box-shadow: 0 0 0 3px rgba(44, 182, 165, 0.25) !important;
}

/* FAQ Cards */
#faq .card {
  background: #FFFFFF;
  border: 1.5px solid #E2E8F0;
  border-radius: 16px;
  padding: 1.65rem 1.85rem;
}

#faq .card h2 {
  color: #111827;
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

#faq .card p {
  color: #344054;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 0;
}
"""

if "DELIBERATE SURFACE VARIATION: DARK FEATURE PANELS" not in css:
    css += features_css

# 12. Footer: Midnight Navy surface with readable text & subtle teal accents
footer_pattern = r"footer\s*\{[^}]+\}"
new_footer = """footer {
  background: #111827; /* Midnight Navy */
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding: 4.5rem 0 2.5rem;
  margin-top: 5rem;
  color: #98A2B3;
}"""
css = re.sub(footer_pattern, new_footer, css, count=1)

footer_h4_pattern = r"\.footer-col\s+h4\s*\{[^}]+\}"
new_footer_h4 = """.footer-col h4 {
  font-size: 0.9rem;
  font-weight: 750;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #FFFFFF;
  margin-bottom: 1rem;
}"""
css = re.sub(footer_h4_pattern, new_footer_h4, css, count=1)

footer_a_pattern = r"\.footer-col\s+a\s*\{[^}]+\}"
new_footer_a = """.footer-col a {
  text-decoration: none;
  color: #98A2B3;
  font-size: 0.88rem;
  transition: color 0.18s ease;
}"""
css = re.sub(footer_a_pattern, new_footer_a, css, count=1)

footer_a_hover_pattern = r"\.footer-col\s+a:hover\s*\{[^}]+\}"
new_footer_a_hover = """.footer-col a:hover {
  color: #2CB6A5;
}"""
css = re.sub(footer_a_hover_pattern, new_footer_a_hover, css, count=1)

footer_bottom_pattern = r"\.footer-bottom\s*\{[^}]+\}"
new_footer_bottom = """.footer-bottom {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  padding-top: 2rem;
  text-align: center;
  font-size: 0.82rem;
  color: #667085;
}"""
css = re.sub(footer_bottom_pattern, new_footer_bottom, css, count=1)

# Write updated CSS
with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("Successfully applied Premium Modern AI-Tech Design System to assets/style.css.")

# 13. Update index.html: Add class="homepage-theme" to body if not present
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index_html = f.read()

if '<body class="homepage-theme">' not in index_html:
    index_html = index_html.replace('<body>', '<body class="homepage-theme">', 1)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Added class='homepage-theme' to index.html body.")
else:
    print("index.html body already has class='homepage-theme'.")
