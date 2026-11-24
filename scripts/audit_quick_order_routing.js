const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

const routingAudit = [];

files.forEach(f => {
  const expectedSlug = f.replace('.html', '');
  const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  
  // Find all openQuickOrderModal calls
  const matches = Array.from(content.matchAll(/openQuickOrderModal\(['"]([^'"]+)['"]\)/g));
  
  const foundSlugs = matches.map(m => m[1]);
  const mismatches = matches.filter(m => m[1] !== expectedSlug);
  
  routingAudit.push({
    file: f,
    expectedSlug,
    totalCalls: matches.length,
    foundSlugs: [...new Set(foundSlugs)],
    mismatches: mismatches.map(m => m[1])
  });
});

console.log('=== QUICK ORDER ROUTING AUDIT ===');
const problematic = routingAudit.filter(r => r.mismatches.length > 0);
console.log(`Total files with routing mismatches: ${problematic.length} / ${files.length}`);

problematic.forEach(p => {
  console.log(`\n[${p.file}] Expected: '${p.expectedSlug}' | Found: ${JSON.stringify(p.foundSlugs)} | Mismatches: ${JSON.stringify(p.mismatches)}`);
});
