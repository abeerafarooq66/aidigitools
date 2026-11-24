const fs = require('fs');

const blogPath = 'blog.html';
let html = fs.readFileSync(blogPath, 'utf8');

const m = html.match(/<script\s+type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/i);
if (m) {
  const data = JSON.parse(m[1].trim());
  if (data['@graph'] && Array.isArray(data['@graph'])) {
    const seen = new Set();
    const cleanNodes = [];
    data['@graph'].forEach(node => {
      const type = node['@type'];
      const id = node['@id'] || '';
      const key = `${type}::${id}`;
      if (!seen.has(key)) {
        seen.add(key);
        cleanNodes.push(node);
      }
    });
    data['@graph'] = cleanNodes;
    const newJson = JSON.stringify(data, null, 2);
    html = html.replace(m[0], `<script type="application/ld+json">\n${newJson}\n  </script>`);
    fs.writeFileSync(blogPath, html, 'utf8');
    console.log(`Cleaned blog.html schema: reduced from ${data['@graph'].length + (seen.size - cleanNodes.length)} to ${cleanNodes.length} nodes.`);
  }
}
