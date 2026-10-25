import os
import zlib
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
images_dir = ROOT / "assets" / "images"
images_dir.mkdir(parents=True, exist_ok=True)

# List of all 36 tools
tools_list = [
    # Hub 1
    ("chatgpt-plus", "ChatGPT Plus", "OpenAI", "2,300", "8.00", "#10a37f", "#042f2e"),
    ("claude-pro", "Claude Pro", "Anthropic", "2,500", "9.00", "#d97706", "#451a03"),
    ("perplexity-pro", "Perplexity Pro", "Perplexity AI", "2,200", "8.00", "#22d3ee", "#083344"),
    ("gemini-advanced", "Google Gemini Advanced", "Google DeepMind", "1,200", "4.50", "#3b82f6", "#172554"),
    ("grok-ai", "Grok AI Super", "xAI", "1,100", "4.00", "#f43f5e", "#4c0519"),
    ("deepseek-pro", "DeepSeek Pro API", "DeepSeek", "1,100", "4.00", "#6366f1", "#1e1b4b"),
    # Hub 2
    ("cursor-pro", "Cursor AI Pro", "Anysphere", "3,800", "14.00", "#8b5cf6", "#2e1065"),
    ("jetbrains-all", "JetBrains All Products", "JetBrains", "2,500", "9.00", "#ec4899", "#500724"),
    ("github-copilot", "GitHub Copilot", "GitHub", "1,500", "5.50", "#a855f7", "#3b0764"),
    ("replit-core", "Replit Core", "Replit", "2,800", "10.00", "#f97316", "#431407"),
    ("claude-artifacts", "Claude Code Developer", "Anthropic", "1,200", "4.50", "#eab308", "#422006"),
    ("chatgpt-codex", "OpenAI API & Codex", "OpenAI", "600", "2.50", "#10b981", "#022c22"),
    # Hub 3
    ("canva-pro", "Canva Pro", "Canva", "600", "2.50", "#06b6d4", "#083344"),
    ("adobe-creative-cloud", "Adobe Creative Cloud", "Adobe", "1,400", "5.50", "#ef4444", "#450a0a"),
    ("figma-pro", "Figma Pro", "Figma", "1,800", "6.50", "#8b5cf6", "#2e1065"),
    ("midjourney", "Midjourney v6", "Midjourney", "2,800", "10.00", "#e0e7ff", "#1e1b4b"),
    ("freepik-premium", "Freepik Premium", "Freepik", "1,800", "6.50", "#3b82f6", "#172554"),
    ("envato-elements", "Envato Elements", "Envato", "2,600", "9.50", "#84cc16", "#1a2e05"),
    # Hub 4
    ("capcut-pro", "CapCut Pro", "Bytedance", "950", "3.50", "#06b6d4", "#083344"),
    ("google-veo", "Google Veo Omni", "Google DeepMind", "1,900", "7.00", "#3b82f6", "#172554"),
    ("runway-gen3", "Runway Gen-3 Alpha", "Runway", "1,800", "6.50", "#f43f5e", "#4c0519"),
    ("kling-ai", "Kling AI Pro", "Kuaishou", "700", "2.50", "#f59e0b", "#451a03"),
    ("minimax-ai", "MiniMax Hailuo AI", "MiniMax", "1,600", "6.00", "#ec4899", "#500724"),
    ("leonardo-ai", "Leonardo AI Pro", "Leonardo", "1,300", "5.00", "#a855f7", "#3b0764"),
    # Hub 5
    ("elevenlabs-creator", "ElevenLabs Creator", "ElevenLabs", "2,800", "10.00", "#f43f5e", "#4c0519"),
    ("suno-ai", "Suno AI Pro", "Suno", "2,600", "9.50", "#f97316", "#431407"),
    ("udio-ai", "Udio AI Pro", "Udio", "2,800", "10.00", "#8b5cf6", "#2e1065"),
    ("grammarly-pro", "Grammarly Pro", "Grammarly", "750", "2.80", "#10b981", "#022c22"),
    ("quillbot-premium", "QuillBot Premium", "QuillBot", "1,600", "6.00", "#22c55e", "#052e16"),
    ("semrush-guru", "Semrush Guru", "Semrush", "2,500", "9.00", "#f97316", "#431407"),
    # Hub 6
    ("nordvpn", "NordVPN Complete", "Nord Security", "850", "3.00", "#3b82f6", "#172554"),
    ("surfshark-vpn", "Surfshark VPN", "Surfshark", "800", "3.00", "#06b6d4", "#083344"),
    ("notion-business", "Notion Business AI", "Notion Labs", "1,400", "5.00", "#f8fafc", "#0f172a"),
    ("linkedin-premium", "LinkedIn Premium", "LinkedIn", "1,500", "5.50", "#0284c7", "#082f49"),
    ("youtube-premium", "YouTube Premium", "Google", "750", "2.80", "#ef4444", "#450a0a"),
    ("netflix-premium", "Netflix 4K UHD", "Netflix", "1,100", "4.00", "#e11d48", "#4c0519")
]

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def create_gradient_png(width, height, primary_hex, secondary_hex):
    r1, g1, b1 = hex_to_rgb(primary_hex)
    r2, g2, b2 = hex_to_rgb(secondary_hex)
    
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    ihdr = struct.pack('>I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('>I', ihdr_crc)

    raw_data = bytearray()
    
    # Border thickness: 12px
    border_px = 12
    card_border_px = 50
    
    for y in range(height):
        row = bytearray(b'\x00')
        t_y = y / height
        for x in range(width):
            t_x = x / width
            
            # Outer decorative border
            if x < border_px or x >= width - border_px or y < border_px or y >= height - border_px:
                r, g, b = r1, g1, b1
            # Inner card border
            elif (x == card_border_px or x == width - card_border_px) and (card_border_px <= y <= height - card_border_px):
                r, g, b = r1, g1, b1
            elif (y == card_border_px or y == height - card_border_px) and (card_border_px <= x <= width - card_border_px):
                r, g, b = r1, g1, b1
            # Center subtle badge box
            elif 260 <= y <= 370 and 200 <= x <= width - 200:
                if y == 260 or y == 370 or x == 200 or x == width - 200:
                    r, g, b = r1, g1, b1
                else:
                    # Badge background
                    r, g, b = int(r1 * 0.25 + 15), int(g1 * 0.25 + 23), int(b1 * 0.25 + 42)
            else:
                # Deep sleek background gradient with subtle color tinge
                bg_t = (t_x + t_y) * 0.5
                r = int(12 + (r2 * 0.15) * bg_t)
                g = int(17 + (g2 * 0.15) * bg_t)
                b = int(28 + (b2 * 0.15) * bg_t)
            
            row.extend((r, g, b))
        raw_data.extend(row)

    compressed = zlib.compress(bytes(raw_data), 6)
    idat_crc = zlib.crc32(b'IDAT' + compressed)
    idat = struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', idat_crc)

    iend = struct.pack('>I', 0) + b'IEND' + struct.pack('>I', zlib.crc32(b'IEND'))
    return b'\x89PNG\r\n\x1a\n' + ihdr + idat + iend

def create_svg(slug, name, brand, pkr, usd, primary_hex, secondary_hex):
    svg = f"""<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b1120" />
      <stop offset="50%" stop-color="{secondary_hex}" stop-opacity="0.6" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="15" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1200" height="630" fill="url(#bg-{slug})" />

  <!-- Outer Card Frame -->
  <rect x="40" y="40" width="1120" height="550" rx="24" fill="#0f172a" fill-opacity="0.8" stroke="{primary_hex}" stroke-width="2.5" />

  <!-- Header Branding -->
  <text x="90" y="110" font-family="system-ui, -apple-system, sans-serif" font-weight="800" font-size="28" fill="#f8fafc" letter-spacing="1">
    AIDigi<tspan fill="#eab308">Tools</tspan><tspan font-size="18" fill="#94a3b8" font-weight="500"> • Official Verified Marketplace</tspan>
  </text>
  <rect x="980" y="80" width="130" height="36" rx="18" fill="{primary_hex}" fill-opacity="0.2" stroke="{primary_hex}" stroke-width="1.5" />
  <text x="1045" y="104" font-family="system-ui, -apple-system, sans-serif" font-weight="700" font-size="14" fill="{primary_hex}" text-anchor="middle">ACTIVE STOCK</text>

  <!-- Brand Pill -->
  <rect x="90" y="180" width="220" height="38" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" />
  <text x="105" y="205" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="16" fill="#38bdf8">
    VENDOR: {brand.upper()}
  </text>

  <!-- Main Product Title -->
  <text x="90" y="285" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="58" fill="#ffffff" letter-spacing="-0.5">
    {name}
  </text>
  <text x="90" y="335" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="22" fill="#94a3b8">
    Genuine Subscription Access with Instant 15-Minute Delivery
  </text>

  <!-- Pricing Box -->
  <rect x="90" y="380" width="460" height="74" rx="14" fill="#1e293b" stroke="{primary_hex}" stroke-width="2" />
  <text x="120" y="428" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="34" fill="#f8fafc">
    Rs. {pkr} PKR <tspan font-size="22" fill="#eab308" font-weight="600">(~${usd} USD) / mo</tspan>
  </text>

  <!-- Trust Badges Row -->
  <g transform="translate(90, 495)">
    <!-- Badge 1 -->
    <rect x="0" y="0" width="310" height="42" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1" />
    <text x="15" y="27" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="15" fill="#10b981">
      &#10003; 30-Day Full Replacement Warranty
    </text>
    <!-- Badge 2 -->
    <rect x="330" y="0" width="310" height="42" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1" />
    <text x="345" y="27" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="15" fill="#38bdf8">
      &#10003; EasyPaisa, Wise &amp; Crypto USDT
    </text>
    <!-- Badge 3 -->
    <rect x="660" y="0" width="360" height="42" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1" />
    <text x="675" y="27" font-family="system-ui, -apple-system, sans-serif" font-weight="600" font-size="15" fill="#eab308">
      &#10003; Worldwide &amp; Pakistan Delivery (0 PKR)
    </text>
  </g>

  <!-- Footer Watermark -->
  <text x="1110" y="565" font-family="system-ui, -apple-system, sans-serif" font-weight="500" font-size="13" fill="#64748b" text-anchor="end">
    aidigitools.tech • Islamabad, Pakistan • +92 332 6861112
  </text>
</svg>"""
    return svg

print(f"Generating PNG & SVG assets for {len(tools_list)} tools...")
for slug, name, brand, pkr, usd, p_hex, s_hex in tools_list:
    # 1. Write SVG
    svg_content = create_svg(slug, name, brand, pkr, usd, p_hex, s_hex)
    svg_path = images_dir / f"{slug}.svg"
    svg_path.write_text(svg_content, encoding="utf-8")
    
    # 2. Write PNG (1200x630 binary valid PNG)
    png_data = create_gradient_png(1200, 630, p_hex, s_hex)
    png_path = images_dir / f"{slug}.png"
    png_path.write_bytes(png_data)
    
    print(f"[OK] Generated {slug}.png ({len(png_data)} bytes) and {slug}.svg")

print(f"[SUCCESS] All {len(tools_list)} tools have both PNG and SVG assets in {images_dir}!")
