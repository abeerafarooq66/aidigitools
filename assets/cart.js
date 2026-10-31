/**
 * AIDigiTools Interactive Quick Order Drawer & Living Showcase Engine
 * Canonical Multi-Plan Support.
 */

(function () {
  'use strict';

  // Canonical Catalog Data with Verified Plans
  var TOOLS_DATA = {
  "youtube-premium": {
    "slug": "youtube-premium",
    "name": "YouTube Premium",
    "brand": "Google / YouTube",
    "vendor": "YouTube & Google Inc.",
    "cat": "Streaming & Entertainment",
    "icon": "assets/product-logos/youtube-premium.svg",
    "desc": "Ad-free video streaming across mobile, TV, and desktop with background playback, offline downloads, and full YouTube Music Premium.",
    "url": "tools/youtube-premium.html",
    "starting_price_pkr": 750,
    "starting_price_usd": 2.8,
    "plans": [
      {
        "plan_id": "PLAN-YT-IND-1M",
        "name": "Individual (1 Month)",
        "plan_type": "Individual",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 750,
        "price_usd": 2.8,
        "features": [
          "100% Ad-free video playback",
          "Background audio while using other apps",
          "Offline 1080p/4K downloads",
          "YouTube Music Premium included"
        ],
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
        "price_usd": 5.2,
        "features": [
          "5 Independent member profiles with private histories",
          "Ad-free streaming across all household devices",
          "5x YouTube Music Premium accounts",
          "Offline downloads on each member device"
        ],
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
        "price_usd": 27.0,
        "features": [
          "Full 365 days uninterrupted ad-free playback",
          "Includes YouTube Music Premium for 1 year",
          "Zero monthly renewal friction",
          "30-day replacement warranty support"
        ],
        "limits": "Fixed term subscription; non-transferable",
        "badge": "Save 16%",
        "availability": "InStock"
      }
    ]
  },
  "chatgpt-plus": {
    "slug": "chatgpt-plus",
    "name": "ChatGPT Plus",
    "brand": "OpenAI",
    "vendor": "OpenAI Enterprise Systems",
    "cat": "AI Assistant & LLM",
    "icon": "assets/product-logos/chatgpt-plus.svg",
    "desc": "Frontier AI reasoning, Canvas interactive coding workspace, DALL-E image generation, Advanced Voice Mode, and custom GPT builder.",
    "url": "tools/chatgpt-plus.html",
    "starting_price_pkr": 2300,
    "starting_price_usd": 8.0,
    "plans": [
      {
        "plan_id": "PLAN-GPT-PLUS-1M",
        "name": "ChatGPT Plus (1 Month)",
        "plan_type": "Individual",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2300,
        "price_usd": 8.0,
        "features": [
          "Access to GPT-5/GPT-6, o1/o3 reasoning, and GPT-4o fallback",
          "Advanced Voice Mode on iOS & Android",
          "DALL-E image generation & Canvas visual synthesis",
          "File analysis, web browsing & custom GPTs"
        ],
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
        "price_usd": 17.0,
        "features": [
          "Higher message limits on GPT-5/GPT-6 and o1/o3",
          "Dedicated collaborative workspace & admin console",
          "Shared custom GPTs within organization",
          "Zero model training on proprietary business data"
        ],
        "limits": "Team workspace terms apply",
        "badge": "Business Grade",
        "availability": "InStock"
      }
    ]
  },
  "claude-pro": {
    "slug": "claude-pro",
    "name": "Claude Pro",
    "brand": "Anthropic",
    "vendor": "Anthropic AI Systems",
    "cat": "AI Assistant & LLM",
    "icon": "assets/product-logos/claude-pro.svg",
    "desc": "Frontier technical reasoning, 200K token context window, Projects workspace, Artifacts rendering, and priority server access.",
    "url": "tools/claude-pro.html",
    "starting_price_pkr": 2500,
    "starting_price_usd": 9.0,
    "plans": [
      {
        "plan_id": "PLAN-CLAUDE-PRO-1M",
        "name": "Claude Pro (1 Month)",
        "plan_type": "Individual",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2500,
        "price_usd": 9.0,
        "features": [
          "5x higher usage limits vs free Claude tier",
          "Claude Sonnet 5.5 & Claude 3.5 Haiku models",
          "Interactive split-screen Artifacts live runner",
          "Early access to new Anthropic features"
        ],
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
        "price_usd": 18.5,
        "features": [
          "Higher per-user usage limits on Sonnet",
          "Team management & centralized billing",
          "Collaborative project sharing & prompt libraries",
          "Enterprise privacy guarantees"
        ],
        "limits": "Requires organization workspace setup",
        "badge": "Team Collab",
        "availability": "InStock"
      }
    ]
  },
  "canva-pro": {
    "slug": "canva-pro",
    "name": "Canva Pro",
    "brand": "Canva",
    "vendor": "Canva Design Platform",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/canva-pro.svg",
    "desc": "Professional visual design suite with 100M+ premium stock assets, 1 TB cloud storage, Brand Kits, and Magic Studio AI editing.",
    "url": "tools/canva-pro.html",
    "starting_price_pkr": 600,
    "starting_price_usd": 2.5,
    "plans": [
      {
        "plan_id": "PLAN-CANVA-1M",
        "name": "Canva Pro (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 600,
        "price_usd": 2.5,
        "features": [
          "Unlimited 1-click Magic Background Remover",
          "100M+ premium stock photos, videos, and graphics",
          "1TB secure cloud storage for brand assets",
          "Brand Kit color palettes, logos, and custom fonts"
        ],
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
        "price_usd": 7.9,
        "features": [
          "Full 12 months uninterrupted Pro access",
          "Unlimited Magic Studio AI tools & downloads",
          "Complete Brand Kit & 1TB cloud storage",
          "30-day replacement warranty support"
        ],
        "limits": "Annual term with zero renewal hassles",
        "badge": "Save 70%",
        "availability": "InStock"
      }
    ]
  },
  "capcut-pro": {
    "slug": "capcut-pro",
    "name": "CapCut Pro",
    "brand": "ByteDance / CapCut",
    "vendor": "ByteDance Creative Studio",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/capcut-pro.svg",
    "desc": "Advanced multi-track video editor with AI auto-captions, smart background removal, 4K 60fps exports, and premium motion transitions.",
    "url": "tools/capcut-pro.html",
    "starting_price_pkr": 950,
    "starting_price_usd": 3.5,
    "plans": [
      {
        "plan_id": "PLAN-CAPCUT-1M",
        "name": "CapCut Pro (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User (Multi-Device)",
        "price_pkr": 950,
        "price_usd": 3.5,
        "features": [
          "Auto captions with bilingual word-level sync",
          "4K 60fps optical flow ultra-smooth rendering",
          "Smart AI body cutout & green screen remover",
          "100GB CapCut cloud space for multi-device sync"
        ],
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
        "price_usd": 21.0,
        "features": [
          "Full 12 months uninterrupted Pro access",
          "Unlimited 4K exports & premium transitions",
          "100GB cloud project backup",
          "30-day replacement warranty support"
        ],
        "limits": "Non-transferable annual license",
        "badge": "Save 48%",
        "availability": "InStock"
      }
    ]
  },
  "midjourney": {
    "slug": "midjourney",
    "name": "Midjourney V8",
    "brand": "Midjourney",
    "vendor": "Midjourney Research Lab",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/midjourney.svg",
    "desc": "Leading photorealistic AI image generator featuring coherent text rendering, nuanced human textures, and web canvas inpainting.",
    "url": "tools/midjourney.html",
    "starting_price_pkr": 2800,
    "starting_price_usd": 10.0,
    "plans": [
      {
        "plan_id": "PLAN-MIDJ-BASIC-1M",
        "name": "Basic Plan (1 Month)",
        "plan_type": "Basic",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2800,
        "price_usd": 10.0,
        "features": [
          "200 Fast GPU minutes (~200 images)",
          "General commercial usage terms",
          "Access to member web gallery",
          "Direct messaging bot access"
        ],
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
        "features": [
          "15 Fast GPU hours (~1,000 images)",
          "Unlimited Relax GPU mode generation",
          "General commercial terms",
          "Web gallery & inpainting editor"
        ],
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
        "price_usd": 20.0,
        "features": [
          "30 Fast GPU hours (~2,000 images)",
          "Stealth mode (keep generations private)",
          "Unlimited Relax GPU mode",
          "12 concurrent Fast jobs"
        ],
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
    "vendor": "Adobe Creative Cloud Platform",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/adobe-creative-cloud.svg",
    "desc": "Complete suite of 20+ desktop and mobile creative apps including Photoshop, Illustrator, Premiere Pro, and After Effects with Firefly generative credits.",
    "url": "tools/adobe-creative-cloud.html",
    "starting_price_pkr": 1400,
    "starting_price_usd": 5.5,
    "plans": [
      {
        "plan_id": "PLAN-ADOBE-CC-1M",
        "name": "All Apps (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User (2 Devices Active)",
        "price_pkr": 1400,
        "price_usd": 5.5,
        "features": [
          "Access to 20+ desktop & mobile creative apps",
          "Adobe Firefly AI generative credits",
          "100GB Adobe cloud storage",
          "Adobe Fonts library with 20,000+ typefaces"
        ],
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
        "price_usd": 50.0,
        "features": [
          "Full 12 months access to entire Creative Cloud suite",
          "Monthly Firefly AI credit renewals",
          "100GB cloud asset synchronization",
          "30-day replacement warranty support"
        ],
        "limits": "Annual license with uninterrupted activation",
        "badge": "Agency Value",
        "availability": "InStock"
      }
    ]
  },
  "nordvpn": {
    "slug": "nordvpn",
    "name": "NordVPN Standard",
    "brand": "Nord Security",
    "vendor": "Nord Security Systems",
    "cat": "VPN & Privacy",
    "icon": "assets/product-logos/nordvpn.svg",
    "desc": "High-speed encrypted virtual private network with 6,000+ servers in 111 countries, Threat Protection malware blocking, and zero-logs security.",
    "url": "tools/nordvpn.html",
    "starting_price_pkr": 850,
    "starting_price_usd": 3.0,
    "plans": [
      {
        "plan_id": "PLAN-NORD-1M",
        "name": "Standard (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "Up to 10 Simultaneous Devices",
        "price_pkr": 850,
        "price_usd": 3.0,
        "features": [
          "Ultra-fast NordLynx protocol with zero logs",
          "Access to 6,400+ servers in 111 countries",
          "Double VPN & Onion Over VPN routing",
          "Threat Protection malware & ad blocking"
        ],
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
        "price_usd": 19.5,
        "features": [
          "Full 365 days secure high-speed browsing",
          "Includes 1TB encrypted cloud storage",
          "Cross-platform apps (Windows, Mac, iOS, Android)",
          "30-day replacement warranty support"
        ],
        "limits": "Long-term privacy protection",
        "badge": "Save 47%",
        "availability": "InStock"
      }
    ]
  },
  "surfshark-vpn": {
    "slug": "surfshark-vpn",
    "name": "Surfshark VPN",
    "brand": "Surfshark",
    "vendor": "Surfshark Cyber Security",
    "cat": "VPN & Privacy",
    "icon": "assets/product-logos/surfshark-vpn.svg",
    "desc": "Fast virtual private network supporting unlimited simultaneous device connections, CleanWeb ad blocking, and 3,200+ global RAM-only servers.",
    "url": "tools/surfshark-vpn.html",
    "starting_price_pkr": 800,
    "starting_price_usd": 3.0,
    "plans": [
      {
        "plan_id": "PLAN-SURF-1M",
        "name": "Starter (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "Unlimited Simultaneous Devices",
        "price_pkr": 800,
        "price_usd": 3.0,
        "features": [
          "Connect unlimited devices on 1 subscription",
          "CleanWeb 2.0 pop-up and malware blocker",
          "3,200+ servers across 100 countries",
          "Bypasser split tunneling for banking apps"
        ],
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
        "price_usd": 17.5,
        "features": [
          "Full 12 months unlimited VPN protection",
          "Includes Surfshark Antivirus & Alert monitoring",
          "Private search engine with zero logs",
          "30-day replacement warranty support"
        ],
        "limits": "Annual family cyber protection",
        "badge": "Best Value VPN",
        "availability": "InStock"
      }
    ]
  },
  "cursor-pro": {
    "slug": "cursor-pro",
    "name": "Cursor Pro",
    "brand": "Anysphere (Cursor)",
    "vendor": "Anysphere AI Lab",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/cursor-pro.svg",
    "desc": "AI-first code editor with multi-file Composer, predictive Cursor Tab autocompletion, codebase indexing, and frontier LLM integration.",
    "url": "tools/cursor-pro.html",
    "starting_price_pkr": 3800,
    "starting_price_usd": 13.5,
    "plans": [
      {
        "plan_id": "PLAN-CURSOR-1M",
        "name": "Cursor Pro (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer Account",
        "price_pkr": 3800,
        "price_usd": 13.5,
        "features": [
          "500 Fast Premium requests / month (Claude Sonnet 5.5 & GPT-5/4o)",
          "Unlimited Slow requests after fast quota",
          "Multi-file Composer codebase refactoring",
          "Smart line and multi-line code auto-complete"
        ],
        "limits": "Individual developer seat",
        "badge": "Developer Choice",
        "availability": "InStock"
      }
    ]
  },
  "perplexity-pro": {
    "slug": "perplexity-pro",
    "name": "Perplexity Pro",
    "brand": "Perplexity AI",
    "vendor": "Perplexity AI Systems",
    "cat": "AI Assistant & LLM",
    "icon": "assets/product-logos/perplexity-pro.svg",
    "desc": "Conversational answer engine with multi-model switching, unlimited Pro searches, deep document analysis, and verifiable inline citations.",
    "url": "tools/perplexity-pro.html",
    "starting_price_pkr": 2200,
    "starting_price_usd": 8.0,
    "plans": [
      {
        "plan_id": "PLAN-PERP-1M",
        "name": "Perplexity Pro (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2200,
        "price_usd": 8.0,
        "features": [
          "600+ Pro Searches / day with multi-step reasoning",
          "Model switcher: Claude Sonnet 5.5, GPT-5/4o, Sonar Large",
          "Unlimited file and PDF research uploads",
          "Includes $5/month API credits"
        ],
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
        "price_usd": 59.0,
        "features": [
          "Full 12 months uninterrupted Pro research",
          "All premium AI models unlocked",
          "Priority processing & zero search queue",
          "30-day replacement warranty support"
        ],
        "limits": "Annual subscription",
        "badge": "Save 37%",
        "availability": "InStock"
      }
    ]
  },
  "elevenlabs-creator": {
    "slug": "elevenlabs-creator",
    "name": "ElevenLabs Creator",
    "brand": "ElevenLabs",
    "vendor": "ElevenLabs Voice AI",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/elevenlabs-creator.svg",
    "desc": "Studio-grade AI voice synthesis, professional voice cloning, Dubbing Studio, and 100,000 monthly characters for content creators.",
    "url": "tools/elevenlabs-creator.html",
    "starting_price_pkr": 2800,
    "starting_price_usd": 10.0,
    "plans": [
      {
        "plan_id": "PLAN-11LABS-CREATOR-1M",
        "name": "Creator Plan (1 Month)",
        "plan_type": "Creator",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2800,
        "price_usd": 10.0,
        "features": [
          "100,000 characters per month (~2 hours of audio)",
          "Create up to 30 custom instant voice clones",
          "Commercial rights for YouTube & podcasts",
          "192kbps ultra-high quality audio export"
        ],
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
        "price_usd": 23.5,
        "features": [
          "500,000 characters per month (~10 hours of audio)",
          "Professional Voice Cloning (PVC) enabled",
          "160 custom voices & priority rendering",
          "Commercial rights across all broadcast media"
        ],
        "limits": "Professional voice tier",
        "badge": "Studio Pro",
        "availability": "InStock"
      }
    ]
  },
  "deepseek-pro": {
    "slug": "deepseek-pro",
    "name": "DeepSeek Platform",
    "brand": "DeepSeek",
    "vendor": "DeepSeek AI Research",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/deepseek-pro.svg",
    "desc": "Cost-effective open-weights reasoning and high-throughput chat platform powered by DeepSeek-R1 and V3 architecture for developers.",
    "url": "tools/deepseek-pro.html",
    "starting_price_pkr": 1100,
    "starting_price_usd": 4.0,
    "plans": [
      {
        "plan_id": "PLAN-DEEPSEEK-1M",
        "name": "R1 / V3 Pro Tier (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 1100,
        "price_usd": 4.0,
        "features": [
          "Full access to DeepSeek-R1 reasoning model",
          "DeepSeek-V3 MoE 671B architecture",
          "Zero queue delays during peak traffic",
          "High context coding and math capabilities"
        ],
        "limits": "Fair usage limits apply",
        "badge": "Open Reasoning",
        "availability": "InStock"
      }
    ]
  },
  "netflix-premium": {
    "slug": "netflix-premium",
    "name": "Netflix Premium",
    "brand": "Netflix",
    "vendor": "Netflix Entertainment",
    "cat": "Premium Streaming",
    "icon": "assets/product-logos/netflix-premium.svg",
    "desc": "4K Ultra HD streaming, HDR visual fidelity, Spatial Audio, and downloads across 6 household devices simultaneously.",
    "url": "tools/netflix-premium.html",
    "starting_price_pkr": 1100,
    "starting_price_usd": 4.0,
    "plans": [
      {
        "plan_id": "PLAN-NETFLIX-1P-1M",
        "name": "1 Profile 4K UHD (1 Month)",
        "plan_type": "Single Profile",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Profile with PIN",
        "price_pkr": 1100,
        "price_usd": 4.0,
        "features": [
          "4K Ultra HD + HDR video playback",
          "Personal PIN-locked profile & private watch history",
          "Dolby Atmos immersive spatial audio",
          "Works on Smart TV, Phone, Laptop, and Tablet"
        ],
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
        "price_usd": 8.6,
        "features": [
          "Complete private account with full 5 profiles",
          "4 concurrent 4K UHD screens simultaneously",
          "Download on up to 6 supported devices",
          "Spatial audio on all compatible systems"
        ],
        "limits": "Private household account activation",
        "badge": "Full Household",
        "availability": "InStock"
      }
    ]
  },
  "suno-ai": {
    "slug": "suno-ai",
    "name": "Suno AI Music",
    "brand": "Suno AI",
    "vendor": "Suno AI Audio Systems",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/suno-ai.svg",
    "desc": "Generative AI music studio creating full 2-minute vocal and instrumental songs across any genre with commercial ownership rights.",
    "url": "tools/suno-ai.html",
    "starting_price_pkr": 2600,
    "starting_price_usd": 9.5,
    "plans": [
      {
        "plan_id": "PLAN-SUNO-PRO-1M",
        "name": "Pro Plan (1 Month)",
        "plan_type": "Pro",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2600,
        "price_usd": 9.5,
        "features": [
          "2,500 credits / month (~500 songs)",
          "General commercial terms for streaming monetization",
          "Priority generation queue & audio stem separation",
          "Upload audio clips to extend songs"
        ],
        "limits": "Commercial terms apply while subscribed",
        "badge": "Musician Choice",
        "availability": "InStock"
      }
    ]
  },
  "runway-gen3": {
    "slug": "runway-gen3",
    "name": "Runway AI Video",
    "brand": "Runway",
    "vendor": "Runway AI Motion Engine",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/runway-gen3.svg",
    "desc": "Frontier generative video suite with keyframe camera control, multi-directional motion brush, Act-Two expression transfer, and 4K upscaling.",
    "url": "tools/runway-gen3.html",
    "starting_price_pkr": 1800,
    "starting_price_usd": 6.5,
    "plans": [
      {
        "plan_id": "PLAN-RUNWAY-STD-1M",
        "name": "Standard (1 Month)",
        "plan_type": "Standard",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1800,
        "price_usd": 6.5,
        "features": [
          "625 credits / month (~125 seconds of Gen-3 video)",
          "Motion Brush & camera control tools",
          "Export up to 4K resolution with watermark removal",
          "Train 1 custom voice or portrait generator"
        ],
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
        "price_usd": 17.5,
        "features": [
          "Unlimited relaxed video generations",
          "2,250 monthly Fast credits",
          "Full commercial video licensing rights",
          "Priority enterprise rendering tier"
        ],
        "limits": "Relaxed queue speed varies by load",
        "badge": "Pro Studio",
        "availability": "InStock"
      }
    ]
  },
  "semrush-guru": {
    "slug": "semrush-guru",
    "name": "Semrush Guru",
    "brand": "Semrush",
    "vendor": "Semrush Marketing Platform",
    "cat": "Productivity & SEO",
    "icon": "assets/product-logos/semrush-guru.svg",
    "desc": "Comprehensive digital intelligence suite with historical keyword analytics, topic research, backlink audits, and Content Marketing toolkit.",
    "url": "tools/semrush-guru.html",
    "starting_price_pkr": 2500,
    "starting_price_usd": 9.0,
    "plans": [
      {
        "plan_id": "PLAN-SEMRUSH-GURU-1M",
        "name": "Guru Platform (1 Month)",
        "plan_type": "Guru",
        "duration": "1 Month (30 Days)",
        "seats": "1 User (Shared Dedicated Suite)",
        "price_pkr": 2500,
        "price_usd": 9.0,
        "features": [
          "15 projects & 1,500 keywords tracked daily",
          "Historical keyword & backlink data since 2012",
          "Content Marketing Platform & Topic Research",
          "Looker Studio integration & branded PDF reports"
        ],
        "limits": "Subject to daily query limits",
        "badge": "SEO Agency Standard",
        "availability": "InStock"
      },
      {
        "plan_id": "PLAN-SEMRUSH-PRO-1M",
        "name": "Pro Tier (1 Month)",
        "plan_type": "Pro",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1900,
        "price_usd": 7.0,
        "features": [
          "5 projects & 500 keywords tracked daily",
          "Domain & keyword analytics with competitor traffic estimates",
          "On-page SEO checker & site audit crawler (100k pages)",
          "PDF export reports"
        ],
        "limits": "Single user account terms apply",
        "badge": "Freelancer Pick",
        "availability": "InStock"
      }
    ]
  },
  "notion-business": {
    "slug": "notion-business",
    "name": "Notion Plus AI",
    "brand": "Notion",
    "vendor": "Notion Systems Inc.",
    "cat": "Productivity & SEO",
    "icon": "assets/product-logos/notion-business.svg",
    "desc": "Connected collaborative workspace combining docs, project wikis, relational databases, and enterprise-wide Notion AI semantic Q&A.",
    "url": "tools/notion-business.html",
    "starting_price_pkr": 1400,
    "starting_price_usd": 5.0,
    "plans": [
      {
        "plan_id": "PLAN-NOTION-BIZ-1M",
        "name": "Business & AI (1 Month)",
        "plan_type": "Business",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Workspace",
        "price_pkr": 1400,
        "price_usd": 5.0,
        "features": [
          "Unlimited Notion AI prompts, autofill & summaries",
          "Unlimited page history & team collaborative spaces",
          "Advanced database formulas, relations & rollups",
          "Private team spaces & permission management"
        ],
        "limits": "Workspace user account",
        "badge": "Productivity Hub",
        "availability": "InStock"
      }
    ]
  },
  "grammarly-pro": {
    "slug": "grammarly-pro",
    "name": "Grammarly Premium",
    "brand": "Grammarly",
    "vendor": "Grammarly Inc.",
    "cat": "Productivity & SEO",
    "icon": "assets/product-logos/grammarly-pro.svg",
    "desc": "Comprehensive writing assistant with real-time tone adjustments, full-sentence rewrites, vocabulary enhancements, and plagiarism checking.",
    "url": "tools/grammarly-pro.html",
    "starting_price_pkr": 750,
    "starting_price_usd": 2.8,
    "plans": [
      {
        "plan_id": "PLAN-GRAMMARLY-1M",
        "name": "Premium (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User (Multi-Device)",
        "price_pkr": 750,
        "price_usd": 2.8,
        "features": [
          "Full sentence rewrites for clarity & conciseness",
          "Tone adjustments for professional emails & papers",
          "Built-in plagiarism detector across billions of pages",
          "Browser extension, Desktop app & Word plugin"
        ],
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
        "price_usd": 16.0,
        "features": [
          "Full 365 days of uninterrupted Grammarly Premium",
          "Unlimited AI text suggestions & rewrites",
          "Complete browser, mobile & office app sync",
          "30-day replacement warranty support"
        ],
        "limits": "Annual license",
        "badge": "Save 50%",
        "availability": "InStock"
      }
    ]
  },
  "quillbot-premium": {
    "slug": "quillbot-premium",
    "name": "QuillBot Premium",
    "brand": "QuillBot (Learneo)",
    "vendor": "Learneo QuillBot Suite",
    "cat": "Productivity & SEO",
    "icon": "assets/product-logos/quillbot-premium.svg",
    "desc": "AI writing enhancement tool with unlimited paraphrasing modes, custom vocabulary sliders, citation generator, and academic tone adjustment.",
    "url": "tools/quillbot-premium.html",
    "starting_price_pkr": 1600,
    "starting_price_usd": 5.8,
    "plans": [
      {
        "plan_id": "PLAN-QUILL-1M",
        "name": "Premium Suite (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1600,
        "price_usd": 5.8,
        "features": [
          "Unlimited words in Paraphraser",
          "All 8 paraphrasing modes (Creative, Academic, Formal, etc.)",
          "Plagiarism checker (20 pages/month)",
          "Full Freeze Words control & tone detector"
        ],
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
        "price_usd": 15.0,
        "features": [
          "Full 12 months uninterrupted paraphrasing & grammar",
          "Annual Plagiarism Checker scanning credits",
          "Chrome, Word, and Edge extensions included",
          "30-day replacement warranty support"
        ],
        "limits": "Annual subscription",
        "badge": "Save 78%",
        "availability": "InStock"
      }
    ]
  },
  "github-copilot": {
    "slug": "github-copilot",
    "name": "GitHub Copilot",
    "brand": "GitHub / Microsoft",
    "vendor": "GitHub Inc.",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/github-copilot.svg",
    "desc": "AI pair programmer embedded in VS Code, Visual Studio, and JetBrains with multi-model model selection and pull request assistance.",
    "url": "tools/github-copilot.html",
    "starting_price_pkr": 1500,
    "starting_price_usd": 5.5,
    "plans": [
      {
        "plan_id": "PLAN-COPILOT-1M",
        "name": "Copilot Individual (1 Month)",
        "plan_type": "Individual",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer Account",
        "price_pkr": 1500,
        "price_usd": 5.5,
        "features": [
          "Real-time whole line & function autocompletions",
          "Copilot Chat in VS Code and JetBrains IDEs",
          "CLI command generator & code explanations",
          "Public code filter to avoid copyright matches"
        ],
        "limits": "Personal GitHub account linkage",
        "badge": "Coder Essential",
        "availability": "InStock"
      }
    ]
  },
  "figma-pro": {
    "slug": "figma-pro",
    "name": "Figma Professional",
    "brand": "Figma",
    "vendor": "Figma Design Systems",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/figma-pro.svg",
    "desc": "Industry-standard collaborative interface design tool with unlimited version history, team design libraries, and Dev Mode handoff.",
    "url": "tools/figma-pro.html",
    "starting_price_pkr": 1800,
    "starting_price_usd": 6.5,
    "plans": [
      {
        "plan_id": "PLAN-FIGMA-1M",
        "name": "Professional (1 Month)",
        "plan_type": "Professional",
        "duration": "1 Month (30 Days)",
        "seats": "1 Editor Seat",
        "price_pkr": 1800,
        "price_usd": 6.5,
        "features": [
          "Unlimited Figma files & version history",
          "Shared team component libraries & Design Systems",
          "Advanced Dev Mode for CSS/Swift/Kotlin inspect",
          "Private project spaces & prototype sharing"
        ],
        "limits": "Professional editor seat",
        "badge": "UI/UX Standard",
        "availability": "InStock"
      }
    ]
  },
  "envato-elements": {
    "slug": "envato-elements",
    "name": "Envato Elements",
    "brand": "Envato",
    "vendor": "Envato Pty Ltd.",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/envato-elements.svg",
    "desc": "Unlimited digital asset downloads including video templates, graphic mockups, sound effects, presentation decks, and WordPress themes.",
    "url": "tools/envato-elements.html",
    "starting_price_pkr": 2600,
    "starting_price_usd": 9.5,
    "plans": [
      {
        "plan_id": "PLAN-ENVATO-1M",
        "name": "Individual (1 Month Unlimited)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User (Unlimited Downloads)",
        "price_pkr": 2600,
        "price_usd": 9.5,
        "features": [
          "Unlimited downloads of 15M+ creative assets",
          "After Effects & Premiere Pro video templates",
          "Royalty-free commercial music & sound FX",
          "3D assets, fonts, graphics & WordPress themes"
        ],
        "limits": "Lifetime commercial license for downloaded items",
        "badge": "Unlimited Assets",
        "availability": "InStock"
      }
    ]
  },
  "freepik-premium": {
    "slug": "freepik-premium",
    "name": "Freepik Premium",
    "brand": "Freepik Company",
    "vendor": "Freepik Company",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/freepik-premium.svg",
    "desc": "High-resolution vector graphics, editable PSD templates, stock photography, and Freepik Pikaso real-time AI image generation.",
    "url": "tools/freepik-premium.html",
    "starting_price_pkr": 1800,
    "starting_price_usd": 6.5,
    "plans": [
      {
        "plan_id": "PLAN-FREEPIK-1M",
        "name": "Premium (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1800,
        "price_usd": 6.5,
        "features": [
          "100 daily downloads of Premium vectors, PSDs & photos",
          "Zero attribution required with full commercial rights",
          "Freepik Pikaso real-time AI image generator",
          "Ad-free high-speed browsing and downloads"
        ],
        "limits": "100 downloads daily limit per policy",
        "badge": "Designer Favorite",
        "availability": "InStock"
      }
    ]
  },
  "jetbrains-all": {
    "slug": "jetbrains-all",
    "name": "JetBrains All Products",
    "brand": "JetBrains",
    "vendor": "JetBrains s.r.o.",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/jetbrains-all.svg",
    "desc": "Complete ecosystem of professional developer IDEs including IntelliJ IDEA Ultimate, PyCharm Pro, WebStorm, Rider, and GoLand.",
    "url": "tools/jetbrains-all.html",
    "starting_price_pkr": 2500,
    "starting_price_usd": 9.0,
    "plans": [
      {
        "plan_id": "PLAN-JETBRAINS-1M",
        "name": "All Products Pack (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer (Multi-Device)",
        "price_pkr": 2500,
        "price_usd": 9.0,
        "features": [
          "All 16 JetBrains IDEs: IntelliJ, PyCharm, WebStorm, CLion, Rider, GoLand, etc.",
          "Full commercial development rights",
          "JetBrains AI Assistant integration",
          "Cross-platform support on Windows, macOS & Linux"
        ],
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
        "price_usd": 64.0,
        "features": [
          "Full 365 days access to entire JetBrains product family",
          "Includes all major version upgrades during term",
          "Perpetual fallback license rights eligible",
          "30-day replacement warranty support"
        ],
        "limits": "Annual developer license",
        "badge": "Save 40%",
        "availability": "InStock"
      }
    ]
  },
  "replit-core": {
    "slug": "replit-core",
    "name": "Replit Core",
    "brand": "Replit",
    "vendor": "Replit Cloud Development",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/replit-core.svg",
    "desc": "Cloud collaborative development environment with persistent backend servers, custom domains, PostgreSQL database, and Replit Agent.",
    "url": "tools/replit-core.html",
    "starting_price_pkr": 2800,
    "starting_price_usd": 10.0,
    "plans": [
      {
        "plan_id": "PLAN-REPLIT-1M",
        "name": "Core Tier (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer Workspace",
        "price_pkr": 2800,
        "price_usd": 10.0,
        "features": [
          "Unlimited basic Repls & collaborative coding",
          "Replit AI code completion and codebase chat",
          "Fast cloud VMs with 4x memory and 2x vCPU",
          "Persistent background apps and deployments"
        ],
        "limits": "Cloud deployment credits per tier",
        "badge": "Cloud IDE",
        "availability": "InStock"
      }
    ]
  },
  "linkedin-premium": {
    "slug": "linkedin-premium",
    "name": "LinkedIn Premium",
    "brand": "LinkedIn / Microsoft",
    "vendor": "LinkedIn Corporation",
    "cat": "Productivity & SEO",
    "icon": "assets/product-logos/linkedin-premium.svg",
    "desc": "Professional career enhancement tool with InMail message credits, profile visitor insights, applicant competitive benchmarks, and LinkedIn Learning.",
    "url": "tools/linkedin-premium.html",
    "starting_price_pkr": 1500,
    "starting_price_usd": 5.5,
    "plans": [
      {
        "plan_id": "PLAN-LINKEDIN-1M",
        "name": "Career Plan (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 1500,
        "price_usd": 5.5,
        "features": [
          "5 InMail messages per month to reach recruiters directly",
          "See everyone who viewed your profile in the last 365 days",
          "Competitive applicant insights & salary data",
          "Full access to 21,000+ LinkedIn Learning courses"
        ],
        "limits": "Personal LinkedIn profile upgrade",
        "badge": "Career Accelerator",
        "availability": "InStock"
      }
    ]
  },
  "gemini-advanced": {
    "slug": "gemini-advanced",
    "name": "Google AI Pro",
    "brand": "Google",
    "vendor": "Google DeepMind Systems",
    "cat": "AI Assistant & LLM",
    "icon": "assets/product-logos/gemini-advanced.svg",
    "desc": "Google's premier multimodal AI assistant with 1M token context, Gemini Live voice chat, Deep Research agent, and 2 TB cloud storage.",
    "url": "tools/gemini-advanced.html",
    "starting_price_pkr": 1200,
    "starting_price_usd": 4.5,
    "plans": [
      {
        "plan_id": "PLAN-GEMINI-1M",
        "name": "Advanced (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 1200,
        "price_usd": 4.5,
        "features": [
          "Gemini 1.5 Pro with industry-first 2M token context",
          "Deep reasoning across 1,500 pages of documents or 1 hr video",
          "Gemini integrated directly into Gmail, Docs, and Sheets",
          "2TB secure Google One cloud storage"
        ],
        "limits": "Google account activation",
        "badge": "2M Context",
        "availability": "InStock"
      }
    ]
  },
  "grok-ai": {
    "slug": "grok-ai",
    "name": "xAI Grok",
    "brand": "xAI",
    "vendor": "xAI Corporation",
    "cat": "AI Assistant & LLM",
    "icon": "assets/product-logos/grok-ai.svg",
    "desc": "Real-time AI reasoning assistant with direct access to live X platform telemetry, uncensored analysis, and Aurora image generation.",
    "url": "tools/grok-ai.html",
    "starting_price_pkr": 1100,
    "starting_price_usd": 4.0,
    "plans": [
      {
        "plan_id": "PLAN-GROK-1M",
        "name": "SuperGrok / Grok 3 (1 Month)",
        "plan_type": "Monthly",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1100,
        "price_usd": 4.0,
        "features": [
          "Real-time trending news synthesis from global posts",
          "Uncensored Flux.1 photorealistic image generation",
          "Grok 3 frontier reasoning and code interpretation",
          "X Premium badge & reduced ads on timeline"
        ],
        "limits": "Personal user account",
        "badge": "Real-Time AI",
        "availability": "InStock"
      }
    ]
  },
  "kling-ai": {
    "slug": "kling-ai",
    "name": "Kling AI Pro",
    "brand": "Kuaishou Kling AI",
    "vendor": "Kuaishou Kling AI Lab",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/kling-ai.svg",
    "desc": "Next-generation video generation engine rendering 10-second continuous scenes, fluid biological movement, and 1080p/4K HDR video.",
    "url": "tools/kling-ai.html",
    "starting_price_pkr": 700,
    "starting_price_usd": 2.5,
    "plans": [
      {
        "plan_id": "PLAN-KLING-1M",
        "name": "Pro Tier (1 Month)",
        "plan_type": "Pro",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 700,
        "price_usd": 2.5,
        "features": [
          "660 credits / month for 1080p AI video generation",
          "Up to 10-second continuous motion sequences",
          "Motion Brush & camera trajectory controls",
          "No watermark exports in full 1080p"
        ],
        "limits": "Credit pool valid for 30 days",
        "badge": "High Motion",
        "availability": "InStock"
      }
    ]
  },
  "leonardo-ai": {
    "slug": "leonardo-ai",
    "name": "Leonardo.Ai Apprentice",
    "brand": "Leonardo.Ai / Canva",
    "vendor": "Leonardo Interactive Pty",
    "cat": "Design & Creative",
    "icon": "assets/product-logos/leonardo-ai.svg",
    "desc": "Creative asset generation suite offering custom model training, photorealistic rendering, canvas inpainting, and motion video generation.",
    "url": "tools/leonardo-ai.html",
    "starting_price_pkr": 1300,
    "starting_price_usd": 4.8,
    "plans": [
      {
        "plan_id": "PLAN-LEONARDO-1M",
        "name": "Apprentice Plan (1 Month)",
        "plan_type": "Apprentice",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1300,
        "price_usd": 4.8,
        "features": [
          "8,500 Fast generation tokens per month",
          "Realtime Canvas sketch-to-image synthesis",
          "Train up to 10 custom fine-tuned AI models",
          "Full commercial usage terms for game & graphic design"
        ],
        "limits": "Tokens refresh monthly",
        "badge": "Game & Concept Art",
        "availability": "InStock"
      }
    ]
  },
  "minimax-ai": {
    "slug": "minimax-ai",
    "name": "Hailuo AI Video",
    "brand": "MiniMax",
    "vendor": "MiniMax Intelligent Lab",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/minimax-ai.svg",
    "desc": "Cinematic text-to-video and image-to-video generation with realistic physical dynamics, fluid camera movements, and high character consistency.",
    "url": "tools/minimax-ai.html",
    "starting_price_pkr": 1600,
    "starting_price_usd": 5.8,
    "plans": [
      {
        "plan_id": "PLAN-MINIMAX-1M",
        "name": "Standard Video Tier (1 Month)",
        "plan_type": "Standard",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1600,
        "price_usd": 5.8,
        "features": [
          "Priority generation queue for Hailuo AI video model",
          "720p and 1080p high dynamic range motion video",
          "Accurate human face and hand kinetic physics",
          "Fast text-to-video & image-to-video generation"
        ],
        "limits": "Personal creator account",
        "badge": "Cinematic AI",
        "availability": "InStock"
      }
    ]
  },
  "udio-ai": {
    "slug": "udio-ai",
    "name": "Udio Standard",
    "brand": "Udio AI",
    "vendor": "Udio AI Music Lab",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/udio-ai.svg",
    "desc": "High-fidelity AI music generation engine with stem separation, audio inpainting, genre blending, and commercial music licensing.",
    "url": "tools/udio-ai.html",
    "starting_price_pkr": 2800,
    "starting_price_usd": 10.0,
    "plans": [
      {
        "plan_id": "PLAN-UDIO-1M",
        "name": "Standard Tier (1 Month)",
        "plan_type": "Standard",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 2800,
        "price_usd": 10.0,
        "features": [
          "1,200 monthly creation credits (~240 songs)",
          "Stereo audio stem downloads (vocals, drums, bass, synth)",
          "Advanced audio inpainting & track extension up to 15 mins",
          "Commercial rights for music distribution on Spotify/Apple"
        ],
        "limits": "Standard generation queue",
        "badge": "Studio Master",
        "availability": "InStock"
      }
    ]
  },
  "google-veo": {
    "slug": "google-veo",
    "name": "Google Veo 3.1",
    "brand": "Google DeepMind",
    "vendor": "Google DeepMind Video Lab",
    "cat": "AI Video & Audio",
    "icon": "assets/product-logos/google-veo.svg",
    "desc": "Frontier generative video model creating 4K cinematic scenes with camera motion controls, physics consistency, and synchronized sound design.",
    "url": "tools/google-veo.html",
    "starting_price_pkr": 1900,
    "starting_price_usd": 6.8,
    "plans": [
      {
        "plan_id": "PLAN-VEO-1M",
        "name": "VideoFX Early Access (1 Month)",
        "plan_type": "Early Access",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer / Creator",
        "price_pkr": 1900,
        "price_usd": 6.8,
        "features": [
          "1080p high-definition cinematic video generations",
          "Understands technical camera directions (timelapse, aerial, pan)",
          "High physical consistency across continuous shots",
          "Direct integration with Google Labs VideoFX suite"
        ],
        "limits": "Google Labs whitelisted access",
        "badge": "Next-Gen Video",
        "availability": "InStock"
      }
    ]
  },
  "chatgpt-codex": {
    "slug": "chatgpt-codex",
    "name": "OpenAI Codex",
    "brand": "OpenAI",
    "vendor": "OpenAI Developer Platform",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/chatgpt-codex.svg",
    "desc": "Autonomous agentic coding workspace and Agents API environment supporting parallel coding agents, CLI tools, and multi-file refactoring.",
    "url": "tools/chatgpt-codex.html",
    "starting_price_pkr": 600,
    "starting_price_usd": 2.5,
    "plans": [
      {
        "plan_id": "PLAN-CODEX-DEV-1M",
        "name": "Developer Tier (1 Month)",
        "plan_type": "Developer API",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer Organization",
        "price_pkr": 600,
        "price_usd": 2.5,
        "features": [
          "Pre-funded OpenAI developer API balance",
          "Access to GPT-5/4o, GPT-4o-mini, and embeddings",
          "Rate limits up to 500 requests per minute",
          "Full developer dashboard access & usage monitoring"
        ],
        "limits": "API token consumption rates apply",
        "badge": "Dev API",
        "availability": "InStock"
      }
    ]
  },
  "claude-artifacts": {
    "slug": "claude-artifacts",
    "name": "Claude Artifacts",
    "brand": "Anthropic",
    "vendor": "Anthropic AI Systems",
    "cat": "AI Coding & Dev",
    "icon": "assets/product-logos/claude-artifacts.svg",
    "desc": "Dedicated interactive code canvas and UI execution environment built directly into Claude.ai for frontend development and SVG rendering.",
    "url": "tools/claude-artifacts.html",
    "starting_price_pkr": 1200,
    "starting_price_usd": 4.5,
    "plans": [
      {
        "plan_id": "PLAN-ARTIFACTS-1M",
        "name": "Artifacts Suite (1 Month)",
        "plan_type": "Interactive Suite",
        "duration": "1 Month (30 Days)",
        "seats": "1 User",
        "price_pkr": 1200,
        "price_usd": 4.5,
        "features": [
          "Interactive split-screen code and UI renderer",
          "Instant React components, HTML5 games, and SVG graphics",
          "Download and fork generated Artifact code snippets",
          "Claude Sonnet 5.5 reasoning backing every generation"
        ],
        "limits": "Anthropic platform limits apply",
        "badge": "Live Prototyping",
        "availability": "InStock"
      }
    ]
  },
  "heygen-ai": {
    "slug": "heygen-ai",
    "name": "HeyGen Creator",
    "brand": "HeyGen",
    "vendor": "HeyGen Inc.",
    "cat": "Video & Motion AI",
    "icon": "assets/product-logos/heygen-ai.svg",
    "desc": "Hyper-realistic AI video avatars, studio voice cloning, lip-sync translation across 40+ languages, and automated video templates.",
    "url": "tools/heygen-ai.html",
    "starting_price_pkr": 4200,
    "starting_price_usd": 15.0,
    "plans": [
      {
        "plan_id": "PLAN-HEYGEN-CREATOR-1M",
        "name": "Creator Plan (1 Month)",
        "plan_type": "Creator",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Profile",
        "price_pkr": 4200,
        "price_usd": 15.0,
        "features": [
          "Fast video generation with 15 monthly credits",
          "Over 100+ realistic public AI avatars",
          "Auto voice clone & multi-language translation",
          "1080p full HD export with commercial license"
        ],
        "limits": "Standard video generation queue; fair use credit limits",
        "badge": "High Demand",
        "availability": "InStock"
      }
    ]
  },
  "gamma-app": {
    "slug": "gamma-app",
    "name": "Gamma Pro",
    "brand": "Gamma",
    "vendor": "Gamma Tech, Inc.",
    "cat": "Coding & Productivity",
    "icon": "assets/product-logos/gamma-app.svg",
    "desc": "Generative AI presentation builder creating polished slide decks, visual documents, and web pages from simple natural language prompts.",
    "url": "tools/gamma-app.html",
    "starting_price_pkr": 1600,
    "starting_price_usd": 5.9,
    "plans": [
      {
        "plan_id": "PLAN-GAMMA-PRO-1M",
        "name": "Pro Plan (1 Month)",
        "plan_type": "Pro",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 1600,
        "price_usd": 5.9,
        "features": [
          "Unlimited AI deck, document, and webpage generation",
          "Advanced AI model access (Claude & GPT-5/4o powered)",
          "Custom branding, font uploads & custom domains",
          "Export to PDF and PPTX without watermark"
        ],
        "limits": "Subject to Gamma fair use generation limits",
        "badge": "Popular",
        "availability": "InStock"
      }
    ]
  },
  "n8n-automation": {
    "slug": "n8n-automation",
    "name": "n8n Cloud Starter",
    "brand": "n8n",
    "vendor": "n8n GmbH",
    "cat": "Coding & Automation",
    "icon": "assets/product-logos/n8n-automation.svg",
    "desc": "Fair-code workflow automation platform with multi-agent orchestration, 400+ API integrations, and visual workflow building.",
    "url": "tools/n8n-automation.html",
    "starting_price_pkr": 6500,
    "starting_price_usd": 23.5,
    "plans": [
      {
        "plan_id": "PLAN-N8N-START-1Y",
        "name": "Starter Plan (1 Year)",
        "plan_type": "Starter Annual",
        "duration": "12 Months (365 Days)",
        "seats": "1 Workspace",
        "price_pkr": 6500,
        "price_usd": 23.5,
        "features": [
          "Up to 2,500 workflow executions per month",
          "Over 400+ native app and AI node integrations",
          "Built-in LangChain and custom webhook triggers",
          "Full 30-day replacement warranty"
        ],
        "limits": "Cloud starter instance quota; single environment",
        "badge": "Enterprise Automation",
        "availability": "InStock"
      }
    ]
  },
  "vidiq-boost": {
    "slug": "vidiq-boost",
    "name": "vidIQ Boost",
    "brand": "vidIQ",
    "vendor": "vidIQ Inc.",
    "cat": "Video & Motion AI",
    "icon": "assets/product-logos/vidiq-boost.svg",
    "desc": "YouTube channel growth toolkit providing AI title and description recommendations, competitor tracking, and search volume insights.",
    "url": "tools/vidiq-boost.html",
    "starting_price_pkr": 2100,
    "starting_price_usd": 7.5,
    "plans": [
      {
        "plan_id": "PLAN-VIDIQ-BOOST-1M",
        "name": "Boost Plan (1 Month)",
        "plan_type": "Boost",
        "duration": "1 Month (30 Days)",
        "seats": "1 Channel Profile",
        "price_pkr": 2100,
        "price_usd": 7.5,
        "features": [
          "50 AI Video Title, Description & Tag recommendations daily",
          "Live competitor tracking & keyword search volume metrics",
          "Historical trending video alerts & view velocity tracking",
          "SEO scorecard and thumbnail preview inspector"
        ],
        "limits": "Linked to 1 active YouTube channel",
        "badge": "Creator Favorite",
        "availability": "InStock"
      }
    ]
  },
  "coursera-plus": {
    "slug": "coursera-plus",
    "name": "Coursera Plus",
    "brand": "Coursera",
    "vendor": "Coursera Inc.",
    "cat": "Coding & Skills",
    "icon": "assets/product-logos/coursera-plus.svg",
    "desc": "Unlimited access to 7,000+ professional certificates, university specializations, and career credentials from Google, IBM, and top institutions.",
    "url": "tools/coursera-plus.html",
    "starting_price_pkr": 2200,
    "starting_price_usd": 8.0,
    "plans": [
      {
        "plan_id": "PLAN-COURSERA-PLUS-1Y",
        "name": "Coursera Plus (12 Months)",
        "plan_type": "Annual Subscription",
        "duration": "12 Months (365 Days)",
        "seats": "1 Student Profile",
        "price_pkr": 2200,
        "price_usd": 8.0,
        "features": [
          "Unlimited access to 7,000+ courses and Specializations",
          "Professional Certificates from Google, IBM, Meta & AWS",
          "Shareable certificates for LinkedIn and resume profiles",
          "Hands-on guided projects with cloud dev environments"
        ],
        "limits": "Excludes select degree programs and premium masterclasses",
        "badge": "Best Value",
        "availability": "InStock"
      }
    ]
  },
  "google-ai-ultra": {
    "slug": "google-ai-ultra",
    "name": "Google AI Ultra",
    "brand": "Google",
    "vendor": "Google LLC",
    "cat": "Coding & AI Assistants",
    "icon": "assets/product-logos/google-ai-ultra.svg",
    "desc": "Google's maximum-throughput tier featuring 20x compute caps, Deep Think autonomous reasoning, Antigravity orchestrator, and 30 TB storage.",
    "url": "tools/google-ai-ultra.html",
    "starting_price_pkr": 4500,
    "starting_price_usd": 16.5,
    "plans": [
      {
        "plan_id": "PLAN-GOOG-ULTRA-1M",
        "name": "Google AI Ultra 20X (1 Month)",
        "plan_type": "Ultra 20X",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 4500,
        "price_usd": 16.5,
        "features": [
          "Gemini 1.5 Pro with 2-Million token context window",
          "High-priority generation compute with 20X quota scaling",
          "Deep coding, repo upload, and multimodal audio/video analysis",
          "2TB Google Drive cloud storage bundle included"
        ],
        "limits": "Fair usage policy applies to extreme burst inference",
        "badge": "Pro Powerhouse",
        "availability": "InStock"
      }
    ]
  },
  "lovable-ai": {
    "slug": "lovable-ai",
    "name": "Lovable Pro",
    "brand": "Lovable",
    "vendor": "Lovable Inc.",
    "cat": "Coding & Developer Tools",
    "icon": "assets/product-logos/lovable-ai.svg",
    "desc": "Autonomous full-stack web application builder turning plain English descriptions into production-ready React, Tailwind, and Supabase code.",
    "url": "tools/lovable-ai.html",
    "starting_price_pkr": 1500,
    "starting_price_usd": 5.5,
    "plans": [
      {
        "plan_id": "PLAN-LOVABLE-PRO-1M",
        "name": "Pro Plan (1 Month)",
        "plan_type": "Pro",
        "duration": "1 Month (30 Days)",
        "seats": "1 Developer Account",
        "price_pkr": 1500,
        "price_usd": 5.5,
        "features": [
          "Natural language to production web applications",
          "Direct GitHub synchronization and code export",
          "Integrated Supabase backend and authentication setup",
          "High-speed generation tokens for rapid prototyping"
        ],
        "limits": "Subject to Lovable monthly token allocation",
        "badge": "Trending AI Dev",
        "availability": "InStock"
      }
    ]
  },
  "spotify-premium": {
    "slug": "spotify-premium",
    "name": "Spotify Premium",
    "brand": "Spotify",
    "vendor": "Spotify AB",
    "cat": "Streaming & Entertainment",
    "icon": "assets/product-logos/spotify.svg",
    "desc": "Ad-free high-fidelity audio streaming, offline song downloads, unlimited song skips, and personalized AI DJ curation.",
    "url": "tools/spotify-premium.html",
    "starting_price_pkr": 850,
    "starting_price_usd": 3.2,
    "plans": [
      {
        "plan_id": "PLAN-SPOTIFY-IND-3M",
        "name": "Individual (3 Months)",
        "plan_type": "Individual Multi-Month",
        "duration": "3 Months (90 Days)",
        "seats": "1 User Profile",
        "price_pkr": 850,
        "price_usd": 3.2,
        "features": [
          "100% Ad-free uninterrupted music playback",
          "Offline download support on mobile and desktop",
          "Very high audio quality (320kbps Ogg/AAC)",
          "Cross-device Spotify Connect synchronization"
        ],
        "limits": "Personal account activation; non-commercial playback",
        "badge": "Everyday Audio",
        "availability": "InStock"
      }
    ]
  },
  "microsoft-office-365": {
    "slug": "microsoft-office-365",
    "name": "Microsoft 365 Personal",
    "brand": "Microsoft",
    "vendor": "Microsoft Corporation",
    "cat": "Coding & Productivity",
    "icon": "assets/product-logos/microsoft-365.svg",
    "desc": "Premium desktop applications including Word, Excel, PowerPoint, Outlook, and OneNote with 1 TB secure OneDrive cloud storage.",
    "url": "tools/microsoft-office-365.html",
    "starting_price_pkr": 1950,
    "starting_price_usd": 7.0,
    "plans": [
      {
        "plan_id": "PLAN-M365-FAM-1Y",
        "name": "Family Member (1 Year)",
        "plan_type": "Annual License",
        "duration": "12 Months (365 Days)",
        "seats": "1 User (Up to 5 Devices)",
        "price_pkr": 1950,
        "price_usd": 7.0,
        "features": [
          "Full desktop Word, Excel, PowerPoint, Outlook & Access",
          "1,000 GB (1 TB) secure OneDrive cloud storage",
          "Install simultaneously on 5 PCs, Macs, tablets & phones",
          "Full 30-day replacement warranty"
        ],
        "limits": "Standard personal OneDrive quota per member seat",
        "badge": "Essential Office",
        "availability": "InStock"
      }
    ]
  },
  "windows-11-pro": {
    "slug": "windows-11-pro",
    "name": "Windows 11 Pro",
    "brand": "Microsoft",
    "vendor": "Microsoft Corporation",
    "cat": "Coding & Productivity",
    "icon": "assets/product-logos/windows-11-pro.svg",
    "desc": "Professional PC operating system with BitLocker drive encryption, Hyper-V virtualization, Windows Sandbox, and remote desktop capabilities.",
    "url": "tools/windows-11-pro.html",
    "starting_price_pkr": 1850,
    "starting_price_usd": 6.8,
    "plans": [
      {
        "plan_id": "PLAN-WIN11-PRO-RET",
        "name": "Retail License Key (Lifetime)",
        "plan_type": "Perpetual License",
        "duration": "Lifetime Activation (1 PC)",
        "seats": "1 PC Device",
        "price_pkr": 1850,
        "price_usd": 6.8,
        "features": [
          "Genuine 25-digit alphanumeric digital retail activation key",
          "BitLocker device encryption & Windows Sandbox included",
          "Hyper-V virtualization & Remote Desktop server access",
          "Worldwide multi-language support & official Microsoft updates"
        ],
        "limits": "Single machine activation; binds to hardware motherboard ID",
        "badge": "Official License",
        "availability": "InStock"
      }
    ]
  },
  "prime-video": {
    "slug": "prime-video",
    "name": "Amazon Prime Video",
    "brand": "Amazon",
    "vendor": "Amazon.com Inc.",
    "cat": "Streaming & Entertainment",
    "icon": "assets/product-logos/prime-video.svg",
    "desc": "Unlimited streaming of Amazon Originals, blockbuster movies, and award-winning series in 4K UHD with X-Ray behind-the-scenes data.",
    "url": "tools/prime-video.html",
    "starting_price_pkr": 650,
    "starting_price_usd": 2.4,
    "plans": [
      {
        "plan_id": "PLAN-PRIME-SCREEN-1M",
        "name": "Private Screen (1 Month)",
        "plan_type": "Private Screen",
        "duration": "1 Month (30 Days)",
        "seats": "1 Private Profile Screen",
        "price_pkr": 650,
        "price_usd": 2.4,
        "features": [
          "Full 4K Ultra HD and HDR video streaming",
          "Access to exclusive Amazon Originals and global cinema",
          "Private PIN-protected profile with personal watch history",
          "Full 30-day replacement warranty"
        ],
        "limits": "Single concurrent stream per allocated screen profile",
        "badge": "Budget Stream",
        "availability": "InStock"
      }
    ]
  },
  "tradingview-pro": {
    "slug": "tradingview-pro",
    "name": "TradingView Essential",
    "brand": "TradingView",
    "vendor": "TradingView Inc.",
    "cat": "Coding & Productivity",
    "icon": "assets/product-logos/tradingview.svg",
    "desc": "Advanced financial charting platform featuring 5 indicators per chart, custom Pine Script v6 alerts, bar replay, and multi-asset screeners.",
    "url": "tools/tradingview-pro.html",
    "starting_price_pkr": 3200,
    "starting_price_usd": 11.5,
    "plans": [
      {
        "plan_id": "PLAN-TRADINGVIEW-PREM-1M",
        "name": "Premium Tier (1 Month)",
        "plan_type": "Premium",
        "duration": "1 Month (30 Days)",
        "seats": "1 User Account",
        "price_pkr": 3200,
        "price_usd": 11.5,
        "features": [
          "Up to 8 synchronized charts per single layout",
          "25 technical indicators per chart simultaneously",
          "Second-based intervals & tick-level bar replay",
          "400 server-side active price alerts"
        ],
        "limits": "Personal financial charting; single active session",
        "badge": "Trader Choice",
        "availability": "InStock"
      }
    ]
  },
  "turnitin-student": {
    "slug": "turnitin-student",
    "name": "Turnitin Originality",
    "brand": "Turnitin",
    "vendor": "Turnitin, LLC",
    "cat": "Coding & Productivity",
    "icon": "assets/product-logos/turnitin-student.svg",
    "desc": "Institutional-grade plagiarism detection and AI writing analysis comparing submissions against billions of scholarly articles and web pages.",
    "url": "tools/turnitin-student.html",
    "starting_price_pkr": 2800,
    "starting_price_usd": 10.0,
    "plans": [
      {
        "plan_id": "PLAN-TURNITIN-STU-1M",
        "name": "Student Account (1 Month)",
        "plan_type": "Student Account",
        "duration": "1 Month (30 Days)",
        "seats": "1 Student Portal",
        "price_pkr": 2800,
        "price_usd": 10.0,
        "features": [
          "Direct similarity index generation with non-repository option",
          "AI writing and paraphrasing detection breakdown",
          "Full PDF originality report downloads with matched sources",
          "Safe submission settings that do not store student papers in repository"
        ],
        "limits": "Non-repository class enrollment; up to 30 submissions/month",
        "badge": "Academic Guard",
        "availability": "InStock"
      }
    ]
  }
};

  // State variables for Quick Order Drawer
  var HELD_PRODUCTS = ["turnitin-student", "linkedin-premium", "netflix-premium", "spotify-premium", "coursera-plus", "claude-artifacts", "deepseek-pro"];
  var currentTool = TOOLS_DATA["chatgpt-plus"];
  var currentPlan = currentTool && currentTool.plans && currentTool.plans.length > 0 ? currentTool.plans[0] : null;
  var currentPaymentRail = "SadaPay";

  // Check prefix for assets (subfolder vs root)
  function getPathPrefix() {
    var p = window.location.pathname;
    if (p.indexOf('/tools/') !== -1 || p.indexOf('/categories/') !== -1 || p.indexOf('/guides/') !== -1 || p.indexOf('/compare/') !== -1 || p.indexOf('/best/') !== -1) {
      return '../';
    }
    return '';
  }

  // --- Living Centerpiece Showcase Engine ---
  window.setMasterTool = function (slug) {
    var tool = TOOLS_DATA[slug];
    if (!tool) return;

    var prefix = getPathPrefix();

    var iconEl = document.getElementById('mToolIcon');
    var vendorEl = document.getElementById('mToolVendor');
    var titleEl = document.getElementById('mToolTitle');
    var descEl = document.getElementById('mToolDesc');
    var priceEl = document.getElementById('mToolPrice');
    var priceSubEl = document.getElementById('mToolPriceSub');
    var waLinkEl = document.getElementById('mWaLink');
    var specsLinkEl = document.getElementById('mSpecsLink');
    var selectEl = document.getElementById('showcaseToolSelect');

    var primaryPlan = tool.plans && tool.plans.length > 0 ? tool.plans[0] : null;
    var pricePkr = primaryPlan ? primaryPlan.price_pkr : tool.starting_price_pkr;
    var priceUsd = primaryPlan ? primaryPlan.price_usd : tool.starting_price_usd;

    if (iconEl) {
      iconEl.src = prefix + tool.icon;
      iconEl.alt = tool.name + " Official Logo";
    }
    if (vendorEl) vendorEl.textContent = tool.vendor;
    if (titleEl) titleEl.textContent = tool.name + " Subscription";
    if (descEl) descEl.textContent = tool.desc;
    if (priceEl) priceEl.textContent = "Rs. " + pricePkr.toLocaleString();
    if (priceSubEl) priceSubEl.textContent = "PKR (~$" + priceUsd.toFixed(2) + " USD) / month";

    if (specsLinkEl) {
      specsLinkEl.href = prefix + tool.url;
      specsLinkEl.textContent = "View All " + (tool.plans ? tool.plans.length : 1) + " Verified Plans for " + tool.name + " →";
    }

    var isHeld = HELD_PRODUCTS.indexOf(slug) !== -1;
    var waMsg;
    if (isHeld) {
      waMsg = "Hi AIDigiTools, I am inquiring about current availability and compliance terms for " + tool.name + ". (Inquiry only; not an order confirmation).";
    } else {
      waMsg = "Hi AIDigiTools, I want to order " + tool.name + " for Rs " + pricePkr + " PKR / $" + priceUsd + " USD via " + currentPaymentRail + ". Please confirm availability and share payment details.";
    }
    if (waLinkEl) {
      waLinkEl.style.setProperty('background', '#10B981', 'important');
      waLinkEl.style.setProperty('color', '#FFFFFF', 'important');
      waLinkEl.style.setProperty('border', 'none', 'important');
      waLinkEl.innerHTML = '<span style="color:#FFFFFF !important; font-weight:700;">💬 WhatsApp Contact &rarr;</span>';
    }
    if (waLinkEl) {
      waLinkEl.href = "https://wa.me/923326861112?text=" + encodeURIComponent(waMsg);
    }

    if (selectEl && selectEl.value !== slug) {
      selectEl.value = slug;
    }

    // Update active tab buttons if present
    var tabBtns = document.querySelectorAll('.authkit-tab-btn');
    tabBtns.forEach(function (btn) {
      var id = btn.id || '';
      if (id === 'mtab-' + slug) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
  };

  // Category filter for Living Showcase dropdown & tabs (Harmonized with Directory)
  window.filterShowcaseCategory = function (catName, btnEl) {
    var selectEl = document.getElementById('showcaseToolSelect');
    if (!selectEl) return;

    var pills = document.querySelectorAll('.authkit-cat-pill');
    pills.forEach(function (p) {
      p.classList.remove('active');
      p.setAttribute('aria-selected', 'false');
    });
    if (btnEl) {
      btnEl.classList.add('active');
      btnEl.setAttribute('aria-selected', 'true');
    }

    var optgroups = selectEl.querySelectorAll('optgroup');
    var firstMatchingSlug = null;

    optgroups.forEach(function (grp) {
      var grpCat = grp.getAttribute('data-cat') || '';
      if (catName === 'all' || grpCat === catName) {
        grp.style.display = '';
        if (!firstMatchingSlug && grp.querySelector('option')) {
          firstMatchingSlug = grp.querySelector('option').value;
        }
      } else {
        grp.style.display = 'none';
      }
    });

    if (firstMatchingSlug) {
      window.setMasterTool(firstMatchingSlug);
    }
  };

  // --- Canonical Plan Selector in Quick Order Drawer ---
  window.selectPlanInDrawer = function (planId) {
    if (!currentTool || !currentTool.plans) return;
    var found = currentTool.plans.find(function (p) { return p.plan_id === planId; });
    if (found) {
      currentPlan = found;
      renderDrawerPlans();
      updateCartSummary();
    }
  };

  function renderDrawerPlans() {
    var container = document.getElementById('drawerPlanSelectorContainer');
    if (!container) return;

    if (!currentTool.plans || currentTool.plans.length <= 1) {
      container.style.display = 'none';
      return;
    }

    container.style.display = 'block';
    var html = '<label style="display:block; font-size:0.82rem; font-weight:700; color:var(--text-secondary); margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:0.04em;">Select Verified Plan</label>';
    html += '<div style="display:flex; flex-direction:column; gap:0.5rem;">';

    currentTool.plans.forEach(function (plan) {
      var isSelected = currentPlan && currentPlan.plan_id === plan.plan_id;
      var activeStyle = isSelected
        ? 'border:1.5px solid #0284C7; background:#F0F9FF; box-shadow:0 2px 8px rgba(2,132,199,0.15);'
        : 'border:1px solid var(--border-color); background:var(--bg-card);';

      html += '<div onclick="selectPlanInDrawer(\'' + plan.plan_id + '\')" style="padding:0.65rem 0.85rem; border-radius:10px; cursor:pointer; transition:all 0.15s ease; display:flex; justify-content:space-between; align-items:center; ' + activeStyle + '">';
      html += '<div>';
      html += '<div style="font-size:0.9rem; font-weight:700; color:var(--text-primary);">' + plan.name + '</div>';
      html += '<div style="font-size:0.75rem; color:var(--text-muted);">' + plan.duration + ' • ' + plan.seats + '</div>';
      html += '</div>';
      html += '<div style="text-align:right;">';
      html += '<div style="font-size:0.92rem; font-weight:800; color:#0284C7;">Rs. ' + plan.price_pkr.toLocaleString() + '</div>';
      html += '<div style="font-size:0.72rem; color:var(--text-secondary);">(~$' + plan.price_usd.toFixed(2) + ' USD)</div>';
      html += '</div>';
      html += '</div>';
    });

    html += '</div>';
    container.innerHTML = html;
  }

  // --- Quick Order / Cart Drawer Engine ---
  window.openQuickOrderModal = function (slug, planId) {
    var tool = TOOLS_DATA[slug] || currentTool;
    currentTool = tool;

    // Pick requested plan or default to first plan
    if (planId && tool.plans) {
      var target = tool.plans.find(function (p) { return p.plan_id === planId; });
      currentPlan = target || tool.plans[0];
    } else if (tool.plans && tool.plans.length > 0) {
      currentPlan = tool.plans[0];
    } else {
      currentPlan = null;
    }

    var prefix = getPathPrefix();

    var nameEl = document.getElementById('drawerItemName');
    var vendorEl = document.getElementById('drawerItemVendor');
    var iconEl = document.getElementById('drawerItemIcon');

    if (nameEl) nameEl.textContent = tool.name;
    if (vendorEl) vendorEl.textContent = tool.vendor + " • " + tool.cat;
    if (iconEl) {
      iconEl.src = prefix + tool.icon;
      iconEl.alt = tool.name + " Icon";
    }

    var isHeld = HELD_PRODUCTS.indexOf(tool.slug || slug) !== -1;
    var holdNotice = document.getElementById('drawerHoldNotice');
    if (isHeld) {
      if (!holdNotice) {
        holdNotice = document.createElement('div');
        holdNotice.id = 'drawerHoldNotice';
        holdNotice.style.cssText = 'background:rgba(245,158,11,0.12); border:1px solid #f59e0b; border-radius:8px; padding:0.6rem 0.8rem; margin-bottom:0.75rem; font-size:0.82rem; color:var(--text-secondary);';
        holdNotice.innerHTML = '<strong>⏸️ Direct Orders Paused:</strong> Direct checkout for this service is on hold pending secondary licensing verification. Inquiries are for stock &amp; compliance verification only and an inquiry is not an order confirmation.';
        var planWrap = document.getElementById('drawerPlanSelectorContainer');
        if (planWrap && planWrap.parentNode) {
          planWrap.parentNode.insertBefore(holdNotice, planWrap);
        }
      } else {
        holdNotice.style.display = 'block';
      }
    } else if (holdNotice) {
      holdNotice.style.display = 'none';
    }

    renderDrawerPlans();
    window.selectCartRail('SadaPay');

    var drawer = document.getElementById('cartDrawer');
    var backdrop = document.getElementById('cartBackdrop');
    if (drawer && backdrop) {
      drawer.classList.add('active');
      backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  };

  window.closeQuickOrderModal = function () {
    var drawer = document.getElementById('cartDrawer');
    var backdrop = document.getElementById('cartBackdrop');
    if (drawer && backdrop) {
      drawer.classList.remove('active');
      backdrop.classList.remove('active');
      document.body.style.overflow = '';
    }
  };

  window.selectCartRail = function (railName) {
    currentPaymentRail = railName;
    var railOptions = document.querySelectorAll('.rail-option');
    railOptions.forEach(function (opt) {
      if (opt.getAttribute('data-rail') === railName) {
        opt.classList.add('active');
      } else {
        opt.classList.remove('active');
      }
    });

    updateCartSummary();
  };

  function updateCartSummary() {
    if (!currentTool) return;

    var pricePkr = currentPlan ? currentPlan.price_pkr : currentTool.starting_price_pkr;
    var priceUsd = currentPlan ? currentPlan.price_usd : currentTool.starting_price_usd;
    var planTitle = currentPlan ? currentPlan.name : (currentTool.name + " Standard Plan");
    var duration = currentPlan ? currentPlan.duration : "1 Month";

    var subtotalEl = document.getElementById('drawerSubtotal');
    var totalPkrEl = document.getElementById('drawerTotalPkr');
    var totalUsdEl = document.getElementById('drawerTotalUsd');
    var checkoutBtn = document.getElementById('drawerCheckoutBtn');

    if (subtotalEl) subtotalEl.textContent = "Rs. " + pricePkr.toLocaleString() + " PKR";
    if (totalPkrEl) totalPkrEl.textContent = "Rs. " + pricePkr.toLocaleString() + " PKR";
    if (totalUsdEl) totalUsdEl.textContent = "(~$" + priceUsd.toFixed(2) + " USD)";

    var isHeld = HELD_PRODUCTS.indexOf(currentTool.slug || '') !== -1;
    var waMsg;
    if (isHeld) {
      waMsg = "Hi AIDigiTools! I am inquiring about current availability and compliance terms for " + currentTool.name + " (" + planTitle + " - " + duration + "). (Inquiry only; not an order confirmation).";
      if (checkoutBtn) {
        checkoutBtn.textContent = "💬 Inquire on WhatsApp for Current Availability";
      }
    } else {
      waMsg = "Hi AIDigiTools! I want to order " + currentTool.name + " (" + planTitle + " - " + duration + ") for Rs. " + pricePkr.toLocaleString() + " PKR (~$" + priceUsd.toFixed(2) + " USD). I prefer paying via " + currentPaymentRail + ". Please confirm availability and share payment details.";
      if (checkoutBtn) {
        checkoutBtn.textContent = "⚡ Continue to WhatsApp to Order";
      }
    }

    if (checkoutBtn) {
      checkoutBtn.href = "https://wa.me/923326861112?text=" + encodeURIComponent(waMsg);
    }
  }

  // Close modal when pressing ESC or clicking backdrop
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      window.closeQuickOrderModal();
    }
  });

  // Filter tool cards in search box with empty-state handling
  // --- PHASE 13: ADVANCED SEARCH, FILTER, SORT & PRODUCT COMPARISON ENGINE ---

  window.currentSearchQuery = '';
  window.currentCategory = '';
  window.currentPriceRange = 'all';
  window.currentSort = 'featured';
  window.compareList = [];
  var initialCardOrder = [];

  // Initialize card order cache once DOM is loaded
  function cacheInitialCardOrder() {
    var cards = document.querySelectorAll('.tool-card');
    if (cards.length > 0 && initialCardOrder.length === 0) {
      initialCardOrder = Array.from(cards);
    }
  }

  // Master Filter & Sort Application Function
  window.applyFilters = function () {
    cacheInitialCardOrder();
    var queryInput = document.getElementById('toolSearchInput');
    var priceSelect = document.getElementById('priceFilter');
    var sortSelect = document.getElementById('sortSelect');
    var clearBtn = document.getElementById('clearSearchBtn');
    var resetBtn = document.getElementById('resetFiltersBtn');

    var q = (queryInput ? queryInput.value : window.currentSearchQuery || '').toLowerCase().trim();
    window.currentSearchQuery = q;

    if (clearBtn) {
      clearBtn.style.display = q ? 'flex' : 'none';
    }

    var priceRange = priceSelect ? priceSelect.value : window.currentPriceRange || 'all';
    window.currentPriceRange = priceRange;

    var sortOrder = sortSelect ? sortSelect.value : window.currentSort || 'featured';
    window.currentSort = sortOrder;

    var cat = (window.currentCategory || '').toLowerCase().trim();

    // Check if any filter is active
    var isFiltered = (q !== '') || (cat !== '') || (priceRange !== 'all') || (sortOrder !== 'featured');
    if (resetBtn) {
      resetBtn.style.display = isFiltered ? 'inline-block' : 'none';
    }

    var cards = document.querySelectorAll('.tool-card');
    var grid = document.querySelector('.tools-grid') || document.querySelector('.grid');
    var visibleCards = [];
    var visibleCount = 0;

    cards.forEach(function (card) {
      var name = (card.getAttribute('data-name') || '').toLowerCase();
      var cardCat = (card.getAttribute('data-category') || '').toLowerCase();
      var terms = (card.getAttribute('data-terms') || '').toLowerCase();
      var vendor = (card.getAttribute('data-vendor') || '').toLowerCase();
      var fullText = card.textContent.toLowerCase();
      var pricePkr = parseInt(card.getAttribute('data-price-pkr') || '0', 10);

      // 1. Text Query Match
      var matchesQuery = true;
      if (q) {
        matchesQuery = (name.indexOf(q) !== -1) ||
                       (terms.indexOf(q) !== -1) ||
                       (cardCat.indexOf(q) !== -1) ||
                       (vendor.indexOf(q) !== -1) ||
                       (fullText.indexOf(q) !== -1);
      }

      // 2. Category Match
      var matchesCat = true;
      if (cat) {
        matchesCat = (cardCat.indexOf(cat) !== -1) || (terms.indexOf(cat) !== -1);
      }

      // 3. Price Filter Match
      var matchesPrice = true;
      if (priceRange === 'under-1000') {
        matchesPrice = (pricePkr > 0 && pricePkr < 1000);
      } else if (priceRange === '1000-2500') {
        matchesPrice = (pricePkr >= 1000 && pricePkr <= 2500);
      } else if (priceRange === 'above-2500') {
        matchesPrice = (pricePkr > 2500);
      }

      if (matchesQuery && matchesCat && matchesPrice) {
        card.style.display = '';
        visibleCount++;
        visibleCards.push(card);
      } else {
        card.style.display = 'none';
      }
    });

    // 4. Sorting Logic
    if (grid && visibleCards.length > 1) {
      var sortedCards = visibleCards.slice();
      if (sortOrder === 'price-asc') {
        sortedCards.sort(function (a, b) {
          return parseInt(a.getAttribute('data-price-pkr') || '0', 10) - parseInt(b.getAttribute('data-price-pkr') || '0', 10);
        });
      } else if (sortOrder === 'price-desc') {
        sortedCards.sort(function (a, b) {
          return parseInt(b.getAttribute('data-price-pkr') || '0', 10) - parseInt(a.getAttribute('data-price-pkr') || '0', 10);
        });
      } else if (sortOrder === 'name-asc') {
        sortedCards.sort(function (a, b) {
          var nameA = (a.getAttribute('data-name') || '').toLowerCase();
          var nameB = (b.getAttribute('data-name') || '').toLowerCase();
          return nameA.localeCompare(nameB);
        });
      } else if (sortOrder === 'name-desc') {
        sortedCards.sort(function (a, b) {
          var nameA = (a.getAttribute('data-name') || '').toLowerCase();
          var nameB = (b.getAttribute('data-name') || '').toLowerCase();
          return nameB.localeCompare(nameA);
        });
      } else if (sortOrder === 'featured' && initialCardOrder.length > 0) {
        sortedCards.sort(function (a, b) {
          return initialCardOrder.indexOf(a) - initialCardOrder.indexOf(b);
        });
      }

      // Reorder in DOM
      sortedCards.forEach(function (c) {
        grid.appendChild(c);
      });
    }

    // 5. Update Counter Badge
    var countEl = document.getElementById('searchCountBadge');
    if (countEl) {
      countEl.textContent = 'Showing ' + visibleCount + ' of ' + cards.length + ' Tools';
    }

    // 6. Empty State Handling
    var emptyEl = document.getElementById('searchEmptyState');
    if (visibleCount === 0 && cards.length > 0) {
      if (!emptyEl && grid) {
        emptyEl = document.createElement('div');
        emptyEl.id = 'searchEmptyState';
        emptyEl.className = 'empty-state';
        emptyEl.innerHTML = '<span class="empty-state-icon" aria-hidden="true">🔍</span>' +
          '<h3 class="empty-state-title">No Matching AI Tools Found</h3>' +
          '<p class="empty-state-desc">We could not find any software matching your selected filters (<strong id="emptyQueryText"></strong>). Try a broader keyword or browse all 36 tools below.</p>' +
          '<div class="empty-state-suggestions">' +
            '<span>Try Popular:</span> ' +
            '<button type="button" class="empty-state-chip" onclick="window.applyQuickSearch(\'coding\')">💻 Coding</button>' +
            '<button type="button" class="empty-state-chip" onclick="window.applyQuickSearch(\'video\')">🎬 Video</button>' +
            '<button type="button" class="empty-state-chip" onclick="window.applyQuickSearch(\'claude\')">🤖 Claude</button>' +
            '<button type="button" class="empty-state-chip" onclick="window.applyQuickSearch(\'midjourney\')">🎨 Midjourney</button>' +
            '<button type="button" class="empty-state-chip" onclick="window.applyQuickSearch(\'vpn\')">🛡️ VPN</button>' +
          '</div>' +
          '<button type="button" class="empty-state-action" onclick="window.resetAllFilters()">Clear All Filters & View All Tools</button>';
        grid.appendChild(emptyEl);
      }
      if (emptyEl) {
        var querySpan = emptyEl.querySelector('#emptyQueryText');
        var queryDesc = [];
        if (q) queryDesc.push('"' + q + '"');
        if (cat) queryDesc.push('Category: ' + cat);
        if (priceRange !== 'all') queryDesc.push('Price: ' + priceRange);
        if (querySpan) querySpan.textContent = queryDesc.join(' + ') || 'Custom Filter';
        emptyEl.style.display = 'block';
      }
    } else if (emptyEl) {
      emptyEl.style.display = 'none';
    }

    // 7. Prevent Crawler Indexing: Sync client-side URL safely via history.replaceState
    if (window.history && window.history.replaceState) {
      var params = new URLSearchParams();
      if (q) params.set('q', q);
      if (cat) params.set('category', cat);
      if (priceRange !== 'all') params.set('price', priceRange);
      if (sortOrder !== 'featured') params.set('sort', sortOrder);
      var newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
      window.history.replaceState({ q: q, cat: cat, price: priceRange, sort: sortOrder }, '', newUrl);
    }
  };

  // Backwards compatibility wrappers
  window.searchTools = function (query) {
    window.currentSearchQuery = query;
    window.applyFilters();
  };

  window.filterCategory = function (category) {
    window.currentCategory = category || '';
    var buttons = document.querySelectorAll('.cat-pill-btn');
    buttons.forEach(function (btn) {
      var btnCat = btn.getAttribute('data-cat') || '';
      var isActive = (btnCat === category);
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-pressed', isActive ? 'true' : 'false');
    });
    window.applyFilters();
  };

  window.filterTools = function (category) {
    window.filterCategory(category);
  };

  window.clearSearchInput = function () {
    var input = document.getElementById('toolSearchInput');
    if (input) input.value = '';
    window.currentSearchQuery = '';
    window.applyFilters();
  };

  window.resetAllFilters = function () {
    var queryInput = document.getElementById('toolSearchInput');
    if (queryInput) queryInput.value = '';
    window.currentSearchQuery = '';

    var priceSelect = document.getElementById('priceFilter');
    if (priceSelect) priceSelect.value = 'all';
    window.currentPriceRange = 'all';

    var sortSelect = document.getElementById('sortSelect');
    if (sortSelect) sortSelect.value = 'featured';
    window.currentSort = 'featured';

    window.filterCategory('');
  };

  window.applyQuickSearch = function (term) {
    var input = document.getElementById('toolSearchInput');
    if (input) input.value = term;
    window.currentSearchQuery = term;
    window.applyFilters();
  };

  // --- PRODUCT COMPARISON ENGINE ---

  window.toggleCompare = function (slug) {
    var idx = window.compareList.indexOf(slug);
    if (idx !== -1) {
      window.compareList.splice(idx, 1);
    } else {
      if (window.compareList.length >= 3) {
        alert('You can compare a maximum of 3 tools side-by-side.');
        return;
      }
      window.compareList.push(slug);
    }
    updateCompareUI();
  };

  function updateCompareUI() {
    var buttons = document.querySelectorAll('.btn-tool-compare');
    buttons.forEach(function (btn) {
      var slug = btn.getAttribute('data-slug');
      var isSelected = (window.compareList.indexOf(slug) !== -1);
      btn.classList.toggle('active', isSelected);
      btn.textContent = isSelected ? '✓ Added' : '⚖️ Compare';
      btn.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
      var tool = (typeof TOOLS_DATA !== 'undefined') ? TOOLS_DATA[slug] : null;
      var toolName = tool ? tool.name : slug;
      btn.setAttribute('aria-label', (isSelected ? 'Remove ' : 'Compare ') + toolName + (isSelected ? ' from comparison' : ' with other tools'));
    });

    var dock = document.getElementById('compareDock');
    var countEl = document.getElementById('compareDockCount');
    var itemsEl = document.getElementById('compareDockItems');
    var modalBtn = document.getElementById('openCompareModalBtn');

    if (dock) {
      if (window.compareList.length > 0) {
        dock.style.display = 'flex';
        if (countEl) countEl.textContent = 'Selected (' + window.compareList.length + '/3):';
        if (itemsEl) {
          itemsEl.innerHTML = window.compareList.map(function (s) {
            var tool = TOOLS_DATA[s];
            var name = tool ? tool.name : s;
            return '<span class="compare-chip">' + name + '</span>';
          }).join('');
        }
        if (modalBtn) {
          modalBtn.textContent = 'Compare (' + window.compareList.length + ')';
        }
      } else {
        dock.style.display = 'none';
      }
    }
  }

  window.clearComparison = function () {
    window.compareList = [];
    updateCompareUI();
  };

  window.openCompareModal = function () {
    if (window.compareList.length === 0) return;
    var modalBackdrop = document.getElementById('compareModalBackdrop');
    var modalBody = document.getElementById('compareModalBody');
    if (!modalBackdrop || !modalBody) return;

    var tools = window.compareList.map(function (s) {
      return TOOLS_DATA[s] || { slug: s, name: s, starting_price_pkr: 0, starting_price_usd: 0, cat: 'AI Software', vendor: 'Verified Vendor', icon: 'assets/product-logos/chatgpt-plus.svg' };
    });

    var prefix = getPathPrefix();

    var html = '<table class="compare-table" role="table">' +
      '<thead>' +
        '<tr>' +
          '<th>Feature / Specification</th>' +
          tools.map(function (t) {
            return '<th style="text-align:center;">' +
              '<img src="' + prefix + t.icon + '" alt="' + t.name + ' Icon" width="40" height="40" style="margin:0 auto 0.5rem; display:block;" loading="lazy" decoding="async">' +
              '<strong>' + t.name + '</strong>' +
              '<div style="font-size:0.75rem; color:#64748B; font-weight:normal;">' + t.vendor + '</div>' +
            '</th>';
          }).join('') +
        '</tr>' +
      '</thead>' +
      '<tbody>' +
        '<tr>' +
          '<th>Starting Price (PKR)</th>' +
          tools.map(function (t) {
            return '<td style="text-align:center; font-weight:700; color:#059669; font-size:1.05rem;">Rs. ' + t.starting_price_pkr.toLocaleString() + ' PKR</td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>USD Equivalent</th>' +
          tools.map(function (t) {
            return '<td style="text-align:center; color:#64748B;">~$' + t.starting_price_usd.toFixed(2) + ' USD / month</td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>Category</th>' +
          tools.map(function (t) {
            return '<td style="text-align:center;">' + t.cat + '</td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>Access Model</th>' +
          tools.map(function (t) {
            var isHeld = HELD_PRODUCTS.indexOf(t.slug) !== -1;
            var text = isHeld ? 'Direct Orders Paused' : 'Shared Team Workspace';
            var bg = isHeld ? 'rgba(245,158,11,0.15)' : '#F1F5F9';
            var color = isHeld ? '#d97706' : 'inherit';
            return '<td style="text-align:center;"><span style="background:' + bg + '; color:' + color + '; padding:0.2rem 0.6rem; border-radius:9999px; font-size:0.78rem; font-weight:600;">' + text + '</span></td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>Delivery Target</th>' +
          tools.map(function (t) {
            var isHeld = HELD_PRODUCTS.indexOf(t.slug) !== -1;
            return isHeld
              ? '<td style="text-align:center; color:#d97706; font-weight:600;">⏸️ Paused (Inquire)</td>'
              : '<td style="text-align:center; color:#0284C7; font-weight:600;">⚡ 15–30 Minutes</td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>Replacement Warranty</th>' +
          tools.map(function () {
            return '<td style="text-align:center; color:#059669; font-weight:600;">🛡️ 30-Day Replacement</td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>Supported Platforms</th>' +
          tools.map(function () {
            return '<td style="text-align:center; font-size:0.8rem;">Web, Windows, macOS, iOS, Android</td>';
          }).join('') +
        '</tr>' +
        '<tr>' +
          '<th>Action</th>' +
          tools.map(function (t) {
            var isHeld = HELD_PRODUCTS.indexOf(t.slug) !== -1;
            var actionBtn = isHeld
              ? '<a href="https://wa.me/923326861112?text=Hi%20AIDigiTools,%20I%20am%20inquiring%20about%20availability%20for%20' + encodeURIComponent(t.name) + '.%20(Inquiry%20only;%20not%20an%20order%20confirmation)." target="_blank" rel="noopener noreferrer" class="btn-quick-order" style="width:100%; margin-bottom:0.4rem; text-decoration:none; display:inline-flex; align-items:center; justify-content:center; font-size:0.8rem;">⚡ Quick Order</a>'
              : '<button type="button" class="btn-quick-order" style="width:100%; margin-bottom:0.4rem;" onclick="closeCompareModal(); openQuickOrderModal(\'' + t.slug + '\')">⚡ Quick Order</button>';
            return '<td style="text-align:center;">' +
              actionBtn +
              '<a href="' + prefix + t.url + '" style="font-size:0.75rem; color:#4361EE; text-decoration:none; display:block;">Full Specs &rarr;</a>' +
            '</td>';
          }).join('') +
        '</tr>' +
      '</tbody>' +
    '</table>';

    modalBody.innerHTML = html;
    modalBackdrop.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  };

  window.closeCompareModal = function () {
    var modalBackdrop = document.getElementById('compareModalBackdrop');
    if (modalBackdrop) {
      modalBackdrop.style.display = 'none';
      document.body.style.overflow = '';
    }
  };

  // Close modals when pressing ESC or clicking backdrop
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      window.closeQuickOrderModal();
      window.closeCompareModal();
    }
  });

  // Initialize tool search listener if present
  document.addEventListener('DOMContentLoaded', function () {
    cacheInitialCardOrder();
    var searchInput = document.getElementById('toolSearchInput');
    if (searchInput) {
      searchInput.addEventListener('input', function (e) {
        window.currentSearchQuery = e.target.value;
        window.applyFilters();
      });
    }

    // Auto-scroll focused category pill into view when container has horizontal overflow
    document.querySelectorAll('.cat-pill-btn').forEach(function (pill) {
      pill.addEventListener('focus', function () {
        var container = pill.closest('.category-filter-pills');
        if (container && container.scrollWidth > container.clientWidth) {
          pill.scrollIntoView({ block: 'nearest', inline: 'nearest' });
        }
      });
    });

    // Check URL params on load to restore filter state without extra page load
    if (window.location.search) {
      var params = new URLSearchParams(window.location.search);
      var q = params.get('q');
      var cat = params.get('category');
      var price = params.get('price');
      var sort = params.get('sort');

      if (q && searchInput) searchInput.value = q;
      if (price) {
        var priceSelect = document.getElementById('priceFilter');
        if (priceSelect) priceSelect.value = price;
      }
      if (sort) {
        var sortSelect = document.getElementById('sortSelect');
        if (sortSelect) sortSelect.value = sort;
      }
      if (cat) {
        window.filterCategory(cat);
      } else if (q || price || sort) {
        window.applyFilters();
      }
    }
  });

})();
