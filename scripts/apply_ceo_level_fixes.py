"""
scripts/apply_ceo_level_fixes.py
Applies CEO-level master data and showcase synchronization:
1. Updates scripts/generate_products_master.py with true prices and regenerates data/products_master.json and csv.
2. Re-orders plans in tools/semrush-guru.html so Guru (2500 PKR) is Plan 1, matching Hero, Schema, and Cart.
3. Adds PLAN-SEMRUSH-PRO-1M (1900 PKR) to assets/cart.js and scripts/tools_catalog.json as Plan 2 so no orphaned plan exists.
4. Generates comprehensive 49-tool #showcaseToolSelect in index.html with accurate verified prices and categories.
"""

import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def update_master_generator():
    path = os.path.join(ROOT_DIR, 'scripts', 'generate_products_master.py')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # microsoft-office-365
    c = re.sub(
        r'("slug":\s*"microsoft-office-365"[\s\S]*?"aidigitools_price_pkr":\s*)1100(,\s*"aidigitools_price_usd":\s*)4\.0',
        r'\g<1>1950\g<2>7.0',
        c
    )
    # prime-video
    c = re.sub(
        r'("slug":\s*"prime-video"[\s\S]*?"aidigitools_price_pkr":\s*)700(,\s*"aidigitools_price_usd":\s*)2\.5',
        r'\g<1>650\g<2>2.4',
        c
    )
    # spotify-premium
    c = re.sub(
        r'("slug":\s*"spotify-premium"[\s\S]*?"aidigitools_price_pkr":\s*)650(,\s*"aidigitools_price_usd":\s*)2\.5',
        r'\g<1>850\g<2>3.2',
        c
    )
    # tradingview-pro
    c = re.sub(
        r'("slug":\s*"tradingview-pro"[\s\S]*?"aidigitools_price_pkr":\s*)2800(,\s*"aidigitools_price_usd":\s*)10\.0',
        r'\g<1>3200\g<2>11.5',
        c
    )
    # turnitin-student
    c = re.sub(
        r'("slug":\s*"turnitin-student"[\s\S]*?"aidigitools_price_pkr":\s*)950(,\s*"aidigitools_price_usd":\s*)3\.5',
        r'\g<1>2800\g<2>10.0',
        c
    )
    # windows-11-pro
    c = re.sub(
        r'("slug":\s*"windows-11-pro"[\s\S]*?"aidigitools_price_pkr":\s*)1500(,\s*"aidigitools_price_usd":\s*)5\.5',
        r'\g<1>1850\g<2>6.8',
        c
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✓ Updated scripts/generate_products_master.py.")

    # Re-run generate_products_master.py
    os.system(f'python "{path}"')

def fix_semrush_guru():
    # 1. In tools/semrush-guru.html, swap Pro and Guru plan cards so Guru is Plan 1
    sg_path = os.path.join(ROOT_DIR, 'tools', 'semrush-guru.html')
    with open(sg_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract the two plan cards
    pro_match = re.search(r'(<div class="plan-card" id="plan-PLAN-SEMRUSH-PRO-1M">[\s\S]*?</div>\s*</div>)', html)
    guru_match = re.search(r'(<div class="plan-card" id="plan-PLAN-SEMRUSH-GURU-1M">[\s\S]*?</div>\s*</div>)', html)

    if pro_match and guru_match:
        pro_card = pro_match.group(1)
        guru_card = guru_match.group(1)

        # Check if pro comes before guru
        if html.find('plan-PLAN-SEMRUSH-PRO-1M') < html.find('plan-PLAN-SEMRUSH-GURU-1M'):
            # Swap them
            new_grid = f"""      <div class="plans-grid">
      {guru_card}
      {pro_card}
      </div>"""
            html = re.sub(r'<div class="plans-grid">[\s\S]*?</div>\s*</div>\s*</section>', new_grid + '\n    </section>', html)
            with open(sg_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print("✓ tools/semrush-guru.html: Guru Platform (2500 PKR) is now Plan 1.")

    # 2. Add PLAN-SEMRUSH-PRO-1M to cart.js
    cart_path = os.path.join(ROOT_DIR, 'assets', 'cart.js')
    with open(cart_path, 'r', encoding='utf-8') as f:
        cart_content = f.read()

    pro_plan_obj = {
        "plan_id": "PLAN-SEMRUSH-PRO-1M",
        "name": "Pro Tier (1 Month)",
        "plan_type": "Pro",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1900,
        "price_usd": 7.0,
        "features": [
            "5 projects & 500 keywords tracked daily",
            "Domain & keyword analytics with competitor traffic estimates",
            "On-page SEO checker & site audit crawler (100k pages)",
            "PDF export reports"
        ],
        "limits": "Single user account terms apply",
        "badge": "Freelancer Pick",
        "availability": "InStock"
    }

    if '"PLAN-SEMRUSH-PRO-1M"' not in cart_content:
        # insert after PLAN-SEMRUSH-GURU-1M
        target = '"plan_id": "PLAN-SEMRUSH-GURU-1M"'
        idx = cart_content.find(target)
        if idx != -1:
            end_brace = cart_content.find('}', idx)
            insert_str = ',\n      ' + json.dumps(pro_plan_obj, indent=6)[6:]
            cart_content = cart_content[:end_brace+1] + insert_str + cart_content[end_brace+1:]
            with open(cart_path, 'w', encoding='utf-8') as f:
                f.write(cart_content)
            print("✓ assets/cart.js: Added PLAN-SEMRUSH-PRO-1M as Plan 2 for Semrush.")

    # 3. Add to scripts/tools_catalog.json
    cat_path = os.path.join(ROOT_DIR, 'scripts', 'tools_catalog.json')
    with open(cat_path, 'r', encoding='utf-8') as f:
        cat = json.load(f)

    if len(cat['semrush-guru']['plans']) == 1:
        cat['semrush-guru']['plans'].append(pro_plan_obj)
        cat['semrush-guru']['total_plans'] = 2
        with open(cat_path, 'w', encoding='utf-8') as f:
            json.dump(cat, f, indent=2, ensure_ascii=False)
        print("✓ scripts/tools_catalog.json: Added PLAN-SEMRUSH-PRO-1M as Plan 2.")

def build_showcase_select():
    # Load products master
    master_path = os.path.join(ROOT_DIR, 'data', 'products_master.json')
    with open(master_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # Group products by category
    categories = [
        ("ai", "⭐ Featured AI Assistants", ["google-ai-ultra", "chatgpt-plus", "claude-pro", "gemini-advanced", "perplexity-pro", "deepseek-pro", "grok-ai"]),
        ("coding", "💻 AI Coding & Developer Tools", ["cursor-pro", "github-copilot", "lovable-ai", "jetbrains-all", "replit-core", "chatgpt-codex", "claude-artifacts", "n8n-automation"]),
        ("video", "🎬 AI Video & Audio Engines", ["runway-gen3", "kling-ai", "google-veo", "minimax-ai", "heygen-ai", "capcut-pro", "vidiq-boost", "elevenlabs-creator", "suno-ai", "udio-ai"]),
        ("image", "🎨 Design, Image & Creative Studios", ["midjourney", "canva-pro", "adobe-creative-cloud", "figma-pro", "freepik-premium", "envato-elements", "leonardo-ai"]),
        ("vpn", "🔒 VPN & Workstation Privacy", ["nordvpn", "surfshark-vpn"]),
        ("productivity", "⚡ Productivity, SEO & Enterprise", ["semrush-guru", "notion-business", "gamma-app", "microsoft-office-365", "windows-11-pro", "tradingview-pro", "linkedin-premium", "grammarly-pro", "quillbot-premium"]),
        ("education", "🎓 Online Learning & Academic Tools", ["coursera-plus", "turnitin-student"]),
        ("streaming", "📺 Streaming & Entertainment", ["netflix-premium", "youtube-premium", "spotify-premium", "prime-video"])
    ]

    prod_map = {p['slug']: p for p in products}

    options_html = ['<select id="showcaseToolSelect" class="authkit-tool-select" onchange="setMasterTool(this.value)">']

    all_slotted = set()
    for cat_key, cat_label, slugs in categories:
        options_html.append(f'              <optgroup label="{cat_label}" data-cat="{cat_key}">')
        for s in slugs:
            all_slotted.add(s)
            p = prod_map.get(s)
            if not p:
                continue
            name = p['official_product_name']
            pkr = p['aidigitools_price_pkr']
            usd = p['aidigitools_price_usd']
            sel = ' selected' if s == 'chatgpt-plus' else ''
            options_html.append(f'                <option value="{s}"{sel}>{name} — Rs. {pkr:,} PKR / ${usd:.2f} USD</option>')
        options_html.append('              </optgroup>')

    options_html.append('          </select>')
    new_select_str = '\n'.join(options_html)

    # Replace in index.html
    index_path = os.path.join(ROOT_DIR, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        idx_content = f.read()

    idx_content = re.sub(
        r'<select id="showcaseToolSelect"[^>]*>[\s\S]*?</select>',
        new_select_str,
        idx_content
    )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(idx_content)
    print(f"✓ index.html: Updated #showcaseToolSelect with all {len(all_slotted)} products across 8 categories.")

if __name__ == '__main__':
    print("--- Applying CEO Level Forensic Fixes ---")
    update_master_generator()
    fix_semrush_guru()
    build_showcase_select()
    print("--- Done Applying Fixes ---")
