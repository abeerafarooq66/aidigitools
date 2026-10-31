import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT = r"c:\Users\Dell\Desktop\aidigitools"
DATA_DIR = os.path.join(REPO_ROOT, "data")
MASTER_JSON_PATH = os.path.join(DATA_DIR, "products_master.json")
SITEMAP_PATH = os.path.join(REPO_ROOT, "sitemap.xml")
ROBOTS_PATH = os.path.join(REPO_ROOT, "robots.txt")
FEED_PATH = os.path.join(REPO_ROOT, "merchant_feed.xml")
LLMS_PATH = os.path.join(REPO_ROOT, "llms.txt")
STYLE_PATH = os.path.join(REPO_ROOT, "assets", "style.css")
CART_PATH = os.path.join(REPO_ROOT, "assets", "cart.js")

ALL_HTML_FILES = glob.glob(os.path.join(REPO_ROOT, "**", "*.html"), recursive=True)

with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
    MASTER_PRODUCTS = json.load(f)
MASTER_BY_SLUG = {p["slug"]: p for p in MASTER_PRODUCTS}

report = {
    "pages_tested": {
        "total_discovered": len(ALL_HTML_FILES),
        "passed": 0,
        "failed": 0,
        "untested": 0
    },
    "seo_results": {},
    "product_data_results": {},
    "geo_aeo_results": {},
    "ui_ux_results": {},
    "performance_results": {},
    "security_results": {},
    "consistency_results": {},
    "regression_results": {},
    "defects": []
}

def log_defect(task, severity, message, url_or_file=""):
    report["defects"].append({
        "task": task,
        "severity": severity,
        "message": message,
        "location": url_or_file
    })

print("=" * 80)
print("🛡️ AIDigiTools Phase 7 — Master End-to-End QA, Security & Regression Audit")
print("=" * 80)

# ==============================================================================
# TASK 1: COMPLETE PAGE CRAWL & METADATA VALIDATION
# ==============================================================================
print("\n--- [TASK 1] Complete Page Crawl & Metadata Audit ---")
canonical_issues = []
title_issues = []
desc_issues = []
h1_issues = []
viewport_issues = []
structured_data_issues = []

for hf in ALL_HTML_FILES:
    rel_path = os.path.relpath(hf, REPO_ROOT).replace("\\", "/")
    with open(hf, "r", encoding="utf-8") as f:
        html = f.read()

    # Canonical check
    can_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', html)
    if not can_match:
        can_match = re.search(r'<link\s+href=["\']([^"\']+)["\']\s+rel=["\']canonical["\']', html)
    
    if not can_match:
        canonical_issues.append((rel_path, "Missing canonical tag"))
        log_defect("Task 1", "HIGH", "Missing canonical tag", rel_path)
    else:
        can_url = can_match.group(1)
        expected_can = f"https://aidigitools.tech/{rel_path}" if rel_path != "index.html" else "https://aidigitools.tech/"
        if can_url != expected_can:
            canonical_issues.append((rel_path, f"Canonical mismatch: got {can_url}, expected {expected_can}"))
            log_defect("Task 1", "MEDIUM", f"Canonical mismatch: {can_url}", rel_path)

    # Title check (30-65 chars)
    t_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    if not t_match:
        title_issues.append((rel_path, "Missing <title>"))
        log_defect("Task 1", "CRITICAL", "Missing title tag", rel_path)
    else:
        t_len = len(t_match.group(1).strip())
        if t_len < 30 or t_len > 65:
            title_issues.append((rel_path, f"Title length {t_len} outside 30-65 chars"))
            log_defect("Task 1", "MEDIUM", f"Title length {t_len} out of bounds", rel_path)

    # Meta desc check (70-165 chars)
    d_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html)
    if not d_match:
        desc_issues.append((rel_path, "Missing meta description"))
        log_defect("Task 1", "HIGH", "Missing meta description", rel_path)
    else:
        d_len = len(d_match.group(1).strip())
        if d_len < 70 or d_len > 165:
            desc_issues.append((rel_path, f"Meta desc length {d_len} outside 70-165 chars"))
            log_defect("Task 1", "MEDIUM", f"Meta description length {d_len} out of bounds", rel_path)

    # Single H1 check
    h1s = re.findall(r'<h1\b[^>]*>(.*?)</h1>', html, re.DOTALL)
    if len(h1s) != 1:
        h1_issues.append((rel_path, f"Found {len(h1s)} <h1> tags (expected 1)"))
        log_defect("Task 1", "HIGH", f"H1 count {len(h1s)} != 1", rel_path)

    # Viewport check
    if 'name="viewport"' not in html:
        viewport_issues.append(rel_path)
        log_defect("Task 1", "HIGH", "Missing responsive viewport meta tag", rel_path)

    # Structured data check
    schemas = re.findall(r'<script\s+type=["\']application/ld\+json["\']\s*>(.*?)</script>', html, re.DOTALL)
    for s in schemas:
        try:
            json.loads(s)
        except Exception as e:
            structured_data_issues.append((rel_path, str(e)))
            log_defect("Task 1", "HIGH", f"Invalid JSON-LD schema: {e}", rel_path)

