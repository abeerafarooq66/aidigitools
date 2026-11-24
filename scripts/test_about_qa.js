const fs = require('fs');
const c = fs.readFileSync('about.html', 'utf8');

const regex1 = /<([a-z0-9]+)\s+[^>]*class=["'][^"']*quick-answer[^"']*["'][^>]*>([\s\S]*?)<\/\1>/i;
const match1 = c.match(regex1);
console.log('Regex 1 matched?', !!match1);
if (match1) {
  const text = match1[2].replace(/<[^>]+>/g, '').trim();
  const words = text.split(/\s+/).filter(Boolean);
  console.log('Words count:', words.length);
}

const regex2 = /<[a-z0-9]+\s+[^>]*class=["'][^"']*quick-answer[^"']*["'][^>]*>([\s\S]*?)<\/[a-z0-9]+>/i;
const match2 = c.match(regex2);
console.log('Regex 2 matched?', !!match2);
if (match2) {
  const text = match2[1].replace(/<[^>]+>/g, '').trim();
  const words = text.split(/\s+/).filter(Boolean);
  console.log('Words count 2:', words.length);
  console.log('Match 2 full text:\n', match2[0]);
}
