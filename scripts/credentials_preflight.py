import os
import sys
import json
import re
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Helper: Simple .env parser without external dependencies
def load_env_file(env_path: Path):
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip("'\"")
            if k and k not in os.environ:
                os.environ[k] = v

# Load .env if present
load_env_file(ROOT_DIR / ".env")

STATUS_SET = "SET"
STATUS_MISSING = "MISSING"
STATUS_INVALID = "INVALID FORMAT"
STATUS_FAILED = "CONNECTION FAILED"
STATUS_VERIFIED = "VERIFIED"
STATUS_OPTIONAL = "OPTIONAL / NOT CONFIGURED"
STATUS_PENDING = "PENDING USER ACTION"

def sanitize_value(val: str) -> bool:
    """Returns True if value is set and not a template placeholder."""
    if not val:
        return False
    v = val.strip().lower()
    placeholders = [
        "your_", "example", "placeholder", "xxx", "123456789012",
        "projects/123456789012", "content-agent-sa@aidigitools-content-agent"
    ]
    return not any(p in v for p in placeholders)

def check_indexnow(test_live=False):
    key = os.environ.get("INDEXNOW_KEY", "89d63ab53a63527b12a199a3096e51ad").strip()
    if not key:
        return STATUS_MISSING, "Key not defined"
    if not re.match(r"^[0-9a-f]{32}$", key, re.I):
        return STATUS_INVALID, "Key must be 32-character hexadecimal"
    
    key_file = ROOT_DIR / f"{key}.txt"
    if not key_file.exists():
        return STATUS_FAILED, f"Local public key file {key}.txt missing in root"
    
    if test_live:
        url = f"https://aidigitools.tech/{key}.txt"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-Preflight/1.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                content = resp.read().decode("utf-8").strip()
                if content == key:
                    return STATUS_VERIFIED, "Live HTTPS file verified and matching key"
                else:
                    return STATUS_FAILED, "Live HTTPS file content mismatch"
        except Exception as e:
            return STATUS_FAILED, f"Could not verify live HTTPS file: {e}"
            
    return STATUS_SET, "Local file present and format valid"

def check_bing(test_live=False):
    key = (os.environ.get("BING_WEBMASTER_API_KEY") or os.environ.get("BING_API_KEY") or "").strip()
    if not key:
        return STATUS_MISSING, "BING_WEBMASTER_API_KEY is not set"
    if len(key) < 20 or not re.match(r"^[0-9a-zA-Z]+$", key):
        return STATUS_INVALID, "Invalid API key length/format"
        
    if test_live:
        url = f"https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl=https://aidigitools.tech&apikey={urllib.parse.quote_plus(key)}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-Preflight/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    d = data.get("d", {})
                    daily = d.get("DailyQuota", "N/A")
                    return STATUS_VERIFIED, f"Authenticated HTTP 200 OK (Daily quota: {daily})"
                return STATUS_FAILED, f"HTTP Status: {resp.status}"
        except urllib.error.HTTPError as e:
            return STATUS_FAILED, f"HTTP Error {e.code}: {e.reason}"
        except Exception as e:
            return STATUS_FAILED, f"Connection error: {e}"
            
    return STATUS_SET, "Key present and format valid"

def check_pagespeed(test_live=False):
    key = os.environ.get("PAGESPEED_API_KEY", "").strip()
    if not key:
        return STATUS_MISSING, "PAGESPEED_API_KEY is not set"
    if len(key) < 25 or not key.startswith("AIza"):
        return STATUS_INVALID, "Invalid Google API key format (expected AIza...)"
        
    if test_live:
        url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://aidigitools.tech&key={urllib.parse.quote_plus(key)}&strategy=mobile&category=performance"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-Preflight/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status == 200:
                    return STATUS_VERIFIED, "PageSpeed Insights API returned valid Lighthouse performance payload"
                return STATUS_FAILED, f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            return STATUS_FAILED, f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            return STATUS_FAILED, f"Connection error: {e}"
            
    return STATUS_SET, "Key present and format valid"

def check_crux(test_live=False):
    key = (os.environ.get("CRUX_API_KEY") or os.environ.get("PAGESPEED_API_KEY") or "").strip()
    if not key:
        return STATUS_MISSING, "CRUX_API_KEY is not set"
    if len(key) < 25 or not key.startswith("AIza"):
        return STATUS_INVALID, "Invalid Google API key format (expected AIza...)"
        
    if test_live:
        url = f"https://chromeuxreport.googleapis.com/v1/records:queryRecord?key={urllib.parse.quote_plus(key)}"
        payload = json.dumps({"origin": "https://aidigitools.tech"}).encode("utf-8")
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return STATUS_VERIFIED, "CrUX API returned genuine origin record"
                return STATUS_FAILED, f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            # 404 is standard in CrUX when origin has insufficient traffic density in the last 28 days
            if e.code == 404:
                return STATUS_VERIFIED, "API authenticated; Origin has insufficient traffic density for CrUX (reported as unavailable, not zero)"
            return STATUS_FAILED, f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            return STATUS_FAILED, f"Connection error: {e}"
            
    return STATUS_SET, "Key present and format valid"

