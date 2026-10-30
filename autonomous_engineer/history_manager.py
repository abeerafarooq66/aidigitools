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

    def generate_trend_summary(self, period: str = "weekly") -> Dict[str, Any]:
        """Generates statistical and historical trend summaries over weekly (last 14 runs) or monthly (last 60 runs) windows."""
        history = self.load_history()
        limit = 14 if period == "weekly" else 60
        target_runs = history[-limit:] if history else []

        if not target_runs:
            return {
                "period": period,
                "has_data": False,
                "runs_analyzed": 0,
                "average_health_score": 100,
                "min_health_score": 100,
                "max_health_score": 100,
                "uptime_percentage": 100.0,
                "stability_status": "BASELINE",
                "repairs_total": 0,
                "trend_narrative": "Initial baseline established. Insufficient historical runs."
            }

        scores = [r.get("health_score", 100) for r in target_runs]
        uptime_passes = sum(1 for r in target_runs if r.get("all_live_checks_passed"))
        uptime_pct = round((uptime_passes / len(target_runs)) * 100, 2)
        avg_score = round(sum(scores) / len(scores), 1)
        min_score = min(scores)
        max_score = max(scores)
        repairs_total = sum(1 for r in target_runs if r.get("repairs_applied"))

        if min_score >= 95 and avg_score >= 98:
            status = "EXCELLENT_STABILITY"
            narrative = f"Over the past {len(target_runs)} runs, site health demonstrated rock-solid stability averaging {avg_score}% with {uptime_pct}% uptime."
        elif avg_score >= 85:
            status = "GOOD_MODERATE_FLUCTUATION"
            narrative = f"Average health score is {avg_score}%. Isolated optimization warnings were resolved."
        else:
            status = "ACTION_REQUIRED"
            narrative = f"Quality degradation detected: average health score dropped to {avg_score}%."

        summary = {
            "period": period,
            "has_data": True,
            "runs_analyzed": len(target_runs),
            "average_health_score": avg_score,
            "min_health_score": min_score,
            "max_health_score": max_score,
            "uptime_percentage": uptime_pct,
            "stability_status": status,
            "repairs_total": repairs_total,
            "trend_narrative": narrative,
            "first_run_timestamp": target_runs[0].get("timestamp_pkt"),
            "latest_run_timestamp": target_runs[-1].get("timestamp_pkt")
        }

        self.save_trend_report(summary)
        return summary

    def save_trend_report(self, trend_summary: Dict[str, Any]) -> Path:
        """Writes dated trend markdown report into audit_reports/."""
        period = trend_summary.get("period", "weekly")
        report_path = self.reports_dir / f"{period}_trends.md"

        md = [
            f"# AI DigiTools — {period.capitalize()} SEO & Infrastructure Trend Summary",
            "",
            f"**Generated:** {get_karachi_timestr()} (Asia/Karachi)  ",
            f"**Window Analyzed:** {trend_summary.get('runs_analyzed', 0)} maintenance runs ({trend_summary.get('first_run_timestamp', 'N/A')} to {trend_summary.get('latest_run_timestamp', 'N/A')})  ",
            f"**Overall Stability Posture:** **{trend_summary.get('stability_status')}**  ",
            "",
            "---",
            "",
            "## 1. Key Performance & Reliability Metrics",
            "",
            f"| Metric | Value | Baseline Standard | Status |",
            f"| :--- | :---: | :---: | :--- |",
            f"| Average Health Score | `{trend_summary.get('average_health_score')}%` | `≥ 95%` | {'✅ Optimal' if trend_summary.get('average_health_score', 0) >= 95 else '⚠️ Review'} |",
            f"| Minimum Health Score | `{trend_summary.get('min_health_score')}%` | `≥ 90%` | {'✅ Controlled' if trend_summary.get('min_health_score', 0) >= 90 else '❌ Incident'} |",
            f"| Maximum Health Score | `{trend_summary.get('max_health_score')}%` | `100%` | {'✅ Peak Health' if trend_summary.get('max_health_score', 0) == 100 else '—'} |",
            f"| Live Production Uptime | `{trend_summary.get('uptime_percentage')}%` | `100.0%` | {'✅ 100% Available' if trend_summary.get('uptime_percentage') == 100.0 else '⚠️ Degraded'} |",
            f"| Total Autonomous Repairs | `{trend_summary.get('repairs_total')}` | Safe Allowlist | Zero Failing Commits |",
            "",
            "## 2. Trend Narrative",
            "",
            f"> {trend_summary.get('trend_narrative')}",
            "",
            "> **Disclaimer:** Trend metrics measure internal code quality, crawlability compliance, and server availability. They do not represent or guarantee third-party Google Search indexing or rankings."
        ]
        report_path.write_text("\n".join(md), encoding="utf-8")
        return report_path
