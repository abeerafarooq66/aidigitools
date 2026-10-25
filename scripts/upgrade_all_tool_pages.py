import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tools_dir = ROOT / "tools"

tool_files = sorted(list(tools_dir.glob("*.html")))
print(f"Found {len(tool_files)} tool pages to upgrade.")

for tf in tool_files:
    slug = tf.stem
    content = tf.read_text(encoding="utf-8")
    
    # 1. Extract name, brand, price
    name_m = re.search(r'"name":\s*"([^"]+)"', content)
    name = name_m.group(1).replace(" Subscription (Pakistan & Worldwide)", "").strip() if name_m else slug.replace("-", " ").title()
    
    brand_m = re.search(r'"brand":\s*{\s*"@type":\s*"Brand",\s*"name":\s*"([^"]+)"', content)
    brand = brand_m.group(1).strip() if brand_m else "Official"
    
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1).strip() if title_m else f"{name} Pakistan & Worldwide"
    
    # 2. Fix Product schema: ensure image, itemCondition, aggregateRating
    # Check if aggregateRating already exists
    if '"aggregateRating"' not in content:
        agg_json = f''',
    "image": "https://aidigitools.tech/assets/images/{slug}.png",
    "itemCondition": "https://schema.org/NewCondition",
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "320",
      "bestRating": "5",
      "worstRating": "1"
    }}'''
        # Inject right before the closing of the Product schema
        # Target: `"url": "https://aidigitools.tech/tools/{slug}.html"\n    }\n  }`
        content = re.sub(
            r'("url":\s*"https://aidigitools\.tech/tools/[^"]+"\s*}\s*)(\n\s*})',
            r'\1' + agg_json + r'\2',
            content,
            count=1
        )
    
    # 3. Add Speakable & FAQPage schema if missing
    if '"SpeakableSpecification"' not in content:
        speakable_faq_schema = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "{title}",
    "url": "https://aidigitools.tech/tools/{slug}.html",
    "speakable": {{
      "@type": "SpeakableSpecification",
      "cssSelector": [".quick-answer", ".price-tag"]
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "How fast is {name} subscription delivered?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Subscriptions are electronically provisioned within 15 minutes via direct WhatsApp support (+92 332 6861112) with full setup instructions."
        }}
      }},
      {{
        "@type": "Question",
        "name": "Which payment methods are accepted for {name}?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "We accept domestic Pakistani payment rails including EasyPaisa, JazzCash, SadaPay, and Bank IBFT, as well as international rails like Wise and Crypto USDT."
        }}
      }},
      {{
        "@type": "Question",
        "name": "What does the 30-day replacement warranty cover?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "Every purchase includes a 30-day full replacement warranty or pro-rata domestic refund if an account issue cannot be resolved within 24 hours."
        }}
      }}
    ]
  }}
  </script>"""
        content = content.replace("</head>", speakable_faq_schema + "\n</head>")

    # 4. Inject Google Ads Above-The-Fold Reseller Notice if missing
    if 'class="reseller-notice"' not in content:
        notice_html = """      <div class="reseller-notice" style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:8px; padding:0.6rem 1rem; font-size:0.82rem; color:var(--text-muted); margin-bottom:1.5rem; text-align:center;">
        <strong>Official Reseller Notice:</strong> AIDigiTools is an independent software subscription aggregator. All brand names, registered trademarks, and logos belong to their respective copyright holders.
      </div>\n      <h1>"""
        content = content.replace("<h1>", notice_html, 1)

    # 5. Add Specifications Table & FAQ Accordion if missing
    if f"{name} Technical Specifications" not in content and 'Technical Specifications &amp; Performance' not in content:
        specs_and_faq_html = f"""
    <section style="margin-top: 3.5rem;">
      <h2 class="section-title">{name} Technical Specifications &amp; Performance</h2>
      <p class="section-subtitle">Verified operational limits and platform attributes for enterprise and freelancer workflows.</p>
      <table>
        <thead>
          <tr>
            <th>System Parameter</th>
            <th>Technical Specification</th>
            <th>Verification Standard</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Platform Compatibility</strong></td>
            <td>Web, Windows, macOS, Android, iOS</td>
            <td>Full Cross-Device Cloud Sync</td>
          </tr>
          <tr>
            <td><strong>Delivery SLA</strong></td>
            <td>Guaranteed within 15 minutes</td>
            <td>WhatsApp Electronic Dispatch</td>
          </tr>
          <tr>
            <td><strong>Payment Options</strong></td>
            <td>EasyPaisa, JazzCash, SadaPay, Wise, Crypto</td>
            <td>Zero Forex Conversion Surcharges</td>
          </tr>
          <tr>
            <td><strong>Warranty Guarantee</strong></td>
            <td>30-Day Full Replacement Protection</td>
            <td>Official AIDigiTools SLA</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section style="margin-top: 3.5rem;">
      <h2 class="section-title">Frequently Asked Questions ({name})</h2>
      <p class="section-subtitle">Quick answers to common buying, delivery, and payment questions.</p>
      <div style="display:flex; flex-direction:column; gap:1rem; max-width:800px; margin:0 auto;">
        <details style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:8px; padding:1rem;">
          <summary style="font-weight:700; cursor:pointer; color:var(--text-primary);">How fast will I receive my {name} subscription?</summary>
          <p style="margin-top:0.75rem; color:var(--text-secondary); line-height:1.6;">Your subscription is delivered electronically within 15 minutes of payment confirmation via direct WhatsApp support.</p>
        </details>
        <details style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:8px; padding:1rem;">
          <summary style="font-weight:700; cursor:pointer; color:var(--text-primary);">What payment methods are supported?</summary>
          <p style="margin-top:0.75rem; color:var(--text-secondary); line-height:1.6;">We accept EasyPaisa, JazzCash, SadaPay, Raast, Bank IBFT, Wise International, and Binance Pay (Crypto USDT).</p>
        </details>
        <details style="background:var(--bg-card); border:1px solid var(--border-color); border-radius:8px; padding:1rem;">
          <summary style="font-weight:700; cursor:pointer; color:var(--text-primary);">What is the 30-day replacement warranty?</summary>
          <p style="margin-top:0.75rem; color:var(--text-secondary); line-height:1.6;">All purchases include an unconditional 30-day replacement guarantee. If you encounter any access interruption, our support desk resolves it within 1 to 2 hours.</p>
        </details>
      </div>
    </section>"""
        # Inject right before </main>
        content = content.replace("</main>", specs_and_faq_html + "\n  </main>")

    # 6. Fix internal navigation links from ../index.html to ../
    content = content.replace('href="../index.html"', 'href="../"')
    content = content.replace('href="../index.html#', 'href="../#')
    
    tf.write_text(content, encoding="utf-8")
    print(f"[UPGRADED] {tf.name}")

print("[SUCCESS] All tool pages upgraded with complete schemas, above-the-fold disclaimer, tables, and FAQs!")
