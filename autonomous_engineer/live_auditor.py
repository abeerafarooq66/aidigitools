import time
import ssl
import urllib.request
import urllib.error
from typing import Dict, Any, List
from .config import BASE_URL, INDEXNOW_URL, INDEXNOW_KEY, DOMAIN

class LiveAuditor:
    """Probes live production website at aidigitools.tech to verify reachability, SSL, headers, and key files."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.ssl_context = ssl.create_default_context()

    def check_homepage(self) -> Dict[str, Any]:
        """Verifies that the live website homepage responds with HTTP 200 over HTTPS."""
        start = time.time()
        url = f"{BASE_URL}/"
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "AIDigiTools-Autonomous-Engineer/1.0"}
            )
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp:
                elapsed_ms = round((time.time() - start) * 1000, 2)
                headers = dict(resp.headers)
                return {
                    "url": url,
                    "reachable": True,
                    "status_code": resp.status,
                    "latency_ms": elapsed_ms,
                    "server": headers.get("Server", "Unknown"),
                    "headers": {
                        "strict_transport_security": headers.get("Strict-Transport-Security", None),
                        "content_security_policy": headers.get("Content-Security-Policy", None),
                        "x_frame_options": headers.get("X-Frame-Options", None),
                        "x_content_type_options": headers.get("X-Content-Type-Options", None),
                        "referrer_policy": headers.get("Referrer-Policy", None)
                    },
                    "error": None
                }
        except urllib.error.HTTPError as e:
            elapsed_ms = round((time.time() - start) * 1000, 2)
            return {
                "url": url,
                "reachable": False,
                "status_code": e.code,
                "latency_ms": elapsed_ms,
                "error": f"HTTPError {e.code}: {e.reason}"
            }
        except Exception as e:
            return {
                "url": url,
                "reachable": False,
                "status_code": 0,
                "latency_ms": 0,
                "error": f"Network exception: {str(e)}"
            }

    def check_indexnow_key_file(self) -> Dict[str, Any]:
        """Verifies that the IndexNow key verification file is publicly accessible over HTTPS."""
        try:
            req = urllib.request.Request(
                INDEXNOW_URL,
                headers={"User-Agent": "AIDigiTools-Autonomous-Engineer/1.0"}
            )
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8").strip()
                matches_key = (body == INDEXNOW_KEY)
                return {
                    "url": INDEXNOW_URL,
                    "status_code": resp.status,
                    "valid": (resp.status == 200 and matches_key),
                    "matches_key": matches_key,
                    "error": None if (resp.status == 200 and matches_key) else f"Content mismatch: expected {INDEXNOW_KEY}, got {body}"
                }
        except urllib.error.HTTPError as e:
            return {
                "url": INDEXNOW_URL,
                "status_code": e.code,
                "valid": False,
                "error": f"HTTPError {e.code}: {e.reason}"
            }
        except Exception as e:
            return {
                "url": INDEXNOW_URL,
                "status_code": 0,
                "valid": False,
                "error": f"Network exception: {str(e)}"
            }

    def probe_sample_routes(self, sample_urls: List[str]) -> List[Dict[str, Any]]:
        """Probes a representative sample of public URLs to confirm they are live and non-redirected."""
        results = []
        for url in sample_urls:
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "AIDigiTools-Autonomous-Engineer/1.0"}
                )
                with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp:
                    results.append({
                        "url": url,
                        "status_code": resp.status,
                        "final_url": resp.url,
                        "redirected": (resp.url != url),
                        "ok": (resp.status == 200)
                    })
            except urllib.error.HTTPError as e:
                results.append({
                    "url": url,
                    "status_code": e.code,
                    "ok": False,
                    "error": f"HTTP {e.code}"
                })
            except Exception as e:
                results.append({
                    "url": url,
                    "status_code": 0,
                    "ok": False,
                    "error": str(e)
                })
        return results

    def run_live_audit(self, sample_urls: List[str] = None) -> Dict[str, Any]:
        """Runs the complete suite of live HTTP probes."""
        homepage_result = self.check_homepage()
        indexnow_result = self.check_indexnow_key_file()
        sample_results = self.probe_sample_routes(sample_urls or [
            f"{BASE_URL}/",
            f"{BASE_URL}/tools/chatgpt-plus.html",
            f"{BASE_URL}/categories/coding.html",
            f"{BASE_URL}/deals.html"
        ])

        all_ok = homepage_result["reachable"] and indexnow_result["valid"] and all(r["ok"] for r in sample_results)
        return {
            "timestamp": time.time(),
            "homepage": homepage_result,
            "indexnow_key": indexnow_result,
            "sample_routes": sample_results,
            "all_live_checks_passed": all_ok
        }
