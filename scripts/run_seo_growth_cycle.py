"""
AIDigiTools — Master SEO Growth Cycle Runner CLI
================================================
Executes the unified 6-stage autonomous SEO growth cycle:
  Research → Analyze → Optimize → Content Cadence → Index → Monitor Dashboard

Usage:
  python scripts/run_seo_growth_cycle.py
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
SEO_AGENT_DIR = REPO_ROOT / "seo-agent"
sys.path.insert(0, str(SEO_AGENT_DIR))

# Safe encoding reconfiguration for cross-platform terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from agent.autonomous_seo_growth_engine import AutonomousSEOGrowthEngine

def main():
    engine = AutonomousSEOGrowthEngine(REPO_ROOT)
    dashboard = engine.execute_full_cycle()
    metrics = dashboard.get("metrics", {})
    print(f"\n[SUMMARY] Clicks: {metrics.get('total_clicks')}, Impressions: {metrics.get('total_impressions')}, "
          f"Avg Position: {metrics.get('average_position')}, Ranked Queries: {metrics.get('ranked_queries_count')}")
    print(f"[REPORT] Latest dashboard available at: audit_reports/SEO_GROWTH_DASHBOARD_LATEST.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
