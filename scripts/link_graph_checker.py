import os
import re
import sys
import argparse
from pathlib import Path
from html.parser import HTMLParser

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if "id" in attr_dict:
            self.ids.add(attr_dict["id"])
        if tag == "a":
            if "name" in attr_dict:
                self.ids.add(attr_dict["name"])
            if "href" in attr_dict:
                self.links.append(attr_dict["href"])

def check_link_graph(root_dir: Path | str = ".", strict: bool = False) -> dict:
    root = Path(root_dir).resolve()
    html_files = [p for p in root.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)]

    if not html_files:
        print("[LinkGraph] No HTML files found.")
        return {"total_pages": 0, "total_links": 0, "broken_links": 0, "broken_anchors": 0, "passed": True}

    page_data = {}
    for hf in html_files:
        parser = LinkExtractor()
        content = hf.read_text(encoding="utf-8")
        parser.feed(content)
        rel_path = hf.relative_to(root).as_posix()
        page_data[rel_path] = {
            "path": hf,
            "ids": parser.ids,
            "links": parser.links
        }

    broken_links = []
    broken_anchors = []
    total_links_inspected = 0

    for source_rel, data in page_data.items():
        source_dir = Path(source_rel).parent

        for href in data["links"]:
            # Skip external or non-http links
            if href.startswith(("http://", "https://")):
                if not href.startswith("https://aidigitools.tech"):
                    continue
                # Canonical self-referencing links
                href_clean = href.replace("https://aidigitools.tech/", "")
            elif href.startswith(("mailto:", "tel:", "javascript:", "wa.me", "https://wa.me")):
                continue
            else:
                href_clean = href

            total_links_inspected += 1

            # Split path and fragment anchor
            if "#" in href_clean:
                target_path_part, fragment = href_clean.split("#", 1)
            else:
                target_path_part, fragment = href_clean, ""

            # Same page anchor link (e.g. #pricing)
            if not target_path_part:
                target_rel = source_rel
            elif target_path_part.startswith("/"):
                # Absolute from site root
                target_rel = target_path_part.lstrip("/")
                if not target_rel:
                    target_rel = "index.html"
            else:
                # Relative to source file's directory
                combined = os.path.join(str(source_dir), target_path_part)
                norm = os.path.normpath(combined).replace("\\", "/")
                # Clean up any leading ./ or .
                if norm == ".":
                    norm = "index.html"
                elif norm.startswith("./"):
                    norm = norm[2:]
                target_rel = norm

            # Check if target file exists
            if target_rel not in page_data:
                # check if target_rel ends in / or is directory mapping to index.html
                alt_rel = target_rel.rstrip("/") + "/index.html" if not target_rel.endswith(".html") else target_rel
                if alt_rel in page_data:
                    target_rel = alt_rel
                elif (root / target_rel).is_file():
                    # Static asset file (e.g. .css, .webp)
                    continue
                else:
                    broken_links.append({
                        "source": source_rel,
                        "href": href,
                        "target": target_rel,
                        "reason": "Target file does not exist"
                    })
                    continue

            # Check fragment anchor if specified
            if fragment:
                target_ids = page_data[target_rel]["ids"]
                if fragment not in target_ids:
                    broken_anchors.append({
                        "source": source_rel,
                        "href": href,
                        "target_page": target_rel,
                        "missing_anchor": fragment,
                        "reason": f"Anchor #{fragment} not found in {target_rel}"
                    })

    passed = (len(broken_links) == 0) and (len(broken_anchors) == 0)

    print("=" * 60)
    print(f"🔗 AIDigiTools Link Graph & Anchor Integrity Report")
    print("=" * 60)
    print(f"Total Pages Checked: {len(page_data)}")
    print(f"Total Internal Links Checked: {total_links_inspected}")
    print(f"Broken Internal Links: {len(broken_links)}")
    print(f"Broken Anchors: {len(broken_anchors)}")

    if broken_links:
        print("\n❌ Broken Links:")
        for bl in broken_links:
            print(f"  - In {bl['source']} -> '{bl['href']}' ({bl['reason']})")

    if broken_anchors:
        print("\n❌ Broken Anchors:")
        for ba in broken_anchors:
            print(f"  - In {ba['source']} -> '{ba['href']}' ({ba['reason']})")

    if passed:
        print("\n✅ 100% LINK GRAPH INTEGRITY: 0 Broken Links, 0 Broken Anchors!")

    return {
        "total_pages": len(page_data),
        "total_links": total_links_inspected,
        "broken_links": broken_links,
        "broken_anchors": broken_anchors,
        "passed": passed
    }

def main():
    parser = argparse.ArgumentParser(description="Strict Link Graph and Anchor Validator")
    parser.add_argument("--root", default=".", help="Root directory")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 on any error")
    args = parser.parse_args()

    res = check_link_graph(args.root, args.strict)
    if args.strict and not res["passed"]:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
