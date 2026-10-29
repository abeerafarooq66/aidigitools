import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .config import REPORTS_DIR, BASE_URL, get_karachi_timestr, get_karachi_time

class ReportEngine:
    """Generates comprehensive, formatted Markdown audit reports and maintains the audit history index."""

    def __init__(self, reports_dir: Path = REPORTS_DIR):
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_markdown_report(
        self,
        audit_summary: Dict[str, Any],
        live_summary: Dict[str, Any],
        reasoner_summary: Dict[str, Any],
        repair_summary: Dict[str, Any],
        history_diff: Dict[str, Any],
        bing_summary: Optional[Dict[str, Any]] = None
    ) -> Path:
        """Generates a detailed, timestamped Markdown report for the current maintenance cycle."""
        now_str = get_karachi_timestr()
        file_stamp = get_karachi_time().strftime("%Y-%m-%d_%H%M")
        report_filename = f"audit_{file_stamp}.md"
        report_path = self.reports_dir / report_filename

        health_score = audit_summary.get("health_score", 100)
        status_badge = "🟢 PASSED" if health_score >= 95 and audit_summary.get("passed", False) else (
            "🟡 WARNING" if health_score >= 80 else "🔴 ACTION REQUIRED"
        )

        md = []
        md.append(f"# AI DigiTools Autonomous Maintenance & SEO Audit Report")
        md.append(f"")
        md.append(f"**Execution Timestamp:** {now_str} (Asia/Karachi)  ")
        md.append(f"**Domain:** [{BASE_URL}]({BASE_URL})  ")
        md.append(f"**Overall Site Status:** **{status_badge}** (Health Score: **{health_score}%**)  ")
        md.append(f"**Reasoning Engine:** {reasoner_summary.get('engine', 'Gemini Flash')} (`{reasoner_summary.get('model_used', 'none')}`)  ")
        md.append(f"")
        md.append(f"---")
        md.append(f"")

        # 1. Executive Summary
        md.append(f"## 1. Executive Summary")
        md.append(f"")
        md.append(f"> {reasoner_summary.get('diagnosis', 'Site health audit complete.')}")
        md.append(f"")
        if reasoner_summary.get("status_note"):
            md.append(f"> **Engine Note:** {reasoner_summary.get('status_note')}")
            md.append(f"")

        # 2. Live Reachability & Infrastructure Probes
        md.append(f"## 2. Live Reachability & Infrastructure Telemetry")
        md.append(f"")
        hp = live_summary.get("homepage", {})
        idx = live_summary.get("indexnow_key", {})
        md.append(f"| Target Endpoint | Live HTTP Status | Latency | Status Check |")
        md.append(f"| :--- | :---: | :---: | :--- |")
        md.append(f"| Homepage (`/`) | `{hp.get('status_code', 'N/A')}` | `{hp.get('latency_ms', 0)} ms` | {'✅ Verified' if hp.get('reachable') else '❌ Unreachable'} |")
        md.append(f"| IndexNow Key File | `{idx.get('status_code', 'N/A')}` | — | {'✅ Valid & Matching' if idx.get('valid') else '❌ Mismatch / Missing'} |")
        
        sample_routes = live_summary.get("sample_routes", [])
        for sr in sample_routes:
            md.append(f"| `{sr.get('url')}` | `{sr.get('status_code')}` | — | {'✅ OK' if sr.get('ok') else '❌ Failed'} |")
        md.append(f"")

        # 3. Technical SEO & Content Quality Audit
        md.append(f"## 3. Technical SEO & Content Quality Inspection")
        md.append(f"")
        md.append(f"- **Pages Inspected:** {audit_summary.get('pages_scanned', 0)} HTML documents")
        md.append(f"- **Sitemap URLs Declared:** {audit_summary.get('sitemap_urls_count', 0)}")
        md.append(f"- **Broken Internal Links:** {audit_summary.get('link_graph', {}).get('broken_links_count', 0)}")
        md.append(f"- **Broken Fragment Anchors:** {audit_summary.get('link_graph', {}).get('broken_anchors_count', 0)}")
        md.append(f"- **Critical Issues:** {audit_summary.get('critical_count', 0)}")
        md.append(f"- **Optimization Warnings:** {audit_summary.get('warning_count', 0)}")
        md.append(f"")

        # 4. Recurring vs New Issue Trend Analysis
        md.append(f"## 4. Run-over-Run Trend Analysis")
        md.append(f"")
        if history_diff.get("has_previous"):
            md.append(f"- **Previous Audit:** {history_diff.get('previous_timestamp')} (Score: {history_diff.get('previous_health_score')}%)")
            md.append(f"- **Newly Introduced Issues:** {history_diff.get('new_count', 0)}")
            md.append(f"- **Recurring Unresolved Issues:** {history_diff.get('recurring_count', 0)}")
            md.append(f"- **Resolved Issues:** {history_diff.get('resolved_count', 0)}")
        else:
            md.append(f"- *Initial audit cycle recorded. Baseline established.*")
        md.append(f"")

        # 5. Autonomous Repair Actions & Safeguards
        md.append(f"## 5. Autonomous Repair Execution & Safety Verification")
        md.append(f"")
        if repair_summary.get("applied"):
            md.append(f"### ✅ Verified Low-Risk Repairs Applied:")
            for p in repair_summary.get("executed_proposals", []):
                md.append(f"- **{p.get('id')}:** {p.get('action')} — *{p.get('details')}*")
            md.append(f"")
            md.append(f"```diff\n{repair_summary.get('diff', '')}\n```")
            md.append(f"")
            md.append(f"- **Verification Test Suite:** ✅ All tests passed post-repair.")
        elif repair_summary.get("rolled_back"):
            md.append(f"### ⚠️ Autonomous Repair Safely Rolled Back:")
            md.append(f"> {repair_summary.get('error')}")
            md.append(f"> Working tree was restored via emergency rollback to prevent deploying failing code.")
        else:
            md.append(f"- **Repairs Required:** Zero low-risk autonomous fixes were required this cycle. Site is clean.")
        md.append(f"")

        # 6. Manual Review Items
        manual_proposals = reasoner_summary.get("manual_review_proposals", [])
        if manual_proposals:
            md.append(f"## 6. Items Requiring Manual Engineer Review")
            md.append(f"")
            for m in manual_proposals:
                md.append(f"- **[{m.get('risk')}] {m.get('action')}:** {m.get('details')}")
            md.append(f"")

        # 7. Official Search Engine Protocols & Bing Webmaster Integration
        md.append(f"## 7. Search Engine Protocols & Bing Webmaster Telemetry")
        md.append(f"")
        md.append(f"- **IndexNow Protocol (Bing, Yandex, Seznam, Naver):** Active protocol with key [`{idx.get('url', '')}`]({idx.get('url', '')}).")
        md.append(f"- **Google Search (Googlebot / AI Overviews):** Crawlability open via `robots.txt` and verified in `sitemap.xml`. (Google relies on GSC and sitemaps, not IndexNow).")
        md.append(f"")

        if bing_summary:
            md.append(f"### Microsoft Bing Webmaster API Telemetry:")
            if bing_summary.get("connected"):
                md.append(f"- **Bing API Status:** 🟢 Connected & Authorized (`{bing_summary.get('status')}`)")
                if bing_summary.get("quota"):
                    md.append(f"- **Daily URL Quota:** `{bing_summary.get('quota')}`")
                if bing_summary.get("crawl_stats"):
                    md.append(f"- **Crawl Stats:** `{bing_summary.get('crawl_stats')}`")
                if bing_summary.get("query_stats"):
                    md.append(f"- **Query Stats:** `{bing_summary.get('query_stats')}`")
            else:
                md.append(f"- **Bing API Status:** ⚪ `{bing_summary.get('status')}` — *{bing_summary.get('message', 'BING_API_KEY secret not yet set in GitHub Actions.')}*")
            md.append(f"")

        report_path.write_text("\n".join(md), encoding="utf-8")
        self._update_index()
        return report_path

    def _update_index(self):
        """Updates audit_reports/README.md with a chronological log of all generated reports."""
        reports = sorted([f for f in self.reports_dir.glob("audit_*.md")], reverse=True)
        lines = [
            "# AI DigiTools — Autonomous Maintenance & SEO Audit History",
            "",
            "Persistent chronological archive of twice-daily cloud maintenance cycles executed for [aidigitools.tech](https://aidigitools.tech).",
            "",
            "| Report File | Execution Date | Status |",
            "| :--- | :--- | :--- |"
        ]
        for r in reports:
            name = r.name
            date_str = name.replace("audit_", "").replace(".md", "").replace("_", " ")
            lines.append(f"| [{name}](./{name}) | `{date_str}` | Active |")

        (self.reports_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")
