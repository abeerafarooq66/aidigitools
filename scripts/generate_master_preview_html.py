# scripts/generate_master_preview_html.py
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, "scripts", "tools_catalog.json")
LOGOS_DIR = os.path.join(BASE_DIR, "assets", "product-logos")
DEST_FILE = r"C:\Users\Dell\.gemini\antigravity\brain\b9098f9b-3fdd-4d44-b502-c2981cd56d6f\aidigitools_all_tools_master_preview.html"

with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Cache SVG contents
svg_cache = {}
for filename in os.listdir(LOGOS_DIR):
    if filename.endswith(".svg"):
        slug_name = filename.replace(".svg", "")
        with open(os.path.join(LOGOS_DIR, filename), "r", encoding="utf-8") as sf:
            svg_cache[slug_name] = sf.read().strip()

# Group tools by category
categories = {
    "all": "All 40 Tools",
    "coding": "AI Coding & Dev (7)",
    "chat": "AI Assistant & LLMs (6)",
    "image": "Design & Creative (7)",
    "video": "AI Video & Audio (9)",
    "vpn": "VPN & Cyber Privacy (2)",
    "seo": "Productivity & SEO (6)",
    "streaming": "Streaming & Music (3)"
}

def get_cat_filter(tool):
    cat_lbl = tool.get("category_label", "").lower()
    slug = tool.get("slug", "")
    if "assistant" in cat_lbl or "llm" in cat_lbl:
        return "chat"
    elif "coding" in cat_lbl or "dev" in cat_lbl:
        return "coding"
    elif "design" in cat_lbl or "creative" in cat_lbl:
        return "image"
    elif "video" in cat_lbl or "audio" in cat_lbl:
        return "video"
    elif "vpn" in cat_lbl or "privacy" in cat_lbl:
        return "vpn"
    elif "productivity" in cat_lbl or "seo" in cat_lbl:
        return "seo"
    elif "streaming" in cat_lbl or "entertainment" in cat_lbl:
        return "streaming"
    return "all"

cards_html = []
for slug, tool in catalog.items():
    cat_key = get_cat_filter(tool)
    svg_content = svg_cache.get(slug, "")
    if not svg_content:
        # fallback to chatgpt icon if missing
        svg_content = svg_cache.get("chatgpt-plus", '<svg viewBox="0 0 48 48"><rect width="48" height="48" rx="12" fill="#0284C7"/></svg>')

    # Ensure SVG has class
    svg_styled = svg_content.replace("<svg ", '<svg class="tool-logo-svg" ')

    plans = tool.get("plans", [])
    plans_pills = " • ".join([p["name"].split(" (")[0] for p in plans])

    # Build accordion plan rows
    plan_rows_html = []
    for plan in plans:
        badge = f'<span class="mini-badge">{plan["badge"]}</span>' if plan.get("badge") else ""
        features_txt = " • ".join(plan.get("features", [])[:2])
        plan_rows_html.append(f'''
          <div class="inline-plan-row">
            <div class="inline-plan-info">
              <div class="inline-plan-name">{plan['name']} {badge}</div>
              <div class="inline-plan-meta">⏱ {plan['duration']} | 👤 {plan['seats']}</div>
              <div class="inline-plan-features">{features_txt}</div>
            </div>
            <div class="inline-plan-pricing">
              <div class="inline-price-pkr">Rs. {plan['price_pkr']:,}</div>
              <div class="inline-price-usd">(~${plan['price_usd']:.2f} USD)</div>
              <button type="button" class="btn-mini-order" onclick="openOrderDrawer('{slug}', '{plan['plan_id']}')">Select Plan</button>
            </div>
          </div>
        ''')

    accordion_content = "\n".join(plan_rows_html)

    card = f'''
    <div class="tool-item-card" data-category="{cat_key}" data-name="{tool['name'].lower()}" data-slug="{slug}">
      <div class="tool-header">
        <div class="tool-logo-wrap">
          {svg_styled}
        </div>
        <div class="tool-badges">
          <span class="category-pill">{tool.get('category_label', 'Software')}</span>
          <span class="plans-count-pill">{len(plans)} Plans</span>
        </div>
      </div>
      <h3 class="tool-name">{tool['name']}</h3>
      <div class="tool-brand-name">{tool.get('vendor', tool.get('brand', ''))}</div>
      <p class="tool-desc">{tool['description']}</p>
      
      <div class="tool-pricing-box">
        <div class="tool-price-from">Starting from</div>
        <div class="tool-price-main">Rs. {tool['starting_price_pkr']:,} <span class="tool-price-curr">PKR</span></div>
        <div class="tool-price-sub">(~${tool['starting_price_usd']:.2f} USD) • 15m WhatsApp Delivery</div>
      </div>

      <div class="tool-actions-row">
        <button type="button" class="btn-toggle-plans" onclick="togglePlanAccordion(this, '{slug}')">
          <span>Compare {len(plans)} Plans</span>
          <span class="chevron">▼</span>
        </button>
        <button type="button" class="btn-card-order" onclick="openOrderDrawer('{slug}')">
          ⚡ Quick Order
        </button>
      </div>

      <!-- Expandable Multi-Plan Comparison Accordion -->
      <div class="tool-plan-accordion" id="accordion-{slug}">
        <div class="accordion-inner">
          <div class="accordion-title">Verified Plan Variants for {tool['name']}:</div>
          {accordion_content}
        </div>
      </div>
    </div>
    '''
    cards_html.append(card)

