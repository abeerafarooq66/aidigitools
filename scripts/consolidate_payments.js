const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const toolsDir = path.join(repoRoot, 'tools');
const toolFiles = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));

let totalReplacements = 0;
const fileStats = {};

toolFiles.forEach(file => {
  const filePath = path.join(toolsDir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;
  let count = 0;

  // 1. Meta descriptions & og/twitter descriptions remaining
  content = content.replace(/Pay via EasyPaisa or JazzCash\.\s*/gi, () => {
    count++;
    return 'Fast WhatsApp delivery with local payment support. ';
  });
  content = content.replace(/(?:with|via|Pay via|using)\s+(?:EasyPaisa,\s*JazzCash,?\s*(?:and|or)\s*SadaPay|EasyPaisa\s*or\s*JazzCash|SadaPay,\s*NayaPay,?\s*(?:and|or)\s*EasyPaisa|EasyPaisa,\s*JazzCash,\s*SadaPay,?\s*(?:and|or)\s*Raast)\.?/gi, (match) => {
    count++;
    return 'with fast local payment & 15-minute delivery.';
  });

  // 2. Schema description & quotes
  content = content.replace(/,\s*EasyPaisa\.\s*15-min/g, () => {
    count++;
    return '. 15-min';
  });
  content = content.replace(/Paid orders accepted via WhatsApp with manual payment confirmation \(SadaPay, NayaPay, EasyPaisa\)\./g, () => {
    count++;
    return 'Paid orders accepted via WhatsApp with manual payment verification via domestic transfer, local wallets, or Wise/USDT. Covered by 30-day replacement warranty.';
  });

  // 3. Quick answers
  content = content.replace(/payable (?:via|with|through) (?:JazzCash|EasyPaisa|SadaPay|Raast)[^,.]*(?:with 15-minute WhatsApp setup \(\+92 332 6861112\))?/gi, (match) => {
    count++;
    return 'with local payment facilitation and 15-minute WhatsApp setup (+92 332 6861112)';
  });

  // 4. Reseller notice variations
  content = content.replace(/domestic payment processing \(EasyPaisa, JazzCash, Raast, Bank Transfer(?:, Wise)?, USDT\)/g, () => {
    count++;
    return 'domestic and international payment facilitation (Bank IBFT, Raast, local digital wallets, Wise, USDT)';
  });
  content = content.replace(/domestic Pakistani payment processing \(EasyPaisa, JazzCash, Raast, Bank Transfer(?:, Wise)?, USDT\)/g, () => {
    count++;
    return 'domestic and international payment facilitation (Bank IBFT, Raast, local digital wallets, Wise, USDT)';
  });

  // 5. FAQ questions & text
  content = content.replace(/How do I pay for Spotify Premium with EasyPaisa or JazzCash\?/g, () => {
    count++;
    return 'How do I pay for Spotify Premium locally in Pakistan?';
  });
  content = content.replace(/using EasyPaisa, JazzCash, SadaPay, or Bank IBFT/g, () => {
    count++;
    return 'using domestic bank transfer (IBFT/Raast) or local digital wallets';
  });
  content = content.replace(/using EasyPaisa, JazzCash, SadaPay, Raast, or Bank IBFT/g, () => {
    count++;
    return 'using domestic bank transfer (IBFT/Raast) or local digital wallets';
  });
  content = content.replace(/transfer the PKR amount via EasyPaisa, JazzCash, or SadaPay/g, () => {
    count++;
    return 'transfer the PKR amount via domestic bank transfer or local digital wallets';
  });
  content = content.replace(/via EasyPaisa, JazzCash, SadaPay, and Raast/g, () => {
    count++;
    return 'via domestic bank transfer (IBFT/Raast) and local digital wallets';
  });
  content = content.replace(/via EasyPaisa, JazzCash, or SadaPay/g, () => {
    count++;
    return 'via domestic bank transfer or local digital wallets';
  });
  content = content.replace(/Pay locally via EasyPaisa, JazzCash, SadaPay, or Raast/g, () => {
    count++;
    return 'Pay locally via domestic bank transfer or local digital wallets';
  });
  content = content.replace(/EasyPaisa, JazzCash, and SadaPay are supported for PKR orders\./g, () => {
    count++;
    return 'Domestic bank transfers and local digital wallets are supported for PKR orders.';
  });
  content = content.replace(/through EasyPaisa, JazzCash, SadaPay, or Raast/g, () => {
    count++;
    return 'through domestic bank transfer, Raast, or local digital wallets';
  });

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    fileStats[file] = (fileStats[file] || 0) + count;
    totalReplacements += count;
  }
});

console.log(`Consolidation round 2 complete: ${totalReplacements} new replacements across ${Object.keys(fileStats).length} files.`);
