import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load all 36 tools data
import generate_30_tools as g30

# The 6 baseline tools + 30 new tools
baseline_6 = [
    {
        "slug": "chatgpt-plus",
        "name": "ChatGPT Plus",
        "brand": "OpenAI",
        "pkr_price": "2300",
        "usd_price": "8.00",
        "desc": "Full access to GPT-4o, Custom GPTs, Canvas, and advanced voice mode with zero downtime.",
        "category": "chat coding writing",
        "bullets": [
            "OpenAI GPT-4o & DALL-E 3 Imaging",
            "EasyPaisa, JazzCash, SadaPay & Wise/Crypto",
            "Instant 15-Minute Delivery SLA Worldwide",
            "30-Day Full Replacement Warranty"
        ]
    },
    {
        "slug": "claude-pro",
        "name": "Claude Pro",
        "brand": "Anthropic",
        "pkr_price": "2500",
        "usd_price": "9.00",
        "desc": "Access Claude 3.5 Sonnet with extended context, Artifacts canvas, and technical programming capabilities.",
        "category": "coding writing chat",
        "bullets": [
            "Anthropic Claude 3.5 Sonnet & Haiku",
            "Interactive Code & UI Artifacts Canvas",
            "EasyPaisa, JazzCash, SadaPay, Wise & Crypto",
            "30-Day Full Replacement Warranty"
        ]
    },
    {
        "slug": "canva-pro",
        "name": "Canva Pro",
        "brand": "Canva",
        "pkr_price": "600",
        "usd_price": "2.50",
        "desc": "Premium graphics workspace, 100M+ stock assets, Magic Studio generative AI, and team Brand Kits.",
        "category": "image design graphics",
        "bullets": [
            "100M+ Stock Photos, Vectors & Videos",
            "Magic Studio AI Background Remover",
            "1TB Secure Cloud & Brand Kits",
            "30-Day Full Replacement Warranty"
        ]
    },
    {
        "slug": "capcut-pro",
        "name": "CapCut Pro",
        "brand": "Bytedance",
        "pkr_price": "950",
        "usd_price": "3.50",
        "desc": "Export in 4K 60fps, generate auto-captions, and access full viral music libraries on PC and Mobile.",
        "category": "video movie reels",
        "bullets": [
            "AI Smart Auto-Captions & Subtitles",
            "4K 60fps Optical Flow Smooth Motion",
            "EasyPaisa, JazzCash, SadaPay & Wise",
            "30-Day Full Replacement Warranty"
        ]
    },
    {
        "slug": "nordvpn",
        "name": "NordVPN Complete",
        "brand": "Nord Security",
        "pkr_price": "850",
        "usd_price": "3.00",
        "desc": "Ultra-fast cybersecurity with 6,400+ servers, Threat Protection Pro, and private browsing in Pakistan.",
        "category": "vpn privacy security",
        "bullets": [
            "6,400+ High-Speed Global Servers",
            "Threat Protection Pro Ad & Malware Blocker",
            "10 Concurrent Device Connections",
            "30-Day Full Replacement Warranty"
        ]
    },
    {
        "slug": "midjourney",
        "name": "Midjourney v6",
        "brand": "Midjourney",
        "pkr_price": "2800",
        "usd_price": "10.00",
        "desc": "State-of-the-art photorealistic generative imaging with Fast GPU rendering hours and commercial license.",
        "category": "image design art",
        "bullets": [
            "Midjourney v6 & Niji v6 Japanese Anime",
            "Fast GPU Hours & Relax Unlimited",
            "EasyPaisa, JazzCash, Wise & Crypto",
            "30-Day Full Replacement Warranty"
        ]
    }
]

