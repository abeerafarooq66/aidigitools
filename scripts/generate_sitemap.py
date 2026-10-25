import datetime
from pathlib import Path

def generate_sitemap(root_dir: Path | str = "."):
    root = Path(root_dir).resolve()
    domain = "https://aidigitools.tech"
    today = datetime.date.today().isoformat()

    urls = []
    
    # 1. Primary Root Pages
    root_pages = [
        ("index.html", "", "daily", "1.0"),
        ("deals.html", "deals.html", "daily", "0.9"),
        ("about.html", "about.html", "monthly", "0.8"),
        ("contact.html", "contact.html", "monthly", "0.8"),
        ("shipping-policy.html", "shipping-policy.html", "monthly", "0.7"),
        ("policies.html", "policies.html", "monthly", "0.6"),
        ("affiliate-disclosure.html", "affiliate-disclosure.html", "monthly", "0.6"),
    ]

    for filename, slug, freq, priority in root_pages:
        if (root / filename).exists():
            loc = f"{domain}/{slug}" if slug else f"{domain}/"
            urls.append(f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    # 2. Directory Mappings
    dir_configs = [
        ("tools", "weekly", "0.9"),
        ("categories", "weekly", "0.9"),
        ("compare", "weekly", "0.8"),
        ("best", "weekly", "0.8"),
        ("guides", "weekly", "0.8"),
    ]

    for dir_name, freq, priority in dir_configs:
        d = root / dir_name
        if d.exists():
            for f in sorted(d.glob("*.html")):
                urls.append(f"""  <url>
    <loc>{domain}/{dir_name}/{f.name}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
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
