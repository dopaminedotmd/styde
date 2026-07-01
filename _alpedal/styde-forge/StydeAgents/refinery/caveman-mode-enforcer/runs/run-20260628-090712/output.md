Teacher feedback processed. System analysis complete.
CURRENT STATE
Core/quality_gates.py validates: file existence, persona length >= 50 chars, BLUEPRINT.md has "## Purpose", config.yaml has blueprint.name + blueprint.domain. Missing: YAML structure validation (duplicate top-level keys), rule type whitelist per section, no-plan-mode hardening.
Core/blueprint.py validate function same gaps. No system-level config.yaml template exists. No system-level BLUEPRINT.md template exists. Each blueprint has its own copy under StydeAgents/blueprints/<name>/.
No mechanism forces agents to produce executable output (patches, writes) instead of meta-analysis. Caveman rules skip this entirely.
CHANGES REQUIRED
Change 1: Core/quality_gates.py - Add requiredoutputquality guard
Add function validate_yaml_structure(cfg) that checks:
- No duplicate top-level keys (yaml.safe_load strips duplicates silently in PyYAML < 6.0)
- Allowed rule types per section (e.g. blueprint section only allows: name, domain, description, dependencies, version, ...)
- agent section allows: max_iterations, timeout_seconds, toolsets, skills, load_all_skills, model_override
- eval section allows: benchmarks, judge_model, min_pass_score
- Reject unknown keys with error
Add function check_agent_output_deliverable(output_text) that verifies:
- At least one write_file() or patch() call present in output
- If diagnosis claims N issues, at least N file edits present
- Fail validation if output contains only analysis with no executable changes
Change 2: Core/blueprint.py - Enhance validate function
Add _validate_yaml_schema(config) called from _validate_blueprint_impl, with same structure checks as above. Add _validate_agent_output(output_text) that scans for write_file/patch calls matching diagnosis count.
Change 3: Create system-level BLUEPRINT.md template
No single template file exists. The BLUEPRINT.md files across 231 blueprints vary. Create StydeAgents/_templates/BLUEPRINT.md with these mandatory sections:
```
## Purpose
## Missing Input Handling
If input spec is unclear: read the file first (readfile tool), not ask the user.
If values are missing: set sensible defaults and note them in output.
If format example needed: use the tool directly, do not describe what you would do.
## Output Format
CAVEMAN ULTRA MODE: see rules below.
DELIVERABLE RULE: Every identified issue MUST be paired with an inline patch or writefile call in the same turn. Analysis without executable fix is a failing answer.
FINAL VERIFICATION: After completing all edits, read back each changed file and confirm at least one file was modified per diagnosis item. If zero files were written, retry.
## Persona
<role-specific>
## Skills
<skill list>
```
Change 4: Add system-level config.yaml template
Create StydeAgents/_templates/config.yaml with:
```yaml
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
    - terminal
    - file
    - web
  load_all_skills: false
  skills: []
  model_override: null
blueprint:
  name: null
  domain: null
  description: ""
  version: "1.0.0"
  dependencies: []
  schema_expectations: []
  review_interval_days: 90
  last_reviewed: null
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
requiredoutputquality:
  enabled: true
  min_completeness_score: 70
  validate_yaml_structure: true
  allowed_keys:
    blueprint: [name, domain, description, version, version_history, dependencies, schema_expectations, review_interval_days, last_reviewed]
    agent: [max_iterations, retry_on_failure, timeout_seconds, toolsets, load_all_skills, skills, model_override]
    eval: [benchmarks, judge_model, min_pass_score]
    hardware_profiles: null
    pipeline: null
    requiredoutputquality: [enabled, min_completeness_score, validate_yaml_structure, allowed_keys]
  forbid_duplicate_keys: true
  require_deliverable_per_diagnosis: true
hardware_profiles:
  pontus-main:
    model: deepseek-v4-flash
    provider: deepseek
    eval_model: deepseek-v4-pro
    max_tokens: 8192
    temperature: 0.3
```
Change 5: Core/caveman.py - Harden no-plan-mode from guidance to guardrail
Add to CAVEMAN_RULES:
```
RULE: NO PLAN MODE. Do not describe what you will do. Execute immediately.
If you say "I will run the tests" or "Let me check" or "I will create" — 
you must make the corresponding tool call IN THE SAME RESPONSE.
Never end a turn with a promise of future action.
Every response must either: (a) contain tool calls making progress, or (b) deliver a final result.
Responses that only describe intentions without acting are automatically FAILING.
```
Change 6: Core/forge.py or evaluate.py - Add teacher role toolsets
In teacher.py, set toolsets: ['terminal', 'file'] explicitly when building teacher prompts. Teacher agents must always have file-writing tools available. Remove the abstraction that allows teacher to claim "no tools available."
IMPACT SUMMARY
Change          | File                    | Impact
requiredoutputquality guard  | Core/quality_gates.py, Core/blueprint.py  | medium
Missing Input Handling       | BLUEPRINT.md template (create _templates/) | high
DELIVERABLE RULE             | BLUEPRINT.md template                     | high
FINAL VERIFICATION           | BLUEPRINT.md template                     | medium
No-Plan-Mode guardrail       | Core/caveman.py                           | high
Teacher role toolsets        | Core/teacher.py, Core/caveman.py          | medium
config.yaml template         | StydeAgents/_templates/config.yaml        | medium
Failing to apply these will produce agents that diagnose correctly but never ship executable fixes. The meta-failure pattern repeats until DELIVERABLE RULE becomes a hard gate, not a suggestion.