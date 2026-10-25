import re

with open(r'c:\Users\Dell\Desktop\aidigitools\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div class="grid" id="toolsGrid">(.*?)</div>\s*</section>', text, re.DOTALL)
if m:
    grid_content = m.group(1)
    # Split by <div class="card tool-card"
    cards = grid_content.split('<div class="card tool-card"')
    print(f"Total tool cards found: {len(cards)-1}")
    for i, c in enumerate(cards[1:]):
        h3 = re.search(r'<h3>(.*?)</h3>', c)
        title = h3.group(1) if h3 else "No H3"
        price = re.search(r'<span class="tool-price">(.*?)</span>', c)
        price_val = price.group(1) if price else "No price"
        link = re.search(r'href="([^"]+)"', c)
        link_val = link.group(1) if link else "No link"
        print(f"{i+1:2d}. {title:35s} | {price_val:20s} | {link_val}")
