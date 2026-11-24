const fs = require('fs');

const master = JSON.parse(fs.readFileSync('data/products_master.json', 'utf8'));
const catalog = JSON.parse(fs.readFileSync('scripts/tools_catalog.json', 'utf8'));

const heldSlugs = [
  "turnitin-student",
  "linkedin-premium",
  "netflix-premium",
  "spotify-premium",
  "coursera-plus",
  "claude-artifacts",
  "deepseek-pro"
];

console.log('=== HELD PRODUCTS AUDIT ===');
heldSlugs.forEach(slug => {
  const mItem = master.find(p => p.slug === slug || p.id === slug);
  const cItem = catalog[slug];
  const htmlFile = `tools/${slug}.html`;
  let htmlSchemaAvail = 'N/A';
  let htmlCta = 'N/A';
  let htmlOrderButton = 'N/A';
  if (fs.existsSync(htmlFile)) {
    const c = fs.readFileSync(htmlFile, 'utf8');
    const avM = c.match(/schema\.org\/(InStock|OutOfStock|PreOrder|Discontinued)/);
    htmlSchemaAvail = avM ? avM[1] : 'NOT FOUND';
    const ctaM = c.match(/<button[^>]*class=["'][^"']*nav-cta[^"']*["'][^>]*>([\s\S]*?)<\/button>/i);
    htmlCta = ctaM ? ctaM[0].replace(/\s+/g, ' ').trim() : 'NOT FOUND';
    const btnM = c.match(/<button[^>]*class=["'][^"']*(?:btn-primary|order-btn|cta-btn)[^"']*["'][^>]*>([\s\S]*?)<\/button>/i);
    htmlOrderButton = btnM ? btnM[0].replace(/\s+/g, ' ').trim() : 'NOT FOUND';
  }

  console.log(`\nTool: ${slug}`);
  console.log(` - Master status: website_display_status=${mItem ? mItem.website_display_status : 'N/A'}, availability_status=${mItem ? mItem.availability_status : 'N/A'}, sale_eligibility=${mItem ? mItem.sale_eligibility : 'N/A'}`);
  console.log(` - Catalog status: available=${cItem ? cItem.available : 'N/A'}, in_stock=${cItem ? cItem.in_stock : 'N/A'}, status=${cItem ? cItem.status : 'N/A'}`);
  console.log(` - HTML Schema Availability: ${htmlSchemaAvail}`);
  console.log(` - HTML Nav CTA: ${htmlCta}`);
  console.log(` - HTML Primary CTA: ${htmlOrderButton}`);
});
