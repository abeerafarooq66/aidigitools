import re

with open(r'c:\Users\Dell\Desktop\aidigitools\assets\style.css', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'(\.[a-zA-Z0-9_-]*(?:badge|rank|cat)[a-zA-Z0-9_-]*\s*\{[^}]+\})', text)
for b in m[:10]:
    print(b)
