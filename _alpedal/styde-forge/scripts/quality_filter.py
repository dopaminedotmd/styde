"""
Output quality detector for Styde Forge.
Finds runs with poor outputs and flags them for re-spawn.

Usage:
  python scripts/quality_filter.py [--min-chars 300] [--list] [--fix]
"""

import sys
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FORGE_ROOT))


def scan_outputs(min_chars: int = 300) -> list[dict]:
    """Find runs with outputs shorter than min_chars or suspiciously low quality."""
    refinery = FORGE_ROOT / "StydeAgents" / "refinery"
    poor = []

    for bp_dir in sorted(refinery.iterdir()):
        if not bp_dir.is_dir():
            continue
        bp_name = bp_dir.name
        runs_dir = bp_dir / "runs"
        if not runs_dir.exists():
            continue

        for run_dir in sorted(runs_dir.iterdir()):
            output_file = run_dir / "output.md"
            if not output_file.exists():
                poor.append({
                    "blueprint": bp_name,
                    "run_id": run_dir.name.replace("run-", ""),
                    "issue": "no output file",
                    "chars": 0,
                    "run_dir": run_dir,
                })
                continue

            size = output_file.stat().st_size

            # Check: empty file
            if size == 0:
                poor.append({
                    "blueprint": bp_name,
                    "run_id": run_dir.name.replace("run-", ""),
                    "issue": "empty file",
                    "chars": 0,
                    "run_dir": run_dir,
                })
                continue

            # Read content
            content = output_file.read_text(encoding="utf-8", errors="replace")
            char_count = len(content)

            # Check: too short
            if char_count < min_chars:
                poor.append({
                    "blueprint": bp_name,
                    "run_id": run_dir.name.replace("run-", ""),
                    "issue": f"too short ({char_count} < {min_chars})",
                    "chars": char_count,
                    "run_dir": run_dir,
                })
                continue

            # Check: looks like an error message
            first_line = content.split("\n")[0].lower() if content else ""
            if any(phrase in first_line for phrase in
                   ["error", "failed", "timeout", "permission", "unboundlocal",
                    "traceback", "syntax error", "keyerror", "filenotfound"]):
                poor.append({
                    "blueprint": bp_name,
                    "run_id": run_dir.name.replace("run-", ""),
                    "issue": f"error-like output: {first_line[:60]}",
                    "chars": char_count,
                    "run_dir": run_dir,
                })

    return poor


def main():
    args = sys.argv[1:]
    min_chars = 300
    just_list = "--list" in args
    do_fix = "--fix" in args

    for a in args:
        if a.startswith("--min-chars="):
            min_chars = int(a.split("=", 1)[1])

    poor = scan_outputs(min_chars)

    if just_list:
        if not poor:
            print("All outputs pass quality check.")
        else:
            print(f"Poor outputs ({len(poor)}):")
            for p in poor:
                print(f"  {p['blueprint']:<45} {p['issue']}")
        return

    # Summary
    print(f"Poor outputs: {len(poor)}")
    for p in poor:
        print(f"  {p['blueprint']:<45} {p['issue']}")

    if do_fix and poor:
        print()
        print("Flagging for re-spawn...")
        for p in poor:
            run_dir = p["run_dir"]
            # Create a .need_respawn flag file
            (run_dir / ".need_respawn").write_text(
                f"Issue: {p['issue']}\nChars: {p['chars']}\n", encoding="utf-8"
            )
        print(f"  {len(poor)} runs flagged with .need_respawn")

    if poor:
        # Show re-spawn command
        bps = sorted(set(p["blueprint"] for p in poor))
        print()
        print(f"Re-spawn {len(poor)} runs across {len(bps)} blueprints:")
        print(f"  python scripts/parallel_spawn.py --blueprint={','.join(bps)}")


if __name__ == "__main__":
    main()
