"""
AIDigiTools — Google Search Console Performance & SEO Action Engine
Analyzes Google Search Console telemetry (Clicks, Impressions, CTR, Position)
and produces high-ROI SEO optimization action plans.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

# Reconfigure stdout for UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Load .env
env_file = REPO_ROOT / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() not in os.environ:
                    os.environ[k.strip()] = v.strip("'\" ")

DATA_OUTPUT = REPO_ROOT / "data" / "gsc_performance_snapshot.json"
REPORT_OUTPUT = REPO_ROOT / "audit_reports" / "GSC_SEO_PERFORMANCE_LATEST.md"

from autonomous_engineer.gsc_client import GoogleSearchConsoleClient

class GSCPerformanceAnalyzer:
    """Analyzes GSC click, impression, and ranking telemetry for actionable SEO growth."""

    def __init__(self):
        self.client = GoogleSearchConsoleClient()
        self.site_url = self.client.site_url

    def run_analysis(self, days: int = 28) -> Dict[str, Any]:
        print("=" * 70)
        print("AIDigiTools — Google Search Console Performance Analyzer")
        print("=" * 70)
        print(f"Target Site: {self.site_url}")

        if not self.client.is_configured():
            print("\n[STATUS: GSC NOT CONFIGURED]")
            print("GSC_SERVICE_ACCOUNT_KEY is not set or credentials/service_account.json is missing.")
            print("Generating empty baseline dataset and guidance report...")
            snapshot = self._generate_unconfigured_snapshot()
            self._write_outputs(snapshot)
            return snapshot

        print("\n[GSC CONNECTED] Fetching live Google Search Analytics...")
        # 1. Fetch query-level data
        end_date = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d")
        start_date = (datetime.now(timezone.utc) - timedelta(days=days + 2)).strftime("%Y-%m-%d")

        query_res = self.client.query_date_range(
            start_date=start_date,
            end_date=end_date,
            dimensions=["query", "page"],
            row_limit=500
        )

        rows = (query_res.get("data") or {}).get("rows", [])
        print(f"Retrieved {len(rows)} query-page records from Google Search Console.")

        snapshot = self._process_gsc_rows(rows, start_date, end_date)
        self._write_outputs(snapshot)
        return snapshot

    def _process_gsc_rows(self, rows: List[Dict[str, Any]], start_date: str, end_date: str) -> Dict[str, Any]:
        total_clicks = sum(r.get("clicks", 0) for r in rows)
        total_impressions = sum(r.get("impressions", 0) for r in rows)
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0.0
        avg_pos = (sum(r.get("position", 0) for r in rows) / len(rows)) if rows else 0.0

        striking_distance = []
        low_ctr_opportunities = []
        page_performance = {}
        cannibalization_map = {}

        for r in rows:
            keys = r.get("keys", [])
            query = keys[0] if len(keys) > 0 else ""
            page = keys[1] if len(keys) > 1 else ""
            clicks = r.get("clicks", 0)
            impr = r.get("impressions", 0)
            ctr = r.get("ctr", 0) * 100
            pos = r.get("position", 0)

            # Page aggregates
            if page:
                if page not in page_performance:
                    page_performance[page] = {"clicks": 0, "impressions": 0, "queries_count": 0}
                page_performance[page]["clicks"] += clicks
                page_performance[page]["impressions"] += impr
                page_performance[page]["queries_count"] += 1

            # Cannibalization tracking
            if query and page:
                cannibalization_map.setdefault(query, set()).add(page)

            # Category 1: Striking distance keywords (rank 4 to 20)
            if 4.0 <= pos <= 20.0 and impr >= 10:
                striking_distance.append({
                    "query": query,
                    "target_page": page,
                    "position": round(pos, 1),
                    "impressions": impr,
                    "clicks": clicks,
                    "ctr_percent": round(ctr, 2),
                    "action": "Add dedicated H2 section, expand PAA FAQ accordion, and enrich comparison table."
                })

            # Category 2: Low-CTR opportunities (high impressions, low CTR)
            if impr >= 25 and ctr < 3.0:
                low_ctr_opportunities.append({
                    "query": query,
                    "target_page": page,
                    "impressions": impr,
                    "clicks": clicks,
                    "ctr_percent": round(ctr, 2),
                    "action": "Rewrite <title> tag with specific PKR pricing and craft high-CTR meta description."
                })

        # Sort opportunities by highest impression potential
        striking_distance.sort(key=lambda x: x["impressions"], reverse=True)
        low_ctr_opportunities.sort(key=lambda x: x["impressions"], reverse=True)

        cannibalization_risks = [
            {"query": q, "competing_urls": list(urls), "pages_count": len(urls)}
            for q, urls in cannibalization_map.items() if len(urls) > 1
        ]

        top_pages = [
            {"url": u, "clicks": data["clicks"], "impressions": data["impressions"], "queries": data["queries_count"]}
            for u, data in page_performance.items()
        ]
        top_pages.sort(key=lambda x: x["clicks"], reverse=True)

        return {
            "status": "CONNECTED",
            "date_range": f"{start_date} to {end_date}",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "overall_metrics": {
                "total_clicks": total_clicks,
                "total_impressions": total_impressions,
                "average_ctr_percent": round(avg_ctr, 2),
                "average_position": round(avg_pos, 1),
                "total_queries_ranked": len(rows)
            },
            "striking_distance_keywords": striking_distance[:15],
            "low_ctr_opportunities": low_ctr_opportunities[:15],
            "top_performing_pages": top_pages[:10],
            "cannibalization_risks": cannibalization_risks[:10]
        }

    def _generate_unconfigured_snapshot(self) -> Dict[str, Any]:
        return {
            "status": "UNCONFIGURED",
            "message": "Google Search Console Service Account is not configured. Falling back to internal heuristic telemetry.",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "overall_metrics": {
                "total_clicks": 0,
                "total_impressions": 0,
                "average_ctr_percent": 0.0,
                "average_position": 0.0,
                "total_queries_ranked": 0
            },
            "striking_distance_keywords": [],
            "low_ctr_opportunities": [],
            "top_performing_pages": [],
            "cannibalization_risks": []
        }

    def _write_outputs(self, snapshot: Dict[str, Any]):
        # 1. Write JSON snapshot
        DATA_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, ensure_ascii=False)
        print(f"  -> Saved JSON Data: {DATA_OUTPUT}")

        # 2. Write Markdown Report
        REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        md = self._render_markdown_report(snapshot)
        with open(REPORT_OUTPUT, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"  -> Saved Markdown Report: {REPORT_OUTPUT}")

    def _render_markdown_report(self, snapshot: Dict[str, Any]) -> str:
        st = snapshot.get("status")
        now_str = snapshot.get("generated_at_utc", "")
        metrics = snapshot.get("overall_metrics", {})

        md = f"""# Google Search Console Performance & Action Plan
