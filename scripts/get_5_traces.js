const { execSync } = require('child_process');

try {
  const log = execSync('gh run view 45440380100 --log', { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  const lines = log.split('\n');
  lines.forEach((l, idx) => {
    if (l.includes('FAIL: ') || l.includes('ERROR: ')) {
      console.log('\n----------------------------------------');
      console.log(l.trim());
      for (let i = idx + 1; i < idx + 35 && i < lines.length; i++) {
        const text = lines[i].trim();
        if (text.includes('FAIL: ') || text.includes('ERROR: ') || text.includes('Ran 465 tests')) break;
        if (text.includes('Traceback') || text.includes('File ') || text.includes('Error:') || text.includes('AssertionError:')) {
          console.log('  ', text);
        }
      }
    }
  });
} catch (e) {
  console.error(e.message);
}
