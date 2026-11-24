const fs = require('fs');
const content = fs.readFileSync('tools/claude-pro.html', 'utf8');
const lines = content.split('\n');
lines.forEach((l, i) => {
  if (l.includes('quick-answer')) {
    console.log(`Line ${i+1}: ${l}`);
  }
});
