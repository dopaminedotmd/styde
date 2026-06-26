"""Clean up empty run dirs for failed blueprints, then re-spawn with parallel spawner."""
from pathlib import Path
import shutil
import subprocess
import sys

FORGE_ROOT = Path(__file__).resolve().parent.parent
refinery = FORGE_ROOT / "StydeAgents" / "refinery"

failed = [
    "capacitor-hybrid-builder", "cdn-edge-architect", "chaos-engineering-specialist",
    "cli-tool-builder", "cpp-performance-engineer", "creative-coding-artist",
    "cross-chain-bridge-architect", "crypto-trading-bot", "customer-feedback-analyzer",
    "dao-governance-designer", "decision-framework-builder", "defi-protocol-designer",
    "dependency-mapper", "distributed-systems-architect", "tool-registry-optimizer",
]

# Step 1: Clean empty run dirs
for bp in failed:
    bp_dir = refinery / bp
    if not bp_dir.exists():
        continue
    runs_dir = bp_dir / "runs"
    if runs_dir.exists():
        for run_dir in list(runs_dir.iterdir()):
            output = run_dir / "output.md"
            if not output.exists() or output.stat().st_size == 0:
                try:
                    shutil.rmtree(run_dir)
                except Exception:
                    pass
        try:
            if not any(runs_dir.iterdir()):
                runs_dir.rmdir()
        except Exception:
            pass
    try:
        if not any(bp_dir.iterdir()):
            bp_dir.rmdir()
    except Exception:
        pass

print(f"Cleaned empty run dirs for {len(failed)} failed blueprints")

# Step 2: Run parallel spawner on failed blueprints
bp_arg = ",".join(failed)
result = subprocess.run(
    [sys.executable, str(FORGE_ROOT / "scripts" / "parallel_spawn.py"),
     f"--blueprint={bp_arg}", "--max-workers=5"],
    cwd=str(FORGE_ROOT),
    capture_output=True, text=True, timeout=1800,
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr[:500])
