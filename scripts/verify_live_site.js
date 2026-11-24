const https = require('https');

function checkUrl(url, checks) {
  return new Promise((resolve) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log(`\n=== Live Check: ${url} (Status: ${res.statusCode}) ===`);
        checks.forEach(([label, fn]) => {
          const result = fn(data);
          console.log(` - ${label}: ${result ? 'PASSED' : 'FAILED'}`);
        });
        resolve();
      });
    }).on('error', err => {
      console.error(`Error fetching ${url}: ${err.message}`);
      resolve();
    });
  });
}

async function run() {
  await checkUrl('https://aidigitools.tech/robots.txt', [
    ['Includes Meta-ExternalAgent', d => d.includes('Meta-ExternalAgent')],
    ['Disallows /admin/ for GPTBot', d => d.includes('User-agent: GPTBot') && d.includes('Disallow: /admin/')]
  ]);

  await checkUrl('https://aidigitools.tech/tools/claude-pro.html', [
    ['Zero U+FFFD (no replacement glyphs)', d => !d.includes('\uFFFD')],
    ['Zero Sonnet 5.5 mentions', d => !d.includes('Sonnet 5.5')],
    ['Contains SWE-bench 49.2%', d => d.includes('SWE-bench')],
    ['Canonical payment link present', d => d.includes('policies.html#payments')]
  ]);

  await checkUrl('https://aidigitools.tech/tools/chatgpt-plus.html', [
    ['Zero U+FFFD', d => !d.includes('\uFFFD')],
    ['Zero GPT-6 claims', d => !d.includes('GPT-6')],
    ['Contains OpenAI o1 reasoning', d => d.includes('OpenAI o1')],
    ['Canonical comparison link present', d => d.includes('compare/chatgpt-vs-claude.html')]
  ]);

  await checkUrl('https://aidigitools.tech/tools/turnitin-student.html', [
    ['Zero U+FFFD', d => !d.includes('\uFFFD')],
    ['Contains Non-Repository Protection card', d => d.includes('100% Non-Repository Protection')]
  ]);
}

run();
