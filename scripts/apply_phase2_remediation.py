"""
scripts/apply_phase2_remediation.py
Phase 2 remediation script for AIDigiTools:
- Reconciles Midjourney price drift across cart.js and tools/midjourney.html
- Reconciles Runway Gen-3 pricing contradictions in compare/runway-vs-pika.html and best/best-ai-video-generators.html
- Clarifies Pika 2.0 CTA in compare/runway-vs-pika.html (inquiry-only for uncataloged tool)
- Fixes drawerPlansContainer DOM ID bug in assets/cart.js
- Standardizes footer SVG gradient IDs (navTeal -> footerTeal, etc.) across all subpages
- Fixes heading hierarchy in footer columns (h4 -> h3) across all subpages
- Normalizes brand tagline casing (all-caps -> title case) across all pages
- Fixes escaped ampersands (&amp; -> &) in llms.txt
- Safely removes unreferenced root asset 'AI DigiTools Orbit Emblem.png'
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def fix_cart_js():
    cart_path = os.path.join(ROOT_DIR, 'assets', 'cart.js')
    with open(cart_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Midjourney starting price and basic plan
    # In midjourney block:
    # "starting_price_pkr": 1800, "starting_price_usd": 6.5,
    # "price_pkr": 1800, "price_usd": 6.5,
    orig = content
    content = re.sub(
        r'("midjourney":\s*\{[^}]*?"starting_price_pkr":\s*)1800(,\s*"starting_price_usd":\s*)6\.5',
        r'\g<1>2800\g<2>10.0',
        content,
        count=1
    )
    content = re.sub(
        r'("plan_id":\s*"PLAN-MIDJ-BASIC-1M"[^}]*?"price_pkr":\s*)1800(,\s*"price_usd":\s*)6\.5',
        r'\g<1>2800\g<2>10.0',
        content,
        count=1
    )

    # 2. Fix drawerPlansContainer -> drawerPlanSelectorContainer
    content = content.replace("document.getElementById('drawerPlansContainer')", "document.getElementById('drawerPlanSelectorContainer')")

    if content != orig:
        with open(cart_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ assets/cart.js updated (Midjourney 2800 PKR & drawerPlanSelectorContainer).")
    else:
        print("! assets/cart.js already up to date.")

def fix_midjourney_html():
    mj_path = os.path.join(ROOT_DIR, 'tools', 'midjourney.html')
    with open(mj_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    # Update Basic Plan card
    content = content.replace(
        '<span class="plan-price-pkr">Rs. 1,800</span>\n          <span class="plan-price-sub">PKR (~$6.50 USD) / 1 Month (30 Days)</span>',
        '<span class="plan-price-pkr">Rs. 2,800</span>\n          <span class="plan-price-sub">PKR (~$10.00 USD) / 1 Month (30 Days)</span>'
    )
    content = content.replace(
        '<span class="plan-price-pkr">Rs. 1,800</span>\r\n          <span class="plan-price-sub">PKR (~$6.50 USD) / 1 Month (30 Days)</span>',
        '<span class="plan-price-pkr">Rs. 2,800</span>\r\n          <span class="plan-price-sub">PKR (~$10.00 USD) / 1 Month (30 Days)</span>'
    )

    if content != orig:
        with open(mj_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ tools/midjourney.html updated (Basic plan price 2,800 PKR).")
    else:
        print("! tools/midjourney.html already up to date.")

def fix_runway_vs_pika():
    path = os.path.join(ROOT_DIR, 'compare', 'runway-vs-pika.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    # Quick answer price reconciliation
    content = content.replace(
        'Runway Gen-3 provides cinematic camera control from Rs. 3,500 PKR ($12 USD), while Pika 2.0 specializes in creative physics effects from Rs. 2,800 PKR ($10 USD)',
        'Runway Gen-3 provides cinematic camera control from Rs. 1,800 PKR ($6.50 USD), while Pika 2.0 specializes in creative physics effects from Rs. 2,800 PKR ($10 USD)'
    )
    # Badge
    content = content.replace(
        '<span class="badge">Runway: Rs. 3,500 PKR ($12 USD)</span>',
        '<span class="badge">Runway: Rs. 1,800 PKR ($6.50 USD)</span>'
    )
    # Comparison table
    content = content.replace(
        '<td>Rs. 3,500 PKR / $12 USD</td>',
        '<td>Rs. 1,800 PKR / $6.50 USD</td>'
    )
    # Runway CTA
    content = content.replace(
        'Order Runway (Rs. 3,500)',
        'Inquire Runway (Rs. 1,800)'
    )
    # Pika CTA
    content = content.replace(
        'Order Pika (Rs. 2,800)',
        'Inquire Availability for Pika'
    )

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ compare/runway-vs-pika.html updated (Runway 1,800 PKR, Pika inquiry CTA).")
    else:
        print("! compare/runway-vs-pika.html already up to date.")

def fix_best_video():
    path = os.path.join(ROOT_DIR, 'best', 'best-ai-video-generators.html')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    content = content.replace(
        '<span class="badge">Runway Gen-3: Rs. 3,500 PKR ($12 USD)</span>',
        '<span class="badge">Runway Gen-3: Rs. 1,800 PKR ($6.50 USD)</span>'
    )
    content = content.replace(
        '<div style="margin: 1rem 0; font-size: 1.15rem; font-weight: 700; color: var(--accent-gold);">Rs. 3,500 / month</div>',
        '<div style="margin: 1rem 0; font-size: 1.15rem; font-weight: 700; color: var(--accent-gold);">Rs. 1,800 / month</div>'
    )

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ best/best-ai-video-generators.html updated (Runway 1,800 PKR).")
    else:
        print("! best/best-ai-video-generators.html already up to date.")

def fix_llms_txt():
    path = os.path.join(ROOT_DIR, 'llms.txt')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    content = content.replace('&amp;', '&')

    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ llms.txt updated (ampersands unescaped).")
    else:
        print("! llms.txt already up to date.")

def fix_footers_and_taglines():
    svg_fixed_count = 0
    h4_fixed_count = 0
    tagline_fixed_count = 0

    for root, _, files in os.walk(ROOT_DIR):
        if any(p in root for p in ['.git', 'node_modules', '.gemini']):
            continue
        for f in files:
            if not f.endswith('.html'):
                continue
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()

            orig = content

            # Fix tagline casing
            if 'SMART TOOLS • BIGGER POSSIBILITIES' in content:
                content = content.replace(
                    '<span class="tagline">SMART TOOLS • BIGGER POSSIBILITIES</span>',
                    '<span class="tagline">Smart Tools • Bigger Possibilities</span>'
                )
                if content != orig:
                    tagline_fixed_count += 1

            # Fix footer SVG and h4
            footer_idx = content.find('<footer')
            if footer_idx != -1:
                header_part = content[:footer_idx]
                footer_part = content[footer_idx:]

                # In footer only: rename SVG duplicate IDs
                if 'id="navTeal"' in footer_part or 'id="navPurple"' in footer_part or 'id="navOrbit"' in footer_part:
                    new_footer = footer_part.replace('id="navTeal"', 'id="footerTeal"')
                    new_footer = new_footer.replace('id="navPurple"', 'id="footerPurple"')
                    new_footer = new_footer.replace('id="navOrbit"', 'id="footerOrbit"')
                    new_footer = new_footer.replace('url(#navTeal)', 'url(#footerTeal)')
                    new_footer = new_footer.replace('url(#navPurple)', 'url(#footerPurple)')
                    new_footer = new_footer.replace('url(#navOrbit)', 'url(#footerOrbit)')
                    if new_footer != footer_part:
                        footer_part = new_footer
                        svg_fixed_count += 1

                # In footer only: replace <div class="footer-col">\s*<h4> with <h3>
                if '<div class="footer-col">' in footer_part and '<h4>' in footer_part:
                    new_footer = re.sub(
                        r'(<div class="footer-col"[^>]*>[\s\S]*?)<h4>([\s\S]*?)</h4>',
                        r'\g<1><h3>\g<2></h3>',
                        footer_part
                    )
                    if new_footer != footer_part:
                        footer_part = new_footer
                        h4_fixed_count += 1

                content = header_part + footer_part

            if content != orig:
                with open(path, 'w', encoding='utf-8') as fp:
                    fp.write(content)

    print(f"✓ Tagline normalized in {tagline_fixed_count} HTML files.")
    print(f"✓ Footer SVG gradient IDs isolated in {svg_fixed_count} HTML files.")
    print(f"✓ Footer heading hierarchy (h4 -> h3) repaired in {h4_fixed_count} HTML files.")

def remove_unused_root_asset():
    asset_path = os.path.join(ROOT_DIR, 'AI DigiTools Orbit Emblem.png')
    if os.path.exists(asset_path):
        os.remove(asset_path)
        print("✓ Unreferenced root asset 'AI DigiTools Orbit Emblem.png' removed.")
    else:
        print("! 'AI DigiTools Orbit Emblem.png' does not exist in root.")

if __name__ == '__main__':
    print("--- Applying Phase 2 Catalog & Architecture Remediation ---")
    fix_cart_js()
    fix_midjourney_html()
    fix_runway_vs_pika()
    fix_best_video()
    fix_llms_txt()
    fix_footers_and_taglines()
    remove_unused_root_asset()
    print("--- Phase 2 Remediation Complete ---")
