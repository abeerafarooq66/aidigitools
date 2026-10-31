import os
import glob
import re
import json

def audit_geo_aeo():
    tool_files = sorted(glob.glob('tools/*.html'))
    tool_files = [f.replace('\\\\', '/').replace('\\', '/') for f in tool_files]
    print(f"Auditing all {len(tool_files)} tool pages for Phase 5 GEO/AEO & Entity SEO...")

    results = {
        "total_tools": len(tool_files),
        "missing_spec_block": [],
        "missing_vendor_citation": [],
        "missing_faq_section": [],
        "missing_limitations": [],
        "missing_alternatives": [],
        "missing_freshness_date": [],
        "thin_content_pages": [],
        "entity_accuracy": {
            "valid": 0,
            "issues": []
        }
    }

    vendor_domains = [
        "openai.com", "anthropic.com", "midjourney.com", "cursor.com", "adobe.com", "canva.com",
        "capcut.com", "github.com", "perplexity.ai", "deepseek.com", "google.com", "jetbrains.com",
        "replit.com", "figma.com", "notion.so", "nordvpn.com", "surfshark.com", "elevenlabs.io",
        "klingai.com", "runwayml.com", "suno.com", "udio.com", "semrush.com", "grammarly.com",
        "netflix.com", "youtube.com", "quillbot.com", "freepik.com", "envato.com", "linkedin.com", "x.ai",
        "deepmind.google", "leonardo.ai", "hailuoai.video", "heygen.com", "gamma.app", "n8n.io", "vidiq.com",
        "coursera.org", "lovable.dev", "spotify.com", "microsoft.com", "primevideo.com", "tradingview.com", "turnitin.com"
    ]

    for path in tool_files:
        with open(path, 'r', encoding='utf-8') as fp:
            content = fp.read()

        # 1. Spec block
        has_spec_block = 'phase6-spec-block' in content
        if not has_spec_block:
            results["missing_spec_block"].append(path)

        # 2. Vendor citation
        has_vendor = False
        links = re.findall(r'<a\s+[^>]*href=[\'"](https?://[^\'"]+)[\'"]', content, re.I)
        for url in links:
            if any(v in url for v in vendor_domains):
                has_vendor = True
                break
        if not has_vendor:
            results["missing_vendor_citation"].append(path)

        # 3. FAQ section
        has_faq = '<details' in content and 'faq' in content.lower()
        if not has_faq:
            results["missing_faq_section"].append(path)

        # 4. Limitations
        has_limits = any(term in content.lower() for term in ['limitation', 'limits', 'excludes', 'quota', 'cap', 'fair use'])
        if not has_limits:
            results["missing_limitations"].append(path)

        # 5. Alternatives
        has_alts = 'alternatives' in content.lower() or 'alternative' in content.lower()
        if not has_alts:
            results["missing_alternatives"].append(path)

        # 6. Freshness date
        has_fresh = 'October 2026' in content or '2026-10' in content
        if not has_fresh:
            results["missing_freshness_date"].append(path)

        # 7. Word count of body content (excluding tags)
        body_text = re.sub(r'<[^>]+>', ' ', content)
        words = len(body_text.split())
        if words < 400:
            results["thin_content_pages"].append((path, words))

    print("\n================ GEO / AEO / ENTITY AUDIT SUMMARY ================")
    print(f"Total Tool Pages Audited: {results['total_tools']}")
    print(f"Missing Spec Block: {len(results['missing_spec_block'])}")
    print(f"Missing Vendor Citations: {len(results['missing_vendor_citation'])}")
    print(f"Missing FAQ Section: {len(results['missing_faq_section'])}")
    print(f"Missing Limitations Disclosure: {len(results['missing_limitations'])}")
    print(f"Missing Relevant Alternatives: {len(results['missing_alternatives'])}")
    print(f"Missing October 2026 Freshness: {len(results['missing_freshness_date'])}")
    print(f"Thin Content Pages (<400 words): {len(results['thin_content_pages'])}")
    print("==================================================================")

    with open('data/phase5_geo_aeo_audit.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print("Full report saved to data/phase5_geo_aeo_audit.json")
    return sum([
        len(results['missing_spec_block']),
        len(results['missing_vendor_citation']),
        len(results['missing_faq_section']),
        len(results['missing_limitations']),
        len(results['missing_alternatives']),
        len(results['missing_freshness_date']),
        len(results['thin_content_pages'])
    ])

if __name__ == '__main__':
    audit_geo_aeo()
