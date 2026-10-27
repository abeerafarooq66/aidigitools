import os
import re
import json
import urllib.parse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ALL_49_SLUGS = [
    'youtube-premium', 'chatgpt-plus', 'claude-pro', 'canva-pro', 'capcut-pro',
    'midjourney', 'adobe-creative-cloud', 'nordvpn', 'surfshark-vpn', 'cursor-pro',
    'perplexity-pro', 'elevenlabs-creator', 'deepseek-pro', 'netflix-premium',
    'suno-ai', 'runway-gen3', 'semrush-guru', 'notion-business', 'grammarly-pro',
    'quillbot-premium', 'github-copilot', 'figma-pro', 'envato-elements',
    'freepik-premium', 'jetbrains-all', 'replit-core', 'linkedin-premium',
    'gemini-advanced', 'grok-ai', 'kling-ai', 'leonardo-ai', 'minimax-ai',
    'udio-ai', 'google-veo', 'chatgpt-codex', 'claude-artifacts', 'heygen-ai',
    'gamma-app', 'n8n-automation', 'vidiq-boost', 'coursera-plus', 'google-ai-ultra',
    'lovable-ai', 'spotify-premium', 'microsoft-office-365', 'windows-11-pro',
    'prime-video', 'tradingview-pro', 'turnitin-student'
]

