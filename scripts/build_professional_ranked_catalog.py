# scripts/build_professional_ranked_catalog.py
import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGOS_DIR = os.path.join(BASE_DIR, "assets", "product-logos")
DEST_HTML = r"C:\Users\Dell\.gemini\antigravity\brain\b9098f9b-3fdd-4d44-b502-c2981cd56d6f\aidigitools_professional_ranked_catalog_preview.html"

# Load SVGs
svg_cache = {}
for filename in os.listdir(LOGOS_DIR):
    if filename.endswith(".svg"):
        slug_name = filename.replace(".svg", "")
        with open(os.path.join(LOGOS_DIR, filename), "r", encoding="utf-8") as f:
            svg_cache[slug_name] = f.read().strip()

# 40 Professional Canonical Tools Strictly Ranked by Market Demand & Professional Utility
RANKED_CATALOG = [
    # --- TIER 1: ELITE PROFESSIONAL BESTSELLERS (Top 12) ---
    {
        "rank": 1,
        "tier": "tier-elite",
        "tier_label": "🔥 #1 Top Pro Choice",
        "slug": "chatgpt-plus",
        "name": "ChatGPT Plus & Team Workspace",
        "brand": "OpenAI",
        "category": "AI Assistant & LLM",
        "cat_key": "chat",
        "desc": "Full access to GPT-4o, OpenAI o1 high-speed reasoning, Advanced Voice Mode, Custom GPTs, Canvas interactive editor, and DALL-E 3 image generation.",
        "icon": "chatgpt-plus",
        "starting_price_pkr": 2300,
        "starting_price_usd": 8.00,
        "plans": [
            {
                "plan_id": "GPT-PLUS-1M",
                "name": "ChatGPT Plus (1 Month)",
                "type": "Personal Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2300,
                "price_usd": 8.00,
                "badge": "Best Seller",
                "features": ["GPT-4o, GPT-4, and o1 high-speed reasoning", "Advanced Voice Mode on iOS & Android", "DALL-E 3 high-res image generation", "File analysis, web browsing & custom GPTs"],
                "terms": "Personal account activation; standard OpenAI rolling rate limits apply."
            },
            {
                "plan_id": "GPT-TEAM-1M",
                "name": "ChatGPT Team Workspace (1 Month)",
                "type": "Team Workspace",
                "duration": "1 Month (30 Days)",
                "seats": "Team Shared Workspace",
                "price_pkr": 4800,
                "price_usd": 17.00,
                "badge": "Business Grade",
                "features": ["Higher message limits on GPT-4o and o1", "Dedicated collaborative workspace & admin console", "Shared custom GPTs within organization", "Zero model training on business data"],
                "terms": "Organization workspace terms apply."
            },
            {
                "plan_id": "GPT-CODEX-1M",
                "name": "OpenAI API & Codex Balance (1 Month)",
                "type": "Developer API",
                "duration": "1 Month (30 Days)",
                "seats": "Developer Tier",
                "price_pkr": 600,
                "price_usd": 2.50,
                "badge": "Dev API",
                "features": ["Pre-funded API balance for GPT-4o & embeddings", "High rate limits up to 500 RPM", "Full developer dashboard & usage metrics"],
                "terms": "Direct developer API token consumption."
            }
        ]
    },
    {
        "rank": 2,
        "tier": "tier-elite",
        "tier_label": "⭐ #2 Top Coding & Reasoning",
        "slug": "claude-pro",
        "name": "Claude Pro & Team Suite",
        "brand": "Anthropic",
        "category": "AI Assistant & LLM",
        "cat_key": "chat",
        "desc": "Claude 3.5 Sonnet with 200,000 token context window, interactive split-screen Artifacts runner, and SWE-bench #1 coding benchmark performance.",
        "icon": "claude-pro",
        "starting_price_pkr": 2500,
        "starting_price_usd": 9.00,
        "plans": [
            {
                "plan_id": "CLAUDE-PRO-1M",
                "name": "Claude Pro (1 Month)",
                "type": "Personal Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2500,
                "price_usd": 9.00,
                "badge": "Most Popular",
                "features": ["5x higher usage limits vs free tier", "Claude 3.5 Sonnet & Claude 3.5 Haiku models", "Interactive Artifacts split-screen canvas", "Early access to upcoming Anthropic features"],
                "terms": "Personal account; subject to Anthropic rolling usage limits."
            },
            {
                "plan_id": "CLAUDE-TEAM-1M",
                "name": "Claude Team Workspace (1 Month)",
                "type": "Team Workspace",
                "duration": "1 Month (30 Days)",
                "seats": "Workspace Seat",
                "price_pkr": 5200,
                "price_usd": 18.50,
                "badge": "Team Collab",
                "features": ["Higher per-user usage limits on Sonnet", "Team project spaces & centralized billing", "Shared prompt libraries & company assets", "Enterprise data privacy guarantees"],
                "terms": "Requires organization workspace setup."
            }
        ]
    },
    {
        "rank": 3,
        "tier": "tier-elite",
        "tier_label": "🎨 #3 Top Design & Marketing",
        "slug": "canva-pro",
        "name": "Canva Pro",
        "brand": "Canva",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "100M+ premium stock photos, videos, and graphics, 1-click Magic Studio AI background remover, 1TB cloud storage, and team Brand Kits.",
        "icon": "canva-pro",
        "starting_price_pkr": 600,
        "starting_price_usd": 2.50,
        "plans": [
            {
                "plan_id": "CANVA-PRO-1M",
                "name": "Canva Pro (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 600,
                "price_usd": 2.50,
                "badge": "Best Seller",
                "features": ["Unlimited 1-click Magic Background Remover", "100M+ premium stock photos, videos, graphics", "1TB secure cloud storage for brand assets", "Full Brand Kit with custom fonts & colors"],
                "terms": "Personal email upgrade; full Pro access."
            },
            {
                "plan_id": "CANVA-PRO-12M",
                "name": "Canva Pro Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 2200,
                "price_usd": 7.90,
                "badge": "Save 70%",
                "features": ["Full 12 months uninterrupted Pro access", "Unlimited Magic Studio AI tools & downloads", "Complete Brand Kit & 1TB cloud storage", "Full 365-day replacement warranty protection"],
                "terms": "Annual license; zero monthly renewal hassle."
            }
        ]
    },
    {
        "rank": 4,
        "tier": "tier-elite",
        "tier_label": "🎬 #4 Top Video Editing",
        "slug": "capcut-pro",
        "name": "CapCut Pro",
        "brand": "ByteDance / CapCut",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "Automated bilingual AI captions with word-level sync, 4K 60fps optical flow smoothing, AI body cutout, and multi-device cloud project sync.",
        "icon": "capcut-pro",
        "starting_price_pkr": 950,
        "starting_price_usd": 3.50,
        "plans": [
            {
                "plan_id": "CAPCUT-PRO-1M",
                "name": "CapCut Pro (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 950,
                "price_usd": 3.50,
                "badge": "Creator Pick",
                "features": ["Auto captions with bilingual word-level sync", "4K 60fps optical flow ultra-smooth rendering", "Smart AI body cutout & green screen remover", "100GB CapCut cloud space for multi-device sync"],
                "terms": "PC, Mac, Android, and iOS cross-sync supported."
            },
            {
                "plan_id": "CAPCUT-PRO-12M",
                "name": "CapCut Pro Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 5900,
                "price_usd": 21.00,
                "badge": "Save 48%",
                "features": ["Full 12 months uninterrupted Pro access", "Unlimited 4K exports & premium transitions", "100GB cloud project backup", "365-day replacement guarantee"],
                "terms": "Fixed term 12-month license."
            }
        ]
    },
    {
        "rank": 5,
        "tier": "tier-elite",
        "tier_label": "🖼️ #5 Top AI Image Generation",
        "slug": "midjourney",
        "name": "Midjourney v6.1",
        "brand": "Midjourney",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "State-of-the-art photorealistic AI image synthesis, texture generation, web canvas inpainting, and commercial rights.",
        "icon": "midjourney",
        "starting_price_pkr": 1800,
        "starting_price_usd": 6.50,
        "plans": [
            {
                "plan_id": "MIDJ-BASIC-1M",
                "name": "Midjourney Basic (1 Month)",
                "type": "Basic",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "badge": "Starter",
                "features": ["200 Fast GPU minutes (~200 images)", "General commercial usage terms", "Access to member web gallery", "Direct messaging bot access"],
                "terms": "Fast GPU mode only; no Relax queue."
            },
            {
                "plan_id": "MIDJ-STD-1M",
                "name": "Midjourney Standard (1 Month)",
                "type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2800,
                "price_usd": 9.99,
                "badge": "Most Popular",
                "features": ["15 Fast GPU hours (~1,000 images)", "Unlimited Relax GPU mode generation", "General commercial terms", "Web gallery & inpainting editor"],
                "terms": "Unlimited Relax mode subject to dynamic server queue."
            },
            {
                "plan_id": "MIDJ-PRO-1M",
                "name": "Midjourney Pro (1 Month)",
                "type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 5600,
                "price_usd": 20.00,
                "badge": "Agency Grade",
                "features": ["30 Fast GPU hours (~2,000 images)", "Stealth mode (keep generations private)", "Unlimited Relax GPU mode", "12 concurrent Fast jobs"],
                "terms": "Full privacy stealth generation tier."
            }
        ]
    },
    {
        "rank": 6,
        "tier": "tier-elite",
        "tier_label": "⚡ #6 Top AI Code Editor",
        "slug": "cursor-pro",
        "name": "Cursor Pro",
        "brand": "Anysphere (Cursor)",
        "category": "AI Coding & Dev",
        "cat_key": "coding",
        "desc": "AI-first code editor with Claude 3.5 Sonnet agentic codebase chat, multi-file Composer refactoring, and instant code prediction.",
        "icon": "cursor-pro",
        "starting_price_pkr": 3800,
        "starting_price_usd": 13.50,
        "plans": [
            {
                "plan_id": "CURSOR-PRO-1M",
                "name": "Cursor Pro (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 3800,
                "price_usd": 13.50,
                "badge": "Developer Choice",
                "features": ["500 Fast Premium requests / month (Claude 3.5 Sonnet & GPT-4o)", "Unlimited Slow requests after fast quota", "Multi-file Composer codebase refactoring", "Smart line and multi-line code auto-complete"],
                "terms": "Individual developer seat activation."
            },
            {
                "plan_id": "CURSOR-PRO-12M",
                "name": "Cursor Pro Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 39000,
                "price_usd": 140.00,
                "badge": "Save 15%",
                "features": ["Full 365 days of uninterrupted Fast Claude 3.5 Sonnet Composer", "Zero monthly subscription renewal friction", "Priority compute allocations during peak hours", "365-day replacement warranty support"],
                "terms": "Annual license with uninterrupted activation."
            }
        ]
    },
    {
        "rank": 7,
        "tier": "tier-elite",
        "tier_label": "🖌️ #7 Top Creative Suite",
        "slug": "adobe-creative-cloud",
        "name": "Adobe Creative Cloud",
        "brand": "Adobe",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "Photoshop, Premiere Pro, Illustrator, After Effects, InDesign, and Firefly generative credits with 100GB cloud storage.",
        "icon": "adobe-creative-cloud",
        "starting_price_pkr": 1400,
        "starting_price_usd": 5.50,
        "plans": [
            {
                "plan_id": "ADOBE-CC-1M",
                "name": "All Apps (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (2 Devices Active)",
                "price_pkr": 1400,
                "price_usd": 5.50,
                "badge": "Industry Standard",
                "features": ["Access to 20+ desktop & mobile creative apps", "Adobe Firefly AI generative credits", "100GB Adobe cloud storage", "Adobe Fonts library with 20,000+ typefaces"],
                "terms": "Active on up to 2 devices concurrently."
            },
            {
                "plan_id": "ADOBE-CC-12M",
                "name": "All Apps Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (2 Devices Active)",
                "price_pkr": 14000,
                "price_usd": 50.00,
                "badge": "Agency Value",
                "features": ["Full 12 months access to entire Creative Cloud suite", "Monthly Firefly AI credit renewals", "100GB cloud asset synchronization", "365-day replacement warranty support"],
                "terms": "Annual license with guaranteed uninterrupted activation."
            }
        ]
    },
    {
        "rank": 8,
        "tier": "tier-elite",
        "tier_label": "🍿 #8 Top Streaming & Audio",
        "slug": "youtube-premium",
        "name": "YouTube Premium Ad-Free",
        "brand": "Google / YouTube",
        "category": "Streaming & Entertainment",
        "cat_key": "streaming",
        "desc": "100% ad-free video streaming, background audio playback while multitasking, offline 1080p downloads, and YouTube Music Premium.",
        "icon": "youtube-premium",
        "starting_price_pkr": 750,
        "starting_price_usd": 2.80,
        "plans": [
            {
                "plan_id": "YT-IND-1M",
                "name": "Individual (1 Month)",
                "type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 750,
                "price_usd": 2.80,
                "badge": "Most Popular",
                "features": ["100% Ad-free video playback", "Background audio while using other apps", "Offline 1080p/4K downloads", "YouTube Music Premium included"],
                "terms": "Personal account activation; single concurrent stream."
            },
            {
                "plan_id": "YT-FAM-1M",
                "name": "Family Plan (1 Month)",
                "type": "Family",
                "duration": "1 Month (30 Days)",
                "seats": "Up to 5 Family Members",
                "price_pkr": 1450,
                "price_usd": 5.20,
                "badge": "Best Value",
                "features": ["5 Independent member profiles with private histories", "Ad-free streaming across all household devices", "5x YouTube Music Premium accounts", "Offline downloads on each member device"],
                "terms": "All members must reside in the same country/region."
            },
            {
                "plan_id": "YT-ANN-12M",
                "name": "Individual Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 7500,
                "price_usd": 27.00,
                "badge": "Save 16%",
                "features": ["Full 365 days uninterrupted ad-free playback", "Includes YouTube Music Premium for 1 year", "Zero monthly renewal friction", "Full 365-day replacement warranty guarantee"],
                "terms": "Fixed term subscription; non-transferable."
            }
        ]
    },
    {
        "rank": 9,
        "tier": "tier-elite",
        "tier_label": "📺 #9 Top Movies & 4K HDR",
        "slug": "netflix-premium",
        "name": "Netflix 4K UHD Premium",
        "brand": "Netflix",
        "category": "Streaming & Entertainment",
        "cat_key": "streaming",
        "desc": "4K Ultra HD HDR streaming, Dolby Atmos spatial audio, unlimited downloads on supported mobile devices.",
        "icon": "netflix-premium",
        "starting_price_pkr": 1100,
        "starting_price_usd": 4.00,
        "plans": [
            {
                "plan_id": "NETFLIX-1P-1M",
                "name": "1 Profile 4K UHD (1 Month)",
                "type": "Single Profile",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Profile with PIN",
                "price_pkr": 1100,
                "price_usd": 4.00,
                "badge": "Most Popular",
                "features": ["4K Ultra HD + HDR video playback", "Personal PIN-locked profile & private watch history", "Dolby Atmos immersive spatial audio", "Works on Smart TV, Phone, Laptop, and Tablet"],
                "terms": "1 screen active at any time on your dedicated profile."
            },
            {
                "plan_id": "NETFLIX-FULL-1M",
                "name": "Full Account 4K UHD (1 Month)",
                "type": "Full Account",
                "duration": "1 Month (30 Days)",
                "seats": "Full 5 Profiles Account",
                "price_pkr": 2400,
                "price_usd": 8.60,
                "badge": "Full Household",
                "features": ["Complete private account with full 5 profiles", "4 concurrent 4K UHD screens simultaneously", "Download on up to 6 supported devices", "Spatial audio on all compatible systems"],
                "terms": "Private household account activation."
            }
        ]
    },
    {
        "rank": 10,
        "tier": "tier-elite",
        "tier_label": "🎵 #10 Top Music Streaming",
        "slug": "spotify-premium",
        "name": "Spotify Premium Individual & Family",
        "brand": "Spotify",
        "category": "Streaming & Entertainment",
        "cat_key": "streaming",
        "desc": "Ad-free music streaming, 320kbps extreme audio quality, offline playlists, and unlimited song skips on all devices.",
        "icon": "spotify",
        "starting_price_pkr": 550,
        "starting_price_usd": 1.95,
        "plans": [
            {
                "plan_id": "SPOTIFY-IND-1M",
                "name": "Individual (1 Month)",
                "type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 550,
                "price_usd": 1.95,
                "badge": "Music Lover",
                "features": ["100% ad-free music listening", "Download to listen offline without internet", "320kbps high-fidelity audio bitrate", "Listen on Phone, Laptop, Smart Speaker, PlayStation"],
                "terms": "Personal Spotify account activation."
            },
            {
                "plan_id": "SPOTIFY-FAM-1M",
                "name": "Family Plan (1 Month)",
                "type": "Family",
                "duration": "1 Month (30 Days)",
                "seats": "Up to 6 Accounts",
                "price_pkr": 1150,
                "price_usd": 4.10,
                "badge": "Best Value",
                "features": ["6 individual accounts for family members living together", "Separate saved songs, playlists, and recommendations", "Spotify Kids app included", "Explicit music filter controls for parents"],
                "terms": "Family members must reside in the same household."
            }
        ]
    },
    {
        "rank": 11,
        "tier": "tier-elite",
        "tier_label": "🔍 #11 Top Research Engine",
        "slug": "perplexity-pro",
        "name": "Perplexity Pro AI",
        "brand": "Perplexity AI",
        "category": "AI Assistant & LLM",
        "cat_key": "chat",
        "desc": "Pro search with real-time web citations, Claude 3.5 Sonnet and GPT-4o models, document analysis, and academic research.",
        "icon": "perplexity-pro",
        "starting_price_pkr": 2200,
        "starting_price_usd": 8.00,
        "plans": [
            {
                "plan_id": "PERP-1M",
                "name": "Perplexity Pro (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2200,
                "price_usd": 8.00,
                "badge": "Research Gold",
                "features": ["600+ Pro Searches / day with multi-step reasoning", "Model switcher: Claude 3.5 Sonnet, GPT-4o, Sonar Large", "Unlimited file and PDF research uploads", "Includes $5/month API credits"],
                "terms": "Personal search account."
            },
            {
                "plan_id": "PERP-12M",
                "name": "Perplexity Pro Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User",
                "price_pkr": 16500,
                "price_usd": 59.00,
                "badge": "Save 37%",
                "features": ["Full 12 months uninterrupted Pro research", "All premium AI models unlocked", "Priority processing & zero search queue", "365-day replacement warranty support"],
                "terms": "Annual subscription."
            }
        ]
    },
    {
        "rank": 12,
        "tier": "tier-elite",
        "tier_label": "🎙️ #12 Top Voice AI & Cloning",
        "slug": "elevenlabs-creator",
        "name": "ElevenLabs Voice AI",
        "brand": "ElevenLabs",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "100,000 monthly voice characters, Instant Voice Cloning, commercial license rights, and 192kbps studio audio.",
        "icon": "elevenlabs-creator",
        "starting_price_pkr": 2800,
        "starting_price_usd": 10.00,
        "plans": [
            {
                "plan_id": "11LABS-CREATOR-1M",
                "name": "Creator Plan (1 Month)",
                "type": "Creator",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2800,
                "price_usd": 10.00,
                "badge": "Top Audio AI",
                "features": ["100,000 characters per month (~2 hours of audio)", "Create up to 30 custom instant voice clones", "Commercial rights for YouTube & podcasts", "192kbps ultra-high quality audio export"],
                "terms": "Unused characters do not roll over to next month."
            },
            {
                "plan_id": "11LABS-PRO-1M",
                "name": "Pro Plan (1 Month)",
                "type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 6500,
                "price_usd": 23.50,
                "badge": "Studio Pro",
                "features": ["500,000 characters per month (~10 hours of audio)", "Professional Voice Cloning (PVC) enabled", "160 custom voices & priority rendering", "Commercial rights across all broadcast media"],
                "terms": "Professional voice tier."
            }
        ]
    },

    # --- TIER 2: HIGH-DEMAND PRO DEVELOPER & CREATIVE TOOLS (Rank 13 to 24) ---
    {
        "rank": 13,
        "tier": "tier-pro",
        "tier_label": "💻 Pro Developer Tool",
        "slug": "github-copilot",
        "name": "GitHub Copilot Pro & Business",
        "brand": "GitHub / Microsoft",
        "category": "AI Coding & Dev",
        "cat_key": "coding",
        "desc": "AI pair programmer inside VS Code, Visual Studio, and JetBrains with code autocompletions and Copilot Chat.",
        "icon": "github-copilot",
        "starting_price_pkr": 1500,
        "starting_price_usd": 5.50,
        "plans": [
            {
                "plan_id": "COPILOT-IND-1M",
                "name": "Copilot Individual (1 Month)",
                "type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 1500,
                "price_usd": 5.50,
                "badge": "Coder Essential",
                "features": ["Real-time whole line & function autocompletions", "Copilot Chat in VS Code and JetBrains IDEs", "CLI command generator & code explanations", "Public code filter to avoid copyright matches"],
                "terms": "Personal GitHub account linkage."
            },
            {
                "plan_id": "COPILOT-BIZ-1M",
                "name": "Copilot Business (1 Month)",
                "type": "Business Seat",
                "duration": "1 Month (30 Days)",
                "seats": "Organization Seat",
                "price_pkr": 3200,
                "price_usd": 11.50,
                "badge": "Enterprise Dev",
                "features": ["Organization-wide policy management", "Copilot in GitHub Mobile & Pull Request summaries", "Zero data retention for model training", "Centralized seat provisioning"],
                "terms": "GitHub organization seat."
            }
        ]
    },
    {
        "rank": 14,
        "tier": "tier-pro",
        "tier_label": "🛡️ Top Cyber Privacy",
        "slug": "nordvpn",
        "name": "NordVPN Complete",
        "brand": "Nord Security",
        "category": "VPN & Privacy",
        "cat_key": "vpn",
        "desc": "6,400+ ultra-fast RAM-only servers, NordLynx WireGuard protocol, Threat Protection Pro, and 10 simultaneous devices.",
        "icon": "nordvpn",
        "starting_price_pkr": 850,
        "starting_price_usd": 3.00,
        "plans": [
            {
                "plan_id": "NORD-1M",
                "name": "Standard (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "Up to 10 Simultaneous Devices",
                "price_pkr": 850,
                "price_usd": 3.00,
                "badge": "Top Privacy",
                "features": ["Ultra-fast NordLynx protocol with zero logs", "Access to 6,400+ servers in 111 countries", "Double VPN & Onion Over VPN routing", "Threat Protection malware & ad blocking"],
                "terms": "Independent audited no-logs policy."
            },
            {
                "plan_id": "NORD-12M",
                "name": "Complete Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "Up to 10 Simultaneous Devices",
                "price_pkr": 5400,
                "price_usd": 19.50,
                "badge": "Save 47%",
                "features": ["Full 365 days secure high-speed browsing", "Includes 1TB encrypted cloud storage", "Cross-platform apps (Windows, Mac, iOS, Android)", "365-day replacement warranty coverage"],
                "terms": "Long-term privacy protection."
            }
        ]
    },
    {
        "rank": 15,
        "tier": "tier-pro",
        "tier_label": "🛡️ Unlimited Device VPN",
        "slug": "surfshark-vpn",
        "name": "Surfshark One VPN",
        "brand": "Surfshark",
        "category": "VPN & Privacy",
        "cat_key": "vpn",
        "desc": "Unlimited simultaneous devices, CleanWeb ad-blocker, camouflage mode, and 3,200+ global RAM-only servers.",
        "icon": "surfshark-vpn",
        "starting_price_pkr": 800,
        "starting_price_usd": 3.00,
        "plans": [
            {
                "plan_id": "SURF-1M",
                "name": "Starter (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "Unlimited Simultaneous Devices",
                "price_pkr": 800,
                "price_usd": 3.00,
                "badge": "Unlimited Devices",
                "features": ["Connect unlimited devices on 1 subscription", "CleanWeb 2.0 pop-up and malware blocker", "3,200+ servers across 100 countries", "Bypasser split tunneling for banking apps"],
                "terms": "Unlimited devices subject to fair usage."
            },
            {
                "plan_id": "SURF-12M",
                "name": "One Plus (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "Unlimited Simultaneous Devices",
                "price_pkr": 4800,
                "price_usd": 17.50,
                "badge": "Best Value VPN",
                "features": ["Full 12 months unlimited VPN protection", "Includes Surfshark Antivirus & Alert monitoring", "Private search engine with zero logs", "365-day replacement warranty"],
                "terms": "Annual family cyber protection."
            }
        ]
    },
    {
        "rank": 16,
        "tier": "tier-pro",
        "tier_label": "🧠 Open Reasoning AI",
        "slug": "deepseek-pro",
        "name": "DeepSeek R1 / V3 Pro",
        "brand": "DeepSeek",
        "category": "AI Assistant & LLM",
        "cat_key": "chat",
        "desc": "DeepSeek-R1 open reasoning model, V3 MoE architecture, high-token API allowances, and code generation.",
        "icon": "deepseek-pro",
        "starting_price_pkr": 1100,
        "starting_price_usd": 4.00,
        "plans": [
            {
                "plan_id": "DEEPSEEK-1M",
                "name": "R1 / V3 Pro Tier (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1100,
                "price_usd": 4.00,
                "badge": "Open Reasoning",
                "features": ["Full access to DeepSeek-R1 reasoning model", "DeepSeek-V3 MoE 671B architecture", "Zero queue delays during peak traffic", "High context coding and math capabilities"],
                "terms": "Fair usage limits apply."
            },
            {
                "plan_id": "DEEPSEEK-DEV-1M",
                "name": "Developer High-Token API Tier",
                "type": "Developer API",
                "duration": "1 Month (30 Days)",
                "seats": "Developer Organization",
                "price_pkr": 2900,
                "price_usd": 10.50,
                "badge": "Dev Scaler",
                "features": ["Pre-funded token balance for R1 and V3 API", "High concurrency limit (50 requests/sec)", "Direct OpenAI-compatible API endpoint", "Dedicated developer support"],
                "terms": "API token consumption rates apply."
            }
        ]
    },
    {
        "rank": 17,
        "tier": "tier-pro",
        "tier_label": "🌐 2M Context Window",
        "slug": "gemini-advanced",
        "name": "Google Gemini Advanced",
        "brand": "Google",
        "category": "AI Assistant & LLM",
        "cat_key": "chat",
        "desc": "Gemini 1.5 Pro with 2-million token context window, Google Workspace integration, and 2TB Google One cloud storage.",
        "icon": "gemini-advanced",
        "starting_price_pkr": 1200,
        "starting_price_usd": 4.50,
        "plans": [
            {
                "plan_id": "GEMINI-1M",
                "name": "Advanced (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1200,
                "price_usd": 4.50,
                "badge": "2M Context",
                "features": ["Gemini 1.5 Pro with 2M token context", "Deep reasoning across 1,500 pages of text", "Gemini integrated directly into Gmail & Docs", "2TB Google One cloud storage"],
                "terms": "Google account activation."
            },
            {
                "plan_id": "GEMINI-ANN-12M",
                "name": "Advanced Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 11500,
                "price_usd": 41.00,
                "badge": "Save 20%",
                "features": ["Full 365 days of 2M token Gemini 1.5 Pro", "Includes 2TB Google One cloud backup for 1 year", "Priority access to new experimental models", "Full 365-day replacement warranty"],
                "terms": "Annual Google account subscription."
            }
        ]
    },
    {
        "rank": 18,
        "tier": "tier-pro",
        "tier_label": "🎥 Cinematic AI Motion",
        "slug": "runway-gen3",
        "name": "Runway Gen-3 Alpha",
        "brand": "Runway",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "Gen-3 Alpha photorealistic video generation with keyframe camera control, motion brush, and text-to-video.",
        "icon": "runway-gen3",
        "starting_price_pkr": 1800,
        "starting_price_usd": 6.50,
        "plans": [
            {
                "plan_id": "RUNWAY-STD-1M",
                "name": "Standard (1 Month)",
                "type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "badge": "Video Filmmaker",
                "features": ["625 credits / month (~125 seconds of Gen-3 video)", "Motion Brush & camera control tools", "Export up to 4K resolution with watermark removal", "Train 1 custom voice or portrait generator"],
                "terms": "Standard generation queue."
            },
            {
                "plan_id": "RUNWAY-UNLTD-1M",
                "name": "Unlimited Plan (1 Month)",
                "type": "Unlimited",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 4900,
                "price_usd": 17.50,
                "badge": "Pro Studio",
                "features": ["Unlimited relaxed video generations", "2,250 monthly Fast credits", "Full commercial video licensing rights", "Priority enterprise rendering tier"],
                "terms": "Relaxed queue speed varies by load."
            }
        ]
    },
    {
        "rank": 19,
        "tier": "tier-pro",
        "tier_label": "🎶 AI Song & Music Studio",
        "slug": "suno-ai",
        "name": "Suno AI Music v3.5",
        "brand": "Suno AI",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "Full 2-minute vocal and instrumental music generation across pop, rock, electronic, orchestral, and classical genres.",
        "icon": "suno-ai",
        "starting_price_pkr": 2600,
        "starting_price_usd": 9.50,
        "plans": [
            {
                "plan_id": "SUNO-PRO-1M",
                "name": "Pro Plan (1 Month)",
                "type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2600,
                "price_usd": 9.50,
                "badge": "Musician Choice",
                "features": ["2,500 credits / month (~500 songs)", "General commercial terms for streaming monetization", "Priority generation queue & audio stem separation", "Upload audio clips to extend songs"],
                "terms": "Commercial terms apply while subscribed."
            },
            {
                "plan_id": "SUNO-PREM-1M",
                "name": "Premier Plan (1 Month)",
                "type": "Premier",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 6800,
                "price_usd": 24.50,
                "badge": "Pro Label",
                "features": ["10,000 credits / month (~2,000 songs)", "Maximum generation priority queue", "Full stem exports with instrumental backing tracks", "Commercial distribution on Spotify, Apple Music & YouTube"],
                "terms": "Professional music producer tier."
            }
        ]
    },
    {
        "rank": 20,
        "tier": "tier-pro",
        "tier_label": "🛠️ All 16 Developer IDEs",
        "slug": "jetbrains-all",
        "name": "JetBrains All Products Pack",
        "brand": "JetBrains",
        "category": "AI Coding & Dev",
        "cat_key": "coding",
        "desc": "Complete suite of 16 IDEs including IntelliJ IDEA Ultimate, PyCharm Pro, WebStorm, Rider, CLion, and GoLand.",
        "icon": "jetbrains-all",
        "starting_price_pkr": 2500,
        "starting_price_usd": 9.00,
        "plans": [
            {
                "plan_id": "JETBRAINS-1M",
                "name": "All Products Pack (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer (Multi-Device)",
                "price_pkr": 2500,
                "price_usd": 9.00,
                "badge": "Dev Superpack",
                "features": ["All 16 JetBrains IDEs: IntelliJ, PyCharm, WebStorm, CLion, Rider, GoLand, etc.", "Full commercial development rights", "JetBrains AI Assistant integration", "Cross-platform support on Windows, macOS & Linux"],
                "terms": "Single developer license."
            },
            {
                "plan_id": "JETBRAINS-12M",
                "name": "All Products Pack Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Developer (Multi-Device)",
                "price_pkr": 18000,
                "price_usd": 64.00,
                "badge": "Save 40%",
                "features": ["Full 365 days access to entire JetBrains product family", "Includes all major version upgrades during term", "Perpetual fallback license rights eligible", "365-day replacement warranty guarantee"],
                "terms": "Annual developer license."
            }
        ]
    },
    {
        "rank": 21,
        "tier": "tier-pro",
        "tier_label": "📝 Workspace & Wiki",
        "slug": "notion-business",
        "name": "Notion Business & AI",
        "brand": "Notion",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "AI automated summaries, project management boards, company wikis, meeting transcript analysis, and team spaces.",
        "icon": "notion-business",
        "starting_price_pkr": 1400,
        "starting_price_usd": 5.00,
        "plans": [
            {
                "plan_id": "NOTION-BIZ-1M",
                "name": "Business & AI (1 Month)",
                "type": "Business",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Workspace",
                "price_pkr": 1400,
                "price_usd": 5.00,
                "badge": "Productivity Hub",
                "features": ["Unlimited Notion AI prompts, autofill & summaries", "Unlimited page history & team collaborative spaces", "Advanced database formulas, relations & rollups", "Private team spaces & permission management"],
                "terms": "Workspace user account."
            },
            {
                "plan_id": "NOTION-ANN-12M",
                "name": "Business & AI Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Workspace",
                "price_pkr": 13500,
                "price_usd": 48.00,
                "badge": "Save 20%",
                "features": ["Full 365 days of uninterrupted Notion AI and Business capabilities", "Unlimited collaborative workspaces and page histories", "Admin audit logs & workspace export tools", "365-day replacement warranty support"],
                "terms": "Annual workspace license."
            }
        ]
    },
    {
        "rank": 22,
        "tier": "tier-pro",
        "tier_label": "📐 UI/UX Design Standard",
        "slug": "figma-pro",
        "name": "Figma Professional",
        "brand": "Figma",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "Collaborative UI/UX design, interactive prototyping, Dev Mode code inspect, and team design systems.",
        "icon": "figma-pro",
        "starting_price_pkr": 1800,
        "starting_price_usd": 6.50,
        "plans": [
            {
                "plan_id": "FIGMA-1M",
                "name": "Professional (1 Month)",
                "type": "Professional",
                "duration": "1 Month (30 Days)",
                "seats": "1 Editor Seat",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "badge": "UI/UX Standard",
                "features": ["Unlimited Figma files & version history", "Shared team component libraries & Design Systems", "Advanced Dev Mode for CSS/Swift/Kotlin inspect", "Private project spaces & prototype sharing"],
                "terms": "Professional editor seat."
            },
            {
                "plan_id": "FIGMA-ANN-12M",
                "name": "Professional Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Editor Seat",
                "price_pkr": 17500,
                "price_usd": 62.00,
                "badge": "Save 19%",
                "features": ["Full 365 days of Professional editor capabilities", "Unlimited design systems & cloud components", "Includes FigJam whiteboarding tools", "365-day replacement warranty"],
                "terms": "Annual editor seat."
            }
        ]
    },
    {
        "rank": 23,
        "tier": "tier-pro",
        "tier_label": "📸 Vectors, PSDs & Photos",
        "slug": "freepik-premium",
        "name": "Freepik Premium",
        "brand": "Freepik Company",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "Millions of vectors, PSDs, stock photos, icons, and AI image generator credits with commercial license.",
        "icon": "freepik-premium",
        "starting_price_pkr": 1800,
        "starting_price_usd": 6.50,
        "plans": [
            {
                "plan_id": "FREEPIK-1M",
                "name": "Premium (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "badge": "Designer Favorite",
                "features": ["100 daily downloads of Premium vectors, PSDs & photos", "Zero attribution required with full commercial rights", "Freepik Pikaso real-time AI image generator", "Ad-free high-speed browsing and downloads"],
                "terms": "100 downloads daily limit per policy."
            },
            {
                "plan_id": "FREEPIK-ANN-12M",
                "name": "Premium Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User",
                "price_pkr": 14500,
                "price_usd": 52.00,
                "badge": "Save 33%",
                "features": ["Full 12 months unlimited access to Premium catalog", "Annual commercial license certificate for all assets", "Daily reset of 100 high-speed downloads", "365-day replacement warranty support"],
                "terms": "Annual individual subscription."
            }
        ]
    },
    {
        "rank": 24,
        "tier": "tier-pro",
        "tier_label": "📦 15M+ Video & Web Templates",
        "slug": "envato-elements",
        "name": "Envato Elements",
        "brand": "Envato",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "Unlimited downloads of 15M+ digital assets: video templates, music tracks, sound effects, graphics, and WordPress themes.",
        "icon": "envato-elements",
        "starting_price_pkr": 2600,
        "starting_price_usd": 9.50,
        "plans": [
            {
                "plan_id": "ENVATO-1M",
                "name": "Individual (1 Month Unlimited)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Unlimited Downloads)",
                "price_pkr": 2600,
                "price_usd": 9.50,
                "badge": "Unlimited Assets",
                "features": ["Unlimited downloads of 15M+ creative assets", "After Effects & Premiere Pro video templates", "Royalty-free commercial music & sound FX", "3D assets, fonts, graphics & WordPress themes"],
                "terms": "Lifetime commercial license for downloaded items."
            },
            {
                "plan_id": "ENVATO-ANN-12M",
                "name": "Individual Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (Unlimited Downloads)",
                "price_pkr": 24000,
                "price_usd": 86.00,
                "badge": "Agency Value",
                "features": ["Full 365 days uninterrupted unlimited asset downloads", "Commercial coverage for all client projects", "Continuous access to new daily design assets", "365-day replacement warranty coverage"],
                "terms": "Annual individual subscription."
            }
        ]
    },

    # --- TIER 3: PRODUCTIVITY, BUSINESS, AUDIO & MEDIA (Rank 25 to 40) ---
    {
        "rank": 25,
        "tier": "tier-utility",
        "tier_label": "✍️ Writing & Tone AI",
        "slug": "grammarly-pro",
        "name": "Grammarly Premium",
        "brand": "Grammarly",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Tone adjustments, full-sentence rewrites, plagiarism detection, English vocabulary enhancements, and Grammarly AI.",
        "icon": "grammarly-pro",
        "starting_price_pkr": 750,
        "starting_price_usd": 2.80,
        "plans": [
            {
                "plan_id": "GRAMMARLY-1M",
                "name": "Premium (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 750,
                "price_usd": 2.80,
                "badge": "Essential for Writers",
                "features": ["Full sentence rewrites for clarity & conciseness", "Tone adjustments for professional emails & papers", "Built-in plagiarism detector across billions of pages", "Browser extension, Desktop app & Word plugin"],
                "terms": "Personal user activation."
            },
            {
                "plan_id": "GRAMMARLY-12M",
                "name": "Premium Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 4500,
                "price_usd": 16.00,
                "badge": "Save 50%",
                "features": ["Full 365 days of uninterrupted Grammarly Premium", "Unlimited AI text suggestions & rewrites", "Complete browser, mobile & office app sync", "365-day replacement warranty guarantee"],
                "terms": "Annual license."
            }
        ]
    },
    {
        "rank": 26,
        "tier": "tier-utility",
        "tier_label": "📚 Academic Paraphraser",
        "slug": "quillbot-premium",
        "name": "QuillBot Premium Suite",
        "brand": "QuillBot (Learneo)",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Unlimited paraphrasing modes, grammar checking, plagiarism checker, summarizer, and citation generator.",
        "icon": "quillbot-premium",
        "starting_price_pkr": 1600,
        "starting_price_usd": 5.80,
        "plans": [
            {
                "plan_id": "QUILL-1M",
                "name": "Premium Suite (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1600,
                "price_usd": 5.80,
                "badge": "Academic Favorite",
                "features": ["Unlimited words in Paraphraser", "All 8 paraphrasing modes (Creative, Academic, Formal, etc.)", "Plagiarism checker (20 pages/month)", "Full Freeze Words control & tone detector"],
                "terms": "Single user account."
            },
            {
                "plan_id": "QUILL-12M",
                "name": "Premium Suite Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User",
                "price_pkr": 4200,
                "price_usd": 15.00,
                "badge": "Save 78%",
                "features": ["Full 12 months uninterrupted paraphrasing & grammar", "Annual Plagiarism Checker scanning credits", "Chrome, Word, and Edge extensions included", "365-day replacement warranty support"],
                "terms": "Annual subscription."
            }
        ]
    },
    {
        "rank": 27,
        "tier": "tier-utility",
        "tier_label": "💼 Word, Excel, PowerPoint",
        "slug": "microsoft-365",
        "name": "Microsoft 365 & Office Suite",
        "brand": "Microsoft",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Word, Excel, PowerPoint, Outlook, and OneDrive cloud storage with Copilot AI integration on Windows and Mac.",
        "icon": "microsoft-365",
        "starting_price_pkr": 900,
        "starting_price_usd": 3.20,
        "plans": [
            {
                "plan_id": "MS365-PERS-1M",
                "name": "Personal (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (5 Devices)",
                "price_pkr": 900,
                "price_usd": 3.20,
                "badge": "Office Essential",
                "features": ["Full desktop apps: Word, Excel, PowerPoint, Outlook", "1TB OneDrive secure cloud storage", "Install on up to 5 PCs/Macs + 5 tablets/phones", "Advanced security & ransomware protection"],
                "terms": "Official Microsoft account activation."
            },
            {
                "plan_id": "MS365-FAM-12M",
                "name": "Family Suite Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "Up to 6 Family Members",
                "price_pkr": 4500,
                "price_usd": 16.00,
                "badge": "Save 58%",
                "features": ["Full suite for up to 6 people (each gets 1TB OneDrive)", "Total 6TB cloud storage across family", "Premium safety features on Microsoft Family Safety", "365-day replacement warranty guarantee"],
                "terms": "Annual family activation."
            }
        ]
    },
    {
        "rank": 28,
        "tier": "tier-utility",
        "tier_label": "🦉 Language Learning Super",
        "slug": "duolingo-super",
        "name": "Duolingo Super",
        "brand": "Duolingo",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Unlimited hearts, ad-free language learning, personalized practice, and unlimited legendary challenges across 40+ languages.",
        "icon": "duolingo",
        "starting_price_pkr": 650,
        "starting_price_usd": 2.30,
        "plans": [
            {
                "plan_id": "DUOLINGO-1M",
                "name": "Super (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Learner Account",
                "price_pkr": 650,
                "price_usd": 2.30,
                "badge": "Language Pro",
                "features": ["Unlimited hearts — learn at your own pace without pauses", "Zero interruptive banner or video ads", "Personalized practice to target past mistakes", "Unlimited attempts at Legendary level challenges"],
                "terms": "Personal Duolingo account upgrade."
            },
            {
                "plan_id": "DUOLINGO-ANN-12M",
                "name": "Super Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Learner Account",
                "price_pkr": 3900,
                "price_usd": 14.00,
                "badge": "Save 50%",
                "features": ["Full 365 days of uninterrupted Super learning", "Includes all 40+ languages (English, German, Spanish, Arabic, etc.)", "Offline lesson progress tracking", "365-day replacement warranty guarantee"],
                "terms": "Annual individual subscription."
            }
        ]
    },
    {
        "rank": 29,
        "tier": "tier-utility",
        "tier_label": "🎮 Gaming & Communities",
        "slug": "discord-nitro",
        "name": "Discord Nitro",
        "brand": "Discord",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Custom animated emojis, 500MB upload size, 4K 60fps HD video streaming, 2 free server boosts, and custom profile banners.",
        "icon": "discord",
        "starting_price_pkr": 1400,
        "starting_price_usd": 5.00,
        "plans": [
            {
                "plan_id": "DISCORD-1M",
                "name": "Nitro Standard (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1400,
                "price_usd": 5.00,
                "badge": "Gamer Standard",
                "features": ["500MB file upload size for clips and projects", "Custom & animated emojis anywhere across all servers", "4K 60fps HD screen sharing and streaming", "2 Free Server Boosts + 30% off extra boosts"],
                "terms": "Personal Discord account upgrade."
            },
            {
                "plan_id": "DISCORD-ANN-12M",
                "name": "Nitro Annual (12 Months)",
                "type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 13500,
                "price_usd": 48.00,
                "badge": "Save 20%",
                "features": ["Full 365 days uninterrupted Discord Nitro perks", "Continuous 2 server boosts for your favorite community", "Exclusive profile badges and animated avatars", "365-day replacement warranty support"],
                "terms": "Annual user license."
            }
        ]
    },
    {
        "rank": 30,
        "tier": "tier-utility",
        "tier_label": "📹 Meetings & Collaboration",
        "slug": "zoom-workplace",
        "name": "Zoom Workplace Pro",
        "brand": "Zoom",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Unlimited 30-hour group meetings, 5GB cloud recording, AI Companion meeting summaries, and up to 100 participants.",
        "icon": "zoom",
        "starting_price_pkr": 1800,
        "starting_price_usd": 6.50,
        "plans": [
            {
                "plan_id": "ZOOM-PRO-1M",
                "name": "Pro Tier (1 Month)",
                "type": "Pro Host",
                "duration": "1 Month (30 Days)",
                "seats": "1 Licensed Host (100 Attendees)",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "badge": "Business Meetings",
                "features": ["Meetings up to 30 hours per session (no 40-min limit)", "Host up to 100 interactive participants", "Zoom AI Companion automated meeting summaries", "5GB cloud meeting video recording with transcript"],
                "terms": "Licensed meeting host account."
            }
        ]
    },
    {
        "rank": 31,
        "tier": "tier-utility",
        "tier_label": "💼 Career & Recruiter InMail",
        "slug": "linkedin-premium",
        "name": "LinkedIn Premium Career & Business",
        "brand": "LinkedIn / Microsoft",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Direct InMail messaging to recruiters, full 'Who's Viewed Your Profile' insights, and 21,000+ LinkedIn Learning courses.",
        "icon": "linkedin-premium",
        "starting_price_pkr": 1500,
        "starting_price_usd": 5.50,
        "plans": [
            {
                "plan_id": "LINKEDIN-1M",
                "name": "Career Plan (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1500,
                "price_usd": 5.50,
                "badge": "Career Accelerator",
                "features": ["5 InMail messages per month to reach recruiters directly", "See everyone who viewed your profile in the last 365 days", "Competitive applicant insights & salary data", "Full access to 21,000+ LinkedIn Learning courses"],
                "terms": "Personal LinkedIn profile upgrade."
            },
            {
                "plan_id": "LINKEDIN-BIZ-1M",
                "name": "Business Plan (1 Month)",
                "type": "Business",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 2900,
                "price_usd": 10.50,
                "badge": "Business Growth",
                "features": ["15 InMail messages per month", "Unlimited profile browsing without revealing identity", "Advanced company insights & employee growth metrics", "Includes full LinkedIn Learning library access"],
                "terms": "Business profile upgrade."
            }
        ]
    },
    {
        "rank": 32,
        "tier": "tier-utility",
        "tier_label": "📈 Financial Charts & Technicals",
        "slug": "tradingview",
        "name": "TradingView Pro / Essential",
        "brand": "TradingView",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "5 indicators per chart, 2 charts in one window, 20 server-side price alerts, second-based intervals, and volume profile.",
        "icon": "tradingview",
        "starting_price_pkr": 2400,
        "starting_price_usd": 8.50,
        "plans": [
            {
                "plan_id": "TV-PRO-1M",
                "name": "Essential / Pro (1 Month)",
                "type": "Essential",
                "duration": "1 Month (30 Days)",
                "seats": "1 Trader Account",
                "price_pkr": 2400,
                "price_usd": 8.50,
                "badge": "Trader Standard",
                "features": ["5 indicators per chart simultaneously", "2 charts in one layout window", "20 active server-side price alerts", "Ad-free experience & volume profile indicators"],
                "terms": "Personal trader account activation."
            },
            {
                "plan_id": "TV-PLUS-1M",
                "name": "Plus / Premium Tier (1 Month)",
                "type": "Plus",
                "duration": "1 Month (30 Days)",
                "seats": "1 Trader Account",
                "price_pkr": 4800,
                "price_usd": 17.00,
                "badge": "Pro Trader",
                "features": ["10 indicators per chart", "4 charts in one layout", "100 server-side price alerts", "Intraday bar replay & custom formulas"],
                "terms": "Advanced technical trader account."
            }
        ]
    },
    {
        "rank": 33,
        "tier": "tier-utility",
        "tier_label": "⚡ High Kinetic Video AI",
        "slug": "kling-ai",
        "name": "Kling AI Pro",
        "brand": "Kuaishou Kling AI",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "High-fidelity AI video generation up to 10 seconds, realistic character physics, and motion brush controls.",
        "icon": "kling-ai",
        "starting_price_pkr": 700,
        "starting_price_usd": 2.50,
        "plans": [
            {
                "plan_id": "KLING-1M",
                "name": "Pro Tier (1 Month)",
                "type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 700,
                "price_usd": 2.50,
                "badge": "High Motion",
                "features": ["660 credits / month for 1080p AI video generation", "Up to 10-second continuous motion sequences", "Motion Brush & camera trajectory controls", "No watermark exports in full 1080p"],
                "terms": "Credit pool valid for 30 days."
            },
            {
                "plan_id": "KLING-PREM-1M",
                "name": "Premier Tier (1 Month)",
                "type": "Premier",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "badge": "VFX Pro",
                "features": ["2,000 credits per month", "Priority video generation queue", "High-definition camera simulation modes", "Watermark-free commercial video licensing"],
                "terms": "Creator studio tier."
            }
        ]
    },
    {
        "rank": 34,
        "tier": "tier-utility",
        "tier_label": "🎥 Cinematic Human Physics",
        "slug": "minimax-ai",
        "name": "MiniMax Hailuo AI Video",
        "brand": "MiniMax",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "Hailuo AI video generator producing smooth, cinematic 6-second video clips with human anatomy accuracy.",
        "icon": "minimax-ai",
        "starting_price_pkr": 1600,
        "starting_price_usd": 5.80,
        "plans": [
            {
                "plan_id": "MINIMAX-1M",
                "name": "Standard Video Tier (1 Month)",
                "type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1600,
                "price_usd": 5.80,
                "badge": "Cinematic AI",
                "features": ["Priority generation queue for Hailuo AI video model", "720p and 1080p high dynamic range motion video", "Accurate human face and hand kinetic physics", "Fast text-to-video & image-to-video generation"],
                "terms": "Personal creator account."
            },
            {
                "plan_id": "MINIMAX-PRO-1M",
                "name": "Studio 1080p Tier (1 Month)",
                "type": "Studio",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 3400,
                "price_usd": 12.00,
                "badge": "Cinema Pro",
                "features": ["Full 1080p 60fps high bitrate exports", "Continuous multi-shot video generation", "Advanced camera motion choreography", "Commercial video rights included"],
                "terms": "Studio production tier."
            }
        ]
    },
    {
        "rank": 35,
        "tier": "tier-utility",
        "tier_label": "🎧 Stereo AI Music Lab",
        "slug": "udio-ai",
        "name": "Udio AI Music Lab",
        "brand": "Udio AI",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "High-fidelity stereo AI music composition with nuanced vocal styling, lyric editing, and musical genre blending.",
        "icon": "udio-ai",
        "starting_price_pkr": 2800,
        "starting_price_usd": 10.00,
        "plans": [
            {
                "plan_id": "UDIO-1M",
                "name": "Standard Tier (1 Month)",
                "type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2800,
                "price_usd": 10.00,
                "badge": "Studio Master",
                "features": ["1,200 monthly creation credits (~240 songs)", "Stereo audio stem downloads (vocals, drums, bass, synth)", "Advanced audio inpainting & track extension up to 15 mins", "Commercial rights for music distribution on Spotify/Apple"],
                "terms": "Standard generation queue."
            },
            {
                "plan_id": "UDIO-PRO-1M",
                "name": "Pro Tier (1 Month)",
                "type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 6200,
                "price_usd": 22.00,
                "badge": "Producer Choice",
                "features": ["4,800 creation credits per month", "Priority generation speed & batch processing", "Extended audio stems and WAV uncompressed export", "Commercial licensing across all digital media"],
                "terms": "Professional audio suite."
            }
        ]
    },
    {
        "rank": 36,
        "tier": "tier-utility",
        "tier_label": "🎬 Google DeepMind Video",
        "slug": "google-veo",
        "name": "Google Veo 2 / Video FX",
        "brand": "Google DeepMind",
        "category": "AI Video & Audio",
        "cat_key": "video",
        "desc": "Next-generation generative video model understanding cinematic terms, lenses, and consistent visual physics.",
        "icon": "google-veo",
        "starting_price_pkr": 1900,
        "starting_price_usd": 6.80,
        "plans": [
            {
                "plan_id": "VEO-1M",
                "name": "VideoFX Early Access (1 Month)",
                "type": "Early Access",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer / Creator",
                "price_pkr": 1900,
                "price_usd": 6.80,
                "badge": "Next-Gen Video",
                "features": ["1080p high-definition cinematic video generations", "Understands technical camera directions (timelapse, aerial, pan)", "High physical consistency across continuous shots", "Direct integration with Google Labs VideoFX suite"],
                "terms": "Google Labs whitelisted access."
            }
        ]
    },
    {
        "rank": 37,
        "tier": "tier-utility",
        "tier_label": "🎮 Game & Concept Art Studio",
        "slug": "leonardo-ai",
        "name": "Leonardo AI Visual Studio",
        "brand": "Leonardo.Ai / Canva",
        "category": "Design & Creative",
        "cat_key": "image",
        "desc": "Phoenix foundational model, real-time Canvas painting, custom fine-tuned LoRAs, and 3D texture synthesis.",
        "icon": "leonardo-ai",
        "starting_price_pkr": 1300,
        "starting_price_usd": 4.80,
        "plans": [
            {
                "plan_id": "LEONARDO-1M",
                "name": "Apprentice Plan (1 Month)",
                "type": "Apprentice",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1300,
                "price_usd": 4.80,
                "badge": "Game & Concept Art",
                "features": ["8,500 Fast generation tokens per month", "Realtime Canvas sketch-to-image synthesis", "Train up to 10 custom fine-tuned AI models", "Full commercial usage terms for game & graphic design"],
                "terms": "Tokens refresh monthly."
            },
            {
                "plan_id": "LEONARDO-ART-1M",
                "name": "Artisan Plan (1 Month)",
                "type": "Artisan",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 3200,
                "price_usd": 11.50,
                "badge": "Studio Pro",
                "features": ["25,000 Fast tokens per month", "Unlimited Relax generation mode", "Train up to 20 custom AI models", "Priority rendering and generation queue"],
                "terms": "Commercial studio tier."
            }
        ]
    },
    {
        "rank": 38,
        "tier": "tier-utility",
        "tier_label": "⚡ Real-Time X Data Grounding",
        "slug": "grok-ai",
        "name": "Grok 2 / xAI SuperGrok",
        "brand": "xAI",
        "category": "AI Assistant & LLM",
        "cat_key": "chat",
        "desc": "Real-time X/Twitter data grounding, Flux.1 image generation, and unfiltered conversational AI capabilities.",
        "icon": "grok-ai",
        "starting_price_pkr": 1100,
        "starting_price_usd": 4.00,
        "plans": [
            {
                "plan_id": "GROK-1M",
                "name": "SuperGrok / Grok 2 (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1100,
                "price_usd": 4.00,
                "badge": "Real-Time AI",
                "features": ["Real-time trending news synthesis from global posts", "Uncensored Flux.1 photorealistic image generation", "Grok 2 reasoning and code interpretation", "X Premium badge & reduced ads on timeline"],
                "terms": "Personal user account."
            },
            {
                "plan_id": "GROK-PLUS-1M",
                "name": "Premium Plus Tier (1 Month)",
                "type": "Premium Plus",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2400,
                "price_usd": 8.60,
                "badge": "Full Ad-Free",
                "features": ["100% Ad-Free For You and Following timeline", "Largest reply boost on X network", "Full creator monetization eligibility", "Priority Grok 2 compute allocations"],
                "terms": "Personal account upgrade."
            }
        ]
    },
    {
        "rank": 39,
        "tier": "tier-utility",
        "tier_label": "📊 Competitor SEO & Backlinks",
        "slug": "semrush-guru",
        "name": "Semrush Guru Platform",
        "brand": "Semrush",
        "category": "Productivity & SEO",
        "cat_key": "seo",
        "desc": "Competitor SEO keyword analysis, domain backlink audits, position tracking, and content marketing toolkit.",
        "icon": "semrush-guru",
        "starting_price_pkr": 1900,
        "starting_price_usd": 7.00,
        "plans": [
            {
                "plan_id": "SEMRUSH-PRO-1M",
                "name": "Pro Tier (1 Month)",
                "type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1900,
                "price_usd": 7.00,
                "badge": "Freelancer Pick",
                "features": ["5 projects & 500 keywords tracked daily", "Domain & keyword analytics with competitor traffic estimates", "On-page SEO checker & site audit crawler (100k pages)", "PDF export reports"],
                "terms": "Single user account."
            },
            {
                "plan_id": "SEMRUSH-GURU-1M",
                "name": "Guru Platform (1 Month)",
                "type": "Guru",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Shared Dedicated Suite)",
                "price_pkr": 2500,
                "price_usd": 9.00,
                "badge": "Agency Standard",
                "features": ["15 projects & 1,500 keywords tracked daily", "Historical keyword & backlink data since 2012", "Content Marketing Platform & Topic Research", "Looker Studio integration & branded PDF reports"],
                "terms": "Subject to daily query limits."
            }
        ]
    },
    {
        "rank": 40,
        "tier": "tier-utility",
        "tier_label": "☁️ Cloud IDE & Instant Host",
        "slug": "replit-core",
        "name": "Replit Core Cloud IDE",
        "brand": "Replit",
        "category": "AI Coding & Dev",
        "cat_key": "coding",
        "desc": "Cloud development environments, Replit AI code assistant, persistent hosting deployments, and collaborative pair coding.",
        "icon": "replit-core",
        "starting_price_pkr": 2800,
        "starting_price_usd": 10.00,
        "plans": [
            {
                "plan_id": "REPLIT-1M",
                "name": "Core Tier (1 Month)",
                "type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Workspace",
                "price_pkr": 2800,
                "price_usd": 10.00,
                "badge": "Cloud IDE",
                "features": ["Unlimited basic Repls & collaborative coding", "Replit AI code completion and codebase chat", "Fast cloud VMs with 4x memory and 2x vCPU", "Persistent background apps and deployments"],
                "terms": "Cloud deployment credits per tier."
            },
            {
                "plan_id": "REPLIT-TEAM-1M",
                "name": "Team Collaboration (1 Month)",
                "type": "Team Workspace",
                "duration": "1 Month (30 Days)",
                "seats": "Shared Team Workspace",
                "price_pkr": 5400,
                "price_usd": 19.50,
                "badge": "Team Dev",
                "features": ["Centralized billing and shared team repls", "8x memory and 4x vCPU cloud dev servers", "Role-based access control and private repos", "Priority deployments and custom domains"],
                "terms": "Team workspace license."
            }
        ]
    }
]

