const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');

const targetFiles = [
  'best/best-ai-coding-tools.html',
  'categories/coding.html',
  'categories/image.html',
  'compare/chatgpt-vs-claude.html',
  'guides/chatgpt-vs-claude.html',
  'index.html',
  '404.html',
  'blog.html',
  'llms.txt',
  'llms-full.txt',
  'data/central_product_registry.json',
  'data/discovered_urls_registry.json',
  'data/business_claims_inventory.json',
  'assets/product-logos/brand_logos_manifest.json'
];

let totalModified = 0;

targetFiles.forEach(relPath => {
  const fullPath = path.join(repoRoot, relPath);
  if (!fs.existsSync(fullPath)) return;
  let content = fs.readFileSync(fullPath, 'utf8');
  const original = content;

  // 1. Anthropic models
  content = content.replace(/Claude Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
  content = content.replace(/Sonnet 5\.5/g, 'Claude 3.5 Sonnet');
  content = content.replace(/Opus 5\.5/g, 'Claude 3 Opus');

  // 2. OpenAI models
  content = content.replace(/GPT-5\.5\s*\/\s*GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\s*\/\s*GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\/GPT-6/g, 'OpenAI o1 & GPT-4o');
  content = content.replace(/GPT-5\/4o/g, 'GPT-4o');
  content = content.replace(/OpenAI o1\/o3/g, 'OpenAI o1 & o1-mini');
  content = content.replace(/o1\/o3/g, 'OpenAI o1');

  // 3. Midjourney
  content = content.replace(/Midjourney V8/g, 'Midjourney v6.1');
  content = content.replace(/Midjourney 8/g, 'Midjourney v6.1');

  // 4. Cursor requests
  content = content.replace(/2600 fast requests/g, '500 fast requests');

  if (content !== original) {
    fs.writeFileSync(fullPath, content, 'utf8');
    totalModified++;
    console.log(`Grounded models in: ${relPath}`);
  }
});

console.log(`Master Repo Grounding complete: ${totalModified} files updated.`);
