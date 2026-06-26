"""
Run ALL blueprints through forge loop-parallel in batches of 3.
Uses subprocess (not direct import) to avoid Python buffering issues.
"""
import subprocess
import sys
import time
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent
BP_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"
FORGE_PY = str(FORGE_ROOT / "Core" / "forge.py")

def get_all_blueprint_names():
    names = sorted(
        d.name for d in BP_DIR.iterdir()
        if d.is_dir() and (d / "BLUEPRINT.md").exists()
    )
    return names

def run_batch(batch_size=3, max_iter=10):
    names = get_all_blueprint_names()
    total = len(names)
    print(f"RUNNING ALL {total} BLUEPRINTS TO PRODUCTION")
    print(f"Batch size: {batch_size} | Max iter per BP: {max_iter}")
    print(f"Caveman Ultra: ON | Model: deepseek-v4-flash\n", flush=True)

    start_time = time.time()
    completed = 0

    for i in range(0, total, batch_size):
        batch = names[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size

        bp_csv = ",".join(batch)
        cmd = [
            sys.executable, FORGE_PY,
            "loop-parallel", bp_csv,
            "--max", str(max_iter),
            "--w", str(len(batch)),
        ]

        print(f"--- Batch {batch_num}/{total_batches}: {', '.join(batch)} ---", flush=True)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=7200)

        if result.stdout:
            # Print last few lines
            lines = result.stdout.strip().split("\n")
            for line in lines[-5:]:
                print(f"  {line}", flush=True)

        if result.returncode == 0:
            completed += len(batch)
            print(f"  ✓ Batch {batch_num} done", flush=True)
        else:
            print(f"  ✗ Batch {batch_num} FAILED (exit {result.returncode})", flush=True)
            if result.stderr:
                for line in result.stderr.strip().split("\n")[-3:]:
                    print(f"  ERR: {line}", flush=True)

        elapsed = time.time() - start_time
        rate = completed / max(elapsed, 1) * 3600
        remaining = total - completed
        eta = remaining / max(rate, 0.01) * 3600 if rate > 0 else 0
        print(f"  Progress: {completed}/{total} ({completed/total*100:.0f}%) | "
              f"{elapsed/60:.0f}m elapsed | ~{eta/60:.0f}m remaining", flush=True)

    elapsed = time.time() - start_time
    print(f"\nALL DONE! {completed}/{total} blueprints processed")
    print(f"Total time: {elapsed/60:.1f}m ({elapsed/3600:.1f}h)", flush=True)

if __name__ == "__main__":
    bs = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    mi = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print(f"Found {len(get_all_blueprint_names())} blueprints", flush=True)
    run_batch(batch_size=bs, max_iter=mi)
