import json
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/products_master.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)

with open('data/products_master.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data_csv = list(reader)

print(f"JSON count: {len(data_json)}")
print(f"CSV count: {len(data_csv)}")

# Check slug alignment
json_slugs = [p['slug'] for p in data_json]
csv_slugs = [p['slug'] for p in data_csv]
assert json_slugs == csv_slugs, "Slug order or content mismatch between JSON and CSV!"

statuses = {}
sale_elig = {}

for p in data_json:
    st = p.get('verification_status', 'UNKNOWN')
    se = p.get('sale_eligibility', 'UNKNOWN')
    statuses[st] = statuses.get(st, 0) + 1
    sale_elig[se] = sale_elig.get(se, 0) + 1

print("\nVerification Statuses in JSON:")
for k, v in statuses.items():
    print(f"  {k}: {v}")

print("\nSale Eligibility in JSON:")
for k, v in sale_elig.items():
    print(f"  {k}: {v}")

print("\nRestricted Products (Not VERIFIED or Not ELIGIBLE):")
restricted = []
for p in data_json:
    st = p.get('verification_status')
    se = p.get('sale_eligibility')
    if st != 'VERIFIED' or se != 'ELIGIBLE':
        restricted.append(p)
        print(f"  - {p['slug']} ({p.get('display_name')}): Status='{st}', Eligibility='{se}', Type='{p.get('product_type')}'")

print(f"\nTotal restricted products: {len(restricted)}")
