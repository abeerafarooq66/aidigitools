const fs = require('fs');
const path = require('path');

function getFiles(dir) {
  let res = [];
  fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
    if (e.name.startsWith('.') || ['node_modules', 'tests', 'scratch', 'data', 'admin', 'private'].includes(e.name)) return;
    const f = path.join(dir, e.name);
    if (e.isDirectory()) res = res.concat(getFiles(f));
    else if (f.endsWith('.html')) res.push(f);
  });
  return res;
}

const files = getFiles('.');
console.log(`Scanning ${files.length} HTML files for duplicate schemas...`);

files.forEach(f => {
  const content = fs.readFileSync(f, 'utf8');
  const matches = Array.from(content.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi));
  const types = [];
  matches.forEach(m => {
    try {
      const data = JSON.parse(m[1].trim());
      if (data['@graph'] && Array.isArray(data['@graph'])) {
        data['@graph'].forEach(node => {
          if (node && node['@type']) types.push(node['@type']);
        });
      } else if (data['@type']) {
        types.push(data['@type']);
      }
    } catch (e) {
      console.log(`JSON parse error in ${f}: ${e.message}`);
    }
  });

  const counts = {};
  types.forEach(t => counts[t] = (counts[t] || 0) + 1);
  ['Product', 'WebSite', 'AboutPage', 'ContactPage', 'CollectionPage'].forEach(t => {
    if (counts[t] > 1) {
      console.log(`[DUPLICATE SCHEMA] ${f} has ${counts[t]} instances of @type: "${t}"`);
    }
  });
});
