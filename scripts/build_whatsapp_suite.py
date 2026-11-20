import os
import shutil
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def build_whatsapp_suite():
    desktop_dir = r"C:\Users\Dell\Desktop\WhatsApp_Business_AIDigiTools"
    os.makedirs(desktop_dir, exist_ok=True)
    catalogue_dir = os.path.join(desktop_dir, "Catalogue_Products")
    os.makedirs(catalogue_dir, exist_ok=True)

    print("Target directory:", desktop_dir)

    # 1. Copy Profile Picture DP (800x800)
    dp_src = os.path.join("assets", "images", "social_dp_aidigitools.png")
    dp_dst = os.path.join(desktop_dir, "01_WhatsApp_Profile_Picture.png")
    if os.path.exists(dp_src):
        shutil.copyfile(dp_src, dp_dst)
        print("Copied DP to:", dp_dst)

    # 2. Design WhatsApp Business Cover Banner (1024x576)
    # Matching Reference Screenshot 1
    w, h = 1024, 576
    banner = Image.new("RGBA", (w, h), (10, 15, 29, 255))
    draw = ImageDraw.Draw(banner)

    # Cosmic gradient & subtle glow
    for y in range(h):
        r = int(11 + (y / h) * 12)
        g = int(15 + (y / h) * 15)
        b = int(29 + (y / h) * 45)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Gradient highlight glow top-left
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse([(-100, -100), (500, 400)], fill=(0, 229, 163, 35))
    glow_draw.ellipse([(600, -150), (1150, 400)], fill=(99, 102, 241, 45))
    banner = Image.alpha_composite(banner, glow)
    draw = ImageDraw.Draw(banner)

    # Fonts setup
    font_bold = None
    font_sub = None
    font_badge = None
    font_small = None
    try:
        font_tag = ImageFont.truetype("arialbd.ttf", 22)
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 24)
        font_badge = ImageFont.truetype("arialbd.ttf", 18)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        font_tag = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_badge = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Brand tag
    draw.text((60, 45), "PAKISTAN'S #1 AI SUBSCRIPTION STORE", fill=(0, 229, 163, 255), font=font_tag)

    # Main Headline
    draw.text((60, 85), "Official & Private AI Subscriptions", fill=(255, 255, 255, 255), font=font_title)

    # Subtitle with tool names
    draw.text((60, 150), "ChatGPT Plus  •  Claude Pro  •  Midjourney  •  Canva Pro  •  Cursor  •  Adobe", fill=(203, 213, 225, 255), font=font_sub)

    # Feature badges
    # Badge 1: 15-Minute Instant Activation
    b1_x, b1_y, b1_w, b1_h = 60, 205, 300, 42
    draw.rounded_rectangle([b1_x, b1_y, b1_x + b1_w, b1_y + b1_h], radius=21, fill=(15, 23, 42, 220), outline=(0, 229, 163, 255), width=2)
    draw.text((b1_x + 22, b1_y + 11), "⚡ Instant Activation (15 Mins)", fill=(0, 229, 163, 255), font=font_badge)

    # Badge 2: 100% Replacement Warranty
    b2_x = b1_x + b1_w + 20
    b2_w = 280
    draw.rounded_rectangle([b2_x, b1_y, b2_x + b2_w, b1_y + b1_h], radius=21, fill=(15, 23, 42, 220), outline=(99, 102, 241, 255), width=2)
    draw.text((b2_x + 22, b1_y + 11), "🛡️ 100% 30-Day Warranty", fill=(165, 180, 252, 255), font=font_badge)

    # Badge 3: Domestic Rails
    b3_x = b2_x + b2_w + 20
    b3_w = 280
    draw.rounded_rectangle([b3_x, b1_y, b3_x + b3_w, b1_y + b1_h], radius=21, fill=(15, 23, 42, 220), outline=(234, 179, 8, 255), width=2)
    draw.text((b3_x + 18, b1_y + 11), "💳 EasyPaisa • JazzCash • SadaPay", fill=(253, 224, 71, 255), font=font_badge)

    # Tool Icons Row / Grid in bottom-right / bottom
    icons_to_embed = [
        ("chatgpt-plus.png", "ChatGPT Plus"),
        ("claude-pro.png", "Claude Pro"),
        ("canva-pro.png", "Canva Pro"),
        ("midjourney.png", "Midjourney"),
        ("cursor-pro.png", "Cursor Pro"),
        ("adobe-creative-cloud.png", "Adobe Cloud"),
        ("capcut-pro.png", "CapCut Pro"),
    ]

    card_y = 420
    card_w, card_h = 120, 120
    spacing = 16
    start_x = 60

    for idx, (img_name, label) in enumerate(icons_to_embed):
        cx = start_x + idx * (card_w + spacing)
        if cx + card_w > w:
            break
        # Card background
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(15, 23, 42, 230), outline=(51, 65, 85, 255), width=1)
        # Embed icon
        icon_path = os.path.join("assets", "images", img_name)
        if os.path.exists(icon_path):
            try:
                icon_img = Image.open(icon_path).convert("RGBA")
                icon_img = icon_img.resize((card_w - 20, card_h - 20), Image.Resampling.LANCZOS)
                banner.paste(icon_img, (cx + 10, card_y + 10), icon_img)
            except Exception as e:
                print("Failed embedding", img_name, e)

    banner_dst = os.path.join(desktop_dir, "02_WhatsApp_Cover_Banner.png")
    banner.convert("RGB").save(banner_dst, "PNG", quality=95)
    print("Created Cover Banner:", banner_dst)

    # 3. Parse merchant_feed.xml to get top catalog items
    tree = ET.parse("merchant_feed.xml")
    root = tree.getroot()
    ns = {"g": "http://base.google.com/ns/1.0"}

    catalog_data = []
    for item in root.findall(".//item"):
        pid = item.find("g:id", ns).text
        title = item.find("g:title", ns).text
        desc = item.find("g:description", ns).text
        price = item.find("g:price", ns).text
        link = item.find("g:link", ns).text
        img_link = item.find("g:image_link", ns).text
        brand = item.find("g:brand", ns).text

        # Local image name
        slug = pid.replace("aidigitools-", "")
        img_local = os.path.join("assets", "images", f"{slug}.png")

        catalog_data.append({
            "id": pid,
            "slug": slug,
            "title": title,
            "desc": desc,
            "price": price,
            "link": link,
            "img_local": img_local,
            "brand": brand
        })

    # Pick top 15 bestselling products for WhatsApp Catalogue
    top_slugs = [
        "chatgpt-plus",
        "claude-pro",
        "canva-pro",
        "midjourney",
        "cursor-pro",
        "capcut-pro",
        "adobe-creative-cloud",
        "runway-gen3",
        "elevenlabs-creator",
        "perplexity-pro",
        "github-copilot",
        "deepseek-pro",
        "notion-business",
        "kling-ai",
        "envato-elements"
    ]

    selected_products = []
    rank = 1
    for slug in top_slugs:
        match = next((p for p in catalog_data if p["slug"] == slug), None)
        if match:
            # Copy image to Catalogue_Products folder
            dest_img_name = f"{rank:02d}_{slug.replace('-', '_')}.png"
            dest_img_path = os.path.join(catalogue_dir, dest_img_name)
            if os.path.exists(match["img_local"]):
                shutil.copyfile(match["img_local"], dest_img_path)
            selected_products.append({
                "rank": rank,
                "title": match["title"],
                "price": match["price"],
                "desc": match["desc"],
                "link": match["link"],
                "img_file": dest_img_name
            })
            rank += 1

    # 4. Generate WhatsApp Profile & Catalogue Copy-Paste Text File
    text_dst = os.path.join(desktop_dir, "03_WhatsApp_Setup_Details.txt")
    with open(text_dst, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("   AIDIGITOOLS - WHATSAPP BUSINESS SETUP & CATALOGUE GUIDE\n")
        f.write("=" * 70 + "\n\n")

        f.write("📌 STEP 1: WHATSAPP BUSINESS PROFILE SETTINGS\n")
        f.write("-" * 50 + "\n")
        f.write("• Profile Picture (DP): Use file '01_WhatsApp_Profile_Picture.png'\n")
        f.write("• Cover Photo: Use file '02_WhatsApp_Cover_Banner.png'\n")
        f.write("• Business Name: AIDigiTools\n")
        f.write("• Category: Computers & Technology (ya Shopping & Retail / Software)\n")
        f.write("• Description:\n")
        f.write("--------------------------------------------------\n")
        desc_text = (
            "Pakistan's #1 Trusted AI Software & Subscription Store 💎\n\n"
            "Instant activation for ChatGPT Plus, Claude Pro, Midjourney, Canva Pro, "
            "Cursor, Runway, Adobe All Apps & 49+ AI tools.\n\n"
            "⚡ 15-Minute Instant Digital Delivery\n"
            "🛡️ 100% 30-Day Replacement Warranty\n"
            "💳 Payments: EasyPaisa | JazzCash | SadaPay | NayaPay | Bank IBFT | Wise | Crypto USDT\n\n"
            "🌐 Official Website: https://aidigitools.tech/"
        )
        f.write(desc_text + "\n")
        f.write("--------------------------------------------------\n")
        f.write("• Business Address: Online Digital Desk, Islamabad, Pakistan, 44000\n")
        f.write("• Business Hours: Open 24 hours\n")
        f.write("• Email: abeerafarooq731@gmail.com (ya support@aidigitools.tech)\n")
        f.write("• Website: https://aidigitools.tech/\n\n")

        f.write("=" * 70 + "\n")
        f.write("🛍️ STEP 2: CATALOGUE PRODUCTS (Top 15 Tools to Add)\n")
        f.write("Folder: 'Catalogue_Products' mein har tool ki image save hai.\n")
        f.write("=" * 70 + "\n\n")

        for p in selected_products:
            f.write(f"[{p['rank']:02d}] {p['title']}\n")
            f.write(f"• Image File: Catalogue_Products/{p['img_file']}\n")
            f.write(f"• Item Name: {p['title'].split(' — ')[0]}\n")
            f.write(f"• Price: {p['price']}\n")
            f.write(f"• Description: {p['desc']}\n")
            f.write(f"• Link: {p['link']}\n")
            f.write("-" * 50 + "\n\n")

    print("Setup guide created at:", text_dst)
    print("WhatsApp Business Suite built successfully!")

if __name__ == "__main__":
    build_whatsapp_suite()
