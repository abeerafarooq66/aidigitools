# scripts/setup_brand_logos.py
import os
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logos_dir = os.path.join(base_dir, "assets", "product-logos")
os.makedirs(logos_dir, exist_ok=True)

# 4 new SVG vector logos for candidate brands
additional_logos = {
    "spotify.svg": '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#1DB954"/>
  <path d="M34 19.5c-4.8-2.8-12.7-3.1-17.3-1.7-.7.2-1.5-.2-1.7-.9-.2-.7.2-1.5.9-1.7 5.2-1.6 14-1.2 19.5 2 .7.4.9 1.3.5 2-.4.7-1.3.9-1.9.3zm-.3 5.4c-.4.6-1.2.8-1.8.4-4-2.5-10.1-3.2-14.8-1.7-.7.2-1.4-.2-1.6-.9-.2-.7.2-1.4.9-1.6 5.4-1.6 12.2-.9 16.8 2 .6.4.8 1.2.5 1.8zm-2.1 5.3c-.3.5-.9.7-1.4.3-3.5-2.1-7.9-2.6-13.1-1.4-.6.1-1.1-.3-1.3-.8-.1-.6.3-1.1.8-1.3 5.7-1.3 10.6-.7 14.5 1.7.5.3.7.9.5 1.5z" fill="#FFFFFF"/>
</svg>''',
    "duolingo.svg": '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#58CC02"/>
  <circle cx="18" cy="22" r="5" fill="#FFFFFF"/>
  <circle cx="30" cy="22" r="5" fill="#FFFFFF"/>
  <circle cx="18" cy="22" r="2.5" fill="#4B4B4B"/>
  <circle cx="30" cy="22" r="2.5" fill="#4B4B4B"/>
  <polygon points="24,24 21,30 27,30" fill="#FF9600"/>
</svg>''',
    "discord.svg": '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#5865F2"/>
  <path d="M33.2 16.5a16.8 16.8 0 0 0-4.2-1.3.2.2 0 0 0-.2.1c-.2.3-.4.8-.5 1.2a15.5 15.5 0 0 0-8.6 0 11.2 11.2 0 0 0-.6-1.2.2.2 0 0 0-.2-.1 16.8 16.8 0 0 0-4.2 1.3.2.2 0 0 0-.1.1C12 20.6 11.2 24.6 11.6 28.5a.2.2 0 0 0 .1.2 17 17 0 0 0 5.1 2.6.2.2 0 0 0 .3-.1c.4-.6.8-1.2 1.1-1.8a.2.2 0 0 0-.1-.3 11.2 11.2 0 0 1-1.6-.8.2.2 0 0 1 0-.3c.1-.1.3-.2.4-.3a12.2 12.2 0 0 0 14.4 0c.1.1.3.2.4.3a.2.2 0 0 1 0 .3c-.5.3-1 .6-1.6.8a.2.2 0 0 0-.1.3c.4.6.8 1.2 1.1 1.8a.2.2 0 0 0 .3.1 17 17 0 0 0 5.1-2.6.2.2 0 0 0 .1-.2c.5-4.5-.8-8.5-3.1-11.9a.2.2 0 0 0-.1-.1zM19.5 24.8c-1 0-1.8-.9-1.8-2s.8-2 1.8-2c1 0 1.8.9 1.8 2s-.8 2-1.8 2zm9 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2c1 0 1.8.9 1.8 2s-.8 2-1.8 2z" fill="#FFFFFF"/>
</svg>''',
    "zoom.svg": '''<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="48" height="48" rx="12" fill="#2D8CFF"/>
  <rect x="12" y="16" width="16" height="16" rx="3" fill="#FFFFFF"/>
  <polygon points="30,20 36,16 36,32 30,28" fill="#FFFFFF"/>
</svg>'''
}

for filename, content in additional_logos.items():
    path = os.path.join(logos_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Map 40 brands
brand_manifest = [
    {"brand_id": "openai", "canonical_name": "OpenAI (ChatGPT)", "slug": "chatgpt-plus", "official_domain": "openai.com", "logo_file": "assets/product-logos/chatgpt-plus.svg", "category": "AI Chat & Writing"},
    {"brand_id": "openai-codex", "canonical_name": "OpenAI Codex", "slug": "chatgpt-codex", "official_domain": "openai.com", "logo_file": "assets/product-logos/chatgpt-codex.svg", "category": "AI Coding"},
    {"brand_id": "anthropic", "canonical_name": "Anthropic (Claude)", "slug": "claude-pro", "official_domain": "anthropic.com", "logo_file": "assets/product-logos/claude-pro.svg", "category": "AI Chat & Writing"},
    {"brand_id": "anthropic-artifacts", "canonical_name": "Claude Artifacts", "slug": "claude-artifacts", "official_domain": "anthropic.com", "logo_file": "assets/product-logos/claude-artifacts.svg", "category": "AI Coding"},
    {"brand_id": "canva", "canonical_name": "Canva", "slug": "canva-pro", "official_domain": "canva.com", "logo_file": "assets/product-logos/canva-pro.svg", "category": "Design & Creative"},
    {"brand_id": "capcut", "canonical_name": "CapCut", "slug": "capcut-pro", "official_domain": "capcut.com", "logo_file": "assets/product-logos/capcut-pro.svg", "category": "AI Video & Audio"},
    {"brand_id": "google-youtube", "canonical_name": "YouTube", "slug": "youtube-premium", "official_domain": "youtube.com", "logo_file": "assets/product-logos/youtube-premium.svg", "category": "Streaming & Entertainment"},
    {"brand_id": "google-gemini", "canonical_name": "Google Gemini", "slug": "gemini-advanced", "official_domain": "gemini.google.com", "logo_file": "assets/product-logos/gemini-advanced.svg", "category": "AI Chat & Writing"},
    {"brand_id": "google-veo", "canonical_name": "Google Veo", "slug": "google-veo", "official_domain": "deepmind.google", "logo_file": "assets/product-logos/google-veo.svg", "category": "AI Video & Audio"},
    {"brand_id": "midjourney", "canonical_name": "Midjourney", "slug": "midjourney", "official_domain": "midjourney.com", "logo_file": "assets/product-logos/midjourney.svg", "category": "AI Image"},
    {"brand_id": "cursor", "canonical_name": "Cursor", "slug": "cursor-pro", "official_domain": "cursor.com", "logo_file": "assets/product-logos/cursor-pro.svg", "category": "AI Coding"},
    {"brand_id": "deepseek", "canonical_name": "DeepSeek", "slug": "deepseek-pro", "official_domain": "deepseek.com", "logo_file": "assets/product-logos/deepseek-pro.svg", "category": "AI Chat & Writing"},
    {"brand_id": "elevenlabs", "canonical_name": "ElevenLabs", "slug": "elevenlabs-creator", "official_domain": "elevenlabs.io", "logo_file": "assets/product-logos/elevenlabs-creator.svg", "category": "AI Video & Audio"},
    {"brand_id": "figma", "canonical_name": "Figma", "slug": "figma-pro", "official_domain": "figma.com", "logo_file": "assets/product-logos/figma-pro.svg", "category": "Design & Creative"},
    {"brand_id": "github", "canonical_name": "GitHub Copilot", "slug": "github-copilot", "official_domain": "github.com", "logo_file": "assets/product-logos/github-copilot.svg", "category": "AI Coding"},
    {"brand_id": "grammarly", "canonical_name": "Grammarly", "slug": "grammarly-pro", "official_domain": "grammarly.com", "logo_file": "assets/product-logos/grammarly-pro.svg", "category": "Productivity"},
    {"brand_id": "xai-grok", "canonical_name": "xAI Grok", "slug": "grok-ai", "official_domain": "x.ai", "logo_file": "assets/product-logos/grok-ai.svg", "category": "AI Chat & Writing"},
    {"brand_id": "jetbrains", "canonical_name": "JetBrains", "slug": "jetbrains-all", "official_domain": "jetbrains.com", "logo_file": "assets/product-logos/jetbrains-all.svg", "category": "AI Coding"},
    {"brand_id": "kling", "canonical_name": "Kling AI", "slug": "kling-ai", "official_domain": "klingai.com", "logo_file": "assets/product-logos/kling-ai.svg", "category": "AI Video & Audio"},
    {"brand_id": "leonardo", "canonical_name": "Leonardo AI", "slug": "leonardo-ai", "official_domain": "leonardo.ai", "logo_file": "assets/product-logos/leonardo-ai.svg", "category": "AI Image"},
    {"brand_id": "linkedin", "canonical_name": "LinkedIn Learning & Premium", "slug": "linkedin-premium", "official_domain": "linkedin.com", "logo_file": "assets/product-logos/linkedin-premium.svg", "category": "Productivity"},
    {"brand_id": "minimax", "canonical_name": "MiniMax AI (Hailuo)", "slug": "minimax-ai", "official_domain": "minimax.io", "logo_file": "assets/product-logos/minimax-ai.svg", "category": "AI Video & Audio"},
    {"brand_id": "netflix", "canonical_name": "Netflix", "slug": "netflix-premium", "official_domain": "netflix.com", "logo_file": "assets/product-logos/netflix-premium.svg", "category": "Streaming & Entertainment"},
    {"brand_id": "nordvpn", "canonical_name": "NordVPN", "slug": "nordvpn", "official_domain": "nordvpn.com", "logo_file": "assets/product-logos/nordvpn.svg", "category": "VPN & Privacy"},
    {"brand_id": "notion", "canonical_name": "Notion", "slug": "notion-business", "official_domain": "notion.so", "logo_file": "assets/product-logos/notion-business.svg", "category": "Productivity"},
    {"brand_id": "perplexity", "canonical_name": "Perplexity AI", "slug": "perplexity-pro", "official_domain": "perplexity.ai", "logo_file": "assets/product-logos/perplexity-pro.svg", "category": "AI Chat & Writing"},
    {"brand_id": "quillbot", "canonical_name": "QuillBot", "slug": "quillbot-premium", "official_domain": "quillbot.com", "logo_file": "assets/product-logos/quillbot-premium.svg", "category": "AI Chat & Writing"},
    {"brand_id": "replit", "canonical_name": "Replit", "slug": "replit-core", "official_domain": "replit.com", "logo_file": "assets/product-logos/replit-core.svg", "category": "AI Coding"},
    {"brand_id": "runway", "canonical_name": "Runway Gen-3", "slug": "runway-gen3", "official_domain": "runwayml.com", "logo_file": "assets/product-logos/runway-gen3.svg", "category": "AI Video & Audio"},
    {"brand_id": "semrush", "canonical_name": "SEMrush", "slug": "semrush-guru", "official_domain": "semrush.com", "logo_file": "assets/product-logos/semrush-guru.svg", "category": "Productivity"},
    {"brand_id": "suno", "canonical_name": "Suno AI", "slug": "suno-ai", "official_domain": "suno.com", "logo_file": "assets/product-logos/suno-ai.svg", "category": "AI Video & Audio"},
    {"brand_id": "surfshark", "canonical_name": "Surfshark VPN", "slug": "surfshark-vpn", "official_domain": "surfshark.com", "logo_file": "assets/product-logos/surfshark-vpn.svg", "category": "VPN & Privacy"},
    {"brand_id": "udio", "canonical_name": "Udio AI", "slug": "udio-ai", "official_domain": "udio.com", "logo_file": "assets/product-logos/udio-ai.svg", "category": "AI Video & Audio"},
    {"brand_id": "adobe", "canonical_name": "Adobe Creative Cloud", "slug": "adobe-creative-cloud", "official_domain": "adobe.com", "logo_file": "assets/product-logos/adobe-creative-cloud.svg", "category": "Design & Creative"},
    {"brand_id": "envato", "canonical_name": "Envato Elements", "slug": "envato-elements", "official_domain": "elements.envato.com", "logo_file": "assets/product-logos/envato-elements.svg", "category": "Design & Creative"},
    {"brand_id": "freepik", "canonical_name": "Freepik", "slug": "freepik-premium", "official_domain": "freepik.com", "logo_file": "assets/product-logos/freepik-premium.svg", "category": "Design & Creative"},
    # 4 New Verified Candidate Brands:
    {"brand_id": "spotify", "canonical_name": "Spotify", "slug": "spotify-premium", "official_domain": "spotify.com", "logo_file": "assets/product-logos/spotify.svg", "category": "Streaming & Entertainment"},
    {"brand_id": "duolingo", "canonical_name": "Duolingo", "slug": "duolingo-super", "official_domain": "duolingo.com", "logo_file": "assets/product-logos/duolingo.svg", "category": "Productivity"},
    {"brand_id": "discord", "canonical_name": "Discord", "slug": "discord-nitro", "official_domain": "discord.com", "logo_file": "assets/product-logos/discord.svg", "category": "Productivity"},
    {"brand_id": "zoom", "canonical_name": "Zoom", "slug": "zoom-workplace", "official_domain": "zoom.us", "logo_file": "assets/product-logos/zoom.svg", "category": "Productivity"}
]

manifest_data = {
    "total_brands": len(brand_manifest),
    "asset_directory": "assets/product-logos",
    "verification_date": "2026-10-25",
    "brands": brand_manifest
}

manifest_path = os.path.join(logos_dir, "brand_logos_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2)

print(f"Setup complete! {len(brand_manifest)} brand logos registered in {manifest_path}")
