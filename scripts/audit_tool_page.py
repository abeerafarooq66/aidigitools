import subprocess, time, json, urllib.request, os, socket, urllib.parse

CHROME_PATH = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = 9227
USER_DATA = r'C:\Users\Dell\AppData\Local\Temp\chrome_tool_profile'
HTML_URL = f'file:///{os.path.abspath("tools/chatgpt-plus.html").replace(os.sep, "/")}'

proc = subprocess.Popen([
    CHROME_PATH, '--headless=new', '--disable-gpu', '--no-sandbox',
    f'--remote-debugging-port={PORT}', f'--user-data-dir={USER_DATA}', HTML_URL
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    time.sleep(2)
    endpoints = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json').read().decode('utf-8'))
    page_target = next((t for t in endpoints if t.get('type') == 'page'), None)
    ws_url = page_target.get('webSocketDebuggerUrl')
    
    parsed = urllib.parse.urlparse(ws_url)
    s = socket.create_connection((parsed.hostname, parsed.port), timeout=5)
    key = 'dGhlIHNhbXBsZSBub25jZQ=='
    s.sendall((
        f'GET {parsed.path} HTTP/1.1\r\n'
        f'Host: {parsed.hostname}:{parsed.port}\r\n'
        'Upgrade: websocket\r\n'
        'Connection: Upgrade\r\n'
        f'Sec-WebSocket-Key: {key}\r\n'
        'Sec-WebSocket-Version: 13\r\n\r\n'
    ).encode('utf-8'))
    s.recv(4096)
    
    msg_id = 1
    def send_cdp(method, params=None):
        global msg_id
        payload = json.dumps({'id': msg_id, 'method': method, 'params': params or {}}).encode('utf-8')
        msg_id += 1
        mask = os.urandom(4)
        length = len(payload)
        frame = bytearray([0x81])
        if length <= 125: frame.append(0x80 | length)
        elif length <= 65535: frame.extend([0x80 | 126, (length >> 8) & 0xFF, length & 0xFF])
        else: frame.extend([0x80 | 127] + list(length.to_bytes(8, 'big')))
        frame.extend(mask)
        frame.extend(bytes(b ^ mask[i % 4] for i, b in enumerate(payload)))
        s.sendall(frame)
        raw = b''
        while True:
            chunk = s.recv(65536)
            if not chunk: break
            raw += chunk
            if len(raw) >= 2:
                plen = raw[1] & 0x7F
                off = 2
                if plen == 126:
                    if len(raw) < 4: continue
                    plen = int.from_bytes(raw[2:4], 'big')
                    off = 4
                elif plen == 127:
                    if len(raw) < 10: continue
                    plen = int.from_bytes(raw[2:10], 'big')
                    off = 10
                if len(raw) >= off + plen:
                    return json.loads(raw[off:off+plen].decode('utf-8', errors='ignore'))

    def evaluate(expression):
        res = send_cdp('Runtime.evaluate', {'expression': expression, 'returnByValue': True})
        return res.get('result', {}).get('result', {}).get('value')

    check_js = '''
    (function() {
        var targets = [
            { label: 'Page Title h1', sel: 'h1' },
            { label: 'Quick Answer', sel: '.quick-answer' },
            { label: 'Reseller Notice', sel: '.reseller-notice' },
            { label: 'Pricing Section / Box', sel: '.price-tag' },
            { label: 'Inquiry CTA Button', sel: '.btn-wa, .btn-whatsapp, a[href*="wa.me"]' },
            { label: 'Comparison / Spec Table TH', sel: 'th' },
            { label: 'Comparison / Spec Table TD', sel: 'td' },
            { label: 'FAQ Summary', sel: 'summary' },
            { label: 'Footer Title', sel: '.footer-col h4' }
        ];
        return targets.map(function(t) {
            var el = document.querySelector(t.sel);
            if (!el) return { label: t.label, found: false };
            var style = getComputedStyle(el);
            return {
                label: t.label,
                found: true,
                color: style.color,
                backgroundColor: style.backgroundColor
            };
        });
    })()
    '''
    res = evaluate(check_js)
    print('=' * 50)
    print('INNER TOOL PAGE (tools/chatgpt.html) AUDIT:')
    print('=' * 50)
    for r in res:
        if r.get('found'):
            print(f"{r['label']}: Color={r['color']} -- Bg={r['backgroundColor']}")
        else:
            print(f"{r['label']}: NOT FOUND")
finally:
    proc.terminate()
    try: proc.wait(timeout=2)
    except: proc.kill()
