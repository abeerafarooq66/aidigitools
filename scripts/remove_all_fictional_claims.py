import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 1. Update contact.html
contact_path = ROOT / "contact.html"
contact_content = contact_path.read_text(encoding="utf-8")

# Fix Schema address
old_schema_addr = '''      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Suite 402, Level 4, Tech Innovation Hub, Sector F-7",
        "addressLocality": "Islamabad",
        "addressRegion": "ICT",
        "postalCode": "44000",
        "addressCountry": "PK"
      },'''

new_schema_addr = '''      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Islamabad",
        "addressCountry": "PK"
      },'''

contact_content = contact_content.replace(old_schema_addr, new_schema_addr)

# Fix HTML body card
old_card = '''      <div class="card">
        <h2>Registered Office Address</h2>
        <p>Official corporate location in compliance with Google Merchant Center standards:</p>
        <p style="color:var(--accent-gold); font-weight:600; margin-top:0.5rem;">
          Suite 402, Level 4, Tech Innovation Hub, Sector F-7, Islamabad, Pakistan (44000)
        </p>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-top:0.5rem;">Operating Hours: Monday – Sunday, 09:00 AM – 11:00 PM PKT</p>
      </div>'''

new_card = '''      <div class="card">
        <h2>Digital Operations Help Desk</h2>
        <p>100% online software subscription desk serving Pakistan and worldwide customers:</p>
        <p style="color:var(--accent-gold); font-weight:600; margin-top:0.5rem;">
          Online Marketplace Operations, Islamabad, Pakistan
        </p>
        <p style="font-size:0.88rem; color:var(--text-muted); margin-top:0.5rem;">Customer Support Hours: Monday – Sunday, 09:00 AM – 11:00 PM PKT (Digital Delivery within 15 minutes)</p>
      </div>'''

contact_content = contact_content.replace(old_card, new_card)
contact_path.write_text(contact_content, encoding="utf-8")
print("[OK] contact.html updated: 100% genuine online operations desk!")

# 2. Update affiliate-disclosure.html
aff_path = ROOT / "affiliate-disclosure.html"
aff_content = aff_path.read_text(encoding="utf-8")
aff_content = aff_content.replace(
    "<p><strong>Office:</strong> Floor 3, Blue Area, Sector F-7, Islamabad, Pakistan</p>",
    "<p><strong>Operations:</strong> Online Digital Software Marketplace, Islamabad, Pakistan</p>"
)
aff_path.write_text(aff_content, encoding="utf-8")
print("[OK] affiliate-disclosure.html updated: fictional floor/blue area removed!")

# 3. Update tools/*.html footers
tools_dir = ROOT / "tools"
tool_count = 0
for tf in tools_dir.glob("*.html"):
    txt = tf.read_text(encoding="utf-8")
    new_txt = txt.replace(
        "Registered software license aggregator based in Islamabad, Pakistan.",
        "Online AI software marketplace serving Pakistan and worldwide."
    )
    if new_txt != txt:
        tf.write_text(new_txt, encoding="utf-8")
        tool_count += 1

print(f"[OK] Updated {tool_count} tool pages: removed 'Registered aggregator' claim in footer!")

# 4. Check scripts/generate_30_tools.py to keep template updated
gen_path = ROOT / "scripts" / "generate_30_tools.py"
if gen_path.exists():
    gen_txt = gen_path.read_text(encoding="utf-8")
    gen_txt = gen_txt.replace(
        "Registered software license aggregator based in Islamabad, Pakistan.",
        "Online AI software marketplace serving Pakistan and worldwide."
    )
    gen_path.write_text(gen_txt, encoding="utf-8")
    print("[OK] scripts/generate_30_tools.py template sanitized!")

print("[SUCCESS] All fictional street addresses and unverified corporate claims permanently eliminated!")
