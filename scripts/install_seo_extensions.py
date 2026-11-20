import winreg
import urllib.request
import os
import zipfile
import io

extensions = {
    'akdgnmcogleenhbclghghlkkdndkjdjc': 'SEOquake',
    'bfdjmnijjenafhpkgbnbndfdffkfapgg': 'Keyword_Surfer',
    'oegbbglflbpimnoeglobebkohnlojbfg': 'Detailed_SEO'
}

base_key_path = r'Software\Google\Chrome\Extensions'

print("=== 1. REGISTERING EXTENSIONS IN WINDOWS REGISTRY ===")
with winreg.CreateKey(winreg.HKEY_CURRENT_USER, base_key_path) as root_key:
    for ext_id, name in extensions.items():
        with winreg.CreateKey(root_key, ext_id) as ext_key:
            winreg.SetValueEx(ext_key, 'update_url', 0, winreg.REG_SZ, 'https://clients2.google.com/service/update2/crx')
            print(f"Registry Key Set: HKCU\\{base_key_path}\\{ext_id} -> update_url")

print("\n=== 2. DOWNLOADING OFFICIAL CRX PACKAGES ===")
dest_dir = os.path.expanduser(r"~\Downloads\SEO_Extensions")
os.makedirs(dest_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for ext_id, name in extensions.items():
    url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=120.0&acceptformat=crx2,crx3&x=id%3D{ext_id}%26uc"
    crx_path = os.path.join(dest_dir, f"{name}.crx")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            with open(crx_path, 'wb') as out_f:
                out_f.write(content)
        size_kb = round(os.path.getsize(crx_path) / 1024, 1)
        print(f"Downloaded: {name}.crx ({size_kb} KB) -> {crx_path}")
    except Exception as e:
        print(f"Download failed for {name}: {e}")

print(f"\nAll extension packages saved to: {dest_dir}")
