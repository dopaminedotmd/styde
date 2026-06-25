"""
Teacher agent: analyze evals, propose improvements, bump versions.

Reads eval results, diagnoses root causes, proposes concrete blueprint changes.
Integrates auto_version for automatic version bumping.
"""
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from Core.auto_version import bump_version, latest_score

FORGE_ROOT = Path(__file__).resolve().parent.parent

TEACHER_PROMPT = """
You are a Teacher Agent for Styde Forge. Your job: analyze agent evaluations
and propose concrete blueprint improvements.

## INPUT
- Agent self-evaluation score and dimensions
- Judge evaluation score and dimensions
- Composite score (weighted combination)
- Previous evaluation history (if available)

## TASK
1. Identify the WEAKEST dimension (lowest score)
2. Diagnose ROOT CAUSE: why did the agent score low there?
3. Propose CONCRETE fix: what change to the blueprint would help?
4. If composite >= 85, extract REUSABLE PATTERN: what did the agent do well?

## OUTPUT FORMAT
Return ONLY a YAML block:

```yaml
diagnosis:
  weakest_dimension: "<name>"
  root_cause: "<one sentence>"
  severity: "<low|medium|high|critical>"

improvements:
  - target: "<persona.md|BLUEPRINT.md|config.yaml|skills/>"
    change: "<specific change to make>"
    reason: "<why this helps>"
    expected_impact: "<low|medium|high>"

pattern:  # only if composite >= 85
  name: "<pattern name>"
  description: "<what worked well>"
  reusable: "<yes|no>"

summary: "<one sentence verdict>"
```

Do not include any other text. Just the YAML block.
"""


def build_teacher_prompt(
    eval_data: dict,
    previous_evals: list[dict] = None,
) -> str:
    """Build teacher analysis prompt from eval data."""
    prompt = TEACHER_PROMPT

    # Current eval
    composite = eval_data.get("composite", {})
    self_eval = eval_data.get("self_eval", {})
    judge_eval = eval_data.get("judge_eval", {})

    prompt += f"\n\n## CURRENT EVALUATION"
    prompt += f"\nComposite score: {composite.get('composite_score', '?')}/100"
    prompt += f"\nPassed: {composite.get('passed', False)}"
    prompt += f"\nQuality gate (>=80): {composite.get('quality_gate', False)}"
    prompt += f"\nProduction ready (>=85): {composite.get('production_ready', False)}"

    prompt += f"\n\n### Self-Eval ({self_eval.get('score', '?')}/100)"
    if self_eval.get("dimensions"):
        for dim, score in self_eval["dimensions"].items():
            prompt += f"\n  {dim}: {score}"
    prompt += f"\n  Notes: {self_eval.get('notes', 'none')}"

    prompt += f"\n\n### Judge-Eval ({judge_eval.get('score', '?')}/100)"
    if judge_eval.get("dimensions"):
        for dim, score in judge_eval["dimensions"].items():
            prompt += f"\n  {dim}: {score}"
    prompt += f"\n  Notes: {judge_eval.get('notes', 'none')}"

    # History
    if previous_evals:
        prompt += "\n\n## PREVIOUS EVALUATIONS"
        for i, prev in enumerate(previous_evals[-3:], 1):
            pc = prev.get("composite", {})
            prompt += f"\n{i}. Score: {pc.get('composite_score', '?')}/100 (passed: {pc.get('passed')})"

    return prompt


def parse_teacher_response(text: str) -> Optional[dict]:
    """Parse teacher YAML response. Returns None on failure."""
    if "```yaml" in text:
        start = text.find("```yaml") + 7
        end = text.find("```", start)
        if end > start:
            text = text[start:end]

    try:
        result = yaml.safe_load(text)
        if isinstance(result, dict):
            return result
    except yaml.YAMLError:
        pass
    return None


def save_teacher_review(
    run_dir: Path,
    review: dict,
) -> Path:
    """Save teacher review to teacher_review.yaml."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)

    review["timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    review_path = run_dir / "teacher_review.yaml"
    content = yaml.dump(review, default_flow_style=False, allow_unicode=True)
    review_path.write_text(content, encoding="utf-8")
    return review_path


def apply_improvement(
    blueprint_name: str,
    composite_score: float,
    review: dict,
) -> str:
    """
    Apply teacher's improvement: bump blueprint version.

    Returns new version string.
    """
    previous = latest_score(blueprint_name)
    return bump_version(blueprint_name, composite_score, previous)


def should_retry(composite_score: float, iteration: int, consecutive_passes: int = 0, max_iterations: int = 10) -> bool:
    """Determine if agent should be retried (spawned again with improved blueprint)."""
    if iteration >= max_iterations:
        return False
    if composite_score >= 85:
        # Need 3 consecutive ≥85 for production
        if consecutive_passes < 3:
            return True  # Keep going — not at production yet
        return False  # Done — 3 consecutive passes achieved
    if composite_score >= 80:
        return True   # Close — one more try
    if composite_score >= 70:
        return True   # Passed but needs work
    return iteration < 3  # Failed — give it 3 tries


def determine_stage(composite_score: float, consecutive_passes: int = 0) -> str:
    """
    Determine agent stage based on score.

    >= 85 for 3 consecutive runs → production
    >= 70 → refinery (keep improving)
    < 70 → archive (failed)
    """
    if composite_score >= 85 and consecutive_passes >= 3:
        return "production"
    elif composite_score >= 70:
        return "refinery"
    else:
        return "archive"
