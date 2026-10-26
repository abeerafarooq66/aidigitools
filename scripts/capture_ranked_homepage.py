import subprocess
import os
import shutil
import tempfile

index_file = r'C:\Users\Dell\Desktop\aidigitools\index.html'
brain_dir = r'C:\Users\Dell\.gemini\antigravity\brain\b9098f9b-3fdd-4d44-b502-c2981cd56d6f'
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
if not os.path.exists(chrome_path):
    chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

temp_dir = tempfile.gettempdir()

shots = [
    ('preview_index_ranked_top.png', 1400, 1100),
    ('preview_index_ranked_cards.png', 1400, 1800),
]

for filename, w, h in shots:
    temp_out = os.path.join(temp_dir, filename)
    if os.path.exists(temp_out):
        os.remove(temp_out)
    cmd = [
        chrome_path,
        '--headless=new',
        f'--window-size={w},{h}',
        '--virtual-time-budget=2000',
        '--hide-scrollbars',
        f'--screenshot={temp_out}',
        index_file
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(temp_out):
        dest = os.path.join(brain_dir, filename)
        shutil.copy2(temp_out, dest)
        print(f"Captured {filename} ({os.path.getsize(dest)} bytes)")
    else:
        print(f"Failed to capture {filename}")