# Generate standalone HTML
cards_html_list = []
for tool in RANKED_CATALOG:
    slug = tool["slug"]
    icon_key = tool["icon"]
    svg_raw = svg_cache.get(icon_key, svg_cache.get("chatgpt-plus", ""))
    svg_styled = svg_raw.replace("<svg ", '<svg class="tool-svg-icon" ')
    
    plans = tool["plans"]
    
    plan_rows = []
    for p in plans:
        badge_html = f'<span class="mini-pill">{p["badge"]}</span>' if p.get("badge") else ""
        feats_txt = " • ".join(p["features"][:2])
        plan_rows.append(f'''
          <div class="plan-variant-row">
            <div class="plan-variant-info">
              <div class="plan-variant-title">{p['name']} {badge_html}</div>
              <div class="plan-variant-meta">⏱ {p['duration']} • 👤 {p['seats']}</div>
              <div class="plan-variant-feats">{feats_txt}</div>
            </div>
            <div class="plan-variant-action">
              <div class="variant-price-pkr">Rs. {p['price_pkr']:,}</div>
              <div class="variant-price-usd">(~${p['price_usd']:.2f} USD)</div>
              <button type="button" class="btn-select-plan" onclick="openOrderDrawer('{slug}', '{p['plan_id']}')">Choose Plan</button>
            </div>
          </div>
        ''')
    plans_inner_html = "\n".join(plan_rows)

    card = f'''
    <div class="ranked-tool-card {tool['tier']}" data-category="{tool['cat_key']}" data-slug="{slug}" data-name="{tool['name'].lower()}">
      <div class="card-top-bar">
        <div class="rank-pill">{tool['tier_label']}</div>
        <div class="plan-count-tag">{len(plans)} Distinct Plans</div>
      </div>

      <div class="tool-identity">
        <div class="tool-logo-box">
          {svg_styled}
        </div>
        <div>
          <h3 class="tool-heading">{tool['name']}</h3>
          <div class="tool-sub-meta">{tool['brand']} • {tool['category']}</div>
        </div>
      </div>

      <p class="tool-summary-text">{tool['desc']}</p>

      <div class="starting-price-banner">
        <div>
          <span class="price-from-label">Official Starting Price:</span>
          <div class="price-hero-pkr">Rs. {tool['starting_price_pkr']:,} <span class="curr-code">PKR</span></div>
        </div>
        <div class="price-usd-pill">(~${tool['starting_price_usd']:.2f} USD)</div>
      </div>

      <div class="card-button-group">
        <button type="button" class="btn-view-plans" onclick="toggleCardPlans(this, '{slug}')">
          <span>Compare {len(plans)} Plans</span>
          <span class="arrow">▼</span>
        </button>
        <button type="button" class="btn-instant-order" onclick="openOrderDrawer('{slug}')">
          ⚡ Quick Order
        </button>
      </div>

      <div class="card-plans-drawer" id="drawer-{slug}">
        <div class="plans-drawer-inner">
          <div class="drawer-inner-title">Verified Unique Plans for {tool['name']}:</div>
          {plans_inner_html}
        </div>
      </div>
    </div>
    '''
    cards_html_list.append(card)

