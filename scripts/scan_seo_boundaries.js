const fs = require('fs');
const path = require('path');

function getFiles(dir) {
  let res = [];
  fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
    if (e.name.startsWith('.') || ['node_modules', 'tests', 'scratch', 'data', 'admin', 'private'].includes(e.name)) return;
    const f = path.join(dir, e.name);
    if (e.isDirectory()) res = res.concat(getFiles(f));
    else if (f.endsWith('.html') && !f.endsWith('404.html')) res.push(f);
  });
  return res;
}

const files = getFiles('.');
console.log(`Scanning ${files.length} HTML files...`);

files.forEach(f => {
  const c = fs.readFileSync(f, 'utf8');
  
  // Title
  const tm = c.match(/<title>([^<]*)<\/title>/i);
  const t = tm ? tm[1].trim() : '';
  if (t.length < 30 || t.length > 65) {
    console.log(`[TITLE VIOLATION] ${f}: length ${t.length} (expected 30-65) -> "${t}"`);
  }

  // Meta Description
  const dm = c.match(/<meta[^>]*name=["']description["'][^>]*content=(["'])(.*?)\1/i);
  const d = dm ? dm[2].trim() : '';
  if (d.length < 70 || d.length > 165) {
    console.log(`[DESC VIOLATION] ${f}: length ${d.length} (expected 70-165) -> "${d}"`);
  }

  // Quick Answer
  const qm = c.match(/<[a-z0-9]+\s+[^>]*class=["'][^"']*quick-answer[^"']*["'][^>]*>([\s\S]*?)<\/[a-z0-9]+>/i);
  if (qm) {
    const text = qm[1].replace(/<[^>]+>/g, '').trim();
    const words = text.split(/\s+/).filter(Boolean);
    if (words.length < 35 || words.length > 70) {
      console.log(`[QA VIOLATION] ${f}: word count ${words.length} (expected 35-70) -> "${text.slice(0, 60)}..."`);
    }
  } else {
    console.log(`[QA MISSING] ${f}`);
  }
});
