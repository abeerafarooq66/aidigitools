class ContentOptimizer:
    """Generates direct-answer optimization briefs based on high-opportunity queries."""

    def generate_brief(self, query: str, tool_name: str, price_pkr: int, page_url: str) -> dict:
        word_min, word_max = 35, 70
        recommended_qa = (
            f"{tool_name} in Pakistan is available for Rs. {price_pkr:,} per month through AIDigiTools. "
            f"Pakistani users can subscribe directly using EasyPaisa, JazzCash, SadaPay, or local bank transfer "
            f"without needing an international debit or credit card. Activation is delivered instantly within "
            f"15 minutes via direct WhatsApp support with a 30-day replacement warranty."
        )

        words = len(recommended_qa.split())
        return {
            "query": query,
            "tool_name": tool_name,
            "page_url": page_url,
            "word_count": words,
            "is_valid_aeo_length": word_min <= words <= word_max,
            "recommended_h1": f"{tool_name} Pakistan — Pricing, Subscription & EasyPaisa Payment",
            "recommended_direct_answer": recommended_qa,
            "target_fanout": [
                f"Flat PKR price: Rs. {price_pkr:,}",
                "Payment rails: EasyPaisa, JazzCash, SadaPay, Raast",
                "Delivery SLA: 15–30 minutes via WhatsApp",
                "Guarantee: 30-day replacement warranty",
                "Audience: Pakistani students, freelancers, and businesses"
            ]
        }
