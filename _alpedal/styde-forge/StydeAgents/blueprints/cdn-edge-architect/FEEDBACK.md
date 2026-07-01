## Feedback from 20260628-094610 (score: 81.4/100)
**Weakest:** accuracy | **Cause:** Agent generated invalid YAML syntax (workers- key) in verify-hard-numbers section, violating the blueprint's own structured-output guardrail | **Severity:** medium
**Changes:**
- **BLUEPRINT.md**: Add a mandatory 'YAML lint pass' step before final output: 'Run the generated YAML through a syntax validator. Reject and regenerate if any parse errors exist.' _(impact: high)_
- **BLUEPRINT.md**: In all sections that emit YAML output (especially verify-hard-numbers), replace free-form key assembly with a template: 'Do NOT hand-write YAML keys. Use the exact key: value format from the schema.' _(impact: medium)_
- **skills/**: Add a skill that preloads a YAML validator helper: 'Before writing final output, call yaml.safe_load() on the output string. If it raises YAMLError, fix the syntax errors and retry.' _(impact: medium)_
**Summary:** 81.4 composite — quality gate passed but production threshold missed by 3.6 points due to a preventable YAML syntax error pulling down accuracy.

---

---
## Feedback from 20260628-095011 (score: 76.0/100)
**Weakest:** completeness | **Cause:** Blueprint mixes prose narrative with schema keys without standardising on one format, omitting required fields (description, artifacts, tags) and leaving the agent to guess what constitutes a valid deliverable. | **Severity:** high
**Changes:**
- **BLUEPRINT.md**: Strip all plain-text prelude lines and reorganise the file as a strict YAML frontmatter block with keys: description, artifacts, tags, inputs, outputs, and verify-hard-numbers as a sub-section under a methods key. _(impact: high)_
- **BLUEPRINT.md**: Fix the 'crunshbase' typo to 'crunchbase', and add an explicit 'worked_example' section showing a filled-out CDN evaluation with the validation steps applied. _(impact: medium)_
- **BLUEPRINT.md**: Replace the empty 'output' stub under verify-hard-numbers with a real output schema (e.g. a table of domains → CDN provider → confidence) and a 'required_output_fields' list. _(impact: medium)_
**Summary:** Blueprint needs a strict YAML schema with required fields, a fixed typo, a worked example, and an explicit output contract to lift completeness from 58→80+ and pass the quality gate.

---

---
## Feedback from 20260628-095124 (score: 78.8/100)
**Weakest:** usefulness | **Cause:** Agent outputs structurally invalid YAML (duplicate mapping keys in domain_provider_table and workedexample.output_sample), making output unparsable and unusable despite correct reasoning. | **Severity:** high
**Changes:**
- **blueprint prompt**: Add explicit constraint: 'All collections (domain lists, example outputs) MUST be emitted as YAML sequences (list items under a dash), never as repeated top-level mapping keys. Each key must appear exactly once per mapping.' _(impact: high)_
- **blueprint prompt**: Add a pre-submit self-check step: 'After writing your YAML, scan it: does any key appear more than once at the same indentation level? If yes, fix before responding.' _(impact: high)_
- **persona.md**: Add trait: 'You verify YAML structural validity (no duplicate keys, proper list syntax) before final output.' _(impact: medium)_
**Summary:** Agent reasons correctly per-domain but YAML output has duplicate mapping keys that silently drop data — fix blueprint with structural constraints and a self-check step to pass yaml_lint_pass.

---

---
## Feedback from 20260628-095804 (score: 44.2/100)
**Weakest:** accuracy | **Cause:** Agent output the task specification/blueprint itself rather than executing it against real domains — conflated instructions with the expected deliverable. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add explicit guard at the top: 'YOUR ENTIRE OUTPUT MUST BE THE DOMAIN ANALYSIS — do NOT echo, reproduce, or summarize these instructions. Never output the word "blueprint" or any section of this spec in your response.' _(impact: high)_
- **BLUEPRINT.md**: Restructure the 'Output Format' section to use a minimal one-line example instead of a full annotated YAML spec, and move the detailed YAML schema to an appendix prefixed with 'INTERNAL SCHEMA — DO NOT OUTPUT'. _(impact: medium)_
- **BLUEPRINT.md**: Add execution step #0: 'Read domains.txt to see which domains to analyze.' _(impact: high)_
- **persona.md**: Add to persona: 'You are an analyst, not a document author. Your job is to run analysis on real data and output findings, not to describe how analysis should be done.' _(impact: medium)_
**Summary:** Agent produced the blueprint itself instead of domain analysis — critical instruction-vs-deliverable confusion; add output guards and an execution-first step.
