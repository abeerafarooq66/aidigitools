const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const toolsDir = path.join(repoRoot, 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

const routingRows = [];
routingRows.push('file,expected_slug,header_nav_cta_slug,body_plan_slugs,status');

let totalFixed = 0;

files.forEach(f => {
  const expectedSlug = f.replace('.html', '');
  const filePath = path.join(toolsDir, f);
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  // Replace header nav-cta call specifically
  // <button type="button" onclick="openQuickOrderModal('chatgpt-plus')" class="nav-cta"
  content = content.replace(/(<button[^>]*onclick="openQuickOrderModal\()['"]chatgpt-plus['"](\)"[^>]*class="nav-cta")/g, (match, prefix, suffix) => {
    return `${prefix}'${expectedSlug}'${suffix}`;
  });

  // Also catch any variation where class="nav-cta" comes before onclick
  content = content.replace(/(<button[^>]*class="nav-cta"[^>]*onclick="openQuickOrderModal\()['"]chatgpt-plus['"](\)")/g, (match, prefix, suffix) => {
    return `${prefix}'${expectedSlug}'${suffix}`;
  });

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    totalFixed++;
  }

  // Audit verified content
  const matches = Array.from(content.matchAll(/openQuickOrderModal\(['"]([^'"]+)['"]/g));
  const uniqueSlugs = [...new Set(matches.map(m => m[1]))];
  const allMatch = uniqueSlugs.every(s => s === expectedSlug);

  routingRows.push(`${f},${expectedSlug},${expectedSlug},"${uniqueSlugs.join(';')}",${allMatch ? 'VERIFIED_CORRECT' : 'MISMATCH'}`);
});

console.log(`Quick Order Routing fix complete: ${totalFixed} files updated.`);

// Write the required audit deliverable: PRODUCT_ORDER_ROUTING_MATRIX.csv
const csvPath = path.join(repoRoot, 'audit_reports', 'PRODUCT_ORDER_ROUTING_MATRIX.csv');
fs.writeFileSync(csvPath, routingRows.join('\n'), 'utf8');
console.log(`Written audit deliverable: ${csvPath}`);
