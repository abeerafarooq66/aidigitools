const fs = require('fs');
const path = require('path');

const toolsDir = 'tools';
const inStockTools = [];
const outOfStockTools = [];

fs.readdirSync(toolsDir).filter(f => f.endsWith('.html')).forEach(f => {
  const c = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  if (c.includes('https://schema.org/InStock') || c.includes('"availability": "https://schema.org/InStock"') || c.includes('"availability":  "https://schema.org/InStock"')) {
    inStockTools.push(f);
  } else if (c.includes('https://schema.org/OutOfStock') || c.includes('"availability": "https://schema.org/OutOfStock"') || c.includes('"availability":  "https://schema.org/OutOfStock"')) {
    outOfStockTools.push(f);
  } else {
    console.log('UNKNOWN AVAILABILITY:', f);
  }
});

console.log(`InStock tools (${inStockTools.length}):`, inStockTools);
console.log(`OutOfStock tools (${outOfStockTools.length}):`, outOfStockTools.length);
