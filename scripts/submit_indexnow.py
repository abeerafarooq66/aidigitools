import os
import sys
import json
import re
import argparse
import subprocess
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

HTTP_STATUS_MEANINGS = {
    200: "200 OK — URL(s) successfully received by search engine and key verified.",
    202: "202 Accepted — URL(s) received; key validation is pending or asynchronous queue accepted.",
    400: "400 Bad Request — Invalid syntax or missing required JSON fields (host, key, urlList).",
    403: "403 Forbidden — Key invalid, keyLocation domain mismatch, or key file missing on server.",
    422: "422 Unprocessable Entity — Submitted URLs do not belong to the host or key format invalid.",
    429: "429 Too Many Requests — Submission rate limit exceeded. Backoff required."
}

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

def verify_live_key_url(key: str, host: str = HOST, timeout: int = 10) -> bool:
    """Verifies that the key file is publicly live and accessible over HTTPS."""
    url = f"https://{host}/{key}.txt"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AIDigiTools-IndexNow-Verifier/2026"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                body = resp.read().decode("utf-8").strip()
                if body == key:
                    print(f"[LIVE CHECK] Verified key file over HTTPS: {url} (HTTP 200, matching key)")
                    return True
                print(f"[ERROR] Live key mismatch at {url}: expected '{key}', got '{body}'")
                return False
            print(f"[ERROR] Live key check failed with status {resp.status} at {url}")
            return False
    except Exception as e:
        print(f"[WARNING] Live HTTPS key verification notice for {url}: {e}")
        return False

def get_canonical_urls() -> list[str]:
    """Retrieves all legitimate canonical URLs from sitemap.xml."""
    sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
    if not os.path.exists(sitemap_path):
        return []
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    urls = re.findall(r"<loc>(https://aidigitools\.tech/[^<]*)</loc>", content)
    return sorted(list(set(urls)))

def get_changed_urls_from_git() -> list[str]:
    """Inspects git diff against previous commit or working tree to detect changed public HTML pages."""
    changed_urls = []
    canonical_urls = set(get_canonical_urls())
    try:
        # Check diff between HEAD~1 and HEAD
        cmd = ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
        res = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
        files = res.stdout.strip().splitlines() if res.returncode == 0 else []
        if not files:
            # Fallback to diff between HEAD and working tree
            cmd_status = ["git", "diff", "--name-only", "HEAD"]
            res_status = subprocess.run(cmd_status, cwd=ROOT_DIR, capture_output=True, text=True)
            files = res_status.stdout.strip().splitlines() if res_status.returncode == 0 else []

        # If sitemap.xml changed, queue all canonical URLs
        if any("sitemap.xml" in f for f in files):
            print("[INFO] sitemap.xml changed; queueing all canonical URLs.")
            return sorted(list(canonical_urls))

        for f in files:
            f = f.replace("\\", "/").strip()
            if not f.endswith(".html") or "404.html" in f or f.startswith("tests/") or f.startswith("scratch/"):
                continue
            if f == "index.html":
                url = f"https://{HOST}/"
            else:
                url = f"https://{HOST}/{f}"
            if url in canonical_urls:
                changed_urls.append(url)
    except Exception as e:
        print(f"[WARNING] Could not determine changed files from git: {e}")

    return sorted(list(set(changed_urls)))

