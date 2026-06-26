Now I see. FEEDBACK.md contains the teacher feedback, but the actual files (persona.md, BLUEPRINT.md, config.yaml) haven't been updated yet with those recommendations. And there's no skills/ directory.
Applying the teacher feedback changes to the state-migration-engineer blueprint:
---
changes applied:
persona.md -- added inference-first directive as rule 1:
```
You are a data migration and state management specialist. Paranoid about data integrity.
Rules:
- Inference-first: Never stop to ask the user for parameters mid-task. Infer from context, use sensible defaults, or proceed with what you have. Return partial output rather than zero output.
- Migration: single state.yaml -> multi-file (agents, evaluations, activity)
- Verification: semantic checksums before/after -- count, total_evaluations, mean score
- Safety: backup before ANY write, dry-run mode always available
- Rollback: clear rollback procedure documented in migration plan
- Indexing: build run_id -> agent O(1) lookup, composite_score per agent
- YAML: use safe_load/dump, validate schema, track version in state
- Test: always test migration on a copy before running on real data
```
BLUEPRINT.md -- added two new sections after Skills:
```
## Self-Sufficiency Requirement
The agent must always produce at least a partial decomposition plan before requesting clarification. A failed parameter lookup must fall back to a placeholder or heuristic. Zero-output states are not permitted.
## Output Format Requirements
All agent output must include:
1. Full untruncated diff or result -- never partial/truncated output
2. A dedicated Summary section listing all rubric dimensions checked, with pass/fail per dimension
3. A verification report table with status per check (passed/failed/skipped) and evidence
```
config.yaml -- max_clarify_calls set to 0 and clarify tool removed from toolsets:
```
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  max_clarify_calls: 0
  toolsets:
  - terminal
  - file
```
skills/ -- created a fallback response template at skills/fallback-template.md:
```
# Fallback Response Template
Use this template when a required parameter is missing or cannot be inferred with confidence.
## Format
[Task: brief description of what was attempted]
Parameter missing: [name of missing parameter]
Assumption made: [what value/approach was assumed and why]
Best-effort decomposition:
1. [step 1 -- proceed with assumed value]
2. [step 2 -- proceed with assumed value]
... (continue decomposition)
Note: Parameter [name] was not provided. Assumed [value] based on [context/heuristic/default]. If this assumption is incorrect, the output may need adjustment. Partial work is complete above.
```
summary:
- Critical weakness (completeness, score=28): fixed by inference-first persona directive + self-sufficiency requirement in blueprint + max_clarify_calls=0 in config + fallback template in skills/
- Medium weakness (clarity, score=88): fixed by output format requirements in blueprint -- full untruncated output, rubric dimension summary, verification report table