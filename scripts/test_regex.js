const fs = require('fs');
const c = fs.readFileSync('guides/how-to-pay-for-ai-tools-in-pakistan.html', 'utf8');
const qm = c.match(/<[a-z0-9]+\s+[^>]*class=["'][^"']*quick-answer[^"']*["'][^>]*>([\s\S]*?)<\/[a-z0-9]+>/i);
console.log('qm[0]:', qm[0]);
console.log('qm[1]:', qm[1]);
