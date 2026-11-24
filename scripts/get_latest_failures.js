const { execSync } = require('child_process');

try {
  const log = execSync('gh run view 45441472340 --log', { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  const lines = log.split('\n');
  const fails = lines.filter(l => l.includes('FAIL: ') || l.includes('ERROR: ') || l.includes('FAILED ('));
  console.log('=== TEST FAILURES IN 45441472340 ===');
  fails.forEach(f => console.log(f.trim()));
} catch (e) {
  console.error(e.message);
}
