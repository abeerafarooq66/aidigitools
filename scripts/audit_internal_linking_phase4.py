import os
import glob
import re
import json

def audit_internal_linking():
    html_files = sorted(glob.glob('*.html') + glob.glob('*/*.html'))
    html_files = [f.replace('\\\\', '/').replace('\\', '/') for f in html_files]

    domain = "https://aidigitools.tech"
    pages_set = set(html_files)

    inbound_links = {p: set() for p in html_files}
    outbound_links = {p: set() for p in html_files}
    empty_anchors = []
    generic_anchors = []
    breadcrumb_audit = {}

    generic_terms = {'click here', 'here', 'read more', 'link', 'more', 'click', 'learn more'}

    for path in html_files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all anchors
        anchors = re.findall(r'<a\b([^>]*)>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
        for attrs, body in anchors:
            clean_body = re.sub(r'<[^>]+>', '', body).strip().lower()
            href_m = re.search(r'href=[\'"](.*?)[\'"]', attrs, re.IGNORECASE)
            if not href_m:
                continue
            href = href_m.group(1).strip()

            # Check empty anchor (unless it contains an image or svg)
            has_media = bool(re.search(r'<(img|svg)\b', body, re.IGNORECASE))
            if not clean_body and not has_media:
                empty_anchors.append({"file": path, "href": href, "raw": body[:50]})

            # Check generic anchor text
            if clean_body in generic_terms:
                generic_anchors.append({"file": path, "href": href, "anchor": clean_body})

            # Resolve internal link destination
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:'):
                continue
            if href.startswith('https://wa.me') or href.startswith('http://') or (href.startswith('https://') and not href.startswith(domain)):
                continue

            target_clean = href.replace(domain + '/', '').replace(domain, '')
            target_clean = target_clean.split('#')[0].split('?')[0]

            if not target_clean:
                target_file = 'index.html'
            else:
                # Handle relative path
                if target_clean.startswith('/'):
                    target_file = target_clean.lstrip('/')
                elif '/' in path:
                    parent = os.path.dirname(path)
                    target_file = os.path.normpath(os.path.join(parent, target_clean)).replace('\\', '/')
                else:
                    target_file = target_clean

            if target_file in pages_set:
                inbound_links[target_file].add(path)
                outbound_links[path].add(target_file)

        # Check breadcrumbs on subpages
        if path != 'index.html' and path != '404.html':
            bc_match = re.search(r'<nav\b[^>]*class=[\'"][^\'"]*breadcrumb[^\'"]*[\'"][^>]*>(.*?)</nav>', content, re.IGNORECASE | re.DOTALL)
            breadcrumb_audit[path] = bool(bc_match)

    # Check for orphan pages (excluding index.html)
    orphans = [p for p, in_l in inbound_links.items() if len(in_l) == 0 and p != 'index.html']

    # Compute crawl depth from index.html (BFS)
    depth = {'index.html': 0}
    queue = ['index.html']
    while queue:
        curr = queue.pop(0)
        curr_depth = depth[curr]
        for neighbor in outbound_links[curr]:
            if neighbor not in depth:
                depth[neighbor] = curr_depth + 1
                queue.append(neighbor)

    unreachable = [p for p in html_files if p not in depth]
    max_depth = max(depth.values()) if depth else 0
    high_depth = {p: d for p, d in depth.items() if d > 2}

    print("\n================ INTERNAL LINKING GRAPH AUDIT ================")
    print(f"Total HTML Documents: {len(html_files)}")
    print(f"Orphan Pages: {len(orphans)} {orphans}")
    print(f"Unreachable from Homepage: {len(unreachable)} {unreachable}")
    print(f"Max Crawl Depth from Homepage: {max_depth}")
    print(f"Pages with Crawl Depth > 2: {len(high_depth)}")
    print(f"Empty Anchors: {len(empty_anchors)}")
    print(f"Generic Anchor Text: {len(generic_anchors)}")
    
    missing_bc = [p for p, has_bc in breadcrumb_audit.items() if not has_bc]
    print(f"Pages Missing Semantic Breadcrumb Navigation: {len(missing_bc)}")
    if missing_bc:
        print(f"   -> Sample: {missing_bc[:5]}")

    tool_inbound_counts = {p: len(inbound_links[p]) for p in html_files if p.startswith('tools/')}
    min_tool_inbound = min(tool_inbound_counts.values()) if tool_inbound_counts else 0
    avg_tool_inbound = sum(tool_inbound_counts.values()) / len(tool_inbound_counts) if tool_inbound_counts else 0
    print(f"\nTool Pages Inbound Link Distribution (49 tools):")
    print(f"  Min inbound links per tool: {min_tool_inbound}")
    print(f"  Average inbound links per tool: {avg_tool_inbound:.1f}")

    results = {
        "orphans": orphans,
        "unreachable": unreachable,
        "max_crawl_depth": max_depth,
        "empty_anchors": empty_anchors,
        "generic_anchors": generic_anchors,
        "missing_breadcrumbs": missing_bc,
        "tool_inbound_counts": tool_inbound_counts
    }

    with open('data/phase4_internal_linking_audit.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print("Full report saved to data/phase4_internal_linking_audit.json")
    print("=============================================================")
    return len(orphans) + len(unreachable) + len(empty_anchors) + len(generic_anchors)

if __name__ == '__main__':
    audit_internal_linking()

