import os
import re

matches = {}

for root, dirs, files in os.walk('.'):
    if '.git' in root: continue
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            m = re.findall(r'href=["\'](https://wa\.me/923326861112\?[^"\']+)["\']', c)
            orders = [l for l in m if 'want%20to%20order' in l or 'want+to+order' in l or 'want to order' in l]
            if orders:
                matches[p] = len(orders)

print(f"Files containing direct paid order links: {len(matches)}")
for p, count in matches.items():
    print(f"  {p}: {count} links")
