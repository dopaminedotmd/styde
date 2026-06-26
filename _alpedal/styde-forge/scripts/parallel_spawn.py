"""
Optimized parallel spawner for Styde Forge.

Spawns N blueprints concurrently via hermes chat -q.
No sequential bottlenecks. No race conditions.
Output dirs created first, spawns fire in parallel.

Usage:
  python scripts/parallel_spawn.py [--max-workers 5] [--blueprint list,of,names]
  python scripts/parallel_spawn.py --all-failed
"""

import sys
import os
import subprocess
import json
import tempfile
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

FORGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_ROOT))

from Core.hermes_bridge import find_hermes, _run_hermes
from Core.spawn import build_spawn_prompt
from Core.blueprint import validate_blueprint


def find_failed_blueprints():
    """Return list of blueprint names with no completed output."""
    refinery = FORGE_ROOT / "StydeAgents" / "refinery"
    blueprints = sorted(d.name for d in (FORGE_ROOT / "blueprints").iterdir() if d.is_dir())
    failed = []
    for bp in blueprints:
        bp_dir = refinery / bp
        if not bp_dir.exists():
            failed.append(bp)
            continue
        runs_dir = bp_dir / "runs"
        if not runs_dir.exists() or not any(runs_dir.iterdir()):
            failed.append(bp)
            continue
        has_output = False
        for run_dir in runs_dir.iterdir():
            output = run_dir / "output.md"
            if output.exists() and output.stat().st_size > 0:
                has_output = True
                break
        if not has_output:
            failed.append(bp)
    return failed


def spawn_one(blueprint_name: str) -> dict:
    """Spawn a single agent. Returns result dict."""
    start = time.time()
    result = {
        "blueprint": blueprint_name,
        "success": False,
        "output_len": 0,
        "duration_s": 0,
        "error": "",
    }

    try:
        errors = validate_blueprint(blueprint_name)
        if errors:
            result["error"] = f"Blueprint validation: {'; '.join(errors)}"
            return result

        spawn = build_spawn_prompt(blueprint_name, caveman=True)
        run_id = spawn["run_id"]
        output_path = Path(spawn["output_path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save spawn context immediately (no race)
        context_data = {
            "blueprint": blueprint_name,
            "benchmark": "manual",
            "run_id": run_id,
            "caveman": True,
            "spawned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        import yaml
        (output_path.parent / "spawn_context.yaml").write_text(
            yaml.dump(context_data, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )

        # Fire hermes
        hermes_result = _run_hermes(
            prompt=spawn["goal"],
            model="deepseek-v4-flash",
            toolsets=spawn["toolsets"],
            timeout=300,
        )

        if hermes_result["success"]:
            output_path.write_text(hermes_result["output"], encoding="utf-8")
            result["success"] = True
            result["output_len"] = len(hermes_result["output"])
        else:
            result["error"] = hermes_result["stderr"][:200] or "empty response"

    except Exception as e:
        result["error"] = str(e)[:200]

    result["duration_s"] = round(time.time() - start, 1)
    return result


def append_agent_to_journal(agent_entry: dict):
    """Append one agent entry to the journal file (atomic append, no race)."""
    journal = FORGE_ROOT / "99_INDEXES" / "agent_journal.yaml"
    journal.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    line = yaml.dump([agent_entry], default_flow_style=False, allow_unicode=True)
    with open(journal, "a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        os.fsync(f.fileno())


def main():
    args = sys.argv[1:]

    if "--all-failed" in args:
        blueprints = find_failed_blueprints()
        print(f"Re-spawning {len(blueprints)} failed blueprints...")
    elif any(b.startswith("--blueprint=") for b in args):
        for a in args:
            if a.startswith("--blueprint="):
                blueprints = [b.strip() for b in a.split("=", 1)[1].split(",")]
                break
        else:
            blueprints = []
    else:
        # Default: all 149
        blueprints = sorted(d.name for d in (FORGE_ROOT / "blueprints").iterdir() if d.is_dir())
        print(f"Spawning all {len(blueprints)} blueprints...")

    max_workers = 5
    for a in args:
        if a.startswith("--max-workers="):
            max_workers = int(a.split("=", 1)[1])

    print(f"Max parallel workers: {max_workers}")
    print()

    t0 = time.time()
    success = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        fut_map = {executor.submit(spawn_one, bp): bp for bp in blueprints}

        for fut in as_completed(fut_map):
            bp = fut_map[fut]
            res = fut.result()
            status = "OK" if res["success"] else "FAIL"
            dur = res["duration_s"]

            if res["success"]:
                success += 1
                print(f"  [{status}] {bp} — {res['output_len']:>6} chars, {dur:>5.1f}s")
            else:
                failed += 1
                err = res["error"]
                print(f"  [{status}] {bp} — {dur:>5.1f}s, {err}")

    total = time.time() - t0
    print()
    print(f"=== Done in {total:.0f}s ===")
    print(f"  Succeeded: {success}/{len(blueprints)}")
    print(f"  Failed:    {failed}/{len(blueprints)}")
    print(f"  Rate:      {len(blueprints)/total:.2f} bp/s")

    # Update state: rebuild from filesystem
    os.system(f'python "{FORGE_ROOT / "scripts" / "rebuild_state.py"}"')


if __name__ == "__main__":
    main()