all_cards_str = "\n".join(cards_html)

# Category buttons HTML
cat_buttons = []
for key, label in categories.items():
    active_cls = "active" if key == "all" else ""
    cat_buttons.append(f'<button type="button" class="cat-filter-btn {active_cls}" onclick="filterMasterCategory(\'{key}\', this)">{label}</button>')
cat_buttons_html = "\n".join(cat_buttons)

html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AIDigiTools — Complete 40+ Tools Master Catalog & Plan Comparison Preview</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --brand-navy: #0F172A;
      --brand-blue: #0284C7;
      --brand-cyan: #00B4D8;
      --brand-emerald: #10B981;
      --brand-purple: #8B5CF6;
      --bg-page: #F8FAFC;
      --bg-surface: #FFFFFF;
      --bg-card-subtle: #F1F5F9;
      --border-subtle: #E2E8F0;
      --border-focus: #0284C7;
      --text-primary: #0F172A;
      --text-secondary: #475569;
      --text-muted: #64748B;
      --shadow-sm: 0 2px 6px rgba(15, 23, 42, 0.04);
      --shadow-card: 0 6px 18px rgba(15, 23, 42, 0.06);
      --shadow-hover: 0 14px 30px rgba(15, 23, 42, 0.12);
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      --font-display: 'Space Grotesk', system-ui, -apple-system, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font-body);
      background: var(--bg-page);
      color: var(--text-primary);
      line-height: 1.5;
      padding-bottom: 5rem;
    }}

    /* --- Brand Header & Orbit Emblem --- */
    header {{
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
    }}
    .nav-container {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .logo-wrap {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
      text-decoration: none;
    }}
    .logo-emblem {{
      width: 44px;
      height: 44px;
    }}
    .logo-text {{
      display: flex;
      flex-direction: column;
    }}
    .logo-brand {{
      font-family: var(--font-display);
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--brand-navy);
      letter-spacing: -0.02em;
    }}
    .logo-brand .ai {{ color: #00B4D8; }}
    .logo-tagline {{
      font-size: 0.68rem;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}
    .header-actions {{
      display: flex;
      align-items: center;
      gap: 1rem;
    }}
    .stats-badge {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: #F0FDF4;
      color: #166534;
      border: 1px solid #BBF7D0;
      padding: 0.4rem 0.85rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
    }}
    .btn-header-order {{
      background: linear-gradient(135deg, #0284C7 0%, #4361EE 100%);
      color: #FFFFFF;
      padding: 0.55rem 1.15rem;
      border-radius: 10px;
      font-weight: 700;
      font-size: 0.88rem;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
    }}

    /* --- Hero Banner --- */
    .hero-banner {{
      max-width: 1320px;
      margin: 2.5rem auto 1.5rem;
      padding: 0 1.5rem;
      text-align: center;
    }}
    .hero-pill {{
      display: inline-block;
      background: #E0F2FE;
      color: #0369A1;
      padding: 0.35rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      margin-bottom: 0.85rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .hero-title {{
      font-family: var(--font-display);
      font-size: 2.5rem;
      font-weight: 800;
      color: var(--brand-navy);
      letter-spacing: -0.03em;
      margin-bottom: 0.75rem;
      line-height: 1.2;
    }}
    .hero-subtitle {{
      font-size: 1.1rem;
      color: var(--text-secondary);
      max-width: 760px;
      margin: 0 auto 1.8rem;
    }}

    /* --- Search & Category Controls --- */
    .controls-container {{
      max-width: 1320px;
      margin: 0 auto 2rem;
      padding: 0 1.5rem;
    }}
    .search-box-wrap {{
      max-width: 600px;
      margin: 0 auto 1.5rem;
      position: relative;
    }}
    .search-input {{
      width: 100%;
      padding: 0.85rem 1.25rem 0.85rem 3rem;
      border-radius: 14px;
      border: 1.5px solid var(--border-subtle);
      background: #FFFFFF;
      font-family: var(--font-body);
      font-size: 1rem;
      color: var(--text-primary);
      box-shadow: var(--shadow-sm);
      outline: none;
      transition: all 0.2s ease;
    }}
    .search-input:focus {{
      border-color: var(--brand-blue);
      box-shadow: 0 0 0 4px rgba(2, 132, 199, 0.15);
    }}
    .search-icon {{
      position: absolute;
      left: 1.1rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 1.1rem;
    }}

    .category-pills-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
    }}
    .cat-filter-btn {{
      padding: 0.5rem 1rem;
      border-radius: 9999px;
      border: 1.5px solid var(--border-subtle);
      background: #FFFFFF;
      color: var(--text-secondary);
      font-family: var(--font-body);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .cat-filter-btn:hover {{
      border-color: var(--brand-blue);
      color: var(--brand-blue);
      background: #F0F9FF;
    }}
    .cat-filter-btn.active {{
      background: var(--brand-navy);
      color: #FFFFFF;
      border-color: var(--brand-navy);
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.15);
    }}

    /* --- Catalog Grid --- */
    .catalog-grid {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
      gap: 1.75rem;
    }}

    .tool-item-card {{
      background: var(--bg-surface);
      border: 1.5px solid var(--border-subtle);
      border-radius: 20px;
      padding: 1.65rem;
      box-shadow: var(--shadow-card);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }}
    .tool-item-card:hover {{
      transform: translateY(-4px);
      box-shadow: var(--shadow-hover);
      border-color: #0284C7;
    }}

    .tool-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 1.1rem;
    }}
    .tool-logo-wrap {{
      width: 52px;
      height: 52px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #F8FAFC;
      box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
      overflow: hidden;
    }}
    .tool-logo-svg {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    .tool-badges {{
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 0.3rem;
    }}
    .category-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      color: #0284C7;
      background: #F0F9FF;
      padding: 0.2rem 0.6rem;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .plans-count-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      color: #10B981;
      background: #ECFDF5;
      padding: 0.15rem 0.55rem;
      border-radius: 6px;
    }}

    .tool-name {{
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--brand-navy);
      margin-bottom: 0.25rem;
      line-height: 1.3;
    }}
    .tool-brand-name {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-bottom: 0.75rem;
    }}
    .tool-desc {{
      font-size: 0.88rem;
      color: var(--text-secondary);
      line-height: 1.45;
      margin-bottom: 1.25rem;
      flex-grow: 1;
    }}

    .tool-pricing-box {{
      background: #F8FAFC;
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 0.85rem 1rem;
      margin-bottom: 1.2rem;
    }}
    .tool-price-from {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}
    .tool-price-main {{
      font-size: 1.45rem;
      font-weight: 800;
      color: #0284C7;
      line-height: 1.2;
    }}
    .tool-price-curr {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--brand-navy);
    }}
    .tool-price-sub {{
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 0.25rem;
    }}

    .tool-actions-row {{
      display: flex;
      gap: 0.6rem;
    }}
    .btn-toggle-plans {{
      flex: 1;
      padding: 0.65rem 0.85rem;
      border-radius: 10px;
      border: 1.5px solid var(--border-subtle);
      background: #FFFFFF;
      color: var(--brand-navy);
      font-weight: 700;
      font-size: 0.82rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      transition: all 0.15s ease;
    }}
    .btn-toggle-plans:hover {{
      border-color: #0284C7;
      background: #F0F9FF;
      color: #0284C7;
    }}
    .btn-toggle-plans .chevron {{
      font-size: 0.68rem;
      transition: transform 0.2s ease;
    }}
    .btn-toggle-plans.open .chevron {{
      transform: rotate(180deg);
    }}

    .btn-card-order {{
      padding: 0.65rem 1.15rem;
      border-radius: 10px;
      background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
      color: #FFFFFF;
      font-weight: 700;
      font-size: 0.82rem;
      border: none;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.2);
      transition: all 0.15s ease;
    }}
    .btn-card-order:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }}

    /* Accordion */
    .tool-plan-accordion {{
      display: none;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px dashed var(--border-subtle);
      animation: fadeIn 0.2s ease;
    }}
    .tool-plan-accordion.open {{
      display: block;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .accordion-title {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--brand-blue);
      margin-bottom: 0.75rem;
    }}
    .inline-plan-row {{
      background: #F8FAFC;
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 0.75rem 0.85rem;
      margin-bottom: 0.6rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
    }}
    .inline-plan-info {{
      flex-grow: 1;
    }}
    .inline-plan-name {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--brand-navy);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}
    .mini-badge {{
      background: #E0F2FE;
      color: #0369A1;
      font-size: 0.65rem;
      font-weight: 700;
      padding: 0.1rem 0.4rem;
      border-radius: 4px;
    }}
    .inline-plan-meta {{
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-top: 0.15rem;
    }}
    .inline-plan-features {{
      font-size: 0.72rem;
      color: var(--text-secondary);
      margin-top: 0.25rem;
    }}
    .inline-plan-pricing {{
      text-align: right;
      flex-shrink: 0;
    }}
    .inline-price-pkr {{
      font-size: 0.95rem;
      font-weight: 800;
      color: #0284C7;
    }}
    .inline-price-usd {{
      font-size: 0.68rem;
      color: var(--text-muted);
    }}
    .btn-mini-order {{
      margin-top: 0.35rem;
      background: var(--brand-navy);
      color: #FFFFFF;
      border: none;
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s ease;
    }}
    .btn-mini-order:hover {{
      background: #0284C7;
    }}

    /* --- Quick Order Slide-Over Drawer --- */
    .drawer-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 999;
      display: none;
      opacity: 0;
      transition: opacity 0.25s ease;
    }}
    .drawer-backdrop.active {{
      display: block;
      opacity: 1;
    }}
    .order-drawer {{
      position: fixed;
      top: 0;
      right: -480px;
      width: 480px;
      max-width: 95vw;
      height: 100vh;
      background: #FFFFFF;
      z-index: 1000;
      box-shadow: -10px 0 35px rgba(15, 23, 42, 0.2);
      transition: right 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
    }}
    .order-drawer.active {{
      right: 0;
    }}
    .drawer-header {{
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #F8FAFC;
    }}
    .drawer-header-title {{
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--brand-navy);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .drawer-close {{
      background: none;
      border: none;
      font-size: 1.5rem;
      color: var(--text-muted);
      cursor: pointer;
      line-height: 1;
    }}
    .drawer-body {{
      padding: 1.5rem;
      overflow-y: auto;
      flex-grow: 1;
    }}

    .drawer-tool-summary {{
      display: flex;
      align-items: center;
      gap: 1rem;
      background: #F8FAFC;
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 1rem;
      margin-bottom: 1.5rem;
    }}
    .drawer-tool-icon {{
      width: 48px;
      height: 48px;
      border-radius: 12px;
      overflow: hidden;
      flex-shrink: 0;
    }}
    .drawer-tool-title {{
      font-weight: 700;
      font-size: 1.05rem;
      color: var(--brand-navy);
    }}
    .drawer-tool-sub {{
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    .drawer-section-label {{
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-secondary);
      margin-bottom: 0.6rem;
    }}
    .drawer-plans-list {{
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
      margin-bottom: 1.5rem;
    }}
    .drawer-plan-card {{
      border: 1.5px solid var(--border-subtle);
      border-radius: 12px;
      padding: 0.85rem 1rem;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
      transition: all 0.15s ease;
    }}
    .drawer-plan-card:hover {{
      border-color: #0284C7;
      background: #F0F9FF;
    }}
    .drawer-plan-card.active {{
      border-color: #0284C7;
      background: #F0F9FF;
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.15);
    }}
    .drawer-plan-name {{
      font-weight: 700;
      font-size: 0.92rem;
      color: var(--brand-navy);
    }}
    .drawer-plan-meta {{
      font-size: 0.75rem;
      color: var(--text-muted);
    }}
    .drawer-plan-price {{
      text-align: right;
    }}
    .drawer-plan-pkr {{
      font-weight: 800;
      font-size: 1rem;
      color: #0284C7;
    }}
    .drawer-plan-usd {{
      font-size: 0.72rem;
      color: var(--text-muted);
    }}

    .rail-options-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.5rem;
      margin-bottom: 1.5rem;
    }}
    .rail-btn {{
      padding: 0.65rem 0.75rem;
      border: 1px solid var(--border-subtle);
      background: #FFFFFF;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      transition: all 0.15s ease;
    }}
    .rail-btn.active {{
      border-color: #0284C7;
      background: #F0F9FF;
      color: #0284C7;
      font-weight: 700;
    }}

    .drawer-footer {{
      padding: 1.25rem 1.5rem;
      border-top: 1px solid var(--border-subtle);
      background: #F8FAFC;
    }}
    .drawer-total-row {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 1rem;
    }}
    .drawer-total-label {{
      font-size: 0.88rem;
      color: var(--text-secondary);
      font-weight: 600;
    }}
    .drawer-total-pkr {{
      font-size: 1.65rem;
      font-weight: 800;
      color: #0284C7;
      line-height: 1;
    }}
    .drawer-total-usd {{
      font-size: 0.82rem;
      color: var(--text-muted);
      text-align: right;
    }}
    .btn-drawer-checkout {{
      width: 100%;
      padding: 0.95rem;
      border-radius: 12px;
      background: #25D366;
      color: #FFFFFF;
      font-weight: 700;
      font-size: 1rem;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      text-decoration: none;
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.3);
      transition: transform 0.15s ease;
    }}
    .btn-drawer-checkout:hover {{
      transform: translateY(-2px);
      background: #20BD5A;
    }}

    @media (max-width: 768px) {{
      .hero-title {{ font-size: 1.85rem; }}
      .catalog-grid {{ grid-template-columns: 1fr; }}
      .order-drawer {{ width: 100vw; }}
    }}
  </style>
