class SocialCardGenerator:
    """Generates localized deal card copy and image/video metadata for social channels."""

    TEMPLATES = {
        "daily_deal": (
            "🔥 AI Tools Pakistan Deal Alert!\n\n"
            "Get {tool_name} for just Rs. {price_pkr:,}/mo on AIDigiTools!\n"
            "✅ EasyPaisa / JazzCash / SadaPay / Raast\n"
            "⚡ Instant 15-min delivery on WhatsApp\n"
            "🛡️ 30-Day Replacement Warranty\n\n"
            "👉 Order now: {target_url}\n\n"
            "#AIToolsPakistan #{tool_hashtag} #EasyPaisa #FreelancePakistan #AIDigiTools"
        ),
        "educational_tip": (
            "💡 Did you know? You don't need an international credit card to use {tool_name} in Pakistan!\n\n"
            "Subscribe in flat PKR via AIDigiTools with zero conversion fee.\n"
            "🔗 Learn more: {target_url}\n\n"
            "#PakistanFreelancers #AITools #{tool_hashtag} #AIDigiTools"
        )
    }

    def generate_deal_card(self, tool_name: str, price_pkr: int, target_url: str, card_type: str = "daily_deal") -> dict:
        template = self.TEMPLATES.get(card_type, self.TEMPLATES["daily_deal"])
        clean_tag = tool_name.replace(" ", "").replace("+", "Plus").replace("-", "")
        
        caption = template.format(
            tool_name=tool_name,
            price_pkr=price_pkr,
            target_url=target_url,
            tool_hashtag=clean_tag
        )

        return {
            "tool_name": tool_name,
            "price_pkr": price_pkr,
            "target_url": target_url,
            "caption": caption,
            "card_type": card_type,
            "character_count": len(caption),
            "media_spec": {
                "dimensions": "1080x1080",
                "format": "WEBP",
                "badge": "Flat PKR Pricing",
                "rails": ["EasyPaisa", "JazzCash", "SadaPay"]
            }
        }
