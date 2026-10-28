import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSS_PATH = os.path.join(REPO_ROOT, "assets", "style.css")

print("Applying Premium Luminous Light Modern Theme to assets/style.css...")

with open(CSS_PATH, "r", encoding="utf-8") as f:
    css = f.read()

# 1. Update :root variables with Light Palette
root_pattern = r":root\s*\{[^}]+\}"
new_root = """:root {
  /* ========================================================
     AIDigiTools Premium Luminous Light Modern AI-Tech Theme
     Light, Elegant, High-Contrast, Professional Marketplace
     ======================================================== */
  
  /* Primary Design System Tokens */
  --color-canvas: #F8FAFD;         /* Soft Luminous Ice-Pearl Canvas */
  --color-surface: #FFFFFF;        /* Pure White Elevated Surface */
  --color-card: #FFFFFF;           /* Crisp Pure White Card */
  --color-border: #D5E2F0;         /* Refined Slate Border */
  --color-border-subtle: #E2E8F0;  /* Subtle Hairline Border */
  --color-text-title: #0F172A;     /* Deep Midnight Slate (WCAG AAA) */
  --color-text-body: #334155;      /* Readable Slate Charcoal (WCAG AAA) */
  --color-text-muted: #475569;     /* Refined Slate Gray */
  --color-accent-cyan: #00B4D8;    /* Brand Vibrant Cyan */
  --color-accent-blue: #4361EE;    /* Brand Royal Blue */
  --color-accent-emerald: #10B981; /* Verified Emerald Green */

  /* Canvas & Background Surfaces */
  --bg-dark: #F8FAFD;
  --bg-canvas: #F8FAFD;            /* Soft Luminous Ice-Pearl Canvas */
  --bg-surface: #FFFFFF;           /* Pure White Surface */
  --bg-card: #FFFFFF;              /* Pure White Card Base */
  --bg-card-hover: #FFFFFF;
  --bg-card-secondary: #F1F5F9;    /* Soft Slate Pearl Tint */
  --bg-subtle: #F1F5F9;
  
  /* High-Contrast Text Hierarchy */
  --text-primary: #0F172A;         /* Deep Midnight Slate */
  --text-color: #0F172A;
  --text-secondary: #334155;       /* Readable Slate Charcoal */
  --text-muted: #475569;           /* Refined Slate Gray */
  
  /* Brand Orbit Palette */
  --brand-mint: #00E5A3;
  --brand-teal: #05D5A6;
  --brand-cyan: #00B4D8;
  --brand-blue: #4361EE;
  --brand-indigo: #4361EE;
  --brand-purple: #8B5CF6;
  --brand-violet: #7209B7;
  --brand-gradient: linear-gradient(135deg, #00B4D8 0%, #4361EE 50%, #8B5CF6 100%);
  --brand-gradient-hover: linear-gradient(135deg, #0284C7 0%, #3B82F6 50%, #7C3AED 100%);
  
  /* Compatibility with existing test suite */
  --accent-gold: #00B4D8;
  --accent-gold-light: #E0F2FE;
  --accent-gold-glow: rgba(0, 180, 216, 0.15);
  --accent-emerald: #059669;
  --accent-emerald-light: #D1FAE5;
  --accent-violet: #7C3AED;
  --accent-cyan: #00B4D8;
  --accent-rose: #E11D48;
  
  /* Precision Hairline Borders */
  --border-color: #CBD5E1;
  --border-subtle: #E2E8F0;
  --border-subtle-hover: #CBD5E1;
  --border-highlight: #00B4D8;
  --border-emerald: #10B981;
  
  /* Modern Typography Stack */
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", "Helvetica Neue", Arial, sans-serif;
  
  /* Refined Elevation & Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(15, 23, 42, 0.05);
  --shadow-card: 0 2px 8px -1px rgba(15, 23, 42, 0.06), 0 1px 3px -1px rgba(15, 23, 42, 0.04);
  --shadow-card-hover: 0 14px 32px -6px rgba(15, 23, 42, 0.1), 0 4px 10px -3px rgba(15, 23, 42, 0.04), 0 0 0 1px rgba(0, 180, 216, 0.25);
  --shadow-glow: 0 4px 20px -2px rgba(0, 180, 216, 0.18);
  --shadow-lg: 0 12px 28px -5px rgba(15, 23, 42, 0.08), 0 8px 10px -6px rgba(15, 23, 42, 0.03);
}"""
css = re.sub(root_pattern, new_root, css, count=1)

