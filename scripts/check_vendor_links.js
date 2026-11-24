const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

let missing = 0;
files.forEach(f => {
  const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  if (!content.includes('rel="noopener noreferrer nofollow"')) {
    missing++;
    console.log(`Missing in ${f}`);
  }
});
console.log(`Total missing: ${missing} / ${files.length}`);
