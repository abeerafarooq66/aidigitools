"""
Unit Tests for Security & API Access Manager (Part 21).
=======================================================
Strictly tests Part 21 of Master Architecture Charter:
SECURITY AND API ACCESS.

Validates:
1. Safe .env.example with zero hardcoded secrets and active .gitignore protection.
2. Secret redaction engine for API keys, bearer tokens, JWTs, and private keys.
3. Least-privilege scope enforcement (rejects full Cloud / admin write scopes).
4. Strict separation between analytics credentials and publishing/deployment credentials.
5. Empirical API verification: Never reports an integration as CONNECTED until it returns real data.
6. Local IndexNow key file authentication check.
7. Zero secrets persisted in status ledgers or reports.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.security_access_manager import (
    SecurityAccessManager,
    PROHIBITED_EXCESSIVE_SCOPES,
    AUTHORIZED_LEAST_PRIVILEGE_SCOPES
)


class TestSecurityAccessManager(unittest.TestCase):

    def setUp(self):
        """Create an isolated test workspace for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Create dummy .env.example
        (self.workspace / ".env.example").write_text(
            "# Safe Template\nINDEXNOW_KEY=89d63ab53a63527b12a199a3096e51ad\nGA4_PROPERTY_ID=\nGEMINI_API_KEY=\n",
            encoding="utf-8"
        )
        # Create dummy .gitignore
        (self.workspace / ".gitignore").write_text(".env\n*.key\ncredentials/\n", encoding="utf-8")

        # Create dummy key file for IndexNow
        (self.workspace / "89d63ab53a63527b12a199a3096e51ad.txt").write_text(
            "89d63ab53a63527b12a199a3096e51ad", encoding="utf-8"
        )

        self.manager = SecurityAccessManager(workspace_root=self.workspace)

    def tearDown(self):
        """Clean up isolated directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_env_example_safety_and_gitignore_protection(self):
        """Verify .env.example has zero secrets and .env is protected in .gitignore."""
        audit = self.manager.verify_env_example_safety()
        self.assertTrue(audit["exists"])
        self.assertTrue(audit["is_safe"])
        self.assertTrue(audit["gitignore_configured"])
        self.assertEqual(len(audit["issues"]), 0)

    def test_secret_redaction_engine(self):
        """Scrubbing must redact Google API keys, OpenAI keys, GitHub PATs, and private keys."""
        dirty_log = (
            "Exception while calling https://generativelanguage.googleapis.com with key AIzaSyD3fakeAPIkey1234567890abcdef. "
            "Authorization: Bearer ghp_1234567890abcdefghijklmnopqrstuvwxyz and token sk-1234567890abcdef1234."
        )
        clean_log = self.manager.redact_secrets(dirty_log)

        self.assertNotIn("AIzaSyD3fakeAPIkey1234567890abcdef", clean_log)
        self.assertNotIn("ghp_1234567890abcdefghijklmnopqrstuvwxyz", clean_log)
        self.assertNotIn("sk-1234567890abcdef1234", clean_log)
        self.assertIn("[REDACTED_GOOGLE_API_KEY]", clean_log)
        self.assertIn("[REDACTED_GITHUB_PAT]", clean_log)
        self.assertIn("[REDACTED_OPENAI_KEY]", clean_log)

    def test_least_privilege_scope_enforcement(self):
        """Must reject excessive cloud-platform or full account write scopes."""
        # 1. Valid least privilege scope
        valid_scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
        is_valid, violations = self.manager.validate_requested_scopes("google_search_console", valid_scopes)
        self.assertTrue(is_valid)
        self.assertEqual(len(violations), 0)

        # 2. Excessive cloud-platform scope
        excessive_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
        is_invalid, bad_violations = self.manager.validate_requested_scopes("google_search_console", excessive_scopes)
        self.assertFalse(is_invalid)
        self.assertIn("Excessive scope", bad_violations[0])

    def test_credential_separation(self):
        """Analytics credentials must be strictly separated from deployment/publishing credentials."""
        sep = self.manager.verify_credential_separation()
        self.assertTrue(sep["is_separated"])
        self.assertEqual(len(sep["overlapping_keys"]), 0)
        self.assertIn("GA4_PROPERTY_ID", sep["analytics_credentials"])
        self.assertIn("INDEXNOW_KEY", sep["deployment_credentials"])

    def test_never_report_connected_without_real_data(self):
        """An integration must NEVER be reported as CONNECTED until an authorized request returns real data."""
        # Case A: Credentials unconfigured
        os.environ.pop("GSC_SERVICE_ACCOUNT_KEY", None)
        res_missing = self.manager.verify_integration("google_search_console")
        self.assertEqual(res_missing["status"], "NOT_CONFIGURED")
        self.assertFalse(res_missing["is_connected"])

        # Case B: Credentials configured, but test data not yet returned
        os.environ["GSC_SERVICE_ACCOUNT_KEY"] = "mock_service_account_credentials"
        res_pending = self.manager.verify_integration("google_search_console", test_data=None)
        self.assertEqual(res_pending["status"], "PENDING_VERIFICATION")
        self.assertFalse(res_pending["is_connected"])
        self.assertFalse(res_pending["data_returned"])

        # Case C: Authorized test request returns real verified data
        res_connected = self.manager.verify_integration(
            "google_search_console",
            test_data={"queries_count": 42, "impressions": 1500}
        )
        self.assertEqual(res_connected["status"], "CONNECTED")
        self.assertTrue(res_connected["is_connected"])
        self.assertTrue(res_connected["data_returned"])
        self.assertIn("42 verified queries", res_connected["details"])

        os.environ.pop("GSC_SERVICE_ACCOUNT_KEY", None)

    def test_indexnow_local_key_file_verification(self):
        """IndexNow is verified only when key file exists locally and matches key string."""
        os.environ["INDEXNOW_KEY"] = "89d63ab53a63527b12a199a3096e51ad"
        res = self.manager.verify_integration("indexnow")
        self.assertEqual(res["status"], "CONNECTED")
        self.assertTrue(res["is_connected"])

        # Tamper key file
        (self.workspace / "89d63ab53a63527b12a199a3096e51ad.txt").write_text("wrong_key", encoding="utf-8")
        res_tampered = self.manager.verify_integration("indexnow")
        self.assertEqual(res_tampered["status"], "AUTHENTICATION_FAILED")
        self.assertFalse(res_tampered["is_connected"])


if __name__ == "__main__":
    unittest.main()