# 2. Update Body Background to Soft Luminous Ice-Pearl
body_pattern = r"body\s*\{[^}]+\}"
new_body = """body {
  font-family: var(--font-sans);
  background-color: var(--bg-canvas); /* Soft Luminous Ice-Pearl #F8FAFD */
  color: var(--text-primary);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  background-image: 
    radial-gradient(ellipse 70% 50% at 50% 0%, rgba(0, 180, 216, 0.04) 0%, transparent 65%),
    radial-gradient(rgba(15, 23, 42, 0.015) 1px, transparent 1px);
  background-size: 100% 100%, 28px 28px;
  background-attachment: fixed;
  min-height: 100vh;
}"""
css = re.sub(body_pattern, new_body, css, count=1)

# 3. Header: Translucent Frosted Pure White with Crisp Border
header_pattern = r"header\s*\{[^}]+\}"
new_header = """header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.94); /* Crisp Translucent Light Header */
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1.5px solid #E2E8F0;
  transition: all 0.25s ease;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}"""
css = re.sub(header_pattern, new_header, css, count=1)

# 4. Logo & Nav Links inside Header (Light Theme High Contrast)
logo_name_pattern = r"\.logo-brand-name\s*\{[^}]+\}"
new_logo_name = """.logo-brand-name {
  font-size: 1.35rem;
  font-weight: 750;
  letter-spacing: -0.025em;
  color: #0F172A;
}"""
css = re.sub(logo_name_pattern, new_logo_name, css, count=1)

logo_prefix_pattern = r"\.logo-brand-name\s+\.ai-prefix\s*\{[^}]+\}"
new_logo_prefix = """.logo-brand-name .ai-prefix {
  background: linear-gradient(135deg, #00B4D8 0%, #4361EE 100%);
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
  color: #64748B;
  text-transform: uppercase;
  margin-top: 2px;
}"""
css = re.sub(logo_tagline_pattern, new_logo_tagline, css, count=1)

nav_a_pattern = r"nav\s+a\s*\{[^}]+\}"
new_nav_a = """nav a {
  text-decoration: none;
  color: #334155;
  font-size: 0.92rem;
  font-weight: 600;
  padding: 0.45rem 0.75rem;
  border-radius: 8px;
  transition: all 0.18s ease;
}"""
css = re.sub(nav_a_pattern, new_nav_a, css, count=1)

nav_a_hover_pattern = r"nav\s+a:hover\s*\{[^}]+\}"
new_nav_a_hover = """nav a:hover {
  color: #0F172A;
  background: rgba(15, 23, 42, 0.05);
}"""
css = re.sub(nav_a_hover_pattern, new_nav_a_hover, css, count=1)

nav_cta_pattern = r"\.nav-cta\s*\{[^}]+\}"
new_nav_cta = """.nav-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: linear-gradient(135deg, #00B4D8 0%, #4361EE 100%);
  color: #FFFFFF !important;
  font-weight: 600;
  font-size: 0.88rem;
  padding: 0.45rem 1rem !important;
  border-radius: 9999px;
  box-shadow: 0 2px 8px rgba(0, 180, 216, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}"""
css = re.sub(nav_cta_pattern, new_nav_cta, css, count=1)

