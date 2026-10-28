import glob
import re

for f in sorted(glob.glob("*.html") + glob.glob("*/*.html")):
    with open(f, "r", encoding="utf-8") as hf:
        content = hf.read()
    
    inline_darks = re.findall(r'style=["\'][^"\']*(?:background:\s*#(?:111827|1f2937|0f172a|000000|000)|color:\s*#(?:ffffff|fff|f9fafb|f3f4f6))[^"\']*["\']', content, re.I)
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    
    if inline_darks or style_blocks:
        print(f"{f}: {len(inline_darks)} inline dark/white matches, {len(style_blocks)} style blocks")
        for m in inline_darks[:5]:
            print(f"   {m}")
