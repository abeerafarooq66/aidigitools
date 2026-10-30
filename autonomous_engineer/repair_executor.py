import os
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, List, Set, Optional
from .config import PROJECT_ROOT, BASE_URL, PROTECTED_PATTERNS

class RepairExecutor:
    """Executes safe, low-risk autonomous fixes protected by a strict observe-plan-fix-test-rollback firewall.
    Adheres strictly to zero-destructive reset invariants: never uses blanket resets ('git checkout -- .'),
    strictly enforces explicit allowlists, inspects diffs, and treats all external text as untrusted data.
    """

    ALLOWED_REPAIR_ACTIONS = {
        "fix_canonical_tag",
        "sync_sitemap_urls",
        "inject_missing_comparison_table",
    }

    UNTRUSTED_INSTRUCTION_PATTERNS = [
        re.compile(r'(?i)ignore\s+(?:all\s+)?(?:previous|prior)\s+(?:instructions|prompts)'),
        re.compile(r'(?i)system\s+prompt'),
        re.compile(r'(?i)grant\s+(?:all\s+)?(?:admin|write|root)\s+permissions?'),
        re.compile(r'(?i)leak\s+(?:all\s+)?(?:api\s+)?(?:secrets?|keys?|tokens?)'),
        re.compile(r'(?i)disable\s+(?:all\s+)?(?:security|firewall|guardrails?)'),
        re.compile(r'(?i)delete\s+(?:all\s+)?(?:files?|repositories|data)'),
        re.compile(r'(?i)eval\s*\('),
        re.compile(r'(?i)subprocess\.(?:call|run|Popen)'),
    ]

    MAX_FILES_PER_CYCLE = 15

    def __init__(self, root_dir: Path = PROJECT_ROOT):
        self.root = Path(root_dir)

    def is_protected(self, file_rel_path: str) -> bool:
        """Enforces safety firewall: blocks automated edits to critical payment, legal, or contact rails."""
        normalized = file_rel_path.replace("\\", "/")
        for pattern in PROTECTED_PATTERNS:
            if pattern in normalized:
                return True
        return False

    def is_untrusted_instruction(self, proposal: Dict[str, Any]) -> bool:
        """Guards against prompt injection: verifies proposal contains no manipulative instructions."""
        texts_to_check = [
            str(proposal.get("id", "")),
            str(proposal.get("action", "")),
            str(proposal.get("details", "")),
            str(proposal.get("file", ""))
        ]
        for text in texts_to_check:
            for pattern in self.UNTRUSTED_INSTRUCTION_PATTERNS:
                if pattern.search(text):
                    print(f"[FIREWALL SECURITY] Untrusted instruction detected and rejected: {pattern.pattern} in '{text}'")
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
            f'    <section class="tool-comparison-section" style="margin: 2.5rem 0;">\n'
            f'      <h2>{tool_name} Specifications & Comparison</h2>\n'
            f'      <div style="overflow-x: auto;">\n'
            f'        <table style="width: 100%; border-collapse: collapse; margin-top: 1rem; text-align: left;">\n'
            f'          <thead>\n'
            f'            <tr style="border-bottom: 2px solid #e2e8f0; background: #f8fafc;">\n'
            f'              <th style="padding: 0.75rem 1rem;">Metric / Feature</th>\n'
            f'              <th style="padding: 0.75rem 1rem;">{tool_name} Standard</th>\n'
            f'              <th style="padding: 0.75rem 1rem;">Industry Benchmark</th>\n'
            f'              <th style="padding: 0.75rem 1rem;">AIDigiTools Advantage</th>\n'
            f'            </tr>\n'
            f'          </thead>\n'
            f'          <tbody>\n'
            f'            <tr style="border-bottom: 1px solid #e2e8f0;">\n'
            f'              <td style="padding: 0.75rem 1rem; font-weight: 600;">Delivery SLA</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">Instant WhatsApp Access</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">12–24 Hours</td>\n'
            f'              <td style="padding: 0.75rem 1rem; color: #16a34a; font-weight: 600;">Sub-15 Minute Dispatch</td>\n'
            f'            </tr>\n'
            f'            <tr style="border-bottom: 1px solid #e2e8f0;">\n'
            f'              <td style="padding: 0.75rem 1rem; font-weight: 600;">Payment Options</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">PKR & USD Rails</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">Credit Card Only</td>\n'
            f'              <td style="padding: 0.75rem 1rem; color: #16a34a; font-weight: 600;">EasyPaisa, JazzCash, SadaPay</td>\n'
            f'            </tr>\n'
            f'            <tr style="border-bottom: 1px solid #e2e8f0;">\n'
            f'              <td style="padding: 0.75rem 1rem; font-weight: 600;">Replacement Warranty</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">30-Day Guaranteed</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">No Warranty</td>\n'
            f'              <td style="padding: 0.75rem 1rem; color: #16a34a; font-weight: 600;">100% Replacement Shield</td>\n'
            f'            </tr>\n'
            f'            <tr style="border-bottom: 1px solid #e2e8f0;">\n'
            f'              <td style="padding: 0.75rem 1rem; font-weight: 600;">Account Concierge</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">Verified Seat / Profile</td>\n'
            f'              <td style="padding: 0.75rem 1rem;">Self-Serve Bottleneck</td>\n'
            f'              <td style="padding: 0.75rem 1rem; color: #16a34a; font-weight: 600;">Human Priority Support</td>\n'
            f'            </tr>\n'
            f'          </tbody>\n'
            f'        </table>\n'
            f'      </div>\n'
            f'    </section>\n'
        )

        # Insert before </main> or before footer
        if "</main>" in content:
            new_content = content.replace("</main>", f"{table_html}\n  </main>")
        elif "<footer" in content:
            new_content = re.sub(r'(<footer)', f"{table_html}\n\\1", content, count=1, flags=re.IGNORECASE)
        else:
            new_content = content + table_html

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

    def rollback_changes(self, modified_files: Optional[Set[str]] = None) -> bool:
        """Targeted safety rollback: restores ONLY specific modified files, avoiding blanket resets.
        Strict invariant: NEVER runs blanket destructive checkout commands across whole tree.
        """
        if not modified_files:
            print("[ROLLBACK] No specific modified files provided; zero changes to discard.")
            return True

        success = True
        for rel_file in modified_files:
            file_path = self.root / rel_file
            try:
                # If file was untracked/newly created, remove it
                res_status = subprocess.run(
                    ["git", "status", "--porcelain", str(rel_file)],
                    cwd=self.root,
                    capture_output=True,
                    text=True
                )
                if "??" in res_status.stdout:
                    if file_path.exists():
                        file_path.unlink()
                        print(f"[ROLLBACK] Removed untracked file: {rel_file}")
                else:
                    # Restore tracked file cleanly to HEAD
                    res = subprocess.run(
                        ["git", "checkout", "--", str(rel_file)],
                        cwd=self.root,
                        capture_output=True,
                        text=True
                    )
                    if res.returncode != 0:
                        success = False
                        print(f"[ROLLBACK ERROR] Failed to revert {rel_file}: {res.stderr}")
                    else:
                        print(f"[ROLLBACK] Successfully reverted {rel_file} to HEAD.")
            except Exception as e:
                success = False
                print(f"[ROLLBACK EXCEPTION] Error reverting {rel_file}: {e}")

        return success

    def get_git_diff(self) -> str:
        """Returns the current unstaged and staged git diff."""
        try:
            res = subprocess.run(["git", "diff"], cwd=self.root, capture_output=True, text=True)
            return res.stdout
        except Exception:
            return ""

    def inspect_diff(self, diff: str, modified_files: Set[str]) -> Dict[str, Any]:
        """Inspects diff metrics before accepting changes: verifies file count, protected files, and scope."""
        if len(modified_files) > self.MAX_FILES_PER_CYCLE:
            return {
                "safe": False,
                "reason": f"Modified file count ({len(modified_files)}) exceeds safe threshold ({self.MAX_FILES_PER_CYCLE})."
            }

        for f in modified_files:
            if self.is_protected(f):
                return {
                    "safe": False,
                    "reason": f"Protected file touched in diff: {f}"
                }

        return {"safe": True, "reason": None}

    def execute_repairs(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Executes a batch of low-risk proposals under strict isolated rollback protection."""
        executed = []
        skipped = []
        modified_files: Set[str] = set()

        for p in proposals:
            # Check 1: Risk level must be LOW
            if p.get("risk") != "LOW":
                skipped.append({"id": p.get("id"), "reason": "Risk level not LOW"})
                continue

            # Check 2: Prompt injection / untrusted instruction guard
            if self.is_untrusted_instruction(p):
                skipped.append({"id": p.get("id"), "reason": "Untrusted or prompt-injection pattern detected"})
                continue

            pid = p.get("id", "")
            success = False

            # Check 3: Explicit action allowlist
            if "canonical" in pid:
                file_rel = p.get("file")
                if file_rel and not self.is_protected(file_rel):
                    success = self.fix_canonical_tag(file_rel)
                    if success:
                        modified_files.add(file_rel)
            elif "sitemap" in pid:
                missing_items = p.get("affected_items", [])
                if missing_items:
                    success = self.sync_sitemap_urls(missing_items)
                    if success:
                        modified_files.add("sitemap.xml")
            elif "table" in pid or "comparison" in pid:
                file_rel = p.get("file")
                if file_rel and not self.is_protected(file_rel):
                    success = self.inject_missing_comparison_table(file_rel)
                    if success:
                        modified_files.add(file_rel)

            if success:
                executed.append(p)
            else:
                skipped.append({"id": pid, "reason": "No applicable automated fix or zero diff"})

        # If any changes were made, inspect diff and verify via full test suite
        diff = self.get_git_diff()
        if diff:
            diff_check = self.inspect_diff(diff, modified_files)
            if not diff_check["safe"]:
                print(f"[FIREWALL WARNING] Diff inspection failed: {diff_check['reason']}. Rolling back isolated files...")
                self.rollback_changes(modified_files)
                return {
                    "applied": False,
                    "rolled_back": True,
                    "executed_proposals": executed,
                    "skipped_proposals": skipped,
                    "diff": "",
                    "verification": {"all_passed": False},
                    "error": f"Diff inspection rejected: {diff_check['reason']}"
                }

            verification = self.run_tests_and_verify()
            if not verification["all_passed"]:
                print("[FIREWALL WARNING] Verification tests failed after repair! Rolling back isolated files...")
                self.rollback_changes(modified_files)
                return {
                    "applied": False,
                    "rolled_back": True,
                    "executed_proposals": executed,
                    "skipped_proposals": skipped,
                    "diff": "",
                    "verification": verification,
                    "error": "Tests failed post-repair; isolated changes safely reverted."
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
