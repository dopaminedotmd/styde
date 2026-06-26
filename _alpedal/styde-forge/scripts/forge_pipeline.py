"""
Full Forge pipeline: spawn → eval → improve → checkpoint.
Master orchestrator that runs the complete cycle.

Usage:
  python scripts/forge_pipeline.py [--target all|unevaluated|latest]
  python scripts/forge_pipeline.py --target top --top-n 10

Pipeline stages:
  1. Quality filter — detect poor outputs
  2. Rebuild state — sync from filesystem
  3. Re-spawn — flag failed/poor blueprints
  4. Parallel eval — self-eval + judge-eval for all unevaluated runs
  5. Parallel improve — teacher analysis + version bump for all evals
  6. Rebuild state — sync results
  7. Checkpoint — save state snapshot
"""

import sys
import subprocess
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = FORGE_ROOT / "scripts"


def run_script(name: str, args: str = "") -> int:
    """Run a script and return exit code."""
    cmd = [sys.executable, str(SCRIPTS / name)] + (args.split() if args else [])
    print(f"\n{'='*70}")
    print(f"STAGE: {name} {args}")
    print(f"{'='*70}")
    result = subprocess.run(cmd, cwd=str(FORGE_ROOT))
    return result.returncode


def main():
    args = sys.argv[1:]
    target = "all"
    top_n = None
    max_workers = 5

    for a in args:
        if a.startswith("--target="):
            target = a.split("=", 1)[1]
        elif a.startswith("--top-n="):
            top_n = int(a.split("=", 1)[1])
        elif a.startswith("--max-workers="):
            max_workers = int(a.split("=", 1)[1])

    worker_arg = f"--max-workers={max_workers}"

    # Stage 1: Quality check
    print("\n=== STAGE 1/9: Quality Filter ===")
    subprocess.run(
        [sys.executable, str(SCRIPTS / "quality_filter.py"), "--list"],
        cwd=str(FORGE_ROOT),
    )

    # Stage 2: Cleanup & cap (archive old runs, cap at 5)
    print("\n=== STAGE 2/9: Cleanup & Cap ===")
    subprocess.run(
        [sys.executable, str(SCRIPTS / "cleanup_cap.py"), "--max-runs=5", "--archive-failed"],
        cwd=str(FORGE_ROOT),
    )

    # Stage 3: Rebuild state from filesystem
    print("\n=== STAGE 3/9: Rebuild State ===")
    run_script("rebuild_state.py")

    # Stage 4: Flag poor outputs for re-spawn
    print("\n=== STAGE 4/9: Flag Poor Outputs ===")
    subprocess.run(
        [sys.executable, str(SCRIPTS / "quality_filter.py"), "--fix"],
        cwd=str(FORGE_ROOT),
    )

    # Stage 5: Parallel eval
    print("\n=== STAGE 5/9: Parallel Eval ===")
    eval_args = worker_arg
    if target == "top" and top_n:
        eval_args += f" --top-n={top_n}"
    run_script("parallel_eval.py", eval_args)

    # Stage 6: Parallel improve
    print("\n=== STAGE 6/9: Parallel Improve ===")
    run_script("parallel_improve.py", worker_arg)

    # Stage 7: Promote to production
    print("\n=== STAGE 7/9: Production Promotion ===")
    subprocess.run(
        [sys.executable, str(SCRIPTS / "promote_production.py")],
        cwd=str(FORGE_ROOT),
    )

    # Stage 8: Rebuild state
    print("\n=== STAGE 8/9: Rebuild State ===")
    run_script("rebuild_state.py")

    # Stage 9: Checkpoint
    print("\n=== STAGE 9/9: Checkpoint ===")
    subprocess.run(
        [sys.executable, str(FORGE_ROOT / "Core" / "forge.py"), "checkpoint",
         "pipeline-auto"],
        cwd=str(FORGE_ROOT),
    )

    # Final status
    print()
    subprocess.run(
        [sys.executable, str(FORGE_ROOT / "Core" / "forge.py"), "status"],
        cwd=str(FORGE_ROOT),
    )
    print()
    print("=== Forge Pipeline Complete ===")


if __name__ == "__main__":
    main()
