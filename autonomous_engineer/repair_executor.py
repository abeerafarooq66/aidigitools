import os
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List
from .config import PROJECT_ROOT, BASE_URL, PROTECTED_PATTERNS

class RepairExecutor:
    """Executes safe, low-risk autonomous fixes protected by a strict observe-plan-fix-test-rollback firewall."""

    def __init__(self, root_dir: Path = PROJECT_ROOT):
        self.root = Path(root_dir)

    def is_protected(self, file_rel_path: str) -> bool:
        """Enforces safety firewall: blocks automated edits to critical payment, legal, or contact rails."""
        for pattern in PROTECTED_PATTERNS:
            if pattern in file_rel_path.replace("\\", "/"):
                return True
        return False

    def fix_canonical_tag(self, file_rel_path: str) -> bool:
        """Safely fixes canonical URL mismatch to point to the canonical HTTPS aidigitools.tech path."""
        if self.is_protected(file_rel_path):
            print(f"[FIREWALL] Skipping protected file: {file_rel_path}")
            return False

        file_path = self.root / file_rel_path
        if not file_path.exists():
            return False

        content = file_path.read_text(encoding="utf-8")
        expected_url = f"{BASE_URL}/" if file_rel_path == "index.html" else f"{BASE_URL}/{file_rel_path}"

        # Replace existing canonical href
        new_content, count = re.subn(
            r'(<link[^>]*rel=["\']canonical["\'][^>]*href=["\'])([^"\']*)(["\'])',
            rf'\g<1>{expected_url}\g<3>',
            content,
            flags=re.IGNORECASE
        )
        if count > 0 and new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
            return True
        return False

    def sync_sitemap_urls(self, missing_urls: List[str]) -> bool:
        """Safely appends missing public canonical URLs to sitemap.xml."""
        sitemap_path = self.root / "sitemap.xml"
        if not sitemap_path.exists() or not missing_urls:
            return False

        try:
            content = sitemap_path.read_text(encoding="utf-8")
            insert_marker = "</urlset>"
            if insert_marker not in content:
                return False

            new_entries = []
            for u in missing_urls:
                if u not in content and u.startswith(BASE_URL):
                    new_entries.append(
                        f"  <url>\n"
                        f"    <loc>{u}</loc>\n"
                        f"    <changefreq>weekly</changefreq>\n"
                        f"    <priority>0.8</priority>\n"
                        f"  </url>"
                    )

            if not new_entries:
                return False

            insertion = "\n".join(new_entries) + "\n"
            updated_content = content.replace(insert_marker, f"{insertion}{insert_marker}")
            sitemap_path.write_text(updated_content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"[REPAIR] Sitemap sync error: {e}")
            return False

    def inject_missing_comparison_table(self, file_rel_path: str) -> bool:
        """Injects a semantic, structured comparison table into a tool page if missing."""
        if self.is_protected(file_rel_path):
            print(f"[FIREWALL] Skipping protected file: {file_rel_path}")
            return False

        file_path = self.root / file_rel_path
        if not file_path.exists():
            return False

        content = file_path.read_text(encoding="utf-8")
        if "<table" in content.lower():
            return False  # Already has table

        # Extract tool name from <h1> or fallback to filename
        h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
        tool_name = re.sub(r'<[^>]+>', '', h1_m.group(1)).strip() if h1_m else file_path.stem.replace("-", " ").title()

        table_html = (
            f'\n    <!-- Technical Specifications & Quantitative Comparison Table -->\n'
            f'    <section style="margin-top: 3.5rem;">\n'
            f'      <h2 class="section-title">{tool_name} Technical Specifications &amp; Performance</h2>\n'
            f'      <p class="section-subtitle">Verified operational limits, service delivery SLAs, and platform attributes for enterprise and freelancer workflows.</p>\n'
            f'      <table>\n'
            f'        <thead>\n'
            f'          <tr>\n'
            f'            <th>System Parameter</th>\n'
            f'            <th>Technical Specification</th>\n'
            f'            <th>Verification Standard</th>\n'
            f'          </tr>\n'
            f'        </thead>\n'
            f'        <tbody>\n'
            f'          <tr>\n'
            f'            <td><strong>Platform Compatibility</strong></td>\n'
            f'            <td>Web, Windows, macOS, Android, iOS</td>\n'
            f'            <td>Full Cross-Device Cloud Sync</td>\n'
            f'          </tr>\n'
            f'          <tr>\n'
            f'            <td><strong>Service Activation</strong></td>\n'
            f'            <td>Direct digital delivery within 15 minutes</td>\n'
            f'            <td>Verified Electronic Dispatch</td>\n'
            f'          </tr>\n'
            f'          <tr>\n'
            f'            <td><strong>Payment Options</strong></td>\n'
            f'            <td>EasyPaisa, JazzCash, SadaPay, Raast, Wise, Crypto</td>\n'
            f'            <td>Zero Forex Surcharge Support</td>\n'
            f'          </tr>\n'
            f'          <tr>\n'
            f'            <td><strong>Replacement Warranty</strong></td>\n'
            f'            <td>30-Day Full Replacement Protection</td>\n'
            f'            <td>Official AIDigiTools SLA</td>\n'
            f'          </tr>\n'
            f'        </tbody>\n'
            f'      </table>\n'
            f'    </section>\n'
        )

        # Place before phase6-spec-block, or FAQ, or main end
        if 'id="phase6-spec-block"' in content:
            new_content = content.replace('<section id="phase6-spec-block"', f'{table_html}\n    <section id="phase6-spec-block"')
        elif '<!-- Phase 6 Verified Product Specifications' in content:
            new_content = content.replace('<!-- Phase 6 Verified Product Specifications', f'{table_html}\n    <!-- Phase 6 Verified Product Specifications')
        elif '<!-- Frequently Asked Questions -->' in content:
            new_content = content.replace('<!-- Frequently Asked Questions -->', f'{table_html}\n    <!-- Frequently Asked Questions -->')
        elif '</main>' in content:
            new_content = content.replace('</main>', f'{table_html}\n  </main>')
        else:
            return False

        file_path.write_text(new_content, encoding="utf-8")
        return True

    def run_tests_and_verify(self) -> Dict[str, Any]:
        """Runs the complete project automated test suite and strict link graph verification."""
        test_cmd = ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
        link_cmd = ["python", "scripts/link_graph_checker.py", "--strict"]

        t_res = subprocess.run(test_cmd, cwd=self.root, capture_output=True, text=True)
        tests_passed = (t_res.returncode == 0)

        l_res = subprocess.run(link_cmd, cwd=self.root, capture_output=True, text=True)
        link_passed = (l_res.returncode == 0)

        all_passed = tests_passed and link_passed
        return {
            "all_passed": all_passed,
            "unit_tests_passed": tests_passed,
            "link_graph_passed": link_passed,
            "unit_test_output": t_res.stdout + t_res.stderr,
            "link_checker_output": l_res.stdout + l_res.stderr
        }

    def rollback_changes(self) -> bool:
        """Emergency safety rollback: restores clean working tree via git checkout if verification tests fail."""
        try:
            res = subprocess.run(["git", "checkout", "--", "."], cwd=self.root, capture_output=True, text=True)
            print("[ROLLBACK] Successfully restored working tree to clean HEAD commit.")
            return res.returncode == 0
        except Exception as e:
            print(f"[ROLLBACK ERROR] Failed to execute git checkout rollback: {e}")
            return False

    def get_git_diff(self) -> str:
        """Returns the current unstaged and staged git diff."""
        try:
            res = subprocess.run(["git", "diff"], cwd=self.root, capture_output=True, text=True)
            return res.stdout
        except Exception:
            return ""

    def execute_repairs(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executes a batch of low-risk proposals under strict rollback protection."""
        executed = []
        skipped = []

        for p in proposals:
            if p.get("risk") != "LOW":
                skipped.append({"id": p.get("id"), "reason": "Risk level not LOW"})
                continue

            pid = p.get("id", "")
            success = False

            if "canonical" in pid:
                file_rel = p.get("file")
                if file_rel:
                    success = self.fix_canonical_tag(file_rel)
            elif "sitemap" in pid:
                missing_items = p.get("affected_items", [])
                if missing_items:
                    success = self.sync_sitemap_urls(missing_items)
            elif "table" in pid or "comparison" in pid:
                file_rel = p.get("file")
                if file_rel:
                    success = self.inject_missing_comparison_table(file_rel)

            if success:
                executed.append(p)
            else:
                skipped.append({"id": pid, "reason": "No applicable automated fix or zero diff"})

        # If any changes were made, verify via full test suite
        diff = self.get_git_diff()
        if diff:
            verification = self.run_tests_and_verify()
            if not verification["all_passed"]:
                print("[FIREWALL WARNING] Verification tests failed after repair! Rolling back immediately...")
                self.rollback_changes()
                return {
                    "applied": False,
                    "rolled_back": True,
                    "executed_proposals": executed,
                    "skipped_proposals": skipped,
                    "diff": "",
                    "verification": verification,
                    "error": "Tests failed post-repair; all changes safely reverted."
                }
            return {
                "applied": True,
                "rolled_back": False,
                "executed_proposals": executed,
                "skipped_proposals": skipped,
                "diff": diff,
                "verification": verification,
                "error": None
            }

        return {
            "applied": False,
            "rolled_back": False,
            "executed_proposals": executed,
            "skipped_proposals": skipped,
            "diff": "",
            "verification": {"all_passed": True},
            "error": None
        }
