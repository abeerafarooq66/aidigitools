const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.resolve(__dirname, '..');
console.log(`=== AIDigiTools Master Audit V2 System (Node.js Engine) ===`);
console.log(`Auditing directory: ${REPO_ROOT}\n`);

function getHtmlFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (['.git', 'scratch', '.gemini', 'audit_reports', 'node_modules'].includes(file)) continue;
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      getHtmlFiles(fullPath, fileList);
    } else if (file.endsWith('.html')) {
      fileList.push(fullPath);
    }
  }
  return fileList;
}

const htmlFiles = getHtmlFiles(REPO_ROOT).sort();
console.log(`Total HTML files discovered: ${htmlFiles.length}\n`);

const results = {
  totalPages: htmlFiles.length,
  criticalIssues: [],
  highIssues: [],
  mediumIssues: [],
  inStockCount: 0,
  outOfStockCount: 0,
  pagesWithQuickAnswer: 0,
  pagesWithoutQuickAnswer: 0,
  pagesWithMultipleH1: 0,
  pagesMissingH1: 0,
  imagesMissingAltTotal: 0,
  imagesMissingDimensionsTotal: 0,
  pages: {}
};

const paymentTermsRegex = /\b(sadapay|nayapay|jazzcash|easypaisa|raast)\b/gi;

