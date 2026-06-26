"""Find blueprints with no completed runs."""
from pathlib import Path
import sys

refinery = Path("StydeAgents/refinery")
blueprints = sorted(d.name for d in Path("blueprints").iterdir() if d.is_dir())

failed = []
for bp in blueprints:
    bp_dir = refinery / bp
    if not bp_dir.exists():
        failed.append((bp, "no refinery dir"))
        continue
    runs_dir = bp_dir / "runs"
    if not runs_dir.exists() or not any(runs_dir.iterdir()):
        failed.append((bp, "no run dirs"))
        continue
    has_output = False
    for run_dir in runs_dir.iterdir():
        output = run_dir / "output.md"
        if output.exists() and output.stat().st_size > 0:
            has_output = True
            break
    if not has_output:
        failed.append((bp, "no output.md"))

print(f"Blueprints utan lyckade runs: {len(failed)}")
for bp, reason in failed:
    print(f"  - {bp} ({reason})")