# Map 30 generated tools
category_map = {
    "perplexity-pro": "chat writing research",
    "gemini-advanced": "chat multimodal workspace",
    "grok-ai": "chat realtime news",
    "deepseek-pro": "coding reasoning api",
    "cursor-pro": "coding editor ai",
    "jetbrains-all": "coding ide developer",
    "github-copilot": "coding autocomplete vs-code",
    "replit-core": "coding cloud hosting",
    "claude-artifacts": "coding ui react",
    "chatgpt-codex": "coding api tokens",
    "adobe-creative-cloud": "image design video",
    "figma-pro": "image ui-ux design",
    "freepik-premium": "image vectors psd",
    "envato-elements": "image video templates",
    "google-veo": "video generative cinematic",
    "runway-gen3": "video camera motion",
    "kling-ai": "video realistic motion",
    "minimax-ai": "video hailuo animation",
    "leonardo-ai": "image gaming concept-art",
    "elevenlabs-creator": "voice audio cloning",
    "suno-ai": "voice audio music",
    "udio-ai": "voice audio music",
    "grammarly-pro": "writing proofreading grammar",
    "quillbot-premium": "writing paraphrasing essay",
    "semrush-guru": "seo marketing analytics",
    "surfshark-vpn": "vpn privacy unlimited",
    "notion-business": "productivity workspace ai",
    "linkedin-premium": "career business inmail",
    "youtube-premium": "streaming video ad-free",
    "netflix-premium": "streaming 4k entertainment"
}

all_36 = list(baseline_6)
for t in g30.tools_data:
    all_36.append({
        "slug": t["slug"],
        "name": t["name"],
        "brand": t["brand"],
        "pkr_price": t["pkr_price"],
        "usd_price": t["usd_price"],
        "desc": t["cards"][0][1],
        "category": category_map.get(t["slug"], "ai software"),
        "bullets": [
            f"{t['brand']} Verified Enterprise Setup",
            "EasyPaisa, JazzCash, Wise & Crypto",
            "Instant 15-Minute Delivery SLA Worldwide",
            "30-Day Full Replacement Warranty"
        ]
    })

print(f"Total tools for index: {len(all_36)}")

# Generate Grid HTML
cards_html = []
for it in all_36:
    bullet_items = "".join(f"              <li>✓ {b}</li>\n" for b in it["bullets"])
    c = f"""        <div class="card tool-card" data-category="{it['category']}">
          <div>
            <h2>{it['name']}</h2>
            <p>{it['desc']}</p>
            <div class="price-tag">Rs. {it['pkr_price']} PKR <span class="period">(~${it['usd_price']} USD) / month</span></div>
            <ul style="list-style:none; margin:1rem 0; color:var(--text-secondary); font-size:0.92rem; line-height:2;">
{bullet_items}            </ul>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.6rem; margin-top:1rem;">
            <a href="tools/{it['slug']}.html" style="color:var(--accent-gold); text-decoration:none; font-weight:600;">View Full Specs &amp; Benchmark Data →</a>
            <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20{it['name']}%20for%20Rs%20{it['pkr_price']}%20PKR%20/%20${it['usd_price']}%20USD" class="btn-whatsapp">Order {it['name']} on WhatsApp</a>
          </div>
        </div>"""
    cards_html.append(c)

tools_grid_block = "\n\n".join(cards_html)

# Generate Pricing Table Rows
table_rows = []
for it in all_36:
    row = f"""          <tr>
            <td><strong>{it['name']}</strong></td>
            <td>Rs. {it['pkr_price']} PKR / ${it['usd_price']} USD</td>
            <td>EasyPaisa, JazzCash, SadaPay, Wise, Crypto</td>
            <td>15 Minutes</td>
            <td>30-Day Replacement Guarantee</td>
          </tr>"""
    table_rows.append(row)

table_rows_block = "\n".join(table_rows)

index_path = ROOT / "index.html"
content = index_path.read_text(encoding="utf-8")

# Replace <div class="grid" id="toolsGrid">...</div>
grid_pattern = re.compile(r'(<div class="grid" id="toolsGrid">)(.*?)(</div>\s*</section>\s*<section id="pricing")', re.DOTALL)
m = grid_pattern.search(content)
if not m:
    print("Could not match toolsGrid block!")
    exit(1)

new_content = content[:m.start(2)] + "\n" + tools_grid_block + "\n      " + content[m.end(2):]

# Replace <tbody>...</tbody>
tbody_pattern = re.compile(r'(<tbody>)(.*?)(</tbody>)', re.DOTALL)
m2 = tbody_pattern.search(new_content)
if not m2:
    print("Could not match tbody in pricing table!")
    exit(1)

new_content = new_content[:m2.start(2)] + "\n" + table_rows_block + "\n        " + new_content[m2.end(2):]

index_path.write_text(new_content, encoding="utf-8")
print("[SUCCESS] index.html updated with all 36 tools in grid and pricing table!")
