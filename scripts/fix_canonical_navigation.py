from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
html_files = [p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)]

count = 0
for hf in html_files:
    txt = hf.read_text(encoding="utf-8")
    new_txt = txt
    new_txt = new_txt.replace('href="../index.html"', 'href="../"')
    new_txt = new_txt.replace('href="../index.html#', 'href="../#')
    
    # In root pages, replace href="index.html" with href="/" or href="./"
    if hf.parent == ROOT and hf.name != "index.html":
        new_txt = new_txt.replace('href="index.html"', 'href="./"')
        new_txt = new_txt.replace('href="index.html#', 'href="./#')

    if new_txt != txt:
        hf.write_text(new_txt, encoding="utf-8")
        count += 1
        print(f"[OK] Updated navigation in {hf.relative_to(ROOT)}")

print(f"[SUCCESS] Updated navigation in {count} HTML files!")