> **Site:** {self.site_url}  
> **Status:** {st}  
> **Updated:** {now_str}

---

## 1. Overall Organic Search Performance
| Metric | Value |
| :--- | :--- |
| **Total Organic Clicks** | {metrics.get('total_clicks', 0):,} |
| **Total Impressions** | {metrics.get('total_impressions', 0):,} |
| **Average Organic CTR** | {metrics.get('average_ctr_percent', 0.0)}% |
| **Average Search Position** | {metrics.get('average_position', 0.0)} |
| **Total Queries Tracked** | {metrics.get('total_queries_ranked', 0):,} |

---

## 2. High-ROI Striking Distance Keywords (Positions 4.0 – 20.0)
*Keywords where Google has already indexed AIDigiTools on Page 1 or 2, but small on-page optimizations can drive them into the Top 3.*

"""
        sd = snapshot.get("striking_distance_keywords", [])
        if sd:
            md += "| Keyword | Position | Impressions | Clicks | Action Required |\n| :--- | :--- | :--- | :--- | :--- |\n"
            for item in sd:
                md += f"| **{item['query']}** | {item['position']} | {item['impressions']:,} | {item['clicks']} | {item['action']} |\n"
        else:
            md += "_No striking distance keywords recorded yet or credentials awaiting configuration._\n"

        md += """\n---

## 3. High-Impression / Low-CTR Click Opportunities
*Queries that users frequently see in Google Search, but where our Title/Description snippet needs more compelling hooks (PKR pricing, instant WhatsApp delivery).*

"""
        low_ctr = snapshot.get("low_ctr_opportunities", [])
        if low_ctr:
            md += "| Keyword | Impressions | CTR | Action Required |\n| :--- | :--- | :--- | :--- |\n"
            for item in low_ctr:
                md += f"| **{item['query']}** | {item['impressions']:,} | {item['ctr_percent']}% | {item['action']} |\n"
        else:
            md += "_No underperforming snippets detected._\n"

        md += """\n---

## 4. Keyword Cannibalization Risks
*Cases where multiple pages compete for the same query, dividing domain authority.*

"""
        cannibal = snapshot.get("cannibalization_risks", [])
        if cannibal:
            md += "| Query | Competing URLs |\n| :--- | :--- |\n"
            for item in cannibal:
                urls = "<br>".join(item["competing_urls"])
                md += f"| **{item['query']}** | {urls} |\n"
        else:
            md += "_Zero internal keyword cannibalization detected._\n"

        return md

if __name__ == "__main__":
    analyzer = GSCPerformanceAnalyzer()
    analyzer.run_analysis(days=28)
