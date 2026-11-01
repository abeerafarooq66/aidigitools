"""
AIDigiTools — Content Clusters & Product Mapping Registry Builder
Strictly implements Section 6 of Master Architecture Charter:
CONTENT CLUSTER AND PRODUCT MAPPING
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT_DIR / "data" / "content_clusters.json"

CLUSTERS = [
    {
        "cluster_id": "cluster-01",
        "slug": "ai-assistants-and-llms",
        "name": "AI Assistants & Frontier LLMs",
        "description": "Frontier reasoning models, conversational intelligence, voice interfaces, and multimodal LLMs.",
        "primary_category_url": "https://aidigitools.tech/categories/coding.html",
        "associated_products": [
            "chatgpt-plus", "claude-pro", "gemini-advanced", "perplexity-pro",
            "grok-ai", "deepseek-pro", "google-ai-ultra"
        ],
        "supporting_comparisons_and_guides": [
            "https://aidigitools.tech/compare/chatgpt-vs-claude.html",
            "https://aidigitools.tech/guides/chatgpt-vs-claude.html"
        ],
        "target_reader_personas": [
            "Pakistani University Students & Researchers",
            "Remote Knowledge Workers & Consultants",
            "Software Engineers & Technical Leads"
        ],
        "planned_blog_topics": [
            "blog/claude-artifacts-practical-guide-freelancers.html",
            "blog/deepseek-r1-vs-chatgpt-reasoning-analysis.html"
        ]
    },
    {
        "cluster_id": "cluster-02",
        "slug": "ai-coding-and-development",
        "name": "AI Coding & Agentic Development",
        "description": "AI-powered IDEs, code generation, autonomous coding agents, multi-file refactoring, and developer CLI tools.",
        "primary_category_url": "https://aidigitools.tech/categories/coding.html",
        "associated_products": [
            "cursor-pro", "github-copilot", "chatgpt-codex", "replit-core",
            "lovable-ai", "jetbrains-all"
        ],
        "supporting_comparisons_and_guides": [
            "https://aidigitools.tech/best/best-ai-coding-tools.html"
        ],
        "target_reader_personas": [
            "Pakistani Full-Stack Web & Mobile Developers",
            "Upwork / Fiverr Remote Software Engineers",
            "Tech Agency Technical Directors"
        ],
        "planned_blog_topics": [
            "blog/cursor-ai-vs-github-copilot-comparison.html",
            "blog/ai-coding-workflow-optimization-freelancers.html"
        ]
    },
    {
        "cluster_id": "cluster-03",
        "slug": "ai-image-and-design-tools",
        "name": "AI Image, Graphic Design & Creative Suites",
        "description": "Generative imagery, photo editing, vector illustrations, UI/UX prototyping, and template platforms.",
        "primary_category_url": "https://aidigitools.tech/categories/image.html",
        "associated_products": [
            "midjourney", "canva-pro", "adobe-creative-cloud", "leonardo-ai",
            "freepik-premium", "envato-elements", "figma-pro"
        ],
        "supporting_comparisons_and_guides": [],
        "target_reader_personas": [
            "Freelance Graphic Designers & UI/UX Creators",
            "Digital Marketing Specialists & Social Media Managers",
            "E-commerce Brand Owners"
        ],
        "planned_blog_topics": [
            "blog/midjourney-v6-prompting-guide-graphic-designers.html",
            "blog/canva-magic-studio-vs-adobe-firefly-comparison.html"
        ]
    },
    {
        "cluster_id": "cluster-04",
        "slug": "ai-video-and-audio-tools",
        "name": "AI Video, Speech & Audio Generation",
        "description": "Text-to-video generation, AI timeline editing, voice replication, music composition, and automated captions.",
        "primary_category_url": "https://aidigitools.tech/categories/video.html",
        "associated_products": [
            "runway-gen3", "capcut-pro", "kling-ai", "heygen-ai",
            "minimax-ai", "google-veo", "elevenlabs-creator", "suno-ai", "udio-ai"
        ],
        "supporting_comparisons_and_guides": [
            "https://aidigitools.tech/best/best-ai-video-generators.html",
            "https://aidigitools.tech/compare/runway-vs-pika.html"
        ],
        "target_reader_personas": [
            "YouTube Automation & Faceless Channel Creators",
            "Short-Form Video Editors (Reels/TikTok/Shorts)",
            "Podcast Producers & Audio Designers"
        ],
        "planned_blog_topics": [
            "blog/runway-gen3-vs-capcut-pro-video-comparison.html",
            "blog/elevenlabs-voice-cloning-youtube-workflow.html"
        ]
    },
    {
        "cluster_id": "cluster-05",
        "slug": "writing-and-productivity",
        "name": "AI Writing, Research & Workplace Productivity",
        "description": "Grammar enhancement, document summarization, presentation generation, and workspace knowledge bases.",
        "primary_category_url": "https://aidigitools.tech/categories/coding.html",
        "associated_products": [
            "grammarly-pro", "quillbot-premium", "notion-business", "gamma-app",
            "microsoft-office-365", "turnitin-student"
        ],
        "supporting_comparisons_and_guides": [],
        "target_reader_personas": [
            "Content Writers, Copywriters & Academic Students",
            "Corporate Project Managers & Remote Executives"
        ],
        "planned_blog_topics": [
            "blog/quillbot-vs-grammarly-academic-writing-guide.html"
        ]
    },
    {
        "cluster_id": "cluster-06",
        "slug": "digital-marketing-and-seo",
        "name": "AI for Digital Marketing & SEO",
        "description": "Keyword volume discovery, backlink analytics, YouTube algorithm optimization, and content audit tools.",
        "primary_category_url": "https://aidigitools.tech/categories/video.html",
        "associated_products": [
            "semrush-guru", "vidiq-boost"
        ],
        "supporting_comparisons_and_guides": [],
        "target_reader_personas": [
            "SEO Specialists & Agency Owners in Pakistan",
            "YouTube Growth Managers & Channel Strategists"
        ],
        "planned_blog_topics": [
            "blog/vidiq-boost-youtube-seo-growth-guide.html"
        ]
    },
    {
        "cluster_id": "cluster-07",
        "slug": "developer-apis-and-automation",
        "name": "Developer APIs & Agentic Automation",
        "description": "Workflow orchestration, webhook integrations, autonomous subagent chains, and self-hosted automation.",
        "primary_category_url": "https://aidigitools.tech/categories/coding.html",
        "associated_products": [
            "n8n-automation", "chatgpt-codex", "deepseek-pro"
        ],
        "supporting_comparisons_and_guides": [],
        "target_reader_personas": [
            "DevOps Engineers & Backend Architects",
            "Automation Agency Leads & Solopreneurs"
        ],
        "planned_blog_topics": [
            "blog/n8n-ai-automation-workflows-small-business.html"
        ]
    },
    {
        "cluster_id": "cluster-08",
        "slug": "freelancers-and-small-businesses",
        "name": "AI Stacks for Freelancers & Small Businesses",
        "description": "Budget-optimized software stacks, commercial licenses, high-ROI toolkits, and client project deliverables.",
        "primary_category_url": "https://aidigitools.tech/categories/coding.html",
        "associated_products": [
            "canva-pro", "cursor-pro", "capcut-pro", "adobe-creative-cloud",
            "elevenlabs-creator", "notion-business"
        ],
        "supporting_comparisons_and_guides": [
            "https://aidigitools.tech/deals.html"
        ],
        "target_reader_personas": [
            "Pakistani Freelancers on Upwork, Fiverr & LinkedIn",
            "Local Digital Micro-Agencies & Startups"
        ],
        "planned_blog_topics": [
            "blog/best-ai-software-stack-pakistani-freelancers.html"
        ]
    },
    {
        "cluster_id": "cluster-09",
        "slug": "pricing-plans-and-cost-comparisons",
        "name": "AI Pricing, Plans & Currency Cost Comparisons",
        "description": "Transparent PKR vs. USD cost breakdowns, domestic payment rail guides, forex tax savings, and plan ROI.",
        "primary_category_url": "https://aidigitools.tech/deals.html",
        "associated_products": [
            "chatgpt-plus", "claude-pro", "cursor-pro", "adobe-creative-cloud"
        ],
        "supporting_comparisons_and_guides": [
            "https://aidigitools.tech/policies.html"
        ],
        "target_reader_personas": [
            "Budget-Conscious Students & Freelancers",
            "Agencies Seeking Predictable Monthly Software Costs"
        ],
        "planned_blog_topics": [
            "blog/ai-subscriptions-pakistan-payment-methods-guide.html"
        ]
    },
    {
        "cluster_id": "cluster-10",
        "slug": "privacy-security-and-responsible-use",
        "name": "AI Privacy, Security & Responsible Software Access",
        "description": "Secure encrypted browsing, PC security licenses, safe AI workspace hygiene, and non-fraudulent access.",
        "primary_category_url": "https://aidigitools.tech/categories/vpn.html",
        "associated_products": [
            "nordvpn", "surfshark-vpn", "windows-11-pro"
        ],
        "supporting_comparisons_and_guides": [
            "https://aidigitools.tech/policies.html",
            "https://aidigitools.tech/affiliate-disclosure.html"
        ],
        "target_reader_personas": [
            "Remote Developers Handling Confidential Client Code",
            "Digital Nomads Requiring Secure Static IPs"
        ],
        "planned_blog_topics": [
            "blog/vpn-security-guide-remote-freelancers-pakistan.html"
        ]
    }
]

def build_clusters():
    data = {
        "version": "2.0.0",
        "total_clusters": len(CLUSTERS),
        "clusters": CLUSTERS
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Content Clusters & Product Mapping Registry built ({len(CLUSTERS)} clusters) -> {OUTPUT_PATH}")

if __name__ == "__main__":
    build_clusters()

