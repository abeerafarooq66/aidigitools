import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

held_slugs = ['turnitin-student', 'linkedin-premium', 'netflix-premium', 'spotify-premium', 'coursera-plus']
non_separate_slugs = ['claude-artifacts', 'deepseek-pro']
all_restricted = held_slugs + non_separate_slugs

print("=" * 70)
print("AUDIT OF COMPLETE CUSTOMER JOURNEY FOR RESTRICTED PRODUCTS")
print("=" * 70)

# 1. Homepage Card Audit
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

print("\n1. HOMEPAGE CARD CHECKS:")
for slug in all_restricted:
    card_match = re.search(rf'<div class="card tool-card" data-tool="{slug}"[\s\S]*?(?=<div class="card tool-card"|<div class="container"|$)', index_html)
    if not card_match:
        print(f"  [ERROR] Card for {slug} not found in index.html!")
        continue
    block = card_match.group(0)
    has_modal_call = f"openQuickOrderModal('{slug}')" in block or f'openQuickOrderModal("{slug}")' in block
    has_wa_inquiry = "Inquiry only" in block or "inquiry" in block.lower()
    wa_href = re.search(r'href="([^"]*wa\.me[^"]*)"', block)
    status_badge = re.search(r'<span class="tool-status-badge[^"]*">([^<]+)</span>', block)
    badge_text = status_badge.group(1) if status_badge else "NONE"
    
    print(f"\n  Slug: {slug}")
    print(f"    - Status Badge: '{badge_text}'")
    print(f"    - Can trigger Quick Order modal directly: {has_modal_call}")
    print(f"    - Direct WhatsApp Inquiry link present: {bool(wa_href)}")
    if wa_href:
        print(f"    - Prefill text in WhatsApp link contains 'inquiry': {'inquiry' in wa_href.group(1).lower()}")

# 2. Product Detail Page Audit
print("\n" + "=" * 70)
print("2. PRODUCT DETAIL PAGE CHECKS:")
for slug in all_restricted:
    file_path = f"tools/{slug}.html"
    if not os.path.exists(file_path):
        print(f"  [ERROR] {file_path} missing!")
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    h1 = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    h1_text = h1.group(1).strip() if h1 else "NONE"
    qa = re.search(r'<p class="quick-answer">([\s\S]*?)</p>', content)
    qa_text = re.sub(r'\s+', ' ', qa.group(1).strip()) if qa else "NONE"
    has_hold_banner = "Direct Orders Currently On Hold" in content
    has_modal_call = f"openQuickOrderModal('{slug}'" in content or f'openQuickOrderModal("{slug}"' in content
    inquiry_btn = "Inquire on WhatsApp for Current Availability" in content
    disclaimer = "An inquiry is not an order confirmation" in content
    
    # Check JSON-LD
    schema_matches = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', content)
    prod_avail = "NONE"
    for sm in schema_matches:
        try:
            sd = json.loads(sm.strip())
            if sd.get('@type') == 'Product':
                prod_avail = sd.get('offers', {}).get('availability', 'NONE')
        except Exception:
            pass

    print(f"\n  Slug: {slug}")
    print(f"    - H1: {h1_text}")
    print(f"    - Hold Banner Present: {has_hold_banner}")
    print(f"    - Direct Modal Call: {has_modal_call}")
    print(f"    - Inquiry Button Present: {inquiry_btn}")
    print(f"    - Non-binding Disclaimer Present: {disclaimer}")
    print(f"    - Schema Availability: {prod_avail}")

# 3. Quick Order Drawer Safeguard Audit
print("\n" + "=" * 70)
print("3. QUICK ORDER DRAWER SAFEGUARD IN ASSETS/CART.JS:")
with open('assets/cart.js', 'r', encoding='utf-8') as f:
    cart_js = f.read()

held_match = re.search(r'var HELD_PRODUCTS = (\[[\s\S]*?\]);', cart_js)
if held_match:
    held_list = json.loads(held_match.group(1).replace("'", '"'))
    print(f"  Total items in HELD_PRODUCTS: {len(held_list)}")
    for s in all_restricted:
        print(f"    - {s} in HELD_PRODUCTS: {s in held_list}")

has_drawer_hold_notice = "Direct Orders Paused" in cart_js
has_inquire_checkout_text = "Inquire on WhatsApp for Current Availability" in cart_js
print(f"  Drawer shows hold notice for held products: {has_drawer_hold_notice}")
print(f"  Drawer replaces checkout button text with inquiry for held products: {has_inquire_checkout_text}")

