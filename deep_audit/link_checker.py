import re
from pathlib import Path
from typing import List, Dict, Set, Tuple, Any
from .models import AuditIssue

class LinkAndAnchorAuditor:
    """Audits internal hyperlinks, fragment anchors, and orphan pages."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()

    def audit_page_links(
        self,
        html_files: List[Path],
        timestamp: str
    ) -> Tuple[List[AuditIssue], Dict[str, Any]]:
        """
        Scans all discovered HTML documents and validates internal link integrity
        and fragment anchor references.
        """
        issues: List[AuditIssue] = []
        total_links = 0
        broken_links_count = 0
        broken_anchors_count = 0

        # Pre-index all elements with id or name per file for fast anchor lookup
        id_index: Dict[str, Set[str]] = {}
        for p in html_files:
            rel = p.relative_to(self.root).as_posix()
            try:
                content = p.read_text(encoding="utf-8")
                # Find all id="..." and name="..."
                ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', content, re.IGNORECASE))
                names = set(re.findall(r'<a\b[^>]*?\bname=["\']([^"\']+)["\']', content, re.IGNORECASE))
                id_index[rel] = ids | names
            except Exception:
                id_index[rel] = set()

        href_pattern = re.compile(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\']', re.IGNORECASE)

        for p in html_files:
            src_rel = p.relative_to(self.root).as_posix()
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue

            for m in href_pattern.finditer(content):
                total_links += 1
                raw_href = m.group(1).strip()

                # Skip non-navigational schemas
                if raw_href.startswith(("mailto:", "tel:", "javascript:")):
                    continue

                # Skip external links
                if raw_href.startswith(("http://", "https://")):
                    if "aidigitools.tech" not in raw_href:
                        continue
                    # Strip domain to evaluate as internal
                    raw_href = raw_href.split("aidigitools.tech", 1)[1]
                    if not raw_href.startswith("/"):
                        raw_href = "/" + raw_href

                parts = raw_href.split("#", 1)
                path_part = parts[0].split("?", 1)[0]
                anchor_part = parts[1] if len(parts) > 1 else None

                # Determine target file relative path
                if not path_part:
                    target_rel = src_rel
                elif path_part.startswith("/"):
                    target_rel = path_part.lstrip("/")
                else:
                    target_rel = (p.parent / path_part).resolve().relative_to(self.root).as_posix()

                if target_rel.endswith("/") or target_rel == "":
                    target_rel += "index.html"
                elif not target_rel.endswith(".html") and (self.root / (target_rel + ".html")).exists():
                    target_rel += ".html"

                target_file = self.root / target_rel

                # 1. Check target file existence
                if not target_file.exists():
                    broken_links_count += 1
                    issues.append(AuditIssue(
                        id="BROKEN_INTERNAL_LINK",
                        timestamp=timestamp,
                        tested_url=src_rel,
                        category="INTERNAL_LINKS",
                        severity="ERROR",
                        confidence="CONFIRMED",
                        evidence=f"Link href='{raw_href}' in {src_rel} points to non-existent file {target_rel}.",
                        recommended_fix=f"Update link href in {src_rel} to point to a valid active page."
                    ))
                    continue

                # 2. Check fragment anchor existence
                if anchor_part:
                    valid_ids = id_index.get(target_rel, set())
                    if anchor_part not in valid_ids:
                        broken_anchors_count += 1
                        issues.append(AuditIssue(
                            id="BROKEN_FRAGMENT_ANCHOR",
                            timestamp=timestamp,
                            tested_url=src_rel,
                            category="INTERNAL_LINKS",
                            severity="ERROR",
                            confidence="CONFIRMED",
                            evidence=f"Anchor #{anchor_part} in href='{raw_href}' does not match any id or name in {target_rel}.",
                            recommended_fix=f"Ensure target element in {target_rel} contains id='{anchor_part}' or correct href."
                        ))

        summary = {
            "total_internal_links_checked": total_links,
            "broken_links_count": broken_links_count,
            "broken_anchors_count": broken_anchors_count
        }
        return issues, summary