</head>
<body>

  <!-- Brand Header -->
  <header>
    <div class="nav-container">
      <div class="logo-wrap">
        <svg class="logo-emblem" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg">
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
          <path d="M 12 62 C 12 36, 126 18, 134 38" stroke="url(#navOrbit)" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.65"/>
          <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" fill="url(#navTeal)"/>
          <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" fill="url(#navPurple)"/>
          <path d="M 46 64 C 52 58, 66 56, 80 62 L 72 74 C 62 70, 52 72, 46 76 Z" fill="url(#navTeal)" opacity="0.95"/>
          <path d="M 134 38 C 142 58, 38 88, 16 66" stroke="url(#navOrbit)" stroke-width="4.5" stroke-linecap="round" fill="none"/>
          <circle cx="124" cy="34" r="5.5" fill="#4361EE"/>
        </svg>
        <div class="logo-text">
          <span class="logo-brand"><span class="ai">AI</span> DigiTools</span>
          <span class="logo-tagline">CANONICAL DIGITAL PRODUCTS CATALOG</span>
        </div>
      </div>
      <div class="header-actions">
        <span class="stats-badge">✓ 40 Verified Tools • 81 Plans</span>
        <button type="button" class="btn-header-order" onclick="openOrderDrawer('chatgpt-plus')">⚡ Quick Order Drawer</button>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero-banner">
    <span class="hero-pill">Official 40-Tool Catalog & Plan Comparison Hub</span>
    <h1 class="hero-title">Browse All 40+ Tools &amp; Verified Plans</h1>
    <p class="hero-subtitle">
      Compare genuinely distinct official subscription tiers across AI Models, Developer Coding IDEs, Graphic Design, Video/Audio Generators, Cyber VPNs, and Streaming with transparent Pakistani Rupee (PKR) pricing and zero foreign forex barriers.
    </p>
  </section>

  <!-- Search & Category Filters -->
  <section class="controls-container">
    <div class="search-box-wrap">
      <span class="search-icon">🔍</span>
      <input type="text" id="liveSearchInput" class="search-input" placeholder="Search 40+ tools by name, category, or features (e.g. YouTube, ChatGPT, Canva, Midjourney)..." oninput="handleLiveSearch(this.value)">
    </div>

    <div class="category-pills-bar">
      {cat_buttons_html}
    </div>
  </section>

  <!-- Catalog Grid -->
  <main class="catalog-grid" id="catalogGrid">
    {all_cards_str}
  </main>

  <!-- Slide-Over Quick Order Drawer -->
  <div class="drawer-backdrop" id="drawerBackdrop" onclick="closeOrderDrawer()"></div>
  <aside class="order-drawer" id="orderDrawer" aria-label="Quick Order Drawer">
    <div class="drawer-header">
      <div class="drawer-header-title">
        <span>⚡</span>
        <span>Quick Order Checkout</span>
      </div>
      <button type="button" class="drawer-close" onclick="closeOrderDrawer()">&times;</button>
    </div>

    <div class="drawer-body">
      <!-- Tool Info Box -->
      <div class="drawer-tool-summary">
        <div class="drawer-tool-icon" id="drawerToolIcon"></div>
        <div>
          <div class="drawer-tool-title" id="drawerToolTitle">Tool Name</div>
          <div class="drawer-tool-sub" id="drawerToolSub">Category • Vendor</div>
        </div>
      </div>

      <!-- Plan Selector -->
      <div class="drawer-section-label">Select Verified Plan:</div>
      <div class="drawer-plans-list" id="drawerPlansList"></div>

      <!-- Payment Rail Selector -->
      <div class="drawer-section-label">Select Payment Rail:</div>
      <div class="rail-options-grid">
        <button type="button" class="rail-btn active" onclick="selectRail('EasyPaisa', this)">EasyPaisa</button>
        <button type="button" class="rail-btn" onclick="selectRail('JazzCash', this)">JazzCash</button>
        <button type="button" class="rail-btn" onclick="selectRail('SadaPay', this)">SadaPay</button>
        <button type="button" class="rail-btn" onclick="selectRail('Bank IBFT', this)">Bank Transfer</button>
        <button type="button" class="rail-btn" onclick="selectRail('Nayapay', this)">Nayapay</button>
        <button type="button" class="rail-btn" onclick="selectRail('Crypto USDT', this)">Crypto / USDT</button>
      </div>

      <!-- Trust Assurance Box -->
      <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:0.75rem; font-size:0.78rem; color:#166534; line-height:1.4;">
        <strong>🛡️ AIDigiTools Guarantee:</strong> 15-Minute WhatsApp electronic dispatch, dedicated setup guide, and 30-Day full replacement warranty protection.
      </div>
    </div>

    <div class="drawer-footer">
      <div class="drawer-total-row">
        <div>
          <div class="drawer-total-label">Total Payable:</div>
          <div class="drawer-total-pkr" id="drawerTotalPkr">Rs. 0</div>
        </div>
        <div class="drawer-total-usd" id="drawerTotalUsd">(~$0.00 USD)</div>
      </div>
      <a href="#" id="drawerWhatsappBtn" target="_blank" rel="noopener noreferrer" class="btn-drawer-checkout">
        <span>Order on WhatsApp (03326861112)</span>
        <span>→</span>
      </a>
    </div>
  </aside>

  <script>
    var CATALOG_DATA = {json.dumps(catalog)};
    var currentSelectedTool = CATALOG_DATA["chatgpt-plus"];
    var currentSelectedPlan = currentSelectedTool.plans[0];
    var currentRail = "EasyPaisa";

    // Toggle Plan Accordion on Cards
    function togglePlanAccordion(btn, slug) {{
      var accordion = document.getElementById('accordion-' + slug);
      if (!accordion) return;
      var isOpen = accordion.classList.contains('open');
      if (isOpen) {{
        accordion.classList.remove('open');
        btn.classList.remove('open');
      }} else {{
        accordion.classList.add('open');
        btn.classList.add('open');
      }}
    }}

    // Category Filter
    function filterMasterCategory(catKey, btn) {{
      var pills = document.querySelectorAll('.cat-filter-btn');
      pills.forEach(function(p) {{ p.classList.remove('active'); }});
      if (btn) btn.classList.add('active');

      var cards = document.querySelectorAll('.tool-item-card');
      cards.forEach(function(card) {{
        var cCat = card.getAttribute('data-category');
        if (catKey === 'all' || cCat === catKey) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Live Search
    function handleLiveSearch(query) {{
      var q = (query || '').toLowerCase().trim();
      var cards = document.querySelectorAll('.tool-item-card');
      cards.forEach(function(card) {{
        var name = card.getAttribute('data-name') || '';
        var text = card.textContent.toLowerCase();
        if (!q || name.indexOf(q) !== -1 || text.indexOf(q) !== -1) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Open Drawer
    function openOrderDrawer(slug, planId) {{
      var tool = CATALOG_DATA[slug] || CATALOG_DATA["chatgpt-plus"];
      currentSelectedTool = tool;

      if (planId && tool.plans) {{
        currentSelectedPlan = tool.plans.find(function(p) {{ return p.plan_id === planId; }}) || tool.plans[0];
      }} else if (tool.plans && tool.plans.length > 0) {{
        currentSelectedPlan = tool.plans[0];
      }}

      // Populate Tool Summary
      var iconWrap = document.getElementById('drawerToolIcon');
      var cardIcon = document.querySelector('[data-slug=\"' + slug + '\"] .tool-logo-wrap');
      if (iconWrap && cardIcon) {{
        iconWrap.innerHTML = cardIcon.innerHTML;
      }}
      document.getElementById('drawerToolTitle').textContent = tool.name;
      document.getElementById('drawerToolSub').textContent = tool.category_label + ' • ' + (tool.vendor || tool.brand);

      // Populate Plans
      renderDrawerPlans();
      updateDrawerSummary();

      document.getElementById('drawerBackdrop').classList.add('active');
      document.getElementById('orderDrawer').classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeOrderDrawer() {{
      document.getElementById('drawerBackdrop').classList.remove('active');
      document.getElementById('orderDrawer').classList.remove('active');
      document.body.style.overflow = '';
    }}

    function selectPlanInDrawer(planId) {{
      var found = currentSelectedTool.plans.find(function(p) {{ return p.plan_id === planId; }});
      if (found) {{
        currentSelectedPlan = found;
        renderDrawerPlans();
        updateDrawerSummary();
      }}
    }}

    function renderDrawerPlans() {{
      var list = document.getElementById('drawerPlansList');
      if (!list || !currentSelectedTool.plans) return;

      var html = '';
      currentSelectedTool.plans.forEach(function(plan) {{
        var isActive = currentSelectedPlan && currentSelectedPlan.plan_id === plan.plan_id;
        var activeClass = isActive ? ' active' : '';
        html += '<div class=\"drawer-plan-card' + activeClass + '\" onclick=\"selectPlanInDrawer(\\'' + plan.plan_id + '\\')\">';
        html += '<div>';
        html += '<div class=\"drawer-plan-name\">' + plan.name + '</div>';
        html += '<div class=\"drawer-plan-meta\">⏱ ' + plan.duration + ' • 👤 ' + plan.seats + '</div>';
        html += '</div>';
        html += '<div class=\"drawer-plan-price\">';
        html += '<div class=\"drawer-plan-pkr\">Rs. ' + plan.price_pkr.toLocaleString() + '</div>';
        html += '<div class=\"drawer-plan-usd\">(~$' + plan.price_usd.toFixed(2) + ' USD)</div>';
        html += '</div>';
        html += '</div>';
      }});
      list.innerHTML = html;
    }}

    function selectRail(railName, btn) {{
      currentRail = railName;
      var btns = document.querySelectorAll('.rail-btn');
      btns.forEach(function(b) {{ b.classList.remove('active'); }});
      if (btn) btn.classList.add('active');
      updateDrawerSummary();
    }}

    function updateDrawerSummary() {{
      if (!currentSelectedPlan) return;

      var pkr = currentSelectedPlan.price_pkr;
      var usd = currentSelectedPlan.price_usd;

      document.getElementById('drawerTotalPkr').textContent = 'Rs. ' + pkr.toLocaleString() + ' PKR';
      document.getElementById('drawerTotalUsd').textContent = '(~$' + usd.toFixed(2) + ' USD)';

      var waMsg = "Hi AIDigiTools! I want to order " + currentSelectedTool.name + " (" + currentSelectedPlan.name + ") for Rs. " + pkr.toLocaleString() + " PKR (~$" + usd.toFixed(2) + " USD) via " + currentRail + ". Please share payment details and 15m delivery activation.";
      var btn = document.getElementById('drawerWhatsappBtn');
      if (btn) {{
        btn.href = "https://wa.me/923326861112?text=" + encodeURIComponent(waMsg);
      }}
    }}

    // Close on Escape key
    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeOrderDrawer();
    }});
  </script>
</body>
</html>
'''

with open(DEST_FILE, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Master preview file generated successfully at {DEST_FILE} ({len(html_template)} bytes)")
