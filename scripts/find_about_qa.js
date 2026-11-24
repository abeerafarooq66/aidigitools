const fs = require('fs');
const c = fs.readFileSync('about.html', 'utf8');
const matches = Array.from(c.matchAll(/class=["'][^"']*quick-answer[^"']*["']/g));
console.log('Matches count:', matches.length);
matches.forEach((m, i) => {
  const start = Math.max(0, m.index - 50);
  const end = Math.min(c.length, m.index + 150);
  console.log(`Match ${i}:\n`, c.slice(start, end));
});
