import argparse
import sys
import json
from pathlib import Path
from .gsc_filter_engine import GSCFilterEngine
from .competitor_gap import CompetitorGapAnalyzer
from .page_mapper import PageMapper
from .content_optimizer import ContentOptimizer

def main():
    parser = argparse.ArgumentParser(description="AIDigiTools Keyword Intelligence Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # audit
    audit_parser = subparsers.add_parser("audit", help="Audit striking distance and commercial keywords")
    audit_parser.add_argument("--sample-file", help="Path to JSON file with GSC query rows")

    # competitor-gap
    gap_parser = subparsers.add_parser("competitor-gap", help="Analyze catalog gaps against Pakistani benchmarks")
    gap_parser.add_argument("--root", default=".", help="Root directory of aidigitools")

    # map-query
    map_parser = subparsers.add_parser("map-query", help="Map a query to a target URL and page type")
    map_parser.add_argument("query", help="Query string")

    # brief
    brief_parser = subparsers.add_parser("brief", help="Generate an AEO direct-answer optimization brief")
    brief_parser.add_argument("tool", help="Tool Name (e.g. ChatGPT Plus)")
    brief_parser.add_argument("price", type=int, help="Price in PKR")

    args = parser.parse_args()

    if args.command == "audit":
        if args.sample_file and Path(args.sample_file).is_file():
            rows = json.loads(Path(args.sample_file).read_text(encoding="utf-8"))
        else:
            rows = [
                {"query": "buy chatgpt plus in pakistan easypaisa", "position": 6.4, "impressions": 1250, "clicks": 85, "ctr": 0.068},
                {"query": "claude 3.5 sonnet price pakistan jazzcash", "position": 4.8, "impressions": 940, "clicks": 62, "ctr": 0.066},
                {"query": "canva pro subscription rate sadapay", "position": 8.1, "impressions": 2100, "clicks": 110, "ctr": 0.052},
                {"query": "what is claude ai", "position": 22.0, "impressions": 400, "clicks": 5, "ctr": 0.012},
                {"query": "midjourney shared account pakistan", "position": 5.2, "impressions": 1800, "clicks": 95, "ctr": 0.053}
            ]

        opps = GSCFilterEngine.filter_opportunities(rows)
        print(f"[KeywordAgent] Found {len(opps)} Striking Distance & Commercial Opportunities:")
        for op in opps:
            print(f"  [{op['priority']}] pos:{op['position']} | {op['query']} ({op['impressions']} imp, {op['clicks']} clicks)")
        return 0

    elif args.command == "competitor-gap":
        analyzer = CompetitorGapAnalyzer()
        root = Path(args.root)
        tools_dir = root / "tools"
        existing = [f.stem for f in tools_dir.glob("*.html")] if tools_dir.exists() else []

        gap_report = analyzer.analyze_catalog(existing)
        print(f"[KeywordAgent] Competitor Benchmark Coverage: {gap_report['catalog_coverage_pct']}%")
        print(f"  Covered Tools ({len(gap_report['covered_tools'])}): {[t['id'] for t in gap_report['covered_tools']]}")
        print(f"  Missing Opportunities ({len(gap_report['missing_tools'])}): {gap_report['recommended_expansion']}")
        return 0

    elif args.command == "map-query":
        mapper = PageMapper()
        res = mapper.map_query(args.query)
        print(json.dumps(res, indent=2))
        return 0

    elif args.command == "brief":
        opt = ContentOptimizer()
        res = opt.generate_brief(args.tool, args.price, f"https://aidigitools.tech/tools/{args.tool.lower().replace(' ', '-')}.html")
        print(json.dumps(res, indent=2))
        return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
