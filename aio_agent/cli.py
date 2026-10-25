import argparse
import sys
from pathlib import Path
from .extractability import ExtractabilityAuditor
from .query_fanout import QueryFanoutAuditor
from .grounding_scorer import GroundingScorer
from .llms_sync import LLMsSync

def main():
    parser = argparse.ArgumentParser(description="AIDigiTools AIO Grounding Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # audit command
    audit_parser = subparsers.add_parser("audit", help="Audit all HTML files for AIO Grounding standards")
    audit_parser.add_argument("--root", default=".", help="Root directory of aidigitools")

    # score command
    score_parser = subparsers.add_parser("score", help="Score a single HTML file")
    score_parser.add_argument("file", help="Path to HTML file")

    # fanout command
    fanout_parser = subparsers.add_parser("fan-out", help="Check 5-branch fanout on an HTML file")
    fanout_parser.add_argument("file", help="Path to HTML file")

    # sync-llms command
    sync_parser = subparsers.add_parser("sync-llms", help="Regenerate llms.txt and llms-full.txt")
    sync_parser.add_argument("--root", default=".", help="Root directory of aidigitools")

    args = parser.parse_args()

    if args.command == "audit":
        scorer = GroundingScorer()
        root = Path(args.root)
        html_files = [p for p in root.glob("**/*.html") if not any(part.startswith((".", "venv", "node_modules")) for part in p.parts)]
        if not html_files:
            print(f"[AIO] No HTML files found under {root}")
            return 0

        failed = 0
        print(f"[AIO] Scanning {len(html_files)} HTML pages for AIO Grounding...")
        for hf in sorted(html_files):
            res = scorer.score_file(hf)
            status = res["status"]
            score = res["grounding_score"]
            print(f"  {hf}: {score}/100 [{status}]")
            if score < 70:
                failed += 1

        print(f"[AIO] Audit finished. {len(html_files) - failed} Passed, {failed} Need Optimization.")
        return 1 if failed > 0 else 0

    elif args.command == "score":
        scorer = GroundingScorer()
        res = scorer.score_file(args.file)
        print(f"File: {res['file']}")
        print(f"Grounding Score: {res['grounding_score']}/100 [{res['status']}]")
        print(f"H1 Valid: {res['extractability']['has_single_h1']}")
        print(f"Quick Answer Word Count: {res['extractability']['word_count']} words")
        print(f"Fan-out Branches Matched: {res['query_fanout']['matched_branches']}/5")
        return 0

    elif args.command == "fan-out":
        fanout = QueryFanoutAuditor()
        res = fanout.audit_file(args.file)
        print(f"File: {args.file}")
        print(f"Fan-out Score: {res['fanout_score']}% ({res['matched_branches']}/{res['total_branches']})")
        for k, v in res["branches"].items():
            print(f"  - {k}: {'PASS' if v else 'MISSING'}")
        return 0

    elif args.command == "sync-llms":
        syncer = LLMsSync(args.root)
        res = syncer.sync()
        print(f"[AIO] Synchronized llms.txt and llms-full.txt ({res['bytes_written']} bytes)")
        return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
