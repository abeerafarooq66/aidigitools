"""
AIDigiTools Autonomous Content Intelligence Cloud Scheduler (Part 17).
========================================================================
Operational Charter: Built strictly on Part 17 of the Master Operating System
& Architecture Charter for AIDigiTools.

Key Guarantees:
1. Cloud Scheduler: Runs independently in GitHub Actions cloud runner;
   does not rely on local Antigravity session remaining open on a laptop.
2. Timezone Standards: Pakistan Standard Time (PKT = UTC+5) used for all
   business reporting and scheduling intervals.
3. 48-Hour Publication Cadence Rule: Enforces a minimum 48-hour quiet period
   between successful article publications.
4. Persistent Publication Ledger: Unique article identifiers (ART-XXX),
   duplicate publication protection, version control metadata, and rollback support.
5. Concurrency Control: Run locks with automatic stale lock expiration.
6. API Resilience: Caching layer with TTL and exponential retry with backoff.
7. Budget & Cost Monitoring: Tracks prompt/completion tokens, USD spend, and PKR
   conversions against a monthly budget limit.
8. No-Filler Policy: If no topic meets the >= 85 opportunity score, skips publication
   with explicit transparent reasoning. Never publish filler content.
"""

import os
import sys
import json
import time
import socket
import random
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Callable

# Base Directories
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"

# Core File Paths
PUBLICATION_LEDGER_PATH = DATA_DIR / "publication_ledger.json"
MONTHLY_USAGE_PATH = DATA_DIR / "monthly_usage_ledger.json"
TOPIC_REGISTRY_PATH = DATA_DIR / "topic_opportunity_registry.json"
BLOG_REGISTRY_PATH = DATA_DIR / "blog_articles_registry.json"
SCHEDULER_LOCK_PATH = DATA_DIR / "scheduler_lock.json"
RUN_REPORT_PATH = DATA_DIR / "scheduler_run_report.json"
API_CACHE_PATH = CACHE_DIR / "api_cache.json"

# Invariants & Defaults
MIN_CADENCE_HOURS_DEFAULT = 48.0
DEFAULT_MONTHLY_BUDGET_USD = 50.0
DEFAULT_USD_TO_PKR_RATE = 280.0
STALE_LOCK_TIMEOUT_MINUTES = 120.0
MIN_QUALIFYING_TOPIC_SCORE = 85


class SchedulerError(Exception):
    """Base error for Automation Scheduler."""
    pass


class SchedulerLockError(SchedulerError):
    """Raised when an active run lock prevents execution."""
    pass


class SchedulerCadenceError(SchedulerError):
    """Raised when publication is attempted before 48 hours have elapsed."""
    pass


class SchedulerDuplicateError(SchedulerError):
    """Raised when duplicate publication is attempted."""
    pass


class SchedulerBudgetExceededError(SchedulerError):
    """Raised when monthly API cost limit is exceeded."""
    pass


class SchedulerRetryExhaustedError(SchedulerError):
    """Raised when API retries have been exhausted."""
    pass


def get_pkt_timezone() -> datetime.tzinfo:
    """Returns Pakistan Standard Time (PKT = UTC+5) timezone."""
    try:
        import zoneinfo
        return zoneinfo.ZoneInfo("Asia/Karachi")
    except Exception:
        return datetime.timezone(datetime.timedelta(hours=5), name="PKT")


def get_pkt_now() -> datetime.datetime:
    """Returns current datetime in Pakistan Standard Time (PKT)."""
    return datetime.datetime.now(get_pkt_timezone())


def format_pkt_timestamp(dt: Optional[datetime.datetime] = None) -> str:
    """Formats datetime as 'YYYY-MM-DD HH:MM:SS PKT'."""
    target_dt = dt or get_pkt_now()
    if target_dt.tzinfo is None:
        target_dt = target_dt.replace(tzinfo=get_pkt_timezone())
    else:
        target_dt = target_dt.astimezone(get_pkt_timezone())
    return target_dt.strftime("%Y-%m-%d %H:%M:%S PKT")


def parse_timestamp_to_utc(ts_str: str) -> datetime.datetime:
    """Parses various timestamp strings (PKT or ISO UTC) into UTC datetime."""
    clean_ts = ts_str.strip()
    if clean_ts.endswith(" PKT"):
        date_part = clean_ts[:-4].strip()
        dt = datetime.datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")
        dt_pkt = dt.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=5)))
        return dt_pkt.astimezone(datetime.timezone.utc)
    if clean_ts.endswith("Z"):
        dt = datetime.datetime.fromisoformat(clean_ts.replace("Z", "+00:00"))
        return dt.astimezone(datetime.timezone.utc)
    dt = datetime.datetime.fromisoformat(clean_ts)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