print(f"Total HTML pages crawled: {len(ALL_HTML_FILES)}")
print(f"Canonical tag issues: {len(canonical_issues)}")
print(f"Title tag issues: {len(title_issues)}")
print(f"Meta description issues: {len(desc_issues)}")
print(f"H1 hierarchy issues: {len(h1_issues)}")
print(f"Viewport issues: {len(viewport_issues)}")
print(f"JSON-LD parsing issues: {len(structured_data_issues)}")

task1_passed = (len(canonical_issues) == 0 and len(title_issues) == 0 and 
                len(desc_issues) == 0 and len(h1_issues) == 0 and len(structured_data_issues) == 0)
report["seo_results"]["crawl_passed"] = task1_passed

# ==============================================================================
# TASK 2: ALL PRODUCT PAGE VALIDATION (49 TOOLS)
# ==============================================================================
print("\n--- [TASK 2] All Product Page Validation Against Master Dataset ---")
tool_pages = glob.glob(os.path.join(REPO_ROOT, "tools", "*.html"))
product_data_errors = []
held_products_held = 0

HELD_SLUGS = ['netflix-premium', 'linkedin-premium', 'coursera-plus', 'spotify-premium', 'turnitin-student']

for tp in tool_pages:
    slug = os.path.basename(tp).replace(".html", "")
    with open(tp, "r", encoding="utf-8") as f:
        html = f.read()

    master = MASTER_BY_SLUG.get(slug)
    if not master:
        product_data_errors.append((slug, "Slug not in master dataset"))
        log_defect("Task 2", "CRITICAL", "Tool slug missing in products_master.json", slug)
        continue

    # Verify official price & currency
    pkr_price = str(master["aidigitools_price_pkr"])
    if pkr_price not in html:
        product_data_errors.append((slug, f"PKR price {pkr_price} not rendered in tool page"))
        log_defect("Task 2", "HIGH", f"Price mismatch: {pkr_price} PKR not found", slug)

    # Verify official upstream URL or vendor citation
    u1 = master["official_url"].rstrip('/')
    u2 = master["official_pricing_url"].rstrip('/')
    domain = u1.split('//')[-1].split('/')[0].replace('www.', '')
    
    vendor_link_found = (u1 in html) or (u2 in html) or (domain in html)
    if not vendor_link_found:
        product_data_errors.append((slug, f"Official vendor URL or domain ({domain}) not cited"))
        log_defect("Task 2", "MEDIUM", f"Official upstream link missing: {domain}", slug)

    # Verify October 2026 freshness
    if "October 2026" not in html and "2026-10" not in html:
        product_data_errors.append((slug, "Missing October 2026 freshness date"))
        log_defect("Task 2", "MEDIUM", "Freshness timestamp missing", slug)

    # Verify held product protections
    if slug in HELD_SLUGS:
        held_products_held += 1
        has_inquiry_badge = ("Inquiry Only" in html) or ("Orders On Hold" in html) or ("Direct Orders Paused" in html)
        has_direct_order = 'class="btn-quick-order"' in html
        if not has_inquiry_badge or has_direct_order:
            product_data_errors.append((slug, "Held product allows direct order or missing held badge"))
            log_defect("Task 2", "CRITICAL", "Held product ordering violation", slug)

print(f"Tool pages validated: {len(tool_pages)} / 49")
print(f"Held tools properly protected: {held_products_held} / 5")
print(f"Product data discrepancies: {len(product_data_errors)}")
report["product_data_results"]["tool_pages_count"] = len(tool_pages)
report["product_data_results"]["discrepancies"] = len(product_data_errors)

