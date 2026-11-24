const fs = require('fs');
const path = require('path');

const wfDir = path.join(__dirname, '..', '.github', 'workflows');
const files = fs.readdirSync(wfDir).filter(f => f.endsWith('.yml') || f.endsWith('.yaml'));

console.log('Workflows that run git push:');
files.forEach(f => {
  const content = fs.readFileSync(path.join(wfDir, f), 'utf8');
  if (content.includes('git push') || content.includes('push:')) {
    const lines = content.split('\n');
    lines.forEach((l, i) => {
      if (l.includes('git push')) {
        console.log(`[${f}:${i+1}] ${l.trim()}`);
      }
    });
  }
});
