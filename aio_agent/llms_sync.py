import re
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
            "## Buying Guides & Comparisons",
            ""
        ])

        guides_dir = self.root / "guides"
        if guides_dir.exists():
            for p in sorted(guides_dir.glob("*.html")):
                meta = self.extract_meta(p)
                lines.append(f"- [{meta['title']}]({meta['url']}): {meta['description']}")

        lines.extend([
            "",
            "## Operational Rails & Corporate Identity",
            "- [About Company](https://aidigitools.tech/about.html): Founding mission, corporate background, and 1,200+ active subscriptions.",
            "- [Customer Help Desk](https://aidigitools.tech/contact.html): Real human assistance in Islamabad via WhatsApp (+92 300 1234567) and email (support@aidigitools.tech).",
            "- [Digital Delivery Policy & SLA](https://aidigitools.tech/shipping-policy.html): Free electronic delivery (Rs. 0) with a 15-minute average fulfillment SLA.",
            "- [Payment Rails & Protection](https://aidigitools.tech/policies.html#payments): EasyPaisa, JazzCash, SadaPay, Raast, Bank IBFT.",
            "- [Replacement Warranty](https://aidigitools.tech/policies.html#refunds): 30-day full replacement guarantee or pro-rata domestic refund."
        ])

        return "\n".join(lines) + "\n"

    def sync(self) -> dict:
        content = self.generate_llms_txt()
        llms_path = self.root / "llms.txt"
        llms_full_path = self.root / "llms-full.txt"

        llms_path.write_text(content, encoding="utf-8")
        llms_full_path.write_text(content, encoding="utf-8")

        return {
            "status": "SUCCESS",
            "llms_path": str(llms_path),
            "llms_full_path": str(llms_full_path),
            "bytes_written": len(content.encode("utf-8"))
        }