cards_joined = "\n".join(cards_html_list)

master_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AIDigiTools — Ranked Professional Catalog & Unique Plans Matrix</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --navy: #0F172A;
      --blue: #0284C7;
      --emerald: #10B981;
      --indigo: #4361EE;
      --gold: #D97706;
      --bg: #F8FAFC;
      --surface: #FFFFFF;
      --border: #E2E8F0;
      --text: #0F172A;
      --text-muted: #64748B;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding-bottom: 5rem;
    }}

    header {{
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 100;
    }}
    .nav-inner {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .logo-container {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }}
    .brand-title {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--navy);
    }}
    .brand-title .ai {{ color: #00B4D8; }}
    .brand-tag {{
      font-size: 0.65rem;
      font-weight: 700;
      color: var(--text-muted);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      display: block;
    }}

    .hero-wrap {{
      max-width: 1320px;
      margin: 2rem auto 1.5rem;
      padding: 0 1.5rem;
      text-align: center;
    }}
    .top-badge {{
      display: inline-block;
      background: #FEF3C7;
      color: #92400E;
      border: 1px solid #FDE68A;
      padding: 0.35rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      margin-bottom: 0.75rem;
    }}
    .hero-h1 {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 2.35rem;
      font-weight: 800;
      color: var(--navy);
      letter-spacing: -0.02em;
      margin-bottom: 0.6rem;
    }}
    .hero-p {{
      font-size: 1.05rem;
      color: #475569;
      max-width: 800px;
      margin: 0 auto 1.5rem;
    }}

    /* Filters */
    .controls-wrap {{
      max-width: 1320px;
      margin: 0 auto 2rem;
      padding: 0 1.5rem;
    }}
    .search-bar {{
      max-width: 650px;
      margin: 0 auto 1.25rem;
      position: relative;
    }}
    .search-bar input {{
      width: 100%;
      padding: 0.85rem 1.25rem 0.85rem 3rem;
      border-radius: 12px;
      border: 1.5px solid var(--border);
      background: #FFFFFF;
      font-size: 0.95rem;
      font-family: inherit;
      outline: none;
    }}
    .search-bar input:focus {{
      border-color: var(--blue);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }}
    .search-icon {{
      position: absolute;
      left: 1.1rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 1.1rem;
      color: var(--text-muted);
    }}

    .category-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
    }}
    .cat-btn {{
      padding: 0.45rem 0.9rem;
      border-radius: 9999px;
      border: 1.5px solid var(--border);
      background: #FFFFFF;
      color: #475569;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .cat-btn.active {{
      background: var(--navy);
      color: #FFFFFF;
      border-color: var(--navy);
    }}

    /* Cards Grid */
    .cards-grid {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.75rem;
    }}

    .ranked-tool-card {{
      background: var(--surface);
      border: 1.5px solid var(--border);
      border-radius: 18px;
      padding: 1.6rem;
      box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
      position: relative;
    }}
    .ranked-tool-card:hover {{
      transform: translateY(-4px);
      box-shadow: 0 12px 28px rgba(15, 23, 42, 0.1);
      border-color: var(--blue);
    }}

    .ranked-tool-card.tier-elite {{
      border-color: #BAE6FD;
      background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 22%);
    }}

    .card-top-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }}
    .rank-pill {{
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.2rem 0.65rem;
      border-radius: 9999px;
      background: #E0F2FE;
      color: #0369A1;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .tier-elite .rank-pill {{
      background: #FEF3C7;
      color: #92400E;
    }}
    .plan-count-tag {{
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--emerald);
      background: #ECFDF5;
      padding: 0.15rem 0.55rem;
      border-radius: 6px;
    }}

    .tool-identity {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
      margin-bottom: 0.85rem;
    }}
    .tool-logo-box {{
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: #F8FAFC;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      flex-shrink: 0;
      box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06);
    }}
    .tool-svg-icon {{
      width: 100%;
      height: 100%;
      display: block;
    }}
    .tool-heading {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--navy);
      line-height: 1.25;
    }}
    .tool-sub-meta {{
      font-size: 0.75rem;
      color: var(--text-muted);
    }}

    .tool-summary-text {{
      font-size: 0.85rem;
      color: #475569;
      line-height: 1.45;
      margin-bottom: 1.15rem;
      flex-grow: 1;
    }}

    .starting-price-banner {{
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.75rem 0.9rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }}
    .price-from-label {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      display: block;
    }}
    .price-hero-pkr {{
      font-size: 1.35rem;
      font-weight: 800;
      color: var(--blue);
      line-height: 1;
    }}
    .curr-code {{
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--navy);
    }}
    .price-usd-pill {{
      font-size: 0.75rem;
      font-weight: 700;
      color: #64748B;
    }}

    .card-button-group {{
      display: flex;
      gap: 0.5rem;
    }}
    .btn-view-plans {{
      flex: 1;
      padding: 0.65rem 0.75rem;
      border-radius: 9px;
      border: 1.5px solid var(--border);
      background: #FFFFFF;
      color: var(--navy);
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
    }}
    .btn-view-plans:hover {{
      border-color: var(--blue);
      background: #F0F9FF;
      color: var(--blue);
    }}
    .btn-view-plans .arrow {{
      font-size: 0.65rem;
      transition: transform 0.2s ease;
    }}
    .btn-view-plans.open .arrow {{
      transform: rotate(180deg);
    }}

    .btn-instant-order {{
      padding: 0.65rem 1rem;
      border-radius: 9px;
      background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
      color: #FFFFFF;
      font-size: 0.82rem;
      font-weight: 700;
      border: none;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.2);
    }}
    .btn-instant-order:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35);
    }}

    /* Card Plans Drawer Accordion */
    .card-plans-drawer {{
      display: none;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px dashed var(--border);
    }}
    .card-plans-drawer.open {{
      display: block;
    }}
    .drawer-inner-title {{
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--blue);
      margin-bottom: 0.65rem;
    }}
    .plan-variant-row {{
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 0.7rem 0.8rem;
      margin-bottom: 0.55rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
    }}
    .plan-variant-info {{
      flex-grow: 1;
    }}
    .plan-variant-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--navy);
    }}
    .mini-pill {{
      font-size: 0.62rem;
      font-weight: 700;
      padding: 0.1rem 0.35rem;
      border-radius: 4px;
      background: #E0F2FE;
      color: #0369A1;
      margin-left: 0.3rem;
    }}
    .plan-variant-meta {{
      font-size: 0.7rem;
      color: var(--text-muted);
      margin-top: 0.15rem;
    }}
    .plan-variant-feats {{
      font-size: 0.7rem;
      color: #475569;
      margin-top: 0.2rem;
    }}
    .plan-variant-action {{
      text-align: right;
      flex-shrink: 0;
    }}
    .variant-price-pkr {{
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--blue);
    }}
    .variant-price-usd {{
      font-size: 0.68rem;
      color: var(--text-muted);
    }}
    .btn-select-plan {{
      margin-top: 0.35rem;
      background: var(--navy);
      color: #FFFFFF;
      border: none;
      padding: 0.3rem 0.65rem;
      border-radius: 6px;
      font-size: 0.72rem;
      font-weight: 700;
      cursor: pointer;
    }}
    .btn-select-plan:hover {{
      background: var(--blue);
    }}

    /* Quick Order Drawer */
    .drawer-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 999;
      display: none;
    }}
    .drawer-backdrop.active {{ display: block; }}
    .drawer-panel {{
      position: fixed;
      top: 0;
      right: -480px;
      width: 480px;
      max-width: 95vw;
      height: 100vh;
      background: #FFFFFF;
      z-index: 1000;
      box-shadow: -10px 0 35px rgba(15, 23, 42, 0.2);
      transition: right 0.25s ease;
      display: flex;
      flex-direction: column;
    }}
    .drawer-panel.active {{ right: 0; }}
    .drawer-header {{
      padding: 1.25rem 1.5rem;
      background: #F8FAFC;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .drawer-body {{
      padding: 1.5rem;
      overflow-y: auto;
      flex-grow: 1;
    }}
    .drawer-footer {{
      padding: 1.25rem 1.5rem;
      background: #F8FAFC;
      border-top: 1px solid var(--border);
    }}
    .btn-checkout-wa {{
      width: 100%;
      padding: 0.95rem;
      border-radius: 12px;
      background: #25D366;
      color: #FFFFFF;
      font-weight: 700;
      font-size: 1rem;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      text-decoration: none;
      box-shadow: 0 4px 14px rgba(37, 211, 102, 0.3);
    }}
  </style>
