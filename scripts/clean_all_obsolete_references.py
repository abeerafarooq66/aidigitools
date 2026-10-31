import os
import sys
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

def patch_file(rel_path, replacements):
    fpath = os.path.join(REPO_ROOT, rel_path)
    if not os.path.exists(fpath):
        print(f"File not found: {rel_path}")
        return
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    changed = 0
    for old_s, new_s in replacements:
        if old_s in content:
            content = content.replace(old_s, new_s)
            changed += 1
        else:
            # Try case-insensitive or regex if needed
            pass

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Patched {rel_path}: {changed} replacements made.")

def clean_index_html():
    fpath = os.path.join(REPO_ROOT, "index.html")
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()

    replacements = [
        ('alt="GitHub Copilot Pro Official Logo"', 'alt="GitHub Copilot Official Logo"'),
        ('aria-label="Compare GitHub Copilot Pro"', 'aria-label="Compare GitHub Copilot"'),
        ('alt="Google Gemini Advanced Official Logo"', 'alt="Google AI Pro Official Logo"'),
        ('aria-label="Compare Google Gemini Advanced"', 'aria-label="Compare Google AI Pro"'),
        ('alt="Google Veo 2 Official Logo"', 'alt="Google Veo 3.1 Official Logo"'),
        ('aria-label="Compare Google Veo 2"', 'aria-label="Compare Google Veo 3.1"'),
        ('<td><strong>Google Gemini Advanced</strong></td>', '<td><strong>Google AI Pro</strong></td>'),
        ('data-terms="runway gen-3 alpha', 'data-terms="runway gen-4 gen-3 alpha'),
        ('data-terms="suno ai music v3.5', 'data-terms="suno ai music v5.5 v6'),
        ('data-terms="midjourney v6.1', 'data-terms="midjourney v8 v8.2'),
        ('data-terms="google veo 2', 'data-terms="google veo 3.1 veo 3'),
        ('data-terms="grok 2', 'data-terms="xai grok grok 3 supergrok'),
        ('data-terms="google gemini advanced', 'data-terms="google ai pro gemini advanced'),
        ('data-terms="google ai ultra plan (20x)', 'data-terms="google ai ultra 20x tier'),
        ('data-terms="github copilot pro', 'data-terms="github copilot individual'),
        ('Google AI Ultra (20X Plan) • Rs. 4,500 PKR', 'Google AI Ultra • Rs. 4,500 PKR'),
        ('ChatGPT Plus — Rs. 2,300 PKR', 'ChatGPT Plus • Rs. 2,300 PKR'),
    ]
    for old_s, new_s in replacements:
        if old_s in c:
            c = c.replace(old_s, new_s)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(c)
    print("Cleaned index.html")

