# scripts/upgrade_canonical_storefront.py
import os
import json
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, "scripts", "tools_catalog.json")

with open(CATALOG_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} canonical product families.")

# 1. UPDATE ALL 52 HTML PAGES TO INCLUDE DRAWER PLAN SELECTOR CONTAINER
pages_updated_drawer = 0
for root, dirs, files in os.walk(BASE_DIR):
    # Skip .git, scratch, venv
    if ".git" in root or "scratch" in root:
        continue
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as fl:
                content = fl.read()

            if "cartDrawer" in content and "drawerPlanSelectorContainer" not in content:
                # Find where to insert drawerPlanSelectorContainer
                # Target: right after <div class="cart-item-preview">...</div>
                target = '</div>\n      </div>\n\n      <!-- Plan Duration Selection -->'
                replacement = '</div>\n      </div>\n\n      <!-- Canonical Plan Selector Container -->\n      <div id="drawerPlanSelectorContainer" style="margin-bottom: 1.25rem;"></div>\n\n      <!-- Plan Duration Selection -->'
                
                if target in content:
                    content = content.replace(target, replacement, 1)
                    with open(path, "w", encoding="utf-8") as fl:
                        fl.write(content)
                    pages_updated_drawer += 1
                else:
                    # Alternative target
                    alt_target = '<div class="cart-section-title">Select Subscription Duration:</div>'
                    if alt_target in content:
                        replacement = '<div id="drawerPlanSelectorContainer" style="margin-bottom: 1.25rem;"></div>\n        <div class="cart-section-title">Select Subscription Duration:</div>'
                        content = content.replace(alt_target, replacement, 1)
                        with open(path, "w", encoding="utf-8") as fl:
                            fl.write(content)
                        pages_updated_drawer += 1

print(f"Inserted drawerPlanSelectorContainer in {pages_updated_drawer} HTML pages.")

# 2. UPGRADE 36 TOOL PAGES WITH PLAN COMPARISON SECTION
tools_dir = os.path.join(BASE_DIR, "tools")
tool_pages_upgraded = 0

for slug, fam in catalog.items():
    tool_file = os.path.join(tools_dir, f"{slug}.html")
    if not os.path.exists(tool_file):
        print(f"Warning: Tool file not found: {tool_file}")
        continue

    with open(tool_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Build Plan Comparison HTML
    plans = fam.get("plans", [])
    plans_cards_html = []
    
    for plan in plans:
        is_featured = "Most Popular" in plan.get("badge", "") or "Best Value" in plan.get("badge", "")
        featured_class = " featured" if is_featured else ""
        badge_html = f'<div class="plan-badge-top">{plan["badge"]}</div>' if plan.get("badge") else ""
        
        features_list_html = "\n".join([
            f'          <li class="plan-feature-item"><span class="plan-feature-check">✓</span><span>{feat}</span></li>'
            for feat in plan.get("features", [])
        ])
        
        card = f'''      <div class="plan-card{featured_class}" id="plan-{plan['plan_id']}">
        {badge_html}
        <div class="plan-tier-label">{plan.get('plan_type', 'Plan Tier')}</div>
        <h3 class="plan-title">{plan['name']}</h3>
        <div class="plan-price-wrap">
          <span class="plan-price-pkr">Rs. {plan['price_pkr']:,}</span>
          <span class="plan-price-sub">PKR (~${plan['price_usd']:.2f} USD) / {plan['duration']}</span>
        </div>
        <div class="plan-meta-row">
          <span class="plan-pill">⏱ {plan['duration']}</span>
          <span class="plan-pill">👤 {plan['seats']}</span>
          <span class="plan-pill">⚡ 15m Delivery</span>
        </div>
        <ul class="plan-features-list">
{features_list_html}
        </ul>
        <div class="plan-terms-note">
          <strong>Terms &amp; SLA:</strong> {plan['limits']}
        </div>
        <button type="button" class="btn-choose-plan" onclick="openQuickOrderModal('{slug}', '{plan['plan_id']}')" aria-label="Choose {plan['name']}">
          <span>Choose {plan['name']}</span>
          <span>→</span>
        </button>
      </div>'''
        plans_cards_html.append(card)

    all_cards_joined = "\n".join(plans_cards_html)
    
    plan_section_html = f'''
    <!-- Canonical Plan Comparison Section -->
    <section class="plans-comparison-section" id="compare-plans">
      <h2 class="section-title">Compare Verified {fam['name']} Plans</h2>
      <p class="section-subtitle">Genuinely distinct official plan variants with transparent Pakistani pricing and verified SLA terms.</p>
      <div class="plans-grid">
{all_cards_joined}
      </div>
    </section>
'''

    # If already has plans-comparison-section, replace it
    if 'class="plans-comparison-section"' in html:
        html = re.sub(
            r'<!-- Canonical Plan Comparison Section -->.*?<!-- /Canonical Plan Comparison Section -->',
            f'<!-- Canonical Plan Comparison Section -->{plan_section_html}<!-- /Canonical Plan Comparison Section -->',
            html,
            flags=re.DOTALL
        )
    else:
        # Insert right after the first </section> in <main>
        first_section_end = html.find("</section>")
        if first_section_end != -1:
            insertion_point = first_section_end + len("</section>")
            html = html[:insertion_point] + "\n" + f'<!-- Canonical Plan Comparison Section -->{plan_section_html}<!-- /Canonical Plan Comparison Section -->' + html[insertion_point:]

    # Also update logo asset to ../assets/product-logos/{slug}.svg if ../assets/images/icons/{slug}.svg is used
    old_icon = f'../assets/images/icons/{slug}.svg'
    new_icon = f'../assets/product-logos/{slug}.svg'
    if old_icon in html:
        html = html.replace(old_icon, new_icon)

    # Update Hero CTA to include "Compare Plans" button if not already present
    if '#compare-plans' not in html:
        hero_btn_match = re.search(r'(<a href="https://wa\.me/[^"]+" class="btn-whatsapp">[^<]+</a>)', html)
        if hero_btn_match:
            original_btn = hero_btn_match.group(1)
            replacement_btns = f'{original_btn}\n      <a href="#compare-plans" class="btn-secondary" style="margin-left:0.6rem; display:inline-flex; align-items:center; gap:0.4rem; padding:0.85rem 1.4rem; border-radius:12px; font-weight:700; text-decoration:none; background:var(--bg-card); color:var(--text-primary); border:1.5px solid var(--border-color); vertical-align:middle;">Compare {len(plans)} Plans ↓</a>'
            html = html.replace(original_btn, replacement_btns, 1)

    with open(tool_file, "w", encoding="utf-8") as f:
        f.write(html)
    tool_pages_upgraded += 1

print(f"Successfully upgraded {tool_pages_upgraded} tool pages with Plan Comparison sections!")

# 3. UPGRADE INDEX.HTML TOOL CARDS WITH STARTING PRICES AND VERIFIED PLAN LINKS
index_file = os.path.join(BASE_DIR, "index.html")
with open(index_file, "r", encoding="utf-8") as f:
    index_html = f.read()

# Replace icon references to assets/product-logos/
for slug in catalog.keys():
    old_card_icon = f'src="assets/images/icons/{slug}.svg"'
    new_card_icon = f'src="assets/product-logos/{slug}.svg"'
    if old_card_icon in index_html:
        index_html = index_html.replace(old_card_icon, new_card_icon)

with open(index_file, "w", encoding="utf-8") as f:
    f.write(index_html)

print("Updated index.html tool card brand logos to assets/product-logos/")
