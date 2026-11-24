const fs = require('fs');
const path = require('path');

// 1. ChatGPT Plus Title & Desc
const cgPlusPath = 'tools/chatgpt-plus.html';
let cgPlus = fs.readFileSync(cgPlusPath, 'utf8');
cgPlus = cgPlus.replace(
  /<title>.*?<\/title>/i,
  '<title>ChatGPT Plus Pakistan (PKR) — OpenAI o1 &amp; GPT-4o</title>'
);
cgPlus = cgPlus.replace(
  /<meta\s+name=["']description["']\s+content=["'][^"']*["']/i,
  '<meta name="description" content="Buy ChatGPT Plus in Pakistan with 15-min WhatsApp delivery &amp; 30-day warranty. Access OpenAI o1, GPT-4o, and Canvas with PKR payments.">'
);
fs.writeFileSync(cgPlusPath, cgPlus, 'utf8');
console.log('Fixed tools/chatgpt-plus.html');

// 2. DeepSeek Comparison Blog Meta Description
const dsBlogPath = 'blog/deepseek-r1-vs-chatgpt-plus-vs-claude-pro-comparison.html';
let dsBlog = fs.readFileSync(dsBlogPath, 'utf8');
dsBlog = dsBlog.replace(
  /<meta\s+name=["']description["']\s+content=["'][^"']*["']/i,
  '<meta name="description" content="DeepSeek R1 vs ChatGPT Plus vs Claude Pro 2026 benchmark. Compare reasoning, coding limits, and verified PKR pricing with 15-min delivery via AIDigiTools.">'
);
fs.writeFileSync(dsBlogPath, dsBlog, 'utf8');
console.log('Fixed blog/deepseek-r1-vs-chatgpt-plus-vs-claude-pro-comparison.html');

// 3. Guide Quick Answer tag in guides/how-to-pay-for-ai-tools-in-pakistan.html
const guidePath = 'guides/how-to-pay-for-ai-tools-in-pakistan.html';
let guide = fs.readFileSync(guidePath, 'utf8');
guide = guide.replace(
  /<p\s+class=["']quick-answer["'][^>]*>[\s\S]*?<\/p>/i,
  `<p class="quick-answer" style="background:#F0FDF4; border-left:4px solid #10B981; padding:18px; border-radius:0 8px 8px 0; margin-bottom:30px; font-size:1.05rem;">Quick Answer: Pakistani freelancers, developers, and creators can pay for premium AI subscriptions (ChatGPT Plus, Claude Pro, Cursor Pro, Midjourney) in PKR without international credit cards via domestic bank transfers, Raast, and local digital wallets starting from Rs. 600 PKR, with 15-minute WhatsApp delivery and a 30-day warranty.</p>`
);
fs.writeFileSync(guidePath, guide, 'utf8');
console.log('Fixed guides/how-to-pay-for-ai-tools-in-pakistan.html');

// 4. Tighten Quick Answers exceeding 70 words
const qaToolAdjustments = {
  'tools/gamma-app.html': 'Quick Answer: Gamma App Pro in Pakistan costs Rs. 1600 PKR (~$5.90 USD) monthly via AIDigiTools. It provides unlimited AI presentation deck generation, custom domains, export capabilities, and analytics. Subscriptions activate within 15 minutes on WhatsApp with domestic PKR settlement via EasyPaisa, JazzCash, or SadaPay.',
  'tools/google-ai-ultra.html': 'Quick Answer: Google AI Ultra in Pakistan costs Rs. 4500 PKR (~$16.50 USD) monthly via AIDigiTools. It unlocks Gemini 1.5 Pro and Ultra reasoning models with a 2-million-token context window and 2 TB cloud storage. Subscriptions activate in 15 minutes with domestic PKR settlement.',
  'tools/heygen-ai.html': 'Quick Answer: HeyGen Creator in Pakistan costs Rs. 4200 PKR (~$15.00 USD) monthly via AIDigiTools. It provides 15 monthly video credits, photorealistic avatars, multi-language voice cloning, and 1080p exports. Subscriptions activate within 15 minutes on WhatsApp with a 30-day replacement warranty.',
  'tools/jetbrains-all.html': 'Quick Answer: JetBrains All Products Pack in Pakistan costs Rs. 2500 PKR (~$9.00 USD) monthly via AIDigiTools. It grants full access to IntelliJ IDEA, PyCharm, WebStorm, PhpStorm, and ReSharper. Subscriptions activate in 15 minutes with domestic PKR payment support.',
  'tools/lovable-ai.html': 'Quick Answer: Lovable AI in Pakistan costs Rs. 1500 PKR (~$5.50 USD) monthly via AIDigiTools. It offers full-stack web application generation from natural language prompts, GitHub integration, and instant cloud deployment. Delivery completes within 15 minutes with local PKR payment rails.',
  'tools/microsoft-office-365.html': 'Quick Answer: Microsoft 365 Personal in Pakistan costs Rs. 1950 PKR (~$7.00 USD) monthly via AIDigiTools. It includes Word, Excel, PowerPoint, Outlook, and 1 TB cloud storage for 5 devices. Subscriptions activate in 15 minutes with EasyPaisa, JazzCash, or bank transfer.',
  'tools/prime-video.html': 'Quick Answer: Amazon Prime Video in Pakistan costs Rs. 650 PKR (~$2.40 USD) monthly via AIDigiTools. It provides ad-free 4K Ultra HD streaming on smart TVs, mobile, and web with offline downloads. Subscriptions activate in 15 minutes with a 30-day replacement warranty.',
  'tools/suno-ai.html': 'Quick Answer: Suno AI Music Pro in Pakistan costs Rs. 2600 PKR (~$9.50 USD) monthly via AIDigiTools. It provides 2,500 monthly credits (~500 songs), commercial rights, and high-fidelity v3.5 audio synthesis. Subscriptions activate in 15 minutes with domestic PKR settlement.',
  'tools/tradingview-pro.html': 'Quick Answer: TradingView Pro in Pakistan costs Rs. 3200 PKR (~$11.50 USD) monthly via AIDigiTools. It offers 5 indicators per chart, dual-chart layouts, 20 server-side volume alerts, and real-time market data. Subscriptions activate within 15 minutes on WhatsApp.',
  'tools/vidiq-boost.html': 'Quick Answer: vidIQ Boost in Pakistan costs Rs. 2100 PKR (~$7.50 USD) monthly via AIDigiTools. It features 50 daily AI video ideas, predictive keyword research, competitor tracking, and YouTube channel audits. Subscriptions activate within 15 minutes with local PKR payment rails.'
};

Object.entries(qaToolAdjustments).forEach(([filePath, newText]) => {
  if (!fs.existsSync(filePath)) return;
  let html = fs.readFileSync(filePath, 'utf8');
  html = html.replace(
    /<p\s+class=["']quick-answer["'][^>]*>[\s\S]*?<\/p>/i,
    `<p class="quick-answer" style="background:#F0FDF4; border-left:4px solid #10B981; padding:18px; border-radius:0 8px 8px 0; margin-bottom:30px; font-size:1.05rem;">${newText}</p>`
  );
  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`Updated QA in ${filePath}`);
});

// 5. Tighten Meta Descriptions exceeding 165 chars
const descAdjustments = {
  'tools/adobe-creative-cloud.html': 'Get Adobe Creative Cloud All Apps in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Access 20+ creative apps and Firefly generative credits in PKR.',
  'tools/canva-pro.html': 'Buy Canva Pro subscription in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Full access to Magic Studio, brand kits, and 100M+ assets in PKR.',
  'tools/capcut-pro.html': 'Get CapCut Pro in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Unlocks 4K 60fps exports, AI auto-captions, and cloud space with PKR payments.',
  'tools/chatgpt-codex.html': 'Buy OpenAI Codex workspace in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Multi-file coding agents, CLI tools, and domestic PKR settlement.',
  'tools/elevenlabs-creator.html': 'Buy ElevenLabs Creator in Pakistan with 15-min WhatsApp delivery & 30-day warranty. 100K characters, voice cloning, and domestic PKR payments.',
  'tools/envato-elements.html': 'Buy Envato Elements in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Unlimited downloads of stock video, graphics, and templates in PKR.',
  'tools/figma-pro.html': 'Buy Figma Professional in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Unlimited files, team libraries, and Dev Mode with PKR settlement.',
  'tools/gamma-app.html': 'Buy Gamma Pro in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Unlimited AI deck generation, custom domains, and analytics in PKR.',
  'tools/gemini-advanced.html': 'Buy Google AI Pro in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Access Gemini 1.5 Pro, 2 TB storage, and PKR domestic settlement.',
  'tools/heygen-ai.html': 'Buy HeyGen Creator in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Hyper-realistic AI avatars, voice cloning, and lip-syncing in PKR.',
  'tools/jetbrains-all.html': 'Buy JetBrains All Products Pack in Pakistan with 15-min WhatsApp delivery & 30-day warranty. IntelliJ IDEA, PyCharm, WebStorm, and domestic PKR settlement.',
  'tools/kling-ai.html': 'Buy Kling AI Pro in Pakistan with 15-min WhatsApp delivery & 30-day warranty. 10s continuous generation, motion brush, and 4K rendering in PKR.',
  'tools/microsoft-office-365.html': 'Buy Microsoft 365 Personal in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Premium Word, Excel, PowerPoint, and 1 TB OneDrive in PKR.',
  'tools/midjourney.html': 'Buy Midjourney v6.1 in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Unrestricted fast GPU hours, web editor access, and PKR settlement.',
  'tools/minimax-ai.html': 'Buy Hailuo AI Video (MiniMax) in Pakistan with 15-min WhatsApp delivery & 30-day warranty. 1080p cinematic generation and fast rendering in PKR.',
  'tools/notion-business.html': 'Buy Notion Plus with Notion AI in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Unlimited blocks, AI search, and team sharing in PKR.',
  'tools/replit-core.html': 'Buy Replit Core in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Autonomous Replit Agent, cloud hosting, and PostgreSQL in PKR.',
  'tools/runway-gen3.html': 'Buy Runway AI Video in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Gen-3 video generation, motion brush, and Act-Two in PKR.',
  'tools/vidiq-boost.html': 'Buy vidIQ Boost in Pakistan with 15-min WhatsApp delivery & 30-day warranty. 50 daily AI video ideas, keyword research, and channel audits in PKR.',
  'tools/windows-11-pro.html': 'Buy genuine Windows 11 Pro digital license in Pakistan with 15-min WhatsApp delivery & 30-day warranty. Lifetime activation and BitLocker in PKR.'
};

Object.entries(descAdjustments).forEach(([filePath, newDesc]) => {
  if (!fs.existsSync(filePath)) return;
  let html = fs.readFileSync(filePath, 'utf8');
  html = html.replace(
    /<meta\s+name=["']description["']\s+content=["'][^"']*["']/i,
    `<meta name="description" content="${newDesc}">`
  );
  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`Updated Meta Description in ${filePath}`);
});

console.log('All SEO length adjustments applied successfully!');
