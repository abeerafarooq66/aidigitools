"""
AIDigiTools — Central Product Fact Registry Builder
Strictly implements Section 2 of Master Architecture Charter:
CENTRAL PRODUCT INTELLIGENCE DATABASE
"""

import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PRODUCTS_MASTER_PATH = ROOT_DIR / "data" / "products_master.json"
OUTPUT_REGISTRY_PATH = ROOT_DIR / "data" / "central_product_registry.json"

HOLD_PRODUCTS = {
    "coursera-plus",
    "linkedin-premium",
    "netflix-premium",
    "spotify-premium",
    "turnitin-student"
}

# Documentation URLs mapping
DOCS_MAPPING = {
    "adobe-creative-cloud": "https://helpx.adobe.com/creative-cloud/user-guide.html",
    "canva-pro": "https://www.canva.com/help/",
    "capcut-pro": "https://www.capcut.com/support",
    "chatgpt-codex": "https://platform.openai.com/docs/guides/code-generation",
    "chatgpt-plus": "https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus",
    "claude-artifacts": "https://support.anthropic.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them",
    "claude-pro": "https://support.anthropic.com/en/articles/8324991-about-claude-pro-membership",
    "coursera-plus": "https://www.coursera.support/s/article/360036166172-Coursera-Plus",
    "cursor-pro": "https://docs.cursor.com/",
    "deepseek-pro": "https://api-docs.deepseek.com/",
    "elevenlabs-creator": "https://elevenlabs.io/docs",
    "envato-elements": "https://help.elements.envato.com/",
    "figma-pro": "https://help.figma.com/hc/en-us",
    "freepik-premium": "https://support.freepik.com/",
    "gamma-app": "https://help.gamma.app/",
    "gemini-advanced": "https://support.google.com/gemini/answer/14517446",
    "github-copilot": "https://docs.github.com/en/copilot",
    "google-ai-ultra": "https://support.google.com/gemini/answer/14517446",
    "google-veo": "https://deepmind.google/technologies/veo/",
    "grammarly-pro": "https://support.grammarly.com/",
    "grok-ai": "https://x.ai/blog/grok-2",
    "heygen-ai": "https://docs.heygen.com/",
    "jetbrains-all": "https://www.jetbrains.com/help/",
    "kling-ai": "https://klingai.com/",
    "leonardo-ai": "https://docs.leonardo.ai/",
    "linkedin-premium": "https://www.linkedin.com/help/linkedin/answer/a1338661",
    "lovable-ai": "https://docs.lovable.dev/",
    "microsoft-office-365": "https://support.microsoft.com/en-us/office",
    "midjourney": "https://docs.midjourney.com/",
    "minimax-ai": "https://www.minimaxi.com/document",
    "n8n-automation": "https://docs.n8n.io/",
    "netflix-premium": "https://help.netflix.com/",
    "nordvpn": "https://support.nordvpn.com/",
    "notion-business": "https://www.notion.so/help",
    "perplexity-pro": "https://www.perplexity.ai/hub/faq",
    "prime-video": "https://www.amazon.com/gp/help/customer/display.html?nodeId=G4662GJJ4529V67V",
    "quillbot-premium": "https://help.quillbot.com/",
    "replit-core": "https://docs.replit.com/",
    "runway-gen3": "https://help.runwayml.com/",
    "semrush-guru": "https://www.semrush.com/kb/",
    "spotify-premium": "https://support.spotify.com/",
    "suno-ai": "https://help.suno.ai/",
    "surfshark-vpn": "https://support.surfshark.com/",
    "tradingview-pro": "https://www.tradingview.com/support/",
    "turnitin-student": "https://help.turnitin.com/",
    "udio-ai": "https://www.udio.com/faq",
    "vidiq-boost": "https://support.vidiq.com/",
    "windows-11-pro": "https://support.microsoft.com/en-us/windows",
    "youtube-premium": "https://support.google.com/youtube/answer/6308116"
}

