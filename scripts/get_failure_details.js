const { execSync } = require('child_process');

try {
  const log = execSync('gh run view 45437034140 --log', { encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 });
  const lines = log.split('\n');
  let capturing = false;
  let currentTest = '';
  lines.forEach(l => {
    if (l.includes('FAIL: ') || l.includes('ERROR: ')) {
      capturing = true;
      currentTest = l.trim();
      console.log('\n============================================================');
      console.log(currentTest);
    } else if (capturing) {
      if (l.includes('----------------------------------------------------------------------') || l.includes('Ran 465 tests')) {
        // end of failure
      } else if (l.includes('AssertionError:') || l.includes('Exception:') || l.includes('Error:')) {
        console.log('TRACE:', l.trim());
      }
    }
  });
} catch (e) {
  console.error(e.message);
}