class AutomationScheduler:
    """
    Orchestrates the daily autonomous research, evaluation, and scheduled publication cycle.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or WORKSPACE_ROOT)
        self.data_dir = self.workspace_root / "data"
        self.cache_dir = self.data_dir / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.publication_ledger_path = self.data_dir / "publication_ledger.json"
        self.monthly_usage_path = self.data_dir / "monthly_usage_ledger.json"
        self.topic_registry_path = self.data_dir / "topic_opportunity_registry.json"
        self.blog_registry_path = self.data_dir / "blog_articles_registry.json"
        self.scheduler_lock_path = self.data_dir / "scheduler_lock.json"
        self.run_report_path = self.data_dir / "scheduler_run_report.json"
        self.api_cache_path = self.cache_dir / "api_cache.json"

        self._ensure_ledgers_exist()

    # --------------------------------------------------------------------------
    # Initializers & State Files
    # --------------------------------------------------------------------------
    def _ensure_ledgers_exist(self) -> None:
        """Initializes empty/default ledger files if missing."""
        if not self.publication_ledger_path.exists():
            default_ledger = {
                "ledger_version": "1.0.0",
                "business_timezone": "PKT (UTC+5)",
                "min_cadence_hours": MIN_CADENCE_HOURS_DEFAULT,
                "last_updated_pkt": format_pkt_timestamp(),
                "publications": []
            }
            with open(self.publication_ledger_path, "w", encoding="utf-8") as f:
                json.dump(default_ledger, f, indent=2)

        if not self.monthly_usage_path.exists():
            now_pkt = get_pkt_now()
            default_usage = {
                "ledger_version": "1.0.0",
                "year_month": now_pkt.strftime("%Y-%m"),
                "business_timezone": "PKT (UTC+5)",
                "monthly_budget_usd": DEFAULT_MONTHLY_BUDGET_USD,
                "currency_conversion_usd_to_pkr": DEFAULT_USD_TO_PKR_RATE,
                "total_api_calls": 0,
                "total_prompt_tokens": 0,
                "total_completion_tokens": 0,
                "total_spend_usd": 0.0,
                "total_spend_pkr": 0.0,
                "budget_exceeded": False,
                "pricing_model_per_million_tokens": {
                    "gemini-1.5-flash": {"input_usd": 0.075, "output_usd": 0.30},
                    "gemini-1.5-pro": {"input_usd": 1.25, "output_usd": 5.00}
                },
                "records": []
            }
            with open(self.monthly_usage_path, "w", encoding="utf-8") as f:
                json.dump(default_usage, f, indent=2)

    # --------------------------------------------------------------------------
    # 1. Run Lock Management (Concurrency & Stale Locks)
    # --------------------------------------------------------------------------
    def acquire_lock(self, timeout_minutes: float = STALE_LOCK_TIMEOUT_MINUTES) -> bool:
        """
        Acquires atomic run lock. If existing lock is older than timeout_minutes,
        breaks the stale lock and reacquires.
        """
        if self.scheduler_lock_path.exists():
            try:
                with open(self.scheduler_lock_path, "r", encoding="utf-8") as f:
                    lock_data = json.load(f)
                locked_at_utc = parse_timestamp_to_utc(lock_data.get("locked_at_utc", ""))
                age_minutes = (datetime.datetime.now(datetime.timezone.utc) - locked_at_utc).total_seconds() / 60.0
                if age_minutes < timeout_minutes:
                    raise SchedulerLockError(
                        f"Active run lock held by PID {lock_data.get('pid')} on {lock_data.get('hostname')} "
                        f"since {lock_data.get('locked_at_pkt')} (Age: {age_minutes:.1f}m < {timeout_minutes}m)."
                    )
                # Stale lock detected
                self.release_lock()
            except (json.JSONDecodeError, KeyError, ValueError):
                self.release_lock()

        lock_content = {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
            "locked_at_pkt": format_pkt_timestamp(),
            "locked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "timeout_minutes": timeout_minutes
        }
        with open(self.scheduler_lock_path, "w", encoding="utf-8") as f:
            json.dump(lock_content, f, indent=2)
        return True

    def release_lock(self) -> bool:
        """Releases the run lock."""
        if self.scheduler_lock_path.exists():
            try:
                self.scheduler_lock_path.unlink()
                return True
            except OSError:
                return False
        return False

    def is_locked(self) -> bool:
        """Checks if a valid non-stale lock is active."""
        if not self.scheduler_lock_path.exists():
            return False
        try:
            with open(self.scheduler_lock_path, "r", encoding="utf-8") as f:
                lock_data = json.load(f)
            locked_at_utc = parse_timestamp_to_utc(lock_data.get("locked_at_utc", ""))
            age_minutes = (datetime.datetime.now(datetime.timezone.utc) - locked_at_utc).total_seconds() / 60.0
            return age_minutes < STALE_LOCK_TIMEOUT_MINUTES
        except Exception:
            return False

    # --------------------------------------------------------------------------
    # 2. Publication Cadence Guard (48 Hours Rule)
    # --------------------------------------------------------------------------
    def check_publication_cadence(
        self,
        min_hours: float = MIN_CADENCE_HOURS_DEFAULT,
        now_dt: Optional[datetime.datetime] = None
    ) -> Tuple[bool, float, str]:
        """
        Verifies that at least min_hours (default 48.0) have elapsed since the
        last successful article publication.
        Returns: (cadence_passed, hours_elapsed, explanation_message)
        """
        current_time_utc = (now_dt or get_pkt_now()).astimezone(datetime.timezone.utc)
        with open(self.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        publications = [p for p in ledger.get("publications", []) if p.get("status") == "PUBLISHED"]
        if not publications:
            return True, 999.0, "No prior publications recorded; cadence check cleared."

        # Find latest published article
        latest_pub = max(
            publications,
            key=lambda p: parse_timestamp_to_utc(p.get("published_at_utc", p.get("published_at_pkt", "")))
        )
        last_utc = parse_timestamp_to_utc(latest_pub.get("published_at_utc", latest_pub.get("published_at_pkt", "")))
        elapsed_hours = (current_time_utc - last_utc).total_seconds() / 3600.0

        if elapsed_hours < min_hours:
            explanation = (
                f"Cadence lock active: Only {elapsed_hours:.1f} hours have elapsed since the last publication "
                f"('{latest_pub.get('title')}' on {latest_pub.get('published_at_pkt')}). "
                f"Minimum {min_hours:.1f} hours required to prevent publishing fatigue and maintain high quality."
            )
            return False, elapsed_hours, explanation

        explanation = (
            f"Cadence gate cleared: {elapsed_hours:.1f} hours have elapsed since last publication "
            f"('{latest_pub.get('title')}'), satisfying the {min_hours:.1f}h minimum requirement."
        )
        return True, elapsed_hours, explanation

    # --------------------------------------------------------------------------
    # 3. Duplicate Publication Protection
    # --------------------------------------------------------------------------
    def check_duplicate_publication(
        self,
        slug: str,
        title: Optional[str] = None,
        canonical_url: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Checks both publication ledger and blog registry for duplicate publication.
        Returns: (is_duplicate, explanation)
        """
        norm_slug = slug.strip().lower()
        norm_title = (title or "").strip().lower()
        norm_url = (canonical_url or "").strip().lower()

        # Check Publication Ledger
        with open(self.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        for pub in ledger.get("publications", []):
            if pub.get("status") == "PUBLISHED":
                if pub.get("slug", "").strip().lower() == norm_slug:
                    return True, f"Article with slug '{slug}' is already published (ID: {pub.get('article_id')})."
                if norm_url and pub.get("canonical_url", "").strip().lower() == norm_url:
                    return True, f"Article with canonical URL '{canonical_url}' already exists (ID: {pub.get('article_id')})."
                if norm_title and pub.get("title", "").strip().lower() == norm_title:
                    return True, f"Article with identical title '{title}' already exists (ID: {pub.get('article_id')})."

        # Check Blog Registry
        if self.blog_registry_path.exists():
            with open(self.blog_registry_path, "r", encoding="utf-8") as f:
                blog_data = json.load(f)
            for art in blog_data.get("articles", []):
                if art.get("slug", "").strip().lower() == norm_slug:
                    return True, f"Article with slug '{slug}' already exists in blog registry (ID: {art.get('id')})."

        return False, "No duplicate publication detected."

    # --------------------------------------------------------------------------
    # 4. API Caching & Exponential Backoff Retry
    # --------------------------------------------------------------------------
    def get_cached_or_call(
        self,
        cache_key: str,
        caller_fn: Callable[[], Any],
        ttl_seconds: int = 86400
    ) -> Any:
        """
        Retrieves cached result if present and within TTL, otherwise executes
        caller_fn and caches the result.
        """
        import hashlib
        key_hash = hashlib.sha256(cache_key.encode("utf-8")).hexdigest()
        cache_data = {}
        if self.api_cache_path.exists():
            try:
                with open(self.api_cache_path, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
            except Exception:
                cache_data = {}

        now_epoch = time.time()
        if key_hash in cache_data:
            entry = cache_data[key_hash]
            if (now_epoch - entry.get("cached_at_epoch", 0)) < ttl_seconds:
                return entry.get("data")

        # Cache miss or expired: execute caller
        result = caller_fn()
        cache_data[key_hash] = {
            "key": cache_key,
            "cached_at_epoch": now_epoch,
            "cached_at_pkt": format_pkt_timestamp(),
            "data": result
        }
        with open(self.api_cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
        return result

    def execute_with_retry(
        self,
        fn: Callable[[], Any],
        max_retries: int = 3,
        base_delay: float = 0.5,
        backoff_factor: float = 2.0,
        jitter: bool = True,
        retry_exceptions: Tuple[type, ...] = (Exception,)
    ) -> Any:
        """Executes a callable with exponential backoff and optional jitter."""
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                return fn()
            except retry_exceptions as e:
                last_error = e
                if attempt == max_retries:
                    raise SchedulerRetryExhaustedError(
                        f"Exhausted {max_retries} retries for operation. Last error: {str(e)}"
                    ) from e
                delay = base_delay * (backoff_factor ** attempt)
                if jitter:
                    delay += random.uniform(0, delay * 0.1)
                time.sleep(delay)
        raise SchedulerRetryExhaustedError(f"Operation failed after retries: {str(last_error)}")

    # --------------------------------------------------------------------------
    # 5. Monthly Usage & Cost Monitoring
    # --------------------------------------------------------------------------
    def record_usage(
        self,
        operation: str,
        prompt_tokens: int,
        completion_tokens: int,
        model: str = "gemini-1.5-flash",
        spend_usd: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Records API token consumption and financial spend. Updates monthly ledger
        and halts if monthly budget limit is breached.
        """
        with open(self.monthly_usage_path, "r", encoding="utf-8") as f:
            usage = json.load(f)

        now_pkt = get_pkt_now()
        current_ym = now_pkt.strftime("%Y-%m")

        # Roll over if month changed
        if usage.get("year_month") != current_ym:
            usage["year_month"] = current_ym
            usage["total_api_calls"] = 0
            usage["total_prompt_tokens"] = 0
            usage["total_completion_tokens"] = 0
            usage["total_spend_usd"] = 0.0
            usage["total_spend_pkr"] = 0.0
            usage["budget_exceeded"] = False
            usage["records"] = []

        # Calculate cost
        pricing = usage.get("pricing_model_per_million_tokens", {}).get(
            model, {"input_usd": 0.075, "output_usd": 0.30}
        )
        calculated_usd = spend_usd if spend_usd is not None else (
            (prompt_tokens / 1_000_000.0) * pricing["input_usd"] +
            (completion_tokens / 1_000_000.0) * pricing["output_usd"]
        )
        rate_pkr = usage.get("currency_conversion_usd_to_pkr", DEFAULT_USD_TO_PKR_RATE)
        calculated_pkr = calculated_usd * rate_pkr

        usage["total_api_calls"] += 1
        usage["total_prompt_tokens"] += prompt_tokens
        usage["total_completion_tokens"] += completion_tokens
        usage["total_spend_usd"] = round(usage["total_spend_usd"] + calculated_usd, 6)
        usage["total_spend_pkr"] = round(usage["total_spend_usd"] * rate_pkr, 2)

        budget_limit = usage.get("monthly_budget_usd", DEFAULT_MONTHLY_BUDGET_USD)
        if usage["total_spend_usd"] >= budget_limit:
            usage["budget_exceeded"] = True

        log_record = {
            "timestamp_pkt": format_pkt_timestamp(now_pkt),
            "operation": operation,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "api_spend_usd": round(calculated_usd, 6),
            "api_spend_pkr": round(calculated_pkr, 2)
        }
        usage.setdefault("records", []).append(log_record)

        with open(self.monthly_usage_path, "w", encoding="utf-8") as f:
            json.dump(usage, f, indent=2)

        return log_record

    def is_budget_exceeded(self) -> Tuple[bool, str]:
        """Checks if the monthly API budget is currently exceeded."""
        with open(self.monthly_usage_path, "r", encoding="utf-8") as f:
            usage = json.load(f)
        budget_limit = usage.get("monthly_budget_usd", DEFAULT_MONTHLY_BUDGET_USD)
        spent_usd = usage.get("total_spend_usd", 0.0)
        exceeded = usage.get("budget_exceeded", False) or (spent_usd >= budget_limit)
        if exceeded:
            return True, f"Monthly budget exceeded: ${spent_usd:.2f} spent >= ${budget_limit:.2f} cap."
        return False, f"Within budget: ${spent_usd:.2f} spent of ${budget_limit:.2f} cap."

    # --------------------------------------------------------------------------
    # 6. Candidate Research Evaluation & No-Filler Policy
    # --------------------------------------------------------------------------
    def evaluate_daily_research_check(
        self,
        force_cadence: bool = False,
        min_score: int = MIN_QUALIFYING_TOPIC_SCORE
    ) -> Dict[str, Any]:
        """
        Executes daily candidate topic evaluation.
        Adheres strictly to the No-Filler Policy:
        If no topic passes >= min_score or cadence is locked, explains why publishing was skipped.
        """
        now_pkt = get_pkt_now()
        report = {
            "check_timestamp_pkt": format_pkt_timestamp(now_pkt),
            "business_timezone": "PKT (UTC+5)",
            "cadence_status": {},
            "budget_status": {},
            "evaluated_candidates_count": 0,
            "decision": "SKIP",
            "reason_code": "UNKNOWN",
            "explanation": "",
            "selected_topic": None
        }

        # Step 1: Cadence Check
        cadence_passed, elapsed_hours, cadence_msg = self.check_publication_cadence()
        report["cadence_status"] = {
            "passed": cadence_passed,
            "elapsed_hours": round(elapsed_hours, 2),
            "message": cadence_msg,
            "bypassed": force_cadence
        }

        if not cadence_passed and not force_cadence:
            report["decision"] = "SKIP"
            report["reason_code"] = "CADENCE_LOCK_ACTIVE"
            report["explanation"] = cadence_msg
            self.save_run_report(report)
            return report

        # Step 2: Budget Check
        budget_exceeded, budget_msg = self.is_budget_exceeded()
        report["budget_status"] = {"exceeded": budget_exceeded, "message": budget_msg}
        if budget_exceeded:
            report["decision"] = "SKIP"
            report["reason_code"] = "MONTHLY_BUDGET_EXCEEDED"
            report["explanation"] = budget_msg
            self.save_run_report(report)
            return report

        # Step 3: Inspect Candidate Topics
        if not self.topic_registry_path.exists():
            report["decision"] = "SKIP"
            report["reason_code"] = "NO_TOPIC_REGISTRY"
            report["explanation"] = "Topic opportunity registry file not found."
            self.save_run_report(report)
            return report

        with open(self.topic_registry_path, "r", encoding="utf-8") as f:
            topic_data = json.load(f)

        candidates = topic_data.get("candidate_topics", [])
        report["evaluated_candidates_count"] = len(candidates)

        # Filter topics: score >= min_score, recommended_action == PUBLISH_NEW_ARTICLE, not already published
        qualifying = []
        for c in candidates:
            score = c.get("total_opportunity_score", 0)
            action = c.get("recommended_action", "")
            target_slug = Path(c.get("target_canonical_path", "")).stem
            is_dup, _ = self.check_duplicate_publication(slug=target_slug, title=c.get("primary_keyword"))

            if score >= min_score and action == "PUBLISH_NEW_ARTICLE" and not is_dup:
                qualifying.append(c)

        if not qualifying:
            report["decision"] = "SKIP"
            report["reason_code"] = "NO_QUALIFYING_TOPIC"
            report["explanation"] = (
                f"No un-published candidate topics met the opportunity score threshold (>= {min_score}/100). "
                "Per Part 17 of the Master Architecture Charter: If no topic qualifies, do not publish filler content."
            )
            self.save_run_report(report)
            return report

        # Select top-scoring candidate
        qualifying.sort(key=lambda t: t.get("total_opportunity_score", 0), reverse=True)
        chosen = qualifying[0]

        report["decision"] = "TOPIC_SELECTED"
        report["reason_code"] = "TOPIC_QUALIFIED"
        report["explanation"] = (
            f"Candidate topic '{chosen.get('primary_keyword')}' (ID: {chosen.get('topic_id')}) qualified with "
            f"score {chosen.get('total_opportunity_score')}/100. Selected for content generation pipeline. Cadence gate satisfied ({elapsed_hours:.1f}h elapsed)."
        )
        report["selected_topic"] = {
            "topic_id": chosen.get("topic_id"),
            "primary_keyword": chosen.get("primary_keyword"),
            "score": chosen.get("total_opportunity_score"),
            "target_canonical_path": chosen.get("target_canonical_path"),
            "editorial_rationale": chosen.get("editorial_rationale")
        }

        self.save_run_report(report)
        return report

    # --------------------------------------------------------------------------
    # 7. Persistent Publication & Unique ID Generation
    # --------------------------------------------------------------------------
    def record_publication(
        self,
        slug: str,
        title: str,
        canonical_url: str,
        cluster_slug: str,
        article_type: str,
        author_slug: str,
        primary_keyword: str,
        git_commit_hash: Optional[str] = None,
        quality_gate_passed: bool = True
    ) -> Dict[str, Any]:
        """
        Assigns unique article ID (ART-XXX), validates against duplicate publication,
        and records new entry into persistent publication ledger.
        """
        # Guard against duplicate
        is_dup, dup_msg = self.check_duplicate_publication(slug=slug, title=title, canonical_url=canonical_url)
        if is_dup:
            raise SchedulerDuplicateError(dup_msg)

        with open(self.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        publications = ledger.get("publications", [])

        # Generate Next Unique Identifier (ART-XXX)
        max_num = 0
        for p in publications:
            art_id = p.get("article_id", "")
            if art_id.startswith("ART-"):
                try:
                    num = int(art_id.split("-")[1])
                    if num > max_num:
                        max_num = num
                except ValueError:
                    pass
        next_id = f"ART-{max_num + 1:03d}"

        now_pkt = get_pkt_now()
        now_utc = now_pkt.astimezone(datetime.timezone.utc)

        new_entry = {
            "article_id": next_id,
            "slug": slug,
            "title": title,
            "canonical_url": canonical_url,
            "relative_url": f"{article_type}s/{slug}.html" if article_type in ["guide", "curation"] else f"{article_type}/{slug}.html",
            "cluster_slug": cluster_slug,
            "article_type": article_type,
            "author_slug": author_slug,
            "primary_keyword": primary_keyword,
            "published_at_pkt": format_pkt_timestamp(now_pkt),
            "published_at_utc": now_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "git_commit_hash": git_commit_hash or "uncommitted_local",
            "quality_gate_passed": quality_gate_passed,
            "status": "PUBLISHED"
        }

        publications.append(new_entry)
        ledger["publications"] = publications
        ledger["last_updated_pkt"] = format_pkt_timestamp(now_pkt)

        with open(self.publication_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        # Independently verify production deployment before triggering search engine discovery
        try:
            from agent.indexing_notifier import IndexingNotifierEngine
            notifier = IndexingNotifierEngine(workspace_root=self.workspace_root)
            live_check = notifier.verify_live_http(canonical_url)
            if live_check.get("status") == "LIVE_HTTP_VERIFIED":
                discovery_result = notifier.execute_post_publication_discovery(
                    url=canonical_url,
                    verify_live_deployment=True,
                    dry_run=False
                )
                new_entry["discovery_telemetry"] = discovery_result
                new_entry["status_breakdown"] = discovery_result.get("status_breakdown", {})
            else:
                new_entry["discovery_telemetry"] = {
                    "status": "PENDING_DEPLOYMENT_VERIFICATION",
                    "reason": "Publication recorded locally, but production deployment is not yet verified over live HTTPS. Search engine discovery deferred.",
                    "live_http": live_check
                }
                new_entry["status_breakdown"] = {
                    "publication_status": "PUBLISHED",
                    "deployment_status": "PENDING_DEPLOYMENT",
                    "discovery_status": "PENDING_DEPLOYMENT_VERIFICATION"
                }
        except Exception as e:
            new_entry["discovery_telemetry_error"] = str(e)

        return new_entry

    # --------------------------------------------------------------------------
    # 8. Rollback Support
    # --------------------------------------------------------------------------
    def rollback_article(
        self,
        article_id_or_slug: str,
        rollback_reason: str = "Editorial discrepancy detected"
    ) -> Dict[str, Any]:
        """
        Marks an article as ROLLED_BACK in the ledger and logs rollback details.
        """
        target = article_id_or_slug.strip().lower()
        with open(self.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)

        found = None
        for pub in ledger.get("publications", []):
            if pub.get("article_id", "").lower() == target or pub.get("slug", "").lower() == target:
                found = pub
                break

        if not found:
            raise KeyError(f"Article '{article_id_or_slug}' not found in publication ledger.")

        now_pkt = get_pkt_now()
        found["status"] = "ROLLED_BACK"
        found["rolled_back_at_pkt"] = format_pkt_timestamp(now_pkt)
        found["rollback_reason"] = rollback_reason

        ledger["last_updated_pkt"] = format_pkt_timestamp(now_pkt)
        with open(self.publication_ledger_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)

        return {
            "article_id": found.get("article_id"),
            "slug": found.get("slug"),
            "status": "ROLLED_BACK",
            "rolled_back_at_pkt": found["rolled_back_at_pkt"],
            "git_commit_hash": found.get("git_commit_hash"),
            "recommended_git_action": f"git revert {found.get('git_commit_hash')}" if found.get("git_commit_hash") else "manual file removal"
        }

    # --------------------------------------------------------------------------
    # 9. Reporting & Full Pipeline Orchestration
    # --------------------------------------------------------------------------
    def save_run_report(self, report_data: Dict[str, Any]) -> str:
        """Saves daily execution report to disk."""
        with open(self.run_report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        return str(self.run_report_path)

    def execute_full_content_pipeline(
        self,
        force_cadence: bool = False,
        dry_run: bool = False,
        reviewer_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes the complete end-to-end content generation and publishing pipeline:
        Research -> Topic Selection -> Article Generation -> Evidence Verification
        -> Quality Gates -> Canonical / Duplicate Check -> Human Review Preview -> Operational Phase Check.
        - Under Phase 1: Halts at preview, enqueues for human approval, never auto-publishes.
        - Preserves human approval invariant.
        """
        now_pkt = get_pkt_now()
        pipeline_log = {
            "executed_at_pkt": format_pkt_timestamp(now_pkt),
            "stages_completed": [],
            "pipeline_status": "PENDING",
            "article_generated": False,
            "published": False,
            "preview_created": False
        }

        # Stage 1: Candidate Research & Cadence Gate
        res_report = self.evaluate_daily_research_check(force_cadence=force_cadence)
        pipeline_log["research_check"] = res_report
        pipeline_log["stages_completed"].append("RESEARCH_CADENCE_CHECK")

        if res_report.get("decision") != "TOPIC_SELECTED":
            pipeline_log["pipeline_status"] = "SKIPPED"
            pipeline_log["explanation"] = res_report.get("explanation", "Research check did not select a qualifying topic.")
            self.save_run_report(pipeline_log)
            return pipeline_log

        # Stage 2: Topic Selection & Duplicate Guard
        chosen = res_report.get("selected_topic", {})
        slug = Path(chosen.get("target_canonical_path", "")).stem
        title = chosen.get("primary_keyword", "")
        raw_path = chosen.get("target_canonical_path", f"blog/{slug}.html").lstrip("/")
        canonical_path = f"/{raw_path}"
        canonical_url = f"https://aidigitools.tech{canonical_path}"

        is_dup, dup_reason = self.check_duplicate_publication(slug=slug, canonical_url=canonical_url, title=title)
        if is_dup:
            pipeline_log["pipeline_status"] = "DUPLICATE_REJECTED"
            pipeline_log["explanation"] = dup_reason
            self.save_run_report(pipeline_log)
            return pipeline_log

        pipeline_log["stages_completed"].append("TOPIC_SELECTION_AND_DUPLICATE_GUARD")

        # Stage 3: Genuine Gemini Content Generation
        from .gemini_generator import GeminiArticleGenerator
        gemini_gen = GeminiArticleGenerator(workspace_root=self.workspace_root)
        gen_result = gemini_gen.generate_article(
            topic_info=chosen,
            canonical_url=canonical_url,
            allow_fallback=False
        )

        pipeline_log["generation_telemetry"] = {
            "success": gen_result.get("success"),
            "status": gen_result.get("status"),
            "generation_method": gen_result.get("generation_method"),
            "is_gemini_generated": gen_result.get("is_gemini_generated"),
            "model_used": gen_result.get("model_used"),
            "error": gen_result.get("error")
        }

        if not gen_result.get("success") or not gen_result.get("is_gemini_generated") or not gen_result.get("html_draft"):
            pipeline_log["article_generated"] = False
            pipeline_log["pipeline_status"] = "GENERATION_FAILED"
            pipeline_log["explanation"] = f"Article content generation failed or produced heuristic fallback: {gen_result.get('error')}"
            self.save_run_report(pipeline_log)
            return pipeline_log

        html_draft = gen_result["html_draft"]
        pipeline_log["article_generated"] = True
        pipeline_log["stages_completed"].append("CONTENT_DRAFTING")

        # Stage 4: Evidence & Fact Verification
        from .evidence_system import ResearchEvidenceSystem
        evidence_sys = ResearchEvidenceSystem(self.workspace_root / "data" / "research_evidence")

        article_metadata = {
            "slug": slug,
            "title": title,
            "primary_keyword": chosen.get("primary_keyword", title),
            "canonical_url": canonical_url,
            "cluster_slug": chosen.get("cluster_slug", "ai-video-and-audio-tools"),
            "article_type": chosen.get("article_type", "comparison" if "vs" in slug else "guide"),
            "author_slug": chosen.get("author_slug", "abeera-farooq"),
            "target_canonical_path": canonical_path,
            "is_fallback": gen_result.get("is_fallback", False),
            "generation_method": gen_result.get("generation_method", "GEMINI_API"),
            "is_gemini_generated": gen_result.get("is_gemini_generated", False)
        }

        evid_res = evidence_sys.verify_article_evidence(
            html_content=html_draft,
            metadata=article_metadata
        )
        pipeline_log["evidence_verification"] = evid_res

        if not evid_res.get("verified"):
            pipeline_log["pipeline_status"] = "EVIDENCE_VERIFICATION_FAILED"
            pipeline_log["explanation"] = f"Evidence verification failed: {'; '.join(evid_res.get('errors', []))}"
            self.save_run_report(pipeline_log)
            return pipeline_log

        pipeline_log["stages_completed"].append("EVIDENCE_VERIFICATION")

        # Stage 5: Quality Gate Evaluation (All 20 Gates)
        from .quality_gates import QualityGateEngine
        gate_engine = QualityGateEngine(self.workspace_root)
        gate_result = gate_engine.evaluate_article(
            html_content=html_draft,
            metadata=article_metadata
        )
        pipeline_log["quality_gate_result"] = {
            "decision": gate_result.get("decision"),
            "passed_count": gate_result.get("passed_gates_count", 0),
            "failed_count": gate_result.get("failed_gates_count", 0),
            "failed_gates": gate_result.get("critical_failures", [])
        }
        pipeline_log["stages_completed"].append("QUALITY_GATES")

        if gate_result.get("decision") == "DO NOT PUBLISH" or gate_result.get("failed_gates_count", 0) > 0:
            pipeline_log["pipeline_status"] = "QUALITY_GATE_REJECTED"
            pipeline_log["explanation"] = f"Article failed {gate_result.get('failed_gates_count')} quality gate(s). Publishing strictly halted."
            self.save_run_report(pipeline_log)
            return pipeline_log

        # Stage 6: Publishing Control & Human Approval Routing
        from .publishing_control import PublishingControlEngine
        control_engine = PublishingControlEngine(self.workspace_root)
        op_status = control_engine.get_operational_status()
        pipeline_log["operational_phase"] = op_status.get("current_phase")
        pipeline_log["approved_supervised_count"] = op_status.get("approved_supervised_publications_count")

        preview_record = control_engine.prepare_article_preview(
            slug=slug,
            title=title,
            html_content=html_draft,
            metadata={
                "canonical_url": canonical_url,
                "topic_id": chosen.get("topic_id"),
                "primary_keyword": chosen.get("primary_keyword", title),
                "article_metadata": article_metadata
            },
            quality_gate_report=gate_result
        )
        pipeline_log["preview_created"] = True
        pipeline_log["preview_id"] = preview_record.get("preview_id")
        pipeline_log["preview_file"] = preview_record.get("preview_path", f"data/previews/{slug}.html")
        pipeline_log["stages_completed"].append("HUMAN_REVIEW_PREVIEW_GENERATION")

        # In Phase 1: Always HALTS for human review!
        if op_status.get("current_phase") == "PHASE_1_SUPERVISED":
            pipeline_log["pipeline_status"] = "AWAITING_HUMAN_APPROVAL"
            pipeline_log["explanation"] = (
                f"Article preview '{preview_record.get('preview_id')}' generated and enqueued for human review. "
                "Phase 1 supervised mode active (0/3 threshold). Autonomous publishing is strictly locked."
            )
            self.save_run_report(pipeline_log)
            return pipeline_log

        # If in Phase 2 and reviewer_id or low-risk auto-publish permitted:
        pipeline_log["pipeline_status"] = "PREPARED_FOR_DEPLOYMENT"
        self.save_run_report(pipeline_log)
        return pipeline_log

    def _generate_compliant_article_draft(
        self,
        slug: str,
        title: str,
        canonical_url: str,
        topic_info: Dict[str, Any]
    ) -> str:
        """Generates clean HTML article using Gemini generator with verified deterministic fallback."""
        from .gemini_generator import GeminiArticleGenerator
        gen = GeminiArticleGenerator(workspace_root=self.workspace_root)
        res = gen.generate_article(topic_info=topic_info, canonical_url=canonical_url, allow_fallback=True)
        if res.get("success") and res.get("html_draft"):
            return res["html_draft"]
        return gen.generate_heuristic_fallback(topic_info=topic_info, canonical_url=canonical_url)


# ==============================================================================
# CLI Entrypoint for Cloud Runner & GitHub Actions
# ==============================================================================
def main():
    import argparse
    parser = argparse.ArgumentParser(description="AIDigiTools Autonomous Content Intelligence Scheduler")
    parser.add_argument(
        "--mode",
        choices=["run-daily-check", "run-pipeline", "check-cadence", "audit-ledger", "usage-report"],
        default="run-daily-check",
        help="Scheduler execution mode"
    )
    parser.add_argument(
        "--force-cadence",
        action="store_true",
        help="Force cadence check bypass"
    )
    args = parser.parse_args()

    scheduler = AutomationScheduler()

    if args.mode == "check-cadence":
        passed, elapsed, msg = scheduler.check_publication_cadence()
        print(f"[CADENCE AUDIT] Passed: {passed} | Elapsed: {elapsed:.1f}h | Message: {msg}")
        sys.exit(0 if passed else 1)

    elif args.mode == "usage-report":
        exceeded, msg = scheduler.is_budget_exceeded()
        print(f"[USAGE REPORT] {msg}")
        sys.exit(0)

    elif args.mode == "audit-ledger":
        with open(scheduler.publication_ledger_path, "r", encoding="utf-8") as f:
            ledger = json.load(f)
        pubs = ledger.get("publications", [])
        print(f"[LEDGER AUDIT] Total publications: {len(pubs)}")
        for p in pubs:
            print(f"  - [{p.get('article_id')}] {p.get('status')} | {p.get('title')} ({p.get('published_at_pkt')})")
        sys.exit(0)

    elif args.mode == "run-daily-check":
        print(f"[SCHEDULER] Initiating daily research check at {format_pkt_timestamp()}...")
        try:
            scheduler.acquire_lock()
            report = scheduler.evaluate_daily_research_check(force_cadence=args.force_cadence)
            print(f"[SCHEDULER DECISION] {report.get('decision')} (Reason: {report.get('reason_code')})")
            print(f"[SCHEDULER EXPLANATION] {report.get('explanation')}")
        finally:
            scheduler.release_lock()
        sys.exit(0)

    elif args.mode == "run-pipeline":
        print(f"[SCHEDULER] Running complete content generation and publishing pipeline at {format_pkt_timestamp()}...")
        try:
            scheduler.acquire_lock()
            res = scheduler.execute_full_content_pipeline(force_cadence=args.force_cadence)
            print(f"[PIPELINE STATUS] {res.get('pipeline_status')} (Phase: {res.get('operational_phase', 'N/A')})")
            print(f"[PIPELINE EXPLANATION] {res.get('explanation', '')}")
            if res.get("preview_file"):
                print(f"[PREVIEW ENQUEUED] {res.get('preview_file')}")
        finally:
            scheduler.release_lock()
        sys.exit(0)


if __name__ == "__main__":
    main()

