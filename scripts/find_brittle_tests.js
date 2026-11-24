const fs = require('fs');
const path = require('path');

const testsDir = path.join(__dirname, '..', 'tests');
const files = fs.readdirSync(testsDir).filter(f => f.endsWith('.py'));

console.log('Scanning tests/*.py for sitemap, admin, and schema assertions:');

files.forEach(f => {
  const content = fs.readFileSync(path.join(testsDir, f), 'utf8');
  const lines = content.split('\n');
  lines.forEach((l, i) => {
    if ((l.includes('sitemap') || l.includes('schema') || l.includes('admin')) && l.includes('assert')) {
      console.log(`[${f}:${i+1}] ${l.trim()}`);
    }
  });
});
