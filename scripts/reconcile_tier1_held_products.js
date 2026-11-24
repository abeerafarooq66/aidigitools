const fs = require('fs');
const path = require('path');

const heldSlugs = [
  'turnitin-student',
  'linkedin-premium',
  'netflix-premium',
  'spotify-premium',
  'coursera-plus'
];

// 1. Update HTML tool pages
heldSlugs.forEach(slug => {
  const filePath = `tools/${slug}.html`;
  if (!fs.existsSync(filePath)) return;
  let html = fs.readFileSync(filePath, 'utf8');

  // Replace header nav CTA button
  html = html.replace(
    new RegExp(`<button[^>]*onclick=["']openQuickOrderModal\\(['"]${slug}['"]\\)[^>]*class=["']nav-cta["'][^>]*>[\\s\\S]*?<\\/button>`, 'i'),
    `<a href="https://wa.me/923326861112?text=Hi%20AIDigiTools%2C%20I%20would%20like%20to%20inquire%20about%20${slug}%20availability" class="nav-cta" style="text-decoration:none; display:inline-flex; align-items:center;" aria-label="Inquire on WhatsApp"><span>💬 Inquire Now</span></a>`
  );

  // In case there are any remaining openQuickOrderModal for this slug in the HTML:
  html = html.replace(new RegExp(`openQuickOrderModal\\(['"]${slug}['"]\\)`, 'g'), `window.open('https://wa.me/923326861112?text=Hi%20AIDigiTools%2C%20I%20would%20like%20to%20inquire%20about%20${slug}%20availability', '_blank')`);

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`Updated held product HTML: ${filePath}`);
});

// 2. Update scripts/tools_catalog.json
const catalogPath = 'scripts/tools_catalog.json';
if (fs.existsSync(catalogPath)) {
  const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  heldSlugs.forEach(slug => {
    if (catalog[slug]) {
      catalog[slug].available = false;
      catalog[slug].in_stock = false;
      catalog[slug].status = "inquiry_only";
      if (Array.isArray(catalog[slug].plans)) {
        catalog[slug].plans.forEach(p => {
          p.availability = "OutOfStock";
          p.badge = "Inquiry Only";
        });
      }
    }
  });
  fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2), 'utf8');
  console.log('Updated scripts/tools_catalog.json for held products');
}

// 3. Update data/products_master.json
const masterPath = 'data/products_master.json';
if (fs.existsSync(masterPath)) {
  const master = JSON.parse(fs.readFileSync(masterPath, 'utf8'));
  if (Array.isArray(master)) {
    master.forEach(p => {
      if (heldSlugs.includes(p.slug)) {
        p.website_display_status = "Inquiry Only (Held)";
        p.availability_status = "Paused (Inquiry Only)";
        p.sale_eligibility = "Hold / Inquiry Only";
      }
    });
    fs.writeFileSync(masterPath, JSON.stringify(master, null, 2), 'utf8');
    console.log('Updated data/products_master.json for held products');
  }
}
