import argparse
import sys
import json
from pathlib import Path
from .audit_engine import TechnicalAuditEngine
from .decision_engine import GrowthDecisionEngine
from .deployment_verifier import DeploymentVerifier

def main():
    parser = argparse.ArgumentParser(description="HERMES Autonomous SEO Growth Loop")
    parser.add_argument("--mode", choices=["audit", "propose", "verify"], default="audit", help="Operating mode")
    parser.add_argument("--root", default=".", help="Root directory of aidigitools")
    parser.add_argument("--report", action="store_true", help="Print detailed report")
    parser.add_argument("--url", help="Live URL to verify in verify mode")

    args = parser.parse_args()
    root = Path(args.root)

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

if __name__ == "__main__":
    sys.exit(main() or 0)
