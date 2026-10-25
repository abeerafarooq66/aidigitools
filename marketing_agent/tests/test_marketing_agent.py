import unittest
import os
from marketing_agent.buffer import BufferClient
from marketing_agent.social import SocialCardGenerator

class TestMarketingAgent(unittest.TestCase):

    def test_01_buffer_unconfigured_default(self):
        client = BufferClient(api_key="")
        self.assertFalse(client.is_configured())
        status = client.get_status()
        self.assertEqual(status["status"], "UNCONFIGURED")

    def test_02_buffer_configured(self):
        client = BufferClient(api_key="buff_token_123456789")
        self.assertTrue(client.is_configured())
        status = client.get_status()
        self.assertEqual(status["status"], "READY")

    def test_03_buffer_prepare_post(self):
        client = BufferClient()
        post = client.prepare_post("Hello AIDigiTools Pakistan", media_url="https://aidigitools.tech/assets/banner.webp")
        self.assertEqual(post["status"], "PREPARED")
        self.assertEqual(len(post["channels"]), 3)
        self.assertEqual(post["payload"]["media"]["photo"], "https://aidigitools.tech/assets/banner.webp")

    def test_04_buffer_simulated_dispatch(self):
        client = BufferClient(api_key="")
        res = client.schedule_post("Deal of the day")
        self.assertEqual(res["status"], "SIMULATED")

    def test_05_buffer_active_dispatch(self):
        client = BufferClient(api_key="valid_token_buffer_abc")
        res = client.schedule_post("Deal of the day")
        self.assertEqual(res["status"], "QUEUED")

    def test_06_social_card_generator_daily_deal(self):
        gen = SocialCardGenerator()
        card = gen.generate_deal_card("ChatGPT Plus", 2300, "https://aidigitools.tech/tools/chatgpt-plus.html")
        self.assertEqual(card["tool_name"], "ChatGPT Plus")
        self.assertEqual(card["price_pkr"], 2300)
        self.assertIn("Rs. 2,300", card["caption"])
        self.assertIn("EasyPaisa", card["caption"])
        self.assertIn("JazzCash", card["caption"])
        self.assertIn("AIDigiTools", card["caption"])

    def test_07_social_card_generator_educational_tip(self):
        gen = SocialCardGenerator()
        card = gen.generate_deal_card("Claude Pro", 2500, "https://aidigitools.tech/tools/claude-pro.html", card_type="educational_tip")
        self.assertIn("Did you know?", card["caption"])
        self.assertIn("Claude Pro", card["caption"])
        self.assertIn("AIDigiTools", card["caption"])

    def test_08_social_card_media_spec(self):
        gen = SocialCardGenerator()
        card = gen.generate_deal_card("Canva Pro", 600, "https://aidigitools.tech/tools/canva-pro.html")
        spec = card["media_spec"]
        self.assertEqual(spec["dimensions"], "1080x1080")
        self.assertEqual(spec["format"], "WEBP")
        self.assertIn("EasyPaisa", spec["rails"])

if __name__ == "__main__":
    unittest.main()
