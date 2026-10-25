import re

class PageMapper:
    """Maps high-value search queries to appropriate page types (Product Tool page vs Guide)."""

    def map_query(self, query: str) -> dict:
        q_lower = query.lower()

        # Check for comparison / vs intent
        if re.search(r"\b(vs|versus|difference|comparison|or)\b", q_lower):
            tools = re.findall(r"\b(chatgpt|claude|midjourney|canva|capcut|perplexity|gemini)\b", q_lower)
            if len(tools) >= 2:
                target_slug = f"guides/{tools[0]}-vs-{tools[1]}.html"
            else:
                target_slug = "guides/ai-tools-comparison.html"
            return {
                "query": query,
                "page_type": "GUIDE",
                "target_url": f"https://aidigitools.tech/{target_slug}",
                "intent": "INFORMATIONAL_COMPARISON"
            }

        # Check for direct product purchase intent
        tool_keywords = ["chatgpt", "claude", "canva", "midjourney", "capcut", "perplexity", "grammarly", "elevenlabs"]
        for tk in tool_keywords:
            if tk in q_lower:
                return {
                    "query": query,
                    "page_type": "PRODUCT",
                    "target_url": f"https://aidigitools.tech/tools/{tk}-pro.html" if tk in ["claude", "canva", "capcut", "perplexity"] else f"https://aidigitools.tech/tools/{tk}-plus.html" if tk == "chatgpt" else f"https://aidigitools.tech/tools/{tk}.html",
                    "intent": "COMMERCIAL_TRANSACTIONAL"
                }

        # General inquiry defaults to homepage or catalog
        return {
            "query": query,
            "page_type": "INDEX",
            "target_url": "https://aidigitools.tech/#products",
            "intent": "GENERAL_DISCOVERY"
        }
