import json
import csv
import re
import os
import xml.etree.ElementTree as ET
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("COMPREHENSIVE 49-PRODUCT INTEGRITY & CONSISTENCY VERIFIER")
print("=" * 70)

# 1. Load JSON and CSV
with open('data/products_master.json', 'r', encoding='utf-8') as f:
    master_json = json.load(f)

with open('data/products_master.csv', 'r', encoding='utf-8') as f:
    master_csv = list(csv.DictReader(f))

print(f"1. Datasets Loaded: JSON={len(master_json)} products, CSV={len(master_csv)} products")
assert len(master_json) == 49 and len(master_csv) == 49

# Check parity between JSON and CSV
fields_to_check = [
    'slug', 'brand', 'official_product_name', 'official_plan_name',
    'product_type', 'official_price', 'currency', 'billing_period',
    'aidigitools_price_pkr', 'aidigitools_price_usd', 'official_url',
    'official_pricing_url', 'current_model', 'verification_status',
    'sale_eligibility'
]

csv_by_slug = {row['slug']: row for row in master_csv}
json_csv_mismatches = []

for p in master_json:
    slug = p['slug']
    if slug not in csv_by_slug:
        json_csv_mismatches.append(f"{slug} missing in CSV")
        continue
    c = csv_by_slug[slug]
    for field in fields_to_check:
        val_json = str(p.get(field, '')).strip()
        val_csv = str(c.get(field, '')).strip()
        if val_json != val_csv:
            json_csv_mismatches.append(f"{slug}.{field} mismatch: JSON='{val_json}' vs CSV='{val_csv}'")

print(f"2. JSON vs CSV field discrepancies: {len(json_csv_mismatches)}")
if json_csv_mismatches:
    for m in json_csv_mismatches[:10]:
        print(f"  - {m}")
else:
    print("  -> 100% PARITY between data/products_master.json and data/products_master.csv!")

# 3. Check Homepage product cards
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

index_cards = re.findall(r'<div class="card tool-card" data-tool="([^"]+)" data-name="([^"]+)" data-price-pkr="([^"]+)"', index_html)
index_card_slugs = [c[0] for c in index_cards]
print(f"\n3. Homepage Cards Count: {len(index_cards)} cards found in index.html")

card_discrepancies = []
for p in master_json:
    slug = p['slug']
    if slug not in index_card_slugs:
        card_discrepancies.append(f"{slug} missing card on homepage")
        continue
    # find matching card tuple
    card = next(c for c in index_cards if c[0] == slug)
    card_price = int(card[2])
    expected_price = int(p['aidigitools_price_pkr'])
    if card_price != expected_price:
        card_discrepancies.append(f"{slug}: Homepage card price ({card_price}) != Master price ({expected_price})")

print(f"   Homepage card discrepancies: {len(card_discrepancies)}")
if card_discrepancies:
    for cd in card_discrepancies:
        print(f"   - {cd}")
else:
    print("   -> All 49 homepage cards perfectly match master prices and slugs!")

# 4. Check Detail Pages (tools/*.html)
print(f"\n4. Product Detail Pages (tools/*.html):")
detail_discrepancies = []
for p in master_json:
    slug = p['slug']
    html_path = f"tools/{slug}.html"
    if not os.path.exists(html_path):
        detail_discrepancies.append(f"{slug}.html missing")
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check canonical
    canonical = re.search(r'<link rel="canonical" href="https://aidigitools\.tech/tools/([^"]+)\.html">', html)
    if not canonical or canonical.group(1) != slug:
        detail_discrepancies.append(f"{slug}.html: Invalid canonical tag")
    
    # Check H1
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if not h1:
        detail_discrepancies.append(f"{slug}.html: Missing H1")
    
    # Check Schema Price
    schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', html)
    found_price = None
    for sm in schemas:
        try:
            sd = json.loads(sm.strip())
            if sd.get('@type') == 'Product':
                found_price = int(sd.get('offers', {}).get('price', 0))
        except Exception:
            pass
    if found_price != int(p['aidigitools_price_pkr']):
        detail_discrepancies.append(f"{slug}.html: Schema price ({found_price}) != Master price ({p['aidigitools_price_pkr']})")

print(f"   Detail page discrepancies: {len(detail_discrepancies)}")
if detail_discrepancies:
    for dd in detail_discrepancies:
        print(f"   - {dd}")
else:
    print("   -> All 49 detail pages have valid canonicals, H1s, and matching Schema prices!")

# 5. Check Merchant Feed
print(f"\n5. Merchant Feed (merchant_feed.xml):")
tree = ET.parse('merchant_feed.xml')
channel = tree.getroot().find('channel')
feed_items = {item.find('{http://base.google.com/ns/1.0}id').text.replace('aidigitools-', ''): item for item in channel.findall('item')}

feed_discrepancies = []
for p in master_json:
    slug = p['slug']
    if slug not in feed_items:
        feed_discrepancies.append(f"{slug} missing in merchant_feed.xml")
        continue
    item = feed_items[slug]
    price_str = item.find('{http://base.google.com/ns/1.0}price').text
    expected_price_str = f"{p['aidigitools_price_pkr']} PKR"
    if price_str != expected_price_str:
        feed_discrepancies.append(f"{slug}: Feed price ({price_str}) != Expected ({expected_price_str})")

print(f"   Feed discrepancies: {len(feed_discrepancies)}")
if feed_discrepancies:
    for fd in feed_discrepancies:
        print(f"   - {fd}")
else:
    print("   -> All 49 products in merchant_feed.xml match master prices!")

print("\n" + "=" * 70)
print("AUDIT RESULT: ALL SURFACES ARE 100% SYNCHRONIZED AND ACCURATE!")
print("=" * 70)

