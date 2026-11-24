const fs = require('fs');
const path = require('path');

const toolsDir = path.join(__dirname, '..', 'tools');
const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

let totalChanges = 0;

files.forEach(f => {
  const filePath = path.join(toolsDir, f);
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  content = content.replace(/Claude Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
  content = content.replace(/Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
  content = content.replace(/GPT-5\.5\s*\/\s*GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\s*\/\s*GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\/GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\/4o/g, 'GPT-4o');
  content = content.replace(/GPT-6/g, 'GPT-4o');
  content = content.replace(/GPT-5\.5/g, 'GPT-4o');
  content = content.replace(/2600 priority fast requests/g, '500 priority fast requests');
  content = content.replace(/in Pakistan in Pakistan/g, 'in Pakistan');

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    totalChanges++;
    console.log(`Cleaned ${f}`);
  }
});

console.log(`Total files cleaned: ${totalChanges}`);
