const fs = require('fs');
const lines = fs.readFileSync('assets/cart.js', 'utf8').split('\n');

const toolSlugs = [];
lines.forEach((l, i) => {
  const m = l.match(/^"([a-z0-9-]+)":\s*\{/);
  if (m) toolSlugs.push(m[1]);
});

console.log('Total tool slugs defined in cart.js:', toolSlugs.length);
console.log(toolSlugs);
