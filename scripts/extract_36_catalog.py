import csv
import sys
import json
from collections import defaultdict
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

csv_path = Path(r'C:\Users\Dell\Desktop\reseller_products_2026-10-22.csv')

tools_36 = [
    # Hub 1: AI Chat & Reasoning
    ('chatgpt-plus', 'ChatGPT Plus', ['chatgpt plus', 'chat gpt plus']),
    ('claude-pro', 'Claude Pro', ['claude pro', 'claude.ai']),
    ('perplexity-pro', 'Perplexity Pro', ['perplexity pro']),
    ('gemini-advanced', 'Google Gemini Advanced', ['gemini', 'gemini pro', 'gemini ai']),
    ('grok-ai', 'Grok AI Super', ['grok']),
    ('deepseek-pro', 'DeepSeek Pro API', ['deepseek']),
    
    # Hub 2: AI Coding & Dev
    ('cursor-pro', 'Cursor AI Pro', ['cursor pro']),
    ('jetbrains-all', 'JetBrains All Products', ['jetbrains']),
    ('github-copilot', 'GitHub Copilot', ['copilot', 'github copilot']),
    ('replit-core', 'Replit Core', ['replit']),
    ('claude-artifacts', 'Claude Code Developer', ['claude']),
    ('chatgpt-codex', 'OpenAI API & Codex', ['openai api', 'chatgpt']),
    
    # Hub 3: Design & Graphics
    ('canva-pro', 'Canva Pro', ['canva pro', 'canva']),
    ('adobe-creative-cloud', 'Adobe Creative Cloud', ['adobe express', 'adobe creative', 'adobe']),
    ('figma-pro', 'Figma Pro', ['figma']),
    ('midjourney', 'Midjourney Standard', ['midjourney']),
    ('freepik-premium', 'Freepik Premium', ['freepik']),
    ('envato-elements', 'Envato Elements', ['envato']),
    
    # Hub 4: AI Video & Motion
    ('capcut-pro', 'CapCut Pro', ['capcut pro', 'capcut']),
    ('google-veo', 'Google Veo Omni', ['veo', 'google veo']),
    ('runway-gen3', 'Runway Gen-3 Alpha', ['runway']),
    ('kling-ai', 'Kling AI Pro', ['kling']),
    ('minimax-ai', 'MiniMax Hailuo AI', ['minimax', 'hailuo']),
    ('leonardo-ai', 'Leonardo AI Pro', ['leonardo']),
    
    # Hub 5: AI Voice, Audio & Content
    ('elevenlabs-creator', 'ElevenLabs Creator', ['elevenlabs', 'eleven labs']),
    ('suno-ai', 'Suno AI Pro', ['suno']),
    ('udio-ai', 'Udio AI Pro', ['udio']),
    ('grammarly-pro', 'Grammarly Pro', ['grammarly']),
    ('quillbot-premium', 'QuillBot Premium', ['quillbot']),
    ('semrush-guru', 'Semrush Guru', ['semrush']),
    
    # Hub 6: Cybersecurity & Streaming
    ('nordvpn', 'NordVPN Complete', ['nordvpn', 'nord vpn']),
    ('surfshark-vpn', 'Surfshark VPN', ['surfshark']),
    ('notion-business', 'Notion Business AI', ['notion']),
    ('linkedin-premium', 'LinkedIn Premium Career', ['linkedin']),
    ('youtube-premium', 'YouTube Premium', ['youtube premium', 'youtube']),
    ('netflix-premium', 'Netflix 4K UHD', ['netflix'])
]

catalog = defaultdict(list)
with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row.get('Product Name', '').strip()
        price_raw = row.get('Price (USDT)', '0').strip()
        stock = row.get('Stock', '').strip()
        try:
            price = float(price_raw.replace('USDT', '').strip())
        except:
            price = 0.0
        
        for slug, title, aliases in tools_36:
            if any(a in name.lower() for a in aliases):
                catalog[slug].append({
                    'name': name,
                    'price': price,
                    'stock': stock
                })

print('=' * 105)
print(f"{'Slug':22} | {'Tool Name':25} | {'Variants':8} | {'Min USDT':10} | {'FW USDT':10} | {'Wholesale PKR':13}")
print('=' * 105)

summary_data = []
for slug, title, aliases in tools_36:
    items = catalog[slug]
    priced = [it for it in items if it['price'] > 0]
    if priced:
        min_p = min(p['price'] for p in priced)
        fw_items = [p for p in priced if 'warranty' in p['name'].lower() or 'fw' in p['name'].lower()]
        fw_p = min(f['price'] for f in fw_items) if fw_items else min_p
    else:
        min_p = 0.0
        fw_p = 0.0
        
    pkr_cost = round(fw_p * 280) if fw_p > 0 else round(min_p * 280)
    print(f"{slug:22} | {title:25} | {len(items):8} | ${min_p:8.2f} | ${fw_p:8.2f} | Rs. {pkr_cost:7,d} PKR")
    summary_data.append({
        'slug': slug,
        'title': title,
        'variants': len(items),
        'min_usdt': min_p,
        'fw_usdt': fw_p,
        'pkr_cost': pkr_cost
    })
print('=' * 105)

with open('catalog_36_summary.json', 'w', encoding='utf-8') as out_f:
    json.dump(summary_data, out_f, indent=2)
