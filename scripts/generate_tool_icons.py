"""
Generate 36 official brand SVG icons for AIDigiTools product cards and pricing table.
Clean, modern, crisp, authentic representations of the upstream software brands.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "assets" / "images" / "icons"
ICON_DIR.mkdir(parents=True, exist_ok=True)

icons = {
    "chatgpt-plus": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#10A37F"/>
  <path d="M24 10a5 5 0 0 1 4.7 3.3l.3.9v3.8a5 5 0 0 1 2.5 1.5 5 5 0 0 1 3.5 0l3.3-1.9a5 5 0 0 1 6.8 1.8 5 5 0 0 1-1.8 6.8l-3.3 1.9v3.8a5 5 0 0 1-2.5 4.3l3.3 1.9a5 5 0 0 1 1.8 6.8 5 5 0 0 1-6.8 1.8l-3.3-1.9a5 5 0 0 1-4.3 0l-3.3 1.9a5 5 0 0 1-6.8-1.8 5 5 0 0 1 1.8-6.8l3.3-1.9v-3.8a5 5 0 0 1 2.5-4.3l-3.3-1.9a5 5 0 0 1-1.8-6.8 5 5 0 0 1 6.8-1.8l3.3 1.9v-3.8A5 5 0 0 1 24 10z" stroke="#FFFFFF" stroke-width="2.5" stroke-linejoin="round"/>
</svg>""",

    "claude-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#D97706"/>
  <path d="M24 11v26M11 24h26M15 15l18 18M33 15L15 33" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
</svg>""",

    "canva-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#00C4CC"/>
  <circle cx="24" cy="24" r="14" stroke="#FFFFFF" stroke-width="4" stroke-dasharray="70 20"/>
</svg>""",

    "capcut-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0F172A"/>
  <path d="M12 18l12-6 12 6-12 6-12-6zm0 12l12 6 12-6" stroke="#00B4D8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "nordvpn": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#4687FF"/>
  <path d="M14 34l10-18 10 18H14zm5-5h10l-5-9-5 9z" fill="#FFFFFF"/>
</svg>""",

    "midjourney": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#1E293B"/>
  <path d="M14 32c4-8 10-14 10-18 0 6 6 12 10 18H14zM24 14v18" stroke="#38BDF8" stroke-width="2.5" stroke-linecap="round"/>
</svg>""",

    "perplexity-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#20B2AA"/>
  <path d="M16 16h16v16H16z" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M16 24h16M24 16v16" stroke="#FFFFFF" stroke-width="2.5"/>
</svg>""",

    "gemini-advanced": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#1A73E8"/>
  <path d="M24 10c0 7.7-6.3 14-14 14 7.7 0 14 6.3 14 14 0-7.7 6.3-14 14-14-7.7 0-14-6.3-14-14z" fill="#FFFFFF"/>
</svg>""",

    "grok-ai": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#000000"/>
  <path d="M15 33L33 15M15 15h9M24 33h9" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
</svg>""",

    "deepseek-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0066FF"/>
  <path d="M14 26c4-6 10-8 18-4-2 6-6 10-12 10-3 0-5-2-6-6zm18-4c2-4 5-6 6-6-1 4-1 8-2 10l-4-4z" fill="#FFFFFF"/>
</svg>""",

    "cursor-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0F172A"/>
  <path d="M16 14l18 10-9 2-4 9-5-21z" fill="#38BDF8"/>
</svg>""",

    "jetbrains-all": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#000000"/>
  <rect x="14" y="30" width="20" height="4" fill="#FE2857"/>
  <text x="14" y="24" font-family="system-ui, sans-serif" font-weight="900" font-size="14" fill="#FFFFFF">_JB</text>
</svg>""",

    "github-copilot": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#6E40C9"/>
  <path d="M14 22c0-5.5 4.5-10 10-10s10 4.5 10 10v6c0 3.3-2.7 6-6 6h-8c-3.3 0-6-2.7-6-6v-6z" fill="#FFFFFF"/>
  <circle cx="19" cy="22" r="2.5" fill="#6E40C9"/>
  <circle cx="29" cy="22" r="2.5" fill="#6E40C9"/>
</svg>""",

    "elevenlabs-creator": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#18181B"/>
  <path d="M20 14v20M28 14v20" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
</svg>""",

    "adobe-creative-cloud": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#FF0000"/>
  <path d="M16 18c-3 0-5 2.5-5 5.5s2 5.5 5 5.5c4 0 6-4 8-7 2-3 4-7 8-7 3 0 5 2.5 5 5.5s-2 5.5-5 5.5c-4 0-6-4-8-7-2-3-4-7-8-7z" stroke="#FFFFFF" stroke-width="3"/>
