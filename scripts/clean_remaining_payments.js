const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const toolsDir = path.join(repoRoot, 'tools');

function cleanFile(fileName, transforms) {
  const filePath = path.join(toolsDir, fileName);
  if (!fs.existsSync(filePath)) return;
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;
  transforms.forEach(([target, replacement]) => {
    if (typeof target === 'string') {
      content = content.replaceAll(target, replacement);
    } else {
      content = content.replace(target, replacement);
    }
  });
  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Cleaned ${fileName}`);
  }
}

// 1. gamma-app.html
cleanFile('gamma-app.html', [
  [
    'EasyPaisa, Wise rails. 15-min delivery',
    'domestic and international payment. 15-min delivery'
  ]
]);

// 2. google-ai-ultra.html
cleanFile('google-ai-ultra.html', [
  [
    'via EasyPaisa, JazzCash, or bank transfer with zero forex transaction surcharges.',
    'via domestic bank transfer (IBFT/Raast) or local digital wallets with zero forex transaction surcharges.'
  ]
]);

// 3. heygen-ai.html
cleanFile('heygen-ai.html', [
  [
    'EasyPaisa, Wise. 15-min delivery',
    'domestic and international payment. 15-min delivery'
  ]
]);

// 4. microsoft-office-365.html
cleanFile('microsoft-office-365.html', [
  [
    'EasyPaisa, Wise. 15-min delivery',
    'domestic and international payment. 15-min delivery'
  ],
  [
    'using EasyPaisa, JazzCash, or bank transfer.',
    'using domestic bank transfer (IBFT/Raast) or local digital wallets.'
  ]
]);

// 5. vidiq-boost.html
cleanFile('vidiq-boost.html', [
  [
    'EasyPaisa, Wise. 15-min delivery',
    'domestic and international payment. 15-min delivery'
  ],
  [
    'EasyPaisa, JazzCash, SadaPay, NayaPay, Bank IBFT, Wise, and Binance Pay USDT.',
    'Domestic bank transfers (IBFT/Raast), local digital wallets, Wise, and Binance Pay USDT. See <a href="../policies.html#payments">Payment Policy</a>.'
  ]
]);
