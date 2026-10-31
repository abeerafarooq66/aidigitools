"""
scripts/phase3_claims_inventory.py
Phase 3 Task 1 — Exhaustive Business Claims Inventory
Scans all 66 HTML documents, JS, XML, and text files for:
- Authorization / Partnership claims
- Account authenticity & supply claims
- Replacement & warranty claims
- Refund & money-back guarantees
- Delivery SLA promises
- Instant activation claims
- Security & encryption assertions
- Payment rails & availability
- Lifetime / permanent access claims
- Availability & pause/hold status consistency
"""

import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

CLAIM_PATTERNS = [
    ("Authorization / Partnership", re.compile(r'(?i)\b(authorized\s+(?:reseller|partner|distributor|dealer)|official\s+(?:partner|reseller|distributor)|certified\s+partner)\b')),
    ("Account Supply / Authenticity", re.compile(r'(?i)\b(genuine\s+(?:license|account|subscription|key)|original\s+account|official\s+license|verified\s+account|verified\s+subscription|no\s+stolen|no\s+trial|cracked|shared\s+slot|edu\s+pack)\b')),
    ("Warranty & Replacement", re.compile(r'(?i)\b(30-day\s+replacement|replacement\s+warranty|warranty\s+policy|lifetime\s+warranty|replacement\s+guarantee)\b')),
    ("Refunds & Money Back", re.compile(r'(?i)\b(money-back\s+guarantee|100%\s+refund|unconditional\s+refund|full\s+refund|refunds?\s+policy|refunds?\s+guaranteed?)\b')),
    ("Delivery SLA", re.compile(r'(?i)\b(15-min(?:ute)?\s+(?:delivery|target|setup|fulfillment)|instant\s+(?:delivery|setup|activation|access)|immediate\s+delivery)\b')),
    ("Security & Privacy", re.compile(r'(?i)\b(bank-grade\s+security|100%\s+secure|military-grade\s+encryption|zero-risk\s+payment|guaranteed\s+safety)\b')),
    ("Support Availability", re.compile(r'(?i)\b(24/7\s+support|round-the-clock|instant\s+support|always\s+online)\b')),
    ("Lifetime Claims", re.compile(r'(?i)\b(lifetime\s+(?:access|license|subscription|updates|validity))\b')),
    ("Urgency / False Scarcity", re.compile(r'(?i)\b(only\s+\d+\s+left|limited\s+time\s+offer|hurry|flash\s+sale|expires\s+in|ends\s+tonight)\b')),
    ("Private Account Details Exposure", re.compile(r'(?i)\b(03\d{9}|[A-Z0-9]{16,24}|pk\d{2}[a-z]{4}\d{16})\b')),
    ("Order vs Pause Contradictions", re.compile(r'(?i)\b(orders?\s+on\s+hold|direct\s+orders?\s+currently\s+on\s+hold|direct\s+orders?\s+paused|inquiry\s+only)\b'))
]

def scan_files():
    findings = []
    file_count = 0

    target_exts = ('.html', '.js', '.xml', '.txt', '.json')

    for root, dirs, files in os.walk(ROOT_DIR):
        if any(p in root for p in ['.git', 'node_modules', '.gemini', 'scratch']):
            continue
        for f in files:
            if not f.endswith(target_exts):
                continue
            path = os.path.join(root, f)
            rel_path = os.path.relpath(path, ROOT_DIR)
            file_count += 1

            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()

            for line_no, line in enumerate(lines, 1):
                clean_line = line.strip()
                if not clean_line:
                    continue

                for cat_name, pattern in CLAIM_PATTERNS:
                    match = pattern.search(clean_line)
                    if match:
                        findings.append({
                            "category": cat_name,
                            "file": rel_path,
                            "line": line_no,
                            "matched": match.group(0),
                            "context": clean_line[:180]
                        })

    return file_count, findings

if __name__ == '__main__':
    print("=== Scanning repository for Phase 3 Business Claims Inventory ===")
    count, results = scan_files()
    print(f"Total files scanned: {count}")
    print(f"Total claims flagged: {len(results)}\n")

    by_cat = {}
    for r in results:
        by_cat.setdefault(r['category'], []).append(r)

    for cat, items in by_cat.items():
        print(f"📂 {cat}: {len(items)} instances")
        # Show top 3 samples
        for item in items[:3]:
            print(f"   - {item['file']}:{item['line']} -> [{item['matched']}] \"{item['context'][:100]}...\"")

    # Save full inventory to JSON
    out_path = os.path.join(ROOT_DIR, 'data', 'business_claims_inventory.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nFull inventory saved to: {out_path}")
