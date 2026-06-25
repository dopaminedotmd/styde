"""
Eval pipeline: self-eval, judge-eval, composite scoring.

Self-eval runs inline with agent. Judge-eval runs in fresh context.
Composite = self × 0.4 + judge × 0.6 (Phase 1 fixed weights).
Results saved as eval.yaml in agent run directory.
"""
import yaml
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent

SELF_EVAL_PROMPT = """
Evaluate your own output against the rubric below.
Be honest and critical. Return ONLY a YAML block:

```yaml
score: <0-100 integer>
dimensions:
  accuracy: <0-100>
  clarity: <0-100>
  completeness: <0-100>
  efficiency: <0-100>
  usefulness: <0-100>
notes: "<one sentence explaining the score>"
```

Do not include any other text. Just the YAML block.
"""

JUDGE_EVAL_PROMPT = """
You are an independent judge. Evaluate the agent output below against the rubric.
Be objective and consistent. Return ONLY a YAML block:

```yaml
score: <0-100 integer>
dimensions:
  accuracy: <0-100>
  clarity: <0-100>
  completeness: <0-100>
  efficiency: <0-100>
  usefulness: <0-100>
notes: "<one sentence explaining the score>"
```

Do not include any other text. Just the YAML block.
"""


def build_self_eval_prompt(agent_output: str, rubric: str = "") -> str:
    """Build self-evaluation prompt. Sent to same agent after task completion."""
    prompt = SELF_EVAL_PROMPT
    if rubric:
        prompt += f"\n\n## RUBRIC\n{rubric}"
    prompt += f"\n\n## YOUR OUTPUT\n{agent_output}"
    return prompt


def build_judge_eval_prompt(agent_output: str, rubric: str = "") -> str:
    """Build judge evaluation prompt. Sent to fresh delegate_task with no blueprint context."""
    prompt = JUDGE_EVAL_PROMPT
    if rubric:
        prompt += f"\n\n## RUBRIC\n{rubric}"
    prompt += f"\n\n## AGENT OUTPUT TO EVALUATE\n{agent_output}"
    return prompt


def parse_eval_yaml(text: str) -> Optional[dict]:
    """Parse eval YAML from agent/judge response. Returns None on failure."""
    # Try to find YAML block
    if "```yaml" in text:
        start = text.find("```yaml") + 7
        end = text.find("```", start)
        if end > start:
            text = text[start:end]

    # Try direct YAML parse
    try:
        result = yaml.safe_load(text)
        if isinstance(result, dict) and "score" in result:
            return result
    except yaml.YAMLError:
        pass

    # Fallback: regex extraction
    score_match = re.search(r'score:\s*(\d+)', text)
    if score_match:
        return {
            "score": int(score_match.group(1)),
            "dimensions": {},
            "notes": "regex-extracted",
            "_fallback": True,
        }

    return None


def compute_composite(
    self_eval: dict,
    judge_eval: dict,
    self_weight: float = 0.4,
    judge_weight: float = 0.6,
) -> dict:
    """
    Compute composite score from self-eval and judge-eval.

    Phase 1: fixed weights. Phase 2: Bayesian-optimized per blueprint.
    """
    self_score = self_eval.get("score", 0)
    judge_score = judge_eval.get("score", 0)

    composite = (self_score * self_weight) + (judge_score * judge_weight)

    # Combine dimension scores
    dimensions = {}
    for dim in ["accuracy", "clarity", "completeness", "efficiency", "usefulness"]:
        s = self_eval.get("dimensions", {}).get(dim, 0)
        j = judge_eval.get("dimensions", {}).get(dim, 0)
        if s or j:
            dimensions[dim] = round((s * self_weight) + (j * judge_weight), 1)

    passed = composite >= 70

    return {
        "composite_score": round(composite, 1),
        "self_eval_score": self_score,
        "judge_eval_score": judge_score,
        "dimensions": dimensions,
        "passed": passed,
        "quality_gate": composite >= 80,
        "production_ready": composite >= 85,
        "weights": {
            "self": self_weight,
            "judge": judge_weight,
        },
    }


def save_eval(
    run_dir: Path,
    self_eval: Optional[dict],
    judge_eval: Optional[dict],
    composite: Optional[dict],
    blueprint: str = "",
    benchmark: str = "",
) -> Path:
    """Save eval results to eval.yaml in run directory. Returns path."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    eval_data = {
        "blueprint": blueprint,
        "benchmark": benchmark,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "self_eval": self_eval,
        "judge_eval": judge_eval,
        "composite": composite,
    }

    eval_path = run_dir / "eval.yaml"
    content = yaml.dump(eval_data, default_flow_style=False, allow_unicode=True)
    eval_path.write_text(content, encoding="utf-8")
    return eval_path


def load_agent_output(run_dir: Path) -> str:
    """Load agent output from run directory."""
    output_path = Path(run_dir) / "output.md"
    if not output_path.exists():
        raise FileNotFoundError(f"Agent output not found: {output_path}")
    return output_path.read_text(encoding="utf-8")


def load_rubric(benchmark_name: str) -> str:
    """Load rubric from benchmark directory."""
    rubric_path = FORGE_ROOT / "eval" / "benchmarks" / benchmark_name / "rubric.md"
    if rubric_path.exists():
        return rubric_path.read_text(encoding="utf-8")
    return ""
