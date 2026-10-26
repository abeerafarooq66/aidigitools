"""
Refined catalog generator for all 36 AIDigiTools products.
Ensures pristine brand names, exact prices, category groupings, and official icons.
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"

DISPLAY_NAMES = {
    "adobe-creative-cloud": "Adobe Creative Cloud",
    "canva-pro": "Canva Pro",
    "capcut-pro": "CapCut Pro",
    "chatgpt-codex": "OpenAI API & Codex",
    "chatgpt-plus": "ChatGPT Plus",
    "claude-artifacts": "Claude Artifacts Pro",
    "claude-pro": "Claude Pro",
    "cursor-pro": "Cursor Pro",
    "deepseek-pro": "DeepSeek R1 / V3 Pro",
    "elevenlabs-creator": "ElevenLabs Creator",
    "envato-elements": "Envato Elements",
    "figma-pro": "Figma Pro",
    "freepik-premium": "Freepik Premium",
    "gemini-advanced": "Google Gemini Advanced",
    "github-copilot": "GitHub Copilot Pro",
    "google-veo": "Google Veo 2 / Video FX",
    "grammarly-pro": "Grammarly Premium",
    "grok-ai": "Grok 2 / xAI SuperGrok",
    "jetbrains-all": "JetBrains All Products Pack",
    "kling-ai": "Kling AI Pro",
    "leonardo-ai": "Leonardo AI Visual Studio",
    "linkedin-premium": "LinkedIn Premium Career",
    "midjourney": "Midjourney v6.1",
    "minimax-ai": "MiniMax Hailuo AI Video",
    "netflix-premium": "Netflix 4K UHD Premium",
    "nordvpn": "NordVPN Complete",
    "notion-business": "Notion Business & AI",
    "perplexity-pro": "Perplexity Pro AI",
    "quillbot-premium": "QuillBot Premium Suite",
    "replit-core": "Replit Core Cloud IDE",
    "runway-gen3": "Runway Gen-3 Alpha",
    "semrush-guru": "Semrush Guru Platform",
    "suno-ai": "Suno AI Music v3.5",
    "surfshark-vpn": "Surfshark One VPN",
    "udio-ai": "Udio AI Music Lab",
    "youtube-premium": "YouTube Premium Ad-Free"
}

VENDORS = {
    "adobe-creative-cloud": "Adobe Creative Cloud Platform",
    "canva-pro": "Canva Design Platform",
    "capcut-pro": "ByteDance Creative Studio",
    "chatgpt-codex": "OpenAI Developer Platform",
    "chatgpt-plus": "OpenAI Enterprise Systems",
    "claude-artifacts": "Anthropic AI Systems",
    "claude-pro": "Anthropic AI Systems",
    "cursor-pro": "Anysphere AI Lab",
    "deepseek-pro": "DeepSeek AI Research",
    "elevenlabs-creator": "ElevenLabs Voice AI",
    "envato-elements": "Envato Pty Ltd",
    "figma-pro": "Figma Design Platform",
    "freepik-premium": "Freepik Company",
    "gemini-advanced": "Google DeepMind Engine",
    "github-copilot": "GitHub & Microsoft Copilot",
    "google-veo": "Google DeepMind Generative Video",
    "grammarly-pro": "Grammarly Business",
    "grok-ai": "xAI Foundation Engine",
    "jetbrains-all": "JetBrains IDE Platform",
    "kling-ai": "Kuaishou Kling AI Lab",
    "leonardo-ai": "Leonardo AI Visual Studio",
    "linkedin-premium": "LinkedIn Corporation",
    "midjourney": "Midjourney Research Lab",
    "minimax-ai": "MiniMax Hailuo Video Engine",
    "netflix-premium": "Netflix Streaming Media",
    "nordvpn": "Nord Security Technologies",
    "notion-business": "Notion Labs Inc.",
    "perplexity-pro": "Perplexity AI Systems",
    "quillbot-premium": "Learneo QuillBot Suite",
    "replit-core": "Replit Cloud Development",
    "runway-gen3": "Runway AI Motion Engine",
    "semrush-guru": "Semrush Marketing Platform",
    "suno-ai": "Suno AI Audio Systems",
    "surfshark-vpn": "Surfshark Cyber Security",
    "udio-ai": "Udio AI Music Lab",
    "youtube-premium": "YouTube & Google Inc."
}

CATEGORIES = {
    "adobe-creative-cloud": "image",
    "canva-pro": "image",
    "capcut-pro": "video",
    "chatgpt-codex": "coding",
    "chatgpt-plus": "ai",
    "claude-artifacts": "coding",
    "claude-pro": "ai",
    "cursor-pro": "coding",
    "deepseek-pro": "coding",
    "elevenlabs-creator": "video",
    "envato-elements": "image",
    "figma-pro": "image",
    "freepik-premium": "image",
    "gemini-advanced": "ai",
    "github-copilot": "coding",
    "google-veo": "video",
    "grammarly-pro": "productivity",
    "grok-ai": "ai",
    "jetbrains-all": "coding",
    "kling-ai": "video",
    "leonardo-ai": "image",
    "linkedin-premium": "productivity",
    "midjourney": "image",
    "minimax-ai": "video",
    "netflix-premium": "streaming",
    "nordvpn": "vpn",
    "notion-business": "productivity",
    "perplexity-pro": "ai",
    "quillbot-premium": "productivity",
    "replit-core": "coding",
    "runway-gen3": "video",
    "semrush-guru": "productivity",
    "suno-ai": "video",
    "surfshark-vpn": "vpn",
    "udio-ai": "video",
    "youtube-premium": "streaming"
}

CATEGORY_LABELS = {
    "ai": "AI Assistant & LLM",
    "coding": "AI Coding & Dev",
    "video": "AI Video & Audio",
    "image": "Design & Image",
    "vpn": "VPN & Privacy",
    "productivity": "Productivity & SEO",
    "streaming": "Premium Streaming"
}

DESCRIPTIONS = {
    "chatgpt-plus": "Full access to GPT-4o, Custom GPTs, Advanced Voice Mode, and DALL-E 3 image generation without foreign credit cards.",
    "claude-pro": "Claude 3.5 Sonnet with 200,000 token context window, interactive Artifacts canvas, and SWE-bench coding intelligence.",
    "capcut-pro": "Automated bilingual AI captions, 4K 60fps optical flow smoothing, background removal, and commercial music licensing.",
    "canva-pro": "100M+ premium stock assets, Magic Studio AI background remover, 1TB cloud storage, and team Brand Kits.",
    "nordvpn": "Encrypted tunnel across 6,000+ servers worldwide, Threat Protection Pro ad-blocking, and high-speed streaming support.",
    "midjourney": "Industry-benchmark photorealistic generative art, stylistic controls, character consistency, and high-res upscaling.",
    "perplexity-pro": "Pro search with real-time web citations, Claude 3.5 Sonnet and GPT-4o models, document analysis, and academic research.",
    "gemini-advanced": "Gemini 1.5 Pro with 1,000,000 token context window, integrated Google Workspace apps, and DeepMind reasoning.",
    "cursor-pro": "AI-first code editor with Claude 3.5 Sonnet agentic codebase chat, multi-file edits, and instant code prediction.",
    "deepseek-pro": "DeepSeek R1 and V3 reasoning models, open-weight reasoning breakthroughs, and high-throughput math/code solving.",
    "elevenlabs-creator": "100,000 monthly voice characters, ultra-realistic voice cloning, multilingual speech synthesis, and dubbing.",
    "adobe-creative-cloud": "Photoshop, Premiere Pro, Illustrator, After Effects, and Firefly generative credits with 100GB cloud storage.",
    "figma-pro": "Unlimited Figma design files, version history, dev mode inspect, interactive components, and team libraries.",
    "freepik-premium": "Over 150 million premium vectors, PSD mockups, AI image generation credits, and commercial licensing.",
    "envato-elements": "Unlimited downloads of website templates, Premiere project files, stock footage, sound effects, and 3D assets.",
    "github-copilot": "Inline AI code completions, GitHub Copilot Chat in VS Code and JetBrains, and pull request explanations.",
    "google-veo": "High-definition 1080p AI cinematic video generation with temporal coherence and natural language physics control.",
    "grammarly-pro": "Real-time tone adjustment, advanced sentence rewriting, plagiarism detection, and team style guides.",
    "grok-ai": "Real-time X (Twitter) multimodal search, uncensored conversational reasoning, and Aurora generative image studio.",
    "jetbrains-all": "Full commercial access to IntelliJ IDEA Ultimate, PyCharm Pro, WebStorm, CLion, Rider, and DataGrip.",
    "kling-ai": "Cinematic text-to-video and image-to-video with 1080p resolution, realistic physics, and camera motion controls.",
    "leonardo-ai": "Game asset generation, custom fine-tuned LoRA models, Canvas editor, and high-resolution creative styling.",
    "linkedin-premium": "Direct InMail messaging to recruiters, applicant insights, salary benchmarks, and 20,000+ LinkedIn Learning courses.",
    "minimax-ai": "Hailuo AI video generator delivering fluid human motion, expressive facial animation, and text-to-video fidelity.",
    "netflix-premium": "4K Ultra HD video resolution, Dolby Vision, spatial audio, and simultaneous 4-screen household streaming.",
    "notion-business": "AI automated summaries, project management boards, company wikis, meeting transcript analysis, and team spaces.",
    "quillbot-premium": "Unlimited paraphrasing modes, grammar checking, plagiarism checker, summarizer, and citation generator.",
    "replit-core": "Cloud development environments, Replit AI code assistant, persistent hosting deployments, and collaborative pair coding.",
    "runway-gen3": "Gen-3 Alpha photorealistic video generation with keyframe camera control, motion brush, and text-to-video.",
    "semrush-guru": "Competitor SEO keyword analysis, domain backlink audits, position tracking, and content marketing toolkit.",
    "suno-ai": "Full 2-minute vocal and instrumental music generation across pop, rock, electronic, orchestral, and classical genres.",
    "surfshark-vpn": "Unlimited simultaneous devices, CleanWeb ad-blocker, camouflage mode, and 3,200+ global RAM-only servers.",
    "udio-ai": "High-fidelity stereo AI music composition with nuanced vocal styling, lyric editing, and musical genre blending.",
    "youtube-premium": "Completely ad-free YouTube videos, background playback on mobile, offline video downloads, and YouTube Music.",
    "chatgpt-codex": "High-quota OpenAI API keys for GPT-4o, Codex code completion, Whisper audio transcription, and vector embeddings.",
    "claude-artifacts": "Live preview HTML, React, SVG, and Mermaid diagrams generated in Claude 3.5 Sonnet's split-screen canvas."
}

def extract_tool_info(slug, html_path):
    content = html_path.read_text(encoding="utf-8")
    
    # Clean tool display name
    name = DISPLAY_NAMES.get(slug, slug.replace("-", " ").title())
    
    # Price PKR
    pkr_match = re.search(r'Rs\.?\s*([\d,]+)\s*PKR', content)
    price_pkr = pkr_match.group(1).replace(",", "") if pkr_match else "1,500"
    
    # Price USD
    usd_match = re.search(r'\(\s*~?\$?([\d\.]+)\s*USD\s*\)', content)
    price_usd = usd_match.group(1) if usd_match else "5.50"
    
    desc = DESCRIPTIONS.get(slug, "Verified enterprise subscription with 15-minute delivery and 30-day replacement guarantee.")
            
    cat_key = CATEGORIES.get(slug, "ai")
    cat_label = CATEGORY_LABELS.get(cat_key, "AI Tool")
    vendor = VENDORS.get(slug, "Verified Provider")

    return {
        "slug": slug,
        "name": name,
        "price_pkr": price_pkr,
        "price_usd": price_usd,
        "price_display": f"Rs. {int(price_pkr):,} PKR (~${price_usd} USD)",
        "category_key": cat_key,
        "category_label": cat_label,
        "vendor": vendor,
        "description": desc,
        "url": f"tools/{slug}.html",
        "icon": f"assets/images/icons/{slug}.svg"
    }

def main():
    tools = {}
    for html_file in sorted(TOOLS_DIR.glob("*.html")):
        slug = html_file.stem
        info = extract_tool_info(slug, html_file)
        tools[slug] = info

    out_file = ROOT / "scripts" / "tools_catalog.json"
    out_file.write_text(json.dumps(tools, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Catalog successfully compiled for {len(tools)} tools into {out_file}")

if __name__ == "__main__":
    main()
