import os
import re
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
tools_json_path = ROOT / "data" / "products_master.json"

if tools_json_path.exists():
    tools_data = json.load(open(tools_json_path, "r", encoding="utf-8"))
else:
    tools_data = []

# 7 Policy-Held products (Inquiry Only, out_of_stock for compliance)
HELD_SLUGS = {
    "turnitin-student",
    "linkedin-premium",
    "netflix-premium",
    "spotify-premium",
    "coursera-plus",
    "claude-artifacts",
    "deepseek-pro"
}

items_data = []
for tool in tools_data:
    slug = tool.get("slug")
    name = tool.get("display_name") or tool.get("name") or tool.get("official_product_name")
    brand = tool.get("brand", "AIDigiTools")
    price = str(tool.get("aidigitools_price_pkr", "1200"))
    avail = "out_of_stock" if slug in HELD_SLUGS else "in_stock"
    
    # Exact title format from user reference: {Tool Name} Plan in Pakistan
    title = f"{name} Plan in Pakistan"
    
    # Clean concise description matching WhatsApp catalogue standards
    desc = f"{name} official software plan in Pakistan with 15-minute WhatsApp activation and 30-day warranty."
    
    # Escape xml entities
    name_clean = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    title_clean = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    brand_clean = brand.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    desc_clean = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    items_data.append({
        "slug": slug,
        "name": name_clean,
        "title": title_clean,
        "brand": brand_clean,
        "desc": desc_clean,
        "price": price,
        "availability": avail
    })

print(f"Loaded {len(items_data)} tools for merchant feed.")

feed_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">',
    '  <channel>',
    '    <title>AIDigiTools — Verified AI Software &amp; Digital Subscriptions</title>',
    '    <link>https://aidigitools.tech</link>',
    '    <description>Verified AI software and digital subscriptions marketplace serving Pakistan and worldwide with 30-day warranty, 15-minute digital delivery, and domestic &amp; international rails.</description>',
    ''
]

for it in items_data:
    feed_lines.append("    <item>")
    feed_lines.append(f"      <g:id>aidigitools-{it['slug']}</g:id>")
    feed_lines.append(f"      <g:title>{it['title']}</g:title>")
    feed_lines.append(f"      <g:description>{it['desc']}</g:description>")
    feed_lines.append(f"      <g:link>https://aidigitools.tech/tools/{it['slug']}.html</g:link>")
    feed_lines.append(f"      <g:image_link>https://aidigitools.tech/assets/images/square/{it['slug']}.png</g:image_link>")
    feed_lines.append(f"      <g:price>{it['price']} PKR</g:price>")
    feed_lines.append(f"      <g:availability>{it['availability']}</g:availability>")
    feed_lines.append(f"      <g:brand>{it['brand']}</g:brand>")
    feed_lines.append(f"      <g:condition>new</g:condition>")
    feed_lines.append(f"      <g:google_product_category>Software &gt; Computer Software</g:google_product_category>")
    feed_lines.append(f"      <g:product_type>Software &gt; Artificial Intelligence</g:product_type>")
    feed_lines.append(f"      <g:identifier_exists>no</g:identifier_exists>")
    for country, s_name in [("PK", "Digital Instant Delivery via WhatsApp and Email"),
                            ("US", "Worldwide Digital Delivery via WhatsApp and Email"),
                            ("GB", "Worldwide Digital Delivery via WhatsApp and Email"),
                            ("AE", "Worldwide Digital Delivery via WhatsApp and Email"),
                            ("CA", "Worldwide Digital Delivery via WhatsApp and Email")]:
        feed_lines.append("      <g:shipping>")
        feed_lines.append(f"        <g:country>{country}</g:country>")
        feed_lines.append(f"        <g:service>{s_name}</g:service>")
        feed_lines.append(f"        <g:price>0 PKR</g:price>")
        feed_lines.append("      </g:shipping>")
    feed_lines.append("    </item>")
    feed_lines.append("")

feed_lines.append("  </channel>")
feed_lines.append("</rss>")
feed_lines.append("")

feed_content = "\n".join(feed_lines)

# Write to merchant_feed.xml
feed_path = ROOT / "merchant_feed.xml"
with open(feed_path, "w", encoding="utf-8") as f:
    f.write(feed_content)

# Write to meta-product-feed.xml
meta_feed_path = ROOT / "meta-product-feed.xml"
with open(meta_feed_path, "w", encoding="utf-8") as f:
    f.write(feed_content)

# Validate XML
ET.fromstring(feed_content)
print(f"[SUCCESS] merchant_feed.xml and meta-product-feed.xml updated with {len(items_data)} products and validated syntax!")
