const fs = require('fs');
const path = require('path');

const topTools = [
  'claude-pro.html',
  'chatgpt-plus.html',
  'cursor-pro.html',
  'turnitin-student.html',
  'midjourney.html',
  'canva-pro.html',
  'runway-gen3.html',
  'capcut-pro.html',
  'deepseek-pro.html',
  'elevenlabs-creator.html',
  'github-copilot.html',
  'youtube-premium.html',
  'nordvpn.html',
  'surfshark-vpn.html',
  'semrush-guru.html'
];

topTools.forEach(file => {
  const filePath = path.join(__dirname, '..', 'tools', file);
  if (!fs.existsSync(filePath)) {
    console.log(`MISSING: ${file}`);
    return;
  }
  const content = fs.readFileSync(filePath, 'utf8');
  const h1Match = content.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  const cardH3s = Array.from(content.matchAll(/<div class="card">\s*<h3[^>]*>([\s\S]*?)<\/h3>/gi)).map(m => m[1].trim());
  console.log(`\n=== ${file} ===`);
  console.log(`H1: ${h1Match ? h1Match[1].trim() : 'N/A'}`);
  console.log(`Feature Cards: ${cardH3s.join(' | ')}`);
});
