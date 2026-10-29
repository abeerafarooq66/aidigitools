import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import REPORTS_DIR, HISTORY_FILE, get_karachi_timestr

class HistoryManager:
    """Manages persistent audit history and diffing between scheduled runs to identify recurring problems."""

    def __init__(self, reports_dir: Path = REPORTS_DIR, history_file: Path = HISTORY_FILE):
        self.reports_dir = Path(reports_dir)
        self.history_file = Path(history_file)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def load_history(self) -> List[Dict[str, Any]]:
        """Loads historical audit records."""
        if not self.history_file.exists():
            return []
        try:
            return json.loads(self.history_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def get_latest_run(self) -> Optional[Dict[str, Any]]:
        """Retrieves the most recent audit run record."""
        history = self.load_history()
        return history[-1] if history else None

    def compare_with_previous(self, current_issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compares current issues with previous run to detect recurring and new problems."""
        prev_run = self.get_latest_run()
        if not prev_run:
            return {
                "has_previous": False,
                "new_issues": current_issues,
                "resolved_issues": [],
                "recurring_issues": [],
                "new_count": len(current_issues),
                "resolved_count": 0,
                "recurring_count": 0
            }

        prev_issue_keys = {
            f"{i.get('file')}:{i.get('type')}"
            for i in prev_run.get("issues", [])
        }
        current_issue_keys = {
            f"{i.get('file')}:{i.get('type')}"
            for i in current_issues
        }

        recurring_keys = current_issue_keys.intersection(prev_issue_keys)
        new_keys = current_issue_keys - prev_issue_keys
        resolved_keys = prev_issue_keys - current_issue_keys

        recurring = [i for i in current_issues if f"{i.get('file')}:{i.get('type')}" in recurring_keys]
        new_issues = [i for i in current_issues if f"{i.get('file')}:{i.get('type')}" in new_keys]

        return {
            "has_previous": True,
            "previous_timestamp": prev_run.get("timestamp_pkt"),
            "previous_health_score": prev_run.get("health_score"),
            "recurring_count": len(recurring),
            "new_count": len(new_issues),
            "resolved_count": len(resolved_keys),
            "recurring_issues": recurring,
            "new_issues": new_issues
        }

    def record_run(self, audit_summary: Dict[str, Any], repair_summary: Dict[str, Any], live_summary: Dict[str, Any]) -> str:
        """Appends current run metrics to the persistent audit history file."""
        history = self.load_history()
        record_id = f"run-{get_karachi_timestr().replace(':', '-').replace(' ', '_')}"

        record = {
            "run_id": record_id,
            "timestamp_pkt": get_karachi_timestr(),
            "health_score": audit_summary.get("health_score", 0),
            "pages_scanned": audit_summary.get("pages_scanned", 0),
            "critical_count": audit_summary.get("critical_count", 0),
            "warning_count": audit_summary.get("warning_count", 0),
            "broken_links_count": audit_summary.get("link_graph", {}).get("broken_links_count", 0),
            "all_live_checks_passed": live_summary.get("all_live_checks_passed", False),
            "repairs_applied": repair_summary.get("applied", False),
            "repairs_rolled_back": repair_summary.get("rolled_back", False),
            "issues": audit_summary.get("issues", [])
        }

        # Keep last 50 runs
        history.append(record)
        if len(history) > 50:
            history = history[-50:]

        self.history_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
        return record_id
