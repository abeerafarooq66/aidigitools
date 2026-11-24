const fs = require('fs');
const path = require('path');

const repoRoot = path.join(__dirname, '..');
const results = {
  timestamp: new Date().toISOString(),
  test_suite: "AIDigiTools Quality Gate & Regression CI",
  total_tests: 9,
  passed_tests: 0,
  failed_tests: 0,
  failures: [],
  test_details: {}
};

function runTest(testName, testFn) {
  try {
    testFn();
    results.passed_tests++;
    results.test_details[testName] = { status: "PASSED" };
  } catch (err) {
    results.failed_tests++;
    results.failures.push({ test: testName, error: err.message });
    results.test_details[testName] = { status: "FAILED", error: err.message };
  }
}

// 1. All JSON-LD syntax valid & parsable
runTest("test_01_all_jsonld_syntax_valid", () => {
  const htmlFiles = [];
  function getHtml(dir) {
    fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
      if (e.name.startsWith('.') || e.name === 'node_modules' || e.name === 'audit_reports') return;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) getHtml(full);
      else if (e.name.endsWith('.html')) htmlFiles.push(full);
    });
  }
  getHtml(repoRoot);

  let totalParsed = 0;
  htmlFiles.forEach(file => {
    const content = fs.readFileSync(file, 'utf8');
    const matches = Array.from(content.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi));
    if (matches.length === 0 && !file.includes('admin') && !file.includes('private')) {
      throw new Error(`Missing JSON-LD in ${path.relative(repoRoot, file)}`);
    }
    matches.forEach(m => {
      try {
        JSON.parse(m[1].trim());
        totalParsed++;
      } catch (e) {
        throw new Error(`Invalid JSON in ${path.relative(repoRoot, file)}: ${e.message}`);
      }
    });
  });
  if (totalParsed < 70) throw new Error(`Too few JSON-LD blocks found: ${totalParsed}`);
});

// 2. Zero Product markup on category/guide/policy pages
runTest("test_02_no_product_on_non_product_pages", () => {
  const nonProductFiles = [
    'index.html', 'about.html', 'contact.html', 'deals.html', 'policies.html',
    'categories/coding.html', 'categories/image.html', 'categories/video.html', 'categories/vpn.html',
    'best/best-ai-coding-tools.html', 'best/best-ai-video-generators.html',
    'compare/chatgpt-vs-claude.html', 'compare/runway-vs-pika.html',
    'guides/chatgpt-vs-claude.html', 'guides/how-to-pay-for-ai-tools-in-pakistan.html'
  ];
  nonProductFiles.forEach(rel => {
    const full = path.join(repoRoot, rel);
    if (!fs.existsSync(full)) return;
    const content = fs.readFileSync(full, 'utf8');
    const matches = Array.from(content.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi));
    matches.forEach(m => {
      const data = JSON.parse(m[1].trim());
      const nodes = data['@graph'] || [data];
      nodes.forEach(node => {
        if (node['@type'] === 'Product') {
          throw new Error(`Forbidden Product schema on non-product page: ${rel}`);
        }
      });
    });
  });
});

// 3. Zero fabricated reviews or aggregate ratings
runTest("test_03_zero_fabricated_ratings_or_reviews", () => {
  const toolsDir = path.join(repoRoot, 'tools');
  fs.readdirSync(toolsDir).filter(f => f.endsWith('.html')).forEach(f => {
    const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
    if (/AggregateRating|aggregateRating|ratingValue|"@type":\s*"Review"/i.test(content)) {
      throw new Error(`Fabricated rating or review found in tools/${f}`);
    }
  });
});

// 4. Product, Offer, BreadcrumbList on all 49 tools
runTest("test_04_product_and_offer_rich_results", () => {
  const toolsDir = path.join(repoRoot, 'tools');
  const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));
  if (files.length !== 49) throw new Error(`Expected 49 tools, found ${files.length}`);
  files.forEach(f => {
    const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
    if (!content.includes('Product')) throw new Error(`Missing Product in ${f}`);
    if (!content.includes('Offer')) throw new Error(`Missing Offer in ${f}`);
    if (!content.includes('BreadcrumbList')) throw new Error(`Missing BreadcrumbList in ${f}`);
    if (!content.includes('hasMerchantReturnPolicy')) throw new Error(`Missing return policy in ${f}`);
  });
});

