import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, Any, Optional
from .config import BASE_URL

class PageSpeedInsightsClient:
    """Official Google PageSpeed Insights API Client.
    Connects to Google's PageSpeed service to evaluate live Core Web Vitals and Lighthouse metrics:
    - Performance Score (0-100)
    - Accessibility Score (0-100)
    - Best Practices Score (0-100)
    - SEO Score (0-100)
    - Core Web Vitals: LCP, CLS, FCP, TBT, Speed Index
    """

    API_BASE = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def __init__(self, api_key: Optional[str] = None, site_url: str = BASE_URL):
        self.api_key = api_key if api_key is not None else os.environ.get("PAGESPEED_API_KEY", "").strip()
        self.site_url = site_url

    def is_configured(self) -> bool:
        """Checks if PageSpeed API key is present."""
        return bool(self.api_key and len(self.api_key) > 5)

    def audit_url(self, target_url: str = BASE_URL, strategy: str = "mobile") -> Dict[str, Any]:
        """Calls Google PageSpeed Insights API for a specific URL and strategy (mobile/desktop)."""
        if not self.is_configured():
            return {
                "status_code": 0,
                "data": None,
                "error": "PAGESPEED_API_KEY not configured"
            }

        params = (
            f"url={urllib.parse.quote_plus(target_url)}"
            f"&key={urllib.parse.quote_plus(self.api_key)}"
            f"&strategy={urllib.parse.quote_plus(strategy)}"
            "&category=performance"
            "&category=accessibility"
            "&category=best-practices"
            "&category=seo"
        )
        api_url = f"{self.API_BASE}?{params}"

        req = urllib.request.Request(
            api_url,
            headers={
                "User-Agent": "AIDigiTools-Autonomous-Engineer/1.0",
                "Accept": "application/json"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"status_code": resp.status, "data": data, "error": None}
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            return {"status_code": e.code, "data": None, "error": f"HTTP {e.code}: {e.reason} {err_body}".strip()}
        except Exception as e:
            return {"status_code": 0, "data": None, "error": f"Network exception: {str(e)}"}

    def run_pagespeed_audit(self, target_url: str = BASE_URL) -> Dict[str, Any]:
        """Compiles a complete structured summary of Google PageSpeed Insights performance."""
        if not self.is_configured():
            return {
                "connected": False,
                "status": "UNCONFIGURED",
                "message": "PAGESPEED_API_KEY secret not set in GitHub Actions.",
                "scores": None,
                "metrics": None
            }

        res = self.audit_url(target_url=target_url, strategy="mobile")
        if res.get("status_code") != 200 or not res.get("data"):
            return {
                "connected": False,
                "status": "API_NOTICE",
                "message": f"PageSpeed API notice: {res.get('error')}",
                "scores": None,
                "metrics": None
            }

        data = res.get("data", {})
        lighthouse = data.get("lighthouseResult", {})
        categories = lighthouse.get("categories", {})
        audits = lighthouse.get("audits", {})

        scores = {
            "performance": int((categories.get("performance", {}).get("score") or 0) * 100),
            "accessibility": int((categories.get("accessibility", {}).get("score") or 0) * 100),
            "best_practices": int((categories.get("best-practices", {}).get("score") or 0) * 100),
            "seo": int((categories.get("seo", {}).get("score") or 0) * 100),
        }

        metrics = {
            "largest_contentful_paint": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
            "cumulative_layout_shift": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
            "first_contentful_paint": audits.get("first-contentful-paint", {}).get("displayValue", "N/A"),
            "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue", "N/A"),
            "speed_index": audits.get("speed-index", {}).get("displayValue", "N/A"),
        }

        return {
            "connected": True,
            "status": "ACTIVE",
            "message": "Successfully retrieved live Google PageSpeed & Core Web Vitals telemetry.",
            "scores": scores,
            "metrics": metrics
        }
