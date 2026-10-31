import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

import json
import csv
import glob
import re
import xml.etree.ElementTree as ET
from scripts.master_product_dictionary import PRODUCT_MAP

def update_master_json_and_csv():
    print("--- 1. Updating products_master.json and products_master.csv ---")
    json_path = os.path.join(REPO_ROOT, "data", "products_master.json")
    csv_path = os.path.join(REPO_ROOT, "data", "products_master.csv")

    with open(json_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    for item in master:
        slug = item["slug"]
        if slug in PRODUCT_MAP:
            info = PRODUCT_MAP[slug]
            item["brand"] = info["brand"]
            item["official_product_name"] = info["official_product_name"]
            item["official_plan_name"] = info["official_plan_name"]
            item["display_name"] = info["card_title"]
            item["current_model"] = info["current_model"]
            item["product_name"] = info["card_title"]
            item["name"] = info["card_title"]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    print("Updated products_master.json successfully.")

    # Write CSV
    all_keys = list(master[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        for item in master:
            writer.writerow(item)
    print("Updated products_master.csv successfully.")

def update_merchant_feed():
    print("--- 2. Updating merchant_feed.xml ---")
    feed_path = os.path.join(REPO_ROOT, "merchant_feed.xml")
    with open(feed_path, "r", encoding="utf-8") as f:
        content = f.read()

    for slug, info in PRODUCT_MAP.items():
        # Title in feed: <g:id>slug</g:id> ... <g:title>...</g:title>
        pattern = rf'(<g:id>{slug}</g:id>[\s\S]*?<g:title>)[^<]+(</g:title>[\s\S]*?<g:description>)[^<]+(</g:description>)'
        clean_title = f"{info['official_product_name']} Subscription — Pakistan &amp; Worldwide"
        clean_desc = f"{info['desc']} Available with verified domestic payment rails (EasyPaisa, JazzCash, SadaPay) and 15-minute delivery."
        
        def repl(match):
            return f"{match.group(1)}{clean_title}{match.group(2)}{clean_desc}{match.group(3)}"
            
        content, _ = re.subn(pattern, repl, content, count=1)

    with open(feed_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated merchant_feed.xml successfully.")

def update_cart_js():
    print("--- 3. Updating assets/cart.js TOOLS_DATA ---")
    cart_path = os.path.join(REPO_ROOT, "assets", "cart.js")
    with open(cart_path, "r", encoding="utf-8") as f:
        content = f.read()

    for slug, info in PRODUCT_MAP.items():
        # Pattern to replace name and desc in TOOLS_DATA:
        # "slug": {\n    "slug": "...",\n    "name": "...", ...
        # Match "name": "...",\n    "brand": "...",\n    "vendor": "...", ... "desc": "...",
        pattern = rf'("{slug}":\s*\{{\s*"slug":\s*"{slug}",\s*"name":\s*")[^"]+("[\s\S]*?"desc":\s*")[^"]+(")'
        
        def repl(match):
            return f"{match.group(1)}{info['card_title']}{match.group(2)}{info['desc']}{match.group(3)}"
            
        new_content, count = re.subn(pattern, repl, content, count=1)
        if count > 0:
            content = new_content
        else:
            print(f"Warning: could not update TOOLS_DATA for {slug}")

    with open(cart_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated assets/cart.js successfully.")

def update_index_html():
    print("--- 4. Updating index.html (Dropdown and Cards) ---")
    index_path = os.path.join(REPO_ROOT, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 4A. Update dropdown options in #showcaseToolSelect
    for slug, info in PRODUCT_MAP.items():
        opt_pattern = rf'<option value="{slug}">[^<]+</option>'
        opt_replace = f'<option value="{slug}">{info["dropdown_label"]}</option>'
        content, count = re.subn(opt_pattern, opt_replace, content, count=1)
        if count == 0:
            print(f"Warning: option not found for {slug} in index.html")

    # 4B. Update Homepage Cards
    for slug, info in PRODUCT_MAP.items():
        # Match card header and title:
        # data-tool="slug" data-name="..." ...
        # <h3 class="tool-card-title">...</h3>
        # <span class="tool-card-vendor">...</span>
        # <p class="tool-card-desc">...</p>
        card_pattern = rf'(data-tool="{slug}"[^>]*data-name=")[^"]+("[\s\S]*?<h3 class="tool-card-title">)[^<]+(</h3>\s*<span class="tool-card-vendor">)[^<]+(</span>\s*<p class="tool-card-desc">)[^<]+(</p>)'
        
        def card_repl(match):
            return f"{match.group(1)}{info['card_title']}{match.group(2)}{info['card_title']}{match.group(3)}{info['brand']}{match.group(4)}{info['desc']}{match.group(5)}"
            
        new_content, count = re.subn(card_pattern, card_repl, content, count=1)
        if count > 0:
            content = new_content
        else:
            print(f"Warning: card pattern failed for {slug} in index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated index.html successfully.")

def update_all_tool_pages():
    print("--- 5. Updating all 49 tools/*.html pages ---")
    for slug, info in PRODUCT_MAP.items():
        tp_path = os.path.join(REPO_ROOT, "tools", f"{slug}.html")
        if not os.path.exists(tp_path):
            print(f"Error: {tp_path} does not exist!")
            continue

        with open(tp_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Title
        html = re.sub(r'<title>[^<]+</title>', f"<title>{info['seo_title']}</title>", html, count=1)
        # Meta description
        html = re.sub(r'<meta name="description" content="[^"]+">', f'<meta name="description" content="{info["meta_desc"]}">', html, count=1)
        # OG Title & Desc
        html = re.sub(r'<meta property="og:title" content="[^"]+">', f'<meta property="og:title" content="{info["seo_title"]}">', html, count=1)
        html = re.sub(r'<meta property="og:description" content="[^"]+">', f'<meta property="og:description" content="{info["meta_desc"]}">', html, count=1)
        # Twitter Title & Desc
        html = re.sub(r'<meta name="twitter:title" content="[^"]+">', f'<meta name="twitter:title" content="{info["seo_title"]}">', html, count=1)
        html = re.sub(r'<meta name="twitter:description" content="[^"]+">', f'<meta name="twitter:description" content="{info["meta_desc"]}">', html, count=1)
        # H1
        html = re.sub(r'<h1[^>]*>[^<]+</h1>', f"<h1>{info['tool_h1']}</h1>", html, count=1)
        # Quick Answer
        html = re.sub(r'(<p class="quick-answer">)[^<]+(</p>)', f"\\g<1>{info['quick_answer']}\\g<2>", html, count=1)
        # Breadcrumb visible text
        # <a href="...">Home</a> / ... / <span>Existing Name</span>
        html = re.sub(r'(class="breadcrumb-current"[^>]*>)[^<]+(</span>)', f"\\g<1>{info['card_title']}\\g<2>", html, count=1)

        # JSON-LD Product schema
        # "name": "...",
        # "description": "...",
        # "brand": { ... "name": "..." }
        schema_pattern = r'("@type":\s*"Product",\s*"name":\s*")[^"]+(")'
        html = re.sub(schema_pattern, f'\\g<1>{info["official_product_name"]}\\g<2>', html, count=1)

        with open(tp_path, "w", encoding="utf-8") as f:
            f.write(html)

    print("Updated all 49 tools/*.html pages successfully.")

if __name__ == "__main__":
    update_master_json_and_csv()
    update_merchant_feed()
    update_cart_js()
    update_index_html()
    update_all_tool_pages()
    print("--- ALL SURFACES SYNCHRONIZED ---")
