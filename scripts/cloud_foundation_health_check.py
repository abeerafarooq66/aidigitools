#!/usr/bin/env python3
"""
AI DigiTools — Cloud Foundation Health Check & Telemetry Suite
Executes live HTTPS reachability, SSL certificate audit, robots.txt, sitemap.xml,
and key route integrity checks. Generates a GitHub Actions Job Summary.
"""

import os
import sys
import ssl
import socket
import datetime
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://aidigitools.tech"
TIMEOUT_SECS = 10
MAX_RETRIES = 2

def get_current_timestamps() -> Tuple[str, str]:
    """Returns formatted timestamps in UTC and Asia/Karachi (PKT)."""
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    pkt_tz = datetime.timezone(datetime.timedelta(hours=5))
    pkt_now = utc_now.astimezone(pkt_tz)
    return utc_now.strftime("%Y-%m-%d %H:%M:%S UTC"), pkt_now.strftime("%Y-%m-%d %H:%M:%S PKT (UTC+5)")

def probe_url(url: str) -> Dict[str, Any]:
    """Probes a URL with retry logic and measures latency."""
    headers = {"User-Agent": "AIDigiTools-Cloud-Foundation/1.0"}
    last_err = ""
    for attempt in range(1, MAX_RETRIES + 1):
        start = datetime.datetime.now()
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECS) as resp:
                latency = round((datetime.datetime.now() - start).total_seconds() * 1000, 2)
                return {
                    "url": url,
                    "status_code": resp.status,
                    "latency_ms": latency,
                    "success": 200 <= resp.status < 400,
                    "error": None
                }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            last_err = str(e)
    
    return {
        "url": url,
        "status_code": 0,
        "latency_ms": 0,
        "success": False,
        "error": last_err
    }

def check_ssl_certificate(hostname: str = "aidigitools.tech") -> Dict[str, Any]:
    """Verifies SSL/TLS certificate validity and expiration."""
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=TIMEOUT_SECS) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = cert.get("notAfter", "")
                expire_dt = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=datetime.timezone.utc)
                now_utc = datetime.datetime.now(datetime.timezone.utc)
                days_left = (expire_dt - now_utc).days
                cipher = ssock.cipher()
                return {
                    "hostname": hostname,
                    "valid": days_left > 0,
                    "days_remaining": days_left,
                    "expires_on": not_after,
                    "cipher": cipher[0] if cipher else "Unknown",
                    "error": None
                }
    except Exception as e:
        return {
            "hostname": hostname,
            "valid": False,
            "days_remaining": 0,
            "expires_on": "Unknown",
            "cipher": "Unknown",
            "error": str(e)
        }

def check_robots_txt() -> Dict[str, Any]:
    """Inspects live robots.txt directives and sitemap linkage."""
    url = f"{BASE_URL}/robots.txt"
    res = probe_url(url)
    if not res["success"]:
        return {"success": False, "details": "Failed to fetch robots.txt", "has_sitemap": False, "status_code": res["status_code"]}
    
    req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-Cloud-Foundation/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECS) as resp:
            content = resp.read().decode("utf-8")
            has_sitemap = "sitemap: https://aidigitools.tech/sitemap.xml" in content.lower()
            allows_all = "user-agent: *" in content.lower()
            return {
                "success": has_sitemap and allows_all,
                "has_sitemap": has_sitemap,
                "allows_all": allows_all,
                "status_code": resp.status,
                "latency_ms": res["latency_ms"],
                "details": "Robots.txt permissive & sitemap declared" if (has_sitemap and allows_all) else "Missing sitemap or user-agent declaration"
            }
    except Exception as e:
        return {"success": False, "details": str(e), "has_sitemap": False, "status_code": 0}

def check_sitemap_xml() -> Dict[str, Any]:
    """Validates live sitemap.xml syntax and url count."""
    url = f"{BASE_URL}/sitemap.xml"
    res = probe_url(url)
    if not res["success"]:
        return {"success": False, "url_count": 0, "details": "Failed to fetch sitemap.xml", "status_code": res["status_code"]}
    
    req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-Cloud-Foundation/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECS) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            count = len(urls)
            is_valid = count >= 60
            return {
                "success": is_valid,
                "url_count": count,
                "status_code": resp.status,
                "latency_ms": res["latency_ms"],
                "details": f"Valid XML with {count} canonical URLs" if is_valid else f"Unexpected URL count: {count}"
            }
    except Exception as e:
        return {"success": False, "url_count": 0, "details": f"XML parse error: {str(e)}", "status_code": 0}

