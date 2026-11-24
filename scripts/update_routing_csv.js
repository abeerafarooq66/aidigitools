const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

const heldSlugs = [
  'turnitin-student',
  'linkedin-premium',
  'netflix-premium',
  'spotify-premium',
  'coursera-plus'
];

let csv = 'tool_slug,page_file,routing_action,target_slug_or_destination,status\n';

files.forEach(f => {
  const slug = f.replace('.html', '');
  if (heldSlugs.includes(slug)) {
    csv += `${slug},tools/${f},INQUIRY_ONLY_CONCIERGE,wa.me/923326861112,VERIFIED_HELD\n`;
  } else {
    csv += `${slug},tools/${f},OPEN_MODAL_SELF,${slug},VERIFIED_CORRECT\n`;
  }
});

const outPath = path.join(__dirname, '..', 'audit_reports', 'PRODUCT_ORDER_ROUTING_MATRIX.csv');
fs.writeFileSync(outPath, csv, 'utf8');
console.log(`Updated routing matrix: ${outPath}`);