</head>
<body>

  <header>
    <div class="nav-inner">
      <div class="logo-container">
        <svg width="40" height="40" viewBox="0 0 160 160" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="tG" x1="0%" y1="100%" x2="100%" y2="0%"><stop offset="0%" stop-color="#00E5A3"/><stop offset="100%" stop-color="#00B4D8"/></linearGradient>
            <linearGradient id="pG" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0077B6"/><stop offset="50%" stop-color="#4361EE"/><stop offset="100%" stop-color="#8B5CF6"/></linearGradient>
          </defs>
          <path d="M 22 94 L 46 32 C 48 27, 54 22, 62 25 L 75 30 C 80 32, 81 37, 78 42 L 56 94 C 54 99, 46 102, 38 100 L 26 97 C 22 96, 21 95, 22 94 Z" fill="url(#tG)"/>
          <path d="M 68 34 C 88 22, 118 30, 118 56 C 118 82, 88 98, 62 98 L 74 82 C 90 82, 102 72, 102 56 C 102 42, 86 36, 72 44 Z" fill="url(#pG)"/>
          <circle cx="124" cy="34" r="5.5" fill="#4361EE"/>
        </svg>
        <div>
          <span class="brand-title"><span class="ai">AI</span> DigiTools</span>
          <span class="brand-tag">CANONICAL CATALOG MATRIX</span>
        </div>
      </div>
      <div>
        <span style="font-size:0.85rem; font-weight:700; color:#166534; background:#F0FDF4; border:1px solid #BBF7D0; padding:0.35rem 0.75rem; border-radius:9999px;">✓ Ranked #1 to #40 • Zero Duplicates</span>
      </div>
    </div>
  </header>

  <div class="hero-wrap">
    <div class="top-badge">👑 Strict Priority Ranking — Professional & High-Demand Tools at Top</div>
    <h1 class="hero-h1">Professional Tools &amp; Unique Plans Matrix</h1>
    <p class="hero-p">
      Every tool is deduplicated into single canonical parent listings. Multi-supplier listings for identical subscriptions are merged. Expand any tool to compare its verified plan tiers (seats, duration, limits) with honest domestic Pakistani Rupee pricing.
    </p>
  </div>

  <div class="controls-wrap">
    <div class="search-bar">
      <span class="search-icon">🔍</span>
      <input type="text" placeholder="Search by name, category, or features (e.g., ChatGPT, Claude, Midjourney, Canva, 4K, Family)..." oninput="filterTools(this.value)">
    </div>

    <div class="category-pills">
      <button type="button" class="cat-btn active" onclick="setCategory('all', this)">All 40 Tools</button>
      <button type="button" class="cat-btn" onclick="setCategory('chat', this)">AI Chat & LLMs</button>
      <button type="button" class="cat-btn" onclick="setCategory('coding', this)">AI Coding & Dev</button>
      <button type="button" class="cat-btn" onclick="setCategory('image', this)">Design & Creative</button>
      <button type="button" class="cat-btn" onclick="setCategory('video', this)">AI Video & Audio</button>
      <button type="button" class="cat-btn" onclick="setCategory('vpn', this)">VPN & Privacy</button>
      <button type="button" class="cat-btn" onclick="setCategory('seo', this)">Productivity & SEO</button>
      <button type="button" class="cat-btn" onclick="setCategory('streaming', this)">Streaming & Music</button>
    </div>
  </div>

  <main class="cards-grid" id="toolsGrid">
    {cards_joined}
  </main>

  <!-- Slide-Over Quick Order Drawer -->
  <div class="drawer-backdrop" id="dBackdrop" onclick="closeOrderDrawer()"></div>
  <aside class="drawer-panel" id="dPanel">
    <div class="drawer-header">
      <div style="font-weight:700; font-size:1.1rem; color:var(--navy);">⚡ Quick Order Checkout</div>
      <button type="button" onclick="closeOrderDrawer()" style="background:none; border:none; font-size:1.4rem; cursor:pointer;">&times;</button>
    </div>
    <div class="drawer-body">
      <div id="drawerSummaryBox" style="background:#F8FAFC; border:1px solid var(--border); border-radius:12px; padding:1rem; margin-bottom:1.25rem;">
        <div id="drawerToolName" style="font-weight:700; font-size:1.05rem; color:var(--navy);">Tool Name</div>
        <div id="drawerToolSub" style="font-size:0.78rem; color:var(--text-muted);">Brand • Category</div>
      </div>

      <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:#475569; margin-bottom:0.5rem;">Select Verified Plan:</div>
      <div id="drawerPlansContainer" style="display:flex; flex-direction:column; gap:0.5rem; margin-bottom:1.25rem;"></div>

      <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:#475569; margin-bottom:0.5rem;">Select Payment Rail:</div>
      <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.5rem; margin-bottom:1.25rem;">
        <button type="button" class="cat-btn active" style="text-align:center;">EasyPaisa</button>
        <button type="button" class="cat-btn" style="text-align:center;">JazzCash</button>
        <button type="button" class="cat-btn" style="text-align:center;">SadaPay</button>
        <button type="button" class="cat-btn" style="text-align:center;">Bank IBFT</button>
      </div>

      <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:8px; padding:0.75rem; font-size:0.75rem; color:#166534;">
        🛡️ <strong>AIDigiTools Guarantee:</strong> 15-Minute WhatsApp electronic delivery, setup credentials guide & 30-Day replacement warranty.
      </div>
    </div>
    <div class="drawer-footer">
      <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:1rem;">
        <span style="font-weight:600; font-size:0.85rem; color:#475569;">Total Payable:</span>
        <div style="text-align:right;">
          <div id="drawerTotalPkr" style="font-size:1.55rem; font-weight:800; color:var(--blue); line-height:1;">Rs. 0</div>
          <div id="drawerTotalUsd" style="font-size:0.78rem; color:var(--text-muted);">(~$0.00 USD)</div>
        </div>
      </div>
      <a href="#" id="drawerWaBtn" target="_blank" rel="noopener noreferrer" class="btn-checkout-wa">
        <span>Order on WhatsApp (03326861112)</span>
        <span>→</span>
      </a>
    </div>
  </aside>

  <script>
    var TOOLS_MAP = {json.dumps({t["slug"]: t for t in RANKED_CATALOG})};
    var activeTool = TOOLS_MAP["chatgpt-plus"];
    var activePlan = activeTool.plans[0];

    function toggleCardPlans(btn, slug) {{
      var drawer = document.getElementById('drawer-' + slug);
      if (!drawer) return;
      var isOpen = drawer.classList.contains('open');
      if (isOpen) {{
        drawer.classList.remove('open');
        btn.classList.remove('open');
      }} else {{
        drawer.classList.add('open');
        btn.classList.add('open');
      }}
    }}

    function filterTools(query) {{
      var q = (query || '').toLowerCase().trim();
      var cards = document.querySelectorAll('.ranked-tool-card');
      cards.forEach(function(card) {{
        var text = card.textContent.toLowerCase();
        card.style.display = (!q || text.indexOf(q) !== -1) ? 'flex' : 'none';
      }});
    }}

    function setCategory(catKey, btn) {{
      var btns = document.querySelectorAll('.cat-btn');
      btns.forEach(function(b) {{ b.classList.remove('active'); }});
      if (btn) btn.classList.add('active');

      var cards = document.querySelectorAll('.ranked-tool-card');
      cards.forEach(function(card) {{
        var c = card.getAttribute('data-category');
        card.style.display = (catKey === 'all' || c === catKey) ? 'flex' : 'none';
      }});
    }}

    function openOrderDrawer(slug, planId) {{
      var tool = TOOLS_MAP[slug] || TOOLS_MAP["chatgpt-plus"];
      activeTool = tool;

      if (planId && tool.plans) {{
        activePlan = tool.plans.find(function(p) {{ return p.plan_id === planId; }}) || tool.plans[0];
      }} else if (tool.plans) {{
        activePlan = tool.plans[0];
      }}

      document.getElementById('drawerToolName').textContent = tool.name;
      document.getElementById('drawerToolSub').textContent = tool.brand + ' • ' + tool.category;

      renderDrawerPlans();
      updateDrawerTotals();

      document.getElementById('dBackdrop').classList.add('active');
      document.getElementById('dPanel').classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeOrderDrawer() {{
      document.getElementById('dBackdrop').classList.remove('active');
      document.getElementById('dPanel').classList.remove('active');
      document.body.style.overflow = '';
    }}

    function selectPlan(planId) {{
      var found = activeTool.plans.find(function(p) {{ return p.plan_id === planId; }});
      if (found) {{
        activePlan = found;
        renderDrawerPlans();
        updateDrawerTotals();
      }}
    }}

    function renderDrawerPlans() {{
      var container = document.getElementById('drawerPlansContainer');
      var html = '';
      activeTool.plans.forEach(function(p) {{
        var isSelected = activePlan && activePlan.plan_id === p.plan_id;
        var borderStyle = isSelected ? 'border:1.5px solid #0284C7; background:#F0F9FF;' : 'border:1px solid #E2E8F0; background:#FFFFFF;';
        html += '<div onclick=\"selectPlan(\\'' + p.plan_id + '\\')\" style=\"padding:0.65rem 0.85rem; border-radius:8px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; ' + borderStyle + '\">';
        html += '<div><div style=\"font-weight:700; font-size:0.85rem; color:#0F172A;\">' + p.name + '</div><div style=\"font-size:0.7rem; color:#64748B;\">' + p.duration + ' • ' + p.seats + '</div></div>';
        html += '<div style=\"text-align:right;\"><div style=\"font-weight:800; font-size:0.95rem; color:#0284C7;\">Rs. ' + p.price_pkr.toLocaleString() + '</div><div style=\"font-size:0.68rem; color:#64748B;\">(~$' + p.price_usd.toFixed(2) + ' USD)</div></div>';
        html += '</div>';
      }});
      container.innerHTML = html;
    }}

    function updateDrawerTotals() {{
      if (!activePlan) return;
      document.getElementById('drawerTotalPkr').textContent = 'Rs. ' + activePlan.price_pkr.toLocaleString() + ' PKR';
      document.getElementById('drawerTotalUsd').textContent = '(~$' + activePlan.price_usd.toFixed(2) + ' USD)';

      var msg = "Hi AIDigiTools! I want to order " + activeTool.name + " (" + activePlan.name + ") for Rs. " + activePlan.price_pkr.toLocaleString() + " PKR (~$" + activePlan.price_usd.toFixed(2) + " USD). Please share payment details and 15m delivery activation.";
      document.getElementById('drawerWaBtn').href = "https://wa.me/923326861112?text=" + encodeURIComponent(msg);
    }}

    document.addEventListener('keydown', function(e) {{
      if (e.key === 'Escape') closeOrderDrawer();
    }});
  </script>
</body>
</html>
'''

with open(DEST_HTML, "w", encoding="utf-8") as f:
    f.write(master_html)

print(f"Generated Professional Ranked Master Preview HTML at: {DEST_HTML} ({len(master_html)} bytes)")
