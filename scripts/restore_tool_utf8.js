const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const repoDir = 'C:\\Users\\Dell\\.gemini\\antigravity\\scratch\\aidigitools';
const toolsDir = path.join(repoDir, 'tools');

const toolFiles = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));
console.log(`Processing ${toolFiles.length} tool files for UTF-8 restoration...`);

let restoredCount = 0;
let errors = [];

for (const file of toolFiles) {
  const filePath = path.join(toolsDir, file);
  try {
    // 1. Get the pre-corruption content from git commit eee2c84~1
    const cleanContentBuffer = execSync(`git show eee2c84~1:tools/${file}`, {
      cwd: repoDir,
      maxBuffer: 10 * 1024 * 1024
    });
    const cleanContent = cleanContentBuffer.toString('utf8');

    // 2. Read current content (which has the schema returnMethod fix)
    const currentContent = fs.readFileSync(filePath, 'utf8');

    // 3. We want to keep the valid schema fix (returnMethod removal) while restoring all the clean Unicode text, emojis, and symbols!
    // Notice that commit eee2c84 ONLY changed the schema hasMerchantReturnPolicy (removing returnMethod: "https://schema.org/ReturnByMail")
    // and simultaneously mangled the non-ASCII bytes.
    // So if we take the cleanContent, and apply ONLY the schema fix (removing invalid returnMethod enum) properly in UTF-8:
    let fixedContent = cleanContent;
    
    // Check if returnMethod exists in cleanContent
    if (fixedContent.includes('"returnMethod":')) {
      fixedContent = fixedContent.replace(/\s*"returnMethod":\s*"https:\/\/schema\.org\/ReturnByMail",?/g, '');
      // Clean up any trailing commas if needed in JSON
      fixedContent = fixedContent.replace(/,(\s*})/g, '$1');
    }

    // 4. Save with strict UTF-8 (no BOM)
    fs.writeFileSync(filePath, fixedContent, { encoding: 'utf8' });
    restoredCount++;
  } catch (err) {
    errors.push({ file, error: err.message });
  }
}

console.log(`Successfully restored UTF-8 clean content across ${restoredCount} tool pages!`);
if (errors.length > 0) {
  console.error('Errors encountered:', errors);
}
