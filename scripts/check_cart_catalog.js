const fs = require('fs');
const cart = fs.readFileSync('assets/cart.js', 'utf8');

const match = cart.match(/const\s+(?:TOOLS_CATALOG|TOOLS_DATA|toolsCatalog)\s*=\s*(\{[\s\S]*?\n\};)/i);
if (match) {
  try {
    const catalog = eval('(' + match[1].replace(/;\s*$/, '') + ')');
    console.log('Tools catalog keys count:', Object.keys(catalog).length);
    console.log('Keys:', Object.keys(catalog));
  } catch (e) {
    console.error('Eval error:', e.message);
  }
} else {
  console.log('Checking first 100 lines of cart.js:');
  console.log(cart.split('\n').slice(0, 40).join('\n'));
}
