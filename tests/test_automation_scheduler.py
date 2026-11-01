"""
Unit Tests for Automation and Scheduling Engine (Part 17).
===========================================================
Validates:
1. Pakistan Standard Time (PKT = UTC+5) timezone and business timestamp accuracy.
2. 48-Hour publication cadence enforcement.
3. Persistent publication ledger with unique article identifiers (ART-XXX).
4. Duplicate-publication protection.
5. Run locks, concurrency prevention, and stale lock recovery.
6. API caching and retry with exponential backoff.
7. Monthly usage, token consumption, and cost tracking.
8. No-filler policy: skips publishing with transparent explanations when no topic qualifies.
9. Version control tracking and rollback support.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import datetime
from pathlib import Path
from unittest.mock import MagicMock

# Add seo-agent to sys.path
SEO_AGENT_DIR = Path(__file__).resolve().parent.parent / "seo-agent"
if str(SEO_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(SEO_AGENT_DIR))

from agent.automation_scheduler import (
    AutomationScheduler,
    get_pkt_timezone,
    get_pkt_now,
    format_pkt_timestamp,
    parse_timestamp_to_utc,
    SchedulerLockError,
    SchedulerDuplicateError,
    SchedulerRetryExhaustedError
)


class TestAutomationScheduler(unittest.TestCase):

    def setUp(self):
        """Create an isolated temporary workspace for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir)
        self.data_dir = self.workspace / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Seed initial publication ledger
        self.initial_publications = [
            {
                "article_id": "ART-001",
                "slug": "chatgpt-vs-claude",
                "title": "ChatGPT Plus vs Claude Pro: AI Shootout",
                "canonical_url": "https://aidigitools.tech/compare/chatgpt-vs-claude.html",
                "relative_url": "compare/chatgpt-vs-claude.html",
                "cluster_slug": "ai-assistants-and-llms",
                "article_type": "comparison",
                "author_slug": "abeera-farooq",
                "primary_keyword": "chatgpt plus vs claude pro",
                "published_at_pkt": "2026-10-25 10:00:00 PKT",
                "published_at_utc": "2026-10-25T05:00:00Z",
                "git_commit_hash": "b2f8a19",
                "quality_gate_passed": True,
                "status": "PUBLISHED"
            },
            {
                "article_id": "ART-002",
                "slug": "runway-vs-pika",
                "title": "Runway Gen-3 vs Pika 2.0: Shootout",
                "canonical_url": "https://aidigitools.tech/compare/runway-vs-pika.html",
                "relative_url": "compare/runway-vs-pika.html",
                "cluster_slug": "ai-video-and-audio-tools",
                "article_type": "comparison",
                "author_slug": "aidigitools-editorial",
                "primary_keyword": "runway gen 3 vs pika 2.0",
                "published_at_pkt": "2026-10-28 12:00:00 PKT",
                "published_at_utc": "2026-10-28T07:00:00Z",
                "git_commit_hash": "c4d1e23",
                "quality_gate_passed": True,
                "status": "PUBLISHED"
            }
        ]

        with open(self.data_dir / "publication_ledger.json", "w", encoding="utf-8") as f:
            json.dump({
                "ledger_version": "1.0.0",
                "business_timezone": "PKT (UTC+5)",
                "min_cadence_hours": 48.0,
                "publications": self.initial_publications
            }, f, indent=2)

        # Seed candidate topics
        self.candidate_topics = {
            "registry_version": "2.0.0",
            "candidate_topics": [
                {
                    "topic_id": "TOPIC-001",
                    "primary_keyword": "cursor ai vs github copilot",
                    "total_opportunity_score": 95,
                    "score_threshold_passed": True,
                    "recommended_action": "PUBLISH_NEW_ARTICLE",
                    "target_canonical_path": "blog/cursor-ai-vs-github-copilot-comparison.html",
                    "editorial_rationale": "High-intent developer query."
                },
                {
                    "topic_id": "TOPIC-LOW",
                    "primary_keyword": "generic thin filler topic",
                    "total_opportunity_score": 62,
                    "score_threshold_passed": False,
                    "recommended_action": "SKIP",
                    "target_canonical_path": "blog/filler-topic.html",
                    "editorial_rationale": "Low value."
                }
            ]
        }
        with open(self.data_dir / "topic_opportunity_registry.json", "w", encoding="utf-8") as f:
            json.dump(self.candidate_topics, f, indent=2)

        self.scheduler = AutomationScheduler(workspace_root=self.workspace)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_pkt_timezone_and_timestamp_accuracy(self):
        """Business reporting timestamps must be computed in Pakistan Standard Time (UTC+5)."""
        tz = get_pkt_timezone()
        self.assertIsNotNone(tz)

        now_pkt = get_pkt_now()
        self.assertIsNotNone(now_pkt.tzinfo)

        formatted = format_pkt_timestamp(now_pkt)
        self.assertTrue(formatted.endswith(" PKT"))

        # Verify UTC parsing
        parsed_utc = parse_timestamp_to_utc("2026-11-02 14:00:00 PKT")
        self.assertEqual(parsed_utc.hour, 9)  # 14:00 PKT - 5 hours = 09:00 UTC
        self.assertEqual(parsed_utc.day, 2)

    def test_48_hour_publication_cadence_enforcement(self):
        """Publishing must be blocked if less than 48 hours have elapsed since the last publication."""
        # Case A: Last published 20 hours ago -> Cadence blocked
        recent_time = parse_timestamp_to_utc("2026-10-28 12:00:00 PKT") + datetime.timedelta(hours=20)
        passed, elapsed, msg = self.scheduler.check_publication_cadence(min_hours=48.0, now_dt=recent_time)
        self.assertFalse(passed)
        self.assertAlmostEqual(elapsed, 20.0, places=1)
        self.assertIn("Cadence lock active", msg)
        self.assertIn("Minimum 48.0 hours required", msg)

        # Case B: Last published 50 hours ago -> Cadence passed
        cleared_time = parse_timestamp_to_utc("2026-10-28 12:00:00 PKT") + datetime.timedelta(hours=50)
        passed, elapsed, msg = self.scheduler.check_publication_cadence(min_hours=48.0, now_dt=cleared_time)
        self.assertTrue(passed)
        self.assertAlmostEqual(elapsed, 50.0, places=1)
        self.assertIn("Cadence gate cleared", msg)

    def test_persistent_publication_ledger_and_unique_id(self):
        """New articles must receive unique sequential ART-XXX identifiers and persist to disk."""
        entry = self.scheduler.record_publication(
            slug="cursor-vs-copilot",
            title="Cursor AI vs GitHub Copilot",
            canonical_url="https://aidigitools.tech/compare/cursor-vs-copilot.html",
            cluster_slug="ai-coding-and-development",
            article_type="comparison",
            author_slug="abeera-farooq",
            primary_keyword="cursor ai vs github copilot",
            git_commit_hash="f1e2d3c"
        )

        self.assertEqual(entry["article_id"], "ART-003")
        self.assertEqual(entry["slug"], "cursor-vs-copilot")
        self.assertEqual(entry["status"], "PUBLISHED")
        self.assertTrue(entry["published_at_pkt"].endswith(" PKT"))

        # Verify ledger persistence on disk
        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        self.assertEqual(len(ledger["publications"]), 3)
        self.assertEqual(ledger["publications"][-1]["article_id"], "ART-003")

    def test_duplicate_publication_protection(self):
        """Duplicate slugs, canonical URLs, or identical titles must be rejected."""
        # Attempt to publish already published slug
        with self.assertRaises(SchedulerDuplicateError) as ctx:
            self.scheduler.record_publication(
                slug="chatgpt-vs-claude",  # already exists as ART-001
                title="Another ChatGPT vs Claude",
                canonical_url="https://aidigitools.tech/compare/another-url.html",
                cluster_slug="ai-assistants-and-llms",
                article_type="comparison",
                author_slug="abeera-farooq",
                primary_keyword="chatgpt plus vs claude pro"
            )
        self.assertIn("already published", str(ctx.exception))

    def test_run_lock_and_stale_lock_recovery(self):
        """Run locks must prevent concurrency and automatically recover from stale locks."""
        # 1. Acquire lock
        self.assertTrue(self.scheduler.acquire_lock())
        self.assertTrue(self.scheduler.is_locked())

        # 2. Concurrent acquisition must fail
        with self.assertRaises(SchedulerLockError):
            self.scheduler.acquire_lock()

        # 3. Simulate stale lock (> 120 minutes old)
        stale_time = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=130)).isoformat()
        with open(self.scheduler.scheduler_lock_path, "w", encoding="utf-8") as f:
            json.dump({
                "pid": 99999,
                "hostname": "stale-runner",
                "locked_at_pkt": "2026-11-01 10:00:00 PKT",
                "locked_at_utc": stale_time,
                "timeout_minutes": 120
            }, f, indent=2)

        # 4. Should break stale lock and succeed
        self.assertTrue(self.scheduler.acquire_lock())

        # 5. Release lock
        self.assertTrue(self.scheduler.release_lock())
        self.assertFalse(self.scheduler.is_locked())

    def test_api_caching_and_exponential_retry(self):
        """API caching must return cached result; exponential retry must handle transient failures."""
        mock_fn = MagicMock(return_value={"tokens": 1500, "analysis": "mock analysis"})

        # First call: executes caller
        res1 = self.scheduler.get_cached_or_call("cache_key_01", mock_fn, ttl_seconds=3600)
        self.assertEqual(mock_fn.call_count, 1)

        # Second call: returns cached result without re-executing
        res2 = self.scheduler.get_cached_or_call("cache_key_01", mock_fn, ttl_seconds=3600)
        self.assertEqual(mock_fn.call_count, 1)
        self.assertEqual(res1, res2)

        # Retry with backoff: handles 2 failures then succeeds
        flaky_counter = {"attempts": 0}
        def flaky_api():
            flaky_counter["attempts"] += 1
            if flaky_counter["attempts"] < 3:
                raise ConnectionError("Transient rate limit 429")
            return "SUCCESS"

        retry_result = self.scheduler.execute_with_retry(
            flaky_api, max_retries=3, base_delay=0.01, jitter=False, retry_exceptions=(ConnectionError,)
        )
        self.assertEqual(retry_result, "SUCCESS")
        self.assertEqual(flaky_counter["attempts"], 3)

    def test_monthly_usage_and_cost_monitoring(self):
        """Monthly API token consumption and USD/PKR cost must be accurately tracked."""
        usage_record = self.scheduler.record_usage(
            operation="article_research_gemini",
            prompt_tokens=100_000,
            completion_tokens=20_000,
            model="gemini-1.5-flash"
        )

        self.assertGreater(usage_record["api_spend_usd"], 0.0)
        self.assertGreater(usage_record["api_spend_pkr"], 0.0)

        # Verify disk ledger
        with open(self.scheduler.monthly_usage_path, "r", encoding="utf-8") as f:
            usage = json.load(f)
        self.assertEqual(usage["total_api_calls"], 1)
        self.assertEqual(usage["total_prompt_tokens"], 100_000)
        self.assertEqual(usage["total_completion_tokens"], 20_000)

        # Test budget exceedance detection
        usage["total_spend_usd"] = 52.50
        usage["monthly_budget_usd"] = 50.00
        with open(self.scheduler.monthly_usage_path, "w", encoding="utf-8") as f:
            json.dump(usage, f, indent=2)

        exceeded, msg = self.scheduler.is_budget_exceeded()
        self.assertTrue(exceeded)
        self.assertIn("Monthly budget exceeded", msg)

    def test_no_filler_policy_and_skip_explanation(self):
        """If no topic qualifies or cadence is locked, publishing must be skipped with transparent reason."""
        # 1. When cadence is locked, must skip with CADENCE_LOCK_ACTIVE
        # Add a publication timestamp 10 hours ago
        recent_pkt = format_pkt_timestamp(get_pkt_now() - datetime.timedelta(hours=10))
        recent_utc = (get_pkt_now() - datetime.timedelta(hours=10)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        ledger["publications"].append({
            "article_id": "ART-RECENT",
            "slug": "recent-article",
            "title": "Recent Article",
            "published_at_pkt": recent_pkt,
            "published_at_utc": recent_utc,
            "status": "PUBLISHED"
        })
        with open(self.scheduler.publication_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        report = self.scheduler.evaluate_daily_research_check(force_cadence=False)
        self.assertEqual(report["decision"], "SKIP")
        self.assertEqual(report["reason_code"], "CADENCE_LOCK_ACTIVE")
        self.assertIn("Cadence lock active", report["explanation"])

        # 2. When cadence is forced/cleared, but topics are below 85 threshold:
        # Overwrite topic registry with only low-score topics
        with open(self.data_dir / "topic_opportunity_registry.json", "w", encoding="utf-8") as f:
            json.dump({
                "candidate_topics": [
                    {
                        "topic_id": "TOPIC-SUBPAR",
                        "primary_keyword": "low value spam",
                        "total_opportunity_score": 70,
                        "recommended_action": "PUBLISH_NEW_ARTICLE",
                        "target_canonical_path": "blog/low-value.html"
                    }
                ]
            }, f, indent=2)

        report_no_filler = self.scheduler.evaluate_daily_research_check(force_cadence=True)
        self.assertEqual(report_no_filler["decision"], "SKIP")
        self.assertEqual(report_no_filler["reason_code"], "NO_QUALIFYING_TOPIC")
        self.assertIn("do not publish filler content", report_no_filler["explanation"])

    def test_version_control_tracking_and_rollback(self):
        """Articles must support rollback marking and provide git revert command."""
        entry = self.scheduler.record_publication(
            slug="temporary-article",
            title="Temporary Article to Roll Back",
            canonical_url="https://aidigitools.tech/guides/temporary.html",
            cluster_slug="ai-assistants-and-llms",
            article_type="guide",
            author_slug="abeera-farooq",
            primary_keyword="temporary test article",
            git_commit_hash="a1b2c3d4e"
        )
        art_id = entry["article_id"]

        rollback_res = self.scheduler.rollback_article(art_id, rollback_reason="Quality audit failure")
        self.assertEqual(rollback_res["status"], "ROLLED_BACK")
        self.assertIn("git revert a1b2c3d4e", rollback_res["recommended_git_action"])

        # Verify status in persistent ledger
        with open(self.scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        rolled_back_item = next(p for p in ledger["publications"] if p["article_id"] == art_id)
        self.assertEqual(rolled_back_item["status"], "ROLLED_BACK")
        self.assertEqual(rolled_back_item["rollback_reason"], "Quality audit failure")


if __name__ == "__main__":
    unittest.main()
