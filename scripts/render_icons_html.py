import json
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
svg_dir = ROOT / 'assets/images/square_svg'
out_html = ROOT / 'scratch/render_icons.html'
out_html.parent.mkdir(parents=True, exist_ok=True)

svg_files = sorted(list(svg_dir.glob('*.svg')))

items = []
for f in svg_files:
    slug = f.stem
    svg_txt = f.read_text(encoding='utf-8')
    items.append({
        'slug': slug,
        'svg': svg_txt
    })

html_content = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Render Square Icons</title>
</head>
<body style="background:#111; color:#fff;">
  <h1>Rendering {len(items)} Icons...</h1>
  <div id="status">Starting...</div>
  <canvas id="c" width="600" height="600" style="display:none;"></canvas>

  <script>
    const items = {json.dumps(items)};
    window.__renderedIcons = {{}};
    window.__done = false;

    async function renderAll() {{
      const canvas = document.getElementById('c');
      const ctx = canvas.getContext('2d');
      const status = document.getElementById('status');

      for (let i = 0; i < items.length; i++) {{
        const item = items[i];
        status.innerText = `Rendering ${{i + 1}}/${{items.length}}: ${{item.slug}}`;
        
        ctx.clearRect(0, 0, 600, 600);
        
        // Load SVG via data URL
        const blob = new Blob([item.svg], {{ type: 'image/svg+xml;charset=utf-8' }});
        const url = URL.createObjectURL(blob);
        
        await new Promise((resolve, reject) => {{
          const img = new Image();
          img.onload = () => {{
            ctx.drawImage(img, 0, 0, 600, 600);
            window.__renderedIcons[item.slug] = canvas.toDataURL('image/png');
            URL.revokeObjectURL(url);
            resolve();
          }};
          img.onerror = (e) => {{
            console.error('Failed to load SVG for', item.slug, e);
            URL.revokeObjectURL(url);
            resolve();
          }};
          img.src = url;
        }});
      }}
      
      window.__done = true;
      status.innerText = `All ${{items.length}} icons rendered successfully!`;
    }}

    renderAll();
  </script>
</body>
</html>'''

out_html.write_text(html_content, encoding='utf-8')
print(f"Created {out_html} with {len(items)} items.")