def clean_tool_pages():
    # gemini-advanced.html
    patch_file("tools/gemini-advanced.html", [
        ('<span aria-current="page">Google Gemini Advanced</span>', '<span aria-current="page">Google AI Pro</span>'),
        ('alt="Google Gemini Advanced Official Logo"', 'alt="Google AI Pro Official Logo"'),
        ('Compare Verified Google Gemini Advanced Plans', 'Compare Verified Google AI Pro Plans'),
        ('Google Gemini Advanced Technical Specifications', 'Google AI Pro Technical Specifications'),
        ('Frequently Asked Questions (Google Gemini Advanced)', 'Frequently Asked Questions (Google AI Pro)'),
        ('official vendor disclosures for Google Gemini Advanced.', 'official vendor disclosures for Google AI Pro.'),
        ('"name": "Google Gemini Advanced"', '"name": "Google AI Pro"'),
        ('"name": "Google Gemini Advanced Pakistan & Worldwide | Pricing"', '"name": "Google AI Pro Pakistan & Worldwide | Pricing"'),
        ('How fast is Google Gemini Advanced subscription delivered?', 'How fast is Google AI Pro subscription delivered?'),
        ('Which payment methods are accepted for Google Gemini Advanced?', 'Which payment methods are accepted for Google AI Pro?'),
        ('Google Gemini Advanced Pricing in Pakistan', 'Google AI Pro Pricing in Pakistan'),
    ])

    # google-veo.html
    patch_file("tools/google-veo.html", [
        ('<span aria-current="page">Google Veo 2</span>', '<span aria-current="page">Google Veo 3.1</span>'),
        ('alt="Google Veo 2 Official Logo"', 'alt="Google Veo 3.1 Official Logo"'),
        ('Compare Verified Google Veo 2 Plans', 'Compare Verified Google Veo 3.1 Plans'),
        ('Google Veo 2 Technical Specifications', 'Google Veo 3.1 Technical Specifications'),
        ('Frequently Asked Questions (Google Veo 2)', 'Frequently Asked Questions (Google Veo 3.1)'),
        ('official vendor disclosures for Google Veo 2.', 'official vendor disclosures for Google Veo 3.1.'),
        ('"name": "Google Veo 2"', '"name": "Google Veo 3.1"'),
        ('Google Veo 2 Pricing in Pakistan', 'Google Veo 3.1 Pricing in Pakistan'),
        ('How fast is Google Veo 2 delivered?', 'How fast is Google Veo 3.1 delivered?'),
    ])

    # google-ai-ultra.html
    patch_file("tools/google-ai-ultra.html", [
        ('Buy Google AI Ultra 20X in Pakistan | Pricing', 'Google AI Ultra Pakistan (PKR & USD) — Buy | AIDigiTools'),
        ('Google AI Ultra 20X Advanced Intelligence', 'Google AI Ultra Pakistan & Worldwide — Pricing & Rails'),
        ('The Google AI Ultra plan provides high-compute priority access to Gemini 1.5 Pro and Gemini Advanced', 'The Google AI Ultra plan provides high-compute priority access to Gemini 4 Argon and Deep Think reasoning'),
        ('Google AI Ultra Plan (20X)', 'Google AI Ultra'),
        ('"name": "Buy Google AI Ultra 20X in Pakistan | Pricing"', '"name": "Google AI Ultra Pakistan & Worldwide | Pricing"'),
    ])

    # grok-ai.html
    patch_file("tools/grok-ai.html", [
        ('SuperGrok / Grok 2 (1 Month)', 'SuperGrok / Grok 3 (1 Month)'),
        ('Grok 2 AI model', 'Grok 3 and Grok 2 AI models'),
        ('Grok 2 / xAI SuperGrok', 'xAI Grok / SuperGrok'),
    ])

    # github-copilot.html
    patch_file("tools/github-copilot.html", [
        ('<span aria-current="page">GitHub Copilot Pro</span>', '<span aria-current="page">GitHub Copilot Individual</span>'),
        ('alt="GitHub Copilot Pro Official Logo"', 'alt="GitHub Copilot Official Logo"'),
        ('Compare Verified GitHub Copilot Pro & Business Plans', 'Compare Verified GitHub Copilot Individual & Team Plans'),
        ('GitHub Copilot Pro Technical Specifications', 'GitHub Copilot Technical Specifications'),
        ('Frequently Asked Questions (GitHub Copilot Pro)', 'Frequently Asked Questions (GitHub Copilot)'),
        ('official vendor disclosures for GitHub Copilot Pro.', 'official vendor disclosures for GitHub Copilot.'),
        ('GitHub Copilot Pro Pricing in Pakistan', 'GitHub Copilot Pricing in Pakistan'),
    ])

    # midjourney.html
    patch_file("tools/midjourney.html", [
        ('Midjourney V6 Core Capabilities', 'Midjourney V8 Core Capabilities'),
        ('Midjourney v6.1', 'Midjourney V8'),
    ])

    # perplexity-pro.html
    patch_file("tools/perplexity-pro.html", [
        ('Grok 2 AI', 'xAI Grok'),
    ])

def clean_categories():
    patch_file("categories/video.html", [
        ('"name": "Google Veo 2"', '"name": "Google Veo 3.1"'),
        ('<td><strong>Google Veo 2</strong></td>', '<td><strong>Google Veo 3.1</strong></td>'),
        ('<td><strong>Runway Gen-3</strong></td>', '<td><strong>Runway AI Video (Gen-4/Gen-3)</strong></td>'),
        ('<td><strong>Suno AI Music Generator</strong></td>', '<td><strong>Suno AI Music (v5.5/v6)</strong></td>'),
        ('<td><strong>MiniMax Hailuo AI</strong></td>', '<td><strong>Hailuo AI Video (MiniMax)</strong></td>'),
    ])

    patch_file("categories/coding.html", [
        ('<td><strong>Claude Pro (Claude 3.5 Sonnet)</strong></td>', '<td><strong>Claude Pro (Claude Sonnet 5.5)</strong></td>'),
        ('<td><strong>ChatGPT Plus (GPT-4o & Canvas)</strong></td>', '<td><strong>ChatGPT Plus (GPT-5/GPT-6 & Canvas)</strong></td>'),
        ('<td><strong>DeepSeek Pro Coder</strong></td>', '<td><strong>DeepSeek Platform (R1 / V3)</strong></td>'),
        ('<td><strong>ChatGPT Codex Specialized Seat</strong></td>', '<td><strong>OpenAI Codex (Agent & Desktop)</strong></td>'),
        ('<td><strong>Claude Artifacts Sandbox Seat</strong></td>', '<td><strong>Claude Artifacts (Code Canvas)</strong></td>'),
    ])

    patch_file("categories/image.html", [
        ('<td><strong>Midjourney Standard</strong></td>', '<td><strong>Midjourney V8</strong></td>'),
    ])

    patch_file("best/best-ai-coding-tools.html", [
        ('Anthropic Claude 3.5 Sonnet', 'Anthropic Claude Pro (Sonnet 5.5)'),
        ('OpenAI ChatGPT Plus (GPT-4o)', 'OpenAI ChatGPT Plus (GPT-5/GPT-6)'),
    ])

    patch_file("best/best-ai-video-generators.html", [
        ('Runway Gen-3', 'Runway AI Video (Gen-4 / Gen-3)'),
    ])

