import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

title = re.search(r'<title>(.*?)</title>', html)
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
print('Title:', title.group(1) if title else 'None')
print('H1:', re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else 'None')

# Find all section tags and their headings
matches = re.finditer(r'<section([^>]*)>', html)
for m in matches:
    attrs = m.group(1)
    id_m = re.search(r'id=["\'](.*?)["\']', attrs)
    class_m = re.search(r'class=["\'](.*?)["\']', attrs)
    id_val = id_m.group(1) if id_m else 'none'
    class_val = class_m.group(1) if class_m else 'none'
    
    # search next 400 chars for heading
    snippet = html[m.end():m.end()+600]
    h2_m = re.search(r'<h2[^>]*>(.*?)</h2>', snippet, re.DOTALL)
    h2_val = re.sub(r'<[^>]+>', '', h2_m.group(1)).strip() if h2_m else 'No H2'
    print(f"Section id='{id_val}' class='{class_val}' -> H2: '{h2_val}'")
