---
task: apply feedback from 20260628-162159 and 20260628-162312
target_files:
  - persona.md
  - BLUEPRINT.md
  - config.yaml
status: completed
persona.md_changes:
  - section: instructions
  - added_rule: "IncompleteInput: when task input is partial or missing, offer 3 alternatives — paste full input, point to a file to read, or request a format example — do NOT report the gap and stop"
  - severity: high
BLUEPRINT.md_changes:
  - section: "Incomplete Input Protocol"
  - flow:
      detect: "identify what parts of the input are missing (task body, design specs, target files)"
      propose: "offer the user exactly 3 alternatives — paste full input, point to a file to read, or request a format example"
      proceed: "use best available data (existing files, defaults, inferred specs) to make partial progress"
      output: "produce a partial deliverable annotated with confidence level (e.g. Confidence: 65% — color palette inferred from existing CSS, no explicit spec provided)"
  - post_patch_step: "strip or summarize raw diff output to a formatted summary, e.g. 'Changes applied: {files}. Key additions: {protocolname}, {fieldsadded}.'"
  - severity: high
config.yaml_changes:
  - key: maxretriesonmissinginput
  - value: 3
  - key: fallbackstrategy
  - value: promptuser
  - key: maxconsecutivefileops
  - value: 5
  - key: parallel_task
  - value: true
  - severity: medium
confidence: 95%
reasoning: all three changes from both feedback rounds applied. persona.md gets the incomplete-input rule. BLUEPRINT.md gets the 4-step Incomplete Input Protocol plus diff-summarization step. config.yaml gets maxretries, fallback, concurrency controls. no markdown output.