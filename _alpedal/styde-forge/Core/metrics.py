"""
Metrics collector for Styde Forge — real-time stats for dashboard.

Collects and caches forge statistics from the filesystem.
Uses file-based caching to avoid expensive directory scans.
"""
import time
import json
import threading
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional


FORGE_ROOT = Path(__file__).resolve().parent.parent
CACHE_FILE = FORGE_ROOT / "99_INDEXES" / "metrics_cache.json"


class MetricsCollector:
    """Collects and caches forge statistics."""

    def __init__(self):
        self._cache: Optional[dict] = None
        self._cache_time: float = 0
        self._cache_ttl: float = 5.0  # seconds
        self._lock = threading.Lock()
        self._history: list[dict] = []  # last 100 snapshots
        self._max_history = 100

    def collect(self, force: bool = False) -> dict:
        """Collect current forge statistics. Uses cache unless force=True."""
        now = time.time()
        if not force and self._cache is not None and (now - self._cache_time) < self._cache_ttl:
            return self._cache

        with self._lock:
            metrics = self._collect_inner()
            self._cache = metrics
            self._cache_time = now

            # History
            snapshot = {
                "timestamp": metrics["timestamp"],
                "total_agents": metrics["counts"]["total"],
                "refinery": metrics["counts"]["refinery"],
                "production": metrics["counts"]["production"],
                "archive": metrics["counts"]["archive"],
                "avg_score": metrics["scores"]["average"],
                "promoted_24h": metrics["activity"]["promoted_24h"],
                "spawned_24h": metrics["activity"]["spawned_24h"],
            }
            self._history.append(snapshot)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]

            # Persist cache
            try:
                CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
                CACHE_FILE.write_text(json.dumps(metrics, default=str), encoding="utf-8")
            except Exception:
                pass

            return metrics

    def _collect_inner(self) -> dict:
        """Internal collection logic — no locking."""
        refinery_dir = FORGE_ROOT / "StydeAgents" / "refinery"
        production_dir = FORGE_ROOT / "StydeAgents" / "production"
        archive_dir = FORGE_ROOT / "StydeAgents" / "archive"
        blueprints_dir = FORGE_ROOT / "StydeAgents" / "blueprints"

        # Count agents on filesystem (NOT state.yaml)
        refinery_count = 0
        production_count = 0
        archive_count = 0
        refinery_bps = set()
        production_bps = set()
        archive_bps = set()
        scores = []
        blueprint_scores = {}

        # Scan refinery
        if refinery_dir.exists():
            for bp_dir in refinery_dir.iterdir():
                if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                    continue
                runs_dir = bp_dir / "runs"
                if runs_dir.exists():
                    for run_dir in runs_dir.iterdir():
                        if run_dir.name.startswith("run-"):
                            refinery_count += 1
                            refinery_bps.add(bp_dir.name)
                            # Get score
                            ev = run_dir / "eval.yaml"
                            if ev.exists():
                                try:
                                    import yaml
                                    data = yaml.safe_load(ev.read_text(encoding="utf-8"))
                                    sc = data.get("composite", {}).get("composite_score")
                                    if sc is not None:
                                        scores.append(sc)
                                        if bp_dir.name not in blueprint_scores:
                                            blueprint_scores[bp_dir.name] = []
                                        blueprint_scores[bp_dir.name].append(sc)
                                except Exception:
                                    pass

        # Scan production
        if production_dir.exists():
            for bp_dir in production_dir.iterdir():
                if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                    continue
                runs_dir = bp_dir / "runs"
                if runs_dir.exists():
                    for run_dir in runs_dir.iterdir():
                        if run_dir.name.startswith("run-"):
                            production_count += 1
                            production_bps.add(bp_dir.name)
                            ev = run_dir / "eval.yaml"
                            if ev.exists():
                                try:
                                    import yaml
                                    data = yaml.safe_load(ev.read_text(encoding="utf-8"))
                                    sc = data.get("composite", {}).get("composite_score")
                                    if sc is not None:
                                        scores.append(sc)
                                        if bp_dir.name not in blueprint_scores:
                                            blueprint_scores[bp_dir.name] = []
                                        blueprint_scores[bp_dir.name].append(sc)
                                except Exception:
                                    pass

        # Scan archive
        if archive_dir.exists():
            for bp_dir in archive_dir.iterdir():
                if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                    continue
                runs_dir = bp_dir / "runs"
                if runs_dir.exists():
                    for run_dir in runs_dir.iterdir():
                        if run_dir.name.startswith("run-"):
                            archive_count += 1
                            archive_bps.add(bp_dir.name)

        # Blueprint counts
        blueprint_count = 0
        if blueprints_dir.exists():
            blueprint_count = sum(1 for bp in blueprints_dir.iterdir()
                                if bp.is_dir() and not bp.name.startswith("_"))

        # Compute scores
        avg_score = sum(scores) / len(scores) if scores else 0
        max_score = max(scores) if scores else 0
        min_score = min(scores) if scores else 0

        # Score distribution
        dist = {"85-100": 0, "70-84": 0, "50-69": 0, "0-49": 0}
        for s in scores:
            if s >= 85:
                dist["85-100"] += 1
            elif s >= 70:
                dist["70-84"] += 1
            elif s >= 50:
                dist["50-69"] += 1
            else:
                dist["0-49"] += 1

        # Top blueprints
        bp_avgs = {}
        for bp, bps in blueprint_scores.items():
            bp_avgs[bp] = sum(bps) / len(bps)
        top_bps = sorted(bp_avgs.items(), key=lambda x: x[1], reverse=True)[:10]
        bottom_bps = sorted(bp_avgs.items(), key=lambda x: x[1])[:10]

        # Activity in last 24h
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        promoted_24h = 0
        spawned_24h = 0
        evaled_24h = 0
        archived_24h = 0

        for zone_dir, counter_name in [
            (production_dir, "promoted"),
            (refinery_dir, "spawned"),
            (archive_dir, "archived"),
        ]:
            if not zone_dir.exists():
                continue
            for bp_dir in zone_dir.iterdir():
                if not bp_dir.is_dir():
                    continue
                runs_dir = bp_dir / "runs"
                if not runs_dir.exists():
                    continue
                for run_dir in runs_dir.iterdir():
                    if not run_dir.name.startswith("run-"):
                        continue
                    try:
                        mtime = datetime.fromtimestamp(run_dir.stat().st_mtime, tz=timezone.utc)
                        if mtime > cutoff:
                            if counter_name == "promoted":
                                promoted_24h += 1
                            elif counter_name == "spawned":
                                spawned_24h += 1
                            elif counter_name == "archived":
                                archived_24h += 1
                    except Exception:
                        pass

        # Eval count in 24h
        for zone_dir in [refinery_dir, production_dir]:
            if not zone_dir.exists():
                continue
            for bp_dir in zone_dir.iterdir():
                if not bp_dir.is_dir():
                    continue
                runs_dir = bp_dir / "runs"
                if not runs_dir.exists():
                    continue
                for run_dir in runs_dir.iterdir():
                    ev = run_dir / "eval.yaml"
                    if ev.exists():
                        try:
                            mtime = datetime.fromtimestamp(ev.stat().st_mtime, tz=timezone.utc)
                            if mtime > cutoff:
                                evaled_24h += 1
                        except Exception:
                            pass

        # Read state.yaml for loop iterations
        loop_iterations = 0
        total_agents_spawned = 0
        caveman = True
        try:
            state_file = FORGE_ROOT / "state.yaml"
            if state_file.exists():
                import yaml
                state = yaml.safe_load(state_file.read_text(encoding="utf-8"))
                loop_iterations = state.get("loop_iterations", 0)
                total_agents_spawned = state.get("total_agents_spawned", 0)
                caveman = state.get("caveman_ultra", True)
        except Exception:
            pass

        # Hardware
        import shutil
        disk = shutil.disk_usage(str(FORGE_ROOT))

        # Forge lock
        lock_exists = (FORGE_ROOT / ".forge.lock").exists()

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "forge": {
                "version": "3.1.0",
                "codename": "The Crucible",
                "caveman_ultra": caveman,
                "lock_active": lock_exists,
                "loop_iterations": loop_iterations,
                "total_agents_spawned": total_agents_spawned,
            },
            "counts": {
                "total": refinery_count + production_count + archive_count,
                "refinery": refinery_count,
                "production": production_count,
                "archive": archive_count,
                "blueprints": blueprint_count,
                "blueprints_active": len(refinery_bps) + len(production_bps),
                "blueprints_production": len(production_bps),
                "blueprints_archived": len(archive_bps),
            },
            "scores": {
                "average": round(avg_score, 1),
                "max": max_score,
                "min": min_score,
                "count": len(scores),
                "distribution": dist,
                "pass_rate": round(dist["85-100"] / len(scores) * 100, 1) if scores else 0,
            },
            "top_blueprints": [
                {"name": name, "avg_score": round(avg, 1)}
                for name, avg in top_bps
            ],
            "bottom_blueprints": [
                {"name": name, "avg_score": round(avg, 1)}
                for name, avg in bottom_bps
            ],
            "activity": {
                "spawned_24h": spawned_24h,
                "promoted_24h": promoted_24h,
                "evaluated_24h": evaled_24h,
                "archived_24h": archived_24h,
            },
            "hardware": {
                "disk_total_gb": round(disk.total / (1024**3), 1),
                "disk_used_gb": round(disk.used / (1024**3), 1),
                "disk_free_gb": round(disk.free / (1024**3), 1),
            },
        }

    def get_history(self, limit: int = 20) -> list[dict]:
        """Get historical metric snapshots."""
        with self._lock:
            return self._history[-limit:]

    def get_blueprint_detail(self, blueprint_name: str) -> Optional[dict]:
        """Get detailed stats for a single blueprint."""
        import yaml
        result = {
            "name": blueprint_name,
            "refinery_runs": [],
            "production_runs": [],
            "archive_runs": [],
        }

        for zone, key in [
            ("refinery", "refinery_runs"),
            ("production", "production_runs"),
            ("archive", "archive_runs"),
        ]:
            zone_dir = FORGE_ROOT / "StydeAgents" / zone / blueprint_name / "runs"
            if not zone_dir.exists():
                continue
            for run_dir in sorted(zone_dir.iterdir()):
                if not run_dir.name.startswith("run-"):
                    continue
                ev = run_dir / "eval.yaml"
                score = None
                if ev.exists():
                    try:
                        data = yaml.safe_load(ev.read_text(encoding="utf-8"))
                        score = data.get("composite", {}).get("composite_score")
                    except Exception:
                        pass
                result[key].append({
                    "run": run_dir.name,
                    "score": score,
                    "mtime": datetime.fromtimestamp(
                        run_dir.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                })

        # Compute trends
        all_scores = []
        for zone in ["refinery_runs", "production_runs", "archive_runs"]:
            for run in result[zone]:
                if run["score"] is not None:
                    all_scores.append(run["score"])

        result["trend"] = {
            "total_runs": len(all_scores),
            "avg_score": round(sum(all_scores) / len(all_scores), 1) if all_scores else 0,
            "latest_score": all_scores[-1] if all_scores else None,
            "trending": "up" if len(all_scores) >= 2 and all_scores[-1] > all_scores[-2] else
                        "down" if len(all_scores) >= 2 and all_scores[-1] < all_scores[-2] else
                        "flat",
        }

        return result


# Singleton
_collector: Optional[MetricsCollector] = None
_collector_lock = threading.Lock()


def get_collector() -> MetricsCollector:
    global _collector
    if _collector is None:
        with _collector_lock:
            if _collector is None:
                _collector = MetricsCollector()
    return _collector


def collect_metrics(force: bool = False) -> dict:
    """Convenience: collect metrics."""
    return get_collector().collect(force=force)
