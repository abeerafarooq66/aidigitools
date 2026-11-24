const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

const patterns = {};
const samples = {};

files.forEach(f => {
  const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
  const lines = content.split('\n');
  lines.forEach((l, idx) => {
    if (/sadapay|easypaisa|jazzcash|nayapay/i.test(l)) {
      const trimmed = l.trim();
      let key = 'other';
      if (trimmed.startsWith('<meta property="og:description"') || trimmed.startsWith('<meta name="twitter:description"')) {
        key = 'meta_desc';
      } else if (trimmed.includes('"description":') && trimmed.includes('Paid orders accepted')) {
        key = 'schema_desc';
      } else if (trimmed.includes('Manual payment via SadaPay')) {
        key = 'plan_card_note';
      } else if (trimmed.includes('Verified Rails:')) {
        key = 'footer_rails';
      } else if (trimmed.includes('rail-option')) {
        key = 'cart_rail_modal';
      } else if (trimmed.includes('We accept') || trimmed.includes('we accept')) {
        key = 'faq_or_body_we_accept';
      } else if (trimmed.startsWith('<td>') && trimmed.includes('EasyPaisa')) {
        key = 'table_payment_row';
      }
      patterns[key] = (patterns[key] || 0) + 1;
      if (!samples[key]) {
        samples[key] = { file: f, line: idx + 1, text: trimmed };
      }
    }
  });
});

console.log('Total files scanned:', files.length);
console.log('Pattern counts:', JSON.stringify(patterns, null, 2));
console.log('\nSamples:');
Object.keys(samples).forEach(k => {
  console.log(`\n[${k}] in ${samples[k].file}:${samples[k].line}`);
  console.log('  ' + samples[k].text.substring(0, 150));
});
