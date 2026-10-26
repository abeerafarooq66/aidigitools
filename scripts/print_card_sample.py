import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\Dell\Desktop\aidigitools\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div class="grid" id="toolsGrid">(.*?)</div>\s*</section>', text, re.DOTALL)
if m:
    grid = m.group(1)
    raw_cards = grid.split('<div class="card tool-card"')
    for c in raw_cards[1:]:
        if 'chatgpt-plus.html' in c:
            print(c[300:])
            break
