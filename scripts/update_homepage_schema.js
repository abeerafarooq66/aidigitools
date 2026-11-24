const fs = require('fs');

const indexPath = 'index.html';
let html = fs.readFileSync(indexPath, 'utf8');

const m = html.match(/<script\s+type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/i);
if (m) {
  const data = JSON.parse(m[1].trim());
  const graph = data['@graph'] || [data];
  
  // Organization update
  const org = graph.find(n => n['@type'] === 'Organization');
  if (org) {
    org.telephone = "+92-332-6861112";
    org.email = "support@aidigitools.tech";
  }

  // WebSite update
  const ws = graph.find(n => n['@type'] === 'WebSite');
  if (ws) {
    ws.potentialAction = {
      "@type": "SearchAction",
      "target": "https://aidigitools.tech/?q={search_term_string}",
      "query-input": "required name=search_term_string"
    };
  }

  const newJsonStr = JSON.stringify(data, null, 2);
  html = html.replace(m[0], `<script type="application/ld+json">\n${newJsonStr}\n  </script>`);
  fs.writeFileSync(indexPath, html, 'utf8');
  console.log('Successfully updated homepage schema in index.html');
} else {
  console.error('Could not find JSON-LD in index.html');
}
