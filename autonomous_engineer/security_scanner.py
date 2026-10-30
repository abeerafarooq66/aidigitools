import os
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import PROJECT_ROOT, BASE_URL, PROTECTED_PATTERNS

class SecurityScanner:
    """Enterprise-grade security and vulnerability scanner for AIDigiTools.
    Detects exposed secrets, vulnerable dependencies, suspicious scripts,
    unsafe redirects, security headers, and risky workflow permissions.
    """

    SECRET_PATTERNS = {
        "google_api_key": re.compile(r'\bAIza[0-9A-Za-z-_]{35}\b'),
        "github_pat": re.compile(r'\b(?:ghp|gho|ghu|ghs|ghr)_[0-9a-zA-Z]{36}\b'),
        "github_fine_grained_pat": re.compile(r'\bgithub_pat_[0-9a-zA-Z_]{82}\b'),
        "private_key": re.compile(r'-----BEGIN (?:RSA|OPENSSH|EC|DSA|PGP|PRIVATE) KEY-----'),
        "hardcoded_assignment": re.compile(
            r'(?i)\b(?:api_key|secret_key|private_key|auth_token)\s*=\s*["\'][a-zA-Z0-9_\-]{20,}["\']'
        ),
        "slack_webhook": re.compile(r'https://hooks\.slack\.com/services/T[0-9A-Z]+/B[0-9A-Z]+/[0-9a-zA-Z]+'),
        "telegram_token": re.compile(r'\b\d{9,10}:[a-zA-Z0-9_-]{35}\b')
    }

    SUSPICIOUS_SCRIPT_PATTERNS = [
        (re.compile(r'\beval\s*\('), "eval() invocation detected"),
        (re.compile(r'\bdocument\.write\s*\('), "document.write() invocation detected"),
        (re.compile(r'window\.location\.replace\s*\(\s*["\']http:'), "Unencrypted HTTP redirect"),
        (re.compile(r'String\.fromCharCode\s*\('), "Obfuscated string construction"),
    ]

    PROMPT_INJECTION_PATTERNS = [
        re.compile(r'(?i)ignore\s+(?:all\s+)?(?:previous|prior)\s+(?:instructions|prompts)'),
        re.compile(r'(?i)system\s+prompt\s+override'),
        re.compile(r'(?i)grant\s+(?:all\s+)?(?:admin|write|root)\s+permissions?'),
        re.compile(r'(?i)leak\s+(?:all\s+)?(?:secrets?|keys?|tokens?)'),
        re.compile(r'(?i)disable\s+(?:all\s+)?(?:security|firewall|guardrails?)'),
        re.compile(r'(?i)delete\s+(?:all\s+)?(?:files?|repositories|data)'),
    ]

    TRUSTED_SCRIPT_DOMAINS = [
        "https://aidigitools.tech",
        "https://www.googletagmanager.com",
        "https://www.google-analytics.com",
        "https://cdnjs.cloudflare.com",
        "https://cdn.jsdelivr.net",
        "https://unpkg.com"
    ]

    def __init__(self, root_dir: Path = PROJECT_ROOT):
        self.root = Path(root_dir)

    def scan_exposed_secrets(self, target_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Scans codebase for accidentally committed API keys, tokens, and private keys."""
        scan_dir = target_dir or self.root
        findings = []

        # Directories and files to exclude from secret scan
        exclude_dirs = {".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv", ".idea", "tests"}
        exclude_exts = {".png", ".jpg", ".jpeg", ".webp", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot"}

        for root, dirs, files in os.walk(scan_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.endswith("_tests") and not d == "tests"]
            # Skip if current root is inside a test directory
            path_parts = Path(root).parts
            if any(p in exclude_dirs for p in path_parts):
                continue
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in exclude_exts:
                    continue
                # Skip the security scanner itself and tests to avoid self-flagging test signatures
                try:
                    rel_str = str(file_path.relative_to(self.root)).replace("\\", "/")
                except ValueError:
                    rel_str = str(file_path.name)
                if rel_str in ("autonomous_engineer/security_scanner.py", "tests/test_security_remediation.py"):
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue

                for pattern_name, pattern in self.SECRET_PATTERNS.items():
                    matches = pattern.finditer(content)
                    for m in matches:
                        match_text = m.group(0)
                        # Filter out common false positives (e.g., standard placeholders or environment lookup calls)
                        if "os.environ" in match_text or "process.env" in match_text or "placeholder" in match_text.lower():
                            continue
                        if match_text.startswith("ghp_") and "000000" in match_text:
                            continue
                        # Redact the secret in finding report
                        redacted = match_text[:4] + "..." + match_text[-4:] if len(match_text) > 8 else "***"
                        findings.append({
                            "type": "exposed_secret",
                            "severity": "CRITICAL",
                            "pattern": pattern_name,
                            "file": rel_str,
                            "snippet": redacted,
                            "recommendation": "Revoke secret immediately, purge from git history, and migrate to GitHub Secrets."
                        })

        return findings

    def scan_workflow_permissions(self) -> List[Dict[str, Any]]:
        """Audits GitHub Actions workflows for least-privilege permissions and insecure patterns."""
        findings = []
        workflow_dir = self.root / ".github" / "workflows"
        if not workflow_dir.exists():
            return findings

        for wf in workflow_dir.glob("*.yml"):
            rel_str = str(wf.relative_to(self.root)).replace("\\", "/")
            try:
                content = wf.read_text(encoding="utf-8")
            except Exception:
                continue

            # Check 1: Top-level or job-level permissions
            has_permissions = bool(re.search(r"permissions:\s*(?:[^\n]+|(?:\n\s+[\w\-]+:\s*\w+)+)", content))
            if not has_permissions:
                findings.append({
                    "type": "missing_workflow_permissions",
                    "severity": "HIGH",
                    "file": rel_str,
                    "details": "Workflow lacks explicit permissions block; defaults may allow write access.",
                    "recommendation": "Add explicit top-level 'permissions: contents: read'."
                })

            # Check 2: Risky pull_request_target with checkout
            if "pull_request_target" in content:
                if re.search(r"ref:\s*[\'\"]?\${{\s*github\.event\.pull_request\.head\.sha", content):
                    findings.append({
                        "type": "risky_pull_request_target",
                        "severity": "CRITICAL",
                        "file": rel_str,
                        "details": "Workflow uses pull_request_target while checking out untrusted PR head commit.",
                        "recommendation": "Use pull_request instead or avoid checking out head commit with elevated token."
                    })

            # Check 3: Insecure secret printing / echo
            if re.search(r"echo\s+.*(?:secrets\.|API_KEY|TOKEN)", content, re.IGNORECASE):
                findings.append({
                    "type": "insecure_secret_logging",
                    "severity": "CRITICAL",
                    "file": rel_str,
                    "details": "Workflow contains echo statement referencing secrets or API tokens.",
                    "recommendation": "Remove echo of sensitive secrets in CI scripts."
                })

        return findings

    def scan_suspicious_scripts_and_redirects(self) -> List[Dict[str, Any]]:
        """Audits HTML and JS files for risky JS patterns and untrusted external scripts."""
        findings = []
        html_files = list(self.root.glob("*.html")) + list((self.root / "tools").glob("*.html")) + list((self.root / "categories").glob("*.html"))

        for f in html_files:
            rel_str = str(f.relative_to(self.root)).replace("\\", "/")
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            # 1. Check for suspicious scripts
            for pattern, desc in self.SUSPICIOUS_SCRIPT_PATTERNS:
                if pattern.search(content):
                    findings.append({
                        "type": "suspicious_script_pattern",
                        "severity": "MEDIUM",
                        "file": rel_str,
                        "details": desc,
                        "recommendation": "Avoid dynamic code execution and unencrypted redirects."
                    })

            # 2. Check external script tags
            script_srcs = re.findall(r'<script[^>]*\bsrc=["\']([^"\']+)["\']', content, re.IGNORECASE)
            for src in script_srcs:
                if src.startswith("http://") or src.startswith("https://"):
                    is_trusted = any(src.startswith(td) for td in self.TRUSTED_SCRIPT_DOMAINS)
                    if not is_trusted:
                        findings.append({
                            "type": "untrusted_external_script",
                            "severity": "HIGH",
                            "file": rel_str,
                            "details": f"External script from untrusted domain: {src}",
                            "recommendation": "Host scripts locally or only use verified trusted CDNs."
                        })

            # 3. Check external link security (target="_blank" without rel="noopener noreferrer")
            unsafe_links = re.findall(
                r'<a[^>]*target=["\']_blank["\'](?![^>]*rel=["\'][^"\']*(?:noopener|noreferrer)[^"\']*["\'])[^>]*>',
                content,
                re.IGNORECASE
            )
            if unsafe_links:
                findings.append({
                    "type": "unsafe_target_blank",
                    "severity": "LOW",
                    "file": rel_str,
                    "details": f"Found {len(unsafe_links)} target='_blank' links missing rel='noopener noreferrer'.",
                    "recommendation": "Add rel='noopener noreferrer' to all target='_blank' anchors."
                })

        return findings

    def scan_security_headers(self, live_url: str = BASE_URL) -> Dict[str, Any]:
        """Probes live domain for key HTTP security headers."""
        results = {
            "Content-Security-Policy": {"present": False, "value": None},
            "X-Content-Type-Options": {"present": False, "value": None},
            "X-Frame-Options": {"present": False, "value": None},
            "Strict-Transport-Security": {"present": False, "value": None},
            "Referrer-Policy": {"present": False, "value": None},
            "Permissions-Policy": {"present": False, "value": None}
        }
        try:
            req = urllib.request.Request(live_url, headers={"User-Agent": "AIDigiTools-Security-Audit/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                headers = {k.lower(): v for k, v in resp.headers.items()}
                for sec_header in results.keys():
                    lh = sec_header.lower()
                    if lh in headers:
                        results[sec_header]["present"] = True
                        results[sec_header]["value"] = headers[lh]
        except Exception as e:
            results["error"] = str(e)

        return results

    def is_untrusted_input(self, text: str) -> bool:
        """Evaluates whether arbitrary text contains prompt injection or manipulative instructions."""
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            if pattern.search(text):
                return True
        return False

    def sanitize_untrusted_content(self, text: str) -> str:
        """Neutralizes prompt injection keywords from untrusted strings before parsing."""
        sanitized = text
        for pattern in self.PROMPT_INJECTION_PATTERNS:
            sanitized = pattern.sub("[REDACTED_INJECTION_ATTEMPT]", sanitized)
        return sanitized

    def verify_supply_chain_security(self) -> Dict[str, Any]:
        """Verifies Dependabot and package configuration."""
        dependabot_path = self.root / ".github" / "dependabot.yml"
        codeql_path = self.root / ".github" / "workflows" / "codeql.yml"

        has_dependabot = dependabot_path.exists()
        has_codeql = codeql_path.exists()

        pip_status = "clean"
        try:
            res = subprocess.run(["pip", "check"], capture_output=True, text=True)
            if res.returncode != 0:
                pip_status = f"warning: {res.stdout.strip()}"
        except Exception as e:
            pip_status = f"skipped: {e}"

        return {
            "dependabot_configured": has_dependabot,
            "codeql_configured": has_codeql,
            "pip_check_status": pip_status
        }

    def run_full_security_audit(self) -> Dict[str, Any]:
        """Executes the full suite of security audits and outputs structured diagnostics."""
        secrets = self.scan_exposed_secrets()
        workflows = self.scan_workflow_permissions()
        scripts = self.scan_suspicious_scripts_and_redirects()
        supply_chain = self.verify_supply_chain_security()
        headers = self.scan_security_headers()

        critical_count = sum(1 for f in secrets + workflows + scripts if f.get("severity") == "CRITICAL")
        high_count = sum(1 for f in secrets + workflows + scripts if f.get("severity") == "HIGH")
        medium_count = sum(1 for f in secrets + workflows + scripts if f.get("severity") == "MEDIUM")
        low_count = sum(1 for f in secrets + workflows + scripts if f.get("severity") == "LOW")

        is_secure = (critical_count == 0 and high_count == 0)

        return {
            "is_secure": is_secure,
            "critical_count": critical_count,
            "high_count": high_count,
            "medium_count": medium_count,
            "low_count": low_count,
            "exposed_secrets": secrets,
            "workflow_permission_issues": workflows,
            "script_and_redirect_issues": scripts,
            "supply_chain_security": supply_chain,
            "live_security_headers": headers
        }