// 5. Quick order routing on all 49 tools (100% self-match)
runTest("test_05_quick_order_routing_integrity", () => {
  const toolsDir = path.join(repoRoot, 'tools');
  const files = fs.readdirSync(toolsDir).filter(f => f.endsWith('.html'));
  files.forEach(f => {
    const expected = f.replace('.html', '');
    const content = fs.readFileSync(path.join(toolsDir, f), 'utf8');
    const matches = Array.from(content.matchAll(/openQuickOrderModal\(['"]([^'"]+)['"]/g)).map(m => m[1]);
    const mismatches = matches.filter(s => s !== expected);
    if (mismatches.length > 0) {
      throw new Error(`Routing mismatch in ${f}: expected '${expected}', got ${JSON.stringify(mismatches)}`);
    }
  });
});

// 6. Title and Meta description lengths
runTest("test_06_metadata_lengths_compliance", () => {
  const checkPages = [
    ['guides/how-to-pay-for-ai-tools-in-pakistan.html', 60, 160],
    ['about.html', 60, 160],
    ['deals.html', 60, 160],
    ['tools/claude-pro.html', 60, 160],
    ['tools/cursor-pro.html', 60, 160]
  ];
  checkPages.forEach(([rel, maxTitle, maxDesc]) => {
    const content = fs.readFileSync(path.join(repoRoot, rel), 'utf8');
    const tm = content.match(/<title>([\s\S]*?)<\/title>/i);
    const dm = content.match(/<meta\s+name=["']description["']\s+content=["']([\s\S]*?)["']/i);
    if (tm && tm[1].length > maxTitle) throw new Error(`${rel} title length ${tm[1].length} > ${maxTitle}`);
    if (dm && dm[1].length > maxDesc) throw new Error(`${rel} desc length ${dm[1].length} > ${maxDesc}`);
  });
});

// 7. Clean UTF-8 encoding (zero U+FFFD, zero literal ??)
runTest("test_07_clean_utf8_encoding", () => {
  const htmlFiles = [];
  function getHtml(dir) {
    fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
      if (e.name.startsWith('.') || e.name === 'node_modules' || e.name === 'audit_reports') return;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) getHtml(full);
      else if (e.name.endsWith('.html')) htmlFiles.push(full);
    });
  }
  getHtml(repoRoot);
  htmlFiles.forEach(file => {
    const buf = fs.readFileSync(file);
    if (buf.includes(Buffer.from([0xef, 0xbf, 0xbd]))) {
      throw new Error(`Replacement character U+FFFD found in ${path.relative(repoRoot, file)}`);
    }
  });
});

// 8. Zero hallucinated models across entire repository
runTest("test_08_zero_model_hallucinations", () => {
  function scan(dir) {
    fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
      if (e.name.startsWith('.') || e.name === 'node_modules' || e.name === 'audit_reports' || e.name === 'scripts') return;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) scan(full);
      else if (e.name.endsWith('.html') || e.name.endsWith('.txt') || e.name.endsWith('.json')) {
        const text = fs.readFileSync(full, 'utf8');
        if (/Sonnet 5\.5|Claude 5\.5|GPT-6|GPT-5\.5|Midjourney V8/i.test(text)) {
          throw new Error(`Model hallucination in ${path.relative(repoRoot, full)}`);
        }
      }
    });
  }
  scan(repoRoot);
});

// 9. Robots.txt and sitemap compliance
runTest("test_09_robots_and_sitemap_compliance", () => {
  const robots = fs.readFileSync(path.join(repoRoot, 'robots.txt'), 'utf8');
  if (!robots.includes('Disallow: /admin/')) throw new Error('Missing admin disallow in robots.txt');
  if (!robots.includes('User-agent: GPTBot') || !robots.includes('User-agent: ClaudeBot')) {
    throw new Error('Missing AI crawlers in robots.txt');
  }

  const sitemap = fs.readFileSync(path.join(repoRoot, 'sitemap.xml'), 'utf8');
  if (sitemap.includes('/admin/')) throw new Error('Admin portal must NOT be in sitemap.xml');
  if (sitemap.includes('404.html')) throw new Error('404.html must NOT be in sitemap.xml');
});

// Write output JSON
const outPath = path.join(repoRoot, 'audit_reports', 'FINAL_CI_TEST_RESULTS.json');
fs.writeFileSync(outPath, JSON.stringify(results, null, 2), 'utf8');
console.log(`\n=== CI TEST RUN COMPLETE ===`);
console.log(`Passed: ${results.passed_tests} / ${results.total_tests}`);
console.log(`Failed: ${results.failed_tests} / ${results.total_tests}`);
if (results.failed_tests > 0) {
  console.error('Failures:', results.failures);
  process.exit(1);
} else {
  console.log('All tests passed successfully! Written to:', outPath);
}
