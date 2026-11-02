"""
Unit Tests for Publishing Control Engine (Part 20).
===================================================
Strictly tests Part 20 of Master Architecture Charter:
PUBLISHING CONTROL.

Validates:
1. Phase 1 Supervised Mode: First 3 articles require preview and explicit human approval.
2. Phase 1 -> Phase 2 transition after 3 successful human-approved cycles.
3. Phase 2 Autonomous Mode: Low-risk compliant content is approved for auto-publication.
4. Persistent High-Risk Triggers requiring human approval even in Phase 2:
   - Unverified product/supplier status
   - Authorization and licensing claims
   - Product access model changes
   - Material pricing claims that cannot be verified
   - Warranty or legal policy changes
   - Sensitive commercial promises
   - Uncertain factual claims
5. Critical Invariant: Never bypass a failed quality gate to meet a publishing target.
6. Human rejection workflow with reviewer feedback.
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

from agent.publishing_control import (
    PublishingControlEngine,
    QualityGateBypassProhibitedError,
    PHASE_1_SUPERVISED,
    PHASE_2_AUTONOMOUS_LOW_RISK
)


class TestPublishingControl(unittest.TestCase):

    def setUp(self):
        """Create an isolated test workspace for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.engine = PublishingControlEngine(workspace_root=self.workspace)

        # Compliant baseline content
        self.sample_html = """<!DOCTYPE html>
<html>
<head><title>Cursor vs Copilot</title></head>
<body>
  <h1>Cursor vs Copilot Comparison</h1>
  <p class="quick-answer">Cursor Pro costs Rs. 3,800 while Copilot costs Rs. 2,900 on AIDigiTools.</p>
</body>
</html>"""

        self.sample_meta = {
            "slug": "cursor-vs-copilot",
            "title": "Cursor vs Copilot",
            "primary_keyword": "cursor vs copilot",
            "cluster_slug": "ai-coding-and-development"
        }

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_phase_1_supervised_mode_halts_for_human_approval(self):
        """In Phase 1, article previews must be held for explicit human approval."""
        status = self.engine.get_operational_status()
        self.assertEqual(status["current_phase"], PHASE_1_SUPERVISED)
        self.assertEqual(status["approved_supervised_publications_count"], 0)

        preview = self.engine.prepare_article_preview(
            slug=self.sample_meta["slug"],
            title=self.sample_meta["title"],
            html_content=self.sample_html,
            metadata=self.sample_meta
        )

        self.assertTrue(preview["approval_required"])
        self.assertEqual(preview["decision"], "HELD_FOR_HUMAN_APPROVAL")
        self.assertTrue((self.workspace / preview["preview_path"]).exists())
        self.assertEqual(preview["status"], "PENDING")

        # Verify ledger persistence
        st = self.engine.get_operational_status()
        self.assertEqual(st["pending_previews_count"], 1)

    def test_phase_1_approval_workflow_and_phase_2_unlock(self):
        """Approving 3 supervised cycles must automatically unlock Phase 2 Autonomous Mode."""
        for i in range(1, 4):
            slug = f"article-{i}"
            prev = self.engine.prepare_article_preview(
                slug=slug,
                title=f"Article {i}",
                html_content=self.sample_html,
                metadata={"slug": slug}
            )
            app_res = self.engine.human_approve_preview(
                preview_id_or_slug=prev["preview_id"],
                reviewer_name="Abeera Farooq",
                reviewer_notes=f"Approved article {i}."
            )
            self.assertEqual(app_res["status"], "APPROVED_BY_HUMAN")
            self.assertEqual(app_res["approved_supervised_count"], i)

        # After 3 approvals, Phase 2 must be unlocked!
        status_after = self.engine.get_operational_status()
        self.assertEqual(status_after["current_phase"], PHASE_2_AUTONOMOUS_LOW_RISK)
        self.assertTrue(status_after["phase_2_unlocked"])
        self.assertEqual(status_after["approved_supervised_publications_count"], 3)

    def test_phase_2_autonomous_publication_for_low_risk_content(self):
        """In Phase 2, low-risk content passing all checks must be approved for auto-publication."""
        # Force ledger into Phase 2
        with open(self.engine.control_ledger_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["approved_supervised_publications_count"] = 3
        data["current_phase"] = PHASE_2_AUTONOMOUS_LOW_RISK
        with open(self.engine.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        preview = self.engine.prepare_article_preview(
            slug="low-risk-article",
            title="Low Risk Article",
            html_content=self.sample_html,
            metadata={"slug": "low-risk-article"},
            quality_gate_report={"decision": "APPROVED", "failed_gates_count": 0}
        )

        self.assertFalse(preview["approval_required"])
        self.assertEqual(preview["decision"], "APPROVED_FOR_AUTO_PUBLICATION")
        self.assertEqual(preview["status"], "READY_TO_PUBLISH")

    def test_persistent_high_risk_trigger_unverified_product_supplier(self):
        """Content touching unverified products/suppliers must require human approval even in Phase 2."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>Sourced from an unverified product and gray market broker.</p>"
        prev = self.engine.prepare_article_preview("test-sup", "Title", tampered_html, {"slug": "test-sup"})
        self.assertTrue(prev["approval_required"])
        self.assertEqual(prev["decision"], "HELD_FOR_HUMAN_APPROVAL")
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("unverified_product_supplier_status", categories)

    def test_persistent_high_risk_trigger_authorization_licensing(self):
        """Content claiming official partnership must require human approval even in Phase 2."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>We are an official partner of OpenAI and authorized licensee.</p>"
        prev = self.engine.prepare_article_preview("test-auth", "Title", tampered_html, {"slug": "test-auth"})
        self.assertTrue(prev["approval_required"])
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("authorization_and_licensing_claims", categories)

    def test_persistent_high_risk_trigger_product_access_model(self):
        """Content mentioning shared slot or profile PIN must require human approval even in Phase 2."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>Delivered via shared slot with profile PIN access.</p>"
        prev = self.engine.prepare_article_preview("test-pin", "Title", tampered_html, {"slug": "test-pin"})
        self.assertTrue(prev["approval_required"])
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("product_access_model_changes", categories)

    def test_persistent_high_risk_trigger_unverified_pricing(self):
        """Content mentioning unverified price or secret rate must require human approval even in Phase 2."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>Special secret rate with unverified price discount.</p>"
        prev = self.engine.prepare_article_preview("test-prc", "Title", tampered_html, {"slug": "test-prc"})
        self.assertTrue(prev["approval_required"])
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("unverified_material_pricing", categories)

    def test_persistent_high_risk_trigger_warranty_or_legal_policy(self):
        """Promises of full cash refund or DMCA immunity must require human approval even in Phase 2."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>Comes with 100% money-back guarantee and full cash refund.</p>"
        prev = self.engine.prepare_article_preview("test-war", "Title", tampered_html, {"slug": "test-war"})
        self.assertTrue(prev["approval_required"])
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("warranty_or_legal_policy_changes", categories)

    def test_persistent_high_risk_trigger_sensitive_commercial_promises(self):
        """Promises of guaranteed fastest delivery or guaranteed ranking must require human approval."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>Features guaranteed fastest delivery and zero risk guarantee.</p>"
        prev = self.engine.prepare_article_preview("test-com", "Title", tampered_html, {"slug": "test-com"})
        self.assertTrue(prev["approval_required"])
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("sensitive_commercial_promises", categories)

    def test_persistent_high_risk_trigger_uncertain_factual_claims(self):
        """Unverified benchmarks or hardware claims must require human approval even in Phase 2."""
        self._unlock_phase_2()
        tampered_html = self.sample_html + "<p>In our private benchmark tested on 5000 users across a cluster of 64 GPUs.</p>"
        prev = self.engine.prepare_article_preview("test-fac", "Title", tampered_html, {"slug": "test-fac"})
        self.assertTrue(prev["approval_required"])
        categories = [t["category"] for t in prev["high_risk_triggers"]]
        self.assertIn("uncertain_factual_claims", categories)

    def test_quality_gate_bypass_strictly_prohibited(self):
        """Never bypass a failed quality gate to meet a publishing target."""
        self._unlock_phase_2()
        failed_gate_report = {
            "decision": "DO NOT PUBLISH",
            "failed_gates_count": 2,
            "critical_failures": ["GATE_11_ACCURATE_CTAS", "GATE_19_SECURITY_AND_ZERO_LEAK"]
        }
        with self.assertRaises(QualityGateBypassProhibitedError) as ctx:
            self.engine.prepare_article_preview(
                slug="failing-article",
                title="Failing Article",
                html_content=self.sample_html,
                metadata={"slug": "failing-article"},
                quality_gate_report=failed_gate_report
            )
        self.assertIn("Never bypass a failed quality gate", str(ctx.exception))

    def test_human_rejection_workflow(self):
        """Rejections must move preview to rejected history with documented feedback."""
        prev = self.engine.prepare_article_preview("test-rej", "Reject Me", self.sample_html, {"slug": "test-rej"})
        rej_res = self.engine.human_reject_preview(
            preview_id_or_slug=prev["preview_id"],
            reviewer_name="Abeera Farooq",
            rejection_reason="Needs localized PKR pricing table."
        )

        self.assertEqual(rej_res["status"], "REJECTED_BY_HUMAN")
        self.assertEqual(rej_res["rejection_reason"], "Needs localized PKR pricing table.")

        with open(self.engine.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        self.assertEqual(len(ledger["pending_previews"]), 0)
        self.assertEqual(len(ledger["rejected_history"]), 1)

    def _unlock_phase_2(self):
        """Helper to set ledger state to Phase 2."""
        with open(self.engine.control_ledger_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["approved_supervised_publications_count"] = 3
        data["current_phase"] = PHASE_2_AUTONOMOUS_LOW_RISK
        with open(self.engine.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    unittest.main()

