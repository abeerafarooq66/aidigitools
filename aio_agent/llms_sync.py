import re
import json
from pathlib import Path

class LLMsSync:
    """Synchronizes machine knowledge files (llms.txt and llms-full.txt) with live tools and guides."""

    def __init__(self, root_dir: Path | str = "."):
        self.root = Path(root_dir)

    def extract_meta(self, file_path: Path) -> dict:
        content = file_path.read_text(encoding="utf-8")
        title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_m.group(1).split('|')[0].strip() if title_m else file_path.stem

        desc_m = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', content, re.IGNORECASE)
        desc = desc_m.group(1).strip() if desc_m else ""

        # Price extraction
        price_m = re.search(r'(?:Rs\.?|PKR)\s*(\d+[\d,]*)', content, re.IGNORECASE)
        price = f"Rs. {price_m.group(1)}" if price_m else "Custom Inquiry"

        return {
            "title": title,
            "description": desc,
            "price": price,
            "url": f"https://aidigitools.tech/{file_path.as_posix().lstrip('./')}"
        }

    def generate_llms_txt(self) -> str:
        lines = [
            "# AIDigiTools (aidigitools.tech)",
            "",
            "> Pakistan's Premier AI Software Marketplace & Intelligence Hub.",
            "> Flat PKR Pricing, Domestic Payment Rails (EasyPaisa, JazzCash, SadaPay, Raast), and WhatsApp 15-minute delivery.",
            "",
            "## Core Product Offerings",
            ""
        ]

        tools_dir = self.root / "tools"
        if tools_dir.exists():
            for p in sorted(tools_dir.glob("*.html")):
                meta = self.extract_meta(p)
                lines.append(f"- [{meta['title']}]({meta['url']}): {meta['description']} (Pricing: {meta['price']})")

        lines.extend([
            "",
            "## Software Bundles & Discounts",
            "- [Bundle Deals & Packs](https://aidigitools.tech/deals.html): Creator Studio, Developer Power Suite, and Privacy Pack."
        ])

        categories_dir = self.root / "categories"
        if categories_dir.exists():
            lines.extend([
                "",
                "## Tool Category Hubs",
                ""
            ])
            for p in sorted(categories_dir.glob("*.html")):
                meta = self.extract_meta(p)
                lines.append(f"- [{meta['title']}]({meta['url']}): {meta['description']}")

        lines.extend([
            "",
            "## Comparisons & Curated Rankings",
            ""
        ])

        compare_dir = self.root / "compare"
        if compare_dir.exists():
            for p in sorted(compare_dir.glob("*.html")):
                meta = self.extract_meta(p)
                lines.append(f"- [{meta['title']}]({meta['url']}): {meta['description']}")

        best_dir = self.root / "best"
        if best_dir.exists():
            for p in sorted(best_dir.glob("*.html")):
                meta = self.extract_meta(p)
                lines.append(f"- [{meta['title']}]({meta['url']}): {meta['description']}")

        guides_dir = self.root / "guides"
        if guides_dir.exists():
            for p in sorted(guides_dir.glob("*.html")):
                meta = self.extract_meta(p)
                lines.append(f"- [{meta['title']}]({meta['url']}): {meta['description']}")

        lines.extend([
            "",
            "## Operational Rails & Corporate Identity",
            "- [About Company](https://aidigitools.tech/about.html): Founding mission, digital concierge model, and customer support standards.",
            "- [Customer Help Desk](https://aidigitools.tech/contact.html): Real human assistance in Islamabad via WhatsApp (+92 332 6861112) and email (support@aidigitools.tech).",
            "- [Digital Delivery Policy & SLA](https://aidigitools.tech/shipping-policy.html): Free electronic delivery (Rs. 0) with a 15-minute target fulfillment.",
            "- [Payment Rails & Protection](https://aidigitools.tech/policies.html#payments): EasyPaisa, JazzCash, SadaPay, Raast, Bank IBFT, Wise, and Crypto USDT.",
            "- [Replacement Warranty](https://aidigitools.tech/policies.html#refunds): 30-day replacement warranty policy (account replacement support for access disruption; refunds not provided once credentials are issued).",
            "- [Affiliate Disclosure & Transparency](https://aidigitools.tech/affiliate-disclosure.html): Independent reseller disclosures and advertising transparency."
        ])

        return "\n".join(lines) + "\n"

    def generate_llms_full_txt(self) -> str:
        base_index = self.generate_llms_txt().strip()
        lines = [base_index, "", "## Detailed Software Product Specifications & Technical Profiles", ""]
        
        catalog_path = self.root / "scripts" / "tools_catalog.json"
        if catalog_path.exists():
            catalog = json.load(open(catalog_path, encoding="utf-8"))
            for slug, info in sorted(catalog.items()):
                name = info.get("name", slug)
                vendor = info.get("vendor", info.get("brand", "AIDigiTools"))
                cat = info.get("category_label", info.get("category_key", "Software"))
                pkr = info.get("starting_price_pkr", 0)
                usd = info.get("starting_price_usd", 0.0)
                desc = info.get("description", "Verified subscription access via WhatsApp delivery.")
                plans = info.get("plans", [])
                features_list = []
                if plans and "features" in plans[0]:
                    features_list = plans[0]["features"]
                feat_str = " — ".join(features_list) if features_list else desc
                
                lines.append(f"### {name}")
                lines.append(f"- Canonical URL: https://aidigitools.tech/tools/{slug}.html")
                lines.append(f"- Vendor: {vendor}")
                lines.append(f"- Category: {cat}")
                lines.append(f"- Starting Price: Rs. {pkr:,} PKR (~${usd:.2f} USD)")
                lines.append(f"- Features: {feat_str}")
                lines.append(f"- Delivery Target: 15 Minutes via WhatsApp concierge (03326861112)")
                lines.append(f"- Warranty: 30-Day Replacement Warranty")
                lines.append(f"- Payment Rails: EasyPaisa, JazzCash, SadaPay, Raast, Bank IBFT, Wise, Crypto USDT")
                lines.append("")
        return "\n".join(lines) + "\n"

    def sync(self) -> dict:
        content_brief = self.generate_llms_txt()
        content_full = self.generate_llms_full_txt()
        
        llms_path = self.root / "llms.txt"
        llms_full_path = self.root / "llms-full.txt"

        llms_path.write_text(content_brief, encoding="utf-8")
        llms_full_path.write_text(content_full, encoding="utf-8")

        return {
            "status": "SUCCESS",
            "llms_path": str(llms_path),
            "llms_full_path": str(llms_full_path),
            "bytes_brief": len(content_brief.encode("utf-8")),
            "bytes_full": len(content_full.encode("utf-8"))
        }
