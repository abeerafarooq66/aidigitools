const fs = require('fs');
const c = fs.readFileSync('guides/how-to-pay-for-ai-tools-in-pakistan.html', 'utf8');
const qa_m = c.match(/<p[^>]*class=["']quick-answer["'][^>]*>([\s\S]*?)<\/p>/i);
if (qa_m) {
  console.log('FULL MATCH:\n', qa_m[0]);
  console.log('GROUP 1:\n', qa_m[1]);
  const clean = qa_m[1].replace(/<[^>]+>/g, '').trim();
  console.log('CLEAN TEXT:\n', clean);
  console.log('WORDS:', clean.split(/\s+/));
  console.log('WORD COUNT:', clean.split(/\s+/).length);
} else {
  console.log('NO MATCH');
}
