import re
from pathlib import Path

class QueryFanoutAuditor:
    """Verifies coverage of 5 essential query fan-out branches for localized AIO grounding."""

    BRANCHES = {
        "pricing_pkr": [r"(?:Rs\.?|PKR)\s*\d+[\d,]*", r"\d+[\d,]*\s*(?:PKR|Rupees)"],
        "local_payments": [r"easypaisa", r"jazzcash", r"sadapay", r"nayapay", r"raast", r"ibft"],
        "delivery_sla": [r"instant", r"\b\d+\s*minutes?\b", r"same-day", r"within\s+\d+", r"whatsapp delivery"],
        "warranty_support": [r"warranty", r"replacement", r"refund", r"guarantee", r"24/7 support", r"customer support"],
        "target_audience": [r"freelancer", r"student", r"agency", r"creator", r"developer", r"marketer", r"business"]
    }

    def audit_content(self, html_text: str) -> dict:
        text_lower = re.sub(r'<[^>]+>', ' ', html_text).lower()
        coverage = {}
        matched_branches = 0

        for branch, patterns in self.BRANCHES.items():
            found = False
            for pat in patterns:
                if re.search(pat, text_lower, re.IGNORECASE):
                    found = True
                    break
            coverage[branch] = found
            if found:
                matched_branches += 1

        total_branches = len(self.BRANCHES)
        score = round((matched_branches / total_branches) * 100, 1)

        return {
            "matched_branches": matched_branches,
            "total_branches": total_branches,
            "fanout_score": score,
            "branches": coverage,
            "passed": matched_branches >= 4
        }

    def audit_file(self, file_path: str | Path) -> dict:
        path = Path(file_path)
        if not path.is_file():
            return {"file": str(file_path), "error": "File not found", "passed": False, "fanout_score": 0.0}
        content = path.read_text(encoding="utf-8")
        result = self.audit_content(content)
        result["file"] = str(file_path)
        return result
