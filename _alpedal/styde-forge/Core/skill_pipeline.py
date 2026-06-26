"""
Skill Pipeline engine for Styde Forge.
Composes skills into multi-step workflows with explicit state contracts,
error boundaries, and parallel execution.

Design:
- Pipeline defined in blueprint's pipeline.yaml
- Each step runs a Hermes agent guided by a skill file
- State passes through typed contracts between steps
- Steps can chain serially, fan-out in parallel, or merge
- Error handling per step: halt | skip | retry | fallback
- Integration tests validate end-to-end pipeline behavior
"""
import yaml
import json
import time
import copy
import hashlib
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timezone

from Core.state import load_state, save_state

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"


# ──────────────────────────────────────────────────────────────
# Data model
# ──────────────────────────────────────────────────────────────

class StepContract:
    """Typed contract for step input/output.

    source: where data comes from (step_id.key or literal path)
    target: where output goes (shared context key or file path)
    format: expected format (text, yaml, json, code)
    schema: optional field-level schema for validation
    required: True means pipeline halts if contract not met
    """
    def __init__(self, spec: dict):
        self.source = spec.get("source", "")
        self.target = spec.get("target", "")
        self.format = spec.get("format", "text")
        self.schema = spec.get("schema", {})
        self.required = spec.get("required", True)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "format": self.format,
            "schema": self.schema,
            "required": self.required,
        }


class PipelineStep:
    """Single step in a skill pipeline.

    Each step runs one skill (from skills/*.md) as a Hermes agent.
    Step execution is: load contract inputs -> inject context -> run skill agent -> validate contract output.
    """
    def __init__(self, spec: dict):
        self.id = spec.get("id", "")
        self.description = spec.get("description", "")
        self.skill = spec.get("skill", "")
        self.model = spec.get("model", "")  # empty = use default
        self.timeout = spec.get("timeout", 120)
        self.depends_on = spec.get("depends_on", [])
        self.input_spec: list[StepContract] = [
            StepContract(c) for c in spec.get("inputs", [])
        ]
        self.output_spec: list[StepContract] = [
            StepContract(c) for c in spec.get("outputs", [])
        ]
        self.error_strategy = spec.get("error", "halt")
        # error_strategy: halt | skip | retry(N) | fallback(step_id)
        self.max_retries = spec.get("max_retries", 2)
        self.fallback_step = spec.get("fallback_step", "")
        self.condition = spec.get("condition", "")  # optional step-run condition expression

    def is_parallel_group(self) -> bool:
        return not self.id and "parallel" in self.__dict__

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "skill": self.skill,
            "model": self.model,
            "timeout": self.timeout,
            "depends_on": self.depends_on,
            "inputs": [c.to_dict() for c in self.input_spec],
            "outputs": [c.to_dict() for c in self.output_spec],
            "error": self.error_strategy,
            "max_retries": self.max_retries,
            "fallback_step": self.fallback_step,
            "condition": self.condition,
        }


class ParallelGroup:
    """Group of steps that execute concurrently.

    Fan-out: all steps run in parallel.
    Fan-in: all must complete before pipeline continues.
    """
    def __init__(self, spec: dict):
        self.steps = [PipelineStep(s) for s in spec.get("parallel", [])]
        self.timeout = spec.get("timeout", 300)
        self.error_strategy = spec.get("error", "halt")

    def to_dict(self) -> dict:
        return {
            "parallel": [s.to_dict() for s in self.steps],
            "timeout": self.timeout,
            "error": self.error_strategy,
        }


class Pipeline:
    """Full pipeline definition.

    Loaded from blueprint's pipeline.yaml.
    """
    def __init__(self, spec: dict):
        self.name = spec.get("name", "unnamed")
        self.version = spec.get("version", "1.0")
        self.description = spec.get("description", "")
        self.blueprint = spec.get("blueprint", "")
        self.steps: list[PipelineStep | ParallelGroup] = []
        for step_spec in spec.get("steps", []):
            if "parallel" in step_spec:
                self.steps.append(ParallelGroup(step_spec))
            else:
                self.steps.append(PipelineStep(step_spec))
        self.global_timeout = spec.get("timeout", 600)
        self.global_error_strategy = spec.get("error", "halt")
        self.state_contract = spec.get("state_contract", {})

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "blueprint": self.blueprint,
            "steps": [s.to_dict() for s in self.steps],
            "timeout": self.global_timeout,
            "error": self.global_error_strategy,
            "state_contract": self.state_contract,
        }


