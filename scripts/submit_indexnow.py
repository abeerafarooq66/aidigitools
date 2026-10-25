import os
import json
import urllib.request
import urllib.error

INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
HOST = "aidigitools.tech"

def submit_urls(urls: list[str], key: str | None = None) -> dict:
    api_key = key or os.environ.get("INDEXNOW_KEY", "aidigitools-indexnow-key-2026")
    payload = {
        "host": HOST,
        "key": api_key,
        "keyLocation": f"https://{HOST}/{api_key}.txt",
        "urlList": urls
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {
                "status": resp.status,
                "message": "Submitted successfully to IndexNow",
                "urls_count": len(urls)
            }
    except urllib.error.HTTPError as e:
        return {"status": e.code, "message": str(e), "urls_count": len(urls)}
    except Exception as e:
        return {"status": 0, "message": f"Simulation / Network notice: {e}", "urls_count": len(urls)}

if __name__ == "__main__":
    import re
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
    res = submit_urls(urls_to_submit)
    print(f"[IndexNow] {res['message']} ({res['urls_count']} URLs, status: {res['status']})")
