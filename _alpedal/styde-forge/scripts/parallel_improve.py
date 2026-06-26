"""
Parallel improve pipeline for Styde Forge.
For each blueprint with evaluated runs: teacher analysis → version bump → stage determination.

Usage:
  python scripts/parallel_improve.py [--max-workers 5] [--dry-run]
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
from Core.teacher import (
    build_teacher_prompt, parse_teacher_response,
    save_teacher_review, apply_improvement,
    should_retry, determine_stage,
)
from Core.hermes_bridge import run_teacher
from Core.state import save_state, load_state


def find_blueprints_with_evals():
    """Find blueprints that have at least one run with eval.yaml but no teacher_review.yaml."""
    refinery = FORGE_ROOT / "StydeAgents" / "refinery"
    result = []
    for bp_dir in sorted(refinery.iterdir()):
        if not bp_dir.is_dir():
            continue
        bp_name = bp_dir.name
        runs_dir = bp_dir / "runs"
        if not runs_dir.exists():
            continue

        # Find latest run with eval.yaml but no teacher_review.yaml
        runs_with_eval = []
        for run_dir in sorted(runs_dir.iterdir()):
            eval_file = run_dir / "eval.yaml"
            review_file = run_dir / "teacher_review.yaml"
            if eval_file.exists() and not review_file.exists():
                runs_with_eval.append(run_dir)

        if runs_with_eval:
            latest = runs_with_eval[-1]  # Most recent
            result.append({
                "blueprint": bp_name,
                "run_dir": latest,
                "run_id": latest.name.replace("run-", ""),
                "total_evals": len(runs_with_eval),
            })

    return result


def improve_one(info: dict) -> dict:
    """Run teacher analysis on a single run."""
    start = time.time()
    bp = info["blueprint"]
    run_dir = info["run_dir"]
    result = {"blueprint": bp, "run_id": info["run_id"], "success": False, "duration_s": 0}

    try:
        eval_file = run_dir / "eval.yaml"
        eval_data = yaml.safe_load(eval_file.read_text(encoding="utf-8")) or {}
        composite = eval_data.get("composite", {})
        score = composite.get("composite_score", 0)

        # Build teacher prompt
        teacher_prompt = build_teacher_prompt(eval_data)
        teacher_result = run_teacher(teacher_prompt, timeout=90)
        review = parse_teacher_response(teacher_result["output"]) if teacher_result["success"] else None

        if not review:
            result["error"] = "Teacher parse failed"
            result["duration_s"] = round(time.time() - start, 1)
            return result

        # Determine stage before saving
        stage = determine_stage(score, consecutive_passes=1 if score >= 85 else 0)
        review["stage"] = stage

        # Save review
        save_teacher_review(run_dir, review)

        # Apply improvement (version bump)
        new_version = apply_improvement(bp, score, review)
        result["success"] = True
        result["score"] = score
        result["version"] = new_version
        result["diagnosis"] = review.get("diagnosis", {}).get("severity", "?")
        result["stage"] = stage

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

    runs = find_blueprints_with_evals()
    print(f"Blueprints needing teacher review: {len(runs)}")
    print(f"Max workers: {max_workers}")
    print()

    if dry_run:
        for r in runs[:10]:
            print(f"  Would review: {r['blueprint']} ({r['total_evals']} evals pending)")
        print(f"  ... and {len(runs) - 10} more")
        return

    t0 = time.time()
    success = 0
    failed = 0
    production = []
    refinery = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        fut_map = {executor.submit(improve_one, r): r for r in runs}
        for fut in as_completed(fut_map):
            r = fut_map[fut]
            res = fut.result()
            stage = res.get("stage", "?")
            if res["success"]:
                success += 1
                ver = res.get("version", "?")
                score = res.get("score", "?")
                print(f"  [OK] {res['blueprint']:<40} v{ver} score={score} stage={stage} ({res['duration_s']:.0f}s)")
                if stage == "production":
                    production.append(res["blueprint"])
                elif stage == "refinery":
                    refinery.append(res["blueprint"])
            else:
                failed += 1
                print(f"  [FAIL] {res['blueprint']:<40} {res.get('error', 'unknown')}")

    total = time.time() - t0
    print()
    print(f"=== Improve complete in {total:.0f}s ===")
    print(f"  Reviewed: {success}/{len(runs)}")
    print(f"  Failed:   {failed}/{len(runs)}")
    print(f"  Production candidates: {len(production)}")
    print(f"  Refinery: {len(refinery)}")

    subprocess.run([sys.executable, str(FORGE_ROOT / "scripts" / "rebuild_state.py")], cwd=str(FORGE_ROOT))


if __name__ == "__main__":
    main()
