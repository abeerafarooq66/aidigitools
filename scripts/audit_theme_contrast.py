import subprocess
import time
import json
import urllib.request
import os

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = 9226
USER_DATA = r"C:\Users\Dell\AppData\Local\Temp\chrome_contrast_profile"
HTML_URL = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"

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
    endpoints = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json").read().decode("utf-8"))
    page_target = next((t for t in endpoints if t.get("type") == "page"), None)
    ws_url = page_target.get("webSocketDebuggerUrl")
    
    import socket, urllib.parse
    parsed = urllib.parse.urlparse(ws_url)
    s = socket.create_connection((parsed.hostname, parsed.port), timeout=5)
    key = "dGhlIHNhbXBsZSBub25jZQ=="
    s.sendall((
        f"GET {parsed.path} HTTP/1.1\r\n"
        f"Host: {parsed.hostname}:{parsed.port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    ).encode("utf-8"))
    s.recv(4096)
    
    msg_id = 1
    def send_cdp(method, params=None):
        global msg_id
        payload = json.dumps({"id": msg_id, "method": method, "params": params or {}}).encode("utf-8")
        msg_id += 1
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

    def evaluate(expression):
        res = send_cdp("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value")

    check_elements_js = """
    (function() {
        var targets = [
            { label: "Header Nav Links", sel: "nav a" },
            { label: "Header CTA Button", sel: ".nav-cta" },
            { label: "Hero Title", sel: ".hero h1" },
            { label: "Hero Quick Answer", sel: ".hero .quick-answer" },
            { label: "Hero Badges", sel: ".hero .badge" },
            { label: "AuthKit Title", sel: ".authkit-tool-title" },
            { label: "AuthKit Price", sel: ".authkit-price-val" },
            { label: "AuthKit Inquire CTA", sel: "#mWaLink" },
            { label: "Search Field Text", sel: "#toolSearchInput" },
            { label: "Category Pill Inactive", sel: ".cat-pill-btn:not(.active)" },
            { label: "Category Pill Active", sel: ".cat-pill-btn.active" },
            { label: "Tool Card Title", sel: ".tool-card h3" },
            { label: "Tool Card Description", sel: ".tool-card p" },
            { label: "Tool Card Price Amount", sel: ".tool-card .price-amount" },
            { label: "Tool Card Quick Order Button", sel: ".tool-card .btn-quick-order" },
            { label: "Tool Card WhatsApp Button", sel: ".tool-card .btn-wa-subtle" },
            { label: "Tool Card Compare Button", sel: ".tool-card .btn-tool-compare" },
            { label: "Feature Card Title", sel: "#features .card h2" },
            { label: "Feature Card Paragraph", sel: "#features .card p" },
            { label: "Table Header", sel: "th" },
            { label: "Table Data Cell", sel: "td" },
            { label: "Footer Column Title", sel: ".footer-col h4" },
            { label: "Footer Links", sel: ".footer-col a" }
        ];

        return targets.map(function(t) {
            var el = document.querySelector(t.sel);
            if (!el) return { label: t.label, found: false };
            var style = getComputedStyle(el);
            return {
                label: t.label,
                found: true,
                color: style.color,
                backgroundColor: style.backgroundColor,
                fontSize: style.fontSize,
                fontWeight: style.fontWeight,
                border: style.border
            };
        });
    })()
    """

    results = evaluate(check_elements_js)
    print("=" * 65)
    print("COMPREHENSIVE LIGHT THEME CONTRAST & VISIBILITY AUDIT")
    print("=" * 65)
    for r in results:
        if r.get("found"):
            print(f"[{r['label']}]")
            print(f"   Color: {r['color']} | Bg: {r['backgroundColor']}")
            print(f"   Font: {r['fontSize']} (weight {r['fontWeight']}) | Border: {r['border'][:30]}...")
        else:
            print(f"[{r['label']}] NOT FOUND")
    print("=" * 65)

finally:
    proc.terminate()
    try: proc.wait(timeout=2)
    except: proc.kill()