for (const filePath of htmlFiles) {
  const relPath = path.relative(REPO_ROOT, filePath).replace(/\\/g, '/');
  const content = fs.readFileSync(filePath, 'utf8');

  const pageData = {
    file: relPath,
    h1Count: 0,
    title: null,
    metaDesc: null,
    canonical: null,
    quickAnswer: false,
    schemas: [],
    productAvailability: null,
    imagesCount: 0,
    imagesMissingAlt: 0,
    imagesMissingDimensions: 0,
    paymentMentions: 0,
    issues: []
  };

  // H1 match
  const h1Matches = content.match(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi) || [];
  pageData.h1Count = h1Matches.length;
  if (pageData.h1Count === 0) {
    pageData.issues.push('Missing H1 heading');
    results.criticalIssues.push(`${relPath}: Missing H1 heading`);
    results.pagesMissingH1++;
  } else if (pageData.h1Count > 1) {
    pageData.issues.push(`Multiple H1 headings (${pageData.h1Count})`);
    results.highIssues.push(`${relPath}: Multiple H1 headings (${pageData.h1Count})`);
    results.pagesWithMultipleH1++;
  }

  // Title match
  const titleMatch = content.match(/<title\b[^>]*>([\s\S]*?)<\/title>/i);
  if (titleMatch) {
    pageData.title = titleMatch[1].trim();
    if (pageData.title.length < 25) {
      pageData.issues.push(`Title too short (${pageData.title.length} chars)`);
      results.mediumIssues.push(`${relPath}: Short title (${pageData.title.length} chars)`);
    } else if (pageData.title.length > 75) {
      pageData.issues.push(`Title too long (${pageData.title.length} chars)`);
      results.mediumIssues.push(`${relPath}: Long title (${pageData.title.length} chars)`);
    }
  } else {
    pageData.issues.push('Missing <title> tag');
    results.criticalIssues.push(`${relPath}: Missing <title> tag`);
  }

  // Meta description
  const metaDescMatch = content.match(/<meta\s+name=["']description["']\s+content=["'](.*?)["']/i) ||
                        content.match(/<meta\s+content=["'](.*?)["']\s+name=["']description["']/i);
  if (metaDescMatch) {
    pageData.metaDesc = metaDescMatch[1].trim();
    if (pageData.metaDesc.length < 50) {
      pageData.issues.push(`Meta description too short (${pageData.metaDesc.length} chars)`);
      results.mediumIssues.push(`${relPath}: Short meta description`);
    } else if (pageData.metaDesc.length > 170) {
      pageData.issues.push(`Meta description too long (${pageData.metaDesc.length} chars)`);
      results.mediumIssues.push(`${relPath}: Long meta description`);
    }
  } else {
    pageData.issues.push('Missing meta description');
    results.highIssues.push(`${relPath}: Missing meta description`);
  }

  // Canonical link
  const canonicalMatch = content.match(/<link\s+rel=["']canonical["']\s+href=["'](.*?)["']/i);
  if (canonicalMatch) {
    pageData.canonical = canonicalMatch[1].trim();
  } else {
    pageData.issues.push('Missing canonical tag');
    results.highIssues.push(`${relPath}: Missing canonical tag`);
  }

  // Quick Answer
  pageData.quickAnswer = /class=["'][^"']*\bquick-answer\b[^"']*["']/i.test(content);
  if (pageData.quickAnswer) {
    results.pagesWithQuickAnswer++;
  } else {
    results.pagesWithoutQuickAnswer++;
    if (relPath.startsWith('tools/') || relPath.startsWith('guides/')) {
      pageData.issues.push('Missing .quick-answer capsule for AEO/GEO');
      results.highIssues.push(`${relPath}: Missing .quick-answer capsule`);
    }
  }

  // JSON-LD Schemas
  const scriptRegex = /<script\s+type=["']application\/ld\+json["']>([\s\S]*?)<\/script>/gi;
  let scriptMatch;
  while ((scriptMatch = scriptRegex.exec(content)) !== null) {
    try {
      const data = JSON.parse(scriptMatch[1]);
      if (data['@graph']) {
        for (const node of data['@graph']) {
          pageData.schemas.push(node['@type']);
          if (node['@type'] === 'Product' && node.offers) {
            pageData.productAvailability = node.offers.availability;
          }
        }
      } else {
        pageData.schemas.push(data['@type']);
        if (data['@type'] === 'Product' && data.offers) {
          pageData.productAvailability = data.offers.availability;
        }
      }
    } catch (e) {
      pageData.issues.push(`Invalid JSON-LD syntax: ${e.message}`);
      results.highIssues.push(`${relPath}: Invalid JSON-LD syntax`);
    }
  }

  if (pageData.productAvailability === 'https://schema.org/InStock') {
    results.inStockCount++;
  } else if (pageData.productAvailability === 'https://schema.org/OutOfStock') {
    results.outOfStockCount++;
  }

  // Images check
  const imgRegex = /<img\b([^>]*)>/gi;
  let imgMatch;
  while ((imgMatch = imgRegex.exec(content)) !== null) {
    pageData.imagesCount++;
    const attrs = imgMatch[1];
    if (!/alt=["'][^"']*["']/i.test(attrs)) {
      pageData.imagesMissingAlt++;
      results.imagesMissingAltTotal++;
    }
    if (!(/width=["'][^"']*["']/i.test(attrs) && /height=["'][^"']*["']/i.test(attrs))) {
      pageData.imagesMissingDimensions++;
      results.imagesMissingDimensionsTotal++;
    }
  }

  // Payment terms count
  const paymentMatches = content.match(paymentTermsRegex);
  pageData.paymentMentions = paymentMatches ? paymentMatches.length : 0;

  results.pages[relPath] = pageData;
}

console.log('='.repeat(70));
console.log('MASTER AUDIT METRICS SUMMARY:');
console.log(`Total Pages Audited:               ${results.totalPages}`);
console.log(`Pages with InStock Product:        ${results.inStockCount}`);
console.log(`Pages with OutOfStock Product:     ${results.outOfStockCount}`);
console.log(`Pages with .quick-answer Capsule:  ${results.pagesWithQuickAnswer}`);
console.log(`Pages missing H1:                  ${results.pagesMissingH1}`);
console.log(`Pages with Multiple H1:            ${results.pagesWithMultipleH1}`);
console.log(`Images Missing alt attributes:     ${results.imagesMissingAltTotal}`);
console.log(`Images Missing width/height (CLS): ${results.imagesMissingDimensionsTotal}`);
console.log(`Critical Issues Count:             ${results.criticalIssues.length}`);
console.log(`High Priority Issues Count:        ${results.highIssues.length}`);
console.log(`Medium Priority Issues Count:      ${results.mediumIssues.length}`);
console.log('='.repeat(70));

const outJsonPath = path.join(REPO_ROOT, 'audit_reports', 'master_audit_v2_system_results.json');
fs.writeFileSync(outJsonPath, JSON.stringify(results, null, 2), 'utf8');
console.log(`\nMaster audit report saved to: ${outJsonPath}`);
