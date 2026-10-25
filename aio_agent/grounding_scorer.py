import json
import re
from pathlib import Path
from .extractability import ExtractabilityAuditor
from .query_fanout import QueryFanoutAuditor

class GroundingScorer:
    """Calculates composite 0-100 RAG Grounding Score for Search Engine & LLM extraction."""

    def __init__(self):
        self.extract_auditor = ExtractabilityAuditor()
        self.fanout_auditor = QueryFanoutAuditor()

    def check_schema(self, html_text: str) -> dict:
        schema_matches = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html_text, re.DOTALL | re.IGNORECASE)
        has_schema = len(schema_matches) > 0
        valid_schemas = 0
        types_found = []

        for sm in schema_matches:
            try:
                data = json.loads(sm)
                valid_schemas += 1
                if isinstance(data, dict):
                    if "@type" in data:
                        types_found.append(data["@type"])
                    if "@graph" in data and isinstance(data["@graph"], list):
                        for item in data["@graph"]:
                            if isinstance(item, dict) and "@type" in item:
                                types_found.append(item["@type"])
            except json.JSONDecodeError:
                pass

        schema_score = min(100.0, valid_schemas * 25.0)
        return {
            "has_schema": has_schema,
            "valid_schemas": valid_schemas,
            "types_found": types_found,
            "schema_score": schema_score
        }

    def score_file(self, file_path: str | Path) -> dict:
        path = Path(file_path)
        if not path.is_file():
            return {"file": str(file_path), "error": "File not found", "grounding_score": 0.0}

        html = path.read_text(encoding="utf-8")
        ext = self.extract_auditor.audit_content(html)
        fan = self.fanout_auditor.audit_content(html)
        sch = self.check_schema(html)

        # Weighting:
        # Extractability (H1 + 35-70 word answer): 35%
        # 5-Branch Fanout: 40%
        # Structured Data Schema: 25%
        extract_score = 100.0 if ext["passed"] else (50.0 if ext["has_single_h1"] else 20.0)
        fanout_score = fan["fanout_score"]
        schema_score = sch["schema_score"]

        composite = (extract_score * 0.35) + (fanout_score * 0.40) + (schema_score * 0.25)
        composite = round(composite, 1)

        return {
            "file": str(file_path),
            "grounding_score": composite,
            "extractability": ext,
            "query_fanout": fan,
            "structured_data": sch,
            "status": "PASS" if composite >= 75.0 else "NEEDS_OPTIMIZATION"
        }