def run_foundation_health_check() -> int:
    """Executes all cloud foundation checks and writes summary."""
    utc_time, pkt_time = get_current_timestamps()
    print("=" * 70)
    print("[AUDIT] AI DIGITOOLS -- CLOUD FOUNDATION HEALTH AUDIT")
    print(f"Timestamp: {pkt_time} | {utc_time}")
    print(f"Target: {BASE_URL}")
    print("=" * 70)

    results: List[Dict[str, Any]] = []

    # 1. Homepage
    hp = probe_url(f"{BASE_URL}/")
    results.append({
        "name": "Live Homepage",
        "target": "/",
        "status": "PASS" if hp["success"] else "FAIL",
        "code": hp["status_code"],
        "latency": f"{hp['latency_ms']} ms",
        "details": "OK" if hp["success"] else hp["error"]
    })

    # 2. SSL Certificate
    ssl_info = check_ssl_certificate("aidigitools.tech")
    results.append({
        "name": "HTTPS SSL Certificate",
        "target": "aidigitools.tech:443",
        "status": "PASS" if ssl_info["valid"] else "FAIL",
        "code": "Valid" if ssl_info["valid"] else "Invalid",
        "latency": "—",
        "details": f"{ssl_info['days_remaining']} days remaining (Expires: {ssl_info['expires_on']})" if ssl_info["valid"] else ssl_info["error"]
    })

    # 3. Robots.txt
    robots = check_robots_txt()
    results.append({
        "name": "Crawler Policy (robots.txt)",
        "target": "/robots.txt",
        "status": "PASS" if robots["success"] else "FAIL",
        "code": robots.get("status_code", "N/A"),
        "latency": f"{robots.get('latency_ms', 0)} ms",
        "details": robots["details"]
    })

    # 4. Sitemap.xml
    sitemap = check_sitemap_xml()
    results.append({
        "name": "Canonical Sitemap (sitemap.xml)",
        "target": "/sitemap.xml",
        "status": "PASS" if sitemap["success"] else "FAIL",
        "code": sitemap.get("status_code", "N/A"),
        "latency": f"{sitemap.get('latency_ms', 0)} ms",
        "details": sitemap["details"]
    })

    # 5. IndexNow Key File
    idx = probe_url(f"{BASE_URL}/89d63ab53a63527b12a199a3096e51ad.txt")
    results.append({
        "name": "IndexNow Key File",
        "target": "/89d63ab53a63527b12a199a3096e51ad.txt",
        "status": "PASS" if idx["success"] else "FAIL",
        "code": idx["status_code"],
        "latency": f"{idx['latency_ms']} ms",
        "details": "200 OK — Active IndexNow Key" if idx["success"] else idx["error"]
    })

    # 6. Key Production Routes
    key_routes = [
        ("Product Route", "/tools/chatgpt-plus.html"),
        ("Category Route", "/categories/coding.html"),
        ("Deals Hub", "/deals.html"),
        ("Contact & WhatsApp", "/contact.html"),
        ("Trust & Policies", "/policies.html"),
    ]
    for label, route in key_routes:
        pr = probe_url(f"{BASE_URL}{route}")
        results.append({
            "name": f"Key Route: {label}",
            "target": route,
            "status": "PASS" if pr["success"] else "FAIL",
            "code": pr["status_code"],
            "latency": f"{pr['latency_ms']} ms",
            "details": "OK" if pr["success"] else pr["error"]
        })

    # Print Console Table
    all_passed = True
    print("\n{:<32} {:<10} {:<10} {:<12} {}".format("CHECK", "STATUS", "HTTP/CODE", "LATENCY", "DETAILS"))
    print("-" * 80)
    for r in results:
        badge = "[PASS]" if r["status"] == "PASS" else "[FAIL]"
        if r["status"] != "PASS":
            all_passed = False
        print("{:<32} {:<10} {:<10} {:<12} {}".format(r["name"][:30], badge, str(r["code"]), r["latency"], r["details"]))

    # Write GitHub Actions Job Summary ($GITHUB_STEP_SUMMARY)
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write("## 🌐 AI DigiTools — Cloud Foundation Health Check\n\n")
                f.write(f"- **Execution Timestamp:** `{pkt_time}` (`{utc_time}`)\n")
                f.write(f"- **Target Domain:** [{BASE_URL}]({BASE_URL})\n")
                f.write(f"- **Overall Status:** {'🟢 **ALL CHECKS PASSED**' if all_passed else '🔴 **HEALTH CHECK FAILED**'}\n\n")
                f.write("| Health Check | Target | Status | HTTP/Code | Latency | Details |\n")
                f.write("| :--- | :--- | :---: | :---: | :---: | :--- |\n")
                for r in results:
                    badge = "✅ PASS" if r["status"] == "PASS" else "❌ FAIL"
                    f.write(f"| **{r['name']}** | `{r['target']}` | {badge} | `{r['code']}` | `{r['latency']}` | {r['details']} |\n")
                f.write("\n---\n")
                f.write("> *Standard Ubuntu Runner (Free Tier) — Zero File Modifications — Zero Secret Leaks.*\n")
        except Exception as e:
            print(f"Warning: Failed to write GITHUB_STEP_SUMMARY: {e}", file=sys.stderr)

    print("\n" + "=" * 70)
    if all_passed:
        print("[SUCCESS] All 10 Cloud Foundation Health Checks PASSED.")
        print("=" * 70)
        return 0
    else:
        print("[FAILURE] One or more Cloud Foundation Health Checks FAILED.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(run_foundation_health_check())
