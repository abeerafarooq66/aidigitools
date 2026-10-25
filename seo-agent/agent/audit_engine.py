import re
import json
from pathlib import Path

class TechnicalAuditEngine:
    """HERMES 10-Step Technical SEO Audit Engine."""

    def __init__(self, root_dir: Path | str = "."):
        self.root = Path(root_dir)

    def audit_page(self, file_path: Path) -> dict:
        content = file_path.read_text(encoding="utf-8")
        checks = {}

        # 1. Title tag (30 - 65 chars)
        title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else ""
        checks["title"] = {
            "passed": 30 <= len(title) <= 65,
            "value": title,
            "length": len(title),
            "step": 1,
            "message": "Title length optimal" if 30 <= len(title) <= 65 else f"Title length {len(title)} outside 30-65 range"
        }

        # 2. Meta description (70 - 160 chars)
        desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
        desc = desc_m.group(1).strip() if desc_m else ""
        checks["meta_description"] = {
            "passed": 70 <= len(desc) <= 165,
            "value": desc,
            "length": len(desc),
            "step": 2,
            "message": "Meta description optimal" if 70 <= len(desc) <= 165 else f"Meta description length {len(desc)} outside 70-165 range"
        }

        # 3. Canonical URL
        canon_m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', content, re.IGNORECASE)
        canonical = canon_m.group(1).strip() if canon_m else ""
        checks["canonical"] = {
            "passed": canonical.startswith("https://aidigitools.tech"),
            "value": canonical,
            "step": 3,
            "message": "Valid canonical URL" if canonical.startswith("https://aidigitools.tech") else "Missing or non-canonical URL"
        }

        # 4. Mobile Viewport
        vp_m = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
        checks["viewport"] = {
            "passed": bool(vp_m and "width=device-width" in vp_m.group(1)),
            "step": 4,
            "message": "Mobile viewport present" if vp_m else "Missing mobile viewport"
        }

        # 5. Single H1
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        checks["single_h1"] = {
            "passed": len(h1s) == 1,
            "count": len(h1s),
            "step": 5,
            "message": f"Exactly 1 H1 found" if len(h1s) == 1 else f"Found {len(h1s)} H1 tags"
        }

        # 6. OpenGraph tags
        og_title = bool(re.search(r'<meta[^>]*property=["\']og:title["\']', content, re.IGNORECASE))
        og_desc = bool(re.search(r'<meta[^>]*property=["\']og:description["\']', content, re.IGNORECASE))
        og_url = bool(re.search(r'<meta[^>]*property=["\']og:url["\']', content, re.IGNORECASE))
        og_passed = og_title and og_desc and og_url
        checks["opengraph"] = {
            "passed": og_passed,
            "step": 6,
            "message": "OpenGraph tags complete" if og_passed else "Missing og:title, og:desc or og:url"
        }

        # 7. Twitter Card
        tw_card = bool(re.search(r'<meta[^>]*name=["\']twitter:card["\']', content, re.IGNORECASE))
        tw_title = bool(re.search(r'<meta[^>]*name=["\']twitter:title["\']', content, re.IGNORECASE))
        tw_passed = tw_card and tw_title
        checks["twitter_card"] = {
            "passed": tw_passed,
            "step": 7,
            "message": "Twitter card tags complete" if tw_passed else "Missing twitter card tags"
        }

        # 8. Structured Data JSON-LD
        schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', content, re.IGNORECASE | re.DOTALL)
        schema_valid = False
        if schemas:
            try:
                for s in schemas:
                    json.loads(s)
                schema_valid = True
            except json.JSONDecodeError:
                schema_valid = False
        checks["json_ld"] = {
            "passed": schema_valid,
            "count": len(schemas),
            "step": 8,
            "message": "Valid JSON-LD schema found" if schema_valid else "Missing or malformed JSON-LD"
        }

        # 9. Image Alt Attributes
        imgs = re.findall(r'<img\s+([^>]+)>', content, re.IGNORECASE)
        imgs_missing_alt = [img for img in imgs if not re.search(r'\balt=["\']', img, re.IGNORECASE)]
        img_passed = len(imgs_missing_alt) == 0
        checks["image_alt"] = {
            "passed": img_passed,
            "total_images": len(imgs),
            "missing_alt": len(imgs_missing_alt),
            "step": 9,
            "message": "All images have alt tags" if img_passed else f"{len(imgs_missing_alt)} images missing alt text"
        }

        # 10. Language attribute
        lang_m = re.search(r'<html[^>]*lang=["\']([a-zA-Z\-]+)["\']', content, re.IGNORECASE)
        checks["html_lang"] = {
            "passed": bool(lang_m),
            "value": lang_m.group(1) if lang_m else "",
            "step": 10,
            "message": "HTML lang attribute set" if lang_m else "Missing html lang attribute"
        }

        passed_steps = sum(1 for c in checks.values() if c["passed"])
        score = (passed_steps / len(checks)) * 100.0

        return {
            "file": str(file_path),
            "checks": checks,
            "passed_steps": passed_steps,
            "total_steps": len(checks),
            "seo_score": round(score, 1),
            "status": "PASS" if score >= 80.0 else "FAIL"
        }

    def audit_site(self) -> dict:
        pages = list(self.root.glob("*.html")) + list(self.root.glob("tools/*.html")) + list(self.root.glob("guides/*.html"))
        results = [self.audit_page(p) for p in sorted(pages)]

        # Check robots.txt and sitemap.xml
        robots_exists = (self.root / "robots.txt").is_file()
        sitemap_exists = (self.root / "sitemap.xml").is_file()

        avg_score = (sum(r["seo_score"] for r in results) / len(results)) if results else 0.0

        return {
            "pages_scanned": len(results),
            "results": results,
            "robots_txt_exists": robots_exists,
            "sitemap_xml_exists": sitemap_exists,
            "average_seo_score": round(avg_score, 1),
            "all_passed": all(r["status"] == "PASS" for r in results) and robots_exists and sitemap_exists
        }
