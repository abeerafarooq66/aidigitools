"""
Generates official, Google Search compliant Favicon and Logo assets for AIDigiTools.
Strictly follows Google Search Central documentation:
"Define a favicon to show in search results"
https://developers.google.com/search/docs/appearance/favicon-in-search

Requirements satisfied:
1. Formats: ICO and PNG (SVG is rejected by Google Search result snippets).
2. Dimensions: Multiples of 48px square (48x48, 96x96, 144x144, 192x192).
3. Root locations: /favicon.ico, /favicon-48x48.png, /favicon-96x96.png, /favicon-192x192.png, /apple-touch-icon.png.
4. Schema Logo: /assets/images/aidigitools-logo.png (512x512px).
"""

import os
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SVG_PATH = ROOT / "favicon.svg"
CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

def build_ico_from_pngs(png_dict: dict, out_path: Path):
    """Packages multiple PNG byte buffers into a valid standard ICO file."""
    num_images = len(png_dict)
    header = struct.pack('<HHH', 0, 1, num_images)
    entries = []
    data_bytes = bytearray()
    offset = 6 + (16 * num_images)
    
    for size, pdata in png_dict.items():
        w = size if size < 256 else 0
        h = size if size < 256 else 0
        size_bytes = len(pdata)
        entry = struct.pack('<BBBBHHII', w, h, 0, 0, 1, 32, size_bytes, offset + len(data_bytes))
        entries.append(entry)
        data_bytes.extend(pdata)
        
    with open(out_path, 'wb') as f:
        f.write(header)
        for e in entries:
            f.write(e)
        f.write(data_bytes)
    print(f"[ICO] Created {out_path.name} ({len(out_path.read_bytes())} bytes, sizes: {list(png_dict.keys())})")

def render_svg_to_png(svg_content: str, size: int, out_path: Path):
    """Renders SVG to transparent square PNG using headless Chrome."""
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {size}px; height: {size}px; background: transparent; overflow: hidden; }}
  svg {{ width: 100%; height: 100%; display: block; }}
</style>
</head>
<body>
{svg_content}
</body>
</html>"""
    
    temp_html = ROOT / f"temp_render_{size}.html"
    temp_html.write_text(html, encoding="utf-8")
    
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--screenshot={out_path.resolve()}",
        f"--window-size={size},{size}",
        "--default-background-color=00000000",
        str(temp_html.resolve())
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"[PNG] Rendered {out_path.name} ({size}x{size}px, {out_path.stat().st_size} bytes)")
    finally:
        if temp_html.exists():
            temp_html.unlink()

def main():
    if not SVG_PATH.exists():
        raise FileNotFoundError(f"Missing {SVG_PATH}")
    
    svg_content = SVG_PATH.read_text(encoding="utf-8")
    
    sizes = {
        16: ROOT / "temp_16.png",
        32: ROOT / "temp_32.png",
        48: ROOT / "favicon-48x48.png",
        96: ROOT / "favicon-96x96.png",
        144: ROOT / "favicon-144x144.png",
        180: ROOT / "apple-touch-icon.png",
        192: ROOT / "favicon-192x192.png",
        512: ROOT / "assets" / "images" / "aidigitools-logo.png"
    }
    
    # 1. Render all sizes
    for sz, target_path in sizes.items():
        render_svg_to_png(svg_content, sz, target_path)
    
    # Also create root favicon-512x512.png
    (ROOT / "favicon-512x512.png").write_bytes(sizes[512].read_bytes())
    print(f"[PNG] Created favicon-512x512.png")
    
    # 2. Build multi-size favicon.ico containing 16x16, 32x32, 48x48
    ico_dict = {
        16: sizes[16].read_bytes(),
        32: sizes[32].read_bytes(),
        48: sizes[48].read_bytes()
    }
    build_ico_from_pngs(ico_dict, ROOT / "favicon.ico")
    
    # 3. Clean up temporary files
    sizes[16].unlink()
    sizes[32].unlink()
    
    print("\n✅ All official Google Favicon & Logo assets generated successfully!")

if __name__ == "__main__":
    main()
