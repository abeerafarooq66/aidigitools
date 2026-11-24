const fs = require('fs');
const path = require('path');

function getFiles(dir) {
  let res = [];
  fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
    if (e.name.startsWith('.') || ['node_modules', 'tests', 'scratch', 'data', 'admin', 'private'].includes(e.name)) return;
    const f = path.join(dir, e.name);
    if (e.isDirectory()) res = res.concat(getFiles(f));
    else if (f.endsWith('.html') && !f.endsWith('404.html')) res.push(f);
  });
  return res;
}

const files = getFiles('.');
const faqFiles = [];
files.forEach(f => {
  const c = fs.readFileSync(f, 'utf8');
  if (c.includes('"@type": "FAQPage"') || c.includes('"@type":  "FAQPage"')) {
    faqFiles.push(f);
  }
});

console.log(`Found ${faqFiles.length} FAQPage files:`);
faqFiles.forEach(f => console.log(' -', f));
