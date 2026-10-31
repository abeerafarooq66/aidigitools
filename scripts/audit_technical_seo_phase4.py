import os
import re
import glob
import json
import xml.etree.ElementTree as ET

def audit_technical_seo():
    html_files = [f.replace('\\\\', '/').replace('\\', '/') for f in glob.glob('*.html') + glob.glob('*/*.html')]
    print(f"Auditing {len(html_files)} HTML pages for Technical SEO...")

    report = {
        "summary": {
            "total_pages": len(html_files),
            "canonical_errors": [],
            "robots_errors": [],
            "h1_errors": [],
            "heading_hierarchy_errors": [],
            "title_errors": [],
            "meta_desc_errors": [],
            "og_errors": [],
            "twitter_errors": [],
            "image_errors": [],
            "schema_errors": [],
            "internal_link_anomalies": [],
            "broken_links": []
        },
        "pages": {}
    }

    # Canonical rules
    for path in sorted(html_files):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        page_issues = []

        # 1. Canonical check
        canonical_match = re.search(r'<link\s+rel=[\'"]canonical[\'"]\s+href=[\'"](.*?)[\'"]', content, re.IGNORECASE)
        if not canonical_match:
            # try reverse order href then rel
            canonical_match = re.search(r'<link\s+href=[\'"](.*?)[\'"]\s+rel=[\'"]canonical[\'"]', content, re.IGNORECASE)

        if not canonical_match:
            err = f"Missing canonical tag in {path}"
            report["summary"]["canonical_errors"].append(err)
            page_issues.append(err)
        else:
            canonical = canonical_match.group(1)
            expected_canonical = "https://aidigitools.tech/" if path == "index.html" else f"https://aidigitools.tech/{path}"
            if canonical != expected_canonical:
                err = f"Canonical mismatch in {path}: found '{canonical}', expected '{expected_canonical}'"
                report["summary"]["canonical_errors"].append(err)
                page_issues.append(err)

        # 2. Robots meta check
        robots_match = re.search(r'<meta\s+name=[\'"]robots[\'"]\s+content=[\'"](.*?)[\'"]', content, re.IGNORECASE)
        if not robots_match:
            robots_match = re.search(r'<meta\s+content=[\'"](.*?)[\'"]\s+name=[\'"]robots[\'"]', content, re.IGNORECASE)

        if path == "404.html":
            if not robots_match or "noindex" not in robots_match.group(1).lower():
                err = f"404.html missing noindex robots tag: found '{robots_match.group(1) if robots_match else 'None'}'"
                report["summary"]["robots_errors"].append(err)
                page_issues.append(err)
        else:
            if not robots_match or "index" not in robots_match.group(1).lower() or "noindex" in robots_match.group(1).lower():
                err = f"{path} has invalid robots tag: found '{robots_match.group(1) if robots_match else 'None'}'"
                report["summary"]["robots_errors"].append(err)
                page_issues.append(err)

        # 3. H1 check
        h1_matches = re.findall(r'<h1\b[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        if len(h1_matches) == 0:
            err = f"Missing <h1> tag in {path}"
            report["summary"]["h1_errors"].append(err)
            page_issues.append(err)
        elif len(h1_matches) > 1:
            err = f"Multiple <h1> tags ({len(h1_matches)}) in {path}"
            report["summary"]["h1_errors"].append(err)
            page_issues.append(err)
        else:
            h1_text = re.sub(r'<[^>]+>', '', h1_matches[0]).strip()
            if not h1_text:
                err = f"Empty <h1> in {path}"
                report["summary"]["h1_errors"].append(err)
                page_issues.append(err)

        # 4. Heading hierarchy check
        headings = re.findall(r'<(h[1-6])\b[^>]*>(.*?)</\1>', content, re.IGNORECASE | re.DOTALL)
        last_level = 0
        for tag, text in headings:
            level = int(tag[1])
            if last_level != 0 and level > last_level + 1:
                # e.g. h1 to h3 without h2, or h2 to h4
                clean_text = re.sub(r'<[^>]+>', '', text).strip()[:30]
                err = f"Skipped heading level in {path}: <{tag}> '{clean_text}' followed <h{last_level}>"
                report["summary"]["heading_hierarchy_errors"].append(err)
                page_issues.append(err)
            last_level = level

        # 5. Title & Meta Description checks
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        if not title_match or not title_match.group(1).strip():
            err = f"Missing or empty <title> in {path}"
            report["summary"]["title_errors"].append(err)
            page_issues.append(err)
        else:
            t_len = len(title_match.group(1).strip())
            if t_len < 30 or t_len > 65:
                err = f"Title length out of bounds ({t_len} chars) in {path}: '{title_match.group(1).strip()}'"
                report["summary"]["title_errors"].append(err)
                page_issues.append(err)

        desc_match = re.search(r'<meta\s+name=[\'"]description[\'"]\s+content=[\'"](.*?)[\'"]', content, re.IGNORECASE)
        if not desc_match or not desc_match.group(1).strip():
            err = f"Missing or empty meta description in {path}"
            report["summary"]["meta_desc_errors"].append(err)
            page_issues.append(err)
        else:
            d_len = len(desc_match.group(1).strip())
            if d_len < 70 or d_len > 165:
                err = f"Meta description length out of bounds ({d_len} chars) in {path}"
                report["summary"]["meta_desc_errors"].append(err)
                page_issues.append(err)

        # 6. Open Graph & Twitter Card checks
        og_required = ['og:title', 'og:description', 'og:url', 'og:image', 'og:type']
        for og_prop in og_required:
            if not re.search(rf'<meta\s+property=[\'"]{re.escape(og_prop)}[\'"]', content, re.IGNORECASE):
                err = f"Missing {og_prop} in {path}"
                report["summary"]["og_errors"].append(err)
                page_issues.append(err)

        tw_required = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']
        for tw_prop in tw_required:
            if not re.search(rf'<meta\s+name=[\'"]{re.escape(tw_prop)}[\'"]', content, re.IGNORECASE):
                err = f"Missing {tw_prop} in {path}"
                report["summary"]["twitter_errors"].append(err)
                page_issues.append(err)

        # 7. Image optimization checks (alt, width, height, loading)
        img_tags = re.findall(r'<img\b[^>]*>', content, re.IGNORECASE)
        for img in img_tags:
            # Check alt
            alt_m = re.search(r'alt=[\'"](.*?)[\'"]', img, re.IGNORECASE)
            if not alt_m or not alt_m.group(1).strip():
                err = f"Image missing non-empty alt text in {path}: {img[:60]}..."
                report["summary"]["image_errors"].append(err)
                page_issues.append(err)
            # Check width and height
            w_m = re.search(r'width=[\'"]\d+[\'"]', img, re.IGNORECASE)
            h_m = re.search(r'height=[\'"]\d+[\'"]', img, re.IGNORECASE)
            if not w_m or not h_m:
                err = f"Image missing explicit width/height in {path}: {img[:60]}..."
                report["summary"]["image_errors"].append(err)
                page_issues.append(err)

        # 8. Schema JSON-LD validation
        json_lds = re.findall(r'<script\s+type=[\'"]application/ld\+json[\'"]>(.*?)</script>', content, re.DOTALL)
        for jstr in json_lds:
            try:
                data = json.loads(jstr.strip())
                # Check for fake ratings
                if isinstance(data, dict):
                    if 'aggregateRating' in data:
                        err = f"Found aggregateRating schema in {path} (violates Google unverified review policy)"
                        report["summary"]["schema_errors"].append(err)
                        page_issues.append(err)
                    if 'review' in data and not isinstance(data.get('review'), list):
                        err = f"Found review schema in {path}"
                        report["summary"]["schema_errors"].append(err)
                        page_issues.append(err)
            except Exception as e:
                err = f"Invalid JSON-LD syntax in {path}: {str(e)}"
                report["summary"]["schema_errors"].append(err)
                page_issues.append(err)

        # 9. Internal link checking
        links = re.findall(r'href=[\'"](.*?)[\'"]', content, re.IGNORECASE)
        for link in links:
            if link.startswith('http://aidigitools.tech'):
                err = f"Insecure HTTP internal link in {path}: {link}"
                report["summary"]["internal_link_anomalies"].append(err)
                page_issues.append(err)
            if 'www.aidigitools.tech' in link:
                err = f"Non-canonical www link in {path}: {link}"
                report["summary"]["internal_link_anomalies"].append(err)
                page_issues.append(err)
            if link == 'index.html' or link.startswith('index.html#'):
                # Valid relative root anchor or link
                pass

        report["pages"][path] = {
            "status": "PASS" if len(page_issues) == 0 else "FAIL",
            "issues": page_issues
        }

    # Print summary
    print("\n================ TECHNICAL SEO AUDIT RESULTS ================")
    total_issues = sum(len(v) for k, v in report["summary"].items() if isinstance(v, list))
    for category, errs in report["summary"].items():
        if isinstance(errs, list):
            print(f"[{category}]: {len(errs)} issues")
            for e in errs[:3]:
                print(f"   -> {e}")
            if len(errs) > 3:
                print(f"   ... and {len(errs) - 3} more")

    print(f"\nTOTAL TECHNICAL ISSUES FOUND: {total_issues}")
    print("=============================================================")

    with open('data/phase4_technical_seo_audit.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print("Full report saved to data/phase4_technical_seo_audit.json")
    return total_issues

if __name__ == '__main__':
    audit_technical_seo()

