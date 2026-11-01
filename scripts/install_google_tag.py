"""
Install GA4 Google Tag (gtag.js) across all 66 production HTML files.
Measurement ID: G-NE094X2Q7H
"""
import os
import re

MEASUREMENT_ID = "G-NE094X2Q7H"

GTAG_SNIPPET = f"""  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{MEASUREMENT_ID}');
  </script>
"""

TARGET_PATTERN = re.compile(r'(<meta\s+name=["\']viewport["\']\s+content=["\']width=device-width,\s*initial-scale=1\.0["\']\s*>)', re.IGNORECASE)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if f"googletagmanager.com/gtag/js?id={MEASUREMENT_ID}" in content:
        return False, "Already contains tag"

    if not TARGET_PATTERN.search(content):
        return False, "Target viewport tag not found"

    # Insert after viewport tag
    new_content = TARGET_PATTERN.sub(r'\1\n' + GTAG_SNIPPET.rstrip(), content, count=1)

    with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)

    return True, "Tag inserted successfully"

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    updated = 0
    total = 0

    for root, dirs, files in os.walk(root_dir):
        # Exclude git, node_modules, tests
        if any(p in root for p in [".git", "node_modules", ".gemini"]):
            continue
        for file in files:
            if file.endswith(".html"):
                total += 1
                filepath = os.path.join(root, file)
                success, msg = process_file(filepath)
                if success:
                    updated += 1
                    rel_path = os.path.relpath(filepath, root_dir)
                    print(f"[{updated}/{total}] Updated: {rel_path}")

    print(f"\nDone. Updated {updated} of {total} HTML files.")

    # Verification scan
    verified = 0
    for root, dirs, files in os.walk(root_dir):
        if any(p in root for p in [".git", "node_modules", ".gemini"]):
            continue
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    c = f.read()
                count = c.count(f"id={MEASUREMENT_ID}")
                assert count == 1, f"Error: {filepath} has count {count} for gtag!"
                verified += 1

    print(f"VERIFIED: All {verified} HTML files contain exactly 1 instance of {MEASUREMENT_ID}!")

if __name__ == "__main__":
    main()

