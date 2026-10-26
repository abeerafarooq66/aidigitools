"""
Comprehensive SEO + GEO + AEO Audit Engine for AIDigiTools.
Audits all 52 pages against Google Search, Bing Webmaster, and AI Overviews standards.
"""

import json
import re
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent

class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.meta_desc = ""
        self.canonical = ""
        self.og_title = ""
        self.og_desc = ""
        self.og_image = ""
        self.h1_list = []
        self.h2_list = []
        self.in_h1 = False
        self.in_h2 = False
        self.current_h1 = ""
        self.current_h2 = ""
        self.json_ld = []
        self.in_json_ld = False
        self.current_json_ld = ""
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.meta_desc = content
            elif prop == "og:title":
                self.og_title = content
            elif prop == "og:description":
                self.og_desc = content
            elif prop == "og:image":
                self.og_image = content
        elif tag == "link":
            rel = attrs_dict.get("rel", "").lower()
            if rel == "canonical":
                self.canonical = attrs_dict.get("href", "")
        elif tag == "h1":
            self.in_h1 = True
            self.current_h1 = ""
        elif tag == "h2":
            self.in_h2 = True
            self.current_h2 = ""
        elif tag == "script":
            if attrs_dict.get("type") == "application/ld+json":
                self.in_json_ld = True
                self.current_json_ld = ""
        elif tag == "img":
            self.images.append({
                "src": attrs_dict.get("src", ""),
                "alt": attrs_dict.get("alt", None),
                "width": attrs_dict.get("width"),
                "height": attrs_dict.get("height")
            })

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            self.h1_list.append(self.current_h1.strip())
        elif tag == "h2":
            self.in_h2 = False
            self.h2_list.append(self.current_h2.strip())
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            try:
                parsed = json.loads(self.current_json_ld.strip())
                self.json_ld.append(parsed)
            except Exception as e:
                self.json_ld.append({"ERROR": str(e), "raw": self.current_json_ld.strip()})

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.current_h1 += data
        elif self.in_h2:
            self.current_h2 += data
        elif self.in_json_ld:
            self.current_json_ld += data

def audit():
    html_files = sorted([p for p in ROOT.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)])
    print(f"Total HTML files to audit: {len(html_files)}")
    
    audit_results = []
    
    for hf in html_files:
        rel = hf.relative_to(ROOT).as_posix()
        raw = hf.read_text(encoding="utf-8")
        parser = HeadParser()
        parser.feed(raw)
        
        # Word count of quick answer if present
        qa_match = re.search(r'<p class="quick-answer[^"]*">(.*?)</p>', raw, re.DOTALL)
        qa_word_count = len(re.sub(r'<[^>]+>', '', qa_match.group(1)).split()) if qa_match else 0
        
        # Total body word count approximately
        body_text = re.sub(r'<[^>]+>', ' ', raw)
        total_words = len(body_text.split())
        
        # Schema checks
        schema_types = []
        schema_errors = []
        for s in parser.json_ld:
            if "ERROR" in s:
                schema_errors.append(s["ERROR"])
            else:
                stype = s.get("@type", "unknown")
                if isinstance(stype, list):
                    stype = ",".join(stype)
                schema_types.append(stype)
                
        # Image checks
        missing_alts = [img["src"] for img in parser.images if img["alt"] is None]
        
        # Page classification
        if rel == "index.html":
            page_type = "Homepage"
        elif rel.startswith("tools/"):
            page_type = "Tool Detail"
        elif rel.startswith("categories/"):
            page_type = "Category Hub"
        elif rel.startswith("guides/"):
            page_type = "In-Depth Guide"
        elif rel.startswith("compare/"):
            page_type = "Comparison"
        elif rel.startswith("best/"):
            page_type = "Best Listicle"
        elif rel in ("about.html", "contact.html"):
            page_type = "E-E-A-T & Trust"
        elif rel in ("policies.html", "shipping-policy.html", "affiliate-disclosure.html"):
            page_type = "Legal & Warranty Policy"
        elif rel == "deals.html":
            page_type = "Deals & Bundles"
        else:
            page_type = "Content Page"

        audit_results.append({
            "file": rel,
            "page_type": page_type,
            "title": parser.title.strip(),
            "title_len": len(parser.title.strip()),
            "meta_desc": parser.meta_desc.strip(),
            "meta_desc_len": len(parser.meta_desc.strip()),
            "canonical": parser.canonical,
            "h1_count": len(parser.h1_list),
            "h1": parser.h1_list[0] if parser.h1_list else "",
            "h2_count": len(parser.h2_list),
            "qa_words": qa_word_count,
            "total_words": total_words,
            "schema_types": schema_types,
            "schema_errors": schema_errors,
            "missing_alts_count": len(missing_alts),
            "og_image": parser.og_image
        })
        
    out_file = ROOT / "scripts" / "audit_results.json"
    out_file.write_text(json.dumps(audit_results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Audit completed for {len(audit_results)} pages. Saved to {out_file}")

if __name__ == "__main__":
    audit()
