import os
import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
from .config import BASE_URL

IMPORT_ERROR_MSG = ""
try:
    from google.oauth2 import service_account
    import google.auth.transport.requests
    HAS_GOOGLE_AUTH = True
except Exception as e:
    HAS_GOOGLE_AUTH = False
    IMPORT_ERROR_MSG = str(e)

class GoogleSearchConsoleClient:
    """Official Google Search Console API Client.
    Connects to Google Search Console via Service Account credentials to monitor:
    - Search Analytics: Impressions, clicks, CTR, and search keyword positions
    - Index Coverage & Sitemaps: Verified sitemap status in Google index
    - URL Inspection: Programmatic index coverage and mobile readiness
    """

    API_V3_BASE = "https://www.googleapis.com/webmasters/v3/sites"
    INSPECT_API = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

    def __init__(self, key_json_str: Optional[str] = None, site_url: str = BASE_URL):
        raw_key = key_json_str if key_json_str is not None else os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "").strip()
        self.raw_key = raw_key
        self.site_url = site_url.rstrip("/") + "/"
        self._parsed_key: Optional[Dict[str, Any]] = None
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

        if self.raw_key:
            try:
                self._parsed_key = json.loads(self.raw_key)
            except Exception:
                self._parsed_key = None

    def is_configured(self) -> bool:
        """Checks if a valid Google Service Account JSON key is available."""
        return bool(self._parsed_key and self._parsed_key.get("client_email"))

    def get_client_email(self) -> Optional[str]:
        """Returns the client email of the service account if configured."""
        if self._parsed_key:
            return self._parsed_key.get("client_email")
        return None

    def get_access_token(self) -> Optional[str]:
        """Refreshes and returns an OAuth 2.0 Bearer token using the service account credentials."""
        if not self.is_configured():
            return None

        if not HAS_GOOGLE_AUTH:
            return None

        # Return cached token if valid
        if self._access_token and self._token_expiry and datetime.now(timezone.utc) < self._token_expiry:
            return self._access_token

        try:
            creds = service_account.Credentials.from_service_account_info(
                self._parsed_key,
                scopes=self.SCOPES
            )
            req = google.auth.transport.requests.Request()
            creds.refresh(req)
            self._access_token = creds.token
            self._token_expiry = datetime.now(timezone.utc) + timedelta(minutes=50)
            return self._access_token
        except Exception as e:
            return None

    def _api_post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Executes an authenticated POST request against a Google API endpoint."""
        token = self.get_access_token()
        if not token:
            return {
                "status_code": 0,
                "data": None,
                "error": "Failed to obtain Google OAuth access token. Ensure google-auth is installed and key is valid."
            }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "AIDigiTools-Autonomous-Engineer/1.0"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
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

    def _api_get(self, url: str) -> Dict[str, Any]:
        """Executes an authenticated GET request against a Google API endpoint."""
        token = self.get_access_token()
        if not token:
            return {
                "status_code": 0,
                "data": None,
                "error": "Failed to obtain Google OAuth access token."
            }

        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": "AIDigiTools-Autonomous-Engineer/1.0"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
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

    def get_search_analytics(self, days: int = 28) -> Dict[str, Any]:
        """Queries Google Search Analytics for total clicks, impressions, and top keywords."""
        if not self.is_configured():
            return {"status_code": 0, "data": None, "error": "GSC_SERVICE_ACCOUNT_KEY not configured"}

        end_date = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d")
        start_date = (datetime.now(timezone.utc) - timedelta(days=days + 2)).strftime("%Y-%m-%d")

        payload = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["query"],
            "rowLimit": 10
        }

        # Try URL-prefix format first, then domain property if needed
        encoded_site = urllib.parse.quote_plus(self.site_url)
        url = f"{self.API_V3_BASE}/{encoded_site}/searchAnalytics/query"
        res = self._api_post(url, payload)

        if res.get("status_code") == 403 or res.get("status_code") == 404:
            # Fallback to domain property identifier
            netloc = urllib.parse.urlparse(self.site_url).netloc
            domain_site = f"sc-domain:{netloc}"
            fallback_url = f"{self.API_V3_BASE}/{urllib.parse.quote_plus(domain_site)}/searchAnalytics/query"
            fallback_res = self._api_post(fallback_url, payload)
            if fallback_res.get("status_code") == 200:
                return fallback_res

        return res

    def get_sitemaps(self) -> Dict[str, Any]:
        """Queries Google Search Console for registered sitemap status and indexing health."""
        if not self.is_configured():
            return {"status_code": 0, "data": None, "error": "GSC_SERVICE_ACCOUNT_KEY not configured"}

        encoded_site = urllib.parse.quote_plus(self.site_url)
        url = f"{self.API_V3_BASE}/{encoded_site}/sitemaps"
        return self._api_get(url)

    def run_gsc_audit(self) -> Dict[str, Any]:
        """Executes a complete Google Search Console telemetry check."""
        if not self.is_configured():
            return {
                "connected": False,
                "status": "UNCONFIGURED",
                "message": "GSC_SERVICE_ACCOUNT_KEY secret not set in GitHub Actions.",
                "client_email": None,
                "analytics": None,
                "sitemaps": None
            }

        client_email = self.get_client_email()

        if not HAS_GOOGLE_AUTH:
            return {
                "connected": False,
                "status": "DEPENDENCY_NOTICE",
                "message": f"google-auth/requests library notice ({IMPORT_ERROR_MSG}).",
                "client_email": client_email,
                "analytics": None,
                "sitemaps": None
            }

        token = self.get_access_token()
        if not token:
            return {
                "connected": False,
                "status": "TOKEN_ERROR",
                "message": "Failed to exchange service account JSON key for Google OAuth Bearer token.",
                "client_email": client_email,
                "analytics": None,
                "sitemaps": None
            }

        analytics_res = self.get_search_analytics(days=28)
        sitemaps_res = self.get_sitemaps()

        is_connected = (analytics_res.get("status_code") == 200 or sitemaps_res.get("status_code") == 200)

        if is_connected:
            return {
                "connected": True,
                "status": "ACTIVE",
                "message": "Connected to official Google Search Console API.",
                "client_email": client_email,
                "analytics": analytics_res.get("data"),
                "sitemaps": sitemaps_res.get("data")
            }
        else:
            primary_err = analytics_res.get("error") or sitemaps_res.get("error")
            return {
                "connected": False,
                "status": "PERMISSION_NOTICE",
                "message": f"Service account authenticated, but property permission notice: {primary_err}",
                "client_email": client_email,
                "analytics": None,
                "sitemaps": None
            }
