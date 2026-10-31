import json
import xml.etree.ElementTree as ET
import re
import os

with open('data/products_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

tree = ET.parse('merchant_feed.xml')
channel = tree.getroot().find('channel')
feed_items = {item.find('{http://base.google.com/ns/1.0}id').text.replace('aidigitools-', ''): item for item in channel.findall('item')}

discrepancies = []
for p in master:
    slug = p['slug']
    html_path = f'tools/{slug}.html'
    if not os.path.exists(html_path):
        discrepancies.append(f'Missing HTML file: {html_path}')
        continue
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if not h1_match:
        discrepancies.append(f'{slug}: Missing H1')
    
    # Check Price in JSON-LD schema
    schema_matches = re.findall(r'<script[^>]*type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
    found_prod_schema = False
    for sm in schema_matches:
        try:
            sd = json.loads(sm.strip())
            if isinstance(sd, dict) and sd.get('@type') == 'Product':
                found_prod_schema = True
                offers = sd.get('offers', {})
                schema_price = str(offers.get('price'))
                expected_price = str(p['aidigitools_price_pkr'])
                if schema_price != expected_price:
                    discrepancies.append(f'{slug}: Schema price mismatch ({schema_price} vs {expected_price})')
        except Exception:
            pass
    if not found_prod_schema:
        discrepancies.append(f'{slug}: Missing Product schema')

    # Check Feed item
    if slug not in feed_items:
        discrepancies.append(f'{slug}: Missing in merchant feed')
    else:
        item = feed_items[slug]
        feed_price = item.find('{http://base.google.com/ns/1.0}price').text
        expected_feed_price = f"{p['aidigitools_price_pkr']} PKR"
        if feed_price != expected_feed_price:
            discrepancies.append(f'{slug}: Feed price mismatch ({feed_price} vs {expected_feed_price})')

print(f"Total discrepancies found: {len(discrepancies)}")
if discrepancies:
    for d in discrepancies[:20]:
        print(f"  - {d}")
else:
    print("SUCCESS: 100% parity across Master JSON, HTML Schema, and Merchant Feed!")
