const https = require('https');

function checkUrl(url, checks) {
  return new Promise((resolve) => {
    const bustUrl = url + (url.includes('?') ? '&' : '?') + 'cb=' + Date.now();
    https.get(bustUrl, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log(`\n=== Live Check: ${url} (Status: ${res.statusCode}) ===`);
        let allPassed = true;
        checks.forEach(([label, fn]) => {
          const result = fn(data);
          if (!result) allPassed = false;
          console.log(` - ${label}: ${result ? 'PASSED' : 'FAILED'}`);
        });
        resolve(allPassed);
      });
    }).on('error', err => {
      console.error(`Error fetching ${url}: ${err.message}`);
      resolve(false);
    });
  });
}

async function run() {
  console.log("Checking deployment status on aidigitools.tech...");
  
  await checkUrl('https://aidigitools.tech/assets/cart.js', [
    ['Contains payment_rail_selected GA4 event', d => d.includes('payment_rail_selected')],
    ['Contains select_payment_rail GA4 event', d => d.includes('select_payment_rail')]
  ]);

  await checkUrl('https://aidigitools.tech/tools/cursor-pro.html', [
    ['Quick Order CTA routes to cursor-pro', d => d.includes("openQuickOrderModal('cursor-pro')")],
    ['Zero U+FFFD', d => !d.includes('\uFFFD')],
    ['Zero Sonnet 5.5 mentions', d => !d.includes('Sonnet 5.5')]
  ]);

  await checkUrl('https://aidigitools.tech/tools/chatgpt-plus.html', [
    ['Quick Order CTA routes to chatgpt-plus', d => d.includes("openQuickOrderModal('chatgpt-plus')")],
    ['Contains OpenAI o1 reasoning', d => d.includes('OpenAI o1')],
    ['Zero GPT-6 claims', d => !d.includes('GPT-6')]
  ]);

  await checkUrl('https://aidigitools.tech/guides/how-to-pay-for-ai-tools-in-pakistan.html', [
    ['Title is concise (< 60 chars)', d => {
      const match = d.match(/<title>([^<]*)<\/title>/i);
      return match && match[1].length <= 60;
    }],
    ['Quick answer capsule properly closed', d => d.includes('class="quick-answer"') && d.includes('</p>')]
  ]);

  await checkUrl('https://aidigitools.tech/categories/coding.html', [
    ['Zero Sonnet 5.5', d => !d.includes('Sonnet 5.5')],
    ['Zero GPT-6', d => !d.includes('GPT-6')]
  ]);
}

run();
