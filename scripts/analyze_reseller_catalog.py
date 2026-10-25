import csv
import sys
from collections import defaultdict
from pathlib import Path

# Ensure utf-8 output handling on windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

csv_path = Path(r"C:\Users\Dell\Desktop\reseller_products_2026-10-22.csv")

candidates = [
    "ChatGPT Plus", "Claude Pro", "Canva Pro", "CapCut Pro", "NordVPN", "Midjourney",
    "Cursor Pro", "Perplexity Pro", "ElevenLabs", "Adobe", "Runway", "Kling",
    "Grok", "Notion", "Figma", "Duolingo", "YouTube Premium", "Spotify", "Netflix",
    "LinkedIn", "Gemini", "Veo", "DeepSeek", "Suno", "Udio", "Freepik",
    "Grammarly", "QuillBot", "TradingView", "Office 365", "Discord Nitro",
    "Surfshark", "ExpressVPN", "JetBrains", "Envato", "Semrush"
]

results = defaultdict(list)
with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    for r in reader:
        name = r.get("Product Name", "").strip()
        price_str = r.get("Price (USDT)", "0").strip()
        stock = r.get("Stock", "").strip()
        desc = r.get("Description", "").replace("\n", " ")
        
        try:
            p_val = float(price_str.replace("USDT", "").strip())
        except:
            p_val = 0.0
            
        for c in candidates:
            if c.lower() in name.lower():
                results[c].append({"name": name, "price": p_val, "stock": stock, "desc": desc[:70]})

print("Candidate Tools Wholesale Price Summary (USDT):")
print("-" * 90)
for c in candidates:
    items = results.get(c, [])
    priced = [it for it in items if it["price"] > 0]
    if priced:
        min_it = min(priced, key=lambda x: x["price"])
        warranty_items = [it for it in priced if "warranty" in it["name"].lower() or "fw" in it["name"].lower()]
        best_w = min(warranty_items, key=lambda x: x["price"]) if warranty_items else min_it
        sample_name = best_w['name'][:30].encode("ascii", "replace").decode("ascii")
        print(f"{c:18} | Variants: {len(items):3} | Min: ${min_it['price']:6.2f} USDT | FW: ${best_w['price']:6.2f} USDT | Sample: {sample_name}")
    else:
        print(f"{c:18} | Variants: {len(items):3} | No priced items")