# Quota and Seat mappings
QUOTAS_MAPPING = {
    "adobe-creative-cloud": "1,000 monthly Firefly generative credits; 100GB cloud storage; 1 individual seat",
    "canva-pro": "1 TB cloud storage; unlimited Brand Kits; 500 monthly Magic Media uses; 1 seat",
    "capcut-pro": "100GB cloud storage; unlimited 4K 60fps exports; auto-captions; 1 seat",
    "chatgpt-codex": "Parallel agent execution; repository-level CLI reasoning; usage bounded by OpenAI token quotas",
    "chatgpt-plus": "Standard GPT-5/GPT-6 80 msgs / 3h (dynamic); Canvas; Advanced Voice; 1 individual seat",
    "claude-artifacts": "Interactive code canvas; React/SVG rendering; tied to Claude Sonnet/Opus compute quota",
    "claude-pro": "5x usage limits vs Free tier; 200,000 token context window; Projects workspace; 1 seat",
    "coursera-plus": "Unlimited access to 7,000+ courses; professional certificates; (INQUIRY ONLY)",
    "cursor-pro": "500 fast Claude 3.5 Sonnet / GPT-4o requests/month; unlimited slow requests; Cursor Composer",
    "deepseek-pro": "DeepSeek R1 & V3 reasoning compute; high-throughput API/Web seat",
    "elevenlabs-creator": "100,000 characters/month; commercial license; instant voice cloning; 1 seat",
    "envato-elements": "Unlimited digital downloads; commercial license; 1 seat",
    "figma-pro": "Unlimited Figma files and version history; Dev Mode access; team libraries; 1 seat",
    "freepik-premium": "100 downloads/day; full commercial license; priority Freepik AI image generation",
    "gamma-app": "Unlimited AI creation credits; custom branding; PDF/PowerPoint export; 1 seat",
    "gemini-advanced": "Gemini 1.5 Pro / Ultra with 1M-2M context window; 2TB Google One cloud storage; 1 seat",
    "github-copilot": "Unlimited inline completions; Copilot Chat; CLI integration; multi-editor support",
    "google-ai-ultra": "Gemini Ultra compute tier; 2TB storage; deep reasoning mode; 1 seat",
    "google-veo": "High-definition 1080p generative video; prompt-to-video compute allocation",
    "grammarly-pro": "Unlimited tone adjustments; 2,000 monthly AI prompt credits; plagiarism detection",
    "grok-ai": "Grok 2 / Grok 2 mini reasoning; real-time X data access; image generation via Aurora",
    "heygen-ai": "15-30 video credits/month; 4K video exports; custom avatar creation; 1 seat",
    "jetbrains-all": "15+ IDEs (IntelliJ, PyCharm, WebStorm, CLion); perpetual fallback license; 1 seat",
    "kling-ai": "660 monthly credits; 1080p 30fps AI video generation; camera motion controls",
    "leonardo-ai": "8,500 monthly fast tokens; Alchemy pipeline; photoreal engine; 1 seat",
    "linkedin-premium": "Business/Career tier; InMail credits; who viewed your profile; (INQUIRY ONLY)",
    "lovable-ai": "Full-stack code generation; unlimited public projects; Supabase integration; 1 seat",
    "microsoft-office-365": "Word, Excel, PowerPoint, Outlook desktop apps; 1TB OneDrive cloud storage; 1 seat",
    "midjourney": "Fast GPU hours allocation; Relax mode unlimited (Standard); stealth generation (Pro)",
    "minimax-ai": "Hailuo video credits; high-fidelity physics simulation; 720p/1080p video generation",
    "n8n-automation": "Self-hosted / Cloud workflow executions; 500+ integrations; community/enterprise nodes",
    "netflix-premium": "4K Ultra HD streaming; HDR; spatial audio; 4 concurrent devices; (INQUIRY ONLY)",
    "nordvpn": "10 simultaneous devices; 6,000+ high-speed servers; Threat Protection Pro; 1 seat",
    "notion-business": "Unlimited team members; private teamspaces; 90-day page history; SAML SSO",
    "perplexity-pro": "300+ Pro queries/day; Claude 3.5 Sonnet, GPT-4o, Sonar Large selection; file uploads",
    "prime-video": "4K Ultra HD streaming; Prime Video exclusive originals; (INQUIRY ONLY)",
    "quillbot-premium": "Unlimited words in Paraphraser; 25,000 Summarizer words; Plagiarism Checker credits",
    "replit-core": "Replit Agent compute credits; unlimited private Repls; high-speed cloud compute VMs",
    "runway-gen3": "625 monthly credits; Gen-3 Alpha text-to-video / image-to-video; custom motion brush",
    "semrush-guru": "1,500 keywords to track; 30,000 results per report; historical data; Content Marketing",
    "spotify-premium": "Individual ad-free audio streaming; offline downloads; 320kbps audio; (INQUIRY ONLY)",
    "suno-ai": "2,500 monthly credits (500 songs); commercial rights; priority generation queue",
    "surfshark-vpn": "Unlimited simultaneous devices; CleanWeb ad blocker; multi-hop VPN servers; 1 seat",
    "tradingview-pro": "5 indicators per chart; 2 charts in one window; 10K historical bars; ad-free",
    "turnitin-student": "Originality check; AI detection report; (INQUIRY ONLY)",
    "udio-ai": "1,200 monthly credits; 2-minute audio tracks; stem separation; commercial terms",
    "vidiq-boost": "50 daily AI video ideas; keyword search volume tool; competitor tracker; 1 channel",
    "windows-11-pro": "1 PC permanent digital retail license; BitLocker; Hyper-V; Remote Desktop",
    "youtube-premium": "Ad-free video playback; background play; YouTube Music Premium; offline downloads"
}

