#!/usr/bin/env python3
"""
hund-forge CLI — Persona Refinement Engine for Hund.

Commands:
  status                              Visa forge-status
  spawn <blueprint> <benchmark>       Bygg spawn-prompt for Hund-agent
  eval <run_id>                       Bygg eval-prompt (sjalv + domare)
  improve <run_id>                    Bygg teacher-prompt for forbattringar
  loop <blueprint> <benchmark>        Komplett cykel (prompter for alla steg)
  runs [blueprint]                    Lista senaste korningar

Alla kommandon genererar prompter. Ingenting kors automatiskt.
William kopierar prompter till valfri LLM och sparar resultat.
"""

import sys
from pathlib import Path

# Ensure engine is importable
FORGE_ROOT = Path(__file__).resolve().parent
if str(FORGE_ROOT) not in sys.path:
    sys.path.insert(0, str(FORGE_ROOT))

from engine.core import (
    load_state, save_state, create_run, update_run,
    get_run_dir, list_runs, BLUEPRINTS_DIR, BENCHMARKS_DIR,
)
from engine.spawn import build_spawn_prompt
from engine.evaluate import build_self_eval_prompt, build_judge_eval_prompt
from engine.teacher import build_teacher_prompt


SEP = "=" * 60


def cmd_status():
    """Show forge status."""
    state = load_state()
    print(f"hund-forge v{state.get('forge_version', '?')} — {state.get('forge_codename', '?')}")
    print(f"Loop iterationer: {state.get('loop_iterations', 0)}")
    print(f"Totala spawns:    {state.get('total_spawns', 0)}")
    print(f"Totala evals:     {state.get('total_evals', 0)}")
    print()
    print("Blueprints:")
    for bp in state.get("blueprints", []):
        print(f"  - {bp}")
    runs = state.get("runs", [])
    if runs:
        latest = runs[-1]
        print(f"\nSenaste korning: {latest['run_id']} ({latest.get('status', '?')})")


def cmd_spawn(blueprint: str, benchmark: str):
    """Build and output spawn prompt."""
    print(f"{SEP}")
    print(f"SPAWN-PROMPT: {blueprint} / {benchmark}")
    print(f"{SEP}")
    print()

    # Create run entry
    run = create_run(blueprint, benchmark)
    print(f"Run ID: {run['run_id']}")
    print(f"Output path: {run['output_path']}")
    print()

    # Build prompt
    prompt = build_spawn_prompt(blueprint, benchmark)
    print("=== KOPIERA DETTA TILL DIN LLM ===")
    print()
    print(prompt["goal"])
    print()
    print(f"{SEP}")
    print("NAR AGENTEN SVARAT — spara output till:")
    print(f"  {run['output_path']}")
    print(f"Kor sedan: python cli.py eval {run['run_id']}")


def cmd_eval(run_id: str):
    """Build eval prompts from agent output."""
    state = load_state()
    run = None
    for r in state.get("runs", []):
        if r["run_id"] == run_id:
            run = r
            break

    if not run:
        print(f"ERROR: Ingen korning med id {run_id}")
        sys.exit(1)

    output_path = Path(run["output_path"])
    if not output_path.exists():
        print(f"ERROR: Output-fil saknas: {output_path}")
        print("Har agenten svarat? Spara svaret till output.md forst.")
        sys.exit(1)

    agent_output = output_path.read_text(encoding="utf-8")
    benchmark = run.get("benchmark", "persona-consistency")

    # Self-eval prompt
    print(f"{SEP}")
    print(f"SJALV-EVAL-PROMPT: {run_id}")
    print(f"{SEP}")
    print()
    self_prompt = build_self_eval_prompt(agent_output, benchmark)
    print(self_prompt)
    print()
    print(f"{SEP}")

    # Save self-eval prompt
    self_path = get_run_dir(run_id) / "self_eval_prompt.txt"
    self_path.write_text(self_prompt, encoding="utf-8")
    print(f"Sjalv-eval prompt sparad: {self_path}")

    print()
    print(f"{SEP}")
    print(f"DOMAR-EVAL-PROMPT: {run_id}")
    print(f"{SEP}")
    print()
    judge_prompt = build_judge_eval_prompt(agent_output, benchmark)
    print(judge_prompt)
    print()
    print(f"{SEP}")

    # Save judge-eval prompt
    judge_path = get_run_dir(run_id) / "judge_eval_prompt.txt"
    judge_path.write_text(judge_prompt, encoding="utf-8")
    print(f"Domar-eval prompt sparad: {judge_path}")
    print()
    print("NAR BADA EVALS KLARA — spara sjalv-eval till: self_eval_response.yaml")
    print(f"  och domar-eval till: judge_eval_response.yaml")
    print(f"Kor sedan: python cli.py improve {run_id}")


