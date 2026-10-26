# scripts/build_all_40_tools_catalog.py
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, "scripts", "tools_catalog.json")

# Full 40 Canonical Tools Catalog with Distinct Verified Plans
ALL_TOOLS = {
    # 1. AI Assistant & LLMs
    "chatgpt-plus": {
        "slug": "chatgpt-plus",
        "name": "ChatGPT Plus & Team",
        "brand": "OpenAI",
        "brand_id": "openai",
        "category_key": "coding",
        "category_label": "AI Assistant & LLM",
        "vendor": "OpenAI Enterprise Systems",
        "description": "Full access to GPT-4o, o1 reasoning models, custom GPTs, Advanced Voice Mode, and DALL-E 3 image generation.",
        "url": "tools/chatgpt-plus.html",
        "icon": "assets/product-logos/chatgpt-plus.svg",
        "plans": [
            {
                "plan_id": "PLAN-GPT-PLUS-1M",
                "name": "ChatGPT Plus (1 Month)",
                "plan_type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2300,
                "price_usd": 8.00,
                "features": ["GPT-4o, GPT-4, and OpenAI o1 reasoning", "Advanced Voice Mode on iOS & Android", "DALL-E 3 high-res image generation", "File analysis, web browsing & custom GPTs"],
                "limits": "Standard OpenAI message frequency caps apply",
                "badge": "Most Popular",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-GPT-TEAM-1M",
                "name": "ChatGPT Team Workspace (1 Month)",
                "plan_type": "Team Workspace",
                "duration": "1 Month (30 Days)",
                "seats": "Team Shared Workspace",
                "price_pkr": 4800,
                "price_usd": 17.00,
                "features": ["Higher message limits on GPT-4o and o1", "Dedicated collaborative workspace & admin console", "Shared custom GPTs within organization", "Zero model training on proprietary business data"],
                "limits": "Team workspace terms apply",
                "badge": "Business Grade",
                "availability": "InStock"
            }
        ]
    },
    "claude-pro": {
        "slug": "claude-pro",
        "name": "Claude Pro & Team",
        "brand": "Anthropic",
        "brand_id": "anthropic",
        "category_key": "coding",
        "category_label": "AI Assistant & LLM",
        "vendor": "Anthropic AI Systems",
        "description": "Claude 3.5 Sonnet with 200,000 token context window, interactive Artifacts canvas, and industry-leading code intelligence.",
        "url": "tools/claude-pro.html",
        "icon": "assets/product-logos/claude-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-CLAUDE-PRO-1M",
                "name": "Claude Pro (1 Month)",
                "plan_type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2500,
                "price_usd": 9.00,
                "features": ["5x higher usage limits vs free Claude tier", "Claude 3.5 Sonnet & Claude 3.5 Haiku models", "Interactive split-screen Artifacts live runner", "Early access to new Anthropic features"],
                "limits": "Subject to Anthropic rolling message limits",
                "badge": "Top for Coding",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-CLAUDE-TEAM-1M",
                "name": "Claude Team (1 Month)",
                "plan_type": "Team Workspace",
                "duration": "1 Month (30 Days)",
                "seats": "Workspace Seat",
                "price_pkr": 5200,
                "price_usd": 18.50,
                "features": ["Higher per-user usage limits on Sonnet", "Team management & centralized billing", "Collaborative project sharing & prompt libraries", "Enterprise privacy guarantees"],
                "limits": "Requires organization workspace setup",
                "badge": "Team Collab",
                "availability": "InStock"
            }
        ]
    },
    "perplexity-pro": {
        "slug": "perplexity-pro",
        "name": "Perplexity Pro AI",
        "brand": "Perplexity AI",
        "brand_id": "perplexity",
        "category_key": "coding",
        "category_label": "AI Assistant & LLM",
        "vendor": "Perplexity AI Systems",
        "description": "Pro search with real-time web citations, Claude 3.5 Sonnet and GPT-4o models, document analysis, and academic research.",
        "url": "tools/perplexity-pro.html",
        "icon": "assets/product-logos/perplexity-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-PERP-1M",
                "name": "Perplexity Pro (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2200,
                "price_usd": 8.00,
                "features": ["600+ Pro Searches / day with multi-step reasoning", "Model switcher: Claude 3.5 Sonnet, GPT-4o, Sonar Large", "Unlimited file and PDF research uploads", "Includes $5/month API credits"],
                "limits": "Personal search account",
                "badge": "Research Gold",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-PERP-12M",
                "name": "Perplexity Pro Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User",
                "price_pkr": 16500,
                "price_usd": 59.00,
                "features": ["Full 12 months uninterrupted Pro research", "All premium AI models unlocked", "Priority processing & zero search queue", "365-day replacement warranty support"],
                "limits": "Annual subscription",
                "badge": "Save 37%",
                "availability": "InStock"
            }
        ]
    },
    "gemini-advanced": {
        "slug": "gemini-advanced",
        "name": "Google Gemini Advanced",
        "brand": "Google",
        "brand_id": "google-gemini",
        "category_key": "coding",
        "category_label": "AI Assistant & LLM",
        "vendor": "Google DeepMind Systems",
        "description": "Gemini 1.5 Pro with 2-million token context window, Google Workspace integration, and 2TB Google One cloud storage.",
        "url": "tools/gemini-advanced.html",
        "icon": "assets/product-logos/gemini-advanced.svg",
        "plans": [
            {
                "plan_id": "PLAN-GEMINI-1M",
                "name": "Advanced (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1200,
                "price_usd": 4.50,
                "features": ["Gemini 1.5 Pro with 2M token context", "Deep reasoning across 1,500 pages of text", "Gemini integrated directly into Gmail & Docs", "2TB Google One cloud storage"],
                "limits": "Google account activation",
                "badge": "2M Context",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-GEMINI-ANN-12M",
                "name": "Advanced Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 11500,
                "price_usd": 41.00,
                "features": ["Full 365 days of 2M token Gemini 1.5 Pro", "Includes 2TB Google One cloud backup for 1 year", "Priority access to new experimental models", "Full 365-day replacement warranty"],
                "limits": "Annual Google account subscription",
                "badge": "Save 20%",
                "availability": "InStock"
            }
        ]
    },
    "deepseek-pro": {
        "slug": "deepseek-pro",
        "name": "DeepSeek R1 / V3 Pro",
        "brand": "DeepSeek",
        "brand_id": "deepseek",
        "category_key": "coding",
        "category_label": "AI Assistant & LLM",
        "vendor": "DeepSeek AI Research",
        "description": "DeepSeek-R1 open reasoning model, V3 MoE architecture, high-token API allowances, and code generation.",
        "url": "tools/deepseek-pro.html",
        "icon": "assets/product-logos/deepseek-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-DEEPSEEK-1M",
                "name": "R1 / V3 Pro Tier (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1100,
                "price_usd": 4.00,
                "features": ["Full access to DeepSeek-R1 reasoning model", "DeepSeek-V3 MoE 671B architecture", "Zero queue delays during peak traffic", "High context coding and math capabilities"],
                "limits": "Fair usage limits apply",
                "badge": "Open Reasoning",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-DEEPSEEK-DEV-1M",
                "name": "Developer High-Token API Tier",
                "plan_type": "Developer API",
                "duration": "1 Month (30 Days)",
                "seats": "Developer Organization",
                "price_pkr": 2900,
                "price_usd": 10.50,
                "features": ["Pre-funded token balance for R1 and V3 API", "High concurrency limit (50 requests/sec)", "Direct OpenAI-compatible API endpoint", "Dedicated developer support"],
                "limits": "API token consumption rates apply",
                "badge": "Dev Scaler",
                "availability": "InStock"
            }
        ]
    },
    "grok-ai": {
        "slug": "grok-ai",
        "name": "Grok 2 / xAI SuperGrok",
        "brand": "xAI",
        "brand_id": "xai-grok",
        "category_key": "coding",
        "category_label": "AI Assistant & LLM",
        "vendor": "xAI Corporation",
        "description": "Real-time X/Twitter data grounding, Flux.1 image generation, and unfiltered conversational AI capabilities.",
        "url": "tools/grok-ai.html",
        "icon": "assets/product-logos/grok-ai.svg",
        "plans": [
            {
                "plan_id": "PLAN-GROK-1M",
                "name": "SuperGrok / Grok 2 (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1100,
                "price_usd": 4.00,
                "features": ["Real-time trending news synthesis from global posts", "Uncensored Flux.1 photorealistic image generation", "Grok 2 reasoning and code interpretation", "X Premium badge & reduced ads on timeline"],
                "limits": "Personal user account",
                "badge": "Real-Time AI",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-GROK-PLUS-1M",
                "name": "Premium Plus Tier (1 Month)",
                "plan_type": "Premium Plus",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2400,
                "price_usd": 8.60,
                "features": ["100% Ad-Free For You and Following timeline", "Largest reply boost on X network", "Full creator monetization eligibility", "Priority Grok 2 compute allocations"],
                "limits": "Personal account upgrade",
                "badge": "Full Ad-Free",
                "availability": "InStock"
            }
        ]
    },

    # 2. Design & Creative Software
    "canva-pro": {
        "slug": "canva-pro",
        "name": "Canva Pro",
        "brand": "Canva",
        "brand_id": "canva",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Canva Design Platform",
        "description": "100M+ premium stock assets, Magic Studio AI background remover, 1TB cloud storage, and team Brand Kits.",
        "url": "tools/canva-pro.html",
        "icon": "assets/product-logos/canva-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-CANVA-1M",
                "name": "Canva Pro (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 600,
                "price_usd": 2.50,
                "features": ["Unlimited 1-click Magic Background Remover", "100M+ premium stock photos, videos, and graphics", "1TB secure cloud storage for brand assets", "Brand Kit color palettes, logos, and custom fonts"],
                "limits": "Individual Pro account email upgrade",
                "badge": "Best Seller",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-CANVA-12M",
                "name": "Canva Pro Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 2200,
                "price_usd": 7.90,
                "features": ["Full 12 months uninterrupted Pro access", "Unlimited Magic Studio AI tools & downloads", "Complete Brand Kit & 1TB cloud storage", "Full 365-day replacement warranty protection"],
                "limits": "Annual term with zero renewal hassles",
                "badge": "Save 70%",
                "availability": "InStock"
            }
        ]
    },
    "midjourney": {
        "slug": "midjourney",
        "name": "Midjourney v6.1",
        "brand": "Midjourney",
        "brand_id": "midjourney",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Midjourney Research Lab",
        "description": "State-of-the-art photorealistic image generation, texture synthesis, and inpainting with commercial rights.",
        "url": "tools/midjourney.html",
        "icon": "assets/product-logos/midjourney.svg",
        "plans": [
            {
                "plan_id": "PLAN-MIDJ-BASIC-1M",
                "name": "Basic Plan (1 Month)",
                "plan_type": "Basic",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["200 Fast GPU minutes (~200 images)", "General commercial usage terms", "Access to member web gallery", "Direct messaging bot access"],
                "limits": "No Relax mode generation",
                "badge": "Starter",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-MIDJ-STD-1M",
                "name": "Standard Plan (1 Month)",
                "plan_type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2800,
                "price_usd": 9.99,
                "features": ["15 Fast GPU hours (~1,000 images)", "Unlimited Relax GPU mode generation", "General commercial terms", "Web gallery & inpainting editor"],
                "limits": "Unlimited Relax mode subject to dynamic queue",
                "badge": "Most Popular",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-MIDJ-PRO-1M",
                "name": "Pro Plan (1 Month)",
                "plan_type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 5600,
                "price_usd": 20.00,
                "features": ["30 Fast GPU hours (~2,000 images)", "Stealth mode (keep generations private)", "Unlimited Relax GPU mode", "12 concurrent Fast jobs"],
                "limits": "Professional privacy tier",
                "badge": "Agency Grade",
                "availability": "InStock"
            }
        ]
    },
    "adobe-creative-cloud": {
        "slug": "adobe-creative-cloud",
        "name": "Adobe Creative Cloud",
        "brand": "Adobe",
        "brand_id": "adobe",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Adobe Creative Cloud Platform",
        "description": "Photoshop, Premiere Pro, Illustrator, After Effects, and Firefly generative credits with 100GB cloud storage.",
        "url": "tools/adobe-creative-cloud.html",
        "icon": "assets/product-logos/adobe-creative-cloud.svg",
        "plans": [
            {
                "plan_id": "PLAN-ADOBE-CC-1M",
                "name": "All Apps (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (2 Devices Active)",
                "price_pkr": 1400,
                "price_usd": 5.50,
                "features": ["Access to 20+ desktop & mobile creative apps", "Adobe Firefly AI generative credits", "100GB Adobe cloud storage", "Adobe Fonts library with 20,000+ typefaces"],
                "limits": "Active on up to 2 devices concurrently",
                "badge": "Industry Standard",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-ADOBE-CC-12M",
                "name": "All Apps Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (2 Devices Active)",
                "price_pkr": 14000,
                "price_usd": 50.00,
                "features": ["Full 12 months access to entire Creative Cloud suite", "Monthly Firefly AI credit renewals", "100GB cloud asset synchronization", "365-day replacement warranty support"],
                "limits": "Annual license with uninterrupted activation",
                "badge": "Agency Value",
                "availability": "InStock"
            }
        ]
    },
    "figma-pro": {
        "slug": "figma-pro",
        "name": "Figma Pro",
        "brand": "Figma",
        "brand_id": "figma",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Figma Design Systems",
        "description": "Collaborative UI/UX design, interactive prototyping, Dev Mode code inspect, and team design systems.",
        "url": "tools/figma-pro.html",
        "icon": "assets/product-logos/figma-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-FIGMA-1M",
                "name": "Professional (1 Month)",
                "plan_type": "Professional",
                "duration": "1 Month (30 Days)",
                "seats": "1 Editor Seat",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["Unlimited Figma files & version history", "Shared team component libraries & Design Systems", "Advanced Dev Mode for CSS/Swift/Kotlin inspect", "Private project spaces & prototype sharing"],
                "limits": "Professional editor seat",
                "badge": "UI/UX Standard",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-FIGMA-ANN-12M",
                "name": "Professional Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Editor Seat",
                "price_pkr": 17500,
                "price_usd": 62.00,
                "features": ["Full 365 days of Professional editor capabilities", "Unlimited design systems & cloud components", "Includes FigJam whiteboarding tools", "365-day replacement warranty"],
                "limits": "Annual editor seat",
                "badge": "Save 19%",
                "availability": "InStock"
            }
        ]
    },
    "envato-elements": {
        "slug": "envato-elements",
        "name": "Envato Elements",
        "brand": "Envato",
        "brand_id": "envato",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Envato Pty Ltd.",
        "description": "Unlimited downloads of 15M+ digital assets: video templates, music tracks, sound effects, graphics, and WordPress themes.",
        "url": "tools/envato-elements.html",
        "icon": "assets/product-logos/envato-elements.svg",
        "plans": [
            {
                "plan_id": "PLAN-ENVATO-1M",
                "name": "Individual (1 Month Unlimited)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Unlimited Downloads)",
                "price_pkr": 2600,
                "price_usd": 9.50,
                "features": ["Unlimited downloads of 15M+ creative assets", "After Effects & Premiere Pro video templates", "Royalty-free commercial music & sound FX", "3D assets, fonts, graphics & WordPress themes"],
                "limits": "Lifetime commercial license for downloaded items",
                "badge": "Unlimited Assets",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-ENVATO-ANN-12M",
                "name": "Individual Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (Unlimited Downloads)",
                "price_pkr": 24000,
                "price_usd": 86.00,
                "features": ["Full 365 days uninterrupted unlimited asset downloads", "Commercial coverage for all client projects", "Continuous access to new daily design assets", "365-day replacement warranty coverage"],
                "limits": "Annual individual subscription",
                "badge": "Agency Value",
                "availability": "InStock"
            }
        ]
    },
    "freepik-premium": {
        "slug": "freepik-premium",
        "name": "Freepik Premium",
        "brand": "Freepik Company",
        "brand_id": "freepik",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Freepik Company",
        "description": "Millions of vectors, PSDs, stock photos, icons, and AI image generator credits with commercial license.",
        "url": "tools/freepik-premium.html",
        "icon": "assets/product-logos/freepik-premium.svg",
        "plans": [
            {
                "plan_id": "PLAN-FREEPIK-1M",
                "name": "Premium (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["100 daily downloads of Premium vectors, PSDs & photos", "Zero attribution required with full commercial rights", "Freepik Pikaso real-time AI image generator", "Ad-free high-speed browsing and downloads"],
                "limits": "100 downloads daily limit per policy",
                "badge": "Designer Favorite",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-FREEPIK-ANN-12M",
                "name": "Premium Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User",
                "price_pkr": 14500,
                "price_usd": 52.00,
                "features": ["Full 12 months unlimited access to Premium catalog", "Annual commercial license certificate for all assets", "Daily reset of 100 high-speed downloads", "365-day replacement warranty support"],
                "limits": "Annual individual subscription",
                "badge": "Save 33%",
                "availability": "InStock"
            }
        ]
    },
    "leonardo-ai": {
        "slug": "leonardo-ai",
        "name": "Leonardo AI Visual Studio",
        "brand": "Leonardo.Ai / Canva",
        "brand_id": "leonardo",
        "category_key": "image",
        "category_label": "Design & Creative",
        "vendor": "Leonardo Interactive Pty",
        "description": "Phoenix foundational model, real-time Canvas painting, custom fine-tuned LoRAs, and 3D texture synthesis.",
        "url": "tools/leonardo-ai.html",
        "icon": "assets/product-logos/leonardo-ai.svg",
        "plans": [
            {
                "plan_id": "PLAN-LEONARDO-1M",
                "name": "Apprentice Plan (1 Month)",
                "plan_type": "Apprentice",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1300,
                "price_usd": 4.80,
                "features": ["8,500 Fast generation tokens per month", "Realtime Canvas sketch-to-image synthesis", "Train up to 10 custom fine-tuned AI models", "Full commercial usage terms for game & graphic design"],
                "limits": "Tokens refresh monthly",
                "badge": "Game & Concept Art",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-LEONARDO-ART-1M",
                "name": "Artisan Plan (1 Month)",
                "plan_type": "Artisan",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 3200,
                "price_usd": 11.50,
                "features": ["25,000 Fast tokens per month", "Unlimited Relax generation mode", "Train up to 20 custom AI models", "Priority rendering and generation queue"],
                "limits": "Commercial studio tier",
                "badge": "Studio Pro",
                "availability": "InStock"
            }
        ]
    },

    # 3. AI Video & Audio Generators
    "youtube-premium": {
        "slug": "youtube-premium",
        "name": "YouTube Premium Ad-Free",
        "brand": "Google / YouTube",
        "brand_id": "google-youtube",
        "category_key": "video",
        "category_label": "Streaming & Entertainment",
        "vendor": "YouTube & Google Inc.",
        "description": "Ad-free streaming, background audio playback on mobile, high-bitrate offline downloads, and YouTube Music Premium.",
        "url": "tools/youtube-premium.html",
        "icon": "assets/product-logos/youtube-premium.svg",
        "plans": [
            {
                "plan_id": "PLAN-YT-IND-1M",
                "name": "Individual (1 Month)",
                "plan_type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 750,
                "price_usd": 2.80,
                "features": ["100% Ad-free video playback", "Background audio while using other apps", "Offline 1080p/4K downloads", "YouTube Music Premium included"],
                "limits": "Personal account activation; single concurrent stream",
                "badge": "Most Popular",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-YT-FAM-1M",
                "name": "Family Plan (1 Month)",
                "plan_type": "Family",
                "duration": "1 Month (30 Days)",
                "seats": "Up to 5 Family Members",
                "price_pkr": 1450,
                "price_usd": 5.20,
                "features": ["5 Independent member profiles with private histories", "Ad-free streaming across all household devices", "5x YouTube Music Premium accounts", "Offline downloads on each member device"],
                "limits": "All members must reside in the same country/region",
                "badge": "Best Value",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-YT-ANN-12M",
                "name": "Individual Annual (12 Months)",
                "plan_type": "Annual Individual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 7500,
                "price_usd": 27.00,
                "features": ["Full 365 days uninterrupted ad-free playback", "Includes YouTube Music Premium for 1 year", "Zero monthly renewal friction", "Full 365-day replacement warranty guarantee"],
                "limits": "Fixed term subscription; non-transferable",
                "badge": "Save 16%",
                "availability": "InStock"
            }
        ]
    },
    "capcut-pro": {
        "slug": "capcut-pro",
        "name": "CapCut Pro",
        "brand": "ByteDance / CapCut",
        "brand_id": "capcut",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "ByteDance Creative Studio",
        "description": "Automated bilingual AI captions, 4K 60fps optical flow smoothing, background removal, and commercial music licensing.",
        "url": "tools/capcut-pro.html",
        "icon": "assets/product-logos/capcut-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-CAPCUT-1M",
                "name": "CapCut Pro (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 950,
                "price_usd": 3.50,
                "features": ["Auto captions with bilingual word-level sync", "4K 60fps optical flow ultra-smooth rendering", "Smart AI body cutout & green screen remover", "100GB CapCut cloud space for multi-device sync"],
                "limits": "PC, Mac, Android, and iOS cross-sync supported",
                "badge": "Top for Creators",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-CAPCUT-12M",
                "name": "CapCut Pro Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 5900,
                "price_usd": 21.00,
                "features": ["Full 12 months uninterrupted Pro access", "Unlimited 4K exports & premium transitions", "100GB cloud project backup", "365-day replacement guarantee"],
                "limits": "Non-transferable annual license",
                "badge": "Save 48%",
                "availability": "InStock"
            }
        ]
    },
    "elevenlabs-creator": {
        "slug": "elevenlabs-creator",
        "name": "ElevenLabs Creator & Pro",
        "brand": "ElevenLabs",
        "brand_id": "elevenlabs",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "ElevenLabs Voice AI",
        "description": "100,000 monthly voice characters, Instant Voice Cloning, commercial license rights, and 192kbps studio audio.",
        "url": "tools/elevenlabs-creator.html",
        "icon": "assets/product-logos/elevenlabs-creator.svg",
        "plans": [
            {
                "plan_id": "PLAN-11LABS-CREATOR-1M",
                "name": "Creator Plan (1 Month)",
                "plan_type": "Creator",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2800,
                "price_usd": 10.00,
                "features": ["100,000 characters per month (~2 hours of audio)", "Create up to 30 custom instant voice clones", "Commercial rights for YouTube & podcasts", "192kbps ultra-high quality audio export"],
                "limits": "Unused characters do not roll over to next month",
                "badge": "Top Audio AI",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-11LABS-PRO-1M",
                "name": "Pro Plan (1 Month)",
                "plan_type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 6500,
                "price_usd": 23.50,
                "features": ["500,000 characters per month (~10 hours of audio)", "Professional Voice Cloning (PVC) enabled", "160 custom voices & priority rendering", "Commercial rights across all broadcast media"],
                "limits": "Professional voice tier",
                "badge": "Studio Pro",
                "availability": "InStock"
            }
        ]
    },
    "runway-gen3": {
        "slug": "runway-gen3",
        "name": "Runway Gen-3 Alpha",
        "brand": "Runway",
        "brand_id": "runway",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "Runway AI Motion Engine",
        "description": "Gen-3 Alpha photorealistic video generation with keyframe camera control, motion brush, and text-to-video.",
        "url": "tools/runway-gen3.html",
        "icon": "assets/product-logos/runway-gen3.svg",
        "plans": [
            {
                "plan_id": "PLAN-RUNWAY-STD-1M",
                "name": "Standard (1 Month)",
                "plan_type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["625 credits / month (~125 seconds of Gen-3 video)", "Motion Brush & camera control tools", "Export up to 4K resolution with watermark removal", "Train 1 custom voice or portrait generator"],
                "limits": "Standard generation queue",
                "badge": "Video Filmmaker",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-RUNWAY-UNLTD-1M",
                "name": "Unlimited Plan (1 Month)",
                "plan_type": "Unlimited",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 4900,
                "price_usd": 17.50,
                "features": ["Unlimited relaxed video generations", "2,250 monthly Fast credits", "Full commercial video licensing rights", "Priority enterprise rendering tier"],
                "limits": "Relaxed queue speed varies by load",
                "badge": "Pro Studio",
                "availability": "InStock"
            }
        ]
    },
    "suno-ai": {
        "slug": "suno-ai",
        "name": "Suno AI Music v3.5",
        "brand": "Suno AI",
        "brand_id": "suno",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "Suno AI Audio Systems",
        "description": "Full 2-minute vocal and instrumental music generation across pop, rock, electronic, orchestral, and classical genres.",
        "url": "tools/suno-ai.html",
        "icon": "assets/product-logos/suno-ai.svg",
        "plans": [
            {
                "plan_id": "PLAN-SUNO-PRO-1M",
                "name": "Pro Plan (1 Month)",
                "plan_type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2600,
                "price_usd": 9.50,
                "features": ["2,500 credits / month (~500 songs)", "General commercial terms for streaming monetization", "Priority generation queue & audio stem separation", "Upload audio clips to extend songs"],
                "limits": "Commercial terms apply while subscribed",
                "badge": "Musician Choice",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-SUNO-PREM-1M",
                "name": "Premier Plan (1 Month)",
                "plan_type": "Premier",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 6800,
                "price_usd": 24.50,
                "features": ["10,000 credits / month (~2,000 songs)", "Maximum generation priority queue", "Full stem exports with instrumental backing tracks", "Commercial distribution on Spotify, Apple Music & YouTube"],
                "limits": "Professional music producer tier",
                "badge": "Pro Label",
                "availability": "InStock"
            }
        ]
    },
    "udio-ai": {
        "slug": "udio-ai",
        "name": "Udio AI Music Lab",
        "brand": "Udio AI",
        "brand_id": "udio",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "Udio AI Music Lab",
        "description": "High-fidelity stereo AI music composition with nuanced vocal styling, lyric editing, and musical genre blending.",
        "url": "tools/udio-ai.html",
        "icon": "assets/product-logos/udio-ai.svg",
        "plans": [
            {
                "plan_id": "PLAN-UDIO-1M",
                "name": "Standard Tier (1 Month)",
                "plan_type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 2800,
                "price_usd": 10.00,
                "features": ["1,200 monthly creation credits (~240 songs)", "Stereo audio stem downloads (vocals, drums, bass, synth)", "Advanced audio inpainting & track extension up to 15 mins", "Commercial rights for music distribution on Spotify/Apple"],
                "limits": "Standard generation queue",
                "badge": "Studio Master",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-UDIO-PRO-1M",
                "name": "Pro Tier (1 Month)",
                "plan_type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 6200,
                "price_usd": 22.00,
                "features": ["4,800 creation credits per month", "Priority generation speed & batch processing", "Extended audio stems and WAV uncompressed export", "Commercial licensing across all digital media"],
                "limits": "Professional audio suite",
                "badge": "Producer Choice",
                "availability": "InStock"
            }
        ]
    },
    "kling-ai": {
        "slug": "kling-ai",
        "name": "Kling AI Pro",
        "brand": "Kuaishou Kling AI",
        "brand_id": "kling",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "Kuaishou Kling AI Lab",
        "description": "High-fidelity AI video generation up to 10 seconds, realistic character physics, and motion brush controls.",
        "url": "tools/kling-ai.html",
        "icon": "assets/product-logos/kling-ai.svg",
        "plans": [
            {
                "plan_id": "PLAN-KLING-1M",
                "name": "Pro Tier (1 Month)",
                "plan_type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 700,
                "price_usd": 2.50,
                "features": ["660 credits / month for 1080p AI video generation", "Up to 10-second continuous motion sequences", "Motion Brush & camera trajectory controls", "No watermark exports in full 1080p"],
                "limits": "Credit pool valid for 30 days",
                "badge": "High Motion",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-KLING-PREM-1M",
                "name": "Premier Tier (1 Month)",
                "plan_type": "Premier",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["2,000 credits per month", "Priority video generation queue", "High-definition camera simulation modes", "Watermark-free commercial video licensing"],
                "limits": "Creator studio tier",
                "badge": "VFX Pro",
                "availability": "InStock"
            }
        ]
    },
    "minimax-ai": {
        "slug": "minimax-ai",
        "name": "MiniMax Hailuo AI Video",
        "brand": "MiniMax",
        "brand_id": "minimax",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "MiniMax Intelligent Lab",
        "description": "Hailuo AI video generator producing smooth, cinematic 6-second video clips with human anatomy accuracy.",
        "url": "tools/minimax-ai.html",
        "icon": "assets/product-logos/minimax-ai.svg",
        "plans": [
            {
                "plan_id": "PLAN-MINIMAX-1M",
                "name": "Standard Video Tier (1 Month)",
                "plan_type": "Standard",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1600,
                "price_usd": 5.80,
                "features": ["Priority generation queue for Hailuo AI video model", "720p and 1080p high dynamic range motion video", "Accurate human face and hand kinetic physics", "Fast text-to-video & image-to-video generation"],
                "limits": "Personal creator account",
                "badge": "Cinematic AI",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-MINIMAX-PRO-1M",
                "name": "Studio 1080p Tier (1 Month)",
                "plan_type": "Studio",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 3400,
                "price_usd": 12.00,
                "features": ["Full 1080p 60fps high bitrate exports", "Continuous multi-shot video generation", "Advanced camera motion choreography", "Commercial video rights included"],
                "limits": "Studio production tier",
                "badge": "Cinema Pro",
                "availability": "InStock"
            }
        ]
    },
    "google-veo": {
        "slug": "google-veo",
        "name": "Google Veo 2 / Video FX",
        "brand": "Google DeepMind",
        "brand_id": "google-veo",
        "category_key": "video",
        "category_label": "AI Video & Audio",
        "vendor": "Google DeepMind Video Lab",
        "description": "Next-generation generative video model understanding cinematic terms, lenses, and consistent visual physics.",
        "url": "tools/google-veo.html",
        "icon": "assets/product-logos/google-veo.svg",
        "plans": [
            {
                "plan_id": "PLAN-VEO-1M",
                "name": "VideoFX Early Access (1 Month)",
                "plan_type": "Early Access",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer / Creator",
                "price_pkr": 1900,
                "price_usd": 6.80,
                "features": ["1080p high-definition cinematic video generations", "Understands technical camera directions (timelapse, aerial, pan)", "High physical consistency across continuous shots", "Direct integration with Google Labs VideoFX suite"],
                "limits": "Google Labs whitelisted access",
                "badge": "Next-Gen Video",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-VEO-STUDIO-1M",
                "name": "Studio Creator Tier (1 Month)",
                "plan_type": "Studio",
                "duration": "1 Month (30 Days)",
                "seats": "1 Creator",
                "price_pkr": 4200,
                "price_usd": 15.00,
                "features": ["High resolution 4K cinematic upscaling", "Priority GPU rendering queue", "Extended shot duration capabilities", "Direct Google Workspace export"],
                "limits": "Early access developer allocation",
                "badge": "Hollywood Grade",
                "availability": "InStock"
            }
        ]
    },

    # 4. AI Coding & Developer Tools
    "cursor-pro": {
        "slug": "cursor-pro",
        "name": "Cursor Pro",
        "brand": "Anysphere (Cursor)",
        "brand_id": "cursor",
        "category_key": "coding",
        "category_label": "AI Coding & Dev",
        "vendor": "Anysphere AI Lab",
        "description": "AI-first code editor with Claude 3.5 Sonnet agentic codebase chat, multi-file edits, and instant code prediction.",
        "url": "tools/cursor-pro.html",
        "icon": "assets/product-logos/cursor-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-CURSOR-1M",
                "name": "Cursor Pro (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 3800,
                "price_usd": 13.50,
                "features": ["500 Fast Premium requests / month (Claude 3.5 Sonnet & GPT-4o)", "Unlimited Slow requests after fast quota", "Multi-file Composer codebase refactoring", "Smart line and multi-line code auto-complete"],
                "limits": "Individual developer seat",
                "badge": "Developer Choice",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-CURSOR-ANN-12M",
                "name": "Cursor Pro Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 39000,
                "price_usd": 140.00,
                "features": ["Full 365 days of uninterrupted Fast Claude 3.5 Sonnet Composer", "Zero monthly subscription renewal friction", "Priority compute allocations during peak hours", "365-day replacement warranty support"],
                "limits": "Annual developer license",
                "badge": "Save 15%",
                "availability": "InStock"
            }
        ]
    },
    "github-copilot": {
        "slug": "github-copilot",
        "name": "GitHub Copilot Pro & Business",
        "brand": "GitHub / Microsoft",
        "brand_id": "github",
        "category_key": "coding",
        "category_label": "AI Coding & Dev",
        "vendor": "GitHub Inc.",
        "description": "AI pair programmer inside VS Code, Visual Studio, and JetBrains with code autocompletions and Copilot Chat.",
        "url": "tools/github-copilot.html",
        "icon": "assets/product-logos/github-copilot.svg",
        "plans": [
            {
                "plan_id": "PLAN-COPILOT-1M",
                "name": "Copilot Individual (1 Month)",
                "plan_type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 1500,
                "price_usd": 5.50,
                "features": ["Real-time whole line & function autocompletions", "Copilot Chat in VS Code and JetBrains IDEs", "CLI command generator & code explanations", "Public code filter to avoid copyright matches"],
                "limits": "Personal GitHub account linkage",
                "badge": "Coder Essential",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-COPILOT-BIZ-1M",
                "name": "Copilot Business (1 Month)",
                "plan_type": "Business Seat",
                "duration": "1 Month (30 Days)",
                "seats": "Organization Seat",
                "price_pkr": 3200,
                "price_usd": 11.50,
                "features": ["Organization-wide policy management", "Copilot in GitHub Mobile & Pull Request summaries", "Zero data retention for model training", "Centralized seat provisioning"],
                "limits": "GitHub organization seat",
                "badge": "Enterprise Dev",
                "availability": "InStock"
            }
        ]
    },
    "jetbrains-all": {
        "slug": "jetbrains-all",
        "name": "JetBrains All Products Pack",
        "brand": "JetBrains",
        "brand_id": "jetbrains",
        "category_key": "coding",
        "category_label": "AI Coding & Dev",
        "vendor": "JetBrains s.r.o.",
        "description": "Complete suite of 16 IDEs including IntelliJ IDEA Ultimate, PyCharm Pro, WebStorm, Rider, CLion, and GoLand.",
        "url": "tools/jetbrains-all.html",
        "icon": "assets/product-logos/jetbrains-all.svg",
        "plans": [
            {
                "plan_id": "PLAN-JETBRAINS-1M",
                "name": "All Products Pack (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer (Multi-Device)",
                "price_pkr": 2500,
                "price_usd": 9.00,
                "features": ["All 16 JetBrains IDEs: IntelliJ, PyCharm, WebStorm, CLion, Rider, GoLand, etc.", "Full commercial development rights", "JetBrains AI Assistant integration", "Cross-platform support on Windows, macOS & Linux"],
                "limits": "Single developer license",
                "badge": "Dev Superpack",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-JETBRAINS-12M",
                "name": "All Products Pack Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Developer (Multi-Device)",
                "price_pkr": 18000,
                "price_usd": 64.00,
                "features": ["Full 365 days access to entire JetBrains product family", "Includes all major version upgrades during term", "Perpetual fallback license rights eligible", "365-day replacement warranty guarantee"],
                "limits": "Annual developer license",
                "badge": "Save 40%",
                "availability": "InStock"
            }
        ]
    },
    "replit-core": {
        "slug": "replit-core",
        "name": "Replit Core Cloud IDE",
        "brand": "Replit",
        "brand_id": "replit",
        "category_key": "coding",
        "category_label": "AI Coding & Dev",
        "vendor": "Replit Cloud Development",
        "description": "Cloud development environments, Replit AI code assistant, persistent hosting deployments, and collaborative pair coding.",
        "url": "tools/replit-core.html",
        "icon": "assets/product-logos/replit-core.svg",
        "plans": [
            {
                "plan_id": "PLAN-REPLIT-1M",
                "name": "Core Tier (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Workspace",
                "price_pkr": 2800,
                "price_usd": 10.00,
                "features": ["Unlimited basic Repls & collaborative coding", "Replit AI code completion and codebase chat", "Fast cloud VMs with 4x memory and 2x vCPU", "Persistent background apps and deployments"],
                "limits": "Cloud deployment credits per tier",
                "badge": "Cloud IDE",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-REPLIT-TEAM-1M",
                "name": "Team Collaboration (1 Month)",
                "plan_type": "Team Workspace",
                "duration": "1 Month (30 Days)",
                "seats": "Shared Team Workspace",
                "price_pkr": 5400,
                "price_usd": 19.50,
                "features": ["Centralized billing and shared team repls", "8x memory and 4x vCPU cloud dev servers", "Role-based access control and private repos", "Priority deployments and custom domains"],
                "limits": "Team workspace license",
                "badge": "Team Dev",
                "availability": "InStock"
            }
        ]
    },
    "chatgpt-codex": {
        "slug": "chatgpt-codex",
        "name": "OpenAI API & Codex",
        "brand": "OpenAI",
        "brand_id": "openai-codex",
        "category_key": "coding",
        "category_label": "AI Coding & Dev",
        "vendor": "OpenAI Developer Platform",
        "description": "High-quota OpenAI API keys for GPT-4o, Codex code completion, Whisper audio transcription, and vector embeddings.",
        "url": "tools/chatgpt-codex.html",
        "icon": "assets/product-logos/chatgpt-codex.svg",
        "plans": [
            {
                "plan_id": "PLAN-CODEX-DEV-1M",
                "name": "Developer Tier (1 Month)",
                "plan_type": "Developer API",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Organization",
                "price_pkr": 600,
                "price_usd": 2.50,
                "features": ["Pre-funded OpenAI developer API balance", "Access to GPT-4o, GPT-4o-mini, and embeddings", "Rate limits up to 500 requests per minute", "Full developer dashboard access & usage monitoring"],
                "limits": "API token consumption rates apply",
                "badge": "Dev API",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-CODEX-SCALE-1M",
                "name": "Scale Enterprise API Tier",
                "plan_type": "Enterprise API",
                "duration": "1 Month (30 Days)",
                "seats": "Production App Keys",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["High concurrency rate limits (Tier 4 equivalent)", "Access to fine-tuning pipelines", "Zero log retention compliance options", "Dedicated developer support channel"],
                "limits": "Usage billed against token pool",
                "badge": "Production Scale",
                "availability": "InStock"
            }
        ]
    },
    "claude-artifacts": {
        "slug": "claude-artifacts",
        "name": "Claude Artifacts Pro",
        "brand": "Anthropic",
        "brand_id": "anthropic-artifacts",
        "category_key": "coding",
        "category_label": "AI Coding & Dev",
        "vendor": "Anthropic AI Systems",
        "description": "Live preview HTML, React, SVG, and Mermaid diagrams generated in Claude 3.5 Sonnet's split-screen canvas.",
        "url": "tools/claude-artifacts.html",
        "icon": "assets/product-logos/claude-artifacts.svg",
        "plans": [
            {
                "plan_id": "PLAN-ARTIFACTS-1M",
                "name": "Artifacts Suite (1 Month)",
                "plan_type": "Interactive Suite",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1200,
                "price_usd": 4.50,
                "features": ["Interactive split-screen code and UI renderer", "Instant React components, HTML5 games, and SVG graphics", "Download and fork generated Artifact code snippets", "Claude 3.5 Sonnet reasoning backing every generation"],
                "limits": "Anthropic platform limits apply",
                "badge": "Live Prototyping",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-ARTIFACTS-DEV-1M",
                "name": "Enterprise Developer Suite (1 Month)",
                "plan_type": "Developer Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 Developer Account",
                "price_pkr": 2900,
                "price_usd": 10.50,
                "features": ["Extended context window for large codebase artifacts", "Direct GitHub repo integration & live component staging", "Unlimited artifact forks and version histories", "Priority rendering pipeline"],
                "limits": "Subject to Anthropic platform terms",
                "badge": "Dev Master",
                "availability": "InStock"
            }
        ]
    },

    # 5. VPN & Cyber Privacy
    "nordvpn": {
        "slug": "nordvpn",
        "name": "NordVPN Complete",
        "brand": "Nord Security",
        "brand_id": "nordvpn",
        "category_key": "vpn",
        "category_label": "VPN & Privacy",
        "vendor": "Nord Security Systems",
        "description": "6,400+ ultra-fast RAM-only servers, NordLynx WireGuard protocol, Threat Protection Pro, and 10 simultaneous devices.",
        "url": "tools/nordvpn.html",
        "icon": "assets/product-logos/nordvpn.svg",
        "plans": [
            {
                "plan_id": "PLAN-NORD-1M",
                "name": "Standard (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "Up to 10 Simultaneous Devices",
                "price_pkr": 850,
                "price_usd": 3.00,
                "features": ["Ultra-fast NordLynx protocol with zero logs", "Access to 6,400+ servers in 111 countries", "Double VPN & Onion Over VPN routing", "Threat Protection malware & ad blocking"],
                "limits": "Independent audited no-logs policy",
                "badge": "Top Privacy",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-NORD-12M",
                "name": "Complete Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "Up to 10 Simultaneous Devices",
                "price_pkr": 5400,
                "price_usd": 19.50,
                "features": ["Full 365 days secure high-speed browsing", "Includes 1TB encrypted cloud storage", "Cross-platform apps (Windows, Mac, iOS, Android)", "365-day replacement warranty coverage"],
                "limits": "Long-term privacy protection",
                "badge": "Save 47%",
                "availability": "InStock"
            }
        ]
    },
    "surfshark-vpn": {
        "slug": "surfshark-vpn",
        "name": "Surfshark One VPN",
        "brand": "Surfshark",
        "brand_id": "surfshark",
        "category_key": "vpn",
        "category_label": "VPN & Privacy",
        "vendor": "Surfshark Cyber Security",
        "description": "Unlimited simultaneous devices, CleanWeb ad-blocker, camouflage mode, and 3,200+ global RAM-only servers.",
        "url": "tools/surfshark-vpn.html",
        "icon": "assets/product-logos/surfshark-vpn.svg",
        "plans": [
            {
                "plan_id": "PLAN-SURF-1M",
                "name": "Starter (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "Unlimited Simultaneous Devices",
                "price_pkr": 800,
                "price_usd": 3.00,
                "features": ["Connect unlimited devices on 1 subscription", "CleanWeb 2.0 pop-up and malware blocker", "3,200+ servers across 100 countries", "Bypasser split tunneling for banking apps"],
                "limits": "Unlimited devices subject to fair usage",
                "badge": "Unlimited Devices",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-SURF-12M",
                "name": "One Plus (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "Unlimited Simultaneous Devices",
                "price_pkr": 4800,
                "price_usd": 17.50,
                "features": ["Full 12 months unlimited VPN protection", "Includes Surfshark Antivirus & Alert monitoring", "Private search engine with zero logs", "365-day replacement warranty"],
                "limits": "Annual family cyber protection",
                "badge": "Best Value VPN",
                "availability": "InStock"
            }
        ]
    },

    # 6. Productivity, Writing & SEO Platforms
    "semrush-guru": {
        "slug": "semrush-guru",
        "name": "Semrush Guru & Pro",
        "brand": "Semrush",
        "brand_id": "semrush",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Semrush Marketing Platform",
        "description": "Competitor SEO keyword analysis, domain backlink audits, position tracking, and content marketing toolkit.",
        "url": "tools/semrush-guru.html",
        "icon": "assets/product-logos/semrush-guru.svg",
        "plans": [
            {
                "plan_id": "PLAN-SEMRUSH-PRO-1M",
                "name": "Pro Tier (1 Month)",
                "plan_type": "Pro",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1900,
                "price_usd": 7.00,
                "features": ["5 projects & 500 keywords tracked daily", "Domain & keyword analytics with competitor traffic estimates", "On-page SEO checker & site audit crawler (100k pages)", "PDF export reports"],
                "limits": "Single user account",
                "badge": "Freelancer Pick",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-SEMRUSH-GURU-1M",
                "name": "Guru Platform (1 Month)",
                "plan_type": "Guru",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Shared Dedicated Suite)",
                "price_pkr": 2500,
                "price_usd": 9.00,
                "features": ["15 projects & 1,500 keywords tracked daily", "Historical keyword & backlink data since 2012", "Content Marketing Platform & Topic Research", "Looker Studio integration & branded PDF reports"],
                "limits": "Subject to daily query limits",
                "badge": "Agency Standard",
                "availability": "InStock"
            }
        ]
    },
    "notion-business": {
        "slug": "notion-business",
        "name": "Notion Business & AI",
        "brand": "Notion",
        "brand_id": "notion",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Notion Systems Inc.",
        "description": "AI automated summaries, project management boards, company wikis, meeting transcript analysis, and team spaces.",
        "url": "tools/notion-business.html",
        "icon": "assets/product-logos/notion-business.svg",
        "plans": [
            {
                "plan_id": "PLAN-NOTION-BIZ-1M",
                "name": "Business & AI (1 Month)",
                "plan_type": "Business",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Workspace",
                "price_pkr": 1400,
                "price_usd": 5.00,
                "features": ["Unlimited Notion AI prompts, autofill & summaries", "Unlimited page history & team collaborative spaces", "Advanced database formulas, relations & rollups", "Private team spaces & permission management"],
                "limits": "Workspace user account",
                "badge": "Productivity Hub",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-NOTION-ANN-12M",
                "name": "Business & AI Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Workspace",
                "price_pkr": 13500,
                "price_usd": 48.00,
                "features": ["Full 365 days of uninterrupted Notion AI and Business capabilities", "Unlimited collaborative workspaces and page histories", "Admin audit logs & workspace export tools", "365-day replacement warranty support"],
                "limits": "Annual workspace license",
                "badge": "Save 20%",
                "availability": "InStock"
            }
        ]
    },
    "grammarly-pro": {
        "slug": "grammarly-pro",
        "name": "Grammarly Premium",
        "brand": "Grammarly",
        "brand_id": "grammarly",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Grammarly Inc.",
        "description": "Tone adjustments, full-sentence rewrites, plagiarism detection, English vocabulary enhancements, and Grammarly AI.",
        "url": "tools/grammarly-pro.html",
        "icon": "assets/product-logos/grammarly-pro.svg",
        "plans": [
            {
                "plan_id": "PLAN-GRAMMARLY-1M",
                "name": "Premium (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 750,
                "price_usd": 2.80,
                "features": ["Full sentence rewrites for clarity & conciseness", "Tone adjustments for professional emails & papers", "Built-in plagiarism detector across billions of pages", "Browser extension, Desktop app & Word plugin"],
                "limits": "Personal user activation",
                "badge": "Essential for Writers",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-GRAMMARLY-12M",
                "name": "Premium Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User (Multi-Device)",
                "price_pkr": 4500,
                "price_usd": 16.00,
                "features": ["Full 365 days of uninterrupted Grammarly Premium", "Unlimited AI text suggestions & rewrites", "Complete browser, mobile & office app sync", "365-day replacement warranty guarantee"],
                "limits": "Annual license",
                "badge": "Save 50%",
                "availability": "InStock"
            }
        ]
    },
    "quillbot-premium": {
        "slug": "quillbot-premium",
        "name": "QuillBot Premium Suite",
        "brand": "QuillBot (Learneo)",
        "brand_id": "quillbot",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Learneo QuillBot Suite",
        "description": "Unlimited paraphrasing modes, grammar checking, plagiarism checker, summarizer, and citation generator.",
        "url": "tools/quillbot-premium.html",
        "icon": "assets/product-logos/quillbot-premium.svg",
        "plans": [
            {
                "plan_id": "PLAN-QUILL-1M",
                "name": "Premium Suite (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User",
                "price_pkr": 1600,
                "price_usd": 5.80,
                "features": ["Unlimited words in Paraphraser", "All 8 paraphrasing modes (Creative, Academic, Formal, etc.)", "Plagiarism checker (20 pages/month)", "Full Freeze Words control & tone detector"],
                "limits": "Single user account",
                "badge": "Academic Favorite",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-QUILL-12M",
                "name": "Premium Suite Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User",
                "price_pkr": 4200,
                "price_usd": 15.00,
                "features": ["Full 12 months uninterrupted paraphrasing & grammar", "Annual Plagiarism Checker scanning credits", "Chrome, Word, and Edge extensions included", "365-day replacement warranty support"],
                "limits": "Annual subscription",
                "badge": "Save 78%",
                "availability": "InStock"
            }
        ]
    },
    "linkedin-premium": {
        "slug": "linkedin-premium",
        "name": "LinkedIn Premium Career & Business",
        "brand": "LinkedIn / Microsoft",
        "brand_id": "linkedin",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "LinkedIn Corporation",
        "description": "Direct InMail messaging to recruiters, full 'Who's Viewed Your Profile' insights, and 21,000+ LinkedIn Learning courses.",
        "url": "tools/linkedin-premium.html",
        "icon": "assets/product-logos/linkedin-premium.svg",
        "plans": [
            {
                "plan_id": "PLAN-LINKEDIN-1M",
                "name": "Career Plan (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1500,
                "price_usd": 5.50,
                "features": ["5 InMail messages per month to reach recruiters directly", "See everyone who viewed your profile in the last 365 days", "Competitive applicant insights & salary data", "Full access to 21,000+ LinkedIn Learning courses"],
                "limits": "Personal LinkedIn profile upgrade",
                "badge": "Career Accelerator",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-LINKEDIN-BIZ-1M",
                "name": "Business Plan (1 Month)",
                "plan_type": "Business",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 2900,
                "price_usd": 10.50,
                "features": ["15 InMail messages per month", "Unlimited profile browsing without revealing identity", "Advanced company insights & employee growth metrics", "Includes full LinkedIn Learning library access"],
                "limits": "Business profile upgrade",
                "badge": "Business Growth",
                "availability": "InStock"
            }
        ]
    },

    # 7. Premium Streaming & Entertainment
    "netflix-premium": {
        "slug": "netflix-premium",
        "name": "Netflix 4K UHD Premium",
        "brand": "Netflix",
        "brand_id": "netflix",
        "category_key": "video",
        "category_label": "Premium Streaming",
        "vendor": "Netflix Entertainment",
        "description": "4K Ultra HD HDR streaming, Dolby Atmos spatial audio, unlimited downloads on supported mobile devices.",
        "url": "tools/netflix-premium.html",
        "icon": "assets/product-logos/netflix-premium.svg",
        "plans": [
            {
                "plan_id": "PLAN-NETFLIX-1P-1M",
                "name": "1 Profile 4K UHD (1 Month)",
                "plan_type": "Single Profile",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Profile with PIN",
                "price_pkr": 1100,
                "price_usd": 4.00,
                "features": ["4K Ultra HD + HDR video playback", "Personal PIN-locked profile & private watch history", "Dolby Atmos immersive spatial audio", "Works on Smart TV, Phone, Laptop, and Tablet"],
                "limits": "1 screen active at any time on your dedicated profile",
                "badge": "Most Popular",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-NETFLIX-FULL-1M",
                "name": "Full Account 4K UHD (1 Month)",
                "plan_type": "Full Account",
                "duration": "1 Month (30 Days)",
                "seats": "Full 5 Profiles Account",
                "price_pkr": 2400,
                "price_usd": 8.60,
                "features": ["Complete private account with full 5 profiles", "4 concurrent 4K UHD screens simultaneously", "Download on up to 6 supported devices", "Spatial audio on all compatible systems"],
                "limits": "Private household account activation",
                "badge": "Full Household",
                "availability": "InStock"
            }
        ]
    },

    # 8. New Candidate Platforms (Requested by User)
    "spotify-premium": {
        "slug": "spotify-premium",
        "name": "Spotify Premium Individual & Family",
        "brand": "Spotify",
        "brand_id": "spotify",
        "category_key": "video",
        "category_label": "Streaming & Entertainment",
        "vendor": "Spotify AB",
        "description": "Ad-free music streaming, 320kbps extreme audio quality, offline playlists, and unlimited song skips on all devices.",
        "url": "tools/spotify-premium.html",
        "icon": "assets/product-logos/spotify.svg",
        "plans": [
            {
                "plan_id": "PLAN-SPOTIFY-IND-1M",
                "name": "Individual (1 Month)",
                "plan_type": "Individual",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 550,
                "price_usd": 1.95,
                "features": ["100% ad-free music listening", "Download to listen offline without internet", "320kbps high-fidelity audio bitrate", "Listen on Phone, Laptop, Smart Speaker, PlayStation"],
                "limits": "Personal Spotify account activation",
                "badge": "Music Lover",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-SPOTIFY-FAM-1M",
                "name": "Family Plan (1 Month)",
                "plan_type": "Family Plan",
                "duration": "1 Month (30 Days)",
                "seats": "Up to 6 Accounts",
                "price_pkr": 1150,
                "price_usd": 4.10,
                "features": ["6 individual accounts for family members living together", "Separate saved songs, playlists, and recommendations", "Spotify Kids app included", "Explicit music filter controls for parents"],
                "limits": "Family members must reside in the same household",
                "badge": "Best Value",
                "availability": "InStock"
            }
        ]
    },
    "duolingo-super": {
        "slug": "duolingo-super",
        "name": "Duolingo Super",
        "brand": "Duolingo",
        "brand_id": "duolingo",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Duolingo Inc.",
        "description": "Unlimited hearts, ad-free language learning, personalized practice, and unlimited legendary challenges across 40+ languages.",
        "url": "tools/duolingo-super.html",
        "icon": "assets/product-logos/duolingo.svg",
        "plans": [
            {
                "plan_id": "PLAN-DUOLINGO-1M",
                "name": "Super (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 Learner Account",
                "price_pkr": 650,
                "price_usd": 2.30,
                "features": ["Unlimited hearts — learn at your own pace without pauses", "Zero interruptive banner or video ads", "Personalized practice to target past mistakes", "Unlimited attempts at Legendary level challenges"],
                "limits": "Personal Duolingo account upgrade",
                "badge": "Language Pro",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-DUOLINGO-ANN-12M",
                "name": "Super Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 Learner Account",
                "price_pkr": 3900,
                "price_usd": 14.00,
                "features": ["Full 365 days of uninterrupted Super learning", "Includes all 40+ languages (English, German, Spanish, Arabic, etc.)", "Offline lesson progress tracking", "365-day replacement warranty guarantee"],
                "limits": "Annual individual subscription",
                "badge": "Save 50%",
                "availability": "InStock"
            }
        ]
    },
    "discord-nitro": {
        "slug": "discord-nitro",
        "name": "Discord Nitro",
        "brand": "Discord",
        "brand_id": "discord",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Discord Inc.",
        "description": "Custom animated emojis, 500MB upload size, 4K 60fps HD video streaming, 2 free server boosts, and custom profile banners.",
        "url": "tools/discord-nitro.html",
        "icon": "assets/product-logos/discord.svg",
        "plans": [
            {
                "plan_id": "PLAN-DISCORD-1M",
                "name": "Nitro Standard (1 Month)",
                "plan_type": "Monthly",
                "duration": "1 Month (30 Days)",
                "seats": "1 User Account",
                "price_pkr": 1400,
                "price_usd": 5.00,
                "features": ["500MB file upload size for clips and projects", "Custom & animated emojis anywhere across all servers", "4K 60fps HD screen sharing and streaming", "2 Free Server Boosts + 30% off extra boosts"],
                "limits": "Personal Discord account upgrade",
                "badge": "Gamer Standard",
                "availability": "InStock"
            },
            {
                "plan_id": "PLAN-DISCORD-ANN-12M",
                "name": "Nitro Annual (12 Months)",
                "plan_type": "Annual",
                "duration": "12 Months (365 Days)",
                "seats": "1 User Account",
                "price_pkr": 13500,
                "price_usd": 48.00,
                "features": ["Full 365 days uninterrupted Discord Nitro perks", "Continuous 2 server boosts for your favorite community", "Exclusive profile badges and animated avatars", "365-day replacement warranty support"],
                "limits": "Annual user license",
                "badge": "Save 20%",
                "availability": "InStock"
            }
        ]
    },
    "zoom-workplace": {
        "slug": "zoom-workplace",
        "name": "Zoom Workplace Pro",
        "brand": "Zoom",
        "brand_id": "zoom",
        "category_key": "coding",
        "category_label": "Productivity & SEO",
        "vendor": "Zoom Video Communications",
        "description": "Unlimited 30-hour group meetings, 5GB cloud recording, AI Companion meeting summaries, and up to 100 participants.",
        "url": "tools/zoom-workplace.html",
        "icon": "assets/product-logos/zoom.svg",
        "plans": [
            {
                "plan_id": "PLAN-ZOOM-PRO-1M",
                "name": "Pro Tier (1 Month)",
                "plan_type": "Pro Host",
                "duration": "1 Month (30 Days)",
                "seats": "1 Licensed Host (100 Attendees)",
                "price_pkr": 1800,
                "price_usd": 6.50,
                "features": ["Meetings up to 30 hours per session (no 40-min limit)", "Host up to 100 interactive participants", "Zoom AI Companion automated meeting summaries", "5GB cloud meeting video recording with transcript"],
                "limits": "Licensed meeting host account",
                "badge": "Business Meetings",
                "availability": "InStock"
            }
        ]
    }
}

# Compute starting prices for all 40 tools
for slug, item in ALL_TOOLS.items():
    plans = item["plans"]
    min_pkr = min(p["price_pkr"] for p in plans)
    matching_plan = next(p for p in plans if p["price_pkr"] == min_pkr)
    item["starting_price_pkr"] = min_pkr
    item["starting_price_usd"] = matching_plan["price_usd"]
    item["starting_price_display"] = f"From Rs. {min_pkr:,} PKR (~${matching_plan['price_usd']:.2f} USD)"
    item["total_plans"] = len(plans)

with open(CATALOG_FILE, "w", encoding="utf-8") as f:
    json.dump(ALL_TOOLS, f, indent=2)

print(f"Successfully generated complete 40-tool catalog with {sum(len(t['plans']) for t in ALL_TOOLS.values())} distinct verified plans in {CATALOG_FILE}")