def update_cart_js():
    cart_path = os.path.join(REPO_ROOT, 'assets', 'cart.js')
    with open(cart_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update HELD_PRODUCTS to include all 49 slugs
    slugs_json = json.dumps(ALL_49_SLUGS)
    old_held_pattern = r'var\s+HELD_PRODUCTS\s*=\s*\[[^\]]+\];'
    new_held_decl = f'var HELD_PRODUCTS = {slugs_json};'
    content = re.sub(old_held_pattern, new_held_decl, content, count=1)

    with open(cart_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated assets/cart.js with all 49 HELD_PRODUCTS.")

def update_merchant_feed():
    feed_path = os.path.join(REPO_ROOT, 'merchant_feed.xml')
    with open(feed_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace <g:availability>in_stock</g:availability> with <g:availability>out_of_stock</g:availability>
    count = content.count('<g:availability>in_stock</g:availability>')
    content = content.replace('<g:availability>in_stock</g:availability>', '<g:availability>out_of_stock</g:availability>')

    with open(feed_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated merchant_feed.xml: {count} items set to out_of_stock.")

def update_tool_pages():
    tools_dir = os.path.join(REPO_ROOT, 'tools')
    modified_count = 0

    hold_banner_html = '''    <!-- Direct Orders Currently On Hold Banner -->
    <div class="card" style="border:1px solid #f59e0b; background:rgba(245, 158, 11, 0.08); padding:1.25rem 1.5rem; border-radius:12px; margin-bottom:1.75rem;">
      <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem;">
        <span style="font-size:1.2rem;">⚠️</span>
        <strong style="color:var(--text-primary); font-size:1.05rem;">Direct Orders Currently On Hold</strong>
      </div>
      <p style="font-size:0.9rem; color:var(--text-secondary); line-height:1.6; margin:0 0 0.5rem 0;">
        Direct automated checkout and subscription fulfillment are currently paused for this service pending verification of secondary licensing and vendor distribution terms.
      </p>
      <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.5; margin:0;">
        <strong>Notice:</strong> Inquiries submitted via WhatsApp are for stock and licensing inquiry only and do not constitute an order confirmation or binding sale.
      </p>
    </div>'''

    for fname in os.listdir(tools_dir):
        if not fname.endswith('.html'):
            continue
        slug = fname[:-5]
        fpath = os.path.join(tools_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            html = f.read()

        orig_html = html

        # 1. Update schema availability to OutOfStock
        html = re.sub(
            r'"availability":\s*"https://schema\.org/InStock"',
            r'"availability": "https://schema.org/OutOfStock"',
            html
        )

        # 2. Add badge if missing
        if 'Orders On Hold' not in html:
            html = re.sub(
                r'(<span class="badge">[^<]+</span>)(\s*)(<span class="badge">30-Day Replacement Warranty</span>)',
                r'\1\2<span class="badge" style="background:#fef3c7; color:#92400e;">Orders On Hold</span>\2\3',
                html,
                count=1
            )

        # 3. Add hold banner if missing
        if 'Direct Orders Currently On Hold' not in html:
            # Insert above <section style="margin-top:2rem;"> or above <h2 ...>Available Subscription Tiers
            tiers_m = re.search(r'(<h2[^>]*>Available Subscription Tiers</h2>)', html)
            if tiers_m:
                idx = tiers_m.start()
                html = html[:idx] + hold_banner_html + "\n\n      " + html[idx:]

        # 4. Replace Hero WhatsApp order button
        # e.g. <a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20... class="btn-whatsapp">Order ... on WhatsApp</a>
        hero_order_pat = r'<a\s+href="https://wa\.me/923326861112\?text=[^"]*want%20to%20order[^"]*"\s+class="btn-whatsapp">[^<]+</a>'
        tool_clean_name = slug.replace('-', ' ').title()
        inquiry_hero_btn = f'''<a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20am%20inquiring%20about%20availability%20for%20{urllib.parse.quote(tool_clean_name)}" target="_blank" rel="noopener noreferrer" class="btn-wa-subtle" style="width:100%; text-align:center; display:block; padding:0.75rem 1rem; border-radius:8px; font-weight:600; text-decoration:none;">
            💬 Inquire on WhatsApp for Current Availability
          </a>
          <p style="font-size:0.78rem; color:var(--text-muted); text-align:center; margin-top:0.4rem; line-height:1.35; margin-bottom:0;">
            Inquiries are for compliance &amp; stock verification only. An inquiry is not an order confirmation.
          </p>'''
        html = re.sub(hero_order_pat, inquiry_hero_btn, html, count=1)

        # 5. Replace choose plan buttons (openQuickOrderModal) with inquiry links
        # <button type="button" class="btn-choose-plan" onclick="openQuickOrderModal('slug', 'plan-id')"...>
        plan_btn_pat = r'<button\s+type="button"\s+class="btn-choose-plan"\s+onclick="openQuickOrderModal\([^)]+\)"[^>]*>.*?<span>Choose\s+([^<]+)</span>.*?<span>⚡</span>.*?</button>'
        def replace_plan_btn(m):
            plan_name = m.group(1).strip()
            msg = f"Hi AIDigiTools, I am inquiring about {plan_name} for {tool_clean_name}"
            return f'''<a href="https://wa.me/923326861112?text={urllib.parse.quote(msg)}" target="_blank" rel="noopener noreferrer" class="btn-wa-subtle" style="width:100%; text-align:center; display:block; padding:0.75rem 1rem; border-radius:8px; font-weight:600; text-decoration:none;">
              💬 Inquire on WhatsApp for Current Availability
            </a>
            <p style="font-size:0.78rem; color:var(--text-muted); text-align:center; margin-top:0.4rem; line-height:1.35; margin-bottom:0;">
              Inquiries are for compliance &amp; stock verification only. An inquiry is not an order confirmation.
            </p>'''
        html = re.sub(plan_btn_pat, replace_plan_btn, html, flags=re.S)

        if html != orig_html:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(html)
            modified_count += 1

    print(f"Updated {modified_count} tool pages in tools/ directory.")

def update_index_html():
    index_path = os.path.join(REPO_ROOT, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace any direct order link with inquiry link
    # href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20([^"]+)"
    def repl_order_link(m):
        raw_tool = m.group(1).replace('%20', ' ')
        inq_msg = f"Hi AIDigiTools, I am inquiring about availability for {raw_tool}. (Inquiry only; not an order confirmation)."
        return f'href="https://wa.me/923326861112?text={urllib.parse.quote(inq_msg)}"'

    html = re.sub(r'href="https://wa\.me/923326861112\?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20([^"]+)"', repl_order_link, html)

    # In centerpiece showcase, replace button text if needed
    html = html.replace('Order Now via WhatsApp', 'Inquire on WhatsApp for Current Availability')

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html: replaced all direct order WhatsApp links with inquiry links.")

def update_other_pages():
    pages = [
        'deals.html',
        '404.html',
        'best/best-ai-coding-tools.html',
        'best/best-ai-video-generators.html',
        'compare/runway-vs-pika.html'
    ]
    for rel in pages:
        p = os.path.join(REPO_ROOT, rel)
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        def repl_order(m):
            raw = m.group(1).replace('%20', ' ')
            inq = f"Hi AIDigiTools, I am inquiring about availability for {raw}. (Inquiry only; not an order confirmation)."
            return f'href="https://wa.me/923326861112?text={urllib.parse.quote(inq)}"'

        html = re.sub(r'href="https://wa\.me/923326861112\?text=Hi%20AIDigiTools,%20I%20want%20to%20order%20([^"]+)"', repl_order, html)
        html = html.replace('Order on WhatsApp', 'Inquire on WhatsApp')
        html = html.replace('Order Bundle on WhatsApp', 'Inquire on WhatsApp')
        html = html.replace('Order Bundle', 'Inquire on WhatsApp')

        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated {rel}.")

def update_test_structured_data():
    test_path = os.path.join(REPO_ROOT, 'tests', 'test_structured_data_compliance.py')
    with open(test_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # In test_04_product_and_offer_rich_result_properties:
    # held_slugs is currently 5 tools. Update held_slugs to all tool pages so all 49 must be OutOfStock
    old_block = '''            held_slugs = [
                "tools/turnitin-student.html",
                "tools/linkedin-premium.html",
                "tools/netflix-premium.html",
                "tools/spotify-premium.html",
                "tools/coursera-plus.html"
            ]
            if rel in held_slugs:
                self.assertEqual(offer.get("availability"), "https://schema.org/OutOfStock", f"Held product {rel} must have OutOfStock availability")
            else:
                self.assertEqual(offer.get("availability"), "https://schema.org/InStock", f"Active product {rel} must have InStock availability")'''

    new_block = '''            # All products have direct paid orders paused pending verification of official vendor supply rights
            self.assertEqual(offer.get("availability"), "https://schema.org/OutOfStock", f"Product {rel} must have OutOfStock availability while direct orders are paused")'''

    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated tests/test_structured_data_compliance.py to enforce OutOfStock across all tool pages.")
    else:
        print("Note: old_block in test_structured_data_compliance.py not matched directly.")

def main():
    update_cart_js()
    update_merchant_feed()
    update_tool_pages()
    update_index_html()
    update_other_pages()
    update_test_structured_data()
    print("\nGovernance and compliance updates applied successfully.")

if __name__ == '__main__':
    main()
