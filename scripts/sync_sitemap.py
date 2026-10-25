import os
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent

html_files = sorted(list(ROOT.glob("*.html")) + list(ROOT.glob("*/*.html")))
# Filter out temporary or unwanted html
valid_html = [f for f in html_files if not f.name.startswith("temp_") and not f.name.startswith("test_")]

print(f"Total HTML files found: {len(valid_html)}")

urls = []
for hf in valid_html:
    rel = hf.relative_to(ROOT).as_posix()
    if rel == "index.html":
        loc = "https://aidigitools.tech/"
        prio = "1.0"
        freq = "daily"
    elif rel.startswith("tools/"):
        loc = f"https://aidigitools.tech/{rel}"
        prio = "0.9"
        freq = "weekly"
    elif rel.startswith("deals.html"):
        loc = f"https://aidigitools.tech/{rel}"
        prio = "0.9"
        freq = "daily"
    elif rel.startswith("categories/"):
        loc = f"https://aidigitools.tech/{rel}"
        prio = "0.8"
        freq = "weekly"
    elif rel.startswith("compare/") or rel.startswith("best/") or rel.startswith("guides/"):
        loc = f"https://aidigitools.tech/{rel}"
        prio = "0.8"
        freq = "weekly"
    else:
        loc = f"https://aidigitools.tech/{rel}"
        prio = "0.7"
        freq = "monthly"
        
    urls.append((loc, prio, freq))

sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, prio, freq in urls:
    sitemap_lines.append("  <url>")
    sitemap_lines.append(f"    <loc>{loc}</loc>")
    sitemap_lines.append("    <lastmod>2026-10-25</lastmod>")
    sitemap_lines.append(f"    <changefreq>{freq}</changefreq>")
    sitemap_lines.append(f"    <priority>{prio}</priority>")
    sitemap_lines.append("  </url>")
sitemap_lines.append("</urlset>")
sitemap_lines.append("")

sitemap_path = ROOT / "sitemap.xml"
sitemap_content = "\n".join(sitemap_lines)
with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

# Validate XML syntax
tree = ET.fromstring(sitemap_content)
print(f"[SUCCESS] sitemap.xml generated with {len(urls)} URLs and valid syntax!")
