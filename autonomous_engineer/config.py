import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Domain & Protocols
DOMAIN = "aidigitools.tech"
BASE_URL = f"https://{DOMAIN}"
INDEXNOW_KEY = "89d63ab53a63527b12a199a3096e51ad"
INDEXNOW_KEY_FILE = f"{INDEXNOW_KEY}.txt"
INDEXNOW_URL = f"{BASE_URL}/{INDEXNOW_KEY_FILE}"

# Timezone & Scheduling (Asia/Karachi is UTC+5)
TIMEZONE_NAME = "Asia/Karachi"
TIMEZONE_OFFSET = timedelta(hours=5)
SCHEDULE_HOURS_LOCAL = [8, 20]  # 08:00 PKT and 20:00 PKT
SCHEDULE_HOURS_UTC = [3, 15]    # 03:00 UTC and 15:00 UTC

# File paths
PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parent
REPORTS_DIR = PROJECT_ROOT / "audit_reports"
HISTORY_FILE = REPORTS_DIR / "audit_history.json"

# Quality & SEO Boundaries
TITLE_MIN_LEN = 30
TITLE_MAX_LEN = 65
DESC_MIN_LEN = 70
DESC_MAX_LEN = 165
QUICK_ANSWER_MIN_WORDS = 30
QUICK_ANSWER_MAX_WORDS = 85

# Security & Safety Boundaries
PROTECTED_PATTERNS = [
    "assets/cart.js",        # Payment and checkout logic
    "contact.html",          # Verified phone and WhatsApp contact info
    "policies.html",         # Legal terms, refund & warranty policies
    "affiliate-disclosure.html", # Legal disclosures
]

# Preferred Gemini Models for Cloud Reasoning (Free tier / zero billing)
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
FALLBACK_GEMINI_MODEL = "gemini-2.0-flash"

def get_karachi_time() -> datetime:
    """Returns the current timestamp in Asia/Karachi (UTC+5)."""
    return datetime.now(timezone(TIMEZONE_OFFSET, name=TIMEZONE_NAME))

def get_karachi_timestr() -> str:
    """Returns formatted timestamp string in Asia/Karachi time."""
    return get_karachi_time().strftime("%Y-%m-%d %H:%M:%S PKT")
