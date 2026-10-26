import re
import sys

INDEX_FILE = r'c:\Users\Dell\Desktop\aidigitools\index.html'

with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'(<div class="grid" id="toolsGrid">)(.*?)(</div>\s*</section>)', html, re.DOTALL)
if not m:
    print("Could not find toolsGrid in index.html")
    sys.exit(1)

pre_grid = m.group(1)
grid_content = m.group(2)
post_grid = m.group(3)

raw_cards = grid_content.split('<div class="card tool-card"')
cards_by_slug = {}

for c in raw_cards[1:]:
    full_card = '<div class="card tool-card"' + c
    link_m = re.search(r'href="tools/([^"]+)\.html"', c)
    if link_m:
        slug = link_m.group(1)
        cards_by_slug[slug] = full_card.strip()

print(f"Extracted {len(cards_by_slug)} tool cards.")

# Strict professional priority ranking
RANKING_ORDER = [
    # --- TIER 1: ELITE BESTSELLERS (Top 12) ---
    ("chatgpt-plus", "🔥 #1 Pro Choice", "rgba(16, 185, 129, 0.12)", "#047857"),
    ("claude-pro", "⭐ #2 Reasoning", "rgba(67, 97, 238, 0.12)", "#3730A3"),
    ("canva-pro", "🎨 #3 Design & Stock", "rgba(245, 158, 11, 0.12)", "#B45309"),
    ("capcut-pro", "🎬 #4 Video Editing", "rgba(239, 68, 68, 0.12)", "#B91C1C"),
    ("midjourney", "🖼️ #5 AI Image", "rgba(139, 92, 246, 0.12)", "#6D28D9"),
    ("cursor-pro", "⚡ #6 AI Code Editor", "rgba(14, 165, 233, 0.12)", "#0369A1"),
    ("adobe-creative-cloud", "🖌️ #7 Creative Suite", "rgba(220, 38, 38, 0.12)", "#991B1B"),
    ("youtube-premium", "🍿 #8 Ad-Free Video", "rgba(220, 38, 38, 0.12)", "#B91C1C"),
    ("netflix-premium", "📺 #9 4K UHD Movies", "rgba(229, 9, 20, 0.12)", "#B91C1C"),
    ("perplexity-pro", "🧠 #10 Pro Search", "rgba(16, 185, 129, 0.12)", "#047857"),
    ("elevenlabs-creator", "🎙️ #11 Voice AI", "rgba(79, 70, 229, 0.12)", "#4338CA"),
    ("github-copilot", "💻 #12 Dev Assistant", "rgba(30, 41, 59, 0.12)", "#1E293B"),

    # --- TIER 2: DEVELOPER, CYBER & CREATIVE FLAGSHIPS (#13 - #24) ---
    ("nordvpn", "🛡️ #13 Privacy VPN", "rgba(59, 130, 246, 0.12)", "#1D4ED8"),
    ("surfshark-vpn", "🔒 #14 High-Speed VPN", "rgba(6, 182, 212, 0.12)", "#0E7490"),
    ("deepseek-pro", "🚀 #15 Open Reasoning", "rgba(99, 102, 241, 0.12)", "#4338CA"),
    ("gemini-advanced", "✨ #16 Multimodal AI", "rgba(59, 130, 246, 0.12)", "#1D4ED8"),
    ("runway-gen3", "🎥 #17 Video Motion", "rgba(168, 85, 247, 0.12)", "#7E22CE"),
    ("suno-ai", "🎵 #18 Music Creation", "rgba(236, 72, 153, 0.12)", "#BE185D"),
    ("jetbrains-all", "⚙️ #19 Dev Suite", "rgba(249, 115, 22, 0.12)", "#C2410C"),
    ("notion-business", "📝 #20 Workspace AI", "rgba(100, 116, 139, 0.12)", "#334155"),
    ("figma-pro", "📐 #21 UI/UX Design", "rgba(244, 63, 94, 0.12)", "#BE123C"),
    ("freepik-premium", "📂 #22 Stock Vectors", "rgba(14, 165, 233, 0.12)", "#0369A1"),
    ("envato-elements", "📦 #23 Unlimited Assets", "rgba(34, 197, 94, 0.12)", "#15803D"),
    ("replit-core", "☁️ #24 Cloud IDE", "rgba(249, 115, 22, 0.12)", "#C2410C"),

    # --- TIER 3: PRODUCTIVITY, SEO & MEDIA (#25 - #36) ---
    ("grammarly-pro", "✍️ #25 Writing Assistant", "rgba(34, 197, 94, 0.12)", "#15803D"),
    ("quillbot-premium", "🔄 #26 Paraphraser", "rgba(16, 185, 129, 0.12)", "#047857"),
    ("linkedin-premium", "💼 #27 Career Pro", "rgba(10, 102, 194, 0.12)", "#0A66C2"),
    ("semrush-guru", "📊 #28 SEO Analytics", "rgba(255, 100, 45, 0.12)", "#C2410C"),
    ("kling-ai", "🎞️ #29 Cinematic AI", "rgba(168, 85, 247, 0.12)", "#7E22CE"),
    ("minimax-ai", "📽️ #30 Video Studio", "rgba(236, 72, 153, 0.12)", "#BE185D"),
    ("udio-ai", "🎧 #31 Studio Audio", "rgba(139, 92, 246, 0.12)", "#6D28D9"),
    ("google-veo", "🎬 #32 DeepMind Video", "rgba(59, 130, 246, 0.12)", "#1D4ED8"),
    ("leonardo-ai", "🖌️ #33 Visual Canvas", "rgba(234, 88, 12, 0.12)", "#C2410C"),
    ("grok-ai", "⚡ #34 Real-Time Search", "rgba(15, 23, 42, 0.12)", "#0F172A"),
    ("chatgpt-codex", "💻 #35 Dev API Tokens", "rgba(16, 185, 129, 0.12)", "#047857"),
    ("claude-artifacts", "🧩 #36 Code Canvas", "rgba(67, 97, 238, 0.12)", "#3730A3")
]

ordered_cards = []
for slug, badge_text, bg, fg in RANKING_ORDER:
    if slug in cards_by_slug:
        card = cards_by_slug[slug]
        # Check if rank badge already present
        if 'class="tool-rank-badge"' not in card:
            # Insert rank badge right after <div class="tool-card-header">
            badge_html = f'<span class="tool-rank-badge" style="background: {bg}; color: {fg}; font-weight: 700; font-size: 0.72rem; padding: 0.22rem 0.6rem; border-radius: 9999px; border: 1px solid {bg}; letter-spacing: 0.02em;">{badge_text}</span>\n              '
            card = card.replace('<div class="tool-card-header">', '<div class="tool-card-header">\n              ' + badge_html, 1)
        ordered_cards.append("        " + card)
    else:
        print(f"Warning: slug {slug} not found in cards_by_slug!")

# Check if any cards were missed
missing_slugs = set(cards_by_slug.keys()) - set([r[0] for r in RANKING_ORDER])
if missing_slugs:
    print(f"Adding unranked slugs: {missing_slugs}")
    for slug in missing_slugs:
        ordered_cards.append("        " + cards_by_slug[slug])

new_grid_content = "\n\n" + "\n\n".join(ordered_cards) + "\n      "
new_html = html[:m.start(2)] + new_grid_content + html[m.end(2):]

with open(INDEX_FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully reordered index.html tool cards with professional ranking!")
