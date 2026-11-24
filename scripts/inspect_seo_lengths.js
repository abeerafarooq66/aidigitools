const fs = require('fs');

const files = [
  'guides/how-to-pay-for-ai-tools-in-pakistan.html',
  'about.html',
  'deals.html',
  'tools/claude-pro.html',
  'tools/cursor-pro.html'
];

files.forEach(f => {
  const content = fs.readFileSync(f, 'utf8');
  const titleM = content.match(/<title>([\s\S]*?)<\/title>/i);
  const descM = content.match(/<meta\s+name=["']description["']\s+content=["']([\s\S]*?)["']/i);
  const qaM = content.match(/<p class=["']quick-answer["'][^>]*>([\s\S]*?)<\/p>/i);
  
  console.log(`=== ${f} ===`);
  if (titleM) console.log(`Title (${titleM[1].length} chars): ${titleM[1]}`);
  if (descM) console.log(`Desc (${descM[1].length} chars): ${descM[1]}`);
  if (qaM) {
    const words = qaM[1].trim().split(/\s+/).filter(Boolean);
    console.log(`QA (${words.length} words): ${qaM[1].trim()}`);
  }
});
