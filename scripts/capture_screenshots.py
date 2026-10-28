import subprocess
import time
import json
import urllib.request
import os
import socket
import urllib.parse
import base64

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9228
USER_DATA = r"C:\Users\Dell\AppData\Local\Temp\chrome_snap_profile"

def capture_all(prefix="before"):
    out_dir = os.path.join("screenshots", prefix)
    os.makedirs(out_dir, exist_ok=True)

    targets = [
        ("index.html", f"{out_dir}/homepage_desktop.png", 1440, 900),
        ("index.html", f"{out_dir}/homepage_mobile.png", 390, 844),
        ("categories/coding.html", f"{out_dir}/category_coding.png", 1440, 900),
        ("tools/chatgpt-plus.html", f"{out_dir}/tool_chatgpt.png", 1440, 900),
        ("compare/chatgpt-vs-claude.html", f"{out_dir}/compare.png", 1440, 900),
        ("deals.html", f"{out_dir}/deals.png", 1440, 900),
        ("about.html", f"{out_dir}/about.png", 1440, 900)
    ]

    for rel_path, out_file, w, h in targets:
        abs_p = os.path.abspath(rel_path).replace(os.sep, "/")
        url = f"file:///{abs_p}"
        proc = subprocess.Popen([
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--window-size={w},{h}",
            f"--remote-debugging-port={PORT}",
            f"--user-data-dir={USER_DATA}",
            url
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        try:
            time.sleep(2)
            endpoints = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json").read().decode("utf-8"))
            page_target = next((t for t in endpoints if t.get("type") == "page"), None)
            ws_url = page_target.get("webSocketDebuggerUrl")
            
            parsed = urllib.parse.urlparse(ws_url)
            s = socket.create_connection((parsed.hostname, parsed.port), timeout=5)
            key = "dGhlIHNhbXBsZSBub25jZQ=="
            s.sendall((
                f"GET {parsed.path} HTTP/1.1\r\nHost: {parsed.hostname}:{parsed.port}\r\n"
                "Upgrade: websocket\r\nConnection: Upgrade\r\n"
                f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
            ).encode("utf-8"))
            s.recv(4096)
            
            def send_cdp(method, params=None):
                payload = json.dumps({"id": 1, "method": method, "params": params or {}}).encode("utf-8")
                mask = os.urandom(4)
                length = len(payload)
                frame = bytearray([0x81])
                if length <= 125: frame.append(0x80 | length)
                elif length <= 65535: frame.extend([0x80 | 126, (length >> 8) & 0xFF, length & 0xFF])
                else: frame.extend([0x80 | 127] + list(length.to_bytes(8, "big")))
                frame.extend(mask)
                frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
                s.sendall(frame)
                raw = b""
                while True:
                    chunk = s.recv(65536)
                    if not chunk: break
                    raw += chunk
                    if len(raw) >= 2:
                        plen = raw[1] & 0x7F
                        off = 2
                        if plen == 126:
                            if len(raw) < 4: continue
                            plen = int.from_bytes(raw[2:4], "big")
                            off = 4
                        elif plen == 127:
                            if len(raw) < 10: continue
                            plen = int.from_bytes(raw[2:10], "big")
                            off = 10
                        if len(raw) >= off + plen:
                            return json.loads(raw[off:off+plen].decode("utf-8", errors="ignore"))
            
            res = send_cdp("Page.captureScreenshot", {"format": "png"})
            data = res.get("result", {}).get("data")
            if data:
                with open(out_file, "wb") as img_f:
                    img_f.write(base64.b64decode(data))
                print(f"Captured: {out_file} ({os.path.getsize(out_file)} bytes)")
            s.close()
        except Exception as e:
            print(f"Error capturing {rel_path}: {e}")
        finally:
            proc.terminate()
            try: proc.wait(timeout=2)
            except: proc.kill()
            time.sleep(0.5)

if __name__ == "__main__":
    import sys
    pref = sys.argv[1] if len(sys.argv) > 1 else "before"
    capture_all(pref)
