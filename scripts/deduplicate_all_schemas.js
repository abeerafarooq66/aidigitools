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
let totalModified = 0;

files.forEach(f => {
  let content = fs.readFileSync(f, 'utf8');
  let changed = false;

  const matches = Array.from(content.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi));
  matches.forEach(m => {
    try {
      const data = JSON.parse(m[1].trim());
      if (data['@graph'] && Array.isArray(data['@graph'])) {
        const seen = new Set();
        const cleanNodes = [];
        data['@graph'].forEach(node => {
          if (!node || !node['@type']) return;
          const type = node['@type'];
          const id = node['@id'] || '';
          const key = `${type}::${id}`;
          if (!seen.has(key)) {
            seen.add(key);
            // Also ensure isPartOf is not an embedded WebSite object
            if (node.isPartOf && typeof node.isPartOf === 'object' && node.isPartOf['@type'] === 'WebSite') {
              node.isPartOf = { "@id": "https://aidigitools.tech/#website" };
              changed = true;
            }
            cleanNodes.push(node);
          } else {
            changed = true;
          }
        });

        if (cleanNodes.length !== data['@graph'].length || changed) {
          data['@graph'] = cleanNodes;
          const newJson = JSON.stringify(data, null, 2);
          content = content.replace(m[0], `<script type="application/ld+json">\n${newJson}\n  </script>`);
        }
      }
    } catch (e) {
      console.log(`JSON parse error in ${f}: ${e.message}`);
    }
  });

  if (changed) {
    fs.writeFileSync(f, content, 'utf8');
    totalModified++;
    console.log(`Deduplicated schema in ${f}`);
  }
});

console.log(`Deduplicated schemas across ${totalModified} files.`);