# ==============================================================================
# TASK 3: LINK & BUTTON INTERACTION TESTING
# ==============================================================================
print("\n--- [TASK 3] Interactive Controls, Links & Button Audit ---")
all_links_count = 0
broken_phone_links = []
broken_email_links = []
dead_anchors = []

for hf in ALL_HTML_FILES:
    rel_path = os.path.relpath(hf, REPO_ROOT).replace("\\", "/")
    with open(hf, "r", encoding="utf-8") as f:
        html = f.read()

    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
    all_links_count += len(hrefs)
    for h in hrefs:
        # Check WhatsApp
        if "wa.me" in h or "whatsapp.com" in h:
            if "03326861112" not in h and "923326861112" not in h:
                broken_phone_links.append((rel_path, h))
                log_defect("Task 3", "HIGH", f"Incorrect WhatsApp phone number: {h}", rel_path)
        # Check email
        elif "mailto:" in h:
            if "aidigitools.tech" not in h:
                broken_email_links.append((rel_path, h))
                log_defect("Task 3", "MEDIUM", f"Unrecognized email link domain: {h}", rel_path)
        # Check empty or dead href
        elif h == "" or h == "#":
            dead_anchors.append((rel_path, h))
            log_defect("Task 3", "LOW", f"Empty or dead anchor href='{h}'", rel_path)

print(f"Total links audited: {all_links_count}")
print(f"WhatsApp phone anomalies: {len(broken_phone_links)}")
print(f"Email domain anomalies: {len(broken_email_links)}")
print(f"Dead anchors (href='#' or ''): {len(dead_anchors)}")

report["ui_ux_results"]["total_links_audited"] = all_links_count
report["ui_ux_results"]["broken_whatsapp_links"] = len(broken_phone_links)
report["ui_ux_results"]["dead_anchors"] = len(dead_anchors)

# ==============================================================================
# TASK 4: SEO & STRUCTURED DATA VALIDATION
# ==============================================================================
print("\n--- [TASK 4] Advanced SEO & Schema Markup Validation ---")
with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
    sitemap_xml = f.read()
root_sitemap = ET.fromstring(sitemap_xml)
sitemap_urls = [e.text for e in root_sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]

sitemap_url_errors = []
for u in sitemap_urls:
    if not u.startswith("https://aidigitools.tech/"):
        sitemap_url_errors.append(u)
    if "404.html" in u:
        sitemap_url_errors.append("404.html in sitemap!")

print(f"Sitemap total URLs: {len(sitemap_urls)}")
print(f"Sitemap anomalies: {len(sitemap_url_errors)}")

breadcrumb_count = 0
faq_schema_count = 0
for tp in tool_pages:
    with open(tp, "r", encoding="utf-8") as f:
        c = f.read()
    if '"@type": "BreadcrumbList"' in c:
        breadcrumb_count += 1
    if '"@type": "FAQPage"' in c:
        faq_schema_count += 1

print(f"Tool pages with BreadcrumbList schema: {breadcrumb_count} / 49")
print(f"Tool pages with FAQPage schema: {faq_schema_count} / 49")
report["seo_results"]["sitemap_url_count"] = len(sitemap_urls)
report["seo_results"]["breadcrumb_schemas"] = breadcrumb_count
report["seo_results"]["faq_schemas"] = faq_schema_count

# ==============================================================================
# TASK 5: PERFORMANCE & ACCESSIBILITY AUDIT
# ==============================================================================
print("\n--- [TASK 5] Performance, Assets & Accessibility ---")
css_size_kb = os.path.getsize(STYLE_PATH) / 1024
js_size_kb = os.path.getsize(CART_PATH) / 1024
print(f"assets/style.css size: {css_size_kb:.2f} KB")
print(f"assets/cart.js size: {js_size_kb:.2f} KB (budget: < 100 KB)")

skip_link_count = sum(1 for f in ALL_HTML_FILES if 'class="skip-link"' in open(f, encoding="utf-8").read())
main_id_count = sum(1 for f in ALL_HTML_FILES if 'id="main"' in open(f, encoding="utf-8").read())
table_responsive_wrappers = sum(1 for f in ALL_HTML_FILES if 'class="table-responsive"' in open(f, encoding="utf-8").read())

print(f"Pages with accessible Skip Link: {skip_link_count} / {len(ALL_HTML_FILES)}")
print(f"Pages with <main id='main'>: {main_id_count} / {len(ALL_HTML_FILES)}")
print(f"Pages containing .table-responsive wrappers: {table_responsive_wrappers}")

