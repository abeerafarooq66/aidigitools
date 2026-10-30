"""
Updates favicon links and Organization schema logo URLs across all HTML files
to strictly adhere to Google Search Central official specifications:
1. "Define a favicon to show in search results"
   - Multiple of 48px square PNGs (48x48, 96x96, 192x192) and standard root favicon.ico
   - apple-touch-icon.png for mobile devices
2. "Logo structured data"
   - PNG format instead of SVG for Google Images and Knowledge Graph ingestion.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FAVICON_BLOCK = """  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/favicon.svg" sizes="any" type="image/svg+xml">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
  <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">"""

def update_file(path: Path):
    content = path.read_text(encoding="utf-8")
    original = content
    
    # 1. Replace old single SVG favicon link with full Google-compliant block
    old_fav_pattern = r'[ \t]*<link\s+rel=["\']icon["\']\s+type=["\']image/svg\+xml["\']\s+href=["\'][^"\']*favicon\.svg["\']\s*>'
    if re.search(old_fav_pattern, content):
        content = re.sub(old_fav_pattern, FAVICON_BLOCK, content, count=1)
    
    # 2. Replace SVG logo with PNG logo in Schema.org
    content = content.replace(
        "https://aidigitools.tech/assets/images/aidigitools-logo.svg",
        "https://aidigitools.tech/assets/images/aidigitools-logo.png"
    )
    
    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    html_files = [
        p for p in ROOT.glob("**/*.html")
        if not any(part.startswith((".", "tests", "scratch", "node_modules", "venv")) for part in p.parts)
    ]
    
    updated_count = 0
    for f in html_files:
        if update_file(f):
            updated_count += 1
            print(f"[UPDATED] {f.relative_to(ROOT)}")
            
    print(f"\nDone. Updated {updated_count} of {len(html_files)} HTML files.")

if __name__ == "__main__":
    main()
