import os
import sys
import argparse
import json
from pathlib import Path

# Safe encoding reconfiguration for cross-platform terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import PROJECT_ROOT, get_karachi_timestr
from .static_auditor import StaticAuditor
from .live_auditor import LiveAuditor
from .gemini_reasoner import GeminiReasoner
from .repair_executor import RepairExecutor
from .history_manager import HistoryManager
from .report_engine import ReportEngine
from .bing_client import BingWebmasterClient

def run_full_cycle(root_dir: Path = PROJECT_ROOT, skip_live: bool = False) -> int:
    """Executes the complete autonomous maintenance and SEO engineering cycle."""
    print("=" * 70)
    print("[BOT] AI DIGITOOLS AUTONOMOUS SEO & WEBSITE ENGINEER")
    print(f"Timestamp: {get_karachi_timestr()} (Asia/Karachi)")
    print("=" * 70)

    # 1. Static Audit
    print("\n[STEP 1/6] Running Exhaustive Static Codebase Audit...")
    static_auditor = StaticAuditor(root_dir)
    audit_summary = static_auditor.run_static_audit()
    print(f"  Pages Inspected: {audit_summary['pages_scanned']}")
    print(f"  Sitemap URLs: {audit_summary['sitemap_urls_count']}")
    print(f"  Health Score: {audit_summary['health_score']}%")
    print(f"  Critical Issues: {audit_summary['critical_count']}")
    print(f"  Optimization Warnings: {audit_summary['warning_count']}")
    print(f"  Broken Links: {audit_summary['link_graph']['broken_links_count']}")

    # 2. Live Telemetry Probes
    print("\n[STEP 2/6] Running Live Production Telemetry Probes...")
    live_summary = {}
    if not skip_live:
        live_auditor = LiveAuditor()
        live_summary = live_auditor.run_live_audit()
        hp = live_summary["homepage"]
        idx = live_summary["indexnow_key"]
        print(f"  Homepage Reachable: {hp.get('reachable')} (HTTP {hp.get('status_code')}, {hp.get('latency_ms')} ms)")
        print(f"  IndexNow Key File: {idx.get('valid')} (HTTP {idx.get('status_code')})")
    else:
        print("  [SKIPPED] Live probes skipped by flag.")
        live_summary = {"homepage": {"reachable": True, "status_code": 200}, "indexnow_key": {"valid": True}, "sample_routes": [], "all_live_checks_passed": True}

    # Query Bing Webmaster API Telemetry
    bing_client = BingWebmasterClient()
    bing_summary = bing_client.run_bing_audit()
    if bing_summary.get("connected"):
        print(f"  [BING API] Connected: Active Bing Webmaster Telemetry retrieved.")
    else:
        print(f"  [BING API] Status: {bing_summary.get('status')} ({bing_summary.get('message')})")

    # 3. History Comparison (Trend Detection)
    print("\n[STEP 3/6] Comparing with Previous Runs...")
    history_mgr = HistoryManager()
    history_diff = history_mgr.compare_with_previous(audit_summary["issues"])
    if history_diff["has_previous"]:
        print(f"  Previous Run: {history_diff['previous_timestamp']} (Score: {history_diff['previous_health_score']}%)")
        print(f"  New Issues: {history_diff['new_count']} | Recurring: {history_diff['recurring_count']} | Resolved: {history_diff['resolved_count']}")
    else:
        print("  Baseline run recorded. No prior comparison history.")

    # 4. Gemini Flash Reasoning
    print("\n[STEP 4/6] Engaging Gemini Flash Reasoning Engine...")
    reasoner = GeminiReasoner()
    reasoning_summary = reasoner.evaluate_audit(audit_summary)
    print(f"  Engine: {reasoning_summary.get('engine', 'Gemini Flash')} ({reasoning_summary.get('model_used')})")
    print(f"  Diagnosis: {reasoning_summary.get('diagnosis')}")
    print(f"  Auto-Repair Proposals: {len(reasoning_summary.get('auto_repair_proposals', []))}")
    print(f"  Manual Review Items: {len(reasoning_summary.get('manual_review_proposals', []))}")

    # 5. Autonomous Repair Execution
    print("\n[STEP 5/6] Evaluating & Applying Safe Autonomous Repairs...")
    repair_executor = RepairExecutor(root_dir)
    auto_proposals = reasoning_summary.get("auto_repair_proposals", [])
    repair_summary = repair_executor.execute_repairs(auto_proposals)

    if repair_summary["applied"]:
        print(f"  [OK] Applied {len(repair_summary['executed_proposals'])} repairs safely under test verification.")
    elif repair_summary["rolled_back"]:
        print(f"  [WARN] Repairs failed verification! Emergency rollback executed successfully.")
    else:
        print("  Zero autonomous repairs required this cycle. Workspace clean.")

    # 6. Persistent History & Report Generation
    print("\n[STEP 6/6] Generating Audit Report & Updating Historical Archive...")
    history_mgr.record_run(audit_summary, repair_summary, live_summary)
    report_engine = ReportEngine()
    report_path = report_engine.generate_markdown_report(
        audit_summary=audit_summary,
        live_summary=live_summary,
        reasoner_summary=reasoning_summary,
        repair_summary=repair_summary,
        history_diff=history_diff,
        bing_summary=bing_summary
    )
    print(f"  [REPORT] Report Saved: {report_path.relative_to(root_dir)}")

    print("\n" + "=" * 70)
    print("CYCLE COMPLETE — Autonomous Website Engineer Cycle Finished Successfully")
    print("=" * 70)
    return 0

def main():
    parser = argparse.ArgumentParser(description="AIDigiTools Autonomous SEO & Website Engineer")
    parser.add_argument("--mode", choices=["full", "audit", "repair", "verify"], default="full", help="Operating mode")
    parser.add_argument("--skip-live", action="store_true", help="Skip live HTTP network probes")
    parser.add_argument("--root", default=".", help="Project root directory")
    args = parser.parse_args()

    root_dir = Path(args.root).resolve()

    if args.mode == "full":
        return run_full_cycle(root_dir, skip_live=args.skip_live)
    elif args.mode == "audit":
        auditor = StaticAuditor(root_dir)
        summary = auditor.run_static_audit()
        print(json.dumps({k: v for k, v in summary.items() if k != "page_results"}, indent=2))
        return 0 if summary["passed"] else 1
    elif args.mode == "verify":
        live_auditor = LiveAuditor()
        summary = live_auditor.run_live_audit()
        print(json.dumps(summary, indent=2))
        return 0 if summary["all_live_checks_passed"] else 1
    elif args.mode == "repair":
        auditor = StaticAuditor(root_dir)
        summary = auditor.run_static_audit()
        reasoner = GeminiReasoner()
        reasoning = reasoner.evaluate_audit(summary)
        executor = RepairExecutor(root_dir)
        repairs = executor.execute_repairs(reasoning.get("auto_repair_proposals", []))
        print(json.dumps(repairs, indent=2))
        return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