report["performance_results"]["css_size_kb"] = round(css_size_kb, 2)
report["performance_results"]["js_size_kb"] = round(js_size_kb, 2)
report["ui_ux_results"]["skip_links_count"] = skip_link_count
report["ui_ux_results"]["main_id_count"] = main_id_count

# ==============================================================================
# TASK 6: SECURITY & CREDENTIAL AUDIT
# ==============================================================================
print("\n--- [TASK 6] Security Review & Credential Scanning ---")
secret_patterns = [
    (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
    (r'ghp_[a-zA-Z0-9]{20,}', "GitHub Token"),
    (r'AKIA[0-9A-Z]{16}', "AWS Access Key"),
    (r'(?:cost_usdt|wholesale_price)\s*[:=]\s*["\']?[0-9.]+', "Private Wholesale Cost"),
    (r'password\s*[:=]\s*["\'][^"\']+["\']', "Hardcoded Password")
]

security_violations = []
for hf in ALL_HTML_FILES + [STYLE_PATH, CART_PATH]:
    with open(hf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    for pat, desc in secret_patterns:
        m = re.findall(pat, content)
        if m:
            rel = os.path.relpath(hf, REPO_ROOT)
            security_violations.append((rel, desc, m))
            log_defect("Task 6", "CRITICAL", f"Potential exposed credential: {desc}", rel)

print(f"Security / Secret violations found: {len(security_violations)}")
report["security_results"]["violations_count"] = len(security_violations)

# ==============================================================================
# TASK 7: MULTI-SURFACE CONSISTENCY AUDIT
# ==============================================================================
print("\n--- [TASK 7] Cross-System Parity & Consistency Audit ---")
with open(LLMS_PATH, "r", encoding="utf-8") as f:
    llms_text = f.read()
llms_tool_matches = sum(1 for slug in MASTER_BY_SLUG if slug in llms_text)
print(f"Tools referenced in llms.txt: {llms_tool_matches} / 49")

tree_feed = ET.parse(FEED_PATH)
feed_root = tree_feed.getroot()
feed_items = feed_root.find("channel").findall("item")
feed_slugs = [item.find("{http://base.google.com/ns/1.0}id").text.replace("aidigitools-", "") for item in feed_items]
feed_parity = len(set(feed_slugs).intersection(set(MASTER_BY_SLUG.keys())))
print(f"Merchant feed tools in master: {feed_parity} / 49")

with open(os.path.join(REPO_ROOT, "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()
index_tool_cards = len(re.findall(r'data-tool=["\']([^"\']+)["\']', index_html))
print(f"Homepage tool cards: {index_tool_cards} / 49")

consistency_passed = (llms_tool_matches == 49 and feed_parity == 49 and index_tool_cards == 49)
report["consistency_results"]["llms_parity"] = llms_tool_matches
report["consistency_results"]["merchant_feed_parity"] = feed_parity
report["consistency_results"]["homepage_cards"] = index_tool_cards
report["consistency_results"]["passed"] = consistency_passed

# ==============================================================================
# SUMMARY & FINAL VERDICT
# ==============================================================================
print("\n" + "=" * 80)
total_defects = len(report["defects"])
critical_defects = sum(1 for d in report["defects"] if d["severity"] == "CRITICAL")
high_defects = sum(1 for d in report["defects"] if d["severity"] == "HIGH")
medium_defects = sum(1 for d in report["defects"] if d["severity"] == "MEDIUM")
low_defects = sum(1 for d in report["defects"] if d["severity"] == "LOW")

print(f"TOTAL DEFECTS FOUND: {total_defects}")
print(f"  CRITICAL : {critical_defects}")
print(f"  HIGH     : {high_defects}")
print(f"  MEDIUM   : {medium_defects}")
print(f"  LOW      : {low_defects}")
print("=" * 80)

report["pages_tested"]["passed"] = len(ALL_HTML_FILES) if total_defects == 0 else len(ALL_HTML_FILES) - total_defects

with open(os.path.join(DATA_DIR, "phase7_master_qa_report.json"), "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

if critical_defects > 0 or high_defects > 0:
    print("❌ PHASE 7 GATE BLOCKED: Critical or High defects detected!")
    sys.exit(1)
else:
    print("✅ PHASE 7 MASTER GATE PASSED: Zero Critical or High defects! Ready for Release.")
    sys.exit(0)
