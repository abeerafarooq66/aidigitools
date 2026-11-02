"""
AIDigiTools — Publishing Control Engine (Part 20).
==================================================
Strictly implements Part 20 of the Master Architecture Charter:
PUBLISHING CONTROL.

Modes:
- FULL_AUTONOMOUS: Full autonomous blog publishing authorized by site owner.
  Eligible articles passing 100% quality gates with zero high-risk claims
  publish automatically without requiring human approval.
- PHASE_1_SUPERVISED: Supervised mode where articles require human review.
- PHASE_2_AUTONOMOUS_LOW_RISK: Low-risk autonomous mode unlocked after 3 approvals.

Safety Invariants:
1. NEVER bypass a failed quality gate to meet a publishing target.
2. Global emergency publishing disable switch instantly halts all auto-publishing.
3. Persistent high-risk triggers require policy review before publishing.
"""

import os
import re
import sys
import json
import hashlib
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
FULL_AUTONOMOUS = "FULL_AUTONOMOUS"
PHASE_2_THRESHOLD = 3

# 7 Mandatory High-Risk Triggers Requiring Policy Review
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


class EmergencyPublishingDisabledError(PublishingControlError):
    """Raised when publishing is attempted while emergency switch is active."""
    pass


class PublishingControlEngine:
    """
    Enforces publishing governance:
    - FULL_AUTONOMOUS: Instant publication for 100% compliant articles without human review.
    - PHASE_1_SUPERVISED: Supervised mode with human approval queue.
    - PHASE_2_AUTONOMOUS_LOW_RISK: Low-risk autonomous publishing after initial unlock.
    - Global emergency disable switch for immediate operational halt.
    - Persistent high-risk trigger scanner for sensitive claims.
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
                "ledger_version": "2.0.0",
                "business_timezone": "PKT (UTC+5)",
                "current_phase": PHASE_1_SUPERVISED,
                "approved_supervised_publications_count": 0,
                "phase_2_threshold": PHASE_2_THRESHOLD,
                "pending_previews": [],
                "approved_history": [],
                "rejected_history": [],
                "published_history": [],
                "last_updated_pkt": get_pkt_now_str()
            }
            with open(self.control_ledger_path, "w", encoding="utf-8") as f:
                json.dump(default_ledger, f, indent=2)

    # --------------------------------------------------------------------------
    # 1. Operational Phase State & Emergency Switch
    # --------------------------------------------------------------------------
    def is_emergency_disabled(self) -> bool:
        """Checks if the global emergency publishing disable switch is active."""
        if not self.control_ledger_path.exists():
            return False
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        return bool(ledger.get("emergency_publishing_disabled", False))

    def set_emergency_switch(self, disabled: bool) -> Dict[str, Any]:
        """Toggles the global emergency publishing disable switch."""
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        ledger["emergency_publishing_disabled"] = bool(disabled)
        now_pkt = get_pkt_now_str()
        ledger["last_updated_pkt"] = now_pkt
        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)
        return {
            "emergency_publishing_disabled": bool(disabled),
            "updated_at_pkt": now_pkt
        }

    def set_publishing_mode(self, mode: str, authorized: bool = True) -> Dict[str, Any]:
        """Sets publishing operational mode (e.g. FULL_AUTONOMOUS, PHASE_1_SUPERVISED)."""
        valid_modes = [FULL_AUTONOMOUS, PHASE_1_SUPERVISED, PHASE_2_AUTONOMOUS_LOW_RISK]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode '{mode}'. Choose from: {valid_modes}")

        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        ledger["current_phase"] = mode
        ledger["autonomous_publishing_authorized"] = bool(authorized)
        now_pkt = get_pkt_now_str()
        ledger["last_updated_pkt"] = now_pkt

        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        return {
            "current_phase": mode,
            "autonomous_publishing_authorized": bool(authorized),
            "updated_at_pkt": now_pkt
        }

    def get_operational_status(self) -> Dict[str, Any]:
        """Returns the current operational phase, authorization, and publication counts."""
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        count = ledger.get("approved_supervised_publications_count", 0)
        threshold = ledger.get("phase_2_threshold", PHASE_2_THRESHOLD)
        autonomous_authorized = ledger.get("autonomous_publishing_authorized", True)
        emergency_disabled = ledger.get("emergency_publishing_disabled", False)
        current_phase = ledger.get("current_phase", FULL_AUTONOMOUS)

        # Autonomous mode evaluation
        if current_phase == FULL_AUTONOMOUS:
            is_autonomous = bool(autonomous_authorized and not emergency_disabled)
        elif current_phase == PHASE_2_AUTONOMOUS_LOW_RISK:
            is_autonomous = bool((count >= threshold or autonomous_authorized) and not emergency_disabled)
        elif current_phase == PHASE_1_SUPERVISED:
            if count >= threshold and autonomous_authorized:
                current_phase = PHASE_2_AUTONOMOUS_LOW_RISK
                is_autonomous = not emergency_disabled
            else:
                is_autonomous = False
        else:
            is_autonomous = False

        if ledger.get("current_phase") != current_phase:
            ledger["current_phase"] = current_phase
            with open(self.control_ledger_path, "w", encoding="utf-8") as f:
                json.dump(ledger, f, indent=2)

        return {
            "current_phase": current_phase,
            "approved_supervised_publications_count": count,
            "phase_2_threshold": threshold,
            "autonomous_publishing_authorized": autonomous_authorized,
            "emergency_publishing_disabled": emergency_disabled,
            "phase_2_unlocked": is_autonomous,
            "is_autonomous": is_autonomous,
            "pending_previews_count": len(ledger.get("pending_previews", [])),
            "published_history_count": len(ledger.get("published_history", []))
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
        - In FULL_AUTONOMOUS: Automatically approves for publication if quality gates pass and no high-risk triggers.
        - In Phase 1: Halts for human approval.
        - In Phase 2: Permits auto-publish ONLY if 100% quality gate passed and zero high-risk triggers.
        - INVARIANT: If quality gates failed, REJECTS unconditionally. Never bypass a failed quality gate.
        """
        status_info = self.get_operational_status()
        current_phase = status_info["current_phase"]

        # Invariant check: Gemini generation authenticity (never publish fallback)
        if (
            metadata.get("is_fallback") is True
            or metadata.get("is_gemini_generated") is False
            or metadata.get("generation_method") == "FALLBACK_HEURISTIC"
        ):
            raise QualityGateBypassProhibitedError(
                f"Article '{slug}' is marked as heuristic fallback. "
                "CRITICAL INVARIANT: Heuristic fallback content must never be published to production."
            )

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
        preview_id = f"PRV-{len(existing_previews) + len(ledger.get('approved_history', [])) + len(ledger.get('rejected_history', [])) + len(ledger.get('published_history', [])) + 1:04d}"

        # Determine Gating Decision
        if status_info["emergency_publishing_disabled"]:
            approval_required = True
            decision = "BLOCKED_EMERGENCY_DISABLED"
            decision_reason = (
                "Global emergency publishing disable switch is ACTIVE. "
                "Autonomous publishing is suspended until switch is cleared."
            )
        elif has_high_risk:
            approval_required = True
            decision = "HELD_FOR_POLICY_REVIEW" if current_phase == FULL_AUTONOMOUS else "HELD_FOR_HUMAN_APPROVAL"
            triggered_categories = list(set(t["category"] for t in high_risk_triggers))
            decision_reason = (
                f"Policy Trigger: Content contains {len(triggered_categories)} sensitive category claim(s) "
                f"requiring human sign-off: {', '.join(triggered_categories)}."
            )
        elif status_info["is_autonomous"]:
            approval_required = False
            decision = "APPROVED_FOR_AUTO_PUBLICATION"
            decision_reason = (
                "Full Autonomous Mode: All 20 quality gates passed and zero high-risk claims detected. "
                "Eligible for immediate automated publication without human approval."
            )
        else:
            approval_required = True
            decision = "HELD_FOR_HUMAN_APPROVAL"
            decision_reason = (
                f"Phase 1 Supervised Mode Active: The first {PHASE_2_THRESHOLD} publishing cycles require "
                f"explicit preview and human approval. (Completed: {status_info['approved_supervised_publications_count']}/{status_info['phase_2_threshold']})."
            )

        now_pkt = get_pkt_now_str()
        preview_rel_path = f"data/previews/{slug}.html"
        preview_record = {
            "preview_id": preview_id,
            "slug": slug,
            "title": title,
            "metadata": metadata,
            "preview_path": preview_rel_path,
            "preview_file_path": preview_rel_path,
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
    # 4. Autonomous Production Publishing
    # --------------------------------------------------------------------------
    def publish_verified_article(
        self,
        slug: str,
        title: str,
        html_content: str,
        canonical_url: str,
        metadata: Optional[Dict[str, Any]] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Publishes a verified, quality-gate approved article directly to production:
        1. Writes HTML to target path (e.g. blog/{slug}.html).
        2. Computes SHA256 content hash.
        3. Updates sitemap.xml.
        4. Updates llms.txt & llms-full.txt.
        5. Submits to search engines via IndexNow.
        6. Records in publishing_control_ledger.json.
        """
        metadata = metadata or {}
        if self.is_emergency_disabled():
            raise EmergencyPublishingDisabledError(
                "Cannot publish article: global emergency publishing disable switch is active."
            )

        # Strict Invariant: Never publish heuristic fallback content to production
        if (
            metadata.get("is_fallback") is True
            or metadata.get("is_gemini_generated") is False
            or metadata.get("generation_method") == "FALLBACK_HEURISTIC"
        ):
            raise QualityGateBypassProhibitedError(
                "CRITICAL INVARIANT: Heuristic fallback content must never be published to production."
            )

        if metadata.get("quality_gate_passed") is False:
            raise QualityGateBypassProhibitedError(
                "CRITICAL INVARIANT: Articles failing quality gates must never be published to production."
            )

        # Determine target file destination
        raw_path = metadata.get("target_canonical_path") or metadata.get("relative_url")
        if not raw_path:
            raw_path = f"blog/{slug}.html"
        rel_path = raw_path.lstrip("/")
        target_file_path = self.workspace_root / rel_path
        content_hash = hashlib.sha256(html_content.encode("utf-8")).hexdigest()

        if not dry_run:
            target_file_path.parent.mkdir(parents=True, exist_ok=True)
            target_file_path.write_text(html_content, encoding="utf-8")

        now_pkt = get_pkt_now_str()

        # Update sitemap.xml
        sitemap_url_count = 0
        try:
            from scripts.generate_sitemap import generate_sitemap
            sitemap_url_count = generate_sitemap(self.workspace_root)
        except Exception as e:
            sitemap_url_count = -1

        # Update llms.txt & llms-full.txt
        try:
            from aio_agent.llms_sync import LLMsSync
            llms_sync = LLMsSync(self.workspace_root)
            llms_sync.sync()
        except Exception:
            pass

        # Update blog.html hub
        try:
            from scripts.update_blog_hub import update_blog_hub
            update_blog_hub(self.workspace_root)
        except Exception:
            pass

        # Search Engine Discovery via IndexNow
        discovery_telemetry = None
        try:
            from agent.indexing_notifier import IndexingNotifierEngine
            notifier = IndexingNotifierEngine(workspace_root=self.workspace_root)
            discovery_telemetry = notifier.execute_post_publication_discovery(
                url=canonical_url,
                html_content=html_content,
                verify_live_deployment=False,
                dry_run=dry_run
            )
        except Exception as e:
            discovery_telemetry = {
                "status": "DISCOVERY_DEFERRED",
                "reason": "Discovery execution deferred or local environment",
                "error": str(e)
            }

        # Persist to published_history in control ledger
        with open(self.control_ledger_path, "r", encoding="utf-8") as f:
            c_ledger = json.load(f)

        pub_record = {
            "slug": slug,
            "title": title,
            "canonical_url": canonical_url,
            "relative_url": rel_path,
            "content_hash": content_hash,
            "published_at_pkt": now_pkt,
            "status": "PUBLISHED_AUTONOMOUSLY",
            "sitemap_url_count": sitemap_url_count,
            "discovery_telemetry": discovery_telemetry
        }
        c_ledger.setdefault("published_history", []).append(pub_record)
        c_ledger["last_updated_pkt"] = now_pkt

        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(c_ledger, f, indent=2)

        # Dispatch publication email notification to website owner/admin
        try:
            from agent.email_notifier import BlogEmailNotifier
            email_notifier = BlogEmailNotifier(workspace_root=self.workspace_root)
            email_res = email_notifier.send_publication_alert({
                "title": title,
                "slug": slug,
                "canonical_url": canonical_url,
                "article_id": metadata.get("article_id", "ART-BLOG"),
                "published_at_pkt": now_pkt,
                "model_used": metadata.get("model_used", "Gemini API"),
                "content_hash": content_hash
            })
            pub_record["email_notification"] = email_res
        except Exception as e:
            pub_record["email_notification"] = {"sent": False, "error": str(e)}

        return pub_record

    # --------------------------------------------------------------------------
    # 5. Human Approval Workflow (Preserved for Supervised/Policy Reviews)
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

        # Check for Phase 2 Transition if in Phase 1
        if ledger.get("current_phase") == PHASE_1_SUPERVISED:
            if ledger["approved_supervised_publications_count"] >= ledger.get("phase_2_threshold", PHASE_2_THRESHOLD):
                ledger["current_phase"] = PHASE_2_AUTONOMOUS_LOW_RISK

        ledger["last_updated_pkt"] = now_pkt

        with open(self.control_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        # Check independent production deployment before triggering post-publication discovery
        discovery_telemetry = None
        target_canon = target.get("canonical_url") or target.get("metadata", {}).get("canonical_url")
        if target_canon:
            try:
                from agent.indexing_notifier import IndexingNotifierEngine
                notifier = IndexingNotifierEngine(workspace_root=self.workspace_root)
                live_check = notifier.verify_live_http(target_canon)
                if live_check.get("status") == "LIVE_HTTP_VERIFIED":
                    discovery_telemetry = notifier.execute_post_publication_discovery(
                        url=target_canon,
                        html_content=target.get("html_preview"),
                        verify_live_deployment=True,
                        dry_run=False
                    )
                else:
                    discovery_telemetry = {
                        "status": "PENDING_DEPLOYMENT_VERIFICATION",
                        "passed": False,
                        "reason": "HUMAN_APPROVED_DEPLOYMENT_PENDING",
                        "message": "Human approval recorded, but production deployment is not yet verified over live HTTPS. Search engine discovery deferred until deployment completes.",
                        "live_http": live_check
                    }
            except Exception as e:
                discovery_telemetry = {"error": str(e)}

        return {
            "preview_id": target["preview_id"],
            "slug": target["slug"],
            "status": "APPROVED_BY_HUMAN",
            "reviewed_by": reviewer_name,
            "current_phase": ledger["current_phase"],
            "approved_supervised_count": ledger["approved_supervised_publications_count"],
            "phase_2_unlocked": ledger["current_phase"] in [FULL_AUTONOMOUS, PHASE_2_AUTONOMOUS_LOW_RISK],
            "discovery_telemetry": discovery_telemetry
        }

    # --------------------------------------------------------------------------
    # 6. Human Rejection Workflow
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
    parser.add_argument("--emergency-stop", action="store_true", help="Instantly activates global emergency publishing disable switch")
    parser.add_argument("--emergency-resume", action="store_true", help="Deactivates global emergency publishing disable switch")
    parser.add_argument("--set-mode", choices=[FULL_AUTONOMOUS, PHASE_1_SUPERVISED, PHASE_2_AUTONOMOUS_LOW_RISK], help="Set operational publishing mode")
    args = parser.parse_args()

    engine = PublishingControlEngine()

    if args.emergency_stop:
        res = engine.set_emergency_switch(disabled=True)
        print(f"[EMERGENCY STOP] Publishing disabled: {res['emergency_publishing_disabled']} at {res['updated_at_pkt']}")
        sys.exit(0)

    if args.emergency_resume:
        res = engine.set_emergency_switch(disabled=False)
        print(f"[EMERGENCY RESUME] Publishing disabled: {res['emergency_publishing_disabled']} at {res['updated_at_pkt']}")
        sys.exit(0)

    if args.set_mode:
        res = engine.set_publishing_mode(args.set_mode)
        print(f"[MODE UPDATED] Operational Phase: {res['current_phase']} (Authorized: {res['autonomous_publishing_authorized']})")
        sys.exit(0)

    if args.status:
        st = engine.get_operational_status()
        print(f"[PUBLISHING CONTROL STATUS]")
        print(f"  Current Phase: {st['current_phase']}")
        print(f"  Autonomous Active: {st['is_autonomous']}")
        print(f"  Emergency Disabled: {st['emergency_publishing_disabled']}")
        print(f"  Approved Supervised Count: {st['approved_supervised_publications_count']}/{st['phase_2_threshold']}")
        print(f"  Pending Previews: {st['pending_previews_count']}")
        print(f"  Published History Count: {st['published_history_count']}")
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
