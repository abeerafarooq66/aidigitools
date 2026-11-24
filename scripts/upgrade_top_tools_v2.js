const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const toolsDir = path.join(repoRoot, 'tools');

function upgradeTool(file, updates) {
  const filePath = path.join(toolsDir, file);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${file}`);
    return;
  }
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  // Apply string or regex replacements
  updates.forEach(([target, replacement]) => {
    if (typeof target === 'string') {
      content = content.replaceAll(target, replacement);
    } else {
      content = content.replace(target, replacement);
    }
  });

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Successfully upgraded ${file} to Master Book V2 standards.`);
  } else {
    console.log(`No changes made to ${file}.`);
  }
}

// 1. claude-pro.html
upgradeTool('claude-pro.html', [
  // H1 and Title
  ['<h1>Claude Pro Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Claude Pro Subscription Pakistan (PKR & USD) — Anthropic 3.5 Access</h1>'],
  ['<title>Claude Pro Pakistan (PKR & USD) — Buy Online | AIDigiTools</title>', '<title>Claude Pro Pakistan (PKR & USD) — Claude 3.5 Sonnet & Artifacts | AIDigiTools</title>'],
  // Benchmarks & Models
  ['Claude Sonnet 5.5 Benchmark', 'Claude 3.5 Sonnet Benchmark (SWE-bench 49.2%)'],
  ['Grounded in Anthropic Claude Sonnet 5.5 & 3.5 technical benchmarks.', 'Grounded in Anthropic Claude 3.5 Sonnet & Claude 3.5 Haiku official benchmarks.'],
  ['building upon Claude 3.5 Sonnet foundations', 'achieving 49.2% on SWE-bench Verified and 65.0% on GPQA Diamond'],
  ['Unlocks Claude Sonnet 5.5, Projects, 200K context', 'Unlocks Claude 3.5 Sonnet, Projects, 200K context'],
  // Canonical comparison link
  ['../guides/chatgpt-vs-claude.html', '../compare/chatgpt-vs-claude.html'],
  // Contextual hub links
  ['<p style="font-size:1.1rem;">Compare with ChatGPT: <a href="../compare/chatgpt-vs-claude.html" style="color:#0369A1; font-weight:700;">View our ChatGPT vs Claude comparison →</a></p>',
   '<p style="font-size:1.05rem; line-height:1.7;">Compare with alternatives: <a href="../compare/chatgpt-vs-claude.html" style="color:#0369A1; font-weight:700;">Claude vs ChatGPT Comparison →</a> &bull; <a href="../best/best-ai-coding-tools.html" style="color:#0369A1; font-weight:700;">Best AI Coding Tools (2026) →</a> &bull; <a href="../categories/coding.html" style="color:#0369A1; font-weight:700;">All Coding &amp; Assistant Hubs →</a></p>']
]);

// 2. chatgpt-plus.html
upgradeTool('chatgpt-plus.html', [
  // H1 and Title
  ['<h1>ChatGPT Plus Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>ChatGPT Plus Subscription Pakistan (PKR & USD) — OpenAI o1 & GPT-4o</h1>'],
  ['<title>ChatGPT Plus Pakistan (PKR & USD) — Buy Online | AIDigiTools</title>', '<title>ChatGPT Plus Pakistan (PKR & USD) — OpenAI o1, GPT-4o & Canvas | AIDigiTools</title>'],
  // Hallucinated GPT-5/GPT-6 -> OpenAI o1 & GPT-4o
  ['<h3>GPT-5 / GPT-6 & Canvas Engine</h3>', '<h3>OpenAI o1 Reasoning & GPT-4o Engine</h3>'],
  ['Access next-generation frontier intelligence including GPT-5 and early research checkpoints.', 'Prioritized access to OpenAI o1 reasoning series and GPT-4o with interactive Canvas workspace.'],
  // Canonical comparison link
  ['../guides/chatgpt-vs-claude.html', '../compare/chatgpt-vs-claude.html'],
  ['<p style="font-size:1.1rem;">Compare with Claude: <a href="../guides/chatgpt-vs-claude.html" style="color:#0369A1; font-weight:700;">View our ChatGPT vs Claude comparison →</a></p>',
   '<p style="font-size:1.05rem; line-height:1.7;">Compare with alternatives: <a href="../compare/chatgpt-vs-claude.html" style="color:#0369A1; font-weight:700;">ChatGPT vs Claude Comparison →</a> &bull; <a href="../best/best-ai-coding-tools.html" style="color:#0369A1; font-weight:700;">Best AI Coding Tools (2026) →</a> &bull; <a href="../categories/coding.html" style="color:#0369A1; font-weight:700;">All Coding AI Tools →</a></p>']
]);

