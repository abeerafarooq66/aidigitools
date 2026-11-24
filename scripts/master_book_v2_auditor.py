#!/usr/bin/env python3
"""
AIDigiTools Master Audit Engine V2
Compliant with: Universal Web Search & SEO Master Book V2 (Nov 2026 Edition)
Audits: Traditional SEO, AEO, GEO, AIO, LLMO, E-E-A-T, Schema Graph, and Telemetry
"""

import os
import re
import json
import glob
from collections import defaultdict

def run_master_audit():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tools_dir = os.path.join(root_dir, 'tools')
    guides_dir = os.path.join(root_dir, 'guides')
    blog_dir = os.path.join(root_dir, 'blog')
    categories_dir = os.path.join(root_dir, 'categories')
    compare_dir = os.path.join(root_dir, 'compare')
    best_dir = os.path.join(root_dir, 'best')
    
    html_files = glob.glob(os.path.join(root_dir, '**', '*.html'), recursive=True)
    # Exclude admin or temporary dirs
    html_files = [f for f in html_files if 'admin' not in f and '.git' not in f]

    print(f"================================================================================")
    print(f"   AIDIGITOOLS FORENSIC DEEP AUDIT ENGINE (MASTER BOOK V2 BENCHMARK)           ")
    print(f"================================================================================")
    print(f"Total HTML Pages Scanned: {len(html_files)}")
    print(f"Base Directory: {root_dir}\n")

    scorecard = {
        "crawlability": {"passed": 0, "failed": 0, "issues": []},
        "canonical": {"passed": 0, "failed": 0, "issues": []},
        "schema": {"passed": 0, "failed": 0, "issues": []},
        "dom_headings": {"passed": 0, "failed": 0, "issues": []},
        "cannibalization": {"passed": 0, "failed": 0, "issues": []},
        "aeo_geo": {"passed": 0, "failed": 0, "issues": []},
        "eeat": {"passed": 0, "failed": 0, "issues": []}
    }

    restricted_slugs = ['turnitin-student', 'linkedin-premium', 'netflix-premium', 'spotify-premium', 'coursera-plus', 'claude-artifacts', 'deepseek-pro']
    keyword_tracker = defaultdict(list)

    # 1. Robots.txt Governance
    robots_path = os.path.join(root_dir, 'robots.txt')
    if os.path.exists(robots_path):
        with open(robots_path, 'r', encoding='utf-8') as rf:
            robots_content = rf.read()
        required_bots = ['OAI-SearchBot', 'Claude-SearchBot', 'PerplexityBot', 'Applebot', 'Googlebot', 'Bingbot']
        for bot in required_bots:
            if bot in robots_content:
                scorecard["crawlability"]["passed"] += 1
            else:
                scorecard["crawlability"]["failed"] += 1
                scorecard["crawlability"]["issues"].append(f"Missing required crawler in robots.txt: {bot}")
    else:
        scorecard["crawlability"]["failed"] += 1
        scorecard["crawlability"]["issues"].append("robots.txt not found!")

    # 2. Page by Page Deep Audit
    for file_path in sorted(html_files):
        rel_path = os.path.relpath(file_path, root_dir).replace('\\', '/')
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # A. Canonical Tag
        canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        if canonical_match:
            c_url = canonical_match.group(1)
            if c_url.startswith("https://aidigitools.tech"):
                scorecard["canonical"]["passed"] += 1
            else:
                scorecard["canonical"]["failed"] += 1
                scorecard["canonical"]["issues"].append(f"{rel_path}: Invalid canonical origin: {c_url}")
        else:
            scorecard["canonical"]["failed"] += 1
            scorecard["canonical"]["issues"].append(f"{rel_path}: Missing canonical link tag")

        # B. Heading Hierarchy (H1 count)
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if len(h1_matches) == 1:
            scorecard["dom_headings"]["passed"] += 1
        else:
            scorecard["dom_headings"]["failed"] += 1
            scorecard["dom_headings"]["issues"].append(f"{rel_path}: Expected 1 H1, found {len(h1_matches)}")

        # C. Schema / Structured Data
        ld_json_matches = re.findall(r'<script\s+type=["\']application/ld\+json["\']>([\s\S]*?)</script>', content, re.IGNORECASE)
        if not ld_json_matches:
            scorecard["schema"]["failed"] += 1
            scorecard["schema"]["issues"].append(f"{rel_path}: Missing JSON-LD structured data")
        else:
            is_valid_json = True
            for script_str in ld_json_matches:
                try:
                    data = json.loads(script_str)
                    # Check Product Schema Availability
                    if rel_path.startswith('tools/'):
                        slug = os.path.basename(rel_path).replace('.html', '')
                        if data.get('@type') == 'Product' or ('@graph' in data and any(item.get('@type') == 'Product' for item in data['@graph'])):
                            # Find offers
                            product_item = data if data.get('@type') == 'Product' else next(item for item in data['@graph'] if item.get('@type') == 'Product')
                            offers = product_item.get('offers', {})
                            avail = offers.get('availability', '')
                            if slug in restricted_slugs:
                                if 'OutOfStock' in avail:
                                    scorecard["schema"]["passed"] += 1
                                else:
                                    scorecard["schema"]["failed"] += 1
                                    scorecard["schema"]["issues"].append(f"{rel_path}: Restricted product must be OutOfStock, found {avail}")
                            else:
                                if 'InStock' in avail:
                                    scorecard["schema"]["passed"] += 1
                                else:
                                    scorecard["schema"]["failed"] += 1
                                    scorecard["schema"]["issues"].append(f"{rel_path}: Active commercial product must be InStock, found {avail}")
                except Exception as e:
                    is_valid_json = False
                    scorecard["schema"]["failed"] += 1
                    scorecard["schema"]["issues"].append(f"{rel_path}: Malformed JSON-LD: {e}")

        # D. Cannibalization Keywords Tracker
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title_text = title_match.group(1).lower() if title_match else ""
        meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', content, re.IGNORECASE)
        desc_text = meta_desc.group(1).lower() if meta_desc else ""
        
        target_queries = ["sadapay", "nayapay", "jazzcash", "easypaisa"]
        for tq in target_queries:
            if tq in title_text or tq in desc_text:
                keyword_tracker[tq].append(rel_path)

        # E. AEO / GEO Quick Answer Capsule
        qa_match = re.search(r'class=["\'][^"\']*quick-answer[^"\']*["\'][^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        if qa_match:
            qa_text = re.sub(r'<[^>]+>', '', qa_match.group(1)).strip()
            word_count = len(qa_text.split())
            # Princeton benchmark: Check for empirical statistics/numbers
            has_numbers = bool(re.search(r'\d+', qa_text))
            has_currency = bool(re.search(r'rs\.|pkr|\$|usd', qa_text, re.IGNORECASE))
            if 30 <= word_count <= 110 and has_numbers and has_currency:
                scorecard["aeo_geo"]["passed"] += 1
            else:
                scorecard["aeo_geo"]["failed"] += 1
                scorecard["aeo_geo"]["issues"].append(f"{rel_path}: Quick answer non-optimal (words: {word_count}, stats: {has_numbers})")
        else:
            if rel_path.startswith(('tools/', 'guides/', 'blog/', 'compare/')):
                scorecard["aeo_geo"]["failed"] += 1
                scorecard["aeo_geo"]["issues"].append(f"{rel_path}: Missing .quick-answer capsule")

        # F. E-E-A-T Footprint
        if rel_path.startswith(('blog/', 'guides/')):
            has_author = bool(re.search(r'abeera\s+farooq|editorial\s+team', content, re.IGNORECASE))
            has_date = bool(re.search(r'2026', content))
            if has_author and has_date:
                scorecard["eeat"]["passed"] += 1
            else:
                scorecard["eeat"]["failed"] += 1
                scorecard["eeat"]["issues"].append(f"{rel_path}: Missing explicit author or freshness timestamp")

    # Cannibalization Evaluation
    for kw, pages in keyword_tracker.items():
        if len(pages) > 2:
            scorecard["cannibalization"]["failed"] += 1
            scorecard["cannibalization"]["issues"].append(f"Keyword '{kw}' is targeted by {len(pages)} pages: {', '.join(pages[:4])}...")
        else:
            scorecard["cannibalization"]["passed"] += 1

    # Report Output
    print("--------------------------------------------------------------------------------")
    print("                    MASTER BOOK V2 COMPLIANCE RESULTS                           ")
    print("--------------------------------------------------------------------------------")
    for category, res in scorecard.items():
        total = res["passed"] + res["failed"]
        pct = (res["passed"] / total * 100) if total > 0 else 0
        status_icon = "🟢" if pct >= 90 else ("🟡" if pct >= 70 else "🔴")
        print(f"{status_icon} {category.upper():<16} : {pct:>5.1f}% Passed ({res['passed']}/{total})")
        if res["issues"]:
            for issue in res["issues"][:3]:
                print(f"    - {issue}")
            if len(res["issues"]) > 3:
                print(f"    - ... and {len(res['issues']) - 3} more issues")

    print("\n================================================================================")
    print("AUDIT SUMMARY COMPLETE. SAVING TO AUDIT_REPORT_MASTER_V2.json")
    print("================================================================================")

    output_path = os.path.join(root_dir, 'audit_reports', 'AUDIT_REPORT_MASTER_V2.json')
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(scorecard, out_f, indent=2)

if __name__ == '__main__':
    run_master_audit()
