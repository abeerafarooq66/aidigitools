import os
import glob
import re
import json

def audit_performance_assets():
    print("=== AIDigiTools Web Performance & Asset Payload Audit ===")

    # 1. Inspect CSS & JS
    css_files = glob.glob('assets/**/*.css', recursive=True)
    js_files = glob.glob('assets/**/*.js', recursive=True)
    img_files = glob.glob('assets/images/**/*', recursive=True)

    asset_stats = {}
    for f in css_files + js_files:
        f_norm = f.replace('\\', '/')
        size_kb = os.path.getsize(f) / 1024.0
        asset_stats[f_norm] = f"{size_kb:.2f} KB"

    print("\nCore Script & Stylesheet Payload:")
    for k, v in asset_stats.items():
        print(f"  {k}: {v}")

    # 2. Inspect Image Assets
    img_stats = []
    for f in img_files:
        if os.path.isfile(f):
            size_kb = os.path.getsize(f) / 1024.0
            f_norm = f.replace('\\', '/')
            img_stats.append((f_norm, size_kb))

    img_stats.sort(key=lambda x: x[1], reverse=True)
    print(f"\nTotal image assets: {len(img_stats)}")
    print("Top 5 largest images:")
    for path, sz in img_stats[:5]:
        print(f"  {path}: {sz:.2f} KB")

    # 3. HTML Page Weight Analysis
    html_files = glob.glob('*.html') + glob.glob('*/*.html')
    html_sizes = []
    for h in html_files:
        h_norm = h.replace('\\', '/')
        sz_kb = os.path.getsize(h) / 1024.0
        html_sizes.append((h_norm, sz_kb))

    html_sizes.sort(key=lambda x: x[1], reverse=True)
    avg_html_kb = sum(x[1] for x in html_sizes) / len(html_sizes)
    print(f"\nHTML Documents (66 files):")
    print(f"  Average HTML page size: {avg_html_kb:.2f} KB")
    print(f"  Largest page: {html_sizes[0][0]} ({html_sizes[0][1]:.2f} KB)")
    print(f"  Smallest page: {html_sizes[-1][0]} ({html_sizes[-1][1]:.2f} KB)")

    # 4. Image Attribute Audit (Lazy loading, decoding async, dimensions)
    missing_lazy = []
    missing_async = []
    missing_dimensions = []

    for h in html_files:
        h_norm = h.replace('\\', '/')
        with open(h, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        imgs = re.findall(r'<img\b[^>]*>', content, re.IGNORECASE)
        for img in imgs:
            # Below the fold check (e.g. not logo)
            is_logo = 'logo' in img.lower()
            if not is_logo:
                if 'loading=' not in img.lower():
                    missing_lazy.append((h_norm, img[:50]))
                if 'decoding=' not in img.lower():
                    missing_async.append((h_norm, img[:50]))
            if 'width=' not in img.lower() or 'height=' not in img.lower():
                missing_dimensions.append((h_norm, img[:50]))

    print(f"\nImage Performance Invariants:")
    print(f"  Images missing loading attribute: {len(missing_lazy)}")
    print(f"  Images missing decoding attribute: {len(missing_async)}")
    print(f"  Images missing explicit width/height: {len(missing_dimensions)}")

    # 5. Font and Third-Party Resource Check
    external_fonts = []
    third_party_scripts = []
    for h in html_files:
        h_norm = h.replace('\\', '/')
        with open(h, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        if 'fonts.googleapis.com' in content or 'fonts.gstatic.com' in content:
            external_fonts.append(h_norm)
        
        scripts = re.findall(r'<script\b[^>]*src=[\'"](.*?)[\'"]', content, re.IGNORECASE)
        for s in scripts:
            if s.startswith('http') and not 'aidigitools.tech' in s:
                third_party_scripts.append((h_norm, s))

    print(f"\nExternal Resource Dependencies:")
    print(f"  Pages with external Google Fonts: {len(external_fonts)} (0 expected - system font stack used)")
    print(f"  External third-party scripts: {len(third_party_scripts)} (0 expected - self-contained vanilla JS)")

    results = {
        "core_assets": asset_stats,
        "total_images": len(img_stats),
        "avg_html_kb": avg_html_kb,
        "missing_lazy_images": len(missing_lazy),
        "missing_dimensions": len(missing_dimensions),
        "external_fonts": len(external_fonts),
        "third_party_scripts": len(third_party_scripts)
    }

    with open('data/phase4_performance_audit.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print("\nFull performance audit saved to data/phase4_performance_audit.json")

if __name__ == '__main__':
    audit_performance_assets()

