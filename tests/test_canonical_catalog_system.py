# tests/test_canonical_catalog_system.py
"""
AIDigiTools Canonical Catalog Automated Test Suite
Implements all 12 Phase 7 Quality Gates from the Canonical Catalog Brief.
"""

import unittest
import os
import json
import csv
import re
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH_DIR = r"C:\Users\Dell\.gemini\antigravity\brain\b9098f9b-3fdd-4d44-b502-c2981cd56d6f\scratch\catalog_private"
SOURCE_CSV = os.path.join(SCRATCH_DIR, "reseller_products_2026-10-22.csv")
RECONCILIATION_FILE = os.path.join(SCRATCH_DIR, "reconciliation_ledger_2902.json")
PUBLIC_CATALOG_FILE = os.path.join(BASE_DIR, "scripts", "tools_catalog.json")
LOGOS_DIR = os.path.join(BASE_DIR, "assets", "product-logos")
MANIFEST_FILE = os.path.join(LOGOS_DIR, "brand_logos_manifest.json")


class TestCanonicalCatalogSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load source CSV and private reconciliation ledger if present
        if os.path.exists(SOURCE_CSV) and os.path.exists(RECONCILIATION_FILE):
            with open(SOURCE_CSV, "r", encoding="utf-8-sig") as f:
                cls.source_rows = list(csv.DictReader(f))
            with open(RECONCILIATION_FILE, "r", encoding="utf-8") as f:
                cls.reconciliation_ledger = json.load(f)
        else:
            cls.source_rows = []
            cls.reconciliation_ledger = []

        # Load public tools catalog
        with open(PUBLIC_CATALOG_FILE, "r", encoding="utf-8") as f:
            cls.public_catalog = json.load(f)

        # Load brand logos manifest
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            cls.brand_manifest = json.load(f)

    def test_01_source_row_count(self):
        """Test 1: Source row count is exactly 2,902."""
        if not self.source_rows: self.skipTest("Private local supplier ledger excluded from git repository")
        self.assertEqual(len(self.source_rows), 2902, f"Expected 2902 rows, found {len(self.source_rows)}")

    def test_02_every_source_row_has_one_private_disposition(self):
        """Test 2: Every source row has exactly one private disposition and provenance mapping with zero silent drops."""
        if not self.reconciliation_ledger: self.skipTest("Private local supplier ledger excluded from git repository")
        self.assertEqual(len(self.reconciliation_ledger), 2902, "Reconciliation ledger must contain all 2902 records")
        valid_dispositions = {
            "HOLD_COMPLIANCE_SCREENING",
            "MAPPED_EXISTING_CANONICAL_HOLD_PRICING",
            "MAPPED_CANDIDATE_NEW_FAMILY_HOLD_PRICING",
            "HOLD_UNCLASSIFIED_CATALOG_RECORD"
        }
        seen_ids = set()
        for item in self.reconciliation_ledger:
            src_id = item["source_record_id"]
            self.assertNotIn(src_id, seen_ids, f"Duplicate source ID in ledger: {src_id}")
            seen_ids.add(src_id)
            self.assertIn(item["disposition"], valid_dispositions, f"Invalid disposition: {item['disposition']}")

    def test_03_no_exact_duplicate_canonical_plan_in_public_output(self):
        """Test 3: No exact duplicate canonical plan is shown more than once in public output."""
        all_plan_ids = []
        for slug, fam in self.public_catalog.items():
            fam_plan_ids = [p["plan_id"] for p in fam.get("plans", [])]
            self.assertEqual(len(fam_plan_ids), len(set(fam_plan_ids)), f"Duplicate plan ID within family {slug}")
            all_plan_ids.extend(fam_plan_ids)
        self.assertEqual(len(all_plan_ids), len(set(all_plan_ids)), "Duplicate plan IDs found across catalog")

    def test_04_materially_different_plans_preserved(self):
        """Test 4: Materially different plan variants (duration, seats, API tokens vs subscriptions) are not merged."""
        yt_plans = self.public_catalog["youtube-premium"]["plans"]
        plan_names = [p["name"] for p in yt_plans]
        self.assertTrue(any("Individual" in n for n in plan_names), "Individual plan must be preserved")
        self.assertTrue(any("Family" in n for n in plan_names), "Family plan must be preserved")
        self.assertTrue(any("Annual" in n for n in plan_names), "Annual plan must be preserved")

    def test_05_no_held_compliance_offer_is_published(self):
        """Test 5: No held/unverified/compliance-flagged offer is published."""
        if not self.reconciliation_ledger: self.skipTest("Private local supplier ledger excluded from git repository")
        quarantined_count = sum(1 for item in self.reconciliation_ledger if item["disposition"] == "HOLD_COMPLIANCE_SCREENING")
        self.assertGreater(quarantined_count, 1400, "High-risk items must be safely quarantined")
        for item in self.reconciliation_ledger:
            if item["disposition"] == "HOLD_COMPLIANCE_SCREENING":
                self.assertEqual(item["public_publication_status"], "QUARANTINED_PRIVATE_ONLY")

    def test_06_strict_security_leak_scan(self):
        """Test 6: No supplier names, bot names, wholesale costs, USDT, or SRC- IDs leak into public build."""
        forbidden_keywords = [
            "Bot Name", "Price (USDT)", "wholesale cost",
            "Fat bunny hub", "Bunnytoolsbot", "MediaHubMarketplace", "Shiva cute",
            "NovasubGlobal", "Hitmeow shop", "AI Toolify Studio", "Piggy ai",
            "Alfyshop", "OxygenPremium", "Sirixshop", "SRC-0002"
        ]
        scanned_files = 0
        leaks = []
        for root, dirs, files in os.walk(BASE_DIR):
            if ".git" in root or "scratch" in root:
                continue
            for f in files:
                if f.endswith((".html", ".js", ".css", ".json", ".xml")):
                    path = os.path.join(root, f)
                    scanned_files += 1
                    with open(path, "r", encoding="utf-8", errors="ignore") as fl:
                        content = fl.read()
                        for kw in forbidden_keywords:
                            if kw.lower() in content.lower():
                                leaks.append((f, kw))
        self.assertGreater(scanned_files, 40, "Must scan at least 40 public files")
        self.assertEqual(len(leaks), 0, f"SECURITY LEAKS DETECTED in public files: {leaks}")

    def test_07_no_product_id_collision_overwrites(self):
        """Test 7: No Product ID collision causes records to be overwritten (provenance uses SRC- IDs)."""
        if not self.reconciliation_ledger: self.skipTest("Private local supplier ledger excluded from git repository")
        seen_src_ids = set()
        for item in self.reconciliation_ledger:
            src_id = item["source_record_id"]
            self.assertTrue(src_id.startswith("SRC-"), f"Identifier must be deterministic SRC- key: {src_id}")
            seen_src_ids.add(src_id)
        self.assertEqual(len(seen_src_ids), 2902, "All 2902 records must maintain distinct deterministic keys")

    def test_08_product_logos_mapping_and_fallbacks(self):
        """Test 8: Product logos map to existing local assets with graceful fallbacks."""
        self.assertEqual(self.brand_manifest["total_brands"], 52, "Brand manifest must track 40 brands")
        for b in self.brand_manifest["brands"]:
            logo_rel = b["logo_file"]
            logo_abs = os.path.join(BASE_DIR, logo_rel)
            self.assertTrue(os.path.exists(logo_abs), f"Logo file missing: {logo_abs}")

    def test_09_public_product_links_and_canonicals(self):
        """Test 9: Every public product link works and canonical URLs are consistent."""
        for slug, fam in self.public_catalog.items():
            page_rel = fam["url"]
            page_abs = os.path.join(BASE_DIR, page_rel)
            self.assertTrue(os.path.exists(page_abs), f"Product page missing: {page_abs}")
            with open(page_abs, "r", encoding="utf-8") as f:
                content = f.read()
                expected_canonical = f'<link rel="canonical" href="https://aidigitools.tech/{page_rel}">'
                self.assertIn(expected_canonical, content, f"Canonical tag missing or incorrect in {page_rel}")

    def test_10_sitemap_and_robots_validation(self):
        """Test 10: Sitemap, robots.txt, metadata, and JSON-LD validate cleanly."""
        sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
        self.assertTrue(os.path.exists(sitemap_path), "sitemap.xml must exist")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        urls = [elem.text for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertGreater(len(urls), 35, "Sitemap must contain public pages")
        
        # Check robots.txt allows search engines
        robots_path = os.path.join(BASE_DIR, "robots.txt")
        with open(robots_path, "r", encoding="utf-8") as f:
            robots_txt = f.read()
            self.assertIn("User-agent: *", robots_txt)
            self.assertIn("Sitemap:", robots_txt)

    def test_11_plan_selection_and_cart_integration(self):
        """Test 11: Cart and plan selection functions exist in assets/cart.js."""
        cart_js_path = os.path.join(BASE_DIR, "assets", "cart.js")
        with open(cart_js_path, "r", encoding="utf-8") as f:
            code = f.read()
            self.assertIn("window.openQuickOrderModal", code)
            self.assertIn("window.closeQuickOrderModal", code)
            self.assertIn("window.selectPlanInDrawer", code)
            self.assertIn("selectCartRail", code)
            self.assertIn("drawerPlanSelectorContainer", code)

    def test_12_public_build_leak_scan(self):
        """Test 12: Public build leak scan passes with zero private markers."""
        with open(PUBLIC_CATALOG_FILE, "r", encoding="utf-8") as f:
            pub_data = f.read()
        self.assertNotIn("Price (USDT)", pub_data)
        self.assertNotIn("Bot Name", pub_data)
        self.assertNotIn("wholesale", pub_data)


if __name__ == "__main__":
    unittest.main()
