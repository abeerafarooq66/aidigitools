import os
import sys
import json
import re
import argparse
import urllib.request
import urllib.error

HOST = "aidigitools.tech"
HEX_KEY = "89d63ab53a63527b12a199a3096e51ad"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

INDEXNOW_ENDPOINTS = [
    ("IndexNow Central", "https://api.indexnow.org/indexnow"),
    ("Microsoft Bing", "https://www.bing.com/indexnow"),
    ("Yandex", "https://yandex.com/indexnow")
]

def validate_key_file(key: str) -> bool:
    """Validates that {key}.txt exists at the root and contains exactly the key."""
    key_file_path = os.path.join(ROOT_DIR, f"{key}.txt")
    if not os.path.exists(key_file_path):
        print(f"[ERROR] IndexNow key verification file missing: {key_file_path}")
        return False
    with open(key_file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    if content != key:
        print(f"[ERROR] Key file content mismatch: expected '{key}', found '{content}'")
        return False
    return True

def get_canonical_urls() -> list[str]:
    """Retrieves all legitimate canonical URLs from sitemap.xml."""
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    if not os.path.exists(sitemap_path):
        return []
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    urls = re.findall(r"<loc>(https://aidigitools\.tech/[^<]*)</loc>", content)
    return sorted(list(set(urls)))

def submit_indexnow(urls: list[str], key: str = HEX_KEY, dry_run: bool = False) -> list[dict]:
    """Submits legitimate canonical URLs to participating IndexNow search engines."""
    # Guardrail 1: Validate key file
    if not validate_key_file(key):
        raise ValueError("IndexNow key verification file validation failed.")

    # Guardrail 2: Filter and sanitize URLs (must belong to aidigitools.tech)
    valid_urls = [u.strip() for u in urls if u.startswith(f"https://{HOST}/")]
    if not valid_urls:
        print("[WARNING] No valid URLs to submit.")
        return []

    # Guardrail 3: Limit submissions to reasonable batch size (IndexNow max is 10,000)
    if len(valid_urls) > 1000:
        print(f"[WARNING] Truncating batch from {len(valid_urls)} to 1,000 URLs to avoid abuse.")
        valid_urls = valid_urls[:1000]

    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": valid_urls
    }

    if dry_run:
        print("\n[DRY RUN] IndexNow payload prepared:")
        print(json.dumps(payload, indent=2))
        return [{"engine": "DryRun", "status": 200, "message": "Dry run successful", "urls_count": len(valid_urls)}]

    data = json.dumps(payload).encode("utf-8")
    results = []

    for name, endpoint in INDEXNOW_ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "AIDigiTools-IndexNow-Protocol/2026"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                results.append({
                    "engine": name,
                    "status": resp.status,
                    "message": "Submitted successfully to IndexNow",
                    "urls_count": len(valid_urls)
                })
        except urllib.error.HTTPError as e:
            results.append({"engine": name, "status": e.code, "message": str(e), "urls_count": len(valid_urls)})
        except Exception as e:
            results.append({"engine": name, "status": 0, "message": f"Network notice: {e}", "urls_count": len(valid_urls)})

    return results

def main():
    parser = argparse.ArgumentParser(description="Official IndexNow Protocol URL Submitter for aidigitools.tech")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending HTTP request")
    parser.add_argument("--key", default=HEX_KEY, help="Custom IndexNow API key")
    parser.add_argument("--urls", nargs="+", help="Specific list of changed URLs to submit")
    args = parser.parse_args()

    urls_to_submit = args.urls if args.urls else get_canonical_urls()

    print("=" * 65)
    print("AIDigiTools — Official IndexNow Multi-Engine Dispatch")
    print("=" * 65)
    print(f"Host: {HOST}")
    print(f"Key: {args.key}")
    print(f"Verification Location: https://{HOST}/{args.key}.txt")
    print(f"URLs in queue: {len(urls_to_submit)}")

    results = submit_indexnow(urls_to_submit, key=args.key, dry_run=args.dry_run)
    for r in results:
        print(f"[{r['engine']}] Status: {r['status']} — {r['message']} ({r['urls_count']} URLs)")
    print("=" * 65)

if __name__ == "__main__":
    main()
