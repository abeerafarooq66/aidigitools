import os
import json
import base64
from pathlib import Path

TEMP_FILE = Path(os.environ.get('TEMP', 'C:/Users/Dell/AppData/Local/Temp')) / 'rendered_icons_dump.json'
ROOT = Path(__file__).resolve().parent.parent

out_dir_square = ROOT / 'assets/images/square'
out_dir_square.mkdir(parents=True, exist_ok=True)

catalogue_dir = Path('C:/Users/Dell/Desktop/WhatsApp_Business_AIDigiTools/Catalogue_Products')
catalogue_dir.mkdir(parents=True, exist_ok=True)

print(f"Reading dumped icons from {TEMP_FILE}...")
data = json.load(open(TEMP_FILE, 'r', encoding='utf-8'))

print(f"Unpacking {len(data)} icons...")
saved_count = 0
for slug, data_url in data.items():
    # data_url is "data:image/png;base64,..."
    if ',' in data_url:
        b64 = data_url.split(',', 1)[1]
    else:
        b64 = data_url
    
    img_bytes = base64.b64decode(b64)
    
    # Save to assets/images/square/{slug}.png
    (out_dir_square / f'{slug}.png').write_bytes(img_bytes)
    
    # Also save to assets/images/{slug}-square.png
    (ROOT / 'assets/images' / f'{slug}-square.png').write_bytes(img_bytes)
    
    # Also save to Desktop/WhatsApp_Business_AIDigiTools/Catalogue_Products/{slug}.png
    (catalogue_dir / f'{slug}.png').write_bytes(img_bytes)
    
    saved_count += 1

print(f"SUCCESS: Unpacked and saved {saved_count} square 600x600 PNG icons to:")
print(f"  1. {out_dir_square}")
print(f"  2. {ROOT / 'assets/images'}")
print(f"  3. {catalogue_dir}")
