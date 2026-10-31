import os
import glob
import subprocess
import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

def get_git_lastmod(file_path):
    try:
        res = subprocess.run(
            ['git', 'log', '-1', '--format=%as', '--', file_path],
            capture_output=True,
            text=True,
            check=True
        )
        date_str = res.stdout.strip()
        if re_date := date_str:
            return date_str
    except Exception:
        pass
    # Fallback to file mtime
    mtime = os.path.getmtime(file_path)
    return datetime.date.fromtimestamp(mtime).isoformat()

def build_official_sitemap():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)

    html_files = sorted(glob.glob('*.html') + glob.glob('*/*.html'))
    html_files = [f.replace('\\\\', '/').replace('\\', '/') for f in html_files]

    # Exclude 404.html and tests/temp
    indexable_files = [
        f for f in html_files
        if f != '404.html' and not f.startswith('temp') and not f.startswith('test')
    ]

    print(f"Total indexable files for sitemap: {len(indexable_files)}")

    urls = []
    domain = "https://aidigitools.tech"

    for path in indexable_files:
        lastmod = get_git_lastmod(path)
        if path == "index.html":
            loc = f"{domain}/"
            priority = "1.0"
            changefreq = "daily"
        elif path == "deals.html":
            loc = f"{domain}/deals.html"
            priority = "0.9"
            changefreq = "daily"
        elif path.startswith("categories/"):
            loc = f"{domain}/{path}"
            priority = "0.9"
            changefreq = "weekly"
        elif path.startswith("tools/"):
            loc = f"{domain}/{path}"
            priority = "0.9"
            changefreq = "weekly"
        elif path.startswith("compare/") or path.startswith("best/") or path.startswith("guides/"):
            loc = f"{domain}/{path}"
            priority = "0.8"
            changefreq = "weekly"
        else: # about, contact, policies, shipping-policy, affiliate-disclosure
            loc = f"{domain}/{path}"
            priority = "0.7"
            changefreq = "monthly"

        urls.append({
            "loc": loc,
            "lastmod": lastmod,
            "changefreq": changefreq,
            "priority": priority
        })

    # Sort URLs: root first, then categories, tools, comparisons, and policies
    def sort_key(u):
        loc = u["loc"]
        if loc == f"{domain}/": return (0, loc)
        if "/deals.html" in loc: return (1, loc)
        if "/categories/" in loc: return (2, loc)
        if "/tools/" in loc: return (3, loc)
        if "/compare/" in loc or "/best/" in loc or "/guides/" in loc: return (4, loc)
        return (5, loc)

    urls.sort(key=sort_key)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for u in urls:
        lines.append('  <url>')
        lines.append(f'    <loc>{u["loc"]}</loc>')
        lines.append(f'    <lastmod>{u["lastmod"]}</lastmod>')
        lines.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
        lines.append(f'    <priority>{u["priority"]}</priority>')
        lines.append('  </url>')

    lines.append('</urlset>')
    lines.append('')

    xml_content = "\n".join(lines)

    # Validate XML
    ET.fromstring(xml_content)

    with open('sitemap.xml', 'w', encoding='utf-8', newline='\n') as f:
        f.write(xml_content)

    print(f"SUCCESS: Generated official sitemap.xml with {len(urls)} URLs and genuine lastmod timestamps!")
    return len(urls)

if __name__ == '__main__':
    build_official_sitemap()

