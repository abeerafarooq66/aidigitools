const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const toolFiles = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

let qaCount = 0;
toolFiles.forEach(f => {
  const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  if (content.includes('quick-answer') && /JazzCash|EasyPaisa|SadaPay|NayaPay/i.test(content)) {
    qaCount++;
    const match = content.match(/<p class="quick-answer"[^>]*>([\s\S]*?)<\/p>/);
    if (match && /JazzCash|EasyPaisa|SadaPay|NayaPay/i.test(match[1])) {
      console.log(`[${f}] ${match[1].substring(0, 120)}...`);
    }
  }
});
console.log(`Total quick-answers with payment keywords: ${qaCount}`);
