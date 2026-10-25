import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = sorted([p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)])

print("Checking SEO & AEO metrics across all HTML files:")
all_ok = True
for f in files:
    content = f.read_text(encoding="utf-8")
    title_m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    title = title_m.group(1).strip() if title_m else "MISSING"
    desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=(["\'])(.*?)\1', content, re.IGNORECASE)
    desc = desc_m.group(2).strip() if desc_m else "MISSING"
    qa_m = re.search(r'<p[^>]*class=["\']quick-answer["\'][^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
    qa = re.sub(r"<[^>]+>", "", qa_m.group(1)).strip() if qa_m else "MISSING"
    words = len(qa.split()) if qa != "MISSING" else 0
    
    t_ok = 30 <= len(title) <= 65
    d_ok = 70 <= len(desc) <= 165
    w_ok = 35 <= words <= 70
    
    status = "OK" if (t_ok and d_ok and w_ok) else "WARN"
    if status == "WARN":
        all_ok = False
        print(f"[{status}] {f.relative_to(ROOT)}: title={len(title)} (ok={t_ok}), desc={len(desc)} (ok={d_ok}), qa_words={words} (ok={w_ok})")
    else:
        print(f"[{status}] {f.relative_to(ROOT)}: title={len(title)}, desc={len(desc)}, qa_words={words}")

if all_ok:
    print(f"\n[SUCCESS] All {len(files)} pages meet strict SEO & AEO character and word count invariants!")
else:
    print("\n[ERROR] Issues found above!")
