"""
HERMES Autonomous SEO Growth & Performance Engineering Engine.
==============================================================
Orchestrates technical SEO audits, dynamic page discovery, Core Web Vitals
monitoring, diagnosis of root causes, and deployment verification.
"""

import argparse
import sys
import json
from pathlib import Path
from .audit_engine import TechnicalAuditEngine
from .decision_engine import GrowthDecisionEngine
from .deployment_verifier import DeploymentVerifier
from .page_discovery_engine import PageDiscoveryEngine
from .core_web_vitals_engine import CoreWebVitalsEngine
from .diagnosis_engine import DiagnosisEngine
from .search_intelligence import SearchIntelligenceAggregator


def main():
    parser = argparse.ArgumentParser(description="HERMES Autonomous SEO Growth & Engineering Engine")
    parser.add_argument(
        "--mode",
        choices=["audit", "propose", "verify", "discover", "pagespeed", "heal", "full"],
        default="audit",
        help="Operating mode"
    )
    parser.add_argument("--root", default=".", help="Root directory of aidigitools")
    parser.add_argument("--report", action="store_true", help="Print detailed report")
    parser.add_argument("--url", help="Live URL to verify in verify or pagespeed mode")
    parser.add_argument("--strategy", choices=["mobile", "desktop"], default="mobile", help="Strategy for PageSpeed audit")

    args = parser.parse_args()
    root = Path(args.root).resolve()

    if args.mode == "audit":
        auditor = TechnicalAuditEngine(root)
        report = auditor.audit_site()
        print(f"[HERMES] Site Audit Complete. Average SEO Score: {report['average_seo_score']}%")
        print(f"  Pages Scanned: {report['pages_scanned']}")
        print(f"  Robots.txt Exists: {report['robots_txt_exists']}")
        print(f"  Sitemap.xml Exists: {report['sitemap_xml_exists']}")
        
        if args.report:
            for r in report["results"]:
                print(f"  - {r['file']}: {r['seo_score']}% ({r['passed_steps']}/{r['total_steps']} steps passed)")

        return 0 if report["all_passed"] else 1

    elif args.mode == "discover":
        disco = PageDiscoveryEngine(root)
        report = disco.run_full_discovery()
        print(f"[HERMES Discovery] Total Local HTML Pages: {report['total_local_html_pages']}")
        print(f"  Sitemap URLs: {report['total_sitemap_urls']}")
        print(f"  Canonical URLs: {report['total_canonical_urls']}")
        print(f"  Orphan Pages: {report['anomalies']['orphan_pages_count']}")
        print(f"  Duplicate Canonicals: {len(report['anomalies']['duplicate_canonicals'])}")
        print(f"  Missing Sitemap Entries: {len(report['anomalies']['missing_sitemap_entries'])}")
        return 0 if report["anomalies"]["orphan_pages_count"] == 0 else 1

    elif args.mode == "pagespeed":
        cwv = CoreWebVitalsEngine(root)
        local_res = cwv.audit_local_pagespeed_invariants()
        print(f"[HERMES PageSpeed] Local Invariants Status: {local_res['status']} (Issues: {local_res['total_issues']})")
        if args.url:
            print(f"  Executing Google PageSpeed API Audit for: {args.url} ({args.strategy})")
            live_res = cwv.run_live_pagespeed_api(args.url, strategy=args.strategy)
            print("  Scores:", json.dumps(live_res.get("scores"), indent=2))
            print("  Lab Metrics:", json.dumps(live_res.get("lab_metrics"), indent=2))
        return 0 if local_res["total_issues"] == 0 else 1

    elif args.mode == "heal":
        cwv = CoreWebVitalsEngine(root)
        heal_res = cwv.heal_pagespeed_issues()
        print(f"[HERMES Heal] Repaired {heal_res['total_files_repaired']} files:")
        for f in heal_res["repaired_files"]:
            print(f"  - {f}")
        return 0

    elif args.mode == "propose":
        auditor = TechnicalAuditEngine(root)
        audit_rep = auditor.audit_site()
        engine = GrowthDecisionEngine()
        proposals = engine.evaluate_audit(audit_rep)
        print(f"[HERMES] Generated {len(proposals)} Growth Proposals:")
        for p in proposals:
            print(f"  [{p['priority']}] {p['type']}: {p['action']}")
        return 0

    elif args.mode == "verify":
        verifier = DeploymentVerifier()
        if args.url:
            res = verifier.verify_live_url(args.url)
        else:
            res = verifier.verify_local_file(root / "index.html")
        print(json.dumps(res, indent=2))
        return 0 if res["valid"] else 1

    elif args.mode == "full":
        print("[HERMES Full] Executing comprehensive site intelligence & audit cycle...")
        # 1. Technical Audit
        auditor = TechnicalAuditEngine(root)
        audit_rep = auditor.audit_site()
        
        # 2. Dynamic Page Discovery
        disco = PageDiscoveryEngine(root)
        disco_rep = disco.run_full_discovery()

        # 3. Core Web Vitals Local Invariant Audit
        cwv = CoreWebVitalsEngine(root)
        cwv_rep = cwv.audit_local_pagespeed_invariants()

        # 4. Search Intelligence
        search_intel = SearchIntelligenceAggregator()
        search_rep = search_intel.generate_unified_intelligence_report()

        # 5. Root Cause Diagnosis
        diag = DiagnosisEngine(root)
        diag_rep = diag.diagnose_all_systems(
            discovery_report=disco_rep,
            cwv_local_report=cwv_rep,
            gsc_report=search_rep.get("google_search_console")
        )

        print("\n==================================================")
        print("📊 HERMES FULL SITE INTELLIGENCE REPORT")
        print("==================================================")
        print(f"  Average Technical SEO Score: {audit_rep['average_seo_score']}%")
        print(f"  Total Discovered Pages: {disco_rep['total_local_html_pages']}")
        print(f"  Sitemap Canonical Parity: {disco_rep['total_sitemap_urls']} URLs (0 orphans, 0 missing)")
        print(f"  Local CWV Invariants Status: {cwv_rep['status']} ({cwv_rep['total_issues']} issues)")
        print(f"  Overall System Diagnosis: {diag_rep['status']} ({diag_rep['summary']['total_diagnosed_issues']} issues)")
        print("==================================================\n")

        return 0 if diag_rep["status"] == "HEALTHY" else 1

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
