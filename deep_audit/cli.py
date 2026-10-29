import argparse
import sys
from pathlib import Path
from .engine import DeepAuditEngine

def main():
    parser = argparse.ArgumentParser(description="AIDigiTools Deep Audit Engine")
    parser.add_argument("--mode", choices=["full", "fast", "ci"], default="full", help="Audit execution mode")
    parser.add_argument("--no-network", action="store_true", help="Skip live network probes")
    parser.add_argument("--no-browser", action="store_true", help="Skip headless browser tests")
    parser.add_argument("--no-lighthouse", action="store_true", help="Skip PageSpeed / Lighthouse API queries")
    args = parser.parse_args()

    # Reconfigure stdout to UTF-8 on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    probe_network = not args.no_network
    probe_browser = not args.no_browser
    probe_lighthouse = not args.no_lighthouse

    if args.mode == "fast":
        probe_browser = False
        probe_lighthouse = False
    elif args.mode == "ci":
        # In CI, run network and browser if available
        pass

    print("======================================================================")
    print("AIDigiTools Deep Audit Engine — Initializing Audit")
    print(f"Mode: {args.mode} | Network: {probe_network} | Browser: {probe_browser} | Lighthouse: {probe_lighthouse}")
    print("======================================================================")

    engine = DeepAuditEngine()
    results = engine.run_audit(
        probe_network=probe_network,
        probe_browser=probe_browser,
        probe_lighthouse=probe_lighthouse
    )

    s = results["summary"]
    print(f"\n[AUDIT COMPLETE]")
    print(f"Total Discovered Pages: {s['total_pages_discovered']}")
    print(f"Sitemap URLs: {s['sitemap_urls_count']}")
    print(f"Orphan Pages: {s['orphan_pages_count']}")
    print(f"Health Score: {s['health_score']}%")
    print(f"Issues by Severity: {s['issues_by_severity']}")
    print(f"Issues by Confidence: {s['issues_by_confidence']}")
    print(f"\nMachine-Readable JSON: {results['json_report_path']}")
    print(f"Human-Readable Markdown: {results['markdown_report_path']}")

    # Critical issues fail the CLI exit code
    if s["issues_by_severity"]["CRITICAL"] > 0:
        print(f"\n[ALERT] Found {s['issues_by_severity']['CRITICAL']} CRITICAL issues.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] No CRITICAL blockers identified.")
        sys.exit(0)

if __name__ == "__main__":
    main()
