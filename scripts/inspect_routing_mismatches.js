const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

files.forEach(f => {
  const expectedSlug = f.replace('.html', '');
  const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  const lines = content.split('\n');
  lines.forEach((l, i) => {
    if (l.includes('openQuickOrderModal') && !l.includes(`'${expectedSlug}'`) && !l.includes(`"${expectedSlug}"`)) {
      console.log(`[${f}:${i+1}] ${l.trim().substring(0, 120)}`);
    }
  });
});
