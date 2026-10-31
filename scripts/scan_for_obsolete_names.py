import glob
import os
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

OBSOLETE_PATTERNS = [
    r'Google AI Ultra Plan \(20X\)',
    r'Google Gemini Advanced',
    r'DeepSeek Platform &amp; Pro Access',
    r'DeepSeek Platform & Pro Access',
    r'Grok 2\b',
    r'Google Veo 2\b',
    r'Midjourney v6\.1',
    r'GitHub Copilot Pro\b',
    r'Suno AI Music v3\.5',
    r'Runway Gen-3 Alpha\b',
    r'OpenAI API &amp; Developer Platform',
    r'OpenAI API & Developer Platform'
]

targets = []
for ext in ['*.html', '**/*.html', '*.js', '**/*.js', '*.xml', '**/*.xml', '*.json', '**/*.json', '*.csv', '**/*.csv']:
    targets.extend(glob.glob(os.path.join(REPO_ROOT, ext), recursive=True))

targets = sorted(list(set(targets)))
# Filter out git and virtualenv / scratch / reports
valid_targets = [t for t in targets if not any(x in t for x in ['.git', 'node_modules', 'venv', 'reports', 'audit_report', 'master_49_product_reverification', 'dump_master_fields.py', 'scan_for_obsolete_names.py'])]

print(f"Scanning {len(valid_targets)} files for obsolete patterns...")

findings = {}
for p in valid_targets:
    rel_p = os.path.relpath(p, REPO_ROOT).replace("\\", "/")
    # Ignore backup or script files that deliberately list obsolete names
    if rel_p.startswith('scripts/'):
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    file_matches = []
    for pat in OBSOLETE_PATTERNS:
        matches = re.findall(pat, content, re.IGNORECASE)
        if matches:
            file_matches.extend(matches)
    
    if file_matches:
        findings[rel_p] = file_matches

print(f"\nFiles with obsolete patterns found: {len(findings)}")
for rel_p, m in findings.items():
    print(f"  {rel_p}: {set(m)}")