def cmd_improve(run_id: str):
    """Build teacher prompt from eval results."""
    run_dir = get_run_dir(run_id)

    # Find eval files
    self_path = run_dir / "self_eval_response.yaml"
    judge_path = run_dir / "judge_eval_response.yaml"

    if not self_path.exists():
        print(f"ERROR: Sjalv-eval saknas: {self_path}")
        print("Kor 'python cli.py eval {run_id}' forst och spara resultaten.")
        sys.exit(1)
    if not judge_path.exists():
        print(f"ERROR: Domar-eval saknas: {judge_path}")
        sys.exit(1)

    # Load agent output
    state = load_state()
    run = None
    for r in state.get("runs", []):
        if r["run_id"] == run_id:
            run = r
            break

    output_path = Path(run["output_path"])
    agent_output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""

    # Parse evals (simple YAML)
    import yaml
    try:
        self_eval = yaml.safe_load(self_path.read_text(encoding="utf-8"))
    except Exception:
        self_eval = {}
    try:
        judge_eval = yaml.safe_load(judge_path.read_text(encoding="utf-8"))
    except Exception:
        judge_eval = {}

    print(f"{SEP}")
    print(f"TEACHER-PROMPT: {run_id}")
    print(f"{SEP}")
    print()

    teacher_prompt = build_teacher_prompt(
        agent_output,
        self_eval.get("evaluation", {}) if self_eval else {},
        judge_eval.get("judge_evaluation", {}) if judge_eval else {},
        run.get("blueprint", "hund-persona"),
    )
    print(teacher_prompt)
    print()
    print(f"{SEP}")

    # Save teacher prompt
    teacher_path = run_dir / "teacher_prompt.txt"
    teacher_path.write_text(teacher_prompt, encoding="utf-8")
    print(f"Teacher prompt sparad: {teacher_path}")
    print()
    print("NAR TEACHER SVARAT — spara till: teacher_response.yaml")
    print(f"Sedan: uppdatera blueprints/hund-persona/ med forbattringarna.")
    print(f"Avsluta med: python cli.py status  (loop-raknaren okar)")


def cmd_loop(blueprint: str, benchmark: str):
    """Output all prompts for a complete cycle."""
    print("=== KOMPLETT LOOP: SPAWN -> EVAL -> IMPROVE ===\n")

    # Step 1: Spawn
    cmd_spawn(blueprint, benchmark)

    print("\n\n")
    print(f"{SEP}")
    print("EFTER AGENTEN SVARAT:")
    print(f"  python cli.py eval <run_id>")
    print(f"  (kopiera sjalv-eval + domar-eval prompter)")
    print(f"  (spara resultat som YAML)")
    print(f"  python cli.py improve <run_id>")
    print(f"  (kopiera teacher prompt)")
    print(f"  (spara teacher resultat som YAML)")
    print(f"  (applicera forbattringar)")
    print(f"{SEP}")


def cmd_runs(blueprint: str = None, limit: int = 10):
    """List recent runs."""
    runs = list_runs(blueprint, limit)
    if not runs:
        print("Inga korningar an.")
        return

    print(f"{'RUN ID':<20} {'BLUEPRINT':<25} {'STATUS':<15} {'STARTAD'}")
    print("-" * 80)
    for r in runs:
        rid = r["run_id"]
        bp = r.get("blueprint", "?")
        status = r.get("status", "?")
        started = r.get("started_at", "?")[:16]
        print(f"{rid:<20} {bp:<25} {status:<15} {started}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "status":
        cmd_status()
    elif cmd == "spawn":
        if len(sys.argv) < 4:
            print("Anvandning: python cli.py spawn <blueprint> <benchmark>")
            sys.exit(1)
        cmd_spawn(sys.argv[2], sys.argv[3])
    elif cmd == "eval":
        if len(sys.argv) < 3:
            print("Anvandning: python cli.py eval <run_id>")
            sys.exit(1)
        cmd_eval(sys.argv[2])
    elif cmd == "improve":
        if len(sys.argv) < 3:
            print("Anvandning: python cli.py improve <run_id>")
            sys.exit(1)
        cmd_improve(sys.argv[2])
    elif cmd == "loop":
        if len(sys.argv) < 4:
            print("Anvandning: python cli.py loop <blueprint> <benchmark>")
            sys.exit(1)
        cmd_loop(sys.argv[2], sys.argv[3])
    elif cmd == "runs":
        bp = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_runs(bp)
    else:
        print(f"Okant kommando: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
