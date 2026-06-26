"""
Production promotion pipeline for Styde Forge.
Scans all runs, finds agents with 3+ consecutive >=85,
promotes them to production/ directory.

Usage:
  python scripts/promote_production.py [--dry-run] [--force]
"""
import sys, shutil, yaml, time
from pathlib import Path
from datetime import datetime, timezone

FORGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_ROOT))

REFINERY = FORGE_ROOT / "StydeAgents" / "refinery"
PRODUCTION = FORGE_ROOT / "StydeAgents" / "production"


def find_promotion_candidates() -> list[dict]:
    """Find blueprints with 3+ consecutive runs scoring >= 85."""
    candidates = []
    for bp_dir in sorted(REFINERY.iterdir()):
        if not bp_dir.is_dir():
            continue
        bp_name = bp_dir.name
        runs_dir = bp_dir / "runs"
        if not runs_dir.exists():
            continue

        # Collect all eval scores, sorted by run timestamp
        run_scores = []
        for run_dir in sorted(runs_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            ev = run_dir / "eval.yaml"
            if not ev.exists():
                continue
            try:
                data = yaml.safe_load(ev.read_text()) or {}
                composite = data.get("composite", {})
                score = composite.get("composite_score", 0)
                ts = data.get("timestamp", "0")
                run_scores.append((ts, score, run_dir.name))
            except Exception:
                continue

        if not run_scores:
            continue

        run_scores.sort()
        # Check last N runs for consecutive >= 85
        consecutive = 0
        for ts, score, rid in reversed(run_scores):
            if score >= 85:
                consecutive += 1
            else:
                break  # break chain

        if consecutive >= 3:
            # Verify not already promoted
            prod_dir = PRODUCTION / bp_name
            if prod_dir.exists():
                continue

            best = max(score for _, score, _ in run_scores)
            candidates.append({
                "blueprint": bp_name,
                "consecutive": consecutive,
                "best_score": best,
                "total_runs": len(run_scores),
                "promote_run": run_scores[-1][2],
            })

    return candidates


def promote(candidate: dict) -> bool:
    """Move blueprint from refinery to production."""
    bp = candidate["blueprint"]
    src = REFINERY / bp
    dst = PRODUCTION / bp

    if not src.exists():
        return False

    dst.mkdir(parents=True, exist_ok=True)

    # Copy blueprint files to production
    for item in src.iterdir():
        s = str(item)
        d = str(dst / item.name)
        if item.is_dir():
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Write promotion badge
    badge = {
        "blueprint": bp,
        "promoted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "consecutive_passes": candidate["consecutive"],
        "best_score": candidate["best_score"],
        "total_runs": candidate["total_runs"],
    }
    (dst / "production_badge.yaml").write_text(
        yaml.dump(badge, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Remove all .need_respawn flags
    for run_dir in src.rglob(".need_respawn"):
        run_dir.unlink()

    print(f"  [PROMOTE] {bp:<40} score={candidate['best_score']} ({candidate['consecutive']}x ≥85)")
    return True


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    force = "--force" in args

    candidates = find_promotion_candidates()
    print(f"Production candidates: {len(candidates)}")

    if not candidates:
        print("No one ready for promotion yet.")
        return

    print(f"{'Blueprint':<45} {'Best':>5} {'Consec':>6} {'Runs':>5}")
    print("-" * 65)
    for c in candidates:
        print(f"{c['blueprint']:<45} {c['best_score']:>5.0f} {c['consecutive']:>6} {c['total_runs']:>5}")

    if dry_run:
        print(f"\nDry-run: {len(candidates)} would be promoted")
        return

    promoted = 0
    for c in candidates:
        if promote(c):
            promoted += 1

    print(f"\nPromoted: {promoted}/{len(candidates)} to production/")

    # Rebuild state
    subprocess.run([sys.executable, str(FORGE_ROOT / "scripts" / "rebuild_state.py")],
                   cwd=str(FORGE_ROOT))


if __name__ == "__main__":
    import subprocess
    main()
