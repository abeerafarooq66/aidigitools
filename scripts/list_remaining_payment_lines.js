const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const toolFiles = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

const otherLines = [];
toolFiles.forEach(f => {
  const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  content.split('\n').forEach((l, i) => {
    if (/sadapay|easypaisa|jazzcash|nayapay/i.test(l)) {
      const trimmed = l.trim();
      if (!trimmed.includes('rail-option') && 
          !trimmed.includes('og:description') && 
          !trimmed.includes('twitter:description') && 
          !trimmed.includes('<span>🟠</span>') &&
          !trimmed.includes('<span>🔵</span>') &&
          !trimmed.includes('<span>🟢</span>')) {
        otherLines.push({ file: f, line: i + 1, text: trimmed });
      }
    }
  });
});

console.log('Total non-cart lines remaining:', otherLines.length);
otherLines.forEach(o => {
  console.log(`[${o.file}:${o.line}] ${o.text.substring(0, 100)}`);
});
