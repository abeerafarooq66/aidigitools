const fs = require('fs');
const path = require('path');

const testsDir = path.join(__dirname, '..', 'tests');
const files = fs.readdirSync(testsDir).filter(f => f.endsWith('.py'));

files.forEach(f => {
  const content = fs.readFileSync(path.join(testsDir, f), 'utf8');
  const lines = content.split('\n');
  lines.forEach((l, i) => {
    if (l.includes('@type') && (l.includes('assertIn') || l.includes('assertEqual'))) {
      console.log(`[${f}:${i+1}] ${l.trim()}`);
    }
  });
});
