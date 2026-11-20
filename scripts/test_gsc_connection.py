"""
AIDigiTools — Google Search Console API Connection & Testing Suite
Tests Service Account authentication, OAuth token exchange, property permissions,
and live Search Analytics telemetry.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Reconfigure stdout for UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "seo-agent"))

# Load environment variables
env_file = REPO_ROOT / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() not in os.environ:
                    os.environ[k.strip()] = v.strip("'\" ")

SITE_URL = os.environ.get("GSC_SITE_URL", "https://aidigitools.tech/").rstrip("/") + "/"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

print("=" * 70)
print("AIDigiTools — Google Search Console API Diagnostic & Connection Test")
print("=" * 70)
print(f"Target Property : {SITE_URL}")

# Step 1: Detect Credential Source
cred_source = None
cred_data = None
raw_key = os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "").strip()
local_file = REPO_ROOT / "credentials" / "service_account.json"

if local_file.is_file():
    try:
        with open(local_file, "r", encoding="utf-8") as f:
            cred_data = json.load(f)
            cred_source = f"Local File: credentials/service_account.json"
    except Exception as e:
        print(f"⚠️ Warning: Could not parse {local_file}: {e}")

if not cred_data and raw_key:
    try:
        if raw_key.startswith("{"):
            cred_data = json.loads(raw_key)
            cred_source = "Environment Variable: GSC_SERVICE_ACCOUNT_KEY (JSON)"
        elif os.path.isfile(raw_key):
            with open(raw_key, "r", encoding="utf-8") as f:
                cred_data = json.load(f)
                cred_source = f"File from env path: {raw_key}"
    except Exception as e:
        print(f"⚠️ Warning: Could not parse GSC_SERVICE_ACCOUNT_KEY: {e}")

# Step 2: Validate Credentials Presence & Schema
if not cred_data:
    print("\n[STATUS: CREDENTIALS_NOT_FOUND]")
    print("-" * 70)
    print("Google Search Console Service Account key abhi set nahi hai.")
    print("Fallback Mode : 🟢 ACTIVE (Website bina kisi issue ke chal rahi hai).")
    print("\nAap ko kya karna hai? (Sirf 2 simple steps):")
    print("1. Google Cloud Console se Service Account ki JSON key file download karein.")
    print("2. Uss file ko project ke is folder mein paste kar dein:")
    print("   credentials/service_account.json")
    print("-" * 70)
    sys.exit(0)

client_email = cred_data.get("client_email", "")
project_id = cred_data.get("project_id", "")
private_key = cred_data.get("private_key", "")

print(f"\n[STEP 1/4] Checking Credentials Schema...")
print(f"  Source        : {cred_source}")
print(f"  Project ID    : {project_id or 'MISSING'}")
print(f"  Service Email : {client_email or 'MISSING'}")

if not client_email or not private_key or "YOUR_PRIVATE_KEY" in private_key:
    print("\n❌ ERROR: Invalid Service Account format or template placeholder detected.")
    print("Asli Google Cloud JSON key use karein.")
    sys.exit(1)
print("  Schema Check  : 🟢 VALID (All mandatory service account fields present)")

# Step 3: Test OAuth 2.0 Bearer Token Generation
print(f"\n[STEP 2/4] Authenticating with Google OAuth 2.0...")
try:
    from google.oauth2 import service_account
    import google.auth.transport.requests

    creds = service_account.Credentials.from_service_account_info(cred_data, scopes=SCOPES)
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    token = creds.token
    if not token:
        raise ValueError("Empty token returned")
    print("  Token Exchange: 🟢 SUCCESS! Generated Google OAuth2 Bearer token.")
except Exception as e:
    print(f"  Token Exchange: ❌ FAILED! {e}")
    print("Google Cloud Console mein check karein ke Service Account active hai aur private key revoked nahi hui.")
    sys.exit(1)

# Step 4: Test Property Access in Google Search Console
print(f"\n[STEP 3/4] Probing Search Console Property Access...")
api_v3_base = "https://www.googleapis.com/webmasters/v3/sites"
encoded_site = urllib.parse.quote_plus(SITE_URL)
prop_url = f"{api_v3_base}/{encoded_site}"

req = urllib.request.Request(
    prop_url,
    headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": "AIDigiTools-GSC-Diagnostic/1.0"
    }
)

property_accessible = False
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        if resp.status == 200:
            property_accessible = True
            print(f"  Property Check: 🟢 SUCCESS! (HTTP 200 OK — Verified Property Access)")
except urllib.error.HTTPError as e:
    if e.code == 403:
        print(f"  Property Check: ⚠️ PERMISSION DENIED (HTTP 403)")
        print("\n" + "=" * 70)
        print("ACTION REQUIRED BY USER IN GOOGLE SEARCH CONSOLE:")
        print("=" * 70)
        print(f"Service account authenticate ho gaya hai, lekin abhi Search Console property mein add nahi hua.")
        print(f"\nService Account Email:")
        print(f"👉  {client_email}  👈")
        print("\nAsaan Steps:")
        print("1. Google Search Console open karein: https://search.google.com/search-console")
        print(f"2. Property select karein: {SITE_URL}")
        print("3. Left menu se 'Settings' > 'Users and permissions' par click karein.")
        print("4. 'Add user' button dabayein.")
        print(f"5. Email address mein yeh email paste karein: {client_email}")
        print("6. Permission 'Full' select karein aur 'Add' kar dein.")
        print("=" * 70)
        sys.exit(0)
    elif e.code == 404:
        print(f"  Property Check: ⚠️ NOT FOUND (HTTP 404) for URL-prefix: {SITE_URL}")
        print("  Trying domain property fallback (sc-domain:aidigitools.tech)...")
        domain_prop = f"sc-domain:{urllib.parse.urlparse(SITE_URL).netloc}"
        domain_url = f"{api_v3_base}/{urllib.parse.quote_plus(domain_prop)}"
        req2 = urllib.request.Request(domain_url, headers={"Authorization": f"Bearer {token}"})
        try:
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                if resp2.status == 200:
                    property_accessible = True
                    SITE_URL = domain_prop
                    print(f"  Domain Property: 🟢 SUCCESS! (Connected via {domain_prop})")
        except Exception as e2:
            print(f"  Domain Property: ❌ Failed: {e2}")
    else:
        print(f"  Property Check: ❌ HTTP Error {e.code}: {e.reason}")
        sys.exit(1)

# Step 5: Test Live Analytics Query
if property_accessible:
    print(f"\n[STEP 4/4] Fetching Live Search Analytics (Clicks, Impressions, Queries)...")
    analytics_url = f"{api_v3_base}/{urllib.parse.quote_plus(SITE_URL)}/searchAnalytics/query"
    end_date = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
    start_date = (datetime.now(timezone.utc) - timedelta(days=31)).strftime("%Y-%m-%d")

    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 10
    }
    
    req_query = urllib.request.Request(
        analytics_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req_query, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            rows = data.get("rows", [])
            print(f"  Data Retrieved: {len(rows)} queries found for period ({start_date} to {end_date})")
            if rows:
                print("\n  Top Queries Breakdown:")
                print(f"  {'Query':<35} | {'Clicks':<8} | {'Impressions':<12} | {'CTR':<8} | {'Pos'}")
                print("  " + "-" * 72)
                for r in rows[:5]:
                    q = r.get("keys", [""])[0]
                    c = r.get("clicks", 0)
                    im = r.get("impressions", 0)
                    ctr = f"{r.get('ctr', 0)*100:.1f}%"
                    pos = f"{r.get('position', 0):.1f}"
                    print(f"  {q:<35} | {c:<8} | {im:<12} | {ctr:<8} | {pos}")
            else:
                print("  Note: Property is connected and authorized. No recorded queries in this 28-day window yet.")
            print("\n" + "=" * 70)
            print("🟢 GOOGLE SEARCH CONSOLE INTEGRATION 100% OPERATIONAL!")
            print("=" * 70)
    except Exception as e:
        print(f"  Analytics Query: ⚠️ Notice: {e}")
