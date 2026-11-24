const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const findings = [];

function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.git') || entry.name === 'node_modules' || entry.name === 'audit_reports') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanDir(full);
    } else if (entry.name.endsWith('.html') || entry.name.endsWith('.txt') || entry.name.endsWith('.json') || entry.name.endsWith('.md')) {
      const content = fs.readFileSync(full, 'utf8');
      const lines = content.split('\n');
      lines.forEach((l, i) => {
        if (/Sonnet 5\.5|Claude 5\.5|GPT-6|GPT-5\.5|Midjourney V8/i.test(l)) {
          findings.push({
            file: path.relative(repoRoot, full),
            line: i + 1,
            text: l.trim()
          });
        }
      });
    }
  }
}

scanDir(repoRoot);

console.log(`=== GLOBAL REPOSITORY MODEL GROUNDING SCAN ===`);
console.log(`Total occurrences found: ${findings.length}`);
findings.forEach(f => {
  console.log(`[${f.file}:${f.line}] ${f.text.substring(0, 120)}`);
});
