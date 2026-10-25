import re

class GSCFilterEngine:
    """Google Search Console RE2 Regular Expression Filter Engine.
    Strictly adheres to Google RE2 syntax: no lookaround assertions, no backreferences.
    """

    RE2_COMMERCIAL_INTENT = r"(?i)\b(buy|price|cost|easypaisa|jazzcash|sadapay|pakistan|pkr|subscription|rate|purchase|account)\b"
    RE2_INFORMATIONAL_INTENT = r"(?i)\b(how to|what is|review|vs|difference|alternative|guide|comparison|tutorial)\b"
    RE2_QUESTION_INTENT = r"(?i)^(who|what|where|when|why|how|can|is|does|are|should)\b"
    RE2_PAKISTAN_GEO = r"(?i)\b(pakistan|karachi|lahore|islamabad|rawalpindi|pkr|rs)\b"
    RE2_BRAND_QUERY = r"(?i)\b(aidigitools|ai digi tools)\b"

    @classmethod
    def match_commercial(cls, query: str) -> bool:
        return bool(re.search(cls.RE2_COMMERCIAL_INTENT, query))

    @classmethod
    def match_informational(cls, query: str) -> bool:
        return bool(re.search(cls.RE2_INFORMATIONAL_INTENT, query))

    @classmethod
    def match_question(cls, query: str) -> bool:
        return bool(re.search(cls.RE2_QUESTION_INTENT, query))

    @classmethod
    def match_pakistan_geo(cls, query: str) -> bool:
        return bool(re.search(cls.RE2_PAKISTAN_GEO, query))

    @classmethod
    def is_striking_distance(cls, position: float) -> bool:
        """Position between 4.0 and 15.0 represents prime striking distance."""
        return 4.0 <= position <= 15.0

    @classmethod
    def filter_opportunities(cls, gsc_rows: list[dict]) -> list[dict]:
        """Filters GSC search rows (query, clicks, impressions, ctr, position) for high-impact opportunities."""
        opportunities = []
        for row in gsc_rows:
            pos = float(row.get("position", 100))
            query = row.get("query", "")
            impressions = int(row.get("impressions", 0))

            if cls.is_striking_distance(pos) and impressions >= 10:
                is_comm = cls.match_commercial(query)
                is_geo = cls.match_pakistan_geo(query)
                priority = "HIGH" if (is_comm and is_geo) else ("MEDIUM" if is_comm or is_geo else "LOW")
                
                opportunities.append({
                    "query": query,
                    "position": pos,
                    "impressions": impressions,
                    "clicks": int(row.get("clicks", 0)),
                    "ctr": float(row.get("ctr", 0.0)),
                    "priority": priority,
                    "is_commercial": is_comm,
                    "is_geo": is_geo
                })
        return sorted(opportunities, key=lambda x: (x["priority"] == "HIGH", x["impressions"]), reverse=True)
