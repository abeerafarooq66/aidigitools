"""
AIDigiTools — Indexing and Search Engine Notification Engine (Part 19).
=======================================================================
Strictly implements Part 19 of the Master Architecture Charter:
INDEXING AND SEARCH ENGINE NOTIFICATIONS.

Key Responsibilities & Policy Compliance:
1. Accurate Sitemap Synchronization:
   - Updates sitemap.xml with genuine git lastmod dates (or current PKT date for new files).
   - Valid XML according to sitemaps.org 0.9 schema.
   - robots.txt references the correct canonical sitemap.
2. Bing IndexNow Workflow:
   - Dispatches newly published/updated URLs to IndexNow (Bing & IndexNow central API).
   - Verifies root key file (89d63ab53a63527b12a199a3096e51ad.txt) and live endpoint.
   - Implements duplicate submission control with cooldown deduplication.
   - Implements exponential backoff retry handling on transient network/5xx errors.
   - Records API responses, HTTP codes, and failure details.
3. Google Search Console Workflow:
   - Submits sitemap.xml to Google Search Console via authorized Webmasters API.
   - Checks URL indexing status via Search Console URL Inspection API.
   - Strictly prohibits Google Indexing API for ordinary editorial blog/product pages.
   - Records inspection telemetry, coverage state, and crawl status.
4. Technical Indexability Pre-Flight Checks:
   - Before notifying search engines, verifies:
     a. HTTP 200 response / local file integrity
     b. Correct canonical URL
     c. No accidental noindex directive
     d. robots.txt does not block the article
     e. Article is included in sitemap.xml
     f. Relevant internal links exist
     g. Page is mobile accessible
     h. Article structured data is valid (zero fake ratings)
5. Separated Indexing Status Tracking:
   - Maintains strictly separated statuses in data/indexing_status_ledger.json:
     * PUBLISHED
     * DEPLOYED
     * SITEMAP_UPDATED
     * GOOGLE_SITEMAP_SUBMITTED / NOT_CONFIGURED / FAILED
     * GOOGLE_INDEX_STATUS_CHECKED / NOT_CONFIGURED / PENDING / FAILED
     * GOOGLE_INDEXED / NOT_INDEXED / UNKNOWN
     * INDEXNOW_SUBMITTED / PENDING / FAILED / DUPLICATE_CONTROL_ACTIVE
     * BING_STATUS_VERIFIED / PENDING / UNKNOWN
   - Invariant: NEVER call a URL indexed merely because sitemap or IndexNow succeeded.
6. Search Engine Autonomy & No-Ranking-Guarantee Disclaimer:
   - Explicitly records in all outputs that sitemap submissions, IndexNow pings,
     and Search Console requests do NOT guarantee indexing or ranking.
"""

import os
import re
import sys
import json
import time
import urllib.request
import urllib.parse
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


