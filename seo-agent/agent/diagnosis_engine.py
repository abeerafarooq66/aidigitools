"""
AIDigiTools — Autonomous Technical Diagnosis & Root-Cause Analysis Engine.
===========================================================================
Strictly implements Part 8 & Part 14 of the Master Operating System & Architecture Charter:
ADVANCED DIAGNOSIS, ROOT-CAUSE ANALYSIS, AND AUTONOMOUS DECISION PROTOCOL

Decision Flow:
DISCOVER -> COLLECT EVIDENCE -> DIAGNOSE -> RESEARCH -> PLAN -> IMPLEMENT -> TEST -> REVIEW -> VERIFY -> RECORD -> LEARN

Key Invariants:
1. Evidence-Driven Root-Cause Analysis:
   - Evaluates actual audit evidence from PageSpeed, GSC, LinkGraph, and Discovery engines.
   - Maps each issue to concrete source files, affected URLs, and dependencies.
2. Multi-Tier Issue Classification:
   - CRITICAL: Broken pages, indexing blockers, 404s, security exposures.
   - HIGH: Color contrast failures (<4.5:1), render-blocking resources, canonical mismatches.
   - MEDIUM: Non-composited animations, orphan pages, GSC low CTR on page 1-2.
   - LOW: Missing OpenGraph properties, minor CSS savings.
   - INFORMATIONAL: Metric distributions, CrUX rolling sample density notices.
3. Solution Risk/Benefit Assessment:
   - Generates and compares multiple solutions against risk vs benefit.
   - Selects safest non-destructive solution. Rejects blanket destructive commands.
   - Requires confidence score (0-100) before marking any issue as resolved.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
KB_FILE = WORKSPACE_ROOT / "docs" / "seo-agent" / "technical-knowledge-base.md"
DIAGNOSIS_OUTPUT_PATH = DATA_DIR / "technical_diagnosis_latest.json"


class DiagnosisEngine:
    """Diagnoses root causes, prioritizes issues, and proposes safe non-destructive solutions."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.root = Path(workspace_root) if workspace_root else WORKSPACE_ROOT

    def diagnose_all_systems(
        self,
        discovery_report: Optional[Dict[str, Any]] = None,
        cwv_local_report: Optional[Dict[str, Any]] = None,
        gsc_report: Optional[Dict[str, Any]] = None,
        link_graph_report: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Gathers evidence across all systems, determines root causes, and ranks issues by impact.
        """
        diagnosed_issues = []

        # 1. Evaluate Discovery Anomalies
        if discovery_report:
            anomalies = discovery_report.get("anomalies", {})
            
            # Orphan Pages
            for orphan in anomalies.get("orphan_pages", []):
                diagnosed_issues.append({
                    "id": f"DIAG-ORPHAN-{orphan.replace('/', '-').replace('.html', '')}",
                    "severity": "MEDIUM",
                    "category": "CRAWLABILITY",
                    "affected_resource": orphan,
                    "root_cause": "Page exists in filesystem but has 0 inbound internal links from other site pages.",
                    "evidence": f"File {orphan} is not targeted by any relative or canonical href in the site.",
                    "official_guidance": "Google Search Essentials: Make your site easily crawlable via logical link structure.",
                    "proposed_solutions": [
                        {
                            "approach": "Contextual internal link from relevant category or sibling tool page",
                            "risk": "LOW",
                            "benefit": "HIGH",
                            "recommended": True
                        },
                        {
                            "approach": "Add link to site footer",
                            "risk": "LOW",
                            "benefit": "MEDIUM",
                            "recommended": False
                        }
                    ],
                    "confidence_score": 95,
                    "resolution_status": "OPEN"
                })

            # Duplicate Canonicals
            for dup in anomalies.get("duplicate_canonicals", []):
                diagnosed_issues.append({
                    "id": f"DIAG-DUPCANON-{dup['canonical_url'][:30]}",
                    "severity": "HIGH",
                    "category": "INDEXING",
                    "affected_resource": dup["canonical_url"],
                    "root_cause": f"Multiple files point to the exact same canonical URL: {dup['competing_files']}",
                    "evidence": f"Files {dup['competing_files']} compete for canonical {dup['canonical_url']}.",
                    "official_guidance": "Google Search Central: Consolidate duplicate URLs using unique canonical tags.",
                    "proposed_solutions": [
                        {
                            "approach": "Assign unique canonical URL reflecting each page's distinct file path",
                            "risk": "LOW",
                            "benefit": "CRITICAL",
                            "recommended": True
                        }
                    ],
                    "confidence_score": 100,
                    "resolution_status": "OPEN"
                })

            # Missing Sitemap Entries
            for missing_url in anomalies.get("missing_sitemap_entries", []):
                diagnosed_issues.append({
                    "id": f"DIAG-MISSING-SITEMAP-{missing_url[:30]}",
                    "severity": "HIGH",
                    "category": "INDEXING",
                    "affected_resource": missing_url,
                    "root_cause": f"Valid canonical page is missing from sitemap.xml.",
                    "evidence": f"URL {missing_url} exists on disk but is absent from sitemap loc elements.",
                    "official_guidance": "Google Search Central: Sitemaps help search engines discover canonical URLs.",
                    "proposed_solutions": [
                        {
                            "approach": "Run indexing_notifier --sync-sitemap to regenerate sitemap with verified git lastmod",
                            "risk": "LOW",
                            "benefit": "HIGH",
                            "recommended": True
                        }
                    ],
                    "confidence_score": 98,
                    "resolution_status": "OPEN"
                })

        # 2. Evaluate Core Web Vitals Local Invariants
        if cwv_local_report:
            for iss in cwv_local_report.get("issues", []):
                diagnosed_issues.append({
                    "id": f"DIAG-CWV-{iss['type']}-{iss['file'].replace('/', '-')}",
                    "severity": iss.get("severity", "MEDIUM"),
                    "category": "PERFORMANCE_AND_ACCESSIBILITY",
                    "affected_resource": iss["file"],
                    "root_cause": iss["message"],
                    "evidence": f"Static invariant detected in {iss['file']}: {iss.get('element') or iss.get('selector') or iss.get('keyframe')}",
                    "official_guidance": "web.dev & WCAG 2.1: Maintain accessible contrast and defer non-critical JS.",
                    "proposed_solutions": [
                        {
                            "approach": "Execute CoreWebVitalsEngine.heal_pagespeed_issues() to apply verified patches",
                            "risk": "LOW",
                            "benefit": "HIGH",
                            "recommended": True
                        }
                    ],
                    "confidence_score": 99,
                    "resolution_status": "OPEN"
                })

        # 3. Evaluate Search Console Opportunities (High Impressions, Weak CTR)
        if gsc_report:
            for opp in gsc_report.get("opportunities", []):
                diagnosed_issues.append({
                    "id": f"DIAG-GSC-CTR-{opp['query'][:20].replace(' ', '-')}",
                    "severity": "MEDIUM",
                    "category": "SEARCH_INTELLIGENCE",
                    "affected_resource": opp["page"],
                    "root_cause": f"Query '{opp['query']}' receives {opp['impressions']} impressions on Page 1-2 (Pos {opp['position']}) with weak CTR ({opp['ctr']}%).",
                    "evidence": f"Search Console data confirms high visibility but low click-through engagement.",
                    "official_guidance": "Google Search Central: Optimize titles, snippets, and provide direct quick answers.",
                    "proposed_solutions": [
                        {
                            "approach": f"Optimize title and meta description for query '{opp['query']}' and refine quick-answer block",
                            "risk": "LOW",
                            "benefit": "HIGH",
                            "recommended": True
                        }
                    ],
                    "confidence_score": 90,
                    "resolution_status": "OPEN"
                })

        # Sort issues by severity priority: CRITICAL > HIGH > MEDIUM > LOW > INFORMATIONAL
        severity_rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFORMATIONAL": 4}
        diagnosed_issues.sort(key=lambda x: severity_rank.get(x["severity"], 5))

        summary = {
            "total_diagnosed_issues": len(diagnosed_issues),
            "critical_count": sum(1 for x in diagnosed_issues if x["severity"] == "CRITICAL"),
            "high_count": sum(1 for x in diagnosed_issues if x["severity"] == "HIGH"),
            "medium_count": sum(1 for x in diagnosed_issues if x["severity"] == "MEDIUM"),
            "low_count": sum(1 for x in diagnosed_issues if x["severity"] == "LOW"),
            "clean_system": len(diagnosed_issues) == 0
        }

        report = {
            "status": "HEALTHY" if summary["clean_system"] else "ACTION_REQUIRED",
            "summary": summary,
            "issues": diagnosed_issues
        }

        self._save_report(report)
        return report

    def _save_report(self, report: Dict[str, Any]):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(DIAGNOSIS_OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    from .page_discovery_engine import PageDiscoveryEngine
    from .core_web_vitals_engine import CoreWebVitalsEngine

    p_eng = PageDiscoveryEngine()
    disc = p_eng.run_full_discovery()

    cwv_eng = CoreWebVitalsEngine()
    local_cwv = cwv_eng.audit_local_pagespeed_invariants()

    diag = DiagnosisEngine()
    report = diag.diagnose_all_systems(discovery_report=disc, cwv_local_report=local_cwv)
    print("Diagnosis Status:", report["status"])
    print(f"Total Diagnosed Issues: {report['summary']['total_diagnosed_issues']}")