def submit_indexnow(urls: list[str], key: str = HEX_KEY, dry_run: bool = False) -> list[dict]:
    """Submits legitimate canonical URLs to participating IndexNow search engines."""
    # Guardrail 1: Validate local key file exists and matches
    if not validate_key_file(key):
        raise ValueError("IndexNow key verification file validation failed.")

    # Guardrail 2: Filter and sanitize URLs (must belong strictly to aidigitools.tech, no params, no hashes)
    canonical_set = set(get_canonical_urls())
    valid_urls = []
    for u in urls:
        u_clean = u.strip()
        if not u_clean.startswith(f"https://{HOST}/"):
            continue
        if "?" in u_clean or "#" in u_clean:
            continue
        # Ensure URL is recognized in canonical sitemap or is a legitimate public page
        if u_clean in canonical_set or u_clean == f"https://{HOST}/":
            valid_urls.append(u_clean)

    valid_urls = sorted(list(set(valid_urls)))

    if not valid_urls:
        print("[NOTICE] No valid public canonical URLs to submit.")
        return []

    # Guardrail 3: Limit submissions to reasonable batch size (IndexNow protocol max is 10,000)
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
        return [{
            "engine": "DryRun",
            "status": 200,
            "message": "Dry run successful (payload validated)",
            "urls_count": len(valid_urls)
        }]

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
            with urllib.request.urlopen(req, timeout=15) as resp:
                meaning = HTTP_STATUS_MEANINGS.get(resp.status, f"HTTP {resp.status}")
                results.append({
                    "engine": name,
                    "status": resp.status,
                    "message": meaning,
                    "urls_count": len(valid_urls)
                })
        except urllib.error.HTTPError as e:
            meaning = HTTP_STATUS_MEANINGS.get(e.code, f"HTTP {e.code} — {e.reason}")
            results.append({
                "engine": name,
                "status": e.code,
                "message": meaning,
                "urls_count": len(valid_urls)
            })
        except Exception as e:
            results.append({
                "engine": name,
                "status": 0,
                "message": f"Network exception: {e}",
                "urls_count": len(valid_urls)
            })

    return results

def main():
    parser = argparse.ArgumentParser(description="Official IndexNow Protocol URL Submitter for aidigitools.tech")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending HTTP request")
    parser.add_argument("--key", default=HEX_KEY, help="Custom IndexNow API key")
    parser.add_argument("--urls", nargs="+", help="Specific list of changed URLs to submit")
    parser.add_argument("--git-diff", action="store_true", help="Submit only public HTML pages changed in recent git commit")
    parser.add_argument("--verify-live", action="store_true", help="Perform live HTTPS check of key file before submitting")
    args = parser.parse_args()

    if args.verify_live:
        live_ok = verify_live_key_url(args.key)
        if not live_ok:
            print("[ERROR] Live verification failed. Aborting submission.")
            sys.exit(1)

    if args.urls:
        urls_to_submit = args.urls
    elif args.git-diff if hasattr(args, "git-diff") else args.git_diff:
        urls_to_submit = get_changed_urls_from_git()
        if not urls_to_submit:
            print("[INFO] No public HTML pages modified in git diff. Checking sitemap...")
            # If nothing in git diff (e.g. initial run or non-page changes), don't spam endpoints
            print("[INFO] Zero webpage changes detected. No IndexNow submission required.")
            sys.exit(0)
    else:
        urls_to_submit = get_canonical_urls()

    print("=" * 68)
    print("AIDigiTools — Official IndexNow Multi-Engine Dispatch")
    print("=" * 68)
    print(f"Host: {HOST}")
    print(f"Key: {args.key}")
    print(f"Verification Location: https://{HOST}/{args.key}.txt")
    print(f"URLs in queue: {len(urls_to_submit)}")

    results = submit_indexnow(urls_to_submit, key=args.key, dry_run=args.dry_run)
    for r in results:
        print(f"[{r['engine']}] Status {r['status']}: {r['message']} ({r['urls_count']} URLs)")
    print("=" * 68)
    print("Note: IndexNow notifies Bing, Yandex, Seznam, and Naver immediately.")
    print("Submission receipt (200/202) confirms search engines received the notification.")
    print("It does not guarantee immediate indexing, which depends on crawl budget and quality.")
    print("=" * 68)

    # Return non-zero if all endpoints failed with error codes
    if results and not args.dry_run:
        success_count = sum(1 for r in results if r['status'] in (200, 202))
        if success_count == 0:
            sys.exit(1)

if __name__ == "__main__":
    main()