# 5. Hero Section: Luminous, Soft Light Luxury Card
hero_pattern = r"\.hero\s*\{[^}]+\}"
new_hero = """.hero {
  padding: 3.5rem 2rem 3rem;
  text-align: center;
  max-width: 980px;
  margin: 1.5rem auto 2.5rem;
  background: linear-gradient(180deg, #FFFFFF 0%, #F0F7FF 60%, #EEF2FF 100%);
  border: 1.5px solid #D5E2F0;
  border-radius: 24px;
  box-shadow: 0 12px 32px -6px rgba(15, 23, 42, 0.06), 0 4px 12px -2px rgba(15, 23, 42, 0.02);
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
    radial-gradient(rgba(67, 97, 238, 0.04) 1px, transparent 1px);
  background-size: 24px 24px;
  pointer-events: none;
}

.hero h1 {
  font-size: clamp(1.9rem, 3.6vw, 2.5rem);
  font-weight: 800;
  line-height: 1.25;
  letter-spacing: -0.025em;
  color: #0F172A;
  margin-bottom: 1.25rem;
  position: relative;
  z-index: 1;
}

.hero .quick-answer {
  background: #FFFFFF;
  border: 1.5px solid #BAE6FD;
  border-left: 4px solid #00B4D8;
  border-radius: 14px;
  padding: 1.35rem 1.65rem;
  font-size: 1.02rem;
  line-height: 1.65;
  color: #1E293B;
  text-align: left;
  box-shadow: 0 4px 16px rgba(0, 180, 216, 0.08);
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
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  color: #1E293B;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  font-size: 0.82rem;
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
  transition: all 0.2s ease;
}

.hero .badge:hover {
  border-color: #00B4D8;
  color: #0284C7;
  background: #F0F9FF;
  transform: translateY(-1px);
}

.hero .badge.emerald {
  background: #ECFDF5;
  border-color: #86EFAC;
  color: #047857;
}"""
css = re.sub(hero_pattern, new_hero, css, count=1)

# 6. Showcase / AuthKit Centerpiece: Pure White Surface with Subtle Radial Glow
border_beam_pattern = r"\.border-beam-card\s*\{[^}]+\}"
new_border_beam = """.border-beam-card {
  position: relative;
  border-radius: 20px;
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.35), rgba(67, 97, 238, 0.25), rgba(0, 229, 163, 0.25));
  padding: 1px;
  box-shadow: 0 16px 36px -8px rgba(15, 23, 42, 0.08), 0 4px 12px -2px rgba(15, 23, 42, 0.03);
}"""
css = re.sub(border_beam_pattern, new_border_beam, css, count=1)

authkit_card_pattern = r"\.authkit-widget-card\s*\{[^}]+\}"
new_authkit_card = """.authkit-widget-card {
  background: #FFFFFF; /* Pure White Light Centerpiece */
  border-radius: 19px;
  overflow: hidden;
  color: #0F172A;
  border: 1px solid #E2E8F0;
}

.authkit-cat-filter-pills {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 1rem 1.25rem;
  background: #F8FAFC;
  border-bottom: 1.5px solid #E2E8F0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.authkit-cat-pill {
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  color: #334155;
  font-size: 0.84rem;
  font-weight: 600;
  padding: 0.4rem 0.85rem;
  border-radius: 9999px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}

.authkit-cat-pill:hover {
  background: #F0F9FF;
  border-color: #00B4D8;
  color: #0284C7;
}

.authkit-cat-pill.active {
  background: linear-gradient(135deg, #00B4D8 0%, #4361EE 100%);
  color: #FFFFFF;
  border-color: transparent;
  box-shadow: 0 2px 8px rgba(0, 180, 216, 0.3);
}

.authkit-tool-select {
  width: 100%;
  padding: 0.65rem 0.95rem;
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 8px;
  color: #0F172A;
  font-size: 0.92rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
}

.authkit-tool-select:focus {
  border-color: #00B4D8;
  box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.2);
}

.authkit-vendor-pill {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #0284C7;
  background: #E0F2FE;
  border: 1px solid #BAE6FD;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  margin-bottom: 0.65rem;
}

.authkit-tool-title {
  font-size: 1.45rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #0F172A;
  margin-bottom: 0.5rem;
}

.authkit-tool-desc {
  font-size: 0.95rem;
  color: #334155;
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
  color: #0284C7;
  letter-spacing: -0.03em;
}

.authkit-price-sub {
  font-size: 0.9rem;
  color: #64748B;
  font-weight: 600;
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
  color: #334155;
  font-weight: 500;
}

.authkit-features-list .check {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background: rgba(16, 185, 129, 0.15);
  color: #059669;
  border-radius: 50%;
  font-size: 0.75rem;
  font-weight: 800;
  flex-shrink: 0;
}

.authkit-simulator-box {
  background: #F8FAFC;
  border: 1.5px solid #E2E8F0;
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1.25rem;
}

.authkit-rails-title {
  font-size: 0.82rem;
  font-weight: 750;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #475569;
  margin-bottom: 0.65rem;
}

.authkit-rail-item {
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  border-radius: 8px;
  padding: 0.5rem;
  text-align: center;
  font-size: 0.82rem;
  font-weight: 700;
  color: #0F172A;
}

.authkit-badge-nofx {
  font-size: 0.78rem;
  font-weight: 700;
  color: #047857;
  text-align: center;
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  padding: 0.4rem;
  border-radius: 6px;
}"""
css = re.sub(authkit_card_pattern, new_authkit_card, css, count=1)

