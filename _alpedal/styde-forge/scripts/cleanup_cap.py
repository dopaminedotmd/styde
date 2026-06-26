"""
Cleanup & cap tool for Styde Forge.
- Caps retries per blueprint (archive after N failed runs)
- Cleans up .need_respawn flags for already-archived
- Removes stale 0-byte output files

Usage:
  python scripts/cleanup_cap.py [--max-runs 5] [--dry-run] [--archive-failed]
"""
import sys, yaml, shutil
from pathlib import Path
from datetime import datetime, timezone

FORGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_ROOT))
REFINERY = FORGE_ROOT / "StydeAgents" / "refinery"
ARCHIVE = FORGE_ROOT / "StydeAgents" / "archive"


def main():
    args = sys.argv[1:]
    max_runs = 5
    dry_run = "--dry-run" in args
    archive_failed = "--archive-failed" in args
    for a in args:
        if a.startswith("--max-runs="):
            max_runs = int(a.split("=", 1)[1])

    ARCHIVE.mkdir(parents=True, exist_ok=True)

    archived = 0
    for bp_dir in sorted(REFINERY.iterdir()):
        if not bp_dir.is_dir():
            continue
        bp_name = bp_dir.name
        runs_dir = bp_dir / "runs"
        if not runs_dir.exists():
            continue

        # Collect runs with scores
        scored_runs = []
        for run_dir in sorted(runs_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            score = 0
            tr = run_dir / "teacher_review.yaml"
            if tr.exists():
                try:
                    d = yaml.safe_load(tr.read_text()) or {}
                    score = 1  # has any teacher review
                    st = d.get("stage", "")
                    if st == "production":
                        score = 3
                    elif st == "refinery":
                        score = 2
                except Exception:
                    pass
            # Higher score for newer runs with valid output
            of = run_dir / "output.md"
            if of.exists() and of.stat().st_size > 500:
                score += 0.5
            scored_runs.append((score, run_dir.name, run_dir))

        # Sort by score DESC, then name DESC (newest first for ties)
        scored_runs.sort(key=lambda x: (-x[0], -int(x[1].replace("run-", "").replace("-", "").replace(":", ""))))

        total = len(scored_runs)
        if total <= max_runs:
            continue

        # Archive lowest-scored runs beyond max_runs
        to_remove = total - max_runs
        for score, rid, run_dir in scored_runs[-to_remove:]:
            if not dry_run:
                arch_dir = ARCHIVE / bp_name / rid
                arch_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(run_dir), str(arch_dir))
                archived += 1
                label = "prod" if score >= 3 else "ref" if score >= 2 else "fail"
                print(f"  [ARCHIVE] {bp_name:<40} {rid} ({label})")

        # 2. Clean stale .need_respawn flags for runs that have teacher_review
        for score, rid, run_dir in scored_runs:
            if not run_dir.is_dir():
                continue
            nr = run_dir / ".need_respawn"
            tr = run_dir / "teacher_review.yaml"
            if nr.exists() and tr.exists():
                if not dry_run:
                    nr.unlink()
                print(f"  [CLEAN] {bp_name:<40} {run_dir.name} — .need_respawn removed (has teacher)")

        # 3. Remove 0-byte output files
        for score, rid, run_dir in scored_runs:
            if not run_dir.is_dir():
                continue
            of = run_dir / "output.md"
            if of.exists() and of.stat().st_size == 0:
                if not dry_run:
                    of.unlink()
                print(f"  [CLEAN] {bp_name:<40} {run_dir.name} — 0-byte output removed")

    print(f"\n=== Done ===")
    print(f"  Archived: {archived}")
    if dry_run:
        print(f"  (dry-run — no changes made)")


if __name__ == "__main__":
    main()
