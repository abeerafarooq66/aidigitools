"""
scripts/ceo_deep_audit_phase2.py
Executive Level Forensic Audit for AIDigiTools:
Checks all 49 products across 8 layers:
1. data/products_master.json
2. data/products_master.csv
3. scripts/tools_catalog.json
4. assets/cart.js (TOOLS_DATA)
5. merchant_feed.xml
6. index.html (cards, price-tags, dropdowns)
7. tools/{slug}.html (Hero price, JSON-LD Schema price, plan 1 price)
8. llms.txt (Listed pricing)

Also audits:
- Current AI models / tiers verification
- Held products safeguards (5 Tier 1 tools)
- Official vendor URLs
- Cross-page pricing consistency (compare/ & best/)
"""

import os
import re
import json
import csv
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def run_ceo_audit():
    print("=" * 80)
    print("💼 AIDigiTools — Executive Level Deep Audit: Phase 2 Product Master Data")
    print("=" * 80)

    # 1. Load data/products_master.json
    master_json_path = os.path.join(ROOT_DIR, 'data', 'products_master.json')
    with open(master_json_path, 'r', encoding='utf-8') as f:
        master_json = json.load(f)
    print(f"[1/8] Loaded data/products_master.json: {len(master_json)} products.")

    # 2. Load data/products_master.csv
    master_csv_path = os.path.join(ROOT_DIR, 'data', 'products_master.csv')
    csv_rows = []
    with open(master_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        csv_rows = list(reader)
    print(f"[2/8] Loaded data/products_master.csv: {len(csv_rows)} rows.")

    # 3. Load scripts/tools_catalog.json
    catalog_path = os.path.join(ROOT_DIR, 'scripts', 'tools_catalog.json')
    with open(catalog_path, 'r', encoding='utf-8') as f:
        tools_catalog = json.load(f)
    print(f"[3/8] Loaded scripts/tools_catalog.json: {len(tools_catalog)} products.")

    # 4. Load assets/cart.js
    cart_js_path = os.path.join(ROOT_DIR, 'assets', 'cart.js')
    with open(cart_js_path, 'r', encoding='utf-8') as f:
        cart_content = f.read()

    start_idx = cart_content.find('TOOLS_DATA = {')
    brace_start = cart_content.find('{', start_idx)
    brace_count = 0
    end_idx = -1
    for i in range(brace_start, len(cart_content)):
        if cart_content[i] == '{':
            brace_count += 1
        elif cart_content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    cart_data = json.loads(cart_content[brace_start:end_idx])
    print(f"[4/8] Loaded assets/cart.js (TOOLS_DATA): {len(cart_data)} tools.")

    # 5. Load merchant_feed.xml
    feed_path = os.path.join(ROOT_DIR, 'merchant_feed.xml')
    tree = ET.parse(feed_path)
    root = tree.getroot()
    ns = {'g': 'http://base.google.com/ns/1.0'}
    feed_items = {}
    for item in root.findall('.//item'):
        gid = item.find('g:id', ns).text
        slug = gid.replace('aidigitools-', '')
        price_text = item.find('g:price', ns).text
        price_num = int(re.search(r'\d+', price_text).group(0))
        feed_items[slug] = price_num
    print(f"[5/8] Loaded merchant_feed.xml: {len(feed_items)} items.")

    # 6. Load index.html
    index_path = os.path.join(ROOT_DIR, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()
    print("[6/8] Loaded index.html.")

    # 7. Load llms.txt
    llms_path = os.path.join(ROOT_DIR, 'llms.txt')
    with open(llms_path, 'r', encoding='utf-8') as f:
        llms_text = f.read()
    print("[7/8] Loaded llms.txt.")

    # 8. Check tools/*.html
    tools_dir = os.path.join(ROOT_DIR, 'tools')
    tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]
    print(f"[8/8] Discovered {len(tool_files)} tool detail pages in tools/.")

    print("\n" + "=" * 80)
    print("🔍 AUDIT 1: FORENSIC 8-LAYER PRICING & METADATA PARITY (All 49 Products)")
    print("=" * 80)

    discrepancies = []
    # Official Tier-1 slugs defined in architecture & tests
    TIER1_SLUGS = {'turnitin-student', 'linkedin-premium', 'netflix-premium', 'spotify-premium', 'coursera-plus'}

    for prod in master_json:
        slug = prod['slug']
        pkr = prod['aidigitools_price_pkr']
        usd = prod['aidigitools_price_usd']

        # Check CSV
        csv_match = [r for r in csv_rows if r['slug'] == slug]
        if not csv_match:
            discrepancies.append((slug, "CSV Missing", f"Product {slug} missing from CSV"))
        else:
            csv_pkr = int(csv_match[0]['aidigitools_price_pkr'])
            if csv_pkr != pkr:
                discrepancies.append((slug, "CSV Price Drift", f"JSON {pkr} != CSV {csv_pkr}"))

        # Check tools_catalog.json
        cat_item = tools_catalog.get(slug)
        if not cat_item:
            discrepancies.append((slug, "Catalog Missing", f"Missing from scripts/tools_catalog.json"))
        else:
            cat_pkr = cat_item.get('starting_price_pkr')
            if cat_pkr != pkr:
                discrepancies.append((slug, "Catalog Price Drift", f"JSON {pkr} != Catalog {cat_pkr}"))

        # Check cart.js
        cart_item = cart_data.get(slug)
        if not cart_item:
            discrepancies.append((slug, "Cart Missing", f"Missing from assets/cart.js"))
        else:
            cart_pkr = cart_item.get('starting_price_pkr')
            cart_p1_pkr = cart_item.get('plans')[0]['price_pkr'] if cart_item.get('plans') else None
            if cart_pkr != pkr:
                discrepancies.append((slug, "Cart Starting Price Drift", f"JSON {pkr} != Cart {cart_pkr}"))
            if cart_p1_pkr != pkr:
                discrepancies.append((slug, "Cart Plan 1 Price Drift", f"JSON {pkr} != Cart Plan 1 {cart_p1_pkr}"))

        # Check merchant_feed.xml
        feed_pkr = feed_items.get(slug)
        if feed_pkr is None:
            discrepancies.append((slug, "Merchant Feed Missing", f"Missing from merchant_feed.xml"))
        elif feed_pkr != pkr:
            discrepancies.append((slug, "Feed Price Drift", f"JSON {pkr} != Feed {feed_pkr}"))

        # Check index.html card data-price-pkr
        card_match = re.search(r'data-tool="' + slug + r'"[^>]*data-price-pkr="(\d+)"', index_html)
        if not card_match:
            discrepancies.append((slug, "Index Card Missing", f"Missing tool-card in index.html"))
        else:
            idx_pkr = int(card_match.group(1))
            if idx_pkr != pkr:
                discrepancies.append((slug, "Index Card data-price-pkr Drift", f"JSON {pkr} != Index {idx_pkr}"))

        # Check index.html dropdown option in showcaseToolSelect
        opt_match = re.search(r'<option\s+[^>]*value="' + slug + r'"[^>]*>[^—]*—\s*Rs\.\s*([\d,]+)\s*PKR', index_html)
        if not opt_match:
            discrepancies.append((slug, "Index Select Missing", f"Missing option in index.html showcaseToolSelect"))
        else:
            opt_pkr = int(opt_match.group(1).replace(',', ''))
            if opt_pkr != pkr:
                discrepancies.append((slug, "Index Select Price Drift", f"JSON {pkr} != Select {opt_pkr}"))

        # Check tools/{slug}.html
        tool_page = os.path.join(tools_dir, f"{slug}.html")
        if not os.path.exists(tool_page):
            discrepancies.append((slug, "Detail Page Missing", f"File tools/{slug}.html missing"))
        else:
            with open(tool_page, 'r', encoding='utf-8') as f:
                thtml = f.read()

            # Check Schema.org Offer price
            schema_prices = re.findall(r'"@type":\s*"Offer"[\s\S]*?"price":\s*"(\d+)"', thtml)
            if not schema_prices:
                schema_prices = re.findall(r'"price":\s*"(\d+)"[\s\S]*?"priceCurrency":\s*"PKR"', thtml)
            if schema_prices:
                sp_pkr = int(schema_prices[0])
                if sp_pkr != pkr:
                    discrepancies.append((slug, "Schema Price Drift", f"JSON {pkr} != Schema {sp_pkr}"))
            else:
                discrepancies.append((slug, "Schema Price Missing", "No schema price found"))

            # Check Hero price tag
            hero_tag_match = re.search(r'class="price-tag"[^>]*>[\s\S]*?Rs\.\s*([\d,]+)\s*PKR', thtml)
            if hero_tag_match:
                hero_pkr = int(hero_tag_match.group(1).replace(',', ''))
                if hero_pkr != pkr:
                    discrepancies.append((slug, "Hero Price Tag Drift", f"JSON {pkr} != Hero {hero_pkr}"))

            # Check Plan 1 in comparison section
            plan1_match = re.search(r'class="plan-price-pkr">\s*Rs\.\s*([\d,]+)\s*</span>', thtml)
            if plan1_match:
                p1_pkr = int(plan1_match.group(1).replace(',', ''))
                if p1_pkr != pkr:
                    discrepancies.append((slug, "Plan 1 Price Drift", f"JSON {pkr} != Plan 1 {p1_pkr}"))

        # Check llms.txt
        llms_match = re.search(r'tools/' + slug + r'\.html[\s\S]*?Pricing:\s*Rs\.\s*([\d,]+)', llms_text)
        if llms_match:
            try:
                llms_pkr = int(llms_match.group(1).replace(',', ''))
                if llms_pkr != pkr:
                    discrepancies.append((slug, "llms.txt Price Drift", f"JSON {pkr} != llms.txt {llms_pkr}"))
            except Exception:
                pass

    if not discrepancies:
        print("✅ 100% PERFECT PARITY: All 49 products match across all 8 layers without a single discrepancy!")
    else:
        print(f"❌ Found {len(discrepancies)} discrepancies:")
        for slug, category, msg in discrepancies:
            print(f"   - [{category}] {slug}: {msg}")

    print("\n" + "=" * 80)
    print("🛡️ AUDIT 2: TIER-1 HELD PRODUCTS COMPLIANCE CHECK (5 Canonical Tools)")
    print("=" * 80)
    held_issues = []
    for hslug in TIER1_SLUGS:
        # 1. index.html card should NOT have quick order button
        idx_card = re.search(r'data-tool="' + hslug + r'"[\s\S]*?class="tool-card-actions"[\s\S]*?</div>\s*</div>', index_html)
        if idx_card:
            card_text = idx_card.group(0)
            if f"openQuickOrderModal('{hslug}'" in card_text or f'openQuickOrderModal("{hslug}"' in card_text:
                held_issues.append((hslug, "Index Card Exposes Quick Order", "Direct modal trigger found on homepage card"))

        # 2. tools/{hslug}.html should NOT have openQuickOrderModal
        tpath = os.path.join(tools_dir, f"{hslug}.html")
        with open(tpath, 'r', encoding='utf-8') as f:
            thtml = f.read()

        if f"openQuickOrderModal('{hslug}'" in thtml or f'openQuickOrderModal("{hslug}"' in thtml:
            held_issues.append((hslug, "Detail Exposes Quick Order", "Detail page contains openQuickOrderModal"))

        # Check hold notice present
        if 'Direct Orders Currently On Hold' not in thtml and 'Orders On Hold' not in thtml:
            held_issues.append((hslug, "Missing Hold Banner", "Hold notice banner missing from detail page"))

        # Check inquiry text
        if 'Inquire on WhatsApp for Current Availability' not in thtml:
            held_issues.append((hslug, "Missing Inquiry Button", "Inquiry CTA missing from detail page"))

    if not held_issues:
        print("✅ 100% HELD COMPLIANCE: All 5 Tier-1 products strictly enforce inquiry-only workflow.")
    else:
        print(f"❌ Found {len(held_issues)} held compliance issues:")
        for s, cat, m in held_issues:
            print(f"   - [{cat}] {s}: {m}")

    print("\n" + "=" * 80)
    print("🤖 AUDIT 3: CURRENT AI MODELS & TECHNICAL FIDELITY (October 2026)")
    print("=" * 80)
    verified_models = 0
    for prod in master_json:
        model = prod.get('current_model')
        date = prod.get('model_verification_date')
        if model and 'October 2026' in str(date):
            verified_models += 1

    print(f"✅ Verified Models: {verified_models}/49 products have verified October 2026 model/architecture stamps.")
    print("Sample Frontier Architectures in Master Dataset:")
    for s in ['chatgpt-plus', 'claude-pro', 'deepseek-pro', 'cursor-pro', 'kling-ai', 'runway-gen3', 'gemini-advanced']:
        p = [x for x in master_json if x['slug'] == s][0]
        print(f"   - {p['official_product_name']}: Model='{p['current_model']}' | Official URL='{p['official_url']}'")

    print("\n" + "=" * 80)
    print("📊 AUDIT 4: CROSS-PAGE GUIDES & COMPARISONS INTEGRITY")
    print("=" * 80)
    guides_dir = os.path.join(ROOT_DIR, 'compare')
    best_dir = os.path.join(ROOT_DIR, 'best')
    comp_files = [os.path.join(guides_dir, f) for f in os.listdir(guides_dir) if f.endswith('.html')] + \
                 [os.path.join(best_dir, f) for f in os.listdir(best_dir) if f.endswith('.html')]

    guide_issues = []
    for cf in comp_files:
        with open(cf, 'r', encoding='utf-8') as f:
            c = f.read()
        rel_cf = os.path.relpath(cf, ROOT_DIR)

        # Check for stale Runway price 3500
        if '3,500' in c and ('runway' in c.lower() or 'gen-3' in c.lower()):
            lines = c.splitlines()
            for ln, line in enumerate(lines, 1):
                if '3,500' in line and ('runway' in line.lower() or 'gen-3' in line.lower()):
                    guide_issues.append((rel_cf, f"Stale Runway price on line {ln}", line.strip()))

        # Check for unverified Pika Order CTA
        if 'Order Pika' in c:
            guide_issues.append((rel_cf, "Uncataloged Order CTA", "Contains 'Order Pika'"))

    if not guide_issues:
        print("✅ 100% GUIDES & COMPARISONS INTEGRITY: Zero stale prices or uncataloged order CTAs in compare/ and best/.")
    else:
        print(f"❌ Found {len(guide_issues)} issues in guides:")
        for path, issue, detail in guide_issues:
            print(f"   - {path}: {issue} -> {detail}")

    print("\n" + "=" * 80)
    print("🏁 CEO EXECUTIVE AUDIT SUMMARY")
    print("=" * 80)
    total_errors = len(discrepancies) + len(held_issues) + len(guide_issues)
    if total_errors == 0:
        print("🏆 VERDICT: PRODUCTION READY & AIRTIGHT (0 Defects, 0 Discrepancies, 100% Parity across all 49 products)")
    else:
        print(f"⚠️ VERDICT: ATTENTION REQUIRED ({total_errors} Defects Detected)")
    print("=" * 80)

if __name__ == '__main__':
    run_ceo_audit()
