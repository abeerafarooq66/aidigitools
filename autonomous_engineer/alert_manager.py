import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
from pathlib import Path
from .config import get_karachi_timestr, BASE_URL

class AlertManager:
    """Free incident alerting and notification engine for AIDigiTools.
    Dispatches instant alerts for downtime, SSL problems, repeated audit failures,
    and security issues via GitHub Actions Job Summaries and optional Telegram Bot.
    Guarantees 100% free operation with zero paid notification services.
    """

    def __init__(self):
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        self.telegram_chat_id = os.environ.get("TELEGRAM_OWNER_CHAT_ID", "").strip()
        self.step_summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "").strip()

    def is_telegram_configured(self) -> bool:
        """Checks if Telegram bot secrets are available."""
        return bool(self.telegram_token and self.telegram_chat_id)

    def evaluate_alert_conditions(
        self,
        audit_summary: Dict[str, Any],
        live_summary: Dict[str, Any],
        history_diff: Optional[Dict[str, Any]] = None,
        security_summary: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Scans run telemetry and returns any triggered incident alerts."""
        alerts = []

        # 1. Downtime & HTTP Reachability Check
        hp = live_summary.get("homepage", {})
        if not hp.get("reachable") or hp.get("status_code") != 200:
            alerts.append({
                "severity": "CRITICAL",
                "type": "site_downtime",
                "title": "🚨 Production Website Reachability Failure",
                "message": f"Homepage ({BASE_URL}) returned HTTP {hp.get('status_code', 0)}: {hp.get('error', 'Unreachable')}."
            })

        # 2. SSL / HTTPS Problems
        hp_error = str(hp.get("error", "")).lower()
        if "ssl" in hp_error or "certificate" in hp_error:
            alerts.append({
                "severity": "CRITICAL",
                "type": "ssl_certificate_error",
                "title": "🔒 SSL / HTTPS Certificate Incident",
                "message": f"SSL validation failed for {BASE_URL}: {hp.get('error')}."
            })

        # 3. Repeated / Consecutive Audit Failures
        health_score = audit_summary.get("health_score", 100)
        if health_score < 80:
            prev_score = (history_diff or {}).get("previous_health_score", 100)
            if prev_score and prev_score < 80:
                alerts.append({
                    "severity": "HIGH",
                    "type": "repeated_audit_failure",
                    "title": "⚠️ Repeated Audit Quality Degradation",
                    "message": f"Website Health Score dropped to {health_score}% for 2 consecutive runs (previous: {prev_score}%)."
                })

        # 4. Critical Security Vulnerabilities or Leaks
        if security_summary and not security_summary.get("is_secure"):
            secrets_count = security_summary.get("critical_count", 0)
            alerts.append({
                "severity": "CRITICAL",
                "type": "security_vulnerability",
                "title": "🛡️ Critical Security Vulnerability Detected",
                "message": f"Security scanner detected {secrets_count} critical issue(s) (exposed credentials or workflow permission escalations)."
            })

        # 5. Broken IndexNow Verification Key
        idx = live_summary.get("indexnow_key", {})
        if not idx.get("valid"):
            alerts.append({
                "severity": "HIGH",
                "type": "indexnow_key_missing",
                "title": "⚠️ IndexNow Ownership Verification File Missing/Mismatch",
                "message": f"IndexNow key verification file at {idx.get('url')} is invalid or mismatching: {idx.get('error')}."
            })

        return alerts

    def send_telegram_alert(self, title: str, message: str, severity: str = "HIGH") -> Dict[str, Any]:
        """Sends an instant alert message via free Telegram Bot API."""
        if not self.is_telegram_configured():
            return {"sent": False, "reason": "TELEGRAM_BOT_TOKEN or TELEGRAM_OWNER_CHAT_ID not configured."}

        text = (
            f"{title}\n\n"
            f"<b>Severity:</b> {severity}\n"
            f"<b>Timestamp:</b> {get_karachi_timestr()}\n"
            f"<b>Domain:</b> {BASE_URL}\n\n"
            f"<b>Details:</b>\n{message}"
        )
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"sent": True, "status_code": resp.status}
        except Exception as e:
            return {"sent": False, "error": str(e)}

    def write_github_step_summary(self, alerts: List[Dict[str, Any]]) -> bool:
        """Appends alert notices to GitHub Actions Step Summary markdown."""
        if not self.step_summary_path or not Path(self.step_summary_path).parent.exists():
            return False

        try:
            lines = []
            if alerts:
                lines.append(f"\n## ⚠️ Incident & Quality Alerts Triggered ({len(alerts)})\n")
                for a in alerts:
                    lines.append(f"### {a['title']} (`{a['severity']}`)")
                    lines.append(f"> {a['message']}\n")
            else:
                lines.append("\n## 🟢 All Systems Operational — Zero Incident Alerts\n")
                lines.append(f"- **Live Website:** Reachable (`HTTP 200`)\n- **SSL Certificate:** Valid\n- **Security Posture:** Secure\n")

            with open(self.step_summary_path, "a", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            return True
        except Exception as e:
            print(f"[ALERT] Could not write GITHUB_STEP_SUMMARY: {e}")
            return False

    def dispatch_alerts(self, alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Dispatches alerts across all available free notification channels."""
        self.write_github_step_summary(alerts)
        telegram_dispatches = []

        for alert in alerts:
            # Print to standard output
            print(f"\n[ALERT - {alert['severity']}] {alert['title']}")
            print(f"  {alert['message']}")

            # Send Telegram notification if configured
            if self.is_telegram_configured():
                res = self.send_telegram_alert(
                    title=alert["title"],
                    message=alert["message"],
                    severity=alert["severity"]
                )
                telegram_dispatches.append(res)

        return {
            "alerts_count": len(alerts),
            "step_summary_updated": bool(self.step_summary_path),
            "telegram_dispatches": telegram_dispatches,
            "alerts": alerts
        }
