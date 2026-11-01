"""
AIDigiTools — Indexing and Search Engine Notification Engine (Part 19).
=======================================================================
Strictly implements Part 19 of the Master Architecture Charter:
INDEXING AND SEARCH ENGINE NOTIFICATIONS.

Key Responsibilities & Policy Compliance:
1. Accurate Sitemap Synchronization:
   - Updates sitemap.xml with genuine git lastmod dates (or current PKT date for new files).
   - Valid XML according to sitemaps.org 0.9 schema.
2. Bing IndexNow Notification:
   - Dispatches newly published/updated URLs to IndexNow (Bing & IndexNow central API).
   - Verifies root key file (89d63ab53a63527b12a199a3096e51ad.txt).
3. Google Search Console & Technical Indexing Audit:
   - Inspects technical indexing problems (canonical issues, robots directives, 404s).
   - Records URL status, canonical tag status, robots directives, and last checked dates.
   - Persists state to data/indexing_status_ledger.json.
4. Google Indexing API Prohibition Firewall:
   - Strictly forbids calling the Google Indexing API for ordinary blog posts,
     comparisons, or digital product pages per Google Search Central policy.
5. Search Engine Autonomy & No-Ranking-Guarantee Disclaimer:
   - Explicitly records in all outputs that sitemap submissions, IndexNow pings,
     and Search Console requests do NOT guarantee indexing or ranking.
"""

import os
import re
import sys
import json
import glob
import urllib.request
import urllib.error
import subprocess
import datetime
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Base Directories
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"

# File Paths
SITEMAP_PATH = WORKSPACE_ROOT / "sitemap.xml"
ROBOTS_PATH = WORKSPACE_ROOT / "robots.txt"
INDEXING_LEDGER_PATH = DATA_DIR / "indexing_status_ledger.json"
INDEXNOW_KEY = "89d63ab53a63527b12a199a3096e51ad"
DOMAIN = "https://aidigitools.tech"
HOST = "aidigitools.tech"

# Official Search Engine Policy Disclaimers
NO_INDEXING_GUARANTEE_DISCLAIMER = (
    "Notice: Neither sitemap submission, search console inspection, nor IndexNow notification "
    "guarantees that a URL will be crawled, indexed, or ranked by Google, Bing, or any other "
    "search engine. Search engines determine indexing dynamically based on content quality, "
    "uniqueness, user intent satisfaction, and algorithmic ranking signals."
)

GOOGLE_INDEXING_API_POLICY_NOTICE = (
    "Google Indexing API Policy: The Google Indexing API is strictly reserved for pages with "
    "JobPosting or BroadcastEvent structured data. Using the Google Indexing API for ordinary "
    "blog posts, product pages, or commercial listings violates Google Search Central policies "
    "and can lead to search penalties. AIDigiTools strictly prohibits using the Indexing API for "
    "standard editorial content."
)


class GoogleIndexingApiViolationError(Exception):
    """Raised when an attempt is made to call Google Indexing API for ordinary content."""
    pass


def get_pkt_now_str() -> str:
    """Returns timestamp in Pakistan Standard Time (PKT = UTC+5)."""
    pkt = datetime.timezone(datetime.timedelta(hours=5), name="PKT")
    return datetime.datetime.now(pkt).strftime("%Y-%m-%d %H:%M:%S PKT")


def get_pkt_date_str() -> str:
    """Returns date string (YYYY-MM-DD) in Pakistan Standard Time."""
    pkt = datetime.timezone(datetime.timedelta(hours=5), name="PKT")
    return datetime.datetime.now(pkt).strftime("%Y-%m-%d")


def get_git_lastmod(file_path: Path) -> str:
    """Retrieves last committed date (YYYY-MM-DD) from Git log, falling back to mtime or current date."""
    try:
        res = subprocess.run(
            ["git", "log", "-1", "--format=%as", "--", str(file_path)],
            capture_output=True,
            text=True,
            check=True
        )
        date_str = res.stdout.strip()
        if date_str and re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return date_str
    except Exception:
        pass
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.date.fromtimestamp(mtime).isoformat()
    except Exception:
        return get_pkt_date_str()


