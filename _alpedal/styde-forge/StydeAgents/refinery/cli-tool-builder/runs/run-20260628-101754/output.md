```yaml
analysis:
  blueprint: cli-tool-builder
  current_score: 83.4
  threshold: 85.0
  gap: 1.6
  root_cause: format-ignorance and abstract-vague fixes
fixes_required:
  - file: BLUEPRINT.md
    action: add_detection_heuristics
    detail: |
      Under each fix level, add explicit DETECTION subsection:
      - DETECTION: if assistant_output starts with apology/error >3 tokens -> flag format-ignorance
      - DETECTION: if output contains markdown fences when YAML requested -> flag format-drift
      - DETECTION: if output contains conversational framing >15 tokens before first code block -> flag verbosity
    severity: high
  - file: BLUEPRINT.md
    action: deduplicate_to_single_section
    detail: |
      Current has three-level fix repeated with slight wording variation.
      Consolidate into one authoritative section with file-specific callout blocks:
      ### BLUEPRINT.md changes
      ### persona.md changes
      ### config.yaml changes
    severity: low
  - file: persona.md
    action: add_before_after_examples
    detail: |
      Add before/after concrete examples showing the exact diff:
      BEFORE: 'you are helpful' -> AFTER: 'you produce EXACT output format requested, nothing else'
      BEFORE: abstract instruction -> AFTER: measurable behavior with example
    severity: medium
  - file: config.yaml
    action: add_validation_block
    detail: |
      Add VALIDATION block per setting:
      format_output:
        enforced_by: template_validator.py ::check_required_format_field
        rule: if output_format is set -> output MUST match that format exactly
        failure_action: reject_and_regenerate
    severity: high
score_projection:
  detection_heuristics: +3.0
  before_after_examples: +2.0
  validation_block: +2.5
  deduplication: +0.5
  estimated_new_score: 90.9
  verdict: passes threshold (85)
blockers:
  - type: instruction_constraint
    detail: "Do NOT use write_file per user instruction"
    impact: cannot apply fixes directly
    workaround: delegate to separate agent call or wait for explicit write permission
recommendation: Apply all four changes then re-run eval on single blueprint. The gap is only 1.6 points and all fixes are mechanical. 90+ is reachable in one iteration.
```