import re

with open(r'c:\Users\Dell\Desktop\aidigitools\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find tools grid section
m = re.search(r'<section[^>]*id=["\'](?:tools|products|catalog)["\'][^>]*>(.*?)</section>', text, re.DOTALL | re.IGNORECASE)
if not m:
    # search for class containing tools or products
    m = re.search(r'<section[^>]*class=["\'][^"\']*(?:tools|grid|catalog)[^"\']*["\'][^>]*>(.*?)</section>', text, re.DOTALL | re.IGNORECASE)

print("Found section:", bool(m))

tool_links = re.findall(r'href=["\'](?:/tools/|tools/)([^"\']+)["\']', text)
unique_links = []
for l in tool_links:
    if l not in unique_links:
        unique_links.append(l)

print(f"Total unique tool links in index.html: {len(unique_links)}")
for i, l in enumerate(unique_links):
    print(f"{i+1}. {l}")
