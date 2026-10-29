import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from .models import AuditIssue

class AccessibilityAuditor:
    """Audits accessibility, mobile viewport, landmarks, and keyboard navigation heuristics."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()

    def audit_accessibility(
        self,
        html_files: List[Path],
        timestamp: str
    ) -> Tuple[List[AuditIssue], Dict[str, Any]]:
        issues: List[AuditIssue] = []
        total_images_checked = 0
        total_buttons_checked = 0

        vague_link_texts = {"click here", "read more", "learn more", "more", "here", "link"}

        for p in html_files:
            rel = p.relative_to(self.root).as_posix()
            try:
                content = p.read_text(encoding="utf-8")
            except Exception:
                continue

            # 1. Viewport Meta Tag (Mobile Rendering)
            if not re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\'][^"\']*width=device-width', content, re.IGNORECASE):
                issues.append(AuditIssue(
                    id="MISSING_MOBILE_VIEWPORT",
                    timestamp=timestamp,
                    tested_url=rel,
                    category="ACCESSIBILITY",
                    severity="CRITICAL",
                    confidence="CONFIRMED",
                    evidence=f"Missing or invalid viewport meta tag in {rel}.",
                    recommended_fix="Add <meta name='viewport' content='width=device-width, initial-scale=1.0'>."
                ))

            # 2. Semantic Landmarks
            for landmark in ["header", "nav", "main", "footer"]:
                if f"<{landmark}" not in content.lower():
                    issues.append(AuditIssue(
                        id=f"MISSING_LANDMARK_{landmark.upper()}",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ACCESSIBILITY",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Missing semantic <{landmark}> landmark tag in {rel}.",
                        recommended_fix=f"Wrap appropriate section in semantic <{landmark}> element."
                    ))

            # 3. Image Alt Attributes
            img_tags = re.findall(r'<img\b[^>]*>', content, re.IGNORECASE)
            for img in img_tags:
                total_images_checked += 1
                alt_m = re.search(r'\balt=["\'](.*?)["\']', img, re.IGNORECASE)
                aria_hidden = "aria-hidden=\"true\"" in img.lower() or "aria-hidden='true'" in img.lower()
                
                if not alt_m and not aria_hidden:
                    issues.append(AuditIssue(
                        id="IMG_MISSING_ALT",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ACCESSIBILITY",
                        severity="ERROR",
                        confidence="CONFIRMED",
                        evidence=f"Image tag missing alt attribute in {rel}: {img[:80]}",
                        recommended_fix="Provide a descriptive alt attribute or aria-hidden='true' if decorative."
                    ))
                elif alt_m and not alt_m.group(1).strip() and not aria_hidden:
                    # Empty alt without aria-hidden
                    issues.append(AuditIssue(
                        id="IMG_EMPTY_ALT",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ACCESSIBILITY",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Image tag has empty alt attribute in {rel}: {img[:80]}",
                        recommended_fix="Populate alt attribute with descriptive text or mark aria-hidden='true'."
                    ))

            # 4. Button Accessible Name
            button_tags = re.findall(r'<button\b[^>]*>(.*?)</button>', content, re.IGNORECASE | re.DOTALL)
            for btn_text in button_tags:
                total_buttons_checked += 1
                clean_btn = re.sub(r'<[^>]+>', '', btn_text).strip()
                # Check if button has aria-label in inner context
                if not clean_btn:
                    # Look up button full tag
                    issues.append(AuditIssue(
                        id="BUTTON_EMPTY_TEXT",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ACCESSIBILITY",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Button element in {rel} has no visible text.",
                        recommended_fix="Add descriptive text or an aria-label to the button."
                    ))

            # 5. Keyboard Navigation & Tabindex
            tabindex_matches = re.findall(r'\btabindex=["\']([^"\']+)["\']', content, re.IGNORECASE)
            for tid in tabindex_matches:
                try:
                    ival = int(tid)
                    if ival > 0:
                        issues.append(AuditIssue(
                            id="DISRUPTIVE_POSITIVE_TABINDEX",
                            timestamp=timestamp,
                            tested_url=rel,
                            category="ACCESSIBILITY",
                            severity="WARNING",
                            confidence="CONFIRMED",
                            evidence=f"Positive tabindex='{tid}' found in {rel}, which disrupts natural tab order.",
                            recommended_fix="Use natural DOM source ordering and set tabindex='0' or '-1'."
                        ))
                except ValueError:
                    pass

            # 6. Vague Link Texts
            link_matches = re.findall(r'<a\b[^>]*>(.*?)</a>', content, re.IGNORECASE | re.DOTALL)
            for ltext in link_matches:
                plain_ltext = re.sub(r'<[^>]+>', '', ltext).strip().lower()
                if plain_ltext in vague_link_texts:
                    issues.append(AuditIssue(
                        id="VAGUE_LINK_ANCHOR_TEXT",
                        timestamp=timestamp,
                        tested_url=rel,
                        category="ACCESSIBILITY",
                        severity="WARNING",
                        confidence="CONFIRMED",
                        evidence=f"Vague anchor text '{plain_ltext}' found in {rel}.",
                        recommended_fix="Replace generic anchor text with descriptive context-rich destination phrase."
                    ))

        summary = {
            "total_images_checked": total_images_checked,
            "total_buttons_checked": total_buttons_checked
        }
        return issues, summary
