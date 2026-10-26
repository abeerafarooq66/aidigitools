"""
Add Organization structured data to index.html for AIDigiTools Brand Entity recognition.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "index.html"

content = INDEX_PATH.read_text(encoding="utf-8")

org_schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "AIDigiTools",
    "url": "https://aidigitools.tech/",
    "logo": "https://aidigitools.tech/assets/images/aidigitools-logo.svg",
    "description": "Premier verified AI software subscription marketplace and digital tools concierge serving Pakistan and worldwide.",
    "email": "support@aidigitools.tech",
    "telephone": "+92-332-6861112",
    "contactPoint": [
      {
        "@type": "ContactPoint",
        "telephone": "+92-332-6861112",
        "contactType": "customer service",
        "contactOption": "TollFree",
        "areaServed": ["PK", "Worldwide"],
        "availableLanguage": ["en", "ur"]
      }
    ],
    "sameAs": [
      "https://github.com/abeerafarooq66/aidigitools"
    ]
  }
  </script>
"""

# Check if Organization schema is already present
if '"@type": "Organization"' not in content:
    # Insert right before </head>
    content = content.replace('</head>', f'{org_schema}</head>')
    INDEX_PATH.write_text(content, encoding="utf-8")
    print("Successfully added Organization schema to index.html")
else:
    print("Organization schema already present in index.html")