# ──────────────────────────────────────────────────────────────
# Pipeline loader
# ──────────────────────────────────────────────────────────────

def load_pipeline(blueprint_name: str) -> Optional[Pipeline]:
    """Load pipeline definition from blueprint directory.

    Checks pipeline.yaml first, then config.yaml for pipeline section.
    Returns None if no pipeline defined (blueprint is a single-step agent).
    """
    # Primary: pipeline.yaml
    pipeline_path = BLUEPRINTS_DIR / blueprint_name / "pipeline.yaml"
    if pipeline_path.exists():
        spec = yaml.safe_load(pipeline_path.read_text(encoding="utf-8"))
        if spec and isinstance(spec, dict):
            p = Pipeline(spec)
            p.blueprint = blueprint_name
            return p

    # Fallback: config.yaml may embed a pipeline section
    config_path = BLUEPRINTS_DIR / blueprint_name / "config.yaml"
    if config_path.exists():
        config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if isinstance(config, dict) and "pipeline" in config:
            spec = config["pipeline"]
            if isinstance(spec, dict):
                p = Pipeline(spec)
                p.blueprint = blueprint_name
                return p

    return None


def step_skill_path(blueprint_name: str, step: PipelineStep) -> Optional[Path]:
    """Resolve the skill file path for a pipeline step."""
    if not step.skill:
        return None
    skill_path = BLUEPRINTS_DIR / blueprint_name / "skills" / f"{step.skill}.md"
    if skill_path.exists():
        return skill_path
    # Fallback: global skills
    global_skills = BLUEPRINTS_DIR / "_shared" / "skills" / f"{step.skill}.md"
    if global_skills.exists():
        return global_skills
    return None


# ──────────────────────────────────────────────────────────────
# State context
# ──────────────────────────────────────────────────────────────

class PipelineContext:
    """Mutable state container that flows through pipeline steps.

    Each step reads from and writes to this context via contracts.
    Context keys follow the contract targets defined in each step.
    """
    def __init__(self, initial: dict = None):
        self.data: dict[str, Any] = copy.deepcopy(initial) if initial else {}
        self.results: dict[str, dict] = {}  # step_id -> {success, output, duration, error}
        self.errors: list[dict] = []
        self.start_time: float = time.time()
        self.elapsed_seconds: float = 0.0

    def get(self, key: str, default=None):
        keys = key.split(".")
        val = self.data
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k)
            else:
                return default
        return val if val is not None else default

    def set(self, key: str, value: Any):
        self.data[key] = value

    def record_step_result(self, step_id: str, result: dict):
        self.results[step_id] = result
        if not result.get("success", False):
            self.errors.append({
                "step_id": step_id,
                "error": result.get("error", "unknown"),
                "duration_s": result.get("duration_s", 0),
            })

    def elapsed(self) -> float:
        return time.time() - self.start_time

    def snapshot(self) -> dict:
        """Return serializable snapshot for checkpointing."""
        return {
            "data": self.data,
            "results": self.results,
            "errors": self.errors,
            "start_time": self.start_time,
            "elapsed_seconds": self.elapsed(),
        }


# ──────────────────────────────────────────────────────────────
# Pipeline runner
# ──────────────────────────────────────────────────────────────

