import os
import json
import re
import urllib.request
import urllib.error

HOST = "aidigitools.tech"
INDEXNOW_ENDPOINTS = [
    ("IndexNow Central", "https://api.indexnow.org/indexnow"),
    ("Microsoft Bing", "https://www.bing.com/indexnow"),
    ("Yandex", "https://yandex.com/indexnow")
]

SITEMAP_PING_ENDPOINTS = [
    ("Google Sitemap Ping", f"https://www.google.com/ping?sitemap=https://{HOST}/sitemap.xml"),
    ("Bing Sitemap Ping", f"https://www.bing.com/ping?sitemap=https://{HOST}/sitemap.xml")
]

def submit_urls(urls: list[str], key: str | None = None) -> list[dict]:
    api_key = key or os.environ.get("INDEXNOW_KEY", "aidigitools-indexnow-key-2026")
    payload = {
        "host": HOST,
        "key": api_key,
        "keyLocation": f"https://{HOST}/{api_key}.txt",
        "urlList": urls
    }

    data = json.dumps(payload).encode("utf-8")
    results = []

    for name, endpoint in INDEXNOW_ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "AIDigiTools-IndexNow-Ping/2026"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                results.append({
                    "engine": name,
                    "status": resp.status,
                    "message": "Submitted successfully to IndexNow",
                    "urls_count": len(urls)
                })
        except urllib.error.HTTPError as e:
            results.append({"engine": name, "status": e.code, "message": str(e), "urls_count": len(urls)})
        except Exception as e:
            results.append({"engine": name, "status": 0, "message": f"Network notice: {e}", "urls_count": len(urls)})

    return results

def ping_sitemaps() -> list[dict]:
    results = []
    for name, url in SITEMAP_PING_ENDPOINTS:
        req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-Sitemap-Ping/2026"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                results.append({"engine": name, "status": resp.status, "message": "Sitemap ping accepted"})
        except urllib.error.HTTPError as e:
            results.append({"engine": name, "status": e.code, "message": str(e)})
        except Exception as e:
            results.append({"engine": name, "status": 0, "message": f"Notice: {e}"})
    return results

if __name__ == "__main__":
    sitemap_path = os.path.join(os.path.dirname(__file__), "..", "sitemap.xml")
    urls_to_submit = []
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()
            urls_to_submit = re.findall(r"<loc>(https://aidigitools\.tech/[^<]*)</loc>", content)
    
    if not urls_to_submit:
        urls_to_submit = [
            "https://aidigitools.tech/",
            "https://aidigitools.tech/deals.html",
            "https://aidigitools.tech/tools/chatgpt-plus.html",
            "https://aidigitools.tech/tools/claude-pro.html",
            "https://aidigitools.tech/tools/canva-pro.html",
            "https://aidigitools.tech/guides/chatgpt-vs-claude.html"
        ]

    print(f"============================================================")
    print(f"[PING] Pinging Global Search Engines (IndexNow + Sitemaps)")
    print(f"============================================================")
    print(f"Submitting {len(urls_to_submit)} canonical URLs from sitemap.xml...")
    
    indexnow_res = submit_urls(urls_to_submit)
    for r in indexnow_res:
        print(f"[{r['engine']}] Status: {r['status']} - {r['message']} ({r['urls_count']} URLs)")

    sitemap_res = ping_sitemaps()
    for s in sitemap_res:
        print(f"[{s['engine']}] Status: {s['status']} - {s['message']}")
    print(f"============================================================")