def build_registry():
    with open(PRODUCTS_MASTER_PATH, "r", encoding="utf-8") as f:
        master_products = json.load(f)

    registry = []

    for p in master_products:
        slug = p["slug"]
        is_hold = slug in HOLD_PRODUCTS or p.get("sale_eligibility") == "Hold / Inquiry Only"
        
        canonical_name = p.get("official_product_name", p.get("name", slug.title()))
        brand = p.get("brand", "Unknown")
        official_url = p.get("official_url", "")
        docs_url = DOCS_MAPPING.get(slug, official_url)
        pricing_url = p.get("official_pricing_url", official_url)
        official_plan = p.get("official_plan_name", "Standard")
        
        provider_price = p.get("official_price", "N/A")
        provider_currency = p.get("currency", "USD")
        
        aidigitools_price_pkr = p.get("aidigitools_price_pkr")
        aidigitools_price_usd = p.get("aidigitools_price_usd")
        
        features = p.get("features", [])
        if isinstance(features, str):
            features = [f.strip() for f in features.split(",") if f.strip()]
            
        limitations = p.get("limitations", "Standard single-seat commercial or personal limits.")
        quotas_info = QUOTAS_MAPPING.get(slug, "Standard provider quotas and seat limits apply.")
        
        geo_avail = p.get("pakistan_availability", "Global availability. Direct payment may require foreign currency transaction enablement.")
        
        access_model = "Verified Workspace Seat / Activation Service (Concierge)"
        if slug == "windows-11-pro":
            access_model = "Genuine Retail Product Key Activation (Single PC Perpetual)"
        elif is_hold:
            access_model = "Informational & Inquiry Concierge (Sales currently on hold pending licensing review)"
            
        supplier_evidence = (
            "Independent Subscription Concierge. No official distributor or partnership claimed. "
            "All trademarks belong to their respective copyright holders. "
            "Concierge access provisioned via verified workspace invites or direct digital activation."
        )
        
        provider_terms = f"Subject to {brand} official Terms of Service, Acceptable Use Policies, and regional end-user licensing agreements."
        
        warranty_ordering = (
            "15-minute digital delivery SLA via official WhatsApp concierge (+92 332 6861112 / 03326861112). "
            "Covered by AIDigiTools 30-day replacement warranty. Domestic settlement via EasyPaisa, JazzCash, SadaPay, Raast, or Bank IBFT; international via Wise/Crypto."
        )
        
        restricted_status = "Hold / Inquiry Only" if is_hold else "Normal / Active"
        purchase_cta_permitted = not is_hold
        
        entry = {
            "slug": slug,
            "canonical_product_name": canonical_name,
            "provider_brand": brand,
            "official_website_url": official_url,
            "official_documentation_url": docs_url,
            "official_pricing_source_url": pricing_url,
            "official_plan_names": official_plan,
            "official_provider_price": f"${provider_price} {provider_currency}/month" if provider_price != "N/A" else "Official Vendor Pricing",
            "verified_features": features,
            "verified_limitations": limitations,
            "credits_quotas_usage_limits": quotas_info,
            "geographic_availability_and_restrictions": geo_avail,
            "access_delivery_model": access_model,
            "aidigitools_offer_price_pkr": aidigitools_price_pkr,
            "aidigitools_offer_price_usd": aidigitools_price_usd,
            "price_currency": "PKR / USD",
            "billing_period": p.get("billing_period", "Monthly"),
            "price_source_and_last_verified": f"{p.get('pricing_last_verified', 'October 2026')} (Independent AIDigiTools Concierge Audit)",
            "current_availability": "InquiryOnly" if is_hold else "InStock",
            "supplier_authorization_status": supplier_evidence,
            "provider_terms_and_access_restrictions": provider_terms,
            "aidigitools_warranty_and_ordering_info": warranty_ordering,
            "restricted_status": restricted_status,
            "purchase_cta_permitted": purchase_cta_permitted,
            "primary_category": p.get("primary_category", "AI Tools"),
            "tool_page_url": f"https://aidigitools.tech/tools/{slug}.html"
        }
        
        registry.append(entry)

    # Write output
    with open(OUTPUT_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully compiled Central Product Fact Registry ({len(registry)} products) -> {OUTPUT_REGISTRY_PATH}")
    print(f"Active ForSale Products (Purchase CTA Permitted): {sum(1 for p in registry if p['purchase_cta_permitted'])}")
    print(f"Hold / Inquiry Only Products (Purchase CTA Blocked): {sum(1 for p in registry if not p['purchase_cta_permitted'])}")

if __name__ == "__main__":
    build_registry()
