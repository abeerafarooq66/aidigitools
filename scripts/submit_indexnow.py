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
    sample_urls = [
        "https://aidigitools.tech/",
        "https://aidigitools.tech/tools/chatgpt-plus.html",
        "https://aidigitools.tech/tools/claude-pro.html",
        "https://aidigitools.tech/tools/canva-pro.html",
        "https://aidigitools.tech/guides/chatgpt-vs-claude.html"
    ]
    res = submit_urls(sample_urls)
    print(f"[IndexNow] {res['message']} ({res['urls_count']} URLs, status: {res['status']})")