// 3. cursor-pro.html
upgradeTool('cursor-pro.html', [
  ['<h1>Cursor Pro Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Cursor Pro Subscription Pakistan (PKR & USD) — AI Code Editor</h1>'],
  ['2600 Fast Premium Requests', '500 Fast Premium Requests + Unlimited Slow'],
  ['2,600 fast requests every month', '500 fast requests monthly for Claude 3.5 Sonnet and GPT-4o with unlimited standard slow requests'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">Related Guides: <a href="../blog/cursor-ai-vs-github-copilot-comparison.html" style="color:#0369A1; font-weight:700;">Cursor vs GitHub Copilot Guide →</a> &bull; <a href="../best/best-ai-coding-tools.html" style="color:#0369A1; font-weight:700;">Best AI Coding Tools (2026) →</a> &bull; <a href="../categories/coding.html" style="color:#0369A1; font-weight:700;">Coding &amp; LLM Category →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 4. github-copilot.html
upgradeTool('github-copilot.html', [
  ['<h1>GitHub Copilot Individual Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>GitHub Copilot Subscription Pakistan (PKR & USD) — AI Pair Programmer</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">Explore Comparisons: <a href="../blog/cursor-ai-vs-github-copilot-comparison.html" style="color:#0369A1; font-weight:700;">GitHub Copilot vs Cursor AI →</a> &bull; <a href="../best/best-ai-coding-tools.html" style="color:#0369A1; font-weight:700;">Top AI Coding Tools →</a> &bull; <a href="../categories/coding.html" style="color:#0369A1; font-weight:700;">Coding Tools Directory →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 5. turnitin-student.html
upgradeTool('turnitin-student.html', [
  ['<h1>Turnitin Originality Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Turnitin Student Account Pakistan (PKR & USD) — Non-Repository Plagiarism & AI Check</h1>'],
  ['<title>Turnitin Originality Pakistan (PKR & USD) — Buy Online | AIDigiTools</title>', '<title>Turnitin Student Account Pakistan (PKR & USD) — Non-Repository Plagiarism Check | AIDigiTools</title>'],
  // Add feature cards
  ['<section class="plans-comparison-section" id="compare-plans">',
   `<section style="margin-top: 3.5rem;">
      <h2 class="section-title">Verified Academic Integrity &amp; Turnitin Specifications</h2>
      <p class="section-subtitle">Grounded in non-repository privacy standards and official Turnitin algorithms.</p>
      <div class="grid">
        <div class="card">
          <h3>100% Non-Repository Protection</h3>
          <p>Student papers and theses are never stored in institutional databases or matched against future institutional submissions.</p>
        </div>
        <div class="card">
          <h3>Dual Similarity &amp; AI Breakdown</h3>
          <p>Generates color-coded source matching percentages alongside Turnitin's specialized AI Writing Detection score report.</p>
        </div>
        <div class="card">
          <h3>Rapid 15-Minute Turnaround</h3>
          <p>Instant file upload processing for PDF, DOCX, and TXT documents with downloadable digital receipt and analysis matrix.</p>
        </div>
      </div>
    </section>
    <section class="plans-comparison-section" id="compare-plans">`]
]);

// 6. midjourney.html
upgradeTool('midjourney.html', [
  ['<h1>Midjourney V8 Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Midjourney Subscription Pakistan (PKR & USD) — v6.1 AI Image Generation</h1>'],
  ['Midjourney V8', 'Midjourney v6.1'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">Creative Suites: <a href="../categories/image.html" style="color:#0369A1; font-weight:700;">All Image &amp; Design AI Tools →</a> &bull; <a href="canva-pro.html" style="color:#0369A1; font-weight:700;">Canva Pro Magic Studio →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 7. canva-pro.html
upgradeTool('canva-pro.html', [
  ['<h1>Canva Pro Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Canva Pro Subscription Pakistan (PKR & USD) — Magic Studio & Brand Kits</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">Explore Graphic Tools: <a href="../categories/image.html" style="color:#0369A1; font-weight:700;">AI Graphic Design Category Hub →</a> &bull; <a href="midjourney.html" style="color:#0369A1; font-weight:700;">Midjourney v6.1 Fast GPU →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 8. runway-gen3.html
upgradeTool('runway-gen3.html', [
  ['<h1>Runway AI Video Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Runway Gen-3 Alpha Pakistan (PKR & USD) — Cinematic AI Video Generator</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">Video Workflows: <a href="../compare/runway-vs-pika.html" style="color:#0369A1; font-weight:700;">Runway vs Pika Labs Comparison →</a> &bull; <a href="../best/best-ai-video-generators.html" style="color:#0369A1; font-weight:700;">Best AI Video Generators (2026) →</a> &bull; <a href="../categories/video.html" style="color:#0369A1; font-weight:700;">Video AI Hub →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 9. capcut-pro.html
upgradeTool('capcut-pro.html', [
  ['<h1>CapCut Pro Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>CapCut Pro Subscription Pakistan (PKR & USD) — 4K 60fps & AI Editing</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">Video AI Tools: <a href="../best/best-ai-video-generators.html" style="color:#0369A1; font-weight:700;">Best Video Generators Guide →</a> &bull; <a href="../categories/video.html" style="color:#0369A1; font-weight:700;">AI Video Category Hub →</a> &bull; <a href="runway-gen3.html" style="color:#0369A1; font-weight:700;">Runway Gen-3 Alpha →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 10. deepseek-pro.html
upgradeTool('deepseek-pro.html', [
  ['<h1>DeepSeek Platform Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>DeepSeek V3 & R1 Pakistan (PKR & USD) — Frontier Reasoning Platform</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">AI Model Comparison: <a href="claude-pro.html" style="color:#0369A1; font-weight:700;">Claude 3.5 Sonnet →</a> &bull; <a href="chatgpt-plus.html" style="color:#0369A1; font-weight:700;">ChatGPT Plus o1 →</a> &bull; <a href="../categories/coding.html" style="color:#0369A1; font-weight:700;">Coding &amp; LLM Category →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 11. elevenlabs-creator.html
upgradeTool('elevenlabs-creator.html', [
  ['<h1>ElevenLabs Creator Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>ElevenLabs Creator Subscription Pakistan (PKR & USD) — AI Voice Cloning</h1>']
]);

// 12. youtube-premium.html
upgradeTool('youtube-premium.html', [
  ['<h1>YouTube Premium Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>YouTube Premium Subscription Pakistan (PKR & USD) — Ad-Free & Music</h1>']
]);

// 13. nordvpn.html
upgradeTool('nordvpn.html', [
  ['<h1>NordVPN Standard Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>NordVPN Standard Subscription Pakistan (PKR & USD) — High-Speed Security</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">VPN Category: <a href="../categories/vpn.html" style="color:#0369A1; font-weight:700;">All Secure VPN Services Hub →</a> &bull; <a href="surfshark-vpn.html" style="color:#0369A1; font-weight:700;">Surfshark VPN Unlimited →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 14. surfshark-vpn.html
upgradeTool('surfshark-vpn.html', [
  ['<h1>Surfshark VPN Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Surfshark VPN Subscription Pakistan (PKR & USD) — Unlimited Devices</h1>'],
  ['<section style="margin-top: 3.5rem; text-align:center;">',
   '<section style="margin-top: 3.5rem; text-align:center;"><p style="font-size:1.05rem; line-height:1.7;">VPN Category: <a href="../categories/vpn.html" style="color:#0369A1; font-weight:700;">All Secure VPN Services Hub →</a> &bull; <a href="nordvpn.html" style="color:#0369A1; font-weight:700;">NordVPN Threat Protection →</a></p></section><section style="margin-top: 3.5rem; display:none;">']
]);

// 15. semrush-guru.html
upgradeTool('semrush-guru.html', [
  ['<h1>Semrush Guru Pakistan & Worldwide — Pricing & Rails</h1>', '<h1>Semrush Guru Subscription Pakistan (PKR & USD) — SEO & Competitor Intelligence</h1>']
]);

console.log('Top tools upgrade execution finished.');