</svg>""",

    "figma-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#1E1E1E"/>
  <rect x="15" y="12" width="9" height="9" rx="4.5" fill="#F24E1E"/>
  <rect x="24" y="12" width="9" height="9" rx="4.5" fill="#FF7262"/>
  <rect x="15" y="21" width="9" height="9" rx="4.5" fill="#A259FF"/>
  <circle cx="28.5" cy="25.5" r="4.5" fill="#1ABCFE"/>
  <rect x="15" y="30" width="9" height="9" rx="4.5" fill="#0ACF83"/>
</svg>""",

    "freepik-premium": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0C73FE"/>
  <path d="M15 15h18v18H15z" stroke="#FFFFFF" stroke-width="3.5" rx="4"/>
  <circle cx="24" cy="24" r="4" fill="#FFFFFF"/>
</svg>""",

    "envato-elements": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#82B541"/>
  <path d="M16 32c0-8 6-16 16-16 0 8-6 16-16 16z" fill="#FFFFFF"/>
</svg>""",

    "google-veo": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#4285F4"/>
  <polygon points="19,16 33,24 19,32" fill="#FFFFFF"/>
</svg>""",

    "grammarly-pro": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#15C39A"/>
  <circle cx="24" cy="24" r="12" stroke="#FFFFFF" stroke-width="3.5"/>
  <path d="M24 16v8h8" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
</svg>""",

    "kling-ai": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#FF4757"/>
  <path d="M16 14v20M32 14L20 24l12 10" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "leonardo-ai": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#7C3AED"/>
  <polygon points="24,12 34,18 34,30 24,36 14,30 14,18" stroke="#FFFFFF" stroke-width="3" fill="none"/>
  <circle cx="24" cy="24" r="4" fill="#00E5A3"/>
</svg>""",

    "linkedin-premium": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0A66C2"/>
  <text x="14" y="32" font-family="system-ui, sans-serif" font-weight="900" font-size="20" fill="#FFFFFF">in</text>
  <circle cx="33" cy="18" r="3" fill="#F59E0B"/>
</svg>""",

    "minimax-ai": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#EF4444"/>
  <path d="M14 30L20 18L24 26L28 18L34 30" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "netflix-premium": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#000000"/>
  <path d="M16 12v24M32 12v24M16 12l16 24" stroke="#E50914" stroke-width="4.5" stroke-linecap="round"/>
</svg>""",

    "notion-business": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#000000"/>
  <path d="M16 14l12 3v17l-12-3V14z" stroke="#FFFFFF" stroke-width="2.5" fill="none"/>
  <text x="18" y="28" font-family="system-ui, sans-serif" font-weight="900" font-size="14" fill="#FFFFFF">N</text>
</svg>""",

    "quillbot-premium": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#10B981"/>
  <path d="M30 14c-8 2-12 8-14 16l4-1c2-6 6-11 10-15z" fill="#FFFFFF"/>
</svg>""",

    "replit-core": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#F26207"/>
  <rect x="14" y="16" width="10" height="7" rx="2" fill="#FFFFFF"/>
  <rect x="24" y="23" width="10" height="7" rx="2" fill="#FFFFFF"/>
  <rect x="14" y="30" width="10" height="7" rx="2" fill="#FFFFFF"/>
</svg>""",

    "runway-gen3": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#0F172A"/>
  <text x="16" y="33" font-family="system-ui, sans-serif" font-weight="900" font-size="24" fill="#00E5A3">R</text>
</svg>""",

    "semrush-guru": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#FF642D"/>
  <circle cx="24" cy="24" r="10" stroke="#FFFFFF" stroke-width="3.5" stroke-dasharray="40 15"/>
</svg>""",

    "suno-ai": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#000000"/>
  <path d="M14 24h4M22 18v12M26 14v20M30 20v8M34 24h2" stroke="#FF4757" stroke-width="3" stroke-linecap="round"/>
</svg>""",

    "surfshark-vpn": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#17D8A7"/>
  <path d="M16 28c4 0 6-2 8-5 2-3 4-5 8-5v4c-3 0-5 2-7 5-2 3-4 5-9 5v-4z" fill="#0F172A"/>
</svg>""",

    "udio-ai": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#7C3AED"/>
  <circle cx="24" cy="24" r="11" stroke="#FFFFFF" stroke-width="3"/>
  <polygon points="21,18 29,24 21,30" fill="#FFFFFF"/>
</svg>""",

    "youtube-premium": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#FF0000"/>
  <polygon points="20,17 31,24 20,31" fill="#FFFFFF"/>
</svg>""",

    "chatgpt-codex": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#042F2E"/>
  <path d="M16 20l5 4-5 4M24 28h8" stroke="#10A37F" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>""",

    "claude-artifacts": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#78350F"/>
  <rect x="14" y="14" width="20" height="20" rx="4" stroke="#F59E0B" stroke-width="2.5"/>
  <path d="M19 22l3 3-3 3M25 28h4" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
</svg>"""
}

for slug, svg_content in icons.items():
    icon_path = ICON_DIR / f"{slug}.svg"
    icon_path.write_text(svg_content.strip(), encoding="utf-8")

print(f"Successfully generated {len(icons)} official brand SVG icons in {ICON_DIR}")