# 7. Tool Cards & Popular Cards: Soft Tinted Ice-Pearl with Distinct Borders & Top Accent
card_pattern = r"\.card,\s*\.tool-card\s*\{[^}]+\}"
new_card = """.card, .tool-card {
  background: linear-gradient(165deg, #FFFFFF 0%, #F8FAFD 50%, #F1F6FB 100%);
  border: 1.5px solid #D5E2F0;
  border-radius: 20px;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05);
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
  background: linear-gradient(90deg, #00B4D8 0%, #4361EE 50%, #10B981 100%);
  opacity: 0.9;
  transition: height 0.25s ease, opacity 0.25s ease;
}"""
css = re.sub(card_before_pattern, new_card_before, css, count=1)

popular_card_pattern = r"\.popular-card\s*\{[^}]+\}"
new_popular_card = """.popular-card {
  border: 1.5px solid #86EFAC !important;
  background: linear-gradient(165deg, #FFFFFF 0%, #F0FDF4 50%, #E8F9F0 100%) !important;
  box-shadow: 0 4px 18px rgba(16, 185, 129, 0.09) !important;
}"""
if re.search(popular_card_pattern, css):
    css = re.sub(popular_card_pattern, new_popular_card, css, count=1)

# 8. Elevated Logo Tile
logo_container_pattern = r"\.tool-brand-logo\s*\{[^}]+\}"
new_logo_container = """.tool-brand-logo {
  background: #FFFFFF;
  border: 1.5px solid #CBD5E1;
  box-shadow: 0 3px 8px rgba(15, 23, 42, 0.06);
  border-radius: 12px;
  padding: 4px;
}"""
if re.search(logo_container_pattern, css):
    css = re.sub(logo_container_pattern, new_logo_container, css, count=1)

# 9. Price Tag Styling (Sky-wash Container with Bold Tabular PKR)
price_tag_pattern = r"\.price-tag\s*\{[^}]+\}"
new_price_tag = """.price-tag {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0F172A;
  letter-spacing: -0.025em;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: space-between;
  gap: 0.35rem 0.6rem;
  margin: 0.95rem 0;
  line-height: 1.35;
  background: linear-gradient(135deg, #E0F2FE 0%, #EEF2FF 100%);
  border: 1.5px solid #BAE6FD;
  border-radius: 12px;
  padding: 0.65rem 0.95rem;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 2px 6px rgba(15, 23, 42, 0.02);
}"""
css = re.sub(price_tag_pattern, new_price_tag, css, count=1)

# 10. Table: Light Header and High Contrast
thead_pattern = r"thead\s*\{[^}]+\}"
new_thead = """thead {
  background: #F1F5F9;
  border-bottom: 2px solid #CBD5E1;
}"""
if re.search(thead_pattern, css):
    css = re.sub(thead_pattern, new_thead, css, count=1)

th_pattern = r"th\s*\{[^}]+\}"
new_th = """th {
  padding: 0.85rem 1.15rem;
  font-weight: 750;
  color: #0F172A;
  font-size: 0.82rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}"""
if re.search(th_pattern, css):
    css = re.sub(th_pattern, new_th, css, count=1)

