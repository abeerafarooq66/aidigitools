import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional, List
from .config import BASE_URL

class BingWebmasterClient:
    """Official Microsoft Bing Webmaster Tools JSON/HTTP API Client.
    Provides complete programmatic access to Bing Webmaster Tools features:
    - URL Submission Quotas (GetUrlSubmissionQuota)
    - Crawl Statistics & Robots.txt blocks (GetCrawlStats)
    - Technical Crawl Issues & Errors (GetCrawlIssues)
    - Search Performance & Queries (GetQueryStats)
    - Rank & Organic Traffic (GetRankAndTrafficStats)
    - Keyword Statistics (GetKeywordStats)
    - Sitemaps & Feeds Management (GetFeeds, SubmitFeed)
    - Direct URL Submission & Batch Submissions (SubmitUrl, SubmitUrlbatch)
    """

    API_BASE = "https://ssl.bing.com/webmaster/api.svc/json"

    def __init__(self, api_key: Optional[str] = None, site_url: str = BASE_URL):
        self.api_key = api_key if api_key is not None else os.environ.get("BING_API_KEY", "").strip()
        self.site_url = site_url

    def is_configured(self) -> bool:
        """Checks if Bing Webmaster API key is present."""
        return bool(self.api_key and len(self.api_key) > 5)

    def _api_get(self, endpoint: str, extra_params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Executes an authenticated GET request against the Bing Webmaster JSON API."""
        if not self.is_configured():
            return {"status_code": 0, "data": None, "error": "BING_API_KEY not configured"}

        params = f"siteUrl={urllib.parse.quote_plus(self.site_url)}&apikey={urllib.parse.quote_plus(self.api_key)}"
        if extra_params:
            for k, v in extra_params.items():
                params += f"&{k}={urllib.parse.quote_plus(str(v))}"

        url = f"{self.API_BASE}/{endpoint}?{params}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AIDigiTools-Autonomous-Engineer/1.0",
                "Content-Type": "application/json; charset=utf-8"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"status_code": resp.status, "data": data.get("d", data), "error": None}
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            return {"status_code": e.code, "data": None, "error": f"HTTP {e.code}: {e.reason} {err_body}".strip()}
        except Exception as e:
            return {"status_code": 0, "data": None, "error": f"Network exception: {str(e)}"}

    def _api_post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes an authenticated POST request against the Bing Webmaster JSON API."""
        if not self.is_configured():
            return {"status_code": 0, "data": None, "error": "BING_API_KEY not configured"}

        url = f"{self.API_BASE}/{endpoint}?apikey={urllib.parse.quote_plus(self.api_key)}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "User-Agent": "AIDigiTools-Autonomous-Engineer/1.0",
                "Content-Type": "application/json; charset=utf-8"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw) if raw else {}
                return {"status_code": resp.status, "data": data.get("d", data), "error": None}
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            return {"status_code": e.code, "data": None, "error": f"HTTP {e.code}: {e.reason} {err_body}".strip()}
        except Exception as e:
            return {"status_code": 0, "data": None, "error": f"Network exception: {str(e)}"}

    def get_url_submission_quota(self) -> Dict[str, Any]:
        """Retrieves remaining daily & monthly URL submission quota for aidigitools.tech on Bing."""
        return self._api_get("GetUrlSubmissionQuota")

    def get_crawl_stats(self) -> Dict[str, Any]:
        """Retrieves official Bingbot crawl metrics (pages crawled, in index, status codes, robots.txt blocks)."""
        return self._api_get("GetCrawlStats")

    def get_crawl_issues(self) -> Dict[str, Any]:
        """Retrieves specific technical crawl issues and errors encountered by Bingbot."""
        return self._api_get("GetCrawlIssues")

    def get_query_stats(self) -> Dict[str, Any]:
        """Retrieves search query clicks, impressions, and click/impression positions from Bing Search."""
        return self._api_get("GetQueryStats")

    def get_rank_and_traffic_stats(self) -> Dict[str, Any]:
        """Retrieves rank and organic search traffic trends from Bing."""
        return self._api_get("GetRankAndTrafficStats")

    def get_keyword_stats(self, query: str = "") -> Dict[str, Any]:
        """Retrieves keyword research metrics from Bing organic search data."""
        extra = {"q": query} if query else None
        return self._api_get("GetKeywordStats", extra_params=extra)

    def get_feeds(self) -> Dict[str, Any]:
        """Retrieves list of sitemaps and feeds registered in Bing Webmaster Tools."""
        return self._api_get("GetFeeds")

    def submit_feed(self, feed_url: str = f"{BASE_URL}/sitemap.xml") -> Dict[str, Any]:
        """Programmatically submits an XML sitemap or feed directly to Bing."""
        return self._api_post("SubmitFeed", {
            "siteUrl": self.site_url,
            "feedUrl": feed_url
        })

    def submit_url(self, url: str) -> Dict[str, Any]:
        """Submits an individual URL to Bing for instant crawling and indexation."""
        return self._api_post("SubmitUrl", {
            "siteUrl": self.site_url,
            "url": url
        })

    def submit_url_batch(self, urls: List[str]) -> Dict[str, Any]:
        """Submits a batch of URLs to Bing for instant crawling and indexation."""
        return self._api_post("SubmitUrlbatch", {
            "siteUrl": self.site_url,
            "urlList": urls
        })

    def sync_sitemap(self, sitemap_url: str = f"{BASE_URL}/sitemap.xml") -> Dict[str, Any]:
        """Verifies if sitemap is registered with Bing; submits it automatically if missing."""
        feeds_res = self.get_feeds()
        if feeds_res.get("status_code") == 200:
            feeds = feeds_res.get("data") or []
            existing_urls = []
            if isinstance(feeds, list):
                existing_urls = [f.get("Url", "") for f in feeds if isinstance(f, dict)]
            if sitemap_url not in existing_urls:
                sub_res = self.submit_feed(sitemap_url)
                return {"synced": True, "submitted_new": True, "details": sub_res}
            return {"synced": True, "submitted_new": False, "details": "Sitemap already registered"}
        return {"synced": False, "submitted_new": False, "details": feeds_res.get("error")}

    def run_bing_audit(self) -> Dict[str, Any]:
        """Compiles a complete audit report of Bing Webmaster connectivity and telemetry."""
        if not self.is_configured():
            return {
                "connected": False,
                "status": "UNCONFIGURED",
                "message": "BING_API_KEY secret not set. The agent is ready to connect once the key is added in GitHub Secrets.",
                "quota": None,
                "crawl_stats": None,
                "query_stats": None,
                "feeds": None,
                "crawl_issues": None,
                "sitemap_synced": False
            }

        quota_res = self.get_url_submission_quota()
        crawl_res = self.get_crawl_stats()
        query_res = self.get_query_stats()
        feeds_res = self.get_feeds()
        issues_res = self.get_crawl_issues()

        is_connected = any(
            r.get("status_code") == 200 for r in [quota_res, crawl_res, feeds_res, query_res]
        )

        sitemap_synced = False
        if is_connected:
            sync_res = self.sync_sitemap()
            sitemap_synced = sync_res.get("synced", False)

        primary_err = quota_res.get("error") or crawl_res.get("error") or feeds_res.get("error")

        return {
            "connected": is_connected,
            "status": "ACTIVE" if is_connected else "AUTHENTICATION_NOTICE",
            "message": "Connected to official Bing Webmaster Tools API." if is_connected else f"Bing API authentication notice: {primary_err}",
            "quota": quota_res.get("data"),
            "crawl_stats": crawl_res.get("data"),
            "query_stats": query_res.get("data"),
            "feeds": feeds_res.get("data"),
            "crawl_issues": issues_res.get("data"),
            "quota_error": quota_res.get("error"),
            "crawl_error": crawl_res.get("error"),
            "sitemap_synced": sitemap_synced
        }
