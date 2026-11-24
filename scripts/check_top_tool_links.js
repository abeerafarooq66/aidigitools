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
  const content = fs.readFileSync(path.join(__dirname, '..', 'tools', file), 'utf8');
  const links = Array.from(content.matchAll(/href="([^"]+)"/g)).map(m => m[1]);
  const catLinks = links.filter(l => l.includes('categories/'));
  const compLinks = links.filter(l => l.includes('compare/') || l.includes('guides/chatgpt'));
  const bestLinks = links.filter(l => l.includes('best/'));
  console.log(`[${file}] Category links: ${catLinks.length}, Comparison links: ${compLinks.length}, Best links: ${bestLinks.length}`);
});
