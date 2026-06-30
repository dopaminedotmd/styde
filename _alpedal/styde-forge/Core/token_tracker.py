"""
Token Usage Tracker — measure and optimize token consumption per blueprint/stage.

Tracks approximate token counts for spawn, eval, and teacher calls.
Stores history in 99_INDEXES/token_usage.json.
Helps identify expensive blueprints and optimize caveman settings.
"""
import json
import time
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional
from collections import defaultdict

FORGE_ROOT = Path(__file__).resolve().parent.parent
TOKEN_LOG = FORGE_ROOT / "99_INDEXES" / "token_usage.json"


class TokenTracker:
    """Tracks token usage across forge operations."""

    def __init__(self):
        self._lock = threading.Lock()
        self._buffer: list[dict] = []
        self._last_flush = time.time()
        self._flush_interval = 60.0  # flush to disk every 60s
        self._load()

    def _load(self):
        """Load history from disk."""
        self._history: list[dict] = []
        if TOKEN_LOG.exists():
            try:
                self._history = json.loads(TOKEN_LOG.read_text(encoding="utf-8"))
            except Exception:
                self._history = []

    def _flush(self):
        """Flush buffer to disk."""
        if self._buffer:
            self._history.extend(self._buffer)
            self._buffer.clear()
            # Keep last 10000 entries
            if len(self._history) > 10000:
                self._history = self._history[-10000:]
            try:
                TOKEN_LOG.parent.mkdir(parents=True, exist_ok=True)
                TOKEN_LOG.write_text(json.dumps(self._history, default=str), encoding="utf-8")
            except Exception:
                pass
        self._last_flush = time.time()

    def record(self, blueprint: str, stage: str, model: str,
               prompt_chars: int, output_chars: int, duration_ms: float,
               success: bool, cost_estimate: float = 0):
        """Record a token usage event.

        Token estimate: ~4 chars per token for English text (rough).
        """
        # Rough token estimate (4 chars/token is standard for English)
        prompt_tokens = max(1, prompt_chars // 4)
        output_tokens = max(1, output_chars // 4)
        total_tokens = prompt_tokens + output_tokens

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "blueprint": blueprint,
            "stage": stage,
            "model": model,
            "prompt_chars": prompt_chars,
            "output_chars": output_chars,
            "prompt_tokens_est": prompt_tokens,
            "output_tokens_est": output_tokens,
            "total_tokens_est": total_tokens,
            "duration_ms": round(duration_ms),
            "success": success,
            "cost_estimate": cost_estimate,
        }

        with self._lock:
            self._buffer.append(entry)
            if time.time() - self._last_flush > self._flush_interval:
                self._flush()

    def stats(self, hours: int = 24) -> dict:
        """Get aggregated token stats for last N hours."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        self._flush()

        by_stage = defaultdict(lambda: {"calls": 0, "tokens": 0, "chars_in": 0, "chars_out": 0,
                                          "success": 0, "failed": 0, "total_ms": 0})
        by_blueprint = defaultdict(lambda: {"calls": 0, "tokens": 0, "avg_tokens": 0})
        by_model = defaultdict(lambda: {"calls": 0, "tokens": 0})

        recent = [e for e in self._history
                  if datetime.fromisoformat(e["timestamp"]) > cutoff]

        for e in recent:
            # By stage
            s = by_stage[e["stage"]]
            s["calls"] += 1
            s["tokens"] += e["total_tokens_est"]
            s["chars_in"] += e["prompt_chars"]
            s["chars_out"] += e["output_chars"]
            s["total_ms"] += e["duration_ms"]
            if e["success"]:
                s["success"] += 1
            else:
                s["failed"] += 1

            # By blueprint
            b = by_blueprint[e["blueprint"]]
            b["calls"] += 1
            b["tokens"] += e["total_tokens_est"]

            # By model
            m = by_model[e["model"]]
            m["calls"] += 1
            m["tokens"] += e["total_tokens_est"]

        # Compute averages
        for bp, b in by_blueprint.items():
            b["avg_tokens"] = round(b["tokens"] / max(b["calls"], 1))

        # Top consumers
        top_consumers = sorted(by_blueprint.items(),
                               key=lambda x: x[1]["tokens"], reverse=True)[:10]

        return {
            "period_hours": hours,
            "total_entries": len(recent),
            "by_stage": {k: dict(v) for k, v in by_stage.items()},
            "by_model": {k: dict(v) for k, v in by_model.items()},
            "top_consumers": [{"blueprint": k, **v} for k, v in top_consumers],
            "summary": {
                "total_tokens": sum(e["total_tokens_est"] for e in recent),
                "total_calls": len(recent),
                "success_rate": round(
                    sum(1 for e in recent if e["success"]) / max(len(recent), 1) * 100, 1
                ),
                "avg_duration_ms": round(
                    sum(e["duration_ms"] for e in recent) / max(len(recent), 1)
                ),
            },
        }

    def blueprint_profile(self, blueprint_name: str, hours: int = 168) -> dict:
        """Get detailed token profile for a specific blueprint over last N hours."""
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        self._flush()

        entries = [e for e in self._history
                   if e["blueprint"] == blueprint_name
                   and datetime.fromisoformat(e["timestamp"]) > cutoff]

        if not entries:
            return {"blueprint": blueprint_name, "entries": 0}

        by_stage = defaultdict(lambda: {"calls": 0, "tokens": 0, "avg_duration_ms": 0})
        for e in entries:
            s = by_stage[e["stage"]]
            s["calls"] += 1
            s["tokens"] += e["total_tokens_est"]
            s["avg_duration_ms"] += e["duration_ms"]

        for stage, s in by_stage.items():
            s["avg_tokens"] = round(s["tokens"] / max(s["calls"], 1))
            s["avg_duration_ms"] = round(s["avg_duration_ms"] / max(s["calls"], 1))

        return {
            "blueprint": blueprint_name,
            "entries": len(entries),
            "total_tokens": sum(e["total_tokens_est"] for e in entries),
            "by_stage": {k: dict(v) for k, v in by_stage.items()},
            "models_used": list(set(e["model"] for e in entries)),
            "success_rate": round(
                sum(1 for e in entries if e["success"]) / max(len(entries), 1) * 100, 1
            ),
        }

    def clear(self):
        """Clear all history."""
        with self._lock:
            self._buffer.clear()
            self._history.clear()
            if TOKEN_LOG.exists():
                TOKEN_LOG.unlink(missing_ok=True)


# Singleton
_tracker: Optional[TokenTracker] = None
_tracker_lock = threading.Lock()


def get_tracker() -> TokenTracker:
    global _tracker
    if _tracker is None:
        with _tracker_lock:
            if _tracker is None:
                _tracker = TokenTracker()
    return _tracker


def record_usage(blueprint: str, stage: str, model: str,
                 prompt_chars: int, output_chars: int, duration_ms: float,
                 success: bool):
    """Convenience: record token usage."""
    get_tracker().record(blueprint, stage, model, prompt_chars, output_chars,
                         duration_ms, success)
