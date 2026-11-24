const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');

const targetFiles = [
  'data/products_master.json',
  'data/topic_opportunity_registry.json',
  'whatsapp_assets/03_WhatsApp_Setup_Details.txt',
  'whatsapp_assets/WhatsApp_Business_AIDigiTools/03_WhatsApp_Setup_Details.txt'
];

targetFiles.forEach(relPath => {
  const fullPath = path.join(repoRoot, relPath);
  if (!fs.existsSync(fullPath)) return;
  let content = fs.readFileSync(fullPath, 'utf8');

  content = content.replace(/Claude Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
  content = content.replace(/Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
  content = content.replace(/Opus 5\.5/g, 'Claude 3 Opus');
  content = content.replace(/Haiku 5\.5/g, 'Claude 3.5 Haiku');

  content = content.replace(/GPT-5\.5\s*\/\s*GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\s*\/\s*GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\/GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\/4o/g, 'GPT-4o');
  content = content.replace(/GPT-6/g, 'GPT-4o');
  content = content.replace(/GPT-5\.5/g, 'GPT-4o');

  content = content.replace(/Midjourney V8(?:\s*\/\s*V8\.2)?/g, 'Midjourney v6.1');
  content = content.replace(/Midjourney 8/g, 'Midjourney v6.1');

  fs.writeFileSync(fullPath, content, 'utf8');
  console.log(`Grounded models in: ${relPath}`);
});

// Also check index.html line 520
const indexPath = path.join(repoRoot, 'index.html');
let indexContent = fs.readFileSync(indexPath, 'utf8');
indexContent = indexContent.replace(/GPT-5\/GPT-6/g, 'OpenAI o1 & GPT-4o');
indexContent = indexContent.replace(/Claude Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
indexContent = indexContent.replace(/Midjourney V8/g, 'Midjourney v6.1');
fs.writeFileSync(indexPath, indexContent, 'utf8');
console.log('Grounded index.html completely.');