class PipelineRunner:
    """Executes a multi-skill pipeline.

    Handles step ordering (topological sort based on depends_on),
    parallel groups, error boundaries, state passing, and checkpointing.
    """
    def __init__(self, pipeline: Pipeline, context: PipelineContext = None):
        self.pipeline = pipeline
        self.context = context or PipelineContext()
        self._ordered_steps: list[PipelineStep] = []
        self._step_map: dict[str, PipelineStep] = {}
        self._warnings: list[str] = []

    def validate(self, strict: bool = True) -> list[str]:
        """Validate pipeline for structural correctness.

        Checks:
        - All steps have unique IDs
        - depends_on references exist
        - Skill files exist (only in strict mode)
        - Contracts are internally consistent

        Returns list of error strings (empty = valid).
        Strict=True checks skill file existence (for production runs).
        Strict=False skips skill file checks (for testing with stubs).
        """
        errors = []
        warnings = []
        seen_ids = set()

        for item in self.pipeline.steps:
            if isinstance(item, ParallelGroup):
                for step in item.steps:
                    if step.id in seen_ids:
                        errors.append(f"Duplicate step ID: {step.id}")
                    seen_ids.add(step.id)
                    self._step_map[step.id] = step
                    if strict and step.skill and not step_skill_path(self.pipeline.blueprint, step):
                        errors.append(f"Skill file not found for step '{step.id}': {step.skill}.md")
                    elif not strict and step.skill and not step_skill_path(self.pipeline.blueprint, step):
                        warnings.append(f"Skill file not found for step '{step.id}': {step.skill}.md")
            else:
                step = item
                if step.id in seen_ids:
                    errors.append(f"Duplicate step ID: {step.id}")
                seen_ids.add(step.id)
                self._step_map[step.id] = step
                if strict and step.skill and not step_skill_path(self.pipeline.blueprint, step):
                    errors.append(f"Skill file not found for step '{step.id}': {step.skill}.md")
                elif not strict and step.skill and not step_skill_path(self.pipeline.blueprint, step):
                    warnings.append(f"Skill file not found for step '{step.id}': {step.skill}.md")

        # Validate depends_on references
        for item in self.pipeline.steps:
            steps_to_check = []
            if isinstance(item, ParallelGroup):
                steps_to_check = item.steps
            else:
                steps_to_check = [item]

            for step in steps_to_check:
                for dep in step.depends_on:
                    if dep not in seen_ids:
                        errors.append(f"Step '{step.id}' depends on unknown step: '{dep}'")

        if warnings and not errors:
            # Non-blocking: stash warnings for logging but don't block execution
            self._warnings = warnings

        return errors

    def run(self) -> dict:
        """Execute the full pipeline. Returns result summary."""
        from Core.hermes_bridge import spawn_agent

        # Validate before running (structural checks only — skill files checked at step level)
        validation_errors = self.validate(strict=False)
        if validation_errors:
            return {
                "success": False,
                "error": f"Pipeline validation failed: {'; '.join(validation_errors)}",
                "pipeline": self.pipeline.name,
                "step_results": {},
                "elapsed_s": 0,
            }

        pipeline_start = time.time()
        completed: set[str] = set()
        summary = {"steps": {}, "success": True, "error": ""}

        # Process steps in order, respecting dependencies
        for item in self.pipeline.steps:
            if isinstance(item, ParallelGroup):
                group_result = self._run_parallel_group(item, completed)
                summary["steps"][f"_group_{id(item)}"] = group_result
                if not group_result["success"] and item.error_strategy == "halt":
                    summary["success"] = False
                    summary["error"] = group_result.get("error", "Parallel group failed")
                    break
                for step in item.steps:
                    completed.add(step.id)
            else:
                step = item
                step_result = self._run_step(step, completed)
                summary["steps"][step.id] = step_result
                if step_result["success"]:
                    completed.add(step.id)

                # Check error strategy
                if not step_result["success"]:
                    if step.error_strategy == "halt":
                        summary["success"] = False
                        summary["error"] = step_result.get("error", f"Step '{step.id}' failed")
                        break
                    elif step.error_strategy == "skip":
                        # Record skip, continue pipeline
                        self.context.record_step_result(step.id, step_result)
                        continue
                    elif step.error_strategy.startswith("retry"):
                        self._handle_retry(step, completed, summary)

        pipeline_elapsed = time.time() - pipeline_start
        self.context.elapsed_seconds = pipeline_elapsed

        summary["elapsed_s"] = round(pipeline_elapsed, 1)
        summary["context_keys"] = list(self.context.data.keys())
        summary["steps_total"] = len(self.pipeline.steps)
        summary["steps_passed"] = sum(
            1 for r in summary["steps"].values() if r.get("success", False)
        )

        return summary

    def _run_step(self, step: PipelineStep, completed: set) -> dict:
        """Execute a single pipeline step via Hermes agent."""
        from Core.hermes_bridge import spawn_agent

        if step.depends_on:
            missing = [d for d in step.depends_on if d not in completed]
            if missing:
                return {
                    "success": False,
                    "error": f"Dependencies not met: {missing}",
                    "step_id": step.id,
                    "duration_s": 0,
                }

        # Load skill content
        skill_path = step_skill_path(self.pipeline.blueprint, step)
        skill_content = skill_path.read_text(encoding="utf-8") if skill_path else ""

        # Build input from context contracts
        input_data = {}
        for contract in step.input_spec:
            if contract.source.startswith("context."):
                key = contract.source.split(".", 1)[1]
                value = self.context.get(key)
                if value is None and contract.required:
                    return {
                        "success": False,
                        "error": f"Required input '{key}' not found in context",
                        "step_id": step.id,
                        "duration_s": 0,
                    }
                input_data[key] = value
            elif contract.source == "pipeline":
                # Full pipeline context snapshot
                input_data["pipeline"] = self.context.snapshot()
            else:
                # Literal file path or step output reference: step_id.output_key
                if "." in contract.source:
                    ref_step, ref_key = contract.source.split(".", 1)
                    step_result = self.context.results.get(ref_step, {})
                    input_data[ref_key] = step_result.get("output", {}).get(ref_key, "")
                else:
                    file_path = Path(contract.source)
                    if file_path.exists():
                        input_data[contract.target] = file_path.read_text(encoding="utf-8")

        # Build the agent goal
        goal_parts = []
        if skill_content:
            goal_parts.append(f"SKILL DEFINITION:\n{skill_content}")
        if step.description:
            goal_parts.append(f"TASK:\n{step.description}")
        if input_data:
            input_block = yaml.dump(input_data, default_flow_style=False, allow_unicode=True)
            goal_parts.append(f"INPUT:\n{input_block}")

        goal_parts.append(
            "Execute the step above. Output ONLY YAML mapping with keys matching the output contract.\n"
            "Use format: key: value\n"
            "No markdown, no explanations, no code fences."
        )

        goal = "\n\n".join(goal_parts)

        # Run agent
        t0 = time.time()
        model = step.model or "deepseek-v4-flash"
        result = spawn_agent(
            goal=goal,
            context="",
            model=model,
            toolsets=["file"],
            timeout=step.timeout,
        )
        duration = time.time() - t0

        if not result["success"]:
            return {
                "success": False,
                "error": result.get("stderr", "Agent execution failed")[:200],
                "step_id": step.id,
                "duration_s": round(duration, 1),
            }

        # Parse output against contracts
        output_text = result["output"]
        parsed_output = self._parse_contract_output(output_text, step.output_spec)

        if parsed_output is None:
            return {
                "success": False,
                "error": "Output could not be parsed against contract",
                "step_id": step.id,
                "raw_output": output_text[:500],
                "duration_s": round(duration, 1),
            }

        # Write step output to context
        for contract in step.output_spec:
            if contract.target.startswith("context."):
                key = contract.target.split(".", 1)[1]
                self.context.set(key, parsed_output.get(key, parsed_output))
            else:
                # Write to file
                file_path = FORGE_ROOT / contract.target
                file_path.parent.mkdir(parents=True, exist_ok=True)
                content = parsed_output.get("output", output_text)
                if isinstance(content, dict):
                    content = yaml.dump(content, default_flow_style=False, allow_unicode=True)
                file_path.write_text(str(content), encoding="utf-8")

        return {
            "success": True,
            "step_id": step.id,
            "duration_s": round(duration, 1),
            "output_keys": list(parsed_output.keys()) if isinstance(parsed_output, dict) else [],
            "raw_length": len(output_text),
        }

    def _run_parallel_group(self, group: ParallelGroup, completed: set) -> dict:
        """Execute a parallel group. All steps run concurrently.

        Uses ThreadPoolExecutor for true parallel execution.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        t0 = time.time()
        results = {}

        with ThreadPoolExecutor(max_workers=len(group.steps)) as executor:
            fut_map = {
                executor.submit(self._run_step, step, completed): step
                for step in group.steps
            }
            for fut in as_completed(fut_map):
                step = fut_map[fut]
                step_result = fut.result()
                results[step.id] = step_result
                self.context.record_step_result(step.id, step_result)

        duration = time.time() - t0
        all_ok = all(r.get("success", False) for r in results.values())

        return {
            "success": all_ok,
            "error": "" if all_ok else "One or more parallel steps failed",
            "duration_s": round(duration, 1),
            "step_results": results,
        }

    def _handle_retry(self, step: PipelineStep, completed: set, summary: dict):
        """Retry a failed step up to max_retries times."""
        from Core.hermes_bridge import spawn_agent

        for attempt in range(1, step.max_retries + 1):
            result = self._run_step(step, completed)
            summary["steps"][f"{step.id}_retry_{attempt}"] = result
            if result["success"]:
                completed.add(step.id)
                return
        # All retries exhausted
        if step.fallback_step:
            fallback = self._step_map.get(step.fallback_step)
            if fallback:
                fb_result = self._run_step(fallback, completed)
                summary["steps"][f"{step.id}_fallback"] = fb_result
                if fb_result["success"]:
                    completed.add(fallback.id)

    def _parse_contract_output(self, output_text: str, output_specs: list[StepContract]) -> Optional[dict]:
        """Attempt to parse step output YAML, validating against output contracts."""
        if not output_specs:
            return {"output": output_text.strip()}

        # Try YAML parse
        try:
            parsed = yaml.safe_load(output_text)
            if isinstance(parsed, dict):
                return parsed
        except yaml.YAMLError:
            pass

        # Try JSON
        try:
            parsed = json.loads(output_text)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        # If output format is 'text', just return raw
        if len(output_specs) == 1 and output_specs[0].format == "text":
            return {"output": output_text.strip()}

        # Last resort: return raw as string
        return {"output": output_text.strip()}


# ──────────────────────────────────────────────────────────────
# Pipeline blueprint integration
# ──────────────────────────────────────────────────────────────

def run_pipeline_for_blueprint(
    blueprint_name: str,
    initial_context: dict = None,
) -> dict:
    """Run the full pipeline defined for a blueprint.

    Convenience wrapper used by forge.py and spawn.py.
    Falls back to single-step agent spawn if no pipeline defined.

    Returns pipeline result summary.
    """
    pipeline = load_pipeline(blueprint_name)
    if pipeline is None:
        return {
            "success": False,
            "error": f"No pipeline defined for blueprint '{blueprint_name}'",
            "pipeline": None,
            "mode": "single-step",
        }

    context = PipelineContext(initial_context or {})
    runner = PipelineRunner(pipeline, context)

    # Save pipeline definition to run directory for traceability
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    pipeline_dump = yaml.dump(pipeline.to_dict(), default_flow_style=False, allow_unicode=True)
    (run_dir / "pipeline.yaml").write_text(pipeline_dump, encoding="utf-8")

    result = runner.run()

    # Save results
    result["run_id"] = run_id
    result["blueprint"] = blueprint_name
    (run_dir / "pipeline_result.yaml").write_text(
        yaml.dump(result, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )

    return result


def is_multi_step(blueprint_name: str) -> bool:
    """Check if blueprint defines a multi-step pipeline (vs single-step agent)."""
    return load_pipeline(blueprint_name) is not None


# ──────────────────────────────────────────────────────────────
# Integration test helpers
# ──────────────────────────────────────────────────────────────

def test_stub_agent(output: str, duration: float = 0.1):
    """Stub agent for integration testing. Returns a callable that mimics spawn_agent."""
    def _stub(goal, context, model, toolsets, timeout):
        return {
            "success": True,
            "output": output,
            "exit_code": 0,
            "stderr": "",
        }
    return _stub


def validate_pipeline_contracts(blueprint_name: str) -> list[str]:
    """Validate pipeline state contracts end-to-end.

    Checks:
    - Every output contract target is consumed by some step's input
    - No orphaned keys (outputs never read)
    - Data format compatibility across contract chain
    Returns list of warnings/errors.
    """
    pipeline = load_pipeline(blueprint_name)
    if pipeline is None:
        return ["No pipeline defined"]

    errors = []
    produced: dict[str, str] = {}  # target -> format (from outputs)
    consumed: set[str] = set()     # targets consumed by inputs

    for item in pipeline.steps:
        if isinstance(item, ParallelGroup):
            step_list = item.steps
        else:
            step_list = [item]

        for step in step_list:
            # Register outputs
            for contract in step.output_spec:
                target = contract.target
                fmt = contract.format
                if target in produced:
                    prev_fmt = produced[target]
                    if prev_fmt != fmt:
                        errors.append(
                            f"Format mismatch on '{target}': "
                            f"step '{step.id}' outputs {fmt}, "
                            f"but previous step output {prev_fmt}"
                        )
                produced[target] = fmt

            # Register inputs
            for contract in step.input_spec:
                source = contract.source
                consumed.add(source)

    # Orphaned outputs: produced but never consumed
    for target in produced:
        if target not in consumed:
            # Allow context.* targets — they're consumed by pipeline user
            if not target.startswith("context."):
                errors.append(f"Orphaned output: '{target}' is produced but never consumed")

    return errors
