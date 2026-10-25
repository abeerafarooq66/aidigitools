import datetime
from pathlib import Path

def generate_sitemap(root_dir: Path | str = "."):
    root = Path(root_dir).resolve()
    domain = "https://aidigitools.tech"
    today = datetime.date.today().isoformat()

    urls = []
    # Primary Pages
    primary_pages = [
        ("index.html", "", "daily", "1.0"),
        ("about.html", "about.html", "monthly", "0.8"),
        ("contact.html", "contact.html", "monthly", "0.8"),
        ("shipping-policy.html", "shipping-policy.html", "monthly", "0.7"),
        ("policies.html", "policies.html", "monthly", "0.6"),
    ]

    for filename, slug, freq, priority in primary_pages:
        if (root / filename).exists():
            loc = f"{domain}/{slug}" if slug else f"{domain}/"
            urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    # Tools
    tools_dir = root / "tools"
    if tools_dir.exists():
        for tf in sorted(tools_dir.glob("*.html")):
            urls.append(f"""  <url>
    <loc>{domain}/tools/{tf.name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>""")

    # Guides
    guides_dir = root / "guides"
    if guides_dir.exists():
        for gf in sorted(guides_dir.glob("*.html")):
            urls.append(f"""  <url>
    <loc>{domain}/guides/{gf.name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
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
