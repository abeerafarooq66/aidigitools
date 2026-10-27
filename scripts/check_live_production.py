import urllib.request
import ssl
import xml.etree.ElementTree as ET

def check_all_sitemap_urls():
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text for e in root.findall('.//s:loc', ns)]
    
    # Also add non-sitemap essential assets
    extra_assets = [
        "https://aidigitools.tech/assets/style.css",
        "https://aidigitools.tech/assets/cart.js",
        "https://aidigitools.tech/merchant_feed.xml",
        "https://aidigitools.tech/robots.txt",
        "https://aidigitools.tech/BingSiteAuth.xml",
        "https://aidigitools.tech/89d63ab53a63527b12a199a3096e51ad.txt",
        "https://aidigitools.tech/llms.txt",
        "https://aidigitools.tech/llms-full.txt"
    ]
    all_urls = urls + extra_assets
    print(f"Total live URLs to verify: {len(all_urls)} ({len(urls)} canonical sitemap + {len(extra_assets)} core assets)")

    ctx = ssl.create_default_context()
    passed = 0
    failed = 0
    
    for url in all_urls:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AIDigiTools-SitemapLiveCheck/1.0"}
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                status = resp.status
                length = len(resp.read())
                passed += 1
                print(f"[OK 200] {length:6d}B : {url}")
        except Exception as e:
            failed += 1
            print(f"[FAILED] {url} -> {e}")

    print(f"\nFinal Live URL Verification Result: {passed} passed, {failed} failed.")
    return failed == 0

if __name__ == '__main__':
    check_all_sitemap_urls()
