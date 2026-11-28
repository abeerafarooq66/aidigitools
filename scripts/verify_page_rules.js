const fs = require('fs');
const path = require('path');

const targetFile = process.argv[2];
if (!targetFile) {
  console.error("Usage: node scripts/verify_page_rules.js <path-to-html>");
  process.exit(1);
}

const fullPath = path.isAbsolute(targetFile) ? targetFile : path.join(process.cwd(), targetFile);
if (!fs.existsSync(fullPath)) {
  console.error(`File not found: ${fullPath}`);
  process.exit(1);
}

const html = fs.readFileSync(fullPath, 'utf8');

const titleMatch = html.match(/<title>(.*?)<\/title>/i);
const title = titleMatch ? titleMatch[1].trim() : '';

const descMatch = html.match(/<meta\s+name=["']description["']\s+content=["'](.*?)["']/i);
const desc = descMatch ? descMatch[1].trim() : '';

const qaMatch = html.match(/<p class=["']quick-answer["']>([\s\S]*?)<\/p>/i);
const qa = qaMatch ? qaMatch[1].replace(/<[^>]+>/g, ' ').trim() : '';
const qaWords = qa ? qa.split(/\s+/).filter(Boolean).length : 0;

const bodyMatch = html.match(/<body[\s\S]*?<\/body>/i);
const bodyHtml = bodyMatch ? bodyMatch[0] : '';
const bodyBackticks = (bodyHtml.match(/`/g) || []).length;

const jsonLdMatch = html.match(/<script type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/i);
let validJson = false;
let jsonError = null;
if (jsonLdMatch) {
  try {
    JSON.parse(jsonLdMatch[1]);
    validJson = true;
  } catch (e) {
    jsonError = e.message;
  }
}

const errors = [];
if (!title) errors.push("Missing <title>");
else if (title.length < 30 || title.length > 60) errors.push(`Title length ${title.length} is outside 30-60 characters ("${title}")`);

if (!desc) errors.push("Missing <meta name='description'>");
else if (desc.length < 70 || desc.length > 160) errors.push(`Meta description length ${desc.length} is outside 70-160 characters ("${desc}")`);

if (!qa) errors.push("Missing <p class='quick-answer'>");
else if (qaWords < 35 || qaWords > 70) errors.push(`Quick answer word count ${qaWords} is outside 35-70 words`);

if (bodyBackticks > 0) errors.push(`Found ${bodyBackticks} literal backticks inside <body> tag`);

if (!jsonLdMatch) errors.push("Missing JSON-LD schema block");
else if (!validJson) errors.push(`Invalid JSON in JSON-LD schema: ${jsonError}`);

console.log(`=== Verification for ${path.basename(fullPath)} ===`);
console.log(`Title (${title.length} chars): "${title}"`);
console.log(`Description (${desc.length} chars): "${desc}"`);
console.log(`Quick Answer (${qaWords} words): "${qa.slice(0, 80)}..."`);
console.log(`Body Backticks: ${bodyBackticks}`);
console.log(`JSON-LD Valid: ${validJson}`);

if (errors.length > 0) {
  console.error("FAILURES DETECTED:");
  errors.forEach(e => console.error(" - " + e));
  process.exit(1);
} else {
  console.log("ALL LOCAL PAGE RULES PASSED!");
  process.exit(0);
}
