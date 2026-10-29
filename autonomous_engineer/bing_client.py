import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from .config import BASE_URL

class BingWebmasterClient:
    """Official Microsoft Bing Webmaster Tools API Client.
    Connects to Bing to retrieve live crawl statistics, URL submission quotas, and search performance.
    """

    API_BASE = "https://ssl.bing.com/webmaster/api.json"

    def __init__(self, api_key: Optional[str] = None, site_url: str = BASE_URL):
        self.api_key = api_key or os.environ.get("BING_API_KEY", "").strip()
        self.site_url = site_url

    def is_configured(self) -> bool:
        """Checks if Bing Webmaster API key is present."""
        return bool(self.api_key)

    def _api_get(self, endpoint: str, extra_params: Dict[str, str] = None) -> Dict[str, Any]:
        """Executes an authenticated GET request against the Bing Webmaster JSON API."""
        if not self.is_configured():
            return {"error": "BING_API_KEY not configured"}

        params = f"siteUrl={urllib.parse.quote_plus(self.site_url)}&apiKey={self.api_key}"
        if extra_params:
            for k, v in extra_params.items():
                params += f"&{k}={urllib.parse.quote_plus(str(v))}"

        url = f"{self.API_BASE}/{endpoint}?{params}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AIDigiTools-Autonomous-Engineer/1.0"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"status_code": resp.status, "data": data.get("d", data), "error": None}
        except urllib.error.HTTPError as e:
            return {"status_code": e.code, "data": None, "error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"status_code": 0, "data": None, "error": f"Network exception: {str(e)}"}

    def get_url_submission_quota(self) -> Dict[str, Any]:
        """Retrieves remaining daily URL submission quota for aidigitools.tech on Bing."""
        return self._api_get("GetUrlSubmissionQuota")

    def get_crawl_stats(self) -> Dict[str, Any]:
        """Retrieves official Bingbot crawl metrics (pages crawled, crawl errors)."""
        return self._api_get("GetCrawlStats")

    def get_query_stats(self) -> Dict[str, Any]:
        """Retrieves search query clicks and impressions from Bing."""
        return self._api_get("GetQueryStats")

    def run_bing_audit(self) -> Dict[str, Any]:
        """Compiles a complete audit report of Bing Webmaster connectivity and telemetry."""
        if not self.is_configured():
            return {
                "connected": False,
                "status": "UNCONFIGURED",
                "message": "BING_API_KEY secret not set. The agent is ready to connect once the key is added in GitHub Secrets.",
                "quota": None,
                "crawl_stats": None,
                "query_stats": None
            }

        quota_res = self.get_url_submission_quota()
        crawl_res = self.get_crawl_stats()
        query_res = self.get_query_stats()

        is_connected = (quota_res.get("status_code") == 200 or crawl_res.get("status_code") == 200)

        return {
            "connected": is_connected,
            "status": "ACTIVE" if is_connected else "AUTHENTICATION_NOTICE",
            "quota": quota_res.get("data"),
            "crawl_stats": crawl_res.get("data"),
            "query_stats": query_res.get("data"),
            "quota_error": quota_res.get("error"),
            "crawl_error": crawl_res.get("error")
        }
