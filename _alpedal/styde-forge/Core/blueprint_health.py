"""
Blueprint Health Scanner — scan all blueprints for issues.

Checks: missing files, size anomalies, domain gaps, version consistency,
stale blueprints (no activity in 7 days), config validity, skill file count,
production-ready scoring patterns, completeness markers.
"""
import yaml
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"


class BlueprintHealthScanner:
    """Scans all blueprints and reports health issues."""

    def __init__(self):
        self._results: Optional[dict] = None
        self._last_scan: float = 0
        self._cache_ttl = 30.0

    def scan(self, force: bool = False) -> dict:
        """Full scan of all blueprints. Results cached for 30s."""
        now = time.time()
        if not force and self._results and (now - self._last_scan) < self._cache_ttl:
            return self._results

        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total": 0,
            "healthy": 0,
            "warnings": 0,
            "critical": 0,
            "issues": [],
            "domains": Counter(),
            "versions": Counter(),
            "missing_files": Counter(),
            "stale": [],
            "no_agents": [],
            "top_health": [],
        }

        if not BLUEPRINTS_DIR.exists():
            results["issues"].append({
                "blueprint": "_global",
                "severity": "critical",
                "issue": "Blueprints directory missing",
            })
            return results

        for bp_dir in sorted(BLUEPRINTS_DIR.iterdir()):
            if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                continue

            results["total"] += 1
            bp_name = bp_dir.name
            bp_issues = []

            # --- Required files ---
            required = ["persona.md", "BLUEPRINT.md", "config.yaml"]
            for fname in required:
                fp = bp_dir / fname
                if not fp.exists():
                    bp_issues.append({
                        "blueprint": bp_name,
                        "severity": "critical",
                        "issue": f"Missing {fname}",
                    })
                    results["missing_files"][fname] += 1
                else:
                    size = fp.stat().st_size
                    if size == 0:
                        bp_issues.append({
                            "blueprint": bp_name,
                            "severity": "critical",
                            "issue": f"{fname} is 0 bytes",
                        })
                    elif fname in ("persona.md", "BLUEPRINT.md") and size < 100:
                        bp_issues.append({
                            "blueprint": bp_name,
                            "severity": "warning",
                            "issue": f"{fname} very short ({size} bytes)",
                        })

            # --- Config analysis ---
            config_path = bp_dir / "config.yaml"
            domain = "unknown"
            version = "0.0.0"
            if config_path.exists():
                try:
                    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
                    if isinstance(cfg, dict):
                        bp_cfg = cfg.get("blueprint", {})
                        domain = bp_cfg.get("domain", "unknown")
                        version = bp_cfg.get("version", "0.0.0")
                        results["domains"][domain] += 1
                        results["versions"][version] += 1

                        # Check model_override
                        agent_cfg = cfg.get("agent", {})
                        if not agent_cfg.get("model_override"):
                            bp_issues.append({
                                "blueprint": bp_name,
                                "severity": "warning",
                                "issue": "No model_override in config (will use default flash)",
                            })
                except Exception as e:
                    bp_issues.append({
                        "blueprint": bp_name,
                        "severity": "critical",
                        "issue": f"config.yaml parse error: {e}",
                    })

            # --- BLUEPRINT.md completeness markers ---
            bp_md_path = bp_dir / "BLUEPRINT.md"
            if bp_md_path.exists():
                try:
                    content = bp_md_path.read_text(encoding="utf-8")
                    markers = {
                        "Output-First Protocol": "output-first" in content.lower(),
                        "No-Input Fallback": "no-input" in content.lower() or "fallback" in content.lower(),
                        "Format Compliance": "format" in content.lower(),
                    }
                    missing_markers = [k for k, v in markers.items() if not v]
                    if missing_markers:
                        bp_issues.append({
                            "blueprint": bp_name,
                            "severity": "warning",
                            "issue": f"Missing completeness markers: {', '.join(missing_markers)}",
                        })
                except Exception:
                    pass

            # --- Skills directory ---
            skills_dir = bp_dir / "skills"
            if skills_dir.exists():
                md_count = len(list(skills_dir.glob("*.md")))
                if md_count == 0:
                    bp_issues.append({
                        "blueprint": bp_name,
                        "severity": "warning",
                        "issue": "skills/ dir exists but has no .md files",
                    })
            else:
                bp_issues.append({
                    "blueprint": bp_name,
                    "severity": "info",
                    "issue": "No skills/ directory — consider adding specialized skills",
                })

            # --- Agent activity check ---
            activity = self._check_agent_activity(bp_name)
            if activity["last_activity"] is None:
                bp_issues.append({
                    "blueprint": bp_name,
                    "severity": "warning",
                    "issue": "No agent runs found for this blueprint",
                })
                results["no_agents"].append(bp_name)
            elif activity["days_since_last"] > 7:
                bp_issues.append({
                    "blueprint": bp_name,
                    "severity": "info",
                    "issue": f"Stale: last activity {activity['days_since_last']} days ago",
                })
                results["stale"].append({
                    "blueprint": bp_name,
                    "days": activity["days_since_last"],
                    "last_score": activity.get("last_score"),
                })

            # --- Production check ---
            if activity["in_production"]:
                bp_issues.append({
                    "blueprint": bp_name,
                    "severity": "info",
                    "issue": "Has agents in production — healthy",
                })

            # --- Tally ---
            for issue in bp_issues:
                if issue["severity"] == "critical":
                    results["critical"] += 1
                elif issue["severity"] == "warning":
                    results["warnings"] += 1
                results["issues"].append(issue)

            if not bp_issues:
                results["healthy"] += 1

        # Top health (fewest issues)
        bp_issue_counts = defaultdict(int)
        for issue in results["issues"]:
            bp_issue_counts[issue["blueprint"]] += 1

        all_bps = set()
        for bp_dir in BLUEPRINTS_DIR.iterdir():
            if bp_dir.is_dir() and not bp_dir.name.startswith("_"):
                all_bps.add(bp_dir.name)

        for bp in all_bps:
            if bp not in bp_issue_counts:
                results["top_health"].append({"blueprint": bp, "issues": 0})

        results["top_health"].sort(key=lambda x: x["issues"])
        results["top_health"] = results["top_health"][:10]

        # Summary
        results["summary"] = {
            "pass_rate": round(results["healthy"] / max(results["total"], 1) * 100, 1),
            "critical_rate": round(results["critical"] / max(results["total"], 1) * 100, 1),
            "total_issues": results["critical"] + results["warnings"],
        }

        self._results = results
        self._last_scan = now
        return results

    def _check_agent_activity(self, blueprint_name: str) -> dict:
        """Check agent activity across refinery/production/archive."""
        result = {
            "last_activity": None,
            "days_since_last": 999,
            "last_score": None,
            "in_production": False,
            "refinery_count": 0,
            "production_count": 0,
            "archive_count": 0,
        }

        now = datetime.now(timezone.utc)
        latest_mtime = None

        for zone in ["refinery", "production", "archive"]:
            runs_dir = FORGE_ROOT / "StydeAgents" / zone / blueprint_name / "runs"
            if not runs_dir.exists():
                continue
            for run_dir in runs_dir.iterdir():
                if not run_dir.name.startswith("run-"):
                    continue
                if zone == "production":
                    result["production_count"] += 1
                elif zone == "refinery":
                    result["refinery_count"] += 1
                else:
                    result["archive_count"] += 1

                mtime = datetime.fromtimestamp(run_dir.stat().st_mtime, tz=timezone.utc)
                if latest_mtime is None or mtime > latest_mtime:
                    latest_mtime = mtime

                # Get score
                ev = run_dir / "eval.yaml"
                if ev.exists():
                    try:
                        data = yaml.safe_load(ev.read_text(encoding="utf-8"))
                        sc = data.get("composite", {}).get("composite_score")
                        if sc is not None:
                            result["last_score"] = sc
                    except Exception:
                        pass

        if latest_mtime:
            result["last_activity"] = latest_mtime.isoformat()
            result["days_since_last"] = (now - latest_mtime).days

        result["in_production"] = result["production_count"] > 0
        return result

    def get_domain_health(self) -> dict:
        """Report health by domain."""
        report = self.scan()
        domain_health = defaultdict(lambda: {"total": 0, "critical": 0, "warnings": 0, "healthy": 0})

        for issue in report["issues"]:
            bp = issue["blueprint"]
            # Find domain
            cfg_path = BLUEPRINTS_DIR / bp / "config.yaml"
            domain = "unknown"
            if cfg_path.exists():
                try:
                    cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
                    domain = cfg.get("blueprint", {}).get("domain", "unknown")
                except Exception:
                    pass
            d = domain_health[domain]
            d["total"] += 1
            if issue["severity"] == "critical":
                d["critical"] += 1
            elif issue["severity"] == "warning":
                d["warnings"] += 1

        # Mark healthy
        for bp_name in report["top_health"]:
            if bp_name.get("issues", 0) == 0:
                cfg_path = BLUEPRINTS_DIR / bp_name["blueprint"] / "config.yaml"
                if cfg_path.exists():
                    try:
                        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
                        domain = cfg.get("blueprint", {}).get("domain", "unknown")
                        domain_health[domain]["healthy"] += 1
                    except Exception:
                        pass

        return dict(domain_health)

    def get_critical_bps(self) -> list[dict]:
        """Return only critical issues."""
        report = self.scan()
        return [i for i in report["issues"] if i["severity"] == "critical"]

    def get_stale_bps(self, days: int = 7) -> list[dict]:
        """Return blueprints with no activity in N days."""
        report = self.scan()
        return [s for s in report.get("stale", []) if s["days"] > days]


# Singleton
_scanner: Optional[BlueprintHealthScanner] = None


def get_scanner() -> BlueprintHealthScanner:
    global _scanner
    if _scanner is None:
        _scanner = BlueprintHealthScanner()
    return _scanner


def scan_blueprints(force: bool = False) -> dict:
    return get_scanner().scan(force=force)
