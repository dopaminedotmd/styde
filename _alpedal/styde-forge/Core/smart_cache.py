"""
Smart response cache for Styde Forge.
Optimized: content-hash keys for eval/teacher (same output = same result).

Cache key: hash(model + prompt + temperature + rubric_id)
Content-hash mode: hash(model + content_hash + temperature + rubric_id)
  ── evals of identical output text hit cache regardless of prompt framing
TTL: 24h default, configurable per blueprint
Invalidation: blueprint version bump clears cache for that blueprint
Store: SQLite at 99_INDEXES/cache.db
"""
import hashlib
import sqlite3
import threading
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
CACHE_DB = FORGE_ROOT / "99_INDEXES" / "cache.db"
DEFAULT_TTL_SECONDS = 86400  # 24 hours

_lock = threading.Lock()


def _get_db() -> sqlite3.Connection:
    """Get or create the cache database."""
    CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(CACHE_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            cache_key TEXT PRIMARY KEY,
            model TEXT NOT NULL,
            prompt_hash TEXT NOT NULL,
            response TEXT NOT NULL,
            blueprint TEXT,
            blueprint_version TEXT,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            hit_count INTEGER DEFAULT 0,
            token_savings INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_cache_blueprint ON cache(blueprint)
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_cache_expires ON cache(expires_at)
    """)
    conn.commit()
    return conn


def _make_key(
    model: str,
    prompt: str,
    temperature: float = 0.1,
    rubric_id: str = "",
    content_hash: str = "",
) -> str:
    """
    Generate deterministic cache key.

    When content_hash is provided (eval/teacher mode), uses content_hash
    instead of full prompt. This means identical agent outputs get cache
    hits regardless of prompt framing differences.
    """
    if content_hash:
        raw = f"{model}|content:{content_hash}|{temperature}|{rubric_id}"
    else:
        raw = f"{model}|{prompt}|{temperature}|{rubric_id}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def get(
    model: str,
    prompt: str,
    temperature: float = 0.1,
    rubric_id: str = "",
    blueprint: str = "",
    content_hash: str = "",
) -> Optional[str]:
    """
    Get cached response. Returns None on miss or expired.

    content_hash: if provided, keys on content identity instead of full prompt.
                  Use for eval/teacher calls where same output = same result.
    """
    key = _make_key(model, prompt, temperature, rubric_id, content_hash)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with _lock:
        conn = _get_db()
        try:
            row = conn.execute(
                "SELECT response, expires_at, blueprint_version FROM cache WHERE cache_key = ?",
                (key,),
            ).fetchone()

            if row is None:
                return None

            response, expires_at, stored_version = row

            # Check TTL
            if expires_at < now:
                conn.execute("DELETE FROM cache WHERE cache_key = ?", (key,))
                conn.commit()
                return None

            # Check blueprint version invalidation
            if blueprint:
                current_version = _get_blueprint_version(blueprint)
                if current_version and stored_version and current_version != stored_version:
                    conn.execute(
                        "DELETE FROM cache WHERE cache_key = ?", (key,)
                    )
                    conn.commit()
                    return None

            # Hit — update stats
            conn.execute(
                "UPDATE cache SET hit_count = hit_count + 1 WHERE cache_key = ?",
                (key,),
            )
            conn.commit()
            return response

        finally:
            conn.close()


def set(
    model: str,
    prompt: str,
    response: str,
    temperature: float = 0.1,
    rubric_id: str = "",
    blueprint: str = "",
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    content_hash: str = "",
) -> None:
    """
    Store a response in cache.

    content_hash: if provided, keys on content identity for eval/teacher caching.
    """
    key = _make_key(model, prompt, temperature, rubric_id, content_hash)
    now = datetime.now(timezone.utc)
    expires = now.timestamp() + ttl_seconds
    now_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    expires_str = datetime.fromtimestamp(expires, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
    blueprint_version = _get_blueprint_version(blueprint) if blueprint else None

    # Estimate token savings: response length in chars / 4 ≈ tokens
    token_savings = len(response) // 4

    with _lock:
        conn = _get_db()
        try:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache
                (cache_key, model, prompt_hash, response, blueprint, blueprint_version,
                 created_at, expires_at, hit_count, token_savings)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
                """,
                (
                    key, model, prompt_hash, response, blueprint or None,
                    blueprint_version, now_str, expires_str, token_savings,
                ),
            )
            conn.commit()
        finally:
            conn.close()


def invalidate_blueprint(blueprint_name: str) -> int:
    """Clear all cache entries for a specific blueprint. Returns count deleted."""
    with _lock:
        conn = _get_db()
        try:
            cursor = conn.execute(
                "DELETE FROM cache WHERE blueprint = ?", (blueprint_name,)
            )
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()


def invalidate_all() -> int:
    """Clear entire cache. Returns count deleted."""
    with _lock:
        conn = _get_db()
        try:
            cursor = conn.execute("DELETE FROM cache")
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()


def cleanup_expired() -> int:
    """Remove all expired entries. Returns count deleted."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with _lock:
        conn = _get_db()
        try:
            cursor = conn.execute("DELETE FROM cache WHERE expires_at < ?", (now,))
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()


def stats() -> dict:
    """Get cache statistics."""
    with _lock:
        conn = _get_db()
        try:
            total = conn.execute("SELECT COUNT(*) FROM cache").fetchone()[0]
            hits = conn.execute(
                "SELECT COALESCE(SUM(hit_count), 0) FROM cache"
            ).fetchone()[0]
            tokens = conn.execute(
                "SELECT COALESCE(SUM(token_savings * hit_count), 0) FROM cache"
            ).fetchone()[0]
            blueprints = conn.execute(
                "SELECT blueprint, COUNT(*) as cnt FROM cache WHERE blueprint IS NOT NULL GROUP BY blueprint"
            ).fetchall()

            # Approximate cost savings: ~$0.50 per 1M tokens (conservative)
            cost_saved = tokens * 0.50 / 1_000_000

            return {
                "total_entries": total,
                "total_hits": hits,
                "tokens_saved": tokens,
                "cost_saved_usd": round(cost_saved, 4),
                "per_blueprint": {b: c for b, c in blueprints},
            }
        finally:
            conn.close()


# --- internals ---

def _get_blueprint_version(blueprint_name: str) -> Optional[str]:
    """Get current version of a blueprint without importing auto_version (avoid circular)."""
    import yaml

    config_path = FORGE_ROOT / "blueprints" / blueprint_name / "config.yaml"
    if not config_path.exists():
        return None
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return config.get("blueprint", {}).get("version")
