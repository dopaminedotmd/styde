"""
Auto-healing for Styde Forge — detect and fix common issues automatically.

Handles:
- Stale .forge.lock cleanup
- Corrupt cache.db detection and removal
- Stale pycache cleanup
- 0-byte forge.py recovery
- Stale state.yaml temp files cleanup
- Hermes CLI availability check
- Disk space monitoring
"""
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


FORGE_ROOT = Path(__file__).resolve().parent.parent


class AutoHealer:
    """Detects and auto-fixes common forge issues."""

    def __init__(self):
        self.heals_applied: list[dict] = []
        self.last_check: Optional[float] = None

    def run_health_check(self, auto_fix: bool = True) -> dict:
        """Run a full health check. Returns findings and fixes applied."""
        self.last_check = time.time()
        findings = []
        fixes = []

        # 1. Check stale .forge.lock
        lock_file = FORGE_ROOT / ".forge.lock"
        if lock_file.exists():
            try:
                content = lock_file.read_text().strip()
                pid = int(content) if content.isdigit() else None
                if pid:
                    # Check if PID is still alive
                    try:
                        os.kill(pid, 0)
                        findings.append({
                            "issue": "stale_lock",
                            "severity": "high",
                            "detail": f"Active PID {pid} holds .forge.lock",
                            "fixed": False,
                        })
                    except (OSError, PermissionError):
                        # PID not running — stale lock
                        findings.append({
                            "issue": "stale_lock",
                            "severity": "medium",
                            "detail": f"Stale .forge.lock with dead PID {pid}",
                            "fixed": False,
                        })
                        if auto_fix:
                            lock_file.unlink()
                            fixes.append({
                                "issue": "stale_lock",
                                "action": "removed",
                                "detail": f"Removed stale .forge.lock (PID {pid} dead)",
                            })
                else:
                    findings.append({
                        "issue": "corrupt_lock",
                        "severity": "low",
                        "detail": ".forge.lock has invalid content",
                        "fixed": False,
                    })
                    if auto_fix:
                        lock_file.unlink()
                        fixes.append({
                            "issue": "corrupt_lock",
                            "action": "removed",
                            "detail": "Removed corrupt .forge.lock",
                        })
            except Exception as e:
                findings.append({
                    "issue": "lock_read_error",
                    "severity": "medium",
                    "detail": f"Cannot read .forge.lock: {e}",
                    "fixed": False,
                })

        # 2. Check corrupt cache.db (quick stat check only — SQLite integrity_check is too slow)
        cache_db = FORGE_ROOT / "99_INDEXES" / "cache.db"
        if cache_db.exists():
            size = cache_db.stat().st_size
            if size == 0:
                findings.append({
                    "issue": "zero_byte_cache",
                    "severity": "critical",
                    "detail": "cache.db is 0 bytes — will cause all spawns to fail",
                    "fixed": False,
                })
                if auto_fix:
                    try:
                        cache_db.unlink()
                        fixes.append({
                            "issue": "zero_byte_cache",
                            "action": "removed",
                            "detail": "Removed 0-byte cache.db",
                        })
                    except Exception:
                        pass
            elif size > 100 * 1024 * 1024:  # >100MB — probably bloated
                findings.append({
                    "issue": "large_cache",
                    "severity": "low",
                    "detail": f"cache.db is {size/1024/1024:.0f}MB — consider pruning",
                    "fixed": False,
                })
            else:
                findings.append({
                    "issue": "cache_db_ok",
                    "severity": "info",
                    "detail": f"cache.db exists ({size/1024:.0f}KB)",
                    "fixed": True,
                })

        # 3. Check 0-byte forge.py
        forge_py = FORGE_ROOT / "Core" / "forge.py"
        if forge_py.exists():
            size = forge_py.stat().st_size
            if size == 0:
                findings.append({
                    "issue": "zero_byte_forge",
                    "severity": "critical",
                    "detail": "Core/forge.py is 0 bytes",
                    "fixed": False,
                })
                if auto_fix:
                    try:
                        subprocess.run(
                            ["git", "checkout", "--", "Core/forge.py"],
                            cwd=str(FORGE_ROOT),
                            capture_output=True,
                            timeout=30,
                        )
                        if forge_py.stat().st_size > 0:
                            fixes.append({
                                "issue": "zero_byte_forge",
                                "action": "restored",
                                "detail": "Restored Core/forge.py from git",
                            })
                    except Exception as e:
                        fixes.append({
                            "issue": "zero_byte_forge",
                            "action": "failed",
                            "detail": f"Git restore failed: {e}",
                        })
            elif size < 1000:
                findings.append({
                    "issue": "small_forge",
                    "severity": "high",
                    "detail": f"Core/forge.py is only {size} bytes (expected ~70KB)",
                    "fixed": False,
                })
        else:
            findings.append({
                "issue": "missing_forge",
                "severity": "critical",
                "detail": "Core/forge.py not found",
                "fixed": False,
            })

        # 4. Check Hermes CLI (quick check only — just verify binary exists)
        try:
            from Core.hermes_bridge import find_hermes
            hp = find_hermes()
            if hp == "hermes" or not Path(hp).exists():
                findings.append({
                    "issue": "hermes_not_found",
                    "severity": "critical",
                    "detail": f"Hermes CLI not found (resolved to: {hp})",
                    "fixed": False,
                })
            else:
                findings.append({
                    "issue": "hermes_ok",
                    "severity": "info",
                    "detail": f"Hermes CLI found: {hp}",
                    "fixed": True,
                })
        except Exception as e:
            findings.append({
                "issue": "hermes_check_failed",
                "severity": "high",
                "detail": f"Hermes check error: {e}",
                "fixed": False,
            })

        # 6. Clean stale temp files
        stale_temps = list(FORGE_ROOT.glob(".state.yaml.*.tmp"))
        if stale_temps:
            findings.append({
                "issue": "stale_temps",
                "severity": "low",
                "detail": f"{len(stale_temps)} stale .tmp files",
                "fixed": False,
            })
            if auto_fix:
                removed = 0
                for tmp in stale_temps:
                    try:
                        tmp.unlink()
                        removed += 1
                    except Exception:
                        pass
                fixes.append({
                    "issue": "stale_temps",
                    "action": "cleaned",
                    "detail": f"Removed {removed}/{len(stale_temps)} stale .tmp files",
                })

        # Record heals
        self.heals_applied.extend(fixes)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "findings": findings,
            "fixes": fixes,
            "total_issues": sum(1 for f in findings if f["severity"] in ("critical", "high")),
            "total_info": sum(1 for f in findings if f["severity"] == "info"),
            "heals_cumulative": len(self.heals_applied),
        }

    def quick_check(self) -> bool:
        """Quick health check — returns True if forge is healthy enough to run."""
        report = self.run_health_check(auto_fix=True)
        critical_issues = sum(
            1 for f in report["findings"]
            if f["severity"] == "critical" and not f.get("fixed", False)
        )
        return critical_issues == 0

    def get_history(self) -> list[dict]:
        """Get history of heals applied."""
        return list(self.heals_applied)


# Singleton
_healer: Optional[AutoHealer] = None


def get_healer() -> AutoHealer:
    global _healer
    if _healer is None:
        _healer = AutoHealer()
    return _healer


def run_health_check(auto_fix: bool = True) -> dict:
    """Convenience: run health check on singleton."""
    return get_healer().run_health_check(auto_fix=auto_fix)


def quick_check() -> bool:
    """Convenience: quick check on singleton."""
    return get_healer().quick_check()
