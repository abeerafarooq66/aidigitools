import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
tools_dir = ROOT / "tools"

items_data = []
for tool_file in sorted(tools_dir.glob("*.html")):
    content = tool_file.read_text(encoding="utf-8")
    slug = tool_file.stem
    
    # Extract name, brand, price, description from JSON-LD
    price_match = re.search(r'"price":\s*"(\d+)"', content)
    price = price_match.group(1) if price_match else "1200"
    
    brand_match = re.search(r'"brand":\s*{\s*"@type":\s*"Brand",\s*"name":\s*"([^"]+)"', content)
    brand = brand_match.group(1) if brand_match else "AIDigiTools"
    
    name_match = re.search(r'"name":\s*"([^"]+)"', content)
    name = name_match.group(1) if name_match else slug.replace("-", " ").title()
    name = name.replace(" Subscription (Pakistan & Worldwide)", "")
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    desc = desc_match.group(1) if desc_match else f"Buy {name} in Pakistan and worldwide with instant 15-minute delivery and 30-day warranty."
    
    # Escape xml
    name_clean = name.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    brand_clean = brand.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    desc_clean = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    items_data.append({
        "slug": slug,
        "name": name_clean,
        "brand": brand_clean,
        "desc": desc_clean,
        "price": price
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
    feed_lines.append(f"      <g:title>{it['brand']} {it['name']} Subscription — 1 Month Access</g:title>")
    feed_lines.append(f"      <g:description>{it['desc']}</g:description>")
    feed_lines.append(f"      <g:link>https://aidigitools.tech/tools/{it['slug']}.html</g:link>")
    feed_lines.append(f"      <g:image_link>https://aidigitools.tech/assets/images/{it['slug']}.png</g:image_link>")
    feed_lines.append(f"      <g:price>{it['price']} PKR</g:price>")
    feed_lines.append(f"      <g:availability>in_stock</g:availability>")
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
feed_path = ROOT / "merchant_feed.xml"
with open(feed_path, "w", encoding="utf-8") as f:
    f.write(feed_content)

# Validate XML
ET.fromstring(feed_content)
print(f"[SUCCESS] merchant_feed.xml updated with {len(items_data)} products and validated syntax!")
