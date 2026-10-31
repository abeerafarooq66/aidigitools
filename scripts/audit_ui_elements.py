import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
for folder in ['tools', 'categories', 'best', 'compare', 'guides']:
    if os.path.isdir(folder):
        html_files.extend([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.html')])

print(f"Total HTML files to scan: {len(html_files)}")

# 1. Check for any remaining 'WhatsApp Concierge' in button/visible text
concierge_findings = []
for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if 'WhatsApp Concierge' in line:
            # ignore comments or meta tags if any
            if not line.strip().startswith('<!--') and not line.strip().startswith('<meta'):
                concierge_findings.append((path, idx + 1, line.strip()))

print(f"\n1. 'WhatsApp Concierge' in visible text: {len(concierge_findings)} found")
for c in concierge_findings[:10]:
    print(f"  {c[0]}:{c[1]} -> {c[2][:80]}")

# 2. Check for button classes that mix .btn with .btn-primary, .btn-secondary, etc.
# Check for any button with missing explicit background or color
btn_findings = []
for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Find all button or anchor tags with class containing btn
    btn_tags = re.findall(r'<[a-z]+[^>]+class=[\'"][^\'"]*btn[^\'"]*[\'"][^>]*>', content)
    for b in btn_tags:
        # Check if inline style contains color:#fff or color:white without background
        if ('color:#fff' in b.lower() or 'color: #fff' in b.lower() or 'color:white' in b.lower()) and 'background' not in b.lower():
            btn_findings.append((path, b))

print(f"\n2. Button tags with inline white text but no inline background: {len(btn_findings)}")
for b in btn_findings[:10]:
    print(f"  {b[0]} -> {b[1][:100]}")

# 3. Check for any elements with 'WhatsApp Inquiry' where 'Quick Order' or 'WhatsApp Contact' should be
inquiry_findings = []
for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        if 'WhatsApp Inquiry' in line:
            inquiry_findings.append((path, idx + 1, line.strip()))

print(f"\n3. 'WhatsApp Inquiry' in HTML files: {len(inquiry_findings)} found")
for inf in inquiry_findings[:10]:
    print(f"  {inf[0]}:{inf[1]} -> {inf[2][:80]}")
