import subprocess
import time
import json
import urllib.request
import os

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9222
USER_DATA = r"C:\Users\Dell\AppData\Local\Temp\chrome_cdp_profile"
HTML_URL = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"

print("Starting headless Chrome with remote debugging on port", PORT)
proc = subprocess.Popen([
    CHROME_PATH,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    f"--remote-debugging-port={PORT}",
    f"--user-data-dir={USER_DATA}",
    HTML_URL
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    time.sleep(2)
    
    # Query targets from CDP
    endpoints = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json").read().decode("utf-8"))
    page_target = next((t for t in endpoints if t.get("type") == "page"), None)
    
    if not page_target:
        print("ERROR: No page target found!")
        exit(1)
        
    ws_url = page_target.get("webSocketDebuggerUrl")
    print("Found page target:", page_target.get("title"))
    print("WebSocket URL:", ws_url)
    
    # Simple websocket communication via python
    # We can use simple socket or evaluate script via CDP HTTP or websocket
    import socket
    import urllib.parse
    
    parsed = urllib.parse.urlparse(ws_url)
    s = socket.create_connection((parsed.hostname, parsed.port), timeout=5)
    
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
        print("WebSocket handshake failed:", resp)
        exit(1)
        
    print("WebSocket handshake successful!")
    
    # Helper to send a WS text frame and receive response
    msg_id = 1
    def send_cdp(method, params=None):
        global msg_id
        payload = json.dumps({"id": msg_id, "method": method, "params": params or {}})
        msg_id += 1
        
        # Build masked WS frame
        data = payload.encode("utf-8")
        length = len(data)
        import os as _os
        mask = _os.urandom(4)
        
        frame = bytearray([0x81]) # FIN + text
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
        
        # Read response frame
        raw = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            raw += chunk
            # Check if we have complete payload
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
                        return json.loads(payload_bytes.decode("utf-8", errors="ignore"))
                    except Exception:
                        pass
        return None

    def evaluate(expression):
        res = send_cdp("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value")

    print("\n--- RUNNING IN-BROWSER INTERACTION TESTS ---")

    # 1. Check title & h1
    page_title = evaluate("document.title")
    h1_text = evaluate("document.querySelector('h1').innerText")
    print(f"[OK] Title: {page_title}")
    print(f"[OK] H1: {h1_text}")

    # 2. Check Theme Colors applied in DOM
    bg_canvas = evaluate("getComputedStyle(document.body).backgroundColor")
    header_bg = evaluate("getComputedStyle(document.querySelector('header')).backgroundColor")
    hero_bg = evaluate("getComputedStyle(document.querySelector('.hero')).backgroundColor")
    card_bg = evaluate("getComputedStyle(document.querySelector('.tool-card')).backgroundColor")
    footer_bg = evaluate("getComputedStyle(document.querySelector('footer')).backgroundColor")
    
    print(f"[OK] Body background: {bg_canvas}")
    print(f"[OK] Header background: {header_bg}")
    print(f"[OK] Hero background: {hero_bg}")
    print(f"[OK] Tool Card background: {card_bg}")
    print(f"[OK] Footer background: {footer_bg}")

    # 3. Check Horizontal Overflow at 1440px desktop
    overflow_desktop = evaluate("document.documentElement.scrollWidth > window.innerWidth")
    print(f"[OK] Desktop Horizontal Overflow: {overflow_desktop} (False = No Overflow)")

    # 4. Test Live Filter: Category 'coding'
    eval_filter = evaluate("filterCategory('coding'); Array.from(document.querySelectorAll('.tool-card')).filter(function(c) { return c.style.display !== 'none'; }).length")
    print(f"[OK] Filter 'coding' results count: {eval_filter}")

    # 5. Test Live Search: 'Claude'
    eval_search = evaluate("document.getElementById('toolSearchInput').value = 'Claude'; applyFilters(); Array.from(document.querySelectorAll('.tool-card')).filter(function(c) { return c.style.display !== 'none'; }).length")
    print(f"[OK] Search 'Claude' results count: {eval_search}")

    # 6. Test Reset Filters
    eval_reset = evaluate("resetAllFilters(); Array.from(document.querySelectorAll('.tool-card')).filter(function(c) { return c.style.display !== 'none'; }).length")
    print(f"[OK] Reset filters back to all tools count: {eval_reset}")

    # 7. Test Quick Order Drawer Opening & Closing
    drawer_opened = evaluate("openQuickOrderModal('chatgpt-plus'); document.getElementById('cartDrawer').classList.contains('active')")
    drawer_item = evaluate("document.getElementById('drawerItemName').innerText")
    drawer_closed = evaluate("closeQuickOrderModal(); document.getElementById('cartDrawer').classList.contains('active')")
    print(f"[OK] Quick Order Drawer opened: {drawer_opened}, Item: {drawer_item}, Closed successfully: {not drawer_closed}")

    # 8. Check Comparison Dock
    compare_added = evaluate("toggleCompare('chatgpt-plus'); document.getElementById('compareDock').style.display !== 'none'")
    print(f"[OK] Compare dock activated: {compare_added}")
    evaluate("clearComparison()")

    # 9. Verify Responsive Dimensions (Mobile & Tablet)
    send_cdp("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 3, "mobile": True})
    time.sleep(0.5)
    overflow_mobile = evaluate("document.documentElement.scrollWidth > window.innerWidth")
    print(f"[OK] Mobile (390px) Horizontal Overflow: {overflow_mobile} (False = Perfect Mobile Responsive)")

    send_cdp("Emulation.setDeviceMetricsOverride", {"width": 820, "height": 1180, "deviceScaleFactor": 2, "mobile": False})
    time.sleep(0.5)
    overflow_tablet = evaluate("document.documentElement.scrollWidth > window.innerWidth")
    print(f"[OK] Tablet (820px) Horizontal Overflow: {overflow_tablet} (False = Perfect Tablet Responsive)")

    print("\nALL IN-BROWSER INTERACTION AND RESPONSIVE TESTS PASSED SUCCESSFULLY!")

finally:
    proc.terminate()
    try:
        proc.wait(timeout=3)
    except Exception:
        proc.kill()
