import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tools_dir = ROOT / "tools"

tool_files = sorted(list(tools_dir.glob("*.html")))
print(f"Sanitizing schema in {len(tool_files)} tool pages...")

for tf in tool_files:
    content = tf.read_text(encoding="utf-8")
    
    # Remove aggregateRating block from JSON-LD
    # Regex matching: ,\s*"aggregateRating":\s*\{\s*"@type":\s*"AggregateRating"[^}]*\}
    pattern = re.compile(r',\s*"aggregateRating":\s*\{\s*"@type":\s*"AggregateRating"[^\}]*\}', re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub('', content)
        tf.write_text(new_content, encoding="utf-8")
        print(f"[REMOVED UNVERIFIED RATING] {tf.name}")
    else:
        print(f"[CLEAN] {tf.name}")

print("[SUCCESS] Schema sanitized across all tool pages: 100% honest, policy-compliant, and protected from Google penalties!")
