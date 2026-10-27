import os
import re
import urllib.parse
import glob

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def audit_whatsapp_urls():
    print("=" * 70)
    print("AIDigiTools — Comprehensive WhatsApp URLs & Business Phone Audit")
    print("=" * 70)

    # 1. Scope: Production Storefront Files
    production_files = []
    for f in glob.glob(os.path.join(REPO_ROOT, "*.html")):
        production_files.append(f)
    for sub in ["categories", "tools", "compare", "guides", "best"]:
        for f in glob.glob(os.path.join(REPO_ROOT, sub, "*.html")):
            production_files.append(f)
    production_files.append(os.path.join(REPO_ROOT, "assets", "cart.js"))

    print(f"Total production storefront files in scope: {len(production_files)}")

    wa_pattern = re.compile(r'https?://(?:wa\.me|api\.whatsapp\.com/send\?phone=)/?([0-9+]+)?(\?[^"\'\s<>]+)?', re.IGNORECASE)
    canonical_phone = "923326861112"

    prod_findings = []
    prod_discrepancies = []
    total_prod_links = 0

    for path in sorted(production_files):
        rel_path = os.path.relpath(path, REPO_ROOT).replace("\\", "/")
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue

        for m in wa_pattern.finditer(content):
            total_prod_links += 1
            raw_url = m.group(0)
            phone_num = (m.group(1) or "").replace("+", "").strip()
            query_str = m.group(2) or ""

            text_param = ""
            if query_str.startswith("?"):
                parsed_query = urllib.parse.parse_qs(query_str[1:])
                text_param = parsed_query.get("text", [""])[0]

            if phone_num != canonical_phone:
                prod_discrepancies.append({
                    "file": rel_path,
                    "url": raw_url,
                    "phone": phone_num
                })
            else:
                prod_findings.append({
                    "file": rel_path,
                    "url": raw_url,
                    "phone": phone_num,
                    "text": text_param
                })

    print(f"Total WhatsApp URLs found in production storefront: {total_prod_links}")
    if prod_discrepancies:
        print(f"[FAIL] Found {len(prod_discrepancies)} discrepancies in production storefront:")
        for d in prod_discrepancies:
            print(f"  - {d['file']}: Phone '{d['phone']}' in URL: {d['url']}")
    else:
        print(f"[PASS] 100% of production storefront WhatsApp links ({total_prod_links}) strictly target canonical phone: +92 332 6861112 ({canonical_phone})")

    # 2. Scope: Internal tests and scripts
    print("\nAuditing test regexes and helper scripts:")
    test_files = glob.glob(os.path.join(REPO_ROOT, "tests", "*.py")) + glob.glob(os.path.join(REPO_ROOT, "scripts", "*.py"))
    test_hits = []
    for path in test_files:
        rel_path = os.path.relpath(path, REPO_ROOT).replace("\\", "/")
        content = open(path, "r", encoding="utf-8", errors="ignore").read()
        for m in wa_pattern.finditer(content):
            raw_url = m.group(0)
            phone = (m.group(1) or "").replace("+", "").strip()
            test_hits.append((rel_path, raw_url, phone))

    print(f"Total WhatsApp string occurrences in tests/scripts: {len(test_hits)}")
    for hit in test_hits:
        status = "CANONICAL PHONE" if hit[2] == canonical_phone else "PREFIX/PATTERN CHECK"
        print(f"  - {hit[0]:45} | Pattern: {hit[1]:30} | Phone: '{hit[2]}' ({status})")

    print("\n" + "=" * 70)
    return len(prod_discrepancies) == 0

if __name__ == "__main__":
    success = audit_whatsapp_urls()
    exit(0 if success else 1)
