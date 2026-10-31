import os
import re
import glob
import json

def scan_phase3_forensics():
    html_files = glob.glob('*.html') + glob.glob('*/*.html')
    html_files = [f.replace('\\', '/') for f in html_files]

    print(f"Total HTML files to inspect: {len(html_files)}")

    findings = {
        "instant_guarantee_claims": [],
        "support_24_7_claims": [],
        "refund_vs_replacement_discrepancies": [],
        "partner_or_authorized_claims": [],
        "lifetime_claims": [],
        "stale_price_references": [],
        "schema_discrepancies": [],
        "held_products_anomalies": [],
    }

    # Regex patterns
    rgx_instant = re.compile(r'\b(instant(?:\s+digital)?\s+delivery\s+in\s+15|guaranteed\s+(?:within\s+)?15\s*min|100%\s+instant)\b', re.IGNORECASE)
    rgx_24_7 = re.compile(r'\b(24/7(?:\s+support|\s+help|\s+live)?|round-the-clock)\b', re.IGNORECASE)
    rgx_money_back = re.compile(r'\b(money[- ]back\s+guarantee|100%\s+refund|full\s+refund\s+guarantee)\b', re.IGNORECASE)
    rgx_partner = re.compile(r'\b(official\s+partner|authorized\s+(?:reseller|distributor|dealer|agent))\b', re.IGNORECASE)
    rgx_lifetime = re.compile(r'\blifetime\b', re.IGNORECASE)

    # Held products
    held_slugs = ['turnitin-student', 'linkedin-premium', 'netflix-premium', 'spotify-premium', 'coursera-plus']

    for path in sorted(html_files):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check instant delivery claims
        for m in rgx_instant.finditer(content):
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            snippet = content[start:end].replace('\n', ' ')
            findings["instant_guarantee_claims"].append({
                "file": path,
                "match": m.group(0),
                "snippet": snippet
            })

        # Check 24/7 claims
        for m in rgx_24_7.finditer(content):
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            snippet = content[start:end].replace('\n', ' ')
            findings["support_24_7_claims"].append({
                "file": path,
                "match": m.group(0),
                "snippet": snippet
            })

        # Check money back refund claims
        for m in rgx_money_back.finditer(content):
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            snippet = content[start:end].replace('\n', ' ')
            findings["refund_vs_replacement_discrepancies"].append({
                "file": path,
                "match": m.group(0),
                "snippet": snippet
            })

        # Check partner / authorized claims
        for m in rgx_partner.finditer(content):
            start = max(0, m.start() - 60)
            end = min(len(content), m.end() + 60)
            snippet = content[start:end].replace('\n', ' ')
            # Check if negative/disclaimer
            lower = snippet.lower()
            if not any(neg in lower for neg in ["not directly affiliated", "not affiliated", "independent reseller", "independent", "neither", "no direct authorization", "disclaimer", "disclosure"]):
                findings["partner_or_authorized_claims"].append({
                    "file": path,
                    "match": m.group(0),
                    "snippet": snippet
                })

        # Check lifetime claims (valid ONLY on Windows 11 Pro)
        if 'windows-11-pro.html' not in path:
            for m in rgx_lifetime.finditer(content):
                start = max(0, m.start() - 40)
                end = min(len(content), m.end() + 40)
                snippet = content[start:end].replace('\n', ' ')
                findings["lifetime_claims"].append({
                    "file": path,
                    "match": m.group(0),
                    "snippet": snippet
                })

        # Check JSON-LD
        json_ld_matches = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]>(.*?)</script>', content, re.DOTALL)
        for jstr in json_ld_matches:
            try:
                data = json.loads(jstr.strip())
                if isinstance(data, dict):
                    if data.get('@type') == 'Product':
                        offers = data.get('offers', {})
                        if isinstance(offers, dict):
                            price = offers.get('price')
                            currency = offers.get('priceCurrency')
                            if not price or currency != 'PKR':
                                findings["schema_discrepancies"].append({
                                    "file": path,
                                    "issue": f"Product schema price={price}, currency={currency}"
                                })
            except Exception as e:
                findings["schema_discrepancies"].append({
                    "file": path,
                    "issue": f"JSON-LD parse error: {str(e)}"
                })

        # Check held products
        for h in held_slugs:
            if f"tools/{h}.html" == path:
                if "openQuickOrderModal" in content:
                    findings["held_products_anomalies"].append({
                        "file": path,
                        "issue": "Found openQuickOrderModal on held product detail page"
                    })

    print("\n--- FORENSIC FINDINGS SUMMARY ---")
    for category, items in findings.items():
        print(f"[{category}]: {len(items)} found")
        for it in items[:5]:
            print(f"  - {it.get('file')}: {it.get('match', '')} -> {it.get('snippet', it.get('issue', ''))}")
        if len(items) > 5:
            print(f"  ... and {len(items) - 5} more")

    with open('data/phase3_forensic_findings.json', 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2)
    print("\nFull findings saved to data/phase3_forensic_findings.json")

if __name__ == '__main__':
    scan_phase3_forensics()
