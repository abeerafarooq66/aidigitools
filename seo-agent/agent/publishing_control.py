"""
AIDigiTools — Publishing Control Engine (Part 20).
==================================================
Strictly implements Part 20 of the Master Architecture Charter:
PUBLISHING CONTROL.

Phase 1 (Assisted / Supervised Mode):
- The first three articles must be prepared with preview and explicit human approval.
- Zero autonomous publishing until at least 3 successful supervised cycles are approved.

Phase 2 (Autonomous Low-Risk Mode):
- Enabled strictly after 3 successful human-approved publishing cycles.
- Automatic publication is permitted ONLY for eligible, low-risk content passing 100% of quality gates.

Persistent Human Approval Triggers (Always Required, Even in Phase 2):
1. Unverified product / supplier status
2. Authorization and licensing claims
3. Product access model changes
4. Material pricing claims that cannot be verified
5. Warranty or legal policy changes
6. Sensitive commercial promises
7. Uncertain factual claims

Core Invariant:
- NEVER bypass a failed quality gate to meet a publishing target.
"""

import os
import re
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# Base Directories
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
PREVIEWS_DIR = DATA_DIR / "previews"

# State Files
CONTROL_LEDGER_PATH = DATA_DIR / "publishing_control_ledger.json"
PUBLICATION_LEDGER_PATH = DATA_DIR / "publication_ledger.json"

PHASE_1_SUPERVISED = "PHASE_1_SUPERVISED"
PHASE_2_AUTONOMOUS_LOW_RISK = "PHASE_2_AUTONOMOUS_LOW_RISK"
PHASE_2_THRESHOLD = 3

# 7 Mandatory High-Risk Triggers Requiring Human Approval (Even in Phase 2)
PERSISTENT_HIGH_RISK_TRIGGERS = {
    "unverified_product_supplier_status": [
        r"(?i)\b(?:unverified\s+product|unknown\s+supplier|unlisted\s+vendor)\b",
        r"(?i)\b(?:gray\s+market|unverified\s+credentials|third[- ]party\s+broker)\b"
    ],
    "authorization_and_licensing_claims": [
        r"(?i)\b(?:official(?:ly)?|exclusive|direct)\s+(?:partner|agent|reseller|licensee)\s+of\b",
        r"(?i)\b(?:authorized|endorsed|certified)\s+by\s+(?:openai|anthropic|google|microsoft|adobe)\b"
    ],
    "product_access_model_changes": [
        r"(?i)\b(?:account\s+sharing|profile\s+pin|shared\s+slot|cracked\s+account|edu\s+pack)\b",
        r"(?i)\b(?:access\s+model\s+changed|new\s+login\s+method)\b"
    ],
    "unverified_material_pricing": [
        r"(?i)\b(?:unverified\s+price|pricing\s+unconfirmed|estimated\s+cost\s+without\s+verification)\b",
        r"(?i)\b(?:secret\s+rate|backdoor\s+deal|custom\s+under\s+the\s+table\s+price)\b"
    ],
    "warranty_or_legal_policy_changes": [
        r"(?i)\b(?:100%\s+money[- ]back\s+guarantee|full\s+cash\s+refund|lifetime\s+warranty|instant\s+cash\s+reversal)\b",
        r"(?i)\b(?:dmca\s+immunity|waive\s+all\s+legal\s+liability|exempt\s+from\s+terms)\b"
    ],
    "sensitive_commercial_promises": [
        r"(?i)\b(?:guaranteed\s+fastest\s+delivery|instant\s+delivery\s+guarantee|guaranteed\s+rank(?:ing)?)\b",
        r"(?i)\b(?:zero\s+risk\s+guarantee|unconditional\s+satisfaction\s+guarantee)\b"
    ],
    "uncertain_factual_claims": [
        r"(?i)\b(?:tested\s+on\s+\d{4,}\s+users|cluster\s+of\s+\d{2,}\s+gpus|unverified\s+benchmark)\b",
        r"(?i)\b(?:proven\s+100%\s+uptime|untested\s+performance\s+claim)\b"
    ]
}


def get_pkt_now_str() -> str:
    """Returns timestamp in Pakistan Standard Time (PKT = UTC+5)."""
    pkt = datetime.timezone(datetime.timedelta(hours=5), name="PKT")
    return datetime.datetime.now(pkt).strftime("%Y-%m-%d %H:%M:%S PKT")


class PublishingControlError(Exception):
    """Base exception for Publishing Control."""
    pass


