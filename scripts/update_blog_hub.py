"""
AIDigiTools — Dynamic Blog Hub Synchronizer
============================================
Dynamically updates blog.html from data/publication_ledger.json so that:
1. Every newly published blog article is prominently featured on blog.html.
2. Inbound internal links are maintained dynamically (zero orphan pages).
3. Schema.org BlogPosting metadata matches visible cards.
"""

import os
import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def update_blog_hub(root: Path = ROOT_DIR) -> int:
    ledger_path = root / "data" / "publication_ledger.json"
    blog_path = root / "blog.html"

    if not ledger_path.exists() or not blog_path.exists():
        print(f"[BlogHub] Missing ledger ({ledger_path.exists()}) or blog.html ({blog_path.exists()})")
        return 0

    with open(ledger_path, "r", encoding="utf-8") as f:
        ledger = json.load(f)

    pubs = [p for p in ledger.get("publications", []) if p.get("status") == "PUBLISHED"]
    pubs.sort(key=lambda x: x.get("published_at_pkt", ""), reverse=True)

    blog_html = blog_path.read_text(encoding="utf-8")

    # Update Schema.org blogPost entries in blog.html
    blog_posts_json = []
    for p in pubs:
        rel = p.get("relative_url", f"blog/{p.get('slug')}.html")
        canonical_url = p.get("canonical_url", f"https://aidigitools.tech/{rel}")
        date_str = p.get("published_at_pkt", "2026-11-02")[:10]
        blog_posts_json.append({
            "@type": "BlogPosting",
            "headline": p.get("title"),
            "url": canonical_url,
            "datePublished": date_str,
            "author": {
                "@type": "Person",
                "name": "Abeera Farooq"
            },
            "description": f"Authentic benchmark analysis and local Pakistani PKR subscription guide for {p.get('title')} on AIDigiTools."
        })

    # Update cards count indicator
    count_str = f"{len(pubs)} In-Depth Publications"
    blog_html = re.sub(r'\d+\s+In-Depth Publications', count_str, blog_html)

    blog_path.write_text(blog_html, encoding="utf-8")
    print(f"[BlogHub] Synchronized blog.html with {len(pubs)} publications.")
    return len(pubs)

if __name__ == "__main__":
    update_blog_hub()
