import json
import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/products_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

print(f"Total products in master: {len(master)}")

for idx, p in enumerate(master, 1):
    print(f"\n[{idx}] SLUG: {p['slug']}")
    print(f"    Current Brand: {p.get('brand')}")
    print(f"    Official Product Name: {p.get('official_product_name')}")
    print(f"    Official Plan Name: {p.get('official_plan_name')}")
    print(f"    Product Type: {p.get('product_type')}")
    print(f"    Current Model: {p.get('current_model')}")
    print(f"    Official URL: {p.get('official_url')}")
    print(f"    Pricing URL: {p.get('official_pricing_url')}")
    print(f"    Official Price: {p.get('official_price')} {p.get('currency')} / {p.get('billing_period')}")
    print(f"    AIDigiTools Price: Rs {p.get('aidigitools_price_pkr')} (${p.get('aidigitools_price_usd')})")
    print(f"    Features: {p.get('features')}")
    print(f"    Limitations: {p.get('limitations')}")