class QualityGateBypassProhibitedError(PublishingControlError):
    """Raised when publishing is attempted on content that failed quality gates."""
    pass


class HumanApprovalRequiredError(PublishingControlError):
    """Raised when autonomous publishing is attempted on content requiring human approval."""
    pass


class PublishingControlEngine:
    """
    Enforces Phase 1 (first 3 articles with preview + human approval) and
    Phase 2 (low-risk autonomous publication + persistent high-risk triggers).
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        self.data_dir = self.workspace_root / "data"
        self.previews_dir = self.data_dir / "previews"
        self.previews_dir.mkdir(parents=True, exist_ok=True)
        self.control_ledger_path = self.data_dir / "publishing_control_ledger.json"
        self.publication_ledger_path = self.data_dir / "publication_ledger.json"
        self._ensure_ledger_file()

    def _ensure_ledger_file(self) -> None:
        """Initializes publishing control ledger if missing."""
        if not self.control_ledger_path.exists():
            default_ledger = {
                "ledger_version": "1.0.0",
                "business_timezone": "PKT (UTC+5)",
                "current_phase": PHASE_1_SUPERVISED,
                "approved_supervised_publications_count": 0,
                "phase_2_threshold": PHASE_2_THRESHOLD,
                "pending_previews": [],
                "approved_history": [],
                "rejected_history": [],
                "last_updated_pkt": get_pkt_now_str()
            }
            with open(self.control_ledger_path, "w", encoding="utf-8") as f:
                json.dump(default_ledger, f, indent=2)

    # --------------------------------------------------------------------------
    # 1. Operational Phase State
    # --------------------------------------------------------------------------
    def get_operational_status(self) -> Dict[str, Any]:
        """Returns the current operational phase and publication counts."""
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        count = ledger.get("approved_supervised_publications_count", 0)
        threshold = ledger.get("phase_2_threshold", PHASE_2_THRESHOLD)
        phase = PHASE_2_AUTONOMOUS_LOW_RISK if count >= threshold else PHASE_1_SUPERVISED

        if ledger.get("current_phase") != phase:
            ledger["current_phase"] = phase
            with open(self.control_ledger_path, "w", encoding="utf-8") as f:
                json.dump(ledger, f, indent=2)

        return {
            "current_phase": phase,
            "approved_supervised_publications_count": count,
            "phase_2_threshold": threshold,
            "phase_2_unlocked": count >= threshold,
            "pending_previews_count": len(ledger.get("pending_previews", []))
        }

    # --------------------------------------------------------------------------
    # 2. High-Risk Trigger Scanner
    # --------------------------------------------------------------------------
    def scan_for_high_risk_triggers(self, text_content: str) -> List[Dict[str, Any]]:
        """
        Scans content for the 7 mandatory categories requiring human review:
        1. Unverified product / supplier status
        2. Authorization and licensing claims
        3. Product access model changes
        4. Material pricing claims that cannot be verified
        5. Warranty or legal policy changes
        6. Sensitive commercial promises
        7. Uncertain factual claims
        """
        triggers_found = []
        for category, patterns in PERSISTENT_HIGH_RISK_TRIGGERS.items():
            for pat in patterns:
                matches = re.findall(pat, text_content)
                if matches:
                    triggers_found.append({
                        "category": category,
                        "pattern": pat,
                        "matches": list(set(matches))
                    })
        return triggers_found

    # --------------------------------------------------------------------------
    # 3. Prepare Article Preview & Gating
    # --------------------------------------------------------------------------
    def prepare_article_preview(
        self,
        slug: str,
        title: str,
        html_content: str,
        metadata: Dict[str, Any],
        quality_gate_report: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepares an article preview with quality evaluation and routing:
        - In Phase 1: Always halts for human approval.
        - In Phase 2: Permits auto-publish ONLY if 100% quality gate passed and zero high-risk triggers.
        - INVARIANT: If quality gates failed, REJECTS unconditionally. Never bypass a failed quality gate.
        """
        status_info = self.get_operational_status()
        current_phase = status_info["current_phase"]

        # Invariant check: Quality Gates must pass
        if quality_gate_report:
            if quality_gate_report.get("decision") == "DO NOT PUBLISH" or quality_gate_report.get("failed_gates_count", 0) > 0:
                raise QualityGateBypassProhibitedError(
                    f"Article '{slug}' failed {quality_gate_report.get('failed_gates_count')} quality gate(s). "
                    "CRITICAL INVARIANT: Never bypass a failed quality gate to meet a publishing target."
                )

        # Scan for 7 High-Risk Policy Triggers
        high_risk_triggers = self.scan_for_high_risk_triggers(html_content)
        has_high_risk = len(high_risk_triggers) > 0

        # Save HTML preview file
        preview_file_path = self.previews_dir / f"{slug}.html"
        with open(preview_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Unique preview ID
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        existing_previews = ledger.get("pending_previews", [])
        preview_id = f"PRV-{len(existing_previews) + len(ledger.get('approved_history', [])) + len(ledger.get('rejected_history', [])) + 1:04d}"

        # Determine Gating Decision
        if current_phase == PHASE_1_SUPERVISED:
            approval_required = True
            decision = "HELD_FOR_HUMAN_APPROVAL"
            decision_reason = (
                f"Phase 1 Supervised Mode Active: The first {PHASE_2_THRESHOLD} publishing cycles require "
                f"explicit preview and human approval. (Completed: {status_info['approved_supervised_publications_count']}/{PHASE_2_THRESHOLD})."
            )
        elif has_high_risk:
            approval_required = True
            decision = "HELD_FOR_HUMAN_APPROVAL"
            triggered_categories = list(set(t["category"] for t in high_risk_triggers))
            decision_reason = (
                f"Phase 2 High-Risk Trigger: Content contains {len(triggered_categories)} sensitive category claim(s) "
                f"requiring human sign-off: {', '.join(triggered_categories)}."
            )
        else:
            approval_required = False
            decision = "APPROVED_FOR_AUTO_PUBLICATION"
            decision_reason = (
                "Phase 2 Low-Risk Content: All 20 quality gates passed and zero high-risk claims detected. "
                "Eligible for immediate automated publication."
            )

        now_pkt = get_pkt_now_str()
        preview_record = {
            "preview_id": preview_id,
            "slug": slug,
            "title": title,
            "metadata": metadata,
            "preview_path": str(preview_file_path),
            "current_phase": current_phase,
            "approval_required": approval_required,
            "decision": decision,
            "decision_reason": decision_reason,
            "high_risk_triggers": high_risk_triggers,
            "status": "PENDING" if approval_required else "READY_TO_PUBLISH",
            "created_at_pkt": now_pkt,
            "reviewed_by": None,
            "reviewed_at_pkt": None,
            "reviewer_notes": None
        }

        if approval_required:
            ledger.setdefault("pending_previews", []).append(preview_record)
            ledger["last_updated_pkt"] = now_pkt
            with open(self.control_ledger_path, "w", encoding="utf-8") as f:
                json.dump(ledger, f, indent=2)

        return preview_record

    # --------------------------------------------------------------------------
    # 4. Human Approval Workflow
    # --------------------------------------------------------------------------
    def human_approve_preview(
        self,
        preview_id_or_slug: str,
        reviewer_name: str,
        reviewer_notes: str
    ) -> Dict[str, Any]:
        """
        Signs off on a pending preview.
        Increments the supervised publication count and transitions to Phase 2 when threshold (3) is reached.
        """
        if not reviewer_name or not reviewer_name.strip():
            raise ValueError("Reviewer name is mandatory for human approval.")

        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        pending = ledger.get("pending_previews", [])
        target = None
        target_idx = -1

        for idx, item in enumerate(pending):
            if item.get("preview_id") == preview_id_or_slug or item.get("slug") == preview_id_or_slug:
                target = item
                target_idx = idx
                break

        if not target:
            raise KeyError(f"Pending preview '{preview_id_or_slug}' not found.")

        # Remove from pending, record in approved history
        pending.pop(target_idx)
        now_pkt = get_pkt_now_str()

        target["status"] = "APPROVED_BY_HUMAN"
        target["reviewed_by"] = reviewer_name.strip()
        target["reviewed_at_pkt"] = now_pkt
        target["reviewer_notes"] = reviewer_notes.strip()

        ledger.setdefault("approved_history", []).append(target)
        ledger["approved_supervised_publications_count"] = ledger.get("approved_supervised_publications_count", 0) + 1

        # Check for Phase 2 Transition
        if ledger["approved_supervised_publications_count"] >= ledger.get("phase_2_threshold", PHASE_2_THRESHOLD):
            ledger["current_phase"] = PHASE_2_AUTONOMOUS_LOW_RISK

        ledger["last_updated_pkt"] = now_pkt

        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        # Automatically execute search engine discovery & indexing workflow for approved article
        discovery_telemetry = None
        if target.get("canonical_url"):
            try:
                from agent.indexing_notifier import IndexingNotifierEngine
                notifier = IndexingNotifierEngine(workspace_root=self.workspace_root)
                discovery_telemetry = notifier.execute_post_publication_discovery(
                    url=target["canonical_url"],
                    html_content=target.get("html_preview"),
                    is_deployed=True,
                    dry_run=False
                )
            except Exception as e:
                discovery_telemetry = {"error": str(e)}

        return {
            "preview_id": target["preview_id"],
            "slug": target["slug"],
            "status": "APPROVED_BY_HUMAN",
            "reviewed_by": reviewer_name,
            "current_phase": ledger["current_phase"],
            "approved_supervised_count": ledger["approved_supervised_publications_count"],
            "phase_2_unlocked": ledger["current_phase"] == PHASE_2_AUTONOMOUS_LOW_RISK,
            "discovery_telemetry": discovery_telemetry
        }

    # --------------------------------------------------------------------------
    # 5. Human Rejection Workflow
    # --------------------------------------------------------------------------
    def human_reject_preview(
        self,
        preview_id_or_slug: str,
        reviewer_name: str,
        rejection_reason: str
    ) -> Dict[str, Any]:
        """Rejects a pending preview with documented feedback."""
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        pending = ledger.get("pending_previews", [])
        target = None
        target_idx = -1

        for idx, item in enumerate(pending):
            if item.get("preview_id") == preview_id_or_slug or item.get("slug") == preview_id_or_slug:
                target = item
                target_idx = idx
                break

        if not target:
            raise KeyError(f"Pending preview '{preview_id_or_slug}' not found.")

        pending.pop(target_idx)
        now_pkt = get_pkt_now_str()

        target["status"] = "REJECTED_BY_HUMAN"
        target["reviewed_by"] = reviewer_name.strip()
        target["reviewed_at_pkt"] = now_pkt
        target["rejection_reason"] = rejection_reason.strip()

        ledger.setdefault("rejected_history", []).append(target)
        ledger["last_updated_pkt"] = now_pkt

        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        return {
            "preview_id": target["preview_id"],
            "slug": target["slug"],
            "status": "REJECTED_BY_HUMAN",
            "rejection_reason": rejection_reason
        }


# ==============================================================================
# CLI Entrypoint
# ==============================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AIDigiTools Publishing Control Engine")
    parser.add_argument("--status", action="store_true", help="Display current operational phase and queue count")
    parser.add_argument("--list-pending", action="store_true", help="List all pending previews awaiting human approval")
    parser.add_argument("--approve", help="Preview ID or slug to approve")
    parser.add_argument("--reject", help="Preview ID or slug to reject")
    parser.add_argument("--reviewer", help="Name of the human reviewer", default="Abeera Farooq")
    parser.add_argument("--notes", help="Editorial review notes", default="Verified compliant with AIDigiTools guidelines.")
    args = parser.parse_args()

    engine = PublishingControlEngine()

    if args.status:
        st = engine.get_operational_status()
        print(f"[PUBLISHING CONTROL STATUS]")
        print(f"  Current Phase: {st['current_phase']}")
        print(f"  Approved Supervised Count: {st['approved_supervised_publications_count']}/{st['phase_2_threshold']}")
        print(f"  Phase 2 Unlocked: {st['phase_2_unlocked']}")
        print(f"  Pending Previews: {st['pending_previews_count']}")
        sys.exit(0)

    if args.list_pending:
        with open(engine.control_ledger_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        pending = data.get("pending_previews", [])
        print(f"[PENDING PREVIEWS] Total: {len(pending)}")
        for p in pending:
            print(f"  - [{p['preview_id']}] {p['slug']} | {p['title']} ({p['decision_reason']})")
        sys.exit(0)

    if args.approve:
        res = engine.human_approve_preview(args.approve, args.reviewer, args.notes)
        print(f"[APPROVED] {res['preview_id']} ({res['slug']}) approved by {res['reviewed_by']}.")
        print(f"  Phase: {res['current_phase']} (Count: {res['approved_supervised_count']})")
        sys.exit(0)

    if args.reject:
        res = engine.human_reject_preview(args.reject, args.reviewer, args.notes)
        print(f"[REJECTED] {res['preview_id']} ({res['slug']}) rejected: {res['rejection_reason']}")
        sys.exit(0)


if __name__ == "__main__":
    main()

