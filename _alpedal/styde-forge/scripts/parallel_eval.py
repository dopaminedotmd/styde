"""
Parallel eval pipeline for Styde Forge.
Processes all runs without eval.yaml: self-eval + judge-eval + composite.

Usage:
  python scripts/parallel_eval.py [--max-workers 5] [--dry-run]
"""

import sys
import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

FORGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_ROOT))

import yaml
from Core.evaluate import (
    build_self_eval_prompt, build_judge_eval_prompt,
    parse_eval_yaml, compute_composite, save_eval,
    load_agent_output, load_rubric,
)
from Core.hermes_bridge import run_eval
from Core.state import save_state, load_state


def find_runs_needing_eval():
    """Find run directories that have output.md but no eval.yaml."""
    refinery = FORGE_ROOT / "StydeAgents" / "refinery"
    runs = []
    for bp_dir in sorted(refinery.iterdir()):
        if not bp_dir.is_dir():
            continue
        bp_name = bp_dir.name
        runs_dir = bp_dir / "runs"
        if not runs_dir.exists():
            continue
        for run_dir in sorted(runs_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            output_file = run_dir / "output.md"
            eval_file = run_dir / "eval.yaml"
            if output_file.exists() and output_file.stat().st_size > 0 and not eval_file.exists():
                runs.append({
                    "blueprint": bp_name,
                    "run_dir": run_dir,
                    "run_id": run_dir.name.replace("run-", ""),
                })
    return runs


def evaluate_one(run_info: dict) -> dict:
    """Evaluate a single run: self-eval + judge-eval + composite."""
    start = time.time()
    bp = run_info["blueprint"]
    run_dir = run_info["run_dir"]
    result = {"blueprint": bp, "run_id": run_info["run_id"], "success": False, "duration_s": 0}

    try:
        output = load_agent_output(run_dir)
        ctx_file = run_dir / "spawn_context.yaml"
        rubric = ""
        benchmark = "manual"
        if ctx_file.exists():
            ctx = yaml.safe_load(ctx_file.read_text(encoding="utf-8")) or {}
            benchmark = ctx.get("benchmark", "manual")
            if benchmark != "manual":
                rubric = load_rubric(benchmark)

        # Self-eval
        self_prompt = build_self_eval_prompt(output, rubric)
        self_result = run_eval(self_prompt, timeout=60)
        self_eval = parse_eval_yaml(self_result["output"]) if self_result["success"] else None

        # Judge-eval
        judge_prompt = build_judge_eval_prompt(output, rubric)
        judge_result = run_eval(judge_prompt, timeout=60)
        judge_eval = parse_eval_yaml(judge_result["output"]) if judge_result["success"] else None

        if not self_eval and not judge_eval:
            result["error"] = "Both evals failed to parse"
            result["duration_s"] = round(time.time() - start, 1)
            return result

        # Composite
        composite = compute_composite(
            self_eval or {"score": 0, "dimensions": {}, "notes": "parse failed"},
            judge_eval or {"score": 0, "dimensions": {}, "notes": "parse failed"},
        )

        # Save
        save_eval(run_dir, self_eval, judge_eval, composite, blueprint=bp, benchmark=benchmark)
        result["success"] = True
        result["composite"] = composite["composite_score"]
        result["self_score"] = self_eval.get("score", "?") if self_eval else "?"
        result["judge_score"] = judge_eval.get("score", "?") if judge_eval else "?"

    except subprocess.TimeoutExpired:
        result["error"] = "Timeout"
    except Exception as e:
        result["error"] = str(e)[:100]

    result["duration_s"] = round(time.time() - start, 1)
    return result


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    max_workers = 5
    for a in args:
        if a.startswith("--max-workers="):
            max_workers = int(a.split("=", 1)[1])

    runs = find_runs_needing_eval()
    print(f"Runs needing eval: {len(runs)}")
    print(f"Max workers: {max_workers}")
    print()

    if dry_run:
        for r in runs[:10]:
            print(f"  Would eval: {r['blueprint']} / {r['run_id']}")
        print(f"  ... and {len(runs) - 10} more")
        return

    t0 = time.time()
    success = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        fut_map = {executor.submit(evaluate_one, r): r for r in runs}
        for fut in as_completed(fut_map):
            r = fut_map[fut]
            res = fut.result()
            if res["success"]:
                success += 1
                comp = res.get("composite", "?")
                print(f"  [OK] {res['blueprint']:<40} comp={comp} ({res['duration_s']:.0f}s)")
            else:
                failed += 1
                print(f"  [FAIL] {res['blueprint']:<40} {res.get('error', 'unknown')}")

    total = time.time() - t0
    print()
    print(f"=== Eval complete in {total:.0f}s ===")
    print(f"  Evaluated: {success}/{len(runs)}")
    print(f"  Failed:    {failed}/{len(runs)}")
    print(f"  Rate:      {len(runs)/total:.2f} evals/s")

    # Rebuild state
    subprocess.run([sys.executable, str(FORGE_ROOT / "scripts" / "rebuild_state.py")], cwd=str(FORGE_ROOT))


if __name__ == "__main__":
    main()