# 11. Feature Panels (#features): Light Luxury Card Style
features_block_pattern = r"/\* =+ \s* DELIBERATE SURFACE VARIATION: DARK FEATURE PANELS.*?#faq \.card p\s*\{[^}]+\}"
new_features_block = """/* ========================================================
   DELIBERATE SURFACE VARIATION: LIGHT LUXURY FEATURE PANELS (#features)
   ======================================================== */
#features .card {
  background: linear-gradient(145deg, #FFFFFF 0%, #F0F7FF 100%) !important;
  border: 1.5px solid #BAE6FD !important;
  border-radius: 18px;
  color: #0F172A !important;
  box-shadow: 0 4px 18px rgba(2, 132, 199, 0.06) !important;
  padding: 2rem;
}

#features .card::before {
  background: linear-gradient(90deg, #00B4D8 0%, #4361EE 100%) !important;
}

#features .card h2 {
  color: #0F172A !important;
  font-size: 1.25rem;
  font-weight: 750;
  margin-bottom: 0.75rem;
}

#features .card p {
  color: #334155 !important;
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Accessible Categories & Filter Controls */
.cat-pill-btn {
  background: #F1F5F9;
  border: 1.5px solid #CBD5E1;
  color: #334155;
  padding: 0.45rem 0.95rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.84rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cat-pill-btn:hover {
  background: #E0F2FE;
  border-color: #00B4D8;
  color: #0284C7;
}

.cat-pill-btn.active {
  background: #0284C7 !important;
  border-color: #0284C7 !important;
  color: #FFFFFF !important;
  box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);
}

.search-input-field:focus {
  border-color: #00B4D8 !important;
  box-shadow: 0 0 0 3px rgba(0, 180, 216, 0.25) !important;
}

/* FAQ Cards */
#faq .card {
  background: #FFFFFF;
  border: 1.5px solid #D5E2F0;
  border-radius: 16px;
  padding: 1.65rem 1.85rem;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

#faq .card h2 {
  color: #0F172A;
  font-size: 1.15rem;
  font-weight: 750;
  margin-bottom: 0.5rem;
}

#faq .card p {
  color: #334155;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 0;
}"""
css = re.sub(features_block_pattern, new_features_block, css, flags=re.DOTALL)

# 12. Footer: Pure White Light Footer with Clean Borders & High Contrast
footer_pattern = r"footer\s*\{[^}]+\}"
new_footer = """footer {
  background: #FFFFFF; /* Pure White Light Footer */
  border-top: 1.5px solid #E2E8F0;
  padding: 4.5rem 0 2.5rem;
  margin-top: 5rem;
  color: #475569;
}"""
css = re.sub(footer_pattern, new_footer, css, count=1)

footer_h4_pattern = r"\.footer-col\s+h4\s*\{[^}]+\}"
new_footer_h4 = """.footer-col h4 {
  font-size: 0.9rem;
  font-weight: 750;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #0F172A;
  margin-bottom: 1rem;
}"""
css = re.sub(footer_h4_pattern, new_footer_h4, css, count=1)

footer_a_pattern = r"\.footer-col\s+a\s*\{[^}]+\}"
new_footer_a = """.footer-col a {
  text-decoration: none;
  color: #475569;
  font-size: 0.88rem;
  transition: color 0.18s ease;
}"""
css = re.sub(footer_a_pattern, new_footer_a, css, count=1)

footer_a_hover_pattern = r"\.footer-col\s+a:hover\s*\{[^}]+\}"
new_footer_a_hover = """.footer-col a:hover {
  color: #0284C7;
  font-weight: 600;
}"""
css = re.sub(footer_a_hover_pattern, new_footer_a_hover, css, count=1)

footer_bottom_pattern = r"\.footer-bottom\s*\{[^}]+\}"
new_footer_bottom = """.footer-bottom {
  border-top: 1px solid #E2E8F0;
  padding-top: 2rem;
  text-align: center;
  font-size: 0.82rem;
  color: #64748B;
}"""
css = re.sub(footer_bottom_pattern, new_footer_bottom, css, count=1)

# Write updated CSS
with open(CSS_PATH, "w", encoding="utf-8") as f:
    f.write(css)

print("Successfully applied Premium Luminous Light Modern Theme to assets/style.css.")
