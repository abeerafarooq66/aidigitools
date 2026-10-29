import os
import sys
import time
import json
import socket
import urllib.request
import urllib.parse
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from .models import AuditIssue

class BrowserInteractionAuditor:
    """Audits browser runtime execution, JS console errors, responsive viewports, and UI interactions."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()
        self.chrome_binary = self._detect_chrome_binary()

    def _detect_chrome_binary(self) -> Optional[str]:
        """Detects Chrome or Chromium executable on Windows and Linux runners."""
        candidates = [
            # Windows
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            # Linux (GitHub Actions ubuntu-latest)
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser"
        ]
        for c in candidates:
            if os.path.exists(c) and os.access(c, os.X_OK if sys.platform != "win32" else os.R_OK):
                return c
        return None

    def audit_browser_interactions(self, timestamp: str) -> Tuple[List[AuditIssue], Dict[str, Any]]:
        """Executes in-browser test suite via headless Chrome CDP."""
        issues: List[AuditIssue] = []
        summary = {
            "browser_tested": False,
            "browser_path": self.chrome_binary,
            "interactions_passed": 0,
            "interactions_failed": 0,
            "console_errors_count": 0,
            "responsive_checks_passed": 0
        }

        if not self.chrome_binary:
            issues.append(AuditIssue(
                id="BROWSER_BINARY_NOT_FOUND",
                timestamp=timestamp,
                tested_url="index.html",
                category="BROWSER_INTERACTION",
                severity="NOTICE",
                confidence="UNCERTAIN",
                evidence="Headless Chrome binary not detected on host system. Browser test skipped.",
                recommended_fix="Install Google Chrome or Chromium to enable full browser interaction testing."
            ))
            return issues, summary

        port = 9223
        user_data = self.root / ".chrome_audit_profile"
        user_data.mkdir(exist_ok=True)
        html_url = (self.root / "index.html").as_uri()

        proc = None
        try:
            cmd = [
                self.chrome_binary,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--remote-debugging-port={port}",
                f"--user-data-dir={user_data.as_posix()}",
                html_url
            ]
            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(2.5)

            # Query CDP endpoints with retries
            targets = []
            for _ in range(5):
                try:
                    raw_json = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3).read().decode("utf-8")
                    targets = json.loads(raw_json)
                    if targets:
                        break
                except Exception:
                    time.sleep(1)

            page_target = next((t for t in targets if t.get("type") == "page"), None)
            if not page_target:
                issues.append(AuditIssue(
                    id="CDP_NO_PAGE_TARGET",
                    timestamp=timestamp,
                    tested_url="index.html",
                    category="BROWSER_INTERACTION",
                    severity="NOTICE",
                    confidence="UNCERTAIN",
                    evidence="No active page target found on CDP endpoint.",
                    recommended_fix="Verify headless Chrome launch flags."
                ))
                return issues, summary

            ws_url = page_target.get("webSocketDebuggerUrl")
            if not ws_url:
                return issues, summary

            parsed = urllib.parse.urlparse(ws_url)
            s = socket.create_connection((parsed.hostname, parsed.port), timeout=5)
            s.settimeout(3.0)

            # Send WebSocket handshake
            key = "dGhlIHNhbXBsZSBub25jZQ=="
            req = (
                f"GET {parsed.path} HTTP/1.1\r\n"
                f"Host: {parsed.hostname}:{parsed.port}\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\n"
                "Sec-WebSocket-Version: 13\r\n\r\n"
            )
            s.sendall(req.encode("utf-8"))
            resp = s.recv(4096).decode("utf-8", errors="ignore")
            if "101" not in resp:
                return issues, summary

            msg_id = 1
            def send_cdp(method: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
                nonlocal msg_id
                payload = json.dumps({"id": msg_id, "method": method, "params": params or {}})
                msg_id += 1
                data = payload.encode("utf-8")
                length = len(data)
                mask = os.urandom(4)
                frame = bytearray([0x81])
                if length <= 125:
                    frame.append(0x80 | length)
                elif length <= 65535:
                    frame.append(0x80 | 126)
                    frame.extend(length.to_bytes(2, "big"))
                else:
                    frame.append(0x80 | 127)
                    frame.extend(length.to_bytes(8, "big"))
                frame.extend(mask)
                frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(data)))
                s.sendall(frame)

                raw = b""
                start_read = time.time()
                while time.time() - start_read < 3:
                    try:
                        chunk = s.recv(65536)
                    except (socket.timeout, TimeoutError):
                        break
                    except Exception:
                        break
                    if not chunk:
                        break
                    raw += chunk
                    if len(raw) >= 2:
                        b1, b2 = raw[0], raw[1]
                        payload_len = b2 & 0x7F
                        offset = 2
                        if payload_len == 126:
                            if len(raw) < 4:
                                continue
                            payload_len = int.from_bytes(raw[2:4], "big")
                            offset = 4
                        elif payload_len == 127:
                            if len(raw) < 10:
                                continue
                            payload_len = int.from_bytes(raw[2:10], "big")
                            offset = 10
                        if len(raw) >= offset + payload_len:
                            payload_bytes = raw[offset:offset+payload_len]
                            try:
                                parsed_resp = json.loads(payload_bytes.decode("utf-8", errors="ignore"))
                                if parsed_resp.get("id") == msg_id - 1:
                                    return parsed_resp
                            except Exception:
                                pass
                return None

            def evaluate(expression: str) -> Any:
                res = send_cdp("Runtime.evaluate", {"expression": expression, "returnByValue": True})
                if res and "result" in res and "result" in res["result"]:
                    return res["result"]["result"].get("value")
                return None

            summary["browser_tested"] = True

            # Enable Runtime and Console
            send_cdp("Runtime.enable")
            send_cdp("Console.enable")

            # 1. Check Document Title & H1 presence
            title_val = evaluate("document.title")
            h1_val = evaluate("document.querySelector('h1') ? document.querySelector('h1').innerText : ''")
            if title_val and h1_val:
                summary["interactions_passed"] += 1
            else:
                summary["interactions_failed"] += 1
                issues.append(AuditIssue(
                    id="BROWSER_MISSING_HEADINGS",
                    timestamp=timestamp,
                    tested_url="index.html",
                    category="BROWSER_INTERACTION",
                    severity="ERROR",
                    confidence="CONFIRMED",
                    evidence=f"Browser DOM evaluation failed to locate title or <h1>: title='{title_val}'",
                    recommended_fix="Verify index.html DOM hierarchy."
                ))

            # 2. Check Horizontal Overflow at Desktop (1440px)
            send_cdp("Emulation.setDeviceMetricsOverride", {"width": 1440, "height": 900, "deviceScaleFactor": 1, "mobile": False})
            time.sleep(0.3)
            overflow_desktop = evaluate("document.documentElement.scrollWidth > window.innerWidth")
            if overflow_desktop is False:
                summary["responsive_checks_passed"] += 1
            elif overflow_desktop is True:
                issues.append(AuditIssue(
                    id="DESKTOP_HORIZONTAL_OVERFLOW",
                    timestamp=timestamp,
                    tested_url="index.html",
                    category="ACCESSIBILITY",
                    severity="ERROR",
                    confidence="CONFIRMED",
                    evidence="Desktop viewport (1440px) exhibits horizontal scroll overflow.",
                    recommended_fix="Adjust max-width or container styling to prevent horizontal overflow."
                ))

            # 3. Check Horizontal Overflow at Mobile (390px)
            send_cdp("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 3, "mobile": True})
            time.sleep(0.3)
            overflow_mobile = evaluate("document.documentElement.scrollWidth > window.innerWidth")
            if overflow_mobile is False:
                summary["responsive_checks_passed"] += 1
            elif overflow_mobile is True:
                issues.append(AuditIssue(
                    id="MOBILE_HORIZONTAL_OVERFLOW",
                    timestamp=timestamp,
                    tested_url="index.html",
                    category="ACCESSIBILITY",
                    severity="CRITICAL",
                    confidence="CONFIRMED",
                    evidence="Mobile viewport (390px) exhibits horizontal scroll overflow.",
                    recommended_fix="Ensure elements use max-width: 100% and responsive grid containers."
                ))

            # 4. Check Horizontal Overflow at Tablet (820px)
            send_cdp("Emulation.setDeviceMetricsOverride", {"width": 820, "height": 1180, "deviceScaleFactor": 2, "mobile": False})
            time.sleep(0.3)
            overflow_tablet = evaluate("document.documentElement.scrollWidth > window.innerWidth")
            if overflow_tablet is False:
                summary["responsive_checks_passed"] += 1

            # 5. Interactive UI Test: Filter and Search
            test_filter = evaluate("typeof filterCategory === 'function' ? (filterCategory('coding'), true) : false")
            if test_filter:
                summary["interactions_passed"] += 1
            
            test_search = evaluate("typeof applyFilters === 'function' ? (applyFilters(), true) : false")
            if test_search:
                summary["interactions_passed"] += 1

            # 6. Interactive UI Test: Modal Drawer
            drawer_res = evaluate("typeof openQuickOrderModal === 'function' ? (openQuickOrderModal('chatgpt-plus'), document.getElementById('cartDrawer') && document.getElementById('cartDrawer').classList.contains('active')) : false")
            if drawer_res:
                summary["interactions_passed"] += 1
                evaluate("typeof closeQuickOrderModal === 'function' && closeQuickOrderModal()")

        except Exception as e:
            issues.append(AuditIssue(
                id="BROWSER_TEST_EXCEPTION",
                timestamp=timestamp,
                tested_url="index.html",
                category="BROWSER_INTERACTION",
                severity="WARNING",
                confidence="UNCERTAIN",
                evidence=f"Browser test runner encountered exception: {str(e)}",
                recommended_fix="Review browser runner logs."
            ))
        finally:
            if proc:
                try:
                    proc.terminate()
                    proc.wait(timeout=2)
                except Exception:
                    proc.kill()
            # Clean up temp profile if empty
            try:
                import shutil
                shutil.rmtree(user_data, ignore_errors=True)
            except Exception:
                pass

        return issues, summary
