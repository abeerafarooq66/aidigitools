import datetime
from pathlib import Path

def generate_sitemap(root_dir: Path | str = "."):
    root = Path(root_dir).resolve()
    domain = "https://aidigitools.tech"
    today = datetime.date.today().isoformat()

    urls = []
    # Root index
    if (root / "index.html").exists():
        urls.append(f"""  <url>
    <loc>{domain}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""")

    # Policies
    if (root / "policies.html").exists():
        urls.append(f"""  <url>
    <loc>{domain}/policies.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>""")

    # Tools
    tools_dir = root / "tools"
    if tools_dir.exists():
        for tf in sorted(tools_dir.glob("*.html")):
            urls.append(f"""  <url>
    <loc>{domain}/tools/{tf.name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    # Guides
    guides_dir = root / "guides"
    if guides_dir.exists():
        for gf in sorted(guides_dir.glob("*.html")):
            urls.append(f"""  <url>
    <loc>{domain}/guides/{gf.name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"\n".join(urls)}
</urlset>
"""
    sitemap_path = root / "sitemap.xml"
    sitemap_path.write_text(sitemap_content, encoding="utf-8")
    print(f"[Sitemap] Generated sitemap.xml with {len(urls)} URLs at {sitemap_path}")
    return len(urls)

if __name__ == "__main__":
    generate_sitemap()
