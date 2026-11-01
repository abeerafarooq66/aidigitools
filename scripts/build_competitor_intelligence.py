"""
AIDigiTools — Competitor Intelligence Database Builder
Strictly implements Section 4 of Master Architecture Charter:
COMPETITOR INTELLIGENCE ENGINE
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT_DIR / "data" / "competitor_intelligence.json"

COMPETITOR_DATABASE = {
    "version": "2.0.0",
    "last_updated": "October 2026",
    "governance_rule": (
        "Strictly compliant research. Never copy competitor text, titles, paragraphs, or layouts. "
        "Never guess or claim access to competitors' private analytics. "
        "The objective is discovering reader information gaps to create 10x more useful original content."
    ),
    "competitors": [
        {
            "id": "comp-001",
            "name": "AI Tools Pak",
            "domain": "aitoolspak.com",
            "type": "Regional AI Reseller & Marketplace",
            "market": "Pakistan (Domestic)",
            "primary_topics": [
                "ChatGPT Plus Pakistan",
                "Canva Pro EasyPaisa",
                "Midjourney Pakistan",
                "Claude Pro buy online",
                "Adobe Creative Cloud cheap"
            ],
            "typical_content_structure": [
                "Short promotional description (150-300 words)",
                "Price in PKR (often without breakdown)",
                "Basic WhatsApp order button",
                "Repetitive keyword tagging"
            ],
            "strengths": [
                "Fast WhatsApp response",
                "Accepts local domestic payment methods (EasyPaisa, JazzCash)"
            ],
            "weaknesses_and_content_gaps": [
                "Thin, low-utility content lacking technical depth",
                "Outdated model references (e.g. still mentioning GPT-3.5 or legacy Claude 2)",
                "No quantitative comparison tables with concrete metrics",
                "Zero explanation of usage limits, compute caps, or throttling policies",
                "Vague warranty terms without formal SLA or replacement commitments",
                "Missing structured data (FAQ, Breadcrumb, Product schema)",
                "No AEO / GEO quick answer summaries for voice or AI search"
            ],
            "unanswered_user_questions": [
                "How does the subscription actually work in Pakistan without international credit card?",
                "What is the exact monthly generation credit limit (e.g., Firefly, Midjourney Fast hours)?",
                "What happens if an account gets flagged or access drops after 2 weeks?",
                "How to activate Canvas or Artifacts workspace for coding projects?"
            ],
            "aidigitools_original_research_opportunity": [
                "Publish comprehensive, technical, 800-1500 word research guides",
                "Provide side-by-side quantitative HTML tables comparing official provider price vs. AIDigiTools concierge PKR price",
                "Clearly disclose the 15-minute delivery SLA and formal 30-day replacement warranty",
                "Include structured AEO Quick Answer capsules (35-70 words) for AI search citations",
                "Provide step-by-step troubleshooting for domestic payment rails (EasyPaisa, JazzCash, SadaPay, Raast)"
            ]
        },
        {
            "id": "comp-002",
            "name": "AI Tool Gems",
            "domain": "aitoolgems.com",
            "type": "Regional AI Tool Directory & Reseller",
            "market": "Pakistan & South Asia",
            "primary_topics": [
                "Best AI tools in Pakistan",
                "Runway Gen-3 price in PKR",
                "ElevenLabs creator Pakistan",
                "Cursor Pro alternative",
                "Perplexity Pro subscription"
            ],
            "typical_content_structure": [
                "Scraped provider bullet points",
                "Coupon code banners and promotional badges",
                "Generic listicles without first-hand verification insight",
                "Unverified 5-star customer review widgets"
            ],
            "strengths": [
                "Broad catalog covering many niche AI tools",
                "Active social media promotions"
            ],
            "weaknesses_and_content_gaps": [
                "Conflates official vendor retail prices with reseller prices, confusing users",
                "Displays unverified aggregate ratings violating Google Search quality essentials",
                "Fails to explain credit burn rates (e.g., how fast video/audio seconds deplete in Runway/ElevenLabs)",
                "Does not mention bank withholding tax (10% WHT) on foreign card payments",
                "Uses forbidden account-sharing buzzwords that risk user security"
            ],
            "unanswered_user_questions": [
                "Are these tools safe to use for business client projects?",
                "What is the difference between individual account activation vs organizational workspace seat?",
                "How does Cursor Composer compare to GitHub Copilot for Pakistani web developers?"
            ],
            "aidigitools_original_research_opportunity": [
                "Enforce transparent price separation (Provider USD price vs. AIDigiTools PKR offer)",
                "Zero fake ratings — 100% compliant Schema.org JSON-LD structured data",
                "Real-world credit usage benchmarks (e.g., exact cost per minute of video rendering)",
                "Full explanation of domestic tax savings when paying via local PKR rails",
                "Independent Reseller Disclaimers protecting brand transparency and user trust"
            ]
        },
        {
            "id": "comp-003",
            "name": "Official Provider Documentation",
            "domain": "openai.com, anthropic.com, cursor.com, midjourney.com",
            "type": "Primary Software Creators & Documentation",
            "market": "Global",
            "primary_topics": [
                "Technical feature documentation",
                "API reference & developer guides",
                "Release notes & changelogs"
            ],
            "typical_content_structure": [
                "Technical API parameters and system prompts",
                "Formal terms of service and billing FAQs based on US Stripe checkout",
                "Feature release notes"
            ],
            "strengths": [
                "Authoritative, definitive source for model capabilities, token limits, and updates"
            ],
            "weaknesses_and_content_gaps": [
                "Assumes global users have frictionless US/EU credit cards enabled for international e-commerce",
                "Completely silent on emerging market banking barriers (forex declines, 3D Secure failures in Pakistan)",
                "Highly technical jargon that overwhelms freelance designers, students, and small business owners"
            ],
            "unanswered_user_questions": [
                "Why is my Meezan / HBL / SadaPay card declining on OpenAI or Midjourney?",
                "How can a Pakistani agency bill AI tools without opening a foreign bank account?",
                "What are the best localized workflows for Pakistani YouTube automation channels?"
            ],
            "aidigitools_original_research_opportunity": [
                "Cite official provider docs as primary source of truth for all technical specs",
                "Bridge the localized accessibility gap with clear Pakistani payment activation guides",
                "Explain complex technical features in plain, accessible, workflow-oriented language"
            ]
        },
        {
            "id": "comp-004",
            "name": "Independent Tech Publications",
            "domain": "tomsguide.com, zapier.com/blog, techradar.com",
            "type": "Global Tech Media & Review Portals",
            "market": "US & Global Western Markets",
            "primary_topics": [
                "ChatGPT vs Claude comparison",
                "Best AI coding assistants",
                "Top AI video generators 2026"
            ],
            "typical_content_structure": [
                "Lengthy editorial reviews (2,000+ words)",
                "High-level benchmarking across generic US user personas",
                "Affiliate links to US pricing plans ($20/mo, $30/mo)"
            ],
            "strengths": [
                "Deep editorial testing and high search engine authority"
            ],
            "weaknesses_and_content_gaps": [
                "Zero relevance to Pakistani rupee purchasing power or South Asian freelance economy",
                "Does not cover regional latency, local banking, or domestic support",
                "Often slow to update localized exchange conversions and regional availability"
            ],
            "unanswered_user_questions": [
                "Is paying $20 USD (Rs. 5,600+ with taxes) worth it for a Pakistani university student?",
                "Can I share project artifacts with non-technical Pakistani clients easily?",
                "What are the best low-cost alternatives for beginner freelancers?"
            ],
            "aidigitools_original_research_opportunity": [
                "Produce deeply relevant, localized economic comparisons (e.g. ROI analysis for Pakistani freelancers)",
                "Address regional software ergonomics and internet speeds",
                "Provide direct WhatsApp concierge support that global publications can never offer"
            ]
        }
    ]
}

def build_database():
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(COMPETITOR_DATABASE, f, indent=2, ensure_ascii=False)
    print(f"Competitor Intelligence Database compiled successfully ({len(COMPETITOR_DATABASE['competitors'])} profiles) -> {OUTPUT_PATH}")

if __name__ == "__main__":
    build_database()
