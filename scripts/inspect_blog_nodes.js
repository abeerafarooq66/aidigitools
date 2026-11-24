const fs = require('fs');
const html = fs.readFileSync('blog.html', 'utf8');
const m = html.match(/<script\s+type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/i);
const data = JSON.parse(m[1].trim());
console.log('Nodes in blog.html:');
data['@graph'].forEach((n, i) => console.log(i, n['@type'], n['@id']));
