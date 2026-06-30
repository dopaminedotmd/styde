"""
Eval Calibration Tracker — monitor self-eval vs judge-eval divergence.

Detects evaluator drift over time. Flags when:
- Self-eval consistently overestimates (optimism bias)
- Self-eval consistently underestimates (pessimism bias)
- Judge-eval drifts from historical norms
- Specific blueprints have calibration issues

Stores calibration data in 99_INDEXES/calibration.json.
"""
import json
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional
from collections import defaultdict

FORGE_ROOT = Path(__file__).resolve().parent.parent
CALIBRATION_LOG = FORGE_ROOT / "99_INDEXES" / "calibration.json"


class CalibrationTracker:
    """Tracks self vs judge divergence across evaluations."""

    def __init__(self):
        self._lock = threading.Lock()
        self._entries: list[dict] = []
        self._load()

    def _load(self):
        if CALIBRATION_LOG.exists():
            try:
                self._entries = json.loads(CALIBRATION_LOG.read_text(encoding="utf-8"))
            except Exception:
                self._entries = []

    def _save(self):
        try:
            CALIBRATION_LOG.parent.mkdir(parents=True, exist_ok=True)
            # Keep last 5000 entries
            if len(self._entries) > 5000:
                self._entries = self._entries[-5000:]
            CALIBRATION_LOG.write_text(json.dumps(self._entries, default=str), encoding="utf-8")
        except Exception:
            pass

    def record(self, blueprint: str, run_id: str,
               self_score: float, judge_score: float, composite_score: float,
               self_dims: dict = None, judge_dims: dict = None):
        """Record an eval calibration point."""
        divergence = self_score - judge_score
        abs_divergence = abs(divergence)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "blueprint": blueprint,
            "run_id": run_id,
            "self_score": self_score,
            "judge_score": judge_score,
            "composite_score": composite_score,
            "divergence": round(divergence, 1),
            "abs_divergence": round(abs_divergence, 1),
            "bias": "optimistic" if divergence > 5 else "pessimistic" if divergence < -5 else "neutral",
            "self_dims": self_dims or {},
            "judge_dims": judge_dims or {},
        }

        with self._lock:
            self._entries.append(entry)
            # Auto-save every 10 entries
            if len(self._entries) % 10 == 0:
                self._save()

    def stats(self, hours: int = 168) -> dict:
        """Calibration statistics for last N hours."""
        self._save()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        recent = [e for e in self._entries
                  if datetime.fromisoformat(e["timestamp"]) > cutoff]

        if not recent:
            return {"entries": 0, "message": "No calibration data"}

        divergences = [e["divergence"] for e in recent]
        abs_divs = [e["abs_divergence"] for e in recent]
        biases = defaultdict(int)
        for e in recent:
            biases[e["bias"]] += 1

        # Per-blueprint calibration
        bp_cal = defaultdict(lambda: {"count": 0, "divergences": [], "avg_self": 0, "avg_judge": 0})
        for e in recent:
            bp = bp_cal[e["blueprint"]]
            bp["count"] += 1
            bp["divergences"].append(e["divergence"])
            bp["avg_self"] += e["self_score"]
            bp["avg_judge"] += e["judge_score"]

        bp_summary = []
        for bp, data in bp_cal.items():
            data["avg_self"] = round(data["avg_self"] / data["count"], 1)
            data["avg_judge"] = round(data["avg_judge"] / data["count"], 1)
            data["avg_divergence"] = round(sum(data["divergences"]) / data["count"], 1)
            data["avg_abs_divergence"] = round(
                sum(abs(d) for d in data["divergences"]) / data["count"], 1
            )
            if data["count"] >= 3:  # Only include BPs with enough data
                bp_summary.append({
                    "blueprint": bp,
                    "evals": data["count"],
                    "avg_self": data["avg_self"],
                    "avg_judge": data["avg_judge"],
                    "avg_divergence": data["avg_divergence"],
                    "avg_abs_div": data["avg_abs_divergence"],
                    "bias": "optimistic" if data["avg_divergence"] > 3
                            else "pessimistic" if data["avg_divergence"] < -3
                            else "neutral",
                })

        bp_summary.sort(key=lambda x: x["avg_abs_div"], reverse=True)

        # Dimension-level calibration
        dim_divergences = defaultdict(list)
        for e in recent:
            sd = e.get("self_dims", {})
            jd = e.get("judge_dims", {})
            for dim in set(list(sd.keys()) + list(jd.keys())):
                sv = sd.get(dim, 0)
                jv = jd.get(dim, 0)
                if sv and jv:
                    dim_divergences[dim].append(sv - jv)

        dim_summary = {}
        for dim, divs in dim_divergences.items():
            if divs:
                dim_summary[dim] = {
                    "avg_divergence": round(sum(divs) / len(divs), 1),
                    "count": len(divs),
                }

        return {
            "period_hours": hours,
            "entries": len(recent),
            "avg_divergence": round(sum(divergences) / len(divergences), 1),
            "avg_abs_divergence": round(sum(abs_divs) / len(abs_divs), 1),
            "max_divergence": round(max(abs_divs), 1),
            "bias_distribution": dict(biases),
            "by_blueprint": bp_summary[:15],
            "by_dimension": dim_summary,
            "flags": self._detect_flags(bp_summary, divergences),
        }

    def _detect_flags(self, bp_summary: list[dict], divergences: list[float]) -> list[str]:
        """Detect calibration issues."""
        flags = []
        avg_div = sum(divergences) / len(divergences) if divergences else 0

        if avg_div > 5:
            flags.append(f"Systematic optimism bias: self-eval {avg_div:.1f} pts higher than judge")
        elif avg_div < -5:
            flags.append(f"Systematic pessimism bias: self-eval {abs(avg_div):.1f} pts lower than judge")

        for bp in bp_summary[:5]:
            if bp["avg_abs_div"] > 15:
                flags.append(f"High divergence: {bp['blueprint']} ({bp['avg_abs_div']:.0f} pts)")

        return flags

    def clear(self):
        """Clear all calibration data."""
        with self._lock:
            self._entries.clear()
            if CALIBRATION_LOG.exists():
                CALIBRATION_LOG.unlink(missing_ok=True)


# Singleton
_tracker: Optional[CalibrationTracker] = None
_tracker_lock = threading.Lock()


def get_calibration() -> CalibrationTracker:
    global _tracker
    if _tracker is None:
        with _tracker_lock:
            if _tracker is None:
                _tracker = CalibrationTracker()
    return _tracker


def record_eval(blueprint: str, run_id: str, self_score: float, judge_score: float,
                composite_score: float, self_dims: dict = None, judge_dims: dict = None):
    """Convenience: record eval for calibration tracking."""
    get_calibration().record(blueprint, run_id, self_score, judge_score,
                             composite_score, self_dims, judge_dims)
