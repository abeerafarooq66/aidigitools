const fs = require('fs');

const policiesPath = 'policies.html';
let html = fs.readFileSync(policiesPath, 'utf8');

const cleanSchema = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://aidigitools.tech/#organization",
      "name": "AIDigiTools",
      "url": "https://aidigitools.tech/",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://aidigitools.tech/#logo",
        "url": "https://aidigitools.tech/assets/images/logo.png",
        "caption": "AIDigiTools"
      },
      "telephone": "+92-332-6861112",
      "email": "support@aidigitools.tech",
      "sameAs": [
        "https://github.com/abeerafarooq66",
        "https://wa.me/923326861112"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+92-332-6861112",
        "contactType": "customer service",
        "areaServed": "PK",
        "availableLanguage": ["English", "Urdu"]
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://aidigitools.tech/#website",
      "url": "https://aidigitools.tech/",
      "name": "AIDigiTools",
      "publisher": {
        "@id": "https://aidigitools.tech/#organization"
      }
    },
    {
      "@type": "WebPage",
      "@id": "https://aidigitools.tech/policies.html#webpage",
      "url": "https://aidigitools.tech/policies.html",
      "name": "Payment & Warranty Policies",
      "description": "Official operating rules, domestic payment rail specifications, and 30-day replacement warranty guidelines for AIDigiTools in Pakistan and worldwide.",
      "isPartOf": {
        "@id": "https://aidigitools.tech/#website"
      },
      "breadcrumb": {
        "@id": "https://aidigitools.tech/policies.html#breadcrumb"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://aidigitools.tech/policies.html#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://aidigitools.tech/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Terms & Policies",
          "item": "https://aidigitools.tech/policies.html"
        }
      ]
    }
  ]
};

const jsonStr = JSON.stringify(cleanSchema, null, 2);
html = html.replace(
  /<script\s+type=["']application\/ld\+json["']>[\s\S]*?<\/script>/i,
  `<script type="application/ld+json">\n${jsonStr}\n  </script>`
);

fs.writeFileSync(policiesPath, html, 'utf8');
console.log('Successfully cleaned schema in policies.html');
