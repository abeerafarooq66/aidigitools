const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');

// 1. Gather all HTML files
const htmlFiles = [];
function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.git') || entry.name === 'node_modules' || entry.name === 'audit_reports') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanDir(full);
    } else if (entry.name.endsWith('.html')) {
      htmlFiles.push(full);
    }
  }
}
scanDir(repoRoot);

console.log(`=== FULL REPOSITORY VALIDATION ===`);
console.log(`Total HTML files scanned: ${htmlFiles.length}`);

// 2. Encoding check
let encodingErrors = 0;
htmlFiles.forEach(file => {
  const buf = fs.readFileSync(file);
  if (buf.includes(Buffer.from([0xef, 0xbf, 0xbd]))) {
    console.error(`[ENCODING ERROR] Replacement character found in: ${path.relative(repoRoot, file)}`);
    encodingErrors++;
  }
});
console.log(`Encoding check: ${encodingErrors === 0 ? 'PASSED (0 errors)' : `FAILED (${encodingErrors} files)`}`);

// 3. Payment keyword cannibalization check in tools/
const toolsDir = path.join(repoRoot, 'tools');
const toolFiles = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));
let toolPaymentKeywordLines = 0;
toolFiles.forEach(file => {
  const content = fs.readFileSync(path.join(toolsDir, file), 'utf8');
  content.split('\n').forEach((l) => {
    if (/sadapay|easypaisa|jazzcash|nayapay/i.test(l)) {
      if (!l.includes('rail-option') && !l.includes('<span>')) {
        toolPaymentKeywordLines++;
      }
    }
  });
});
console.log(`Payment keyword cannibalization check: ${toolPaymentKeywordLines === 0 ? 'PASSED (0 non-cart occurrences)' : `FAILED (${toolPaymentKeywordLines} non-cart occurrences)`}`);

// 4. Meta & Schema integrity check
let missingH1 = 0;
let missingTitle = 0;
let missingCanonical = 0;
let missingSchema = 0;

htmlFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf8');
  const rel = path.relative(repoRoot, file);
  if (!content.includes('<h1')) {
    // some admin or private pages might skip
    if (!rel.startsWith('admin') && !rel.startsWith('private')) missingH1++;
  }
  if (!content.includes('<title>')) missingTitle++;
  if (!content.includes('<link rel="canonical"')) {
    if (!rel.startsWith('admin') && !rel.startsWith('private')) missingCanonical++;
  }
  if (!content.includes('application/ld+json')) {
    if (!rel.startsWith('admin') && !rel.startsWith('private')) missingSchema++;
  }
});

console.log(`Structural checks across public pages:`);
console.log(` - Missing H1: ${missingH1}`);
console.log(` - Missing Title: ${missingTitle}`);
console.log(` - Missing Canonical: ${missingCanonical}`);
console.log(` - Missing Schema: ${missingSchema}`);

// 5. Check Top 15 tools model accuracy
const topCheck = [
  ['claude-pro.html', 'Claude 3.5 Sonnet', 'Claude Sonnet 5.5'],
  ['chatgpt-plus.html', 'OpenAI o1', 'GPT-5 / GPT-6'],
  ['midjourney.html', 'Midjourney v6.1', 'Midjourney V8'],
  ['cursor-pro.html', '500 Fast Premium Requests', '2600 Fast Premium Requests'],
  ['turnitin-student.html', '100% Non-Repository Protection', '']
];

console.log(`Top tools grounding & Master Book V2 checks:`);
topCheck.forEach(([file, mustHave, mustNotHave]) => {
  const content = fs.readFileSync(path.join(toolsDir, file), 'utf8');
  const hasGood = content.includes(mustHave);
  const hasBad = mustNotHave ? content.includes(mustNotHave) : false;
  console.log(` - ${file}: ${hasGood && !hasBad ? 'PASSED' : `FAILED (hasGood: ${hasGood}, hasBad: ${hasBad})`}`);
});

console.log(`=== VALIDATION RUN COMPLETE ===`);