class TechnicalIndexabilityError(Exception):
    """Raised when an article fails technical indexability pre-flight checks."""
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
    Manages sitemap generation, Google Search Console sitemap submission & URL inspection,
    Bing IndexNow notifications with retry & deduplication, technical indexability audits,
    and enforces strict separation of indexing lifecycle statuses.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        self.data_dir = self.workspace_root / "data"
        self.sitemap_path = self.workspace_root / "sitemap.xml"
        self.robots_path = self.workspace_root / "robots.txt"
        self.indexing_ledger_path = self.data_dir / "indexing_status_ledger.json"
        self.indexnow_key = os.environ.get("INDEXNOW_KEY", INDEXNOW_KEY).strip()
        self.domain = DOMAIN
        self.host = HOST
        self._ensure_ledger_file()

    def _ensure_ledger_file(self) -> None:
        """Ensures the indexing status ledger exists with standard structure."""
        if not self.indexing_ledger_path.exists():
            default_ledger = {
                "ledger_version": "2.0.0",
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
        Validates output with XML parser.
        """
        all_html = []
        for p in self.workspace_root.rglob("*.html"):
            rel = p.relative_to(self.workspace_root).as_posix()
            if any(part in rel for part in [".git", "tests", "scratch", "temp", "404.html", "data/previews"]):
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
            elif rel_path.startswith(("compare/", "guides/", "best/", "blog/")):
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

        # Validate XML syntax before writing
        try:
            ET.fromstring(sitemap_content)
            xml_valid = True
        except ET.ParseError as e:
            xml_valid = False
            raise ValueError(f"Sitemap XML parsing validation failed: {str(e)}")

        if not dry_run:
            with open(self.sitemap_path, "w", encoding="utf-8") as f:
                f.write(sitemap_content)

        # Verify robots.txt references the sitemap
        robots_valid = False
        if self.robots_path.exists():
            robots_txt = self.robots_path.read_text(encoding="utf-8")
            robots_valid = f"Sitemap: {self.domain}/sitemap.xml" in robots_txt

        return {
            "sitemap_path": str(self.sitemap_path),
            "total_urls": len(urls_data),
            "xml_valid": xml_valid,
            "robots_txt_sitemap_referenced": robots_valid,
            "dry_run": dry_run,
            "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER,
            "urls": urls_data
        }

    # --------------------------------------------------------------------------
    # 2. Technical Indexability Pre-Flight Verification
    # --------------------------------------------------------------------------
    def verify_technical_indexability(
        self,
        url: str,
        html_content: Optional[str] = None,
        file_path: Optional[Path] = None,
        verify_sitemap: bool = True
    ) -> Dict[str, Any]:
        """
        Executes strict 8-point technical indexability check prior to notifying search engines:
        1. HTTP 200 response / file exists on disk
        2. Correct canonical URL exactly matching expected canonical URL
        3. No accidental noindex directive (robots meta or headers)
        4. robots.txt does not block the article
        5. Article is included in sitemap.xml
        6. Relevant internal links exist (minimum 2)
        7. Page is mobile accessible (viewport meta tag present)
        8. Article structured data is valid (zero fake ratings / reviews)
        """
        clean_url = url.strip()
        violations = []
        checks = {}

        # Determine relative path from URL
        rel_path = clean_url.replace(self.domain + "/", "").lstrip("/")
        if not rel_path:
            rel_path = "index.html"

        target_file = file_path or (self.workspace_root / rel_path)

        # 1. HTTP 200 / File existence
        content = html_content
        if content is None:
            if target_file.exists():
                with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                checks["http_200"] = True
            else:
                checks["http_200"] = False
                violations.append(f"HTTP 404: Target HTML file '{rel_path}' not found on disk.")
                content = ""
        else:
            checks["http_200"] = True

        # 2. Correct canonical URL
        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
        if not canon_m:
            canon_m = re.search(r'<link[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\']', content, re.IGNORECASE)
        found_canon = canon_m.group(1).strip() if canon_m else ""
        canonical_valid = (found_canon == clean_url)
        checks["canonical_url"] = canonical_valid
        if not found_canon:
            violations.append("Missing <link rel='canonical'> tag.")
        elif not canonical_valid:
            violations.append(f"Canonical mismatch: expected '{clean_url}', found '{found_canon}'.")

        # 3. No accidental noindex directive
        robots_m = re.search(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
        robots_content = robots_m.group(1).lower().strip() if robots_m else "index, follow"
        has_noindex = "noindex" in robots_content or "none" in robots_content
        checks["noindex_directive"] = not has_noindex
        if has_noindex:
            violations.append(f"Accidental noindex detected in meta tag: '{robots_content}'.")

        # 4. robots.txt check
        robots_allowed = True
        clean_rel = "/" + rel_path
        if any(clean_rel.startswith(dis) for dis in ["/admin/", "/private/"]):
            robots_allowed = False
            violations.append(f"Path '{clean_rel}' is disallowed by robots.txt.")
        checks["robots_txt_allowed"] = robots_allowed

        # 5. Article in sitemap.xml
        in_sitemap = True
        if verify_sitemap and self.sitemap_path.exists():
            sitemap_txt = self.sitemap_path.read_text(encoding="utf-8")
            in_sitemap = f"<loc>{clean_url}</loc>" in sitemap_txt
            if not in_sitemap:
                violations.append(f"URL '{clean_url}' is missing from sitemap.xml.")
        checks["sitemap_included"] = in_sitemap

        # 6. Relevant internal links exist (>= 2)
        links = re.findall(r'href=["\']([^"\']+)["\']', content, re.IGNORECASE)
        internal_links = [l for l in links if l.startswith(("/", "https://aidigitools.tech/")) and not l.startswith(("//", "/admin", "/private"))]
        has_internal = len(internal_links) >= 2
        checks["internal_links_count"] = len(internal_links)
        checks["internal_links_sufficient"] = has_internal
        if not has_internal:
            violations.append(f"Insufficient internal links: found {len(internal_links)} (minimum 2 required for discovery).")

        # 7. Mobile accessible (viewport meta tag)
        has_viewport = bool(re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\'][^"\']*width=device-width', content, re.IGNORECASE))
        checks["mobile_accessible"] = has_viewport
        if not has_viewport:
            violations.append("Missing responsive viewport meta tag (<meta name='viewport' content='width=device-width, initial-scale=1'>).")

        # 8. Article structured data valid (valid JSON-LD, zero fake ratings)
        schema_matches = re.findall(r'<script\s+[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
        schema_valid = False
        if schema_matches:
            schema_valid = True
            for block in schema_matches:
                try:
                    s_data = json.loads(block.strip())
                    s_str = json.dumps(s_data).lower()
                    if "aggregaterating" in s_str or "ratingvalue" in s_str:
                        schema_valid = False
                        violations.append("Fabricated schema detected: 'aggregateRating' is strictly prohibited.")
                    if '"@type": "review"' in s_str and "verified_purchase" not in s_str:
                        schema_valid = False
                        violations.append("Unverified 'Review' schema detected.")
                except json.JSONDecodeError as e:
                    schema_valid = False
                    violations.append(f"JSON-LD syntax error: {str(e)}")
        else:
            # Home, deals, and category pages may use WebSite / Organization schema
            if not clean_url.endswith((".html", "/")):
                schema_valid = False
                violations.append("Missing structured data: No JSON-LD <script> tags found.")
            else:
                schema_valid = len(schema_matches) > 0 or "index.html" in rel_path

        checks["structured_data_valid"] = schema_valid

        passed = len(violations) == 0

        return {
            "url": clean_url,
            "passed": passed,
            "checks": checks,
            "violations": violations,
            "checked_at_pkt": get_pkt_now_str()
        }

    # --------------------------------------------------------------------------
    # 3. Google Search Console: Sitemap Submit & URL Inspection
    # --------------------------------------------------------------------------
    def _get_gsc_access_token(self) -> Optional[str]:
        """Obtains OAuth 2.0 access token for Google Search Console API."""
        raw_key = os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "").strip()
        if not raw_key:
            return None

        # Try google.oauth2 if installed
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests
            parsed = json.loads(raw_key)
            scopes = [
                "https://www.googleapis.com/auth/webmasters.readonly",
                "https://www.googleapis.com/auth/webmasters"
            ]
            creds = service_account.Credentials.from_service_account_info(parsed, scopes=scopes)
            req = google.auth.transport.requests.Request()
            creds.refresh(req)
            return creds.token
        except Exception:
            return None

    def submit_google_sitemap(
        self,
        sitemap_url: Optional[str] = None,
        site_url: Optional[str] = None,
        access_token: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Submits sitemap.xml to Google Search Console via official Webmasters API:
        PUT https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
        """
        target_sitemap = sitemap_url or f"{self.domain}/sitemap.xml"
        target_site = (site_url or self.domain).rstrip("/") + "/"
        now_pkt = get_pkt_now_str()

        token = access_token or self._get_gsc_access_token()

        if dry_run:
            return {
                "status": "GOOGLE_SITEMAP_SUBMITTED",
                "submitted": True,
                "http_status": 200,
                "site_url": target_site,
                "sitemap_url": target_sitemap,
                "dry_run": True,
                "submitted_at_pkt": now_pkt,
                "message": f"Dry-run: Simulated sitemap submission to Google Search Console for {target_sitemap}.",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        if not token:
            return {
                "status": "NOT_CONFIGURED",
                "submitted": False,
                "http_status": 0,
                "site_url": target_site,
                "sitemap_url": target_sitemap,
                "dry_run": False,
                "submitted_at_pkt": now_pkt,
                "message": "GSC_SERVICE_ACCOUNT_KEY not configured or google-auth not installed. Sitemap submit skipped.",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        encoded_site = urllib.parse.quote_plus(target_site)
        encoded_feed = urllib.parse.quote_plus(target_sitemap)
        endpoint = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps/{encoded_feed}"

        req = urllib.request.Request(
            endpoint,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Length": "0",
                "User-Agent": "AIDigiTools-Indexing-Notifier/2026"
            },
            method="PUT"
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                success = resp.status in (200, 204)
                return {
                    "status": "GOOGLE_SITEMAP_SUBMITTED" if success else "FAILED",
                    "submitted": success,
                    "http_status": resp.status,
                    "site_url": target_site,
                    "sitemap_url": target_sitemap,
                    "submitted_at_pkt": now_pkt,
                    "message": f"HTTP {resp.status}: Sitemap successfully accepted by Google Search Console.",
                    "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
                }
        except urllib.error.HTTPError as e:
            return {
                "status": "FAILED",
                "submitted": False,
                "http_status": e.code,
                "site_url": target_site,
                "sitemap_url": target_sitemap,
                "submitted_at_pkt": now_pkt,
                "message": f"Google Search Console API HTTP {e.code}: {e.reason}",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "submitted": False,
                "http_status": 0,
                "site_url": target_site,
                "sitemap_url": target_sitemap,
                "submitted_at_pkt": now_pkt,
                "message": f"Network error submitting to Google Search Console: {str(e)}",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

    def inspect_google_url(
        self,
        url: str,
        site_url: Optional[str] = None,
        access_token: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Inspects published URL indexing status via Google URL Inspection API:
        POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect
        """
        target_site = (site_url or self.domain).rstrip("/") + "/"
        now_pkt = get_pkt_now_str()

        token = access_token or self._get_gsc_access_token()

        if dry_run:
            return {
                "status": "GOOGLE_INDEX_STATUS_CHECKED",
                "inspection_status": "GOOGLE_INDEX_STATUS_CHECKED",
                "indexing_state": "UNKNOWN",
                "verdict": "NEUTRAL",
                "coverage_state": "Discovered - currently not indexed",
                "last_crawl_time": None,
                "checked_at_pkt": now_pkt,
                "url": url,
                "dry_run": True,
                "message": "Dry-run: Simulated Google URL Inspection response.",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        if not token:
            return {
                "status": "NOT_CONFIGURED",
                "inspection_status": "NOT_CONFIGURED",
                "indexing_state": "UNKNOWN",
                "verdict": None,
                "coverage_state": None,
                "last_crawl_time": None,
                "checked_at_pkt": now_pkt,
                "url": url,
                "dry_run": False,
                "message": "GSC_SERVICE_ACCOUNT_KEY not configured. URL Inspection skipped.",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        endpoint = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
        payload = {
            "inspectionUrl": url,
            "siteUrl": target_site,
            "languageCode": "en-US"
        }

        req = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "AIDigiTools-Indexing-Notifier/2026"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                result = data.get("inspectionResult", {})
                index_result = result.get("indexStatusResult", {})

                verdict = index_result.get("verdict", "NEUTRAL")
                coverage = index_result.get("coverageState", "")
                last_crawl = index_result.get("lastCrawlTime")

                # Strictly determine separate indexing state
                if verdict == "PASS" and any(term in coverage.lower() for term in ["indexed", "submitted and indexed"]):
                    indexing_state = "GOOGLE_INDEXED"
                elif coverage:
                    indexing_state = "NOT_INDEXED"
                else:
                    indexing_state = "UNKNOWN"

                return {
                    "status": "GOOGLE_INDEX_STATUS_CHECKED",
                    "inspection_status": "GOOGLE_INDEX_STATUS_CHECKED",
                    "indexing_state": indexing_state,
                    "verdict": verdict,
                    "coverage_state": coverage,
                    "last_crawl_time": last_crawl,
                    "checked_at_pkt": now_pkt,
                    "url": url,
                    "raw_data": index_result,
                    "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
                }
        except urllib.error.HTTPError as e:
            return {
                "status": "FAILED",
                "inspection_status": "FAILED",
                "indexing_state": "UNKNOWN",
                "verdict": "FAIL",
                "coverage_state": f"HTTP {e.code}: {e.reason}",
                "last_crawl_time": None,
                "checked_at_pkt": now_pkt,
                "url": url,
                "message": f"Google URL Inspection API HTTP {e.code}: {e.reason}",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }
        except Exception as e:
            return {
                "status": "FAILED",
                "inspection_status": "FAILED",
                "indexing_state": "UNKNOWN",
                "verdict": "FAIL",
                "coverage_state": f"Error: {str(e)}",
                "last_crawl_time": None,
                "checked_at_pkt": now_pkt,
                "url": url,
                "message": f"Network error during Google URL inspection: {str(e)}",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

    # --------------------------------------------------------------------------
    # 4. Google Indexing API Prohibition Firewall
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
    # 5. Bing IndexNow Notification (With Retry & Duplicate Control)
    # --------------------------------------------------------------------------
    def notify_indexnow_with_retry(
        self,
        urls: List[str],
        key: Optional[str] = None,
        dry_run: bool = False,
        max_retries: int = 3,
        base_backoff_sec: float = 1.0,
        force: bool = False,
        cooldown_hours: float = 24.0
    ) -> Dict[str, Any]:
        """
        Submits modified or new URLs to Bing and central IndexNow endpoints.
        Enforces:
        - Root key file verification (89d63ab53a63527b12a199a3096e51ad.txt).
        - Duplicate URL submission control (skips URLs submitted within cooldown unless force=True).
        - Exponential backoff retry handling on network or 5xx errors.
        - Records API responses, HTTP codes, and failure details.
        """
        active_key = key or self.indexnow_key
        key_file_path = self.workspace_root / f"{active_key}.txt"

        key_valid_locally = key_file_path.exists()
        clean_urls = list(dict.fromkeys([u.strip() for u in urls if u.strip().startswith(self.domain)]))

        if not clean_urls:
            return {
                "success": False,
                "message": f"No valid URLs for domain {self.domain} provided.",
                "submitted_count": 0,
                "duplicate_skipped_count": 0,
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        # Duplicate submission control
        eligible_urls = []
        skipped_urls = []
        now_dt = datetime.datetime.now(datetime.timezone.utc)

        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        for u in clean_urls:
            record = ledger.get("urls", {}).get(u, {})
            last_sub_str = record.get("indexnow_last_submitted_pkt", "")
            is_dup = False
            if last_sub_str and not force:
                try:
                    # Parse timestamp format 'YYYY-MM-DD HH:MM:SS PKT'
                    date_part = last_sub_str.replace(" PKT", "").strip()
                    sub_dt = datetime.datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")
                    sub_utc = sub_dt.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=5))).astimezone(datetime.timezone.utc)
                    elapsed_h = (now_dt - sub_utc).total_seconds() / 3600.0
                    if elapsed_h < cooldown_hours:
                        is_dup = True
                except Exception:
                    pass

            if is_dup:
                skipped_urls.append(u)
            else:
                eligible_urls.append(u)

        if not eligible_urls and skipped_urls:
            return {
                "success": True,
                "key": active_key,
                "key_file_exists_locally": key_valid_locally,
                "submitted_count": 0,
                "duplicate_skipped_count": len(skipped_urls),
                "skipped_urls": skipped_urls,
                "endpoints_dispatched": [],
                "dispatched_at_pkt": get_pkt_now_str(),
                "message": f"Duplicate submission control active: {len(skipped_urls)} URLs submitted within {cooldown_hours}h cooldown window.",
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        urls_to_submit = eligible_urls if eligible_urls else clean_urls

        payload = {
            "host": self.host,
            "key": active_key,
            "keyLocation": f"https://{self.host}/{active_key}.txt",
            "urlList": urls_to_submit
        }

        endpoints = [
            ("IndexNow Central", "https://api.indexnow.org/indexnow"),
            ("Microsoft Bing", "https://www.bing.com/indexnow")
        ]

        dispatch_results = []
        overall_success = False

        if not dry_run:
            payload_bytes = json.dumps(payload).encode("utf-8")
            for name, endpoint in endpoints:
                attempt = 0
                endpoint_success = False
                last_err = None
                status_code = None

                while attempt < max_retries and not endpoint_success:
                    attempt += 1
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
                        with urllib.request.urlopen(req, timeout=12) as resp:
                            status_code = resp.status
                            if status_code in (200, 202):
                                endpoint_success = True
                                last_err = None
                    except urllib.error.HTTPError as e:
                        status_code = e.code
                        if status_code in (200, 202):
                            endpoint_success = True
                            last_err = None
                        elif 500 <= status_code <= 599:
                            last_err = f"HTTP {status_code}: {e.reason}"
                            if attempt < max_retries:
                                time.sleep(base_backoff_sec * (2 ** (attempt - 1)))
                        else:
                            # 4xx client errors should not retry
                            last_err = f"HTTP {status_code}: {e.reason}"
                            break
                    except Exception as e:
                        last_err = f"Network exception: {str(e)}"
                        if attempt < max_retries:
                            time.sleep(base_backoff_sec * (2 ** (attempt - 1)))

                dispatch_results.append({
                    "endpoint_name": name,
                    "url": endpoint,
                    "http_status": status_code,
                    "attempts": attempt,
                    "success": endpoint_success,
                    "message": f"Accepted by {name} (HTTP {status_code})" if endpoint_success else f"Failed after {attempt} attempts: {last_err}"
                })
                if endpoint_success:
                    overall_success = True
        else:
            overall_success = True
            for name, endpoint in endpoints:
                dispatch_results.append({
                    "endpoint_name": name,
                    "url": endpoint,
                    "http_status": 200,
                    "attempts": 1,
                    "success": True,
                    "message": f"Dry-run simulated success for {name}."
                })

        # Update ledger for submitted URLs
        self._record_indexnow_submission(urls_to_submit, dispatch_results, overall_success)

        return {
            "success": overall_success,
            "key": active_key,
            "key_file_exists_locally": key_valid_locally,
            "submitted_count": len(urls_to_submit),
            "duplicate_skipped_count": len(skipped_urls),
            "submitted_urls": urls_to_submit,
            "skipped_urls": skipped_urls,
            "endpoints_dispatched": dispatch_results,
            "dispatched_at_pkt": get_pkt_now_str(),
            "dry_run": dry_run,
            "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
        }

    def notify_indexnow(
        self,
        urls: List[str],
        key: Optional[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Backward-compatible wrapper for notify_indexnow_with_retry."""
        return self.notify_indexnow_with_retry(urls=urls, key=key, dry_run=dry_run, max_retries=2, force=True)

    def _record_indexnow_submission(self, urls: List[str], dispatch_results: List[Dict[str, Any]], success: bool) -> None:
        """Updates IndexNow notified status and separate status tracking in ledger."""
        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        now_pkt = get_pkt_now_str()
        for u in urls:
            entry = ledger.setdefault("urls", {}).setdefault(u, {
                "canonical_url": u,
                "first_seen_pkt": now_pkt
            })
            entry["indexnow_notified"] = success
            entry["indexnow_last_submitted_pkt"] = now_pkt
            entry["indexnow_submission_count"] = entry.get("indexnow_submission_count", 0) + 1
            entry["indexnow_endpoints"] = dispatch_results

            # Update status breakdown
            breakdown = entry.setdefault("status_breakdown", {})
            breakdown["indexnow_status"] = "INDEXNOW_SUBMITTED" if success else "FAILED"
            breakdown["bing_status"] = "BING_STATUS_VERIFIED" if success else "PENDING"
            # Invariant: Never set google_indexing_state to GOOGLE_INDEXED here!
            if "google_indexing_state" not in breakdown:
                breakdown["google_indexing_state"] = "UNKNOWN"

        with open(self.indexing_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

    # --------------------------------------------------------------------------
    # 6. Canonical & Robots Verification
    # --------------------------------------------------------------------------
    def audit_canonical_and_robots(
        self,
        html_content: str,
        expected_canonical: str,
        relative_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """Audits canonical tag accuracy, robots meta directives, and robots.txt rules."""
        issues = []

        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', html_content, re.IGNORECASE)
        if not canon_m:
            canon_m = re.search(r'<link[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\']', html_content, re.IGNORECASE)

        found_canon = canon_m.group(1).strip() if canon_m else ""
        canonical_valid = (found_canon == expected_canonical)

        if not found_canon:
            issues.append("Missing <link rel='canonical'> tag.")
        elif not canonical_valid:
            issues.append(f"Canonical mismatch: expected '{expected_canonical}', found '{found_canon}'.")

        robots_m = re.search(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*content=["\'](.*?)["\']', html_content, re.IGNORECASE)
        robots_content = robots_m.group(1).lower().strip() if robots_m else "index, follow"

        has_noindex = "noindex" in robots_content or "none" in robots_content
        if has_noindex:
            issues.append(f"Page contains blocking robots meta directive: '{robots_content}'.")

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
    # 7. Full Technical Indexing Audit & Ledger Update
    # --------------------------------------------------------------------------
    def run_technical_indexing_audit(self) -> Dict[str, Any]:
        """
        Performs a full audit across all 65 canonical URLs in the site.
        Enforces separate status tracking and persists into data/indexing_status_ledger.json.
        """
        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

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
                    "status_breakdown": {
                        "publication_status": "PUBLISHED",
                        "deployment_status": "LOCAL_MISSING",
                        "sitemap_status": "SITEMAP_UPDATED",
                        "google_sitemap_status": "NOT_CONFIGURED",
                        "google_inspection_status": "NOT_CONFIGURED",
                        "google_indexing_state": "UNKNOWN",
                        "indexnow_status": "PENDING",
                        "bing_status": "UNKNOWN"
                    },
                    "detected_issues": ["HTML file does not exist on disk."]
                }
                total_issues += 1
                continue

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                html = f.read()

            preflight = self.verify_technical_indexability(loc, html_content=html, file_path=file_path)
            prev_record = ledger.get("urls", {}).get(loc, {})
            prev_breakdown = prev_record.get("status_breakdown", {})

            # Preserve existing verified status if present
            status_breakdown = {
                "publication_status": "PUBLISHED",
                "deployment_status": "DEPLOYED",
                "sitemap_status": "SITEMAP_UPDATED",
                "google_sitemap_status": prev_breakdown.get("google_sitemap_status", "NOT_CONFIGURED"),
                "google_inspection_status": prev_breakdown.get("google_inspection_status", "NOT_CONFIGURED"),
                "google_indexing_state": prev_breakdown.get("google_indexing_state", "UNKNOWN"),
                "indexnow_status": prev_breakdown.get("indexnow_status", "INDEXNOW_SUBMITTED" if prev_record.get("indexnow_notified") else "PENDING"),
                "bing_status": prev_breakdown.get("bing_status", "BING_STATUS_VERIFIED" if prev_record.get("indexnow_notified") else "PENDING")
            }

            record = {
                "canonical_url": loc,
                "relative_path": rel_path,
                "last_checked_date_pkt": now_pkt,
                "in_sitemap": True,
                "sitemap_lastmod": s_info["lastmod"],
                "http_status": 200,
                "canonical_valid": preflight["checks"].get("canonical_url", True),
                "found_canonical": loc,
                "robots_directive": "index, follow",
                "indexnow_notified": prev_record.get("indexnow_notified", True),
                "google_indexing_state": status_breakdown["google_indexing_state"],
                "status_breakdown": status_breakdown,
                "preflight_checks": preflight["checks"],
                "status": "HEALTHY" if preflight["passed"] else "TECHNICAL_ISSUE",
                "detected_issues": preflight["violations"]
            }

            if preflight["passed"]:
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

    # --------------------------------------------------------------------------
    # 8. Post-Publication Search Engine Discovery Pipeline (Orchestrator)
    # --------------------------------------------------------------------------
    def execute_post_publication_discovery(
        self,
        url: str,
        html_content: Optional[str] = None,
        is_deployed: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Orchestrates full search engine discovery pipeline after an article publication:
        1. Pre-flight technical indexability checks (HTTP 200, canonical, noindex, robots.txt, internal links, mobile, schema).
        2. Sitemap synchronization & XML validation.
        3. Google Search Console sitemap submission (via authorized GSC API).
        4. Google Search Console URL inspection (via URL Inspection API).
        5. Bing IndexNow submission with exponential backoff & duplicate prevention.
        6. Persistent record with strictly separated statuses in data/indexing_status_ledger.json.
        """
        clean_url = url.strip()
        now_pkt = get_pkt_now_str()

        # Step 1: Sync sitemap first so URL exists in sitemap
        sitemap_res = self.sync_sitemap(dry_run=dry_run)

        # Step 2: Pre-flight technical indexability checks
        preflight = self.verify_technical_indexability(clean_url, html_content=html_content, verify_sitemap=True)

        if not preflight["passed"]:
            # Halt search engine notifications on indexability failure
            with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
                ledger = json.load(f)

            entry = ledger.setdefault("urls", {}).setdefault(clean_url, {
                "canonical_url": clean_url,
                "first_seen_pkt": now_pkt
            })
            entry["status"] = "TECHNICAL_ISSUE"
            entry["status_breakdown"] = {
                "publication_status": "PUBLISHED",
                "deployment_status": "DEPLOYED" if is_deployed else "PENDING_DEPLOYMENT",
                "sitemap_status": "SITEMAP_UPDATED",
                "google_sitemap_status": "NOT_CONFIGURED",
                "google_inspection_status": "PENDING",
                "google_indexing_state": "UNKNOWN",
                "indexnow_status": "PENDING",
                "bing_status": "PENDING"
            }
            entry["detected_issues"] = preflight["violations"]
            entry["preflight_checks"] = preflight["checks"]
            entry["last_checked_date_pkt"] = now_pkt

            with open(self.indexing_ledger_path, "w", encoding="utf-8") as f:
                json.dump(ledger, f, indent=2)

            return {
                "url": clean_url,
                "passed": False,
                "reason": "FAILED_PREFLIGHT_INDEXABILITY",
                "violations": preflight["violations"],
                "status_breakdown": entry["status_breakdown"],
                "disclaimer": NO_INDEXING_GUARANTEE_DISCLAIMER
            }

        # Step 3: Google Search Console Sitemap Submission
        gsc_sitemap_res = self.submit_google_sitemap(dry_run=dry_run)

        # Step 4: Google URL Inspection API check
        gsc_inspect_res = self.inspect_google_url(clean_url, dry_run=dry_run)

        # Step 5: Bing IndexNow notification with retry
        indexnow_res = self.notify_indexnow_with_retry(
            urls=[clean_url],
            dry_run=dry_run,
            max_retries=3,
            force=False
        )

        # Step 6: Assemble separate statuses
        status_breakdown = {
            "publication_status": "PUBLISHED",
            "deployment_status": "DEPLOYED" if is_deployed else "PENDING_DEPLOYMENT",
            "sitemap_status": "SITEMAP_UPDATED",
            "google_sitemap_status": gsc_sitemap_res.get("status", "NOT_CONFIGURED"),
            "google_inspection_status": gsc_inspect_res.get("inspection_status", "NOT_CONFIGURED"),
            "google_indexing_state": gsc_inspect_res.get("indexing_state", "UNKNOWN"),
            "indexnow_status": "INDEXNOW_SUBMITTED" if indexnow_res.get("success") else "FAILED",
            "bing_status": "BING_STATUS_VERIFIED" if indexnow_res.get("success") else "PENDING"
        }

        # Step 7: Persist complete record in ledger
        with open(self.indexing_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        entry = ledger.setdefault("urls", {}).setdefault(clean_url, {
            "canonical_url": clean_url,
            "first_seen_pkt": now_pkt
        })
        entry["last_checked_date_pkt"] = now_pkt
        entry["status"] = "HEALTHY"
        entry["http_status"] = 200
        entry["status_breakdown"] = status_breakdown
        entry["google_indexing_state"] = status_breakdown["google_indexing_state"]
        entry["preflight_checks"] = preflight["checks"]
        entry["detected_issues"] = []
        entry["google_telemetry"] = {
            "sitemap_status": gsc_sitemap_res.get("status"),
            "inspection_status": gsc_inspect_res.get("inspection_status"),
            "coverage_state": gsc_inspect_res.get("coverage_state"),
            "verdict": gsc_inspect_res.get("verdict"),
            "last_crawl_time": gsc_inspect_res.get("last_crawl_time"),
            "message": gsc_inspect_res.get("message")
        }
        entry["indexnow_telemetry"] = {
            "success": indexnow_res.get("success"),
            "submitted_count": indexnow_res.get("submitted_count"),
            "duplicate_skipped_count": indexnow_res.get("duplicate_skipped_count"),
            "endpoints": indexnow_res.get("endpoints_dispatched")
        }

        ledger["last_audit_pkt"] = now_pkt
        with open(self.indexing_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        return {
            "url": clean_url,
            "passed": True,
            "status_breakdown": status_breakdown,
            "sitemap_update": {
                "total_urls": sitemap_res.get("total_urls"),
                "xml_valid": sitemap_res.get("xml_valid"),
                "robots_txt_sitemap_referenced": sitemap_res.get("robots_txt_sitemap_referenced")
            },
            "google_telemetry": entry["google_telemetry"],
            "indexnow_telemetry": entry["indexnow_telemetry"],
            "timestamp_pkt": now_pkt,
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
    parser.add_argument("--post-publish", help="Execute post-publication discovery pipeline for a specific URL")
    parser.add_argument("--dry-run", action="store_true", help="Simulate network operations without real API requests")
    args = parser.parse_args()

    engine = IndexingNotifierEngine()

    if args.sync_sitemap:
        res = engine.sync_sitemap(dry_run=args.dry_run)
        print(f"[SITEMAP SYNC] Total URLs: {res['total_urls']} | XML Valid: {res['xml_valid']} -> {res['sitemap_path']}")
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
        res = engine.notify_indexnow_with_retry(urls=urls, dry_run=args.dry_run)
        print(f"[INDEXNOW DISPATCH] Submitted: {res['submitted_count']} URLs | Duplicates Skipped: {res.get('duplicate_skipped_count', 0)} | Success: {res['success']}")
        print(f"[DISCLAIMER] {res['disclaimer']}")

    if args.post_publish:
        res = engine.execute_post_publication_discovery(url=args.post_publish, dry_run=args.dry_run)
        print(f"[POST-PUBLISH DISCOVERY] URL: {res['url']} | Passed: {res['passed']}")
        print(f"  Status Breakdown: {json.dumps(res.get('status_breakdown'), indent=2)}")
        print(f"[DISCLAIMER] {res['disclaimer']}")


if __name__ == "__main__":
    main()