def clean_feeds():
    from scripts.master_product_dictionary import PRODUCT_MAP
    
    # 1. Clean merchant_feed.xml
    mf_path = os.path.join(REPO_ROOT, "merchant_feed.xml")
    with open(mf_path, "r", encoding="utf-8") as f:
        mf = f.read()

    for slug, info in PRODUCT_MAP.items():
        pattern = rf'(<g:id>aidigitools-{slug}</g:id>\s*<g:title>)[^<]+(</g:title>\s*<g:description>)[^<]+(</g:description>)'
        clean_title = f"{info['brand']} {info['official_product_name']} Subscription — 1 Month Access"
        clean_desc = f"{info['desc']} Available in Pakistan &amp; worldwide via EasyPaisa, JazzCash, and SadaPay with 15m WhatsApp delivery."
        mf, _ = re.subn(pattern, f"\\g<1>{clean_title}\\g<2>{clean_desc}\\g<3>", mf)

    with open(mf_path, "w", encoding="utf-8") as f:
        f.write(mf)
    print("Cleaned merchant_feed.xml")

    # 2. Clean feed.xml
    feed_path = os.path.join(REPO_ROOT, "feed.xml")
    with open(feed_path, "r", encoding="utf-8") as f:
        feed = f.read()

    for slug, info in PRODUCT_MAP.items():
        pattern = rf'(<guid>https://aidigitools\.tech/tools/{slug}\.html</guid>\s*<description>)[^<]+(</description>)'
        clean_desc = f"Get {info['official_product_name']} on AIDigiTools. EasyPaisa, JazzCash, SadaPay, Wise &amp; Crypto. 15-minute delivery target &amp; 30-day warranty."
        feed, _ = re.subn(pattern, f"\\g<1>{clean_desc}\\g<2>", feed)
        
        title_pattern = rf'(<link>https://aidigitools\.tech/tools/{slug}\.html</link>\s*<guid>https://aidigitools\.tech/tools/{slug}\.html</guid>\s*<title>)[^<]+(</title>)'
        # Also check title preceding link
        title_pattern2 = rf'(<item>\s*<title>)[^<]+(</title>\s*<link>https://aidigitools\.tech/tools/{slug}\.html</link>)'
        clean_item_title = f"{info['official_product_name']} Pakistan &amp; Worldwide Subscription — Pricing"
        feed, _ = re.subn(title_pattern2, f"\\g<1>{clean_item_title}\\g<2>", feed)

    with open(feed_path, "w", encoding="utf-8") as f:
        f.write(feed)
    print("Cleaned feed.xml")

def clean_manifests():
    # brand_logos_manifest.json
    bm_path = os.path.join(REPO_ROOT, "assets", "product-logos", "brand_logos_manifest.json")
    if os.path.exists(bm_path):
        with open(bm_path, "r", encoding="utf-8") as f:
            bm = f.read()
        repls = [
            ('"canonical_name": "Google Gemini Advanced"', '"canonical_name": "Google AI Pro"'),
            ('"canonical_name": "Google Veo 2"', '"canonical_name": "Google Veo 3.1"'),
            ('"canonical_name": "Google AI Ultra Plan (20X)"', '"canonical_name": "Google AI Ultra"'),
            ('"canonical_name": "Grok 2"', '"canonical_name": "xAI Grok"'),
            ('"canonical_name": "Midjourney v6.1"', '"canonical_name": "Midjourney V8"'),
            ('"canonical_name": "GitHub Copilot Pro"', '"canonical_name": "GitHub Copilot Individual"'),
            ('"canonical_name": "Runway Gen-3 Alpha"', '"canonical_name": "Runway AI Video"'),
            ('"canonical_name": "Suno AI Music v3.5"', '"canonical_name": "Suno AI Music"'),
        ]
        for o, n in repls:
            bm = bm.replace(o, n)
        with open(bm_path, "w", encoding="utf-8") as f:
            f.write(bm)
        print("Cleaned brand_logos_manifest.json")

    # business_claims_inventory.json
    bci_path = os.path.join(REPO_ROOT, "data", "business_claims_inventory.json")
    if os.path.exists(bci_path):
        with open(bci_path, "r", encoding="utf-8") as f:
            bci = f.read()
        repls = [
            ('Google Gemini Advanced', 'Google AI Pro'),
            ('Google Veo 2', 'Google Veo 3.1'),
            ('Google AI Ultra Plan (20X)', 'Google AI Ultra'),
            ('Grok 2', 'xAI Grok'),
            ('Midjourney v6.1', 'Midjourney V8'),
            ('GitHub Copilot Pro', 'GitHub Copilot Individual'),
            ('Runway Gen-3 Alpha', 'Runway AI Video'),
            ('Suno AI Music v3.5', 'Suno AI Music'),
        ]
        for o, n in repls:
            bci = bci.replace(o, n)
        with open(bci_path, "w", encoding="utf-8") as f:
            f.write(bci)
        print("Cleaned business_claims_inventory.json")

if __name__ == "__main__":
    clean_index_html()
    clean_tool_pages()
    clean_categories()
    clean_feeds()
    clean_manifests()
    print("--- FINISHED CLEANING OBSOLETE REFERENCES ---")
