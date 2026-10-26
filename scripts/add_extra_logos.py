# scripts/add_extra_logos.py
import os

base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "product-logos")

ms_svg = """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0078D4"/>
  <rect x="13" y="13" width="10" height="10" rx="1.5" fill="#F25022"/>
  <rect x="25" y="13" width="10" height="10" rx="1.5" fill="#7FBA00"/>
  <rect x="13" y="25" width="10" height="10" rx="1.5" fill="#00A4EF"/>
  <rect x="25" y="25" width="10" height="10" rx="1.5" fill="#FFB900"/>
</svg>"""

tv_svg = """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#131722"/>
  <path d="M12 28l6-8 6 5 8-11 4 4" stroke="#2962FF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="36" cy="18" r="2.5" fill="#2962FF"/>
</svg>"""

with open(os.path.join(base, "microsoft-365.svg"), "w", encoding="utf-8") as f:
    f.write(ms_svg)

with open(os.path.join(base, "tradingview.svg"), "w", encoding="utf-8") as f:
    f.write(tv_svg)

print("Added microsoft-365.svg and tradingview.svg successfully!")
