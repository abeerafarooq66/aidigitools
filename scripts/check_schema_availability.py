import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

tools_dir = 'tools'
tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.html')]

print(f"Inspecting Product schema offers across all {len(tool_files)} tool pages...")

held_slugs = ['turnitin-student', 'linkedin-premium', 'netflix-premium', 'spotify-premium', 'coursera-plus']
non_separate_slugs = ['claude-artifacts', 'deepseek-pro']
all_restricted = held_slugs + non_separate_slugs

active_in_stock = 0
restricted_out_of_stock = 0
anomalies = []

for f in sorted(tool_files):
    slug = f.replace('.html', '')
    path = os.path.join(tools_dir, f)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    scripts = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', content)
    for s in scripts:
        try:
            data = json.loads(s)
            if data.get('@type') == 'Product':
                offers = data.get('offers', {})
                avail = offers.get('availability', 'NONE')
                price = offers.get('price', 'NONE')
                if slug in all_restricted:
                    if avail == 'https://schema.org/OutOfStock':
                        restricted_out_of_stock += 1
                    else:
                        anomalies.append((slug, f"Restricted but availability is {avail}"))
                else:
                    if avail == 'https://schema.org/InStock':
                        active_in_stock += 1
                    else:
                        anomalies.append((slug, f"Active but availability is {avail}"))
        except Exception as e:
            anomalies.append((slug, f"Error parsing JSON: {e}"))

print(f"Active InStock products: {active_in_stock} / 42")
print(f"Restricted OutOfStock products: {restricted_out_of_stock} / 7")
print(f"Anomalies: {len(anomalies)}")
for a in anomalies:
    print(f"  {a[0]} -> {a[1]}")
