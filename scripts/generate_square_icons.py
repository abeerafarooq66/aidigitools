import os
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
manifest_path = ROOT / 'assets/product-logos/brand_logos_manifest.json'
manifest = json.load(open(manifest_path, 'r', encoding='utf-8'))
brands = {b['slug']: b for b in manifest['brands']}

tools = json.load(open(ROOT / 'data/products_master.json', 'r', encoding='utf-8'))

out_dir = ROOT / 'assets/images/square_svg'
out_dir.mkdir(parents=True, exist_ok=True)

print(f"Generating square SVGs for {len(tools)} tools...")
count = 0
for t in tools:
    slug = t['slug']
    b = brands.get(slug, {})
    color = b.get('hex_color', '#38bdf8')
    if color.lower() in ['#000000', '#000', '#111111']:
        color = '#ffffff'
    
    svg_file = ROOT / 'assets/product-logos' / f'{slug}.svg'
    if not svg_file.exists():
        continue
    
    raw_svg = svg_file.read_text(encoding='utf-8')
    
    # extract inner content of svg
    viewbox_match = re.search(r'viewBox=["\']([^"\']+)["\']', raw_svg)
    vb = viewbox_match.group(1) if viewbox_match else '0 0 24 24'
    
    inner_content = re.sub(r'<\?xml[^>]*\?>', '', raw_svg)
    inner_content = re.sub(r'<svg[^>]*>', '', inner_content)
    inner_content = inner_content.replace('</svg>', '').strip()
    inner_content = re.sub(r'<title>[^<]*</title>', '', inner_content)
    
    # if fill is currentColor or not set, wrap with fill
    if 'fill="currentColor"' in raw_svg or 'fill=' not in inner_content:
        inner_content = f'<g fill="{color}">{inner_content}</g>'
    
    square_svg = f'''<svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <filter id="glow-{slug}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="25" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Modern Dark Squircle Canvas (App Icon Look) -->
  <rect x="20" y="20" width="560" height="560" rx="130" fill="url(#bg-{slug})" stroke="#334155" stroke-width="3" />

  <!-- Soft Ambient Glow matching Brand Color -->
  <circle cx="300" cy="300" r="160" fill="{color}" opacity="0.14" filter="url(#glow-{slug})" />

  <!-- Centered Scaled Official Vector Emblem -->
  <svg x="140" y="140" width="320" height="320" viewBox="{vb}" style="overflow:visible">
    {inner_content}
  </svg>
</svg>'''
    
    (out_dir / f'{slug}.svg').write_text(square_svg, encoding='utf-8')
    count += 1

print(f"Successfully generated {count} square SVGs in {out_dir}")
