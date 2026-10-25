import unittest
from keyword_agent.gsc_filter_engine import GSCFilterEngine
from keyword_agent.competitor_gap import CompetitorGapAnalyzer
from keyword_agent.page_mapper import PageMapper
from keyword_agent.content_optimizer import ContentOptimizer

class TestKeywordAgent(unittest.TestCase):

    # --- GSC RE2 Filter Tests (1-10) ---
    def test_01_commercial_intent_buy(self):
        self.assertTrue(GSCFilterEngine.match_commercial("buy chatgpt plus"))

    def test_02_commercial_intent_price(self):
        self.assertTrue(GSCFilterEngine.match_commercial("claude pro price in lahore"))

    def test_03_commercial_intent_easypaisa(self):
        self.assertTrue(GSCFilterEngine.match_commercial("pay via easypaisa for canva"))

    def test_04_commercial_intent_jazzcash(self):
        self.assertTrue(GSCFilterEngine.match_commercial("midjourney subscription jazzcash"))

    def test_05_commercial_intent_sadapay(self):
        self.assertTrue(GSCFilterEngine.match_commercial("capcut pro sadapay pkr"))

    def test_06_commercial_intent_negative(self):
        self.assertFalse(GSCFilterEngine.match_commercial("history of artificial intelligence"))

    def test_07_informational_intent_how_to(self):
        self.assertTrue(GSCFilterEngine.match_informational("how to activate chatgpt in pakistan"))

    def test_08_informational_intent_vs(self):
        self.assertTrue(GSCFilterEngine.match_informational("chatgpt vs claude comparison"))

    def test_09_question_intent(self):
        self.assertTrue(GSCFilterEngine.match_question("how can i buy ai tools in pakistan"))
        self.assertTrue(GSCFilterEngine.match_question("what is the price of midjourney"))
        self.assertFalse(GSCFilterEngine.match_question("buy chatgpt now"))

    def test_10_pakistan_geo_matching(self):
        self.assertTrue(GSCFilterEngine.match_pakistan_geo("best ai deals pakistan"))
        self.assertTrue(GSCFilterEngine.match_pakistan_geo("cheapest canva pro karachi"))
        self.assertTrue(GSCFilterEngine.match_pakistan_geo("tools price in pkr"))
        self.assertFalse(GSCFilterEngine.match_pakistan_geo("best ai deals usa"))

    # --- Striking Distance & Opportunity Filtering (11-14) ---
    def test_11_striking_distance_valid(self):
        self.assertTrue(GSCFilterEngine.is_striking_distance(4.0))
        self.assertTrue(GSCFilterEngine.is_striking_distance(8.5))
        self.assertTrue(GSCFilterEngine.is_striking_distance(15.0))

    def test_12_striking_distance_invalid(self):
        self.assertFalse(GSCFilterEngine.is_striking_distance(3.9))
        self.assertFalse(GSCFilterEngine.is_striking_distance(15.1))
        self.assertFalse(GSCFilterEngine.is_striking_distance(1.0))

    def test_13_filter_opportunities_ranking(self):
        rows = [
            {"query": "buy chatgpt plus pakistan", "position": 5.0, "impressions": 1000, "clicks": 50},
            {"query": "random article online", "position": 8.0, "impressions": 50, "clicks": 1},
            {"query": "super high rank query", "position": 1.2, "impressions": 5000, "clicks": 800},
            {"query": "low ranking query", "position": 25.0, "impressions": 300, "clicks": 2}
        ]
        opps = GSCFilterEngine.filter_opportunities(rows)
        self.assertEqual(len(opps), 2)
        self.assertEqual(opps[0]["query"], "buy chatgpt plus pakistan")
        self.assertEqual(opps[0]["priority"], "HIGH")

    def test_14_filter_opportunities_empty_on_low_impressions(self):
        rows = [{"query": "buy chatgpt plus pakistan", "position": 5.0, "impressions": 5, "clicks": 0}]
        opps = GSCFilterEngine.filter_opportunities(rows)
        self.assertEqual(len(opps), 0)

    # --- Competitor Gap Analyzer Tests (15-18) ---
    def test_15_competitor_gap_full_catalog(self):
        analyzer = CompetitorGapAnalyzer()
        tools = ["chatgpt-plus", "claude-pro", "canva-pro", "midjourney", "capcut-pro", "perplexity-pro"]
        rep = analyzer.analyze_catalog(tools)
        self.assertEqual(rep["catalog_coverage_pct"], 100.0)
        self.assertEqual(len(rep["missing_tools"]), 0)

    def test_16_competitor_gap_partial_catalog(self):
        analyzer = CompetitorGapAnalyzer()
        tools = ["chatgpt-plus", "canva-pro"]
        rep = analyzer.analyze_catalog(tools)
        self.assertLess(rep["catalog_coverage_pct"], 50.0)
        self.assertIn("claude-pro", rep["recommended_expansion"])
        self.assertIn("midjourney", rep["recommended_expansion"])

    def test_17_competitor_gap_benchmark_pricing(self):
        analyzer = CompetitorGapAnalyzer()
        benchmarks = analyzer.PRIMARY_COMPETITOR_BENCHMARKS
        self.assertEqual(benchmarks["chatgpt-plus"]["target_price_pkr"], 2300)
        self.assertEqual(benchmarks["canva-pro"]["target_price_pkr"], 600)
        self.assertEqual(benchmarks["claude-pro"]["target_price_pkr"], 2500)

    def test_18_gap_queries_generation(self):
        analyzer = CompetitorGapAnalyzer()
        queries = analyzer.generate_gap_queries(["midjourney"])
        self.assertEqual(len(queries), 3)
        self.assertTrue(any("easypaisa" in q for q in queries))
        self.assertTrue(any("jazzcash" in q for q in queries))

    # --- Page Mapper Tests (19-22) ---
    def test_19_page_mapper_product_chatgpt(self):
        mapper = PageMapper()
        res = mapper.map_query("buy chatgpt plus subscription in pakistan")
        self.assertEqual(res["page_type"], "PRODUCT")
        self.assertIn("chatgpt-plus.html", res["target_url"])

    def test_20_page_mapper_product_claude(self):
        mapper = PageMapper()
        res = mapper.map_query("claude pro rate jazzcash")
        self.assertEqual(res["page_type"], "PRODUCT")
        self.assertIn("claude-pro.html", res["target_url"])

    def test_21_page_mapper_guide_comparison(self):
        mapper = PageMapper()
        res = mapper.map_query("chatgpt vs claude for coding in pakistan")
        self.assertEqual(res["page_type"], "GUIDE")
        self.assertIn("chatgpt-vs-claude.html", res["target_url"])

    def test_22_page_mapper_general_inquiry(self):
        mapper = PageMapper()
        res = mapper.map_query("best ai software store")
        self.assertEqual(res["page_type"], "INDEX")
        self.assertIn("#products", res["target_url"])

    # --- Content Optimizer Tests (23-25) ---
    def test_23_content_optimizer_word_count(self):
        opt = ContentOptimizer()
        brief = opt.generate_brief("ChatGPT Plus", "ChatGPT Plus", 2300, "https://aidigitools.tech/tools/chatgpt-plus.html")
        self.assertTrue(brief["is_valid_aeo_length"])
        self.assertGreaterEqual(brief["word_count"], 35)
        self.assertLessEqual(brief["word_count"], 70)

    def test_24_content_optimizer_fanout_coverage(self):
        opt = ContentOptimizer()
        brief = opt.generate_brief("Claude Pro", "Claude Pro", 2500, "https://aidigitools.tech/tools/claude-pro.html")
        self.assertEqual(len(brief["target_fanout"]), 5)
        self.assertTrue(any("2,500" in f for f in brief["target_fanout"]))

    def test_25_content_optimizer_brand_consistency(self):
        opt = ContentOptimizer()
        brief = opt.generate_brief("Canva Pro", "Canva Pro", 600, "https://aidigitools.tech/tools/canva-pro.html")
        self.assertIn("AIDigiTools", brief["recommended_direct_answer"])
        self.assertIn("EasyPaisa", brief["recommended_direct_answer"])

if __name__ == "__main__":
    unittest.main()
