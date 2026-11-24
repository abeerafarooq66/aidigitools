const { execSync } = require('child_process');

try {
  const log = execSync('gh run view 45441472340 --log', { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  const lines = log.split('\n');
  lines.forEach((l, idx) => {
    if (l.includes('FAIL: test_10')) {
      console.log(l.trim());
      for (let i = idx + 1; i < idx + 25 && i < lines.length; i++) {
        console.log('  ', lines[i].trim());
      }
    }
  });
} catch (e) {
  console.error(e.message);
}
