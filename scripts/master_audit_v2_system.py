import os
import re
import json
import glob
from bs4 import BeautifulSoup

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(REPO_ROOT)

print(f"=== AIDigiTools Master Audit V2 System (Master Book Standard) ===")
print(f"Auditing root: {REPO_ROOT}")

html_files = []
for root, dirs, files in os.walk(REPO_ROOT):
    if any(p in root for p in [".git", "scratch", ".gemini", "audit_reports", "node_modules"]):
        continue
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.relpath(os.path.join(root, f), REPO_ROOT))

html_files = sorted(html_files)
print(f"Total HTML pages discovered for forensic audit: {len(html_files)}\n")

audit_results = {
    "total_pages": len(html_files),
    "critical_issues": [],
    "high_issues": [],
    "medium_issues": [],
    "pages_audit": {}
}

payment_terms_pattern = re.compile(r'\b(sadapay|nayapay|jazzcash|easypaisa|raast)\b', re.IGNORECASE)

for file_rel in html_files:
    file_path = os.path.join(REPO_ROOT, file_rel)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    page_report = {
        "file": file_rel,
        "h1_count": len(soup.find_all("h1")),
        "h1_text": soup.find("h1").get_text(strip=True) if soup.find("h1") else None,
        "title": soup.title.get_text(strip=True) if soup.title else None,
        "meta_desc": soup.find("meta", attrs={"name": "description"}).get("content", "") if soup.find("meta", attrs={"name": "description"}) else None,
        "canonical": soup.find("link", attrs={"rel": "canonical"}).get("href", "") if soup.find("link", attrs={"rel": "canonical"}) else None,
        "quick_answer": bool(soup.find(class_=re.compile(r'\bquick-answer\b'))),
        "schemas": [],
        "product_availability": None,
        "images_total": len(soup.find_all("img")),
        "images_missing_alt": 0,
        "images_missing_dimensions": 0,
        "images_missing_lazy": 0,
        "quotes_count": len(soup.find_all("blockquote")) + len(re.findall(r'["“][^"”]{20,200}["”]', content)),
        "stats_count": len(re.findall(r'\b\d+(?:\.\d+)?%\b|\b\d+K\b|\bRs\.\s*\d+[\d,]*\b', content)),
        "internal_links_count": len([a for a in soup.find_all("a", href=True) if not a['href'].startswith(('http://', 'https://', 'mailto:', 'tel:', 'wa.me'))]),
        "payment_mentions": len(payment_terms_pattern.findall(content)),
        "issues": []
    }

    # Headings check
    if page_report["h1_count"] == 0:
        page_report["issues"].append("Missing H1 heading (Critical)")
        audit_results["critical_issues"].append(f"{file_rel}: Missing H1 heading")
    elif page_report["h1_count"] > 1:
        page_report["issues"].append(f"Multiple H1 headings found ({page_report['h1_count']}) (High)")
        audit_results["high_issues"].append(f"{file_rel}: Multiple H1 headings ({page_report['h1_count']})")

    # Meta Title check
    if not page_report["title"]:
        page_report["issues"].append("Missing <title> tag (Critical)")
        audit_results["critical_issues"].append(f"{file_rel}: Missing <title>")
    elif len(page_report["title"]) < 25:
        page_report["issues"].append(f"Title too short ({len(page_report['title'])} chars) (Medium)")
    elif len(page_report["title"]) > 75:
        page_report["issues"].append(f"Title too long ({len(page_report['title'])} chars) (Medium)")

    # Meta Description check
    if not page_report["meta_desc"]:
        page_report["issues"].append("Missing meta description (High)")
        audit_results["high_issues"].append(f"{file_rel}: Missing meta description")
    elif len(page_report["meta_desc"]) < 50:
        page_report["issues"].append(f"Meta description too short ({len(page_report['meta_desc'])} chars) (Medium)")
    elif len(page_report["meta_desc"]) > 170:
        page_report["issues"].append(f"Meta description too long ({len(page_report['meta_desc'])} chars) (Medium)")

    # Canonical check
    if not page_report["canonical"]:
        page_report["issues"].append("Missing canonical link (High)")
        audit_results["high_issues"].append(f"{file_rel}: Missing canonical link")

    # Schema inspection
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    for s in scripts:
        try:
            raw_text = s.string or s.get_text()
            data = json.loads(raw_text)
            stype = data.get("@type")
            if "@graph" in data:
                graph_types = [node.get("@type") for node in data["@graph"] if "@type" in node]
                page_report["schemas"].extend(graph_types)
                for node in data["@graph"]:
                    if node.get("@type") == "Product":
                        page_report["product_availability"] = node.get("offers", {}).get("availability")
            else:
                page_report["schemas"].append(stype)
                if stype == "Product":
                    page_report["product_availability"] = data.get("offers", {}).get("availability")
        except Exception as e:
            page_report["issues"].append(f"Invalid JSON-LD syntax: {e} (High)")
            audit_results["high_issues"].append(f"{file_rel}: Invalid JSON-LD syntax")

    # Image attributes check (Core Web Vitals & CLS)
    for img in soup.find_all("img"):
        if not img.get("alt") or img.get("alt").strip() == "":
            page_report["images_missing_alt"] += 1
        if not (img.get("width") and img.get("height")):
            page_report["images_missing_dimensions"] += 1
        if not img.get("loading") and file_rel != "index.html":
            page_report["images_missing_lazy"] += 1

    if page_report["images_missing_alt"] > 0:
        page_report["issues"].append(f"{page_report['images_missing_alt']} images missing alt attribute (Medium)")
    if page_report["images_missing_dimensions"] > 0:
        page_report["issues"].append(f"{page_report['images_missing_dimensions']} images missing width/height (CLS Risk) (Medium)")

    # AEO Quick Answer
    if not page_report["quick_answer"] and "tools" in file_rel:
        page_report["issues"].append("Tool page missing .quick-answer capsule (High)")
        audit_results["high_issues"].append(f"{file_rel}: Missing .quick-answer")

    audit_results["pages_audit"][file_rel] = page_report

# Output Summary
print("=" * 60)
print(f"AUDIT COMPLETE ACROSS {len(html_files)} PAGES")
print(f"Critical Issues Found: {len(audit_results['critical_issues'])}")
print(f"High Priority Issues Found: {len(audit_results['high_issues'])}")
print("=" * 60)

for crit in audit_results["critical_issues"][:10]:
    print(f"🔴 CRITICAL: {crit}")

for high in audit_results["high_issues"][:15]:
    print(f"🟠 HIGH: {high}")

# Save detailed JSON report
out_json_path = os.path.join(REPO_ROOT, "audit_reports", "master_audit_v2_system_results.json")
with open(out_json_path, "w", encoding="utf-8") as out_f:
    json.dump(audit_results, out_f, indent=2)

print(f"\nDetailed forensic JSON saved to: {out_json_path}")
