"""Rebuild state.yaml from actual filesystem data."""
import yaml
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent
state_file = FORGE_ROOT / "state.yaml"
old_state = yaml.safe_load(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}

agents = []
blueprint_set = set()
refinery = FORGE_ROOT / "StydeAgents" / "refinery"

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
        ctx_file = run_dir / "spawn_context.yaml"
        output_file = run_dir / "output.md"

        agent = {
            "blueprint": bp_name,
            "run_id": run_dir.name.replace("run-", ""),
            "stage": "refinery",
            "status": "spawned",
        }

        if ctx_file.exists():
            try:
                ctx = yaml.safe_load(ctx_file.read_text(encoding="utf-8"))
                agent["spawned_at"] = ctx.get("spawned_at", "")
                agent["benchmark"] = ctx.get("benchmark", "manual")
                agent["iteration"] = ctx.get("iteration", 1)
            except Exception:
                pass

        if output_file.exists() and output_file.stat().st_size > 0:
            agent["status"] = "completed"

        agents.append(agent)
        blueprint_set.add(bp_name)

new_state = {
    "forge_version": old_state.get("forge_version", "3.0.0"),
    "forge_codename": old_state.get("forge_codename", "The Crucible"),
    "hardware_profile": old_state.get("hardware_profile", "pontus-main"),
    "caveman_ultra": True,
    "loop_iterations": old_state.get("loop_iterations", 0),
    "total_agents_spawned": len(agents),
    "total_evaluations": 0,
    "blueprints": sorted(blueprint_set),
    "agents": agents,
    "evaluations": [],
    "improvements": [],
    "last_checkpoint": old_state.get("last_checkpoint"),
}

content = yaml.dump(new_state, default_flow_style=False, allow_unicode=True)
state_file.write_text(content, encoding="utf-8")
print(f"State rebuilt: {len(blueprint_set)} blueprints, {len(agents)} agents")
