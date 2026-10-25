import re

with open(r'c:\Users\Dell\Desktop\aidigitools\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div class="grid" id="toolsGrid">(.*?)</div>\s*</section>', text, re.DOTALL)
if m:
    grid = m.group(1)
    # Split by <div class="card tool-card"
    raw_cards = grid.split('<div class="card tool-card"')
    card_dict = {}
    for c in raw_cards[1:]:
        full_card = '<div class="card tool-card"' + c
        # find link to tool page
        link_m = re.search(r'href="(tools/[^"]+\.html)"', c)
        if link_m:
            slug = link_m.group(1).replace('tools/', '').replace('.html', '')
            card_dict[slug] = full_card.strip()
    
    print(f"Mapped {len(card_dict)} cards by slug:")
    for slug in sorted(card_dict.keys()):
        print(f" - {slug}")