def check_gemini(test_live=False):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return STATUS_MISSING, "GEMINI_API_KEY is not set"
    if len(key) < 25 or not key.startswith("AIza"):
        return STATUS_INVALID, "Invalid Google AI API key format"
        
    if test_live:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={urllib.parse.quote_plus(key)}"
        try:
            req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    models = [m.get("name") for m in data.get("models", [])]
                    return STATUS_VERIFIED, f"API authenticated ({len(models)} models discovered)"
                return STATUS_FAILED, f"HTTP {resp.status}"
        except urllib.error.HTTPError as e:
            return STATUS_FAILED, f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            return STATUS_FAILED, f"Connection error: {e}"
            
    return STATUS_SET, "Key present and format valid"

def check_gsc(test_live=False):
    key = os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "").strip()
    if not key:
        return STATUS_MISSING, "GSC_SERVICE_ACCOUNT_KEY is not set"
        
    try:
        data = json.loads(key)
        client_email = data.get("client_email", "")
        if not client_email:
            return STATUS_INVALID, "Service account JSON missing 'client_email'"
    except Exception:
        # Check if it's a file path
        if os.path.exists(key):
            try:
                data = json.load(open(key))
                client_email = data.get("client_email", "")
                if not client_email:
                    return STATUS_INVALID, "Service account JSON file missing 'client_email'"
            except Exception:
                return STATUS_INVALID, "Invalid JSON in service account key file"
        else:
            return STATUS_INVALID, "Key is neither valid JSON string nor existing file path"

    if test_live:
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests
            scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
            if os.path.exists(key):
                creds = service_account.Credentials.from_service_account_file(key, scopes=scopes)
            else:
                creds = service_account.Credentials.from_service_account_info(data, scopes=scopes)
            
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            token = creds.token
            
            # List sites
            url = "https://www.googleapis.com/webmasters/v3/sites"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                sites_data = json.loads(resp.read().decode("utf-8"))
                site_entries = sites_data.get("siteEntry", [])
                target_found = any(s.get("siteUrl", "").rstrip("/") == "https://aidigitools.tech" for s in site_entries)
                if target_found:
                    return STATUS_VERIFIED, f"Service Account verified. Property https://aidigitools.tech/ accessible."
                else:
                    return STATUS_PENDING, f"Service Account authenticated ({client_email}), but https://aidigitools.tech/ is not yet added in Search Console Users."
        except ImportError:
            return STATUS_FAILED, "google-auth package not installed locally"
        except Exception as e:
            return STATUS_FAILED, f"Search Console API error: {e}"
            
    return STATUS_SET, f"Service Account configured ({client_email})"

def check_ga4(test_live=False):
    prop_id = os.environ.get("GA4_PROPERTY_ID", "").strip()
    if not prop_id:
        return STATUS_MISSING, "GA4_PROPERTY_ID is not set"
    if not re.match(r"^\d{6,12}$", prop_id):
        return STATUS_INVALID, "GA4_PROPERTY_ID must be a numeric ID (e.g. 123456789), not G-XXXXXX"
    return STATUS_SET, f"Numeric GA4 Property ID defined"

def check_google_ads():
    cid = os.environ.get("GOOGLE_ADS_CUSTOMER_ID", "").strip()
    if not cid:
        return STATUS_OPTIONAL, "Google Ads API access is currently PENDING/OPTIONAL (Developer token model sunset in Sept 2026)"
    return STATUS_SET, "Google Ads Customer ID defined"

def check_google_trends():
    return STATUS_OPTIONAL, "Google Trends API is in private alpha (PENDING APPROVAL; using legitimate fallback)"

def run_preflight(test_live=False):
    print("=" * 70)
    print("AIDigiTools Autonomous SEO Agent V2 — Credential Preflight Verification")
    print("=" * 70)
    print(f"Mode: {'Full Live Authenticated Probing (--test)' if test_live else 'Static Syntax & Presence Verification'}")
    print("-" * 70)
    
    checks = [
        ("IndexNow Protocol", check_indexnow(test_live)),
        ("Bing Webmaster API", check_bing(test_live)),
        ("PageSpeed Insights API", check_pagespeed(test_live)),
        ("Chrome UX Report (CrUX) API", check_crux(test_live)),
        ("Google Gemini API", check_gemini(test_live)),
        ("Google Search Console API", check_gsc(test_live)),
        ("Google Analytics 4 Data API", check_ga4(test_live)),
        ("Google Ads API (Keyword Planner)", check_google_ads()),
        ("Google Trends API (Private Alpha)", check_google_trends()),
    ]
    
    for name, (status, detail) in checks:
        badge = f"[{status}]"
        print(f"{badge:<24} | {name:<30} | {detail}")
        
    print("=" * 70)
    print("Note: Secret values are never displayed or stored in logs.")
    print("=" * 70)

if __name__ == "__main__":
    test_mode = "--test" in sys.argv
    run_preflight(test_live=test_mode)