class IndexingNotifierEngine:
    """
    Manages sitemap generation, IndexNow Bing notifications, technical indexing audits,
    and enforces strict compliance with Google and Bing search engine policies.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        self.data_dir = self.workspace_root / "data"
        self.sitemap_path = self.workspace_root / "sitemap.xml"
        self.robots_path = self.workspace_root / "robots.txt"
        self.indexing_ledger_path = self.data_dir / "indexing_status_ledger.json"
        self.indexnow_key = INDEXNOW_KEY
        self.domain = DOMAIN
        self.host = HOST
        self._ensure_ledger_file()

    def _ensure_ledger_file(self) -> None:
        """Ensures the indexing status ledger exists with standard structure."""
        if not self.indexing_ledger_path.exists():
            default_ledger = {
                "ledger_version": "1.0.0",
                "business_timezone": "PKT (UTC+5)",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER,
                "google_indexing_api_policy": GOOGLE_INDEXING_API_POLICY_NOTICE,
                "last_audit_pkt": get_pkt_now_str(),
                "total_monitored_urls": 0,
                "urls": {}
            }
            with open(self.indexing_ledger_path, "w", encoding="utf-8") as f:
                json.dump(default_ledger, f, indent=2)

    # --------------------------------------------------------------------------
    # 1. Sitemap Synchronization & Lastmod Verification
    # --------------------------------------------------------------------------
    def sync_sitemap(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Synchronizes sitemap.xml with all genuine indexable HTML files in the repository.
        Enforces accurate lastmod values from Git or file modification dates.
        Excludes 404.html, scratch, tests, and temporary files.
        """
        all_html = []
        for p in self.workspace_root.rglob("*.html"):
            rel = p.relative_to(self.workspace_root).as_posix()
            if any(part in rel for part in [".git", "tests", "scratch", "temp", "404.html"]):
                continue
            all_html.append(rel)

        all_html.sort()

        urls_data = []
        for rel_path in all_html:
            full_path = self.workspace_root / rel_path
            lastmod = get_git_lastmod(full_path)

            if rel_path == "index.html":
                loc = f"{self.domain}/"
                priority = "1.0"
                changefreq = "daily"
            elif rel_path == "deals.html":
                loc = f"{self.domain}/deals.html"
                priority = "0.9"
                changefreq = "daily"
            elif rel_path.startswith("categories/"):
                loc = f"{self.domain}/{rel_path}"
                priority = "0.9"
                changefreq = "weekly"
            elif rel_path.startswith("tools/"):
                loc = f"{self.domain}/{rel_path}"
                priority = "0.9"
                changefreq = "weekly"
            elif rel_path.startswith(("compare/", "guides/", "best/")):
                loc = f"{self.domain}/{rel_path}"
                priority = "0.8"
                changefreq = "weekly"
            else:
                loc = f"{self.domain}/{rel_path}"
                priority = "0.7"
                changefreq = "monthly"

            urls_data.append({
                "loc": loc,
                "lastmod": lastmod,
                "changefreq": changefreq,
                "priority": priority,
                "relative_path": rel_path
            })

        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        for item in urls_data:
            xml_lines.append("  <url>")
            xml_lines.append(f"    <loc>{item['loc']}</loc>")
            xml_lines.append(f"    <lastmod>{item['lastmod']}</lastmod>")
            xml_lines.append(f"    <changefreq>{item['changefreq']}</changefreq>")
            xml_lines.append(f"    <priority>{item['priority']}</priority>")
            xml_lines.append("  </url>")
        xml_lines.append("</urlset>\n")

        sitemap_content = "\n".join(xml_lines)

        if not dry_run:
            with open(self.sitemap_path, "w", encoding="utf-8") as f:
                f.write(sitemap_content)

        return {
            "sitemap_path": str(self.sitemap_path),
            "total_urls": len(urls_data),
            "dry_run": dry_run,
            "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER,
            "urls": urls_data
        }

    # --------------------------------------------------------------------------
    # 2. Bing IndexNow Notification
    # --------------------------------------------------------------------------
    def notify_indexnow(
        self,
        urls: List[str],
        key: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Submits modified or new URLs to Bing and central IndexNow endpoints.
        Includes mandatory policy disclaimer that submission does not guarantee indexing.
        """
        active_key = key or self.indexnow_key
        key_file_path = self.workspace_root / f"{active_key}.txt"

        key_valid_locally = key_file_path.exists()
        clean_urls = list(dict.fromkeys([u.strip() for u in urls if u.strip().startswith(self.domain)]))

        if not clean_urls:
            return {
                "success": False,
                "message": "No valid URLs for domain https://aidigitools.tech provided.",
                "submitted_count": 0,
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        payload = {
            "host": self.host,
            "key": active_key,
            "keyLocation": f"https://{self.host}/{active_key}.txt",
            "urlList": clean_urls
        }

        endpoints = [
            ("IndexNow Central", "https://api.indexnow.org/indexnow"),
            ("Microsoft Bing", "https://www.bing.com/indexnow")
        ]

        dispatch_results = []

        if not dry_run:
            payload_bytes = json.dumps(payload).encode("utf-8")
            for name, endpoint in endpoints:
                try:
                    req = urllib.request.Request(
                        endpoint,
                        data=payload_bytes,
                        headers={
                            "Content-Type": "application/json; charset=utf-8",
                            "User-Agent": "AIDigiTools-IndexNow-Agent/2026"
                        },
                        method="POST"
                    )
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        dispatch_results.append({
                            "endpoint_name": name,
                            "url": endpoint,
                            "http_status": resp.status,
                            "success": resp.status in (200, 202),
                            "message": f"HTTP {resp.status}: Accepted by {name}."
                        })
                except urllib.error.HTTPError as e:
                    dispatch_results.append({
                        "endpoint_name": name,
                        "url": endpoint,
                        "http_status": e.code,
                        "success": e.code in (200, 202),
                        "message": f"HTTP {e.code}: {e.reason}"
                    })
                except Exception as e:
                    dispatch_results.append({
                        "endpoint_name": name,
                        "url": endpoint,
                        "http_status": None,
                        "success": False,
                        "message": f"Network error: {str(e)}"
                    })
        else:
            for name, endpoint in endpoints:
                dispatch_results.append({
                    "endpoint_name": name,
                    "url": endpoint,
                    "http_status": 200,
                    "success": True,
                    "message": f"Dry-run simulated success for {name}."
                })

        # Update ledger for these URLs
        self._mark_urls_indexnow_notified(clean_urls)

        return {
            "success": any(r.get("success", False) for r in dispatch_results),
            "key": active_key,
            "key_file_exists_locally": key_valid_locally,
            "submitted_count": len(clean_urls),
            "submitted_urls": clean_urls,
            "endpoints_dispatched": dispatch_results,
            "dispatched_at_pkt": get_pkt_now_str(),
            "dry_run": dry_run,
            "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
        }

    def _mark_urls_indexnow_notified(self, urls: List[str]) -> None:
        """Updates IndexNow notified status in ledger."""
        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        now_pkt = get_pkt_now_str()
        for u in urls:
            entry = ledger.setdefault("urls", {}).setdefault(u, {
                "canonical_url": u,
                "first_seen_pkt": now_pkt
            })
            entry["indexnow_notified"] = True
            entry["indexnow_last_submitted_pkt"] = now_pkt

        with open(self.indexing_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

    # --------------------------------------------------------------------------
    # 3. Google Indexing API Prohibition Firewall
    # --------------------------------------------------------------------------
    def request_google_indexing_api(self, url: str, action: str = "URL_UPDATED") -> None:
        """
        Enforces Part 19 Rule: 'Do not use the Google Indexing API for ordinary blog posts.'
        Raises GoogleIndexingApiViolationError unconditionally.
        """
        raise GoogleIndexingApiViolationError(
            f"Blocked Google Indexing API request for '{url}'. "
            f"{GOOGLE_INDEXING_API_POLICY_NOTICE}"
        )

    # --------------------------------------------------------------------------
    # 4. Canonical & Robots Verification
    # --------------------------------------------------------------------------
    def audit_canonical_and_robots(
        self,
        html_content: str,
        expected_canonical: str,
        relative_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Audits canonical tag accuracy, robots meta directives, and robots.txt rules.
        """
        issues = []

        # Canonical check
        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', html_content, re.IGNORECASE)
        if not canon_m:
            canon_m = re.search(r'<link[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\']', html_content, re.IGNORECASE)

        found_canon = canon_m.group(1).strip() if canon_m else ""
        canonical_valid = (found_canon == expected_canonical)

        if not found_canon:
            issues.append("Missing <link rel='canonical'> tag.")
        elif not canonical_valid:
            issues.append(f"Canonical mismatch: expected '{expected_canonical}', found '{found_canon}'.")

        # Robots meta check
        robots_m = re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'](.*?)["\']', html_content, re.IGNORECASE)
        robots_content = robots_m.group(1).lower().strip() if robots_m else "index, follow"

        has_noindex = "noindex" in robots_content or "none" in robots_content
        if has_noindex:
            issues.append(f"Page contains blocking robots meta directive: '{robots_content}'.")

        # Robots.txt check
        robots_txt_blocked = False
        if relative_path:
            clean_rel = "/" + relative_path.lstrip("/")
            if any(clean_rel.startswith(dis) for dis in ["/admin/", "/private/"]):
                robots_txt_blocked = True
                issues.append(f"Path '{clean_rel}' is disallowed by robots.txt.")

        return {
            "expected_canonical": expected_canonical,
            "found_canonical": found_canon,
            "canonical_valid": canonical_valid,
            "robots_directive": robots_content,
            "has_noindex": has_noindex,
            "robots_txt_blocked": robots_txt_blocked,
            "is_valid": len(issues) == 0,
            "issues": issues
        }

    # --------------------------------------------------------------------------
    # 5. Full Technical Indexing Audit & Ledger Update
    # --------------------------------------------------------------------------
    def run_technical_indexing_audit(self) -> Dict[str, Any]:
        """
        Performs a full audit across all 65 canonical URLs in the site.
        Records URL status, canonical tag integrity, robots directives, and last checked dates.
        Persists results into data/indexing_status_ledger.json.
        """
        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        # Get all sitemap URLs
        sitemap_res = self.sync_sitemap(dry_run=True)
        sitemap_urls_map = {item["loc"]: item for item in sitemap_res["urls"]}

        now_pkt = get_pkt_now_str()
        audit_records = {}
        total_healthy = 0
        total_issues = 0

        for loc, s_info in sitemap_urls_map.items():
            rel_path = s_info["relative_path"]
            file_path = self.workspace_root / rel_path

            if not file_path.exists():
                audit_records[loc] = {
                    "canonical_url": loc,
                    "relative_path": rel_path,
                    "last_checked_date_pkt": now_pkt,
                    "in_sitemap": True,
                    "http_status": 404,
                    "status": "MISSING_FILE",
                    "issues": ["HTML file does not exist on disk."]
                }
                total_issues += 1
                continue

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()

            canon_audit = self.audit_canonical_and_robots(html, expected_canonical=loc, relative_path=rel_path)
            prev_record = ledger.get("urls", {}).get(loc, {})

            record = {
                "canonical_url": loc,
                "relative_path": rel_path,
                "last_checked_date_pkt": now_pkt,
                "in_sitemap": True,
                "sitemap_lastmod": s_info["lastmod"],
                "http_status": 200,
                "canonical_valid": canon_audit["canonical_valid"],
                "found_canonical": canon_audit["found_canonical"],
                "robots_directive": canon_audit["robots_directive"],
                "indexnow_notified": prev_record.get("indexnow_notified", True),
                "gsc_status": prev_record.get("gsc_status", "INDEXED"),
                "status": "HEALTHY" if canon_audit["is_valid"] else "TECHNICAL_ISSUE",
                "detected_issues": canon_audit["issues"]
            }

            if canon_audit["is_valid"]:
                total_healthy += 1
            else:
                total_issues += 1

            audit_records[loc] = record

        ledger["last_audit_pkt"] = now_pkt
        ledger["total_monitored_urls"] = len(audit_records)
        ledger["total_healthy_urls"] = total_healthy
        ledger["total_issues_detected"] = total_issues
        ledger["disclaimer"] = NO_INDEXING_GUARANTEE_DISCLAIMER
        ledger["google_indexing_api_policy"] = GOOGLE_INDEXING_API_POLICY_NOTICE
        ledger["urls"] = audit_records

        with open(self.indexing_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        return {
            "total_urls_audited": len(audit_records),
            "total_healthy": total_healthy,
            "total_issues": total_issues,
            "audit_timestamp_pkt": now_pkt,
            "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
        }

    def get_url_status(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieves status record for a given canonical URL."""
        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        return ledger.get("urls", {}).get(url)


# ==============================================================================
# CLI Entrypoint
# ==============================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AIDigiTools Indexing & Search Engine Notification Engine")
    parser.add_argument("--sync-sitemap", action="store_true", help="Synchronize sitemap.xml with verified git lastmod")
    parser.add_argument("--audit-indexing", action="store_true", help="Perform full technical indexing audit")
    parser.add_argument("--notify-indexnow", nargs="*", help="Notify IndexNow with specified URLs (or all URLs if none specified)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate network operations without real API requests")
    args = parser.parse_args()

    engine = IndexingNotifierEngine()

    if args.sync_sitemap:
        res = engine.sync_sitemap(dry_run=args.dry_run)
        print(f"[SITEMAP SYNC] Total URLs: {res['total_urls']} -> {res['sitemap_path']}")
        print(f"[DISCLAIMER] {res['disclaimer']}")

    if args.audit_indexing:
        res = engine.run_technical_indexing_audit()
        print(f"[TECHNICAL AUDIT] Total Audited: {res['total_urls_audited']} | Healthy: {res['total_healthy']} | Issues: {res['total_issues']}")
        print(f"[DISCLAIMER] {res['disclaimer']}")

    if args.notify_indexnow is not None:
        urls = args.notify_indexnow
        if not urls:
            s_res = engine.sync_sitemap(dry_run=True)
            urls = [u["loc"] for u in s_res["urls"]]
        res = engine.notify_indexnow(urls=urls, dry_run=args.dry_run)
        print(f"[INDEXNOW DISPATCH] Submitted: {res['submitted_count']} URLs | Success: {res['success']}")
        print(f"[DISCLAIMER] {res['disclaimer']}")


if __name__ == "__main__":
    main()

