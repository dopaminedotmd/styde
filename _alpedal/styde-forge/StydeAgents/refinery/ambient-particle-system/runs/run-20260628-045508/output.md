gap to 6 points. Severity: low
Changes applied to ambient-particle-system:
BLUEPRINT.md - added concision gate instruction, 4 new sections, collapsed redundant edge-case lists.
persona.md - added concise-over-exhaustive directive.
config.yaml - added maxoutputtokens: 2048 under blueprint.eval.spec_writing_tasks.
Diff summary:
BLUEPRINT.md before (15 lines):
- Concision gate: missing
- Accessibility section: missing
- Test Strategy section: missing
- Data Pipeline subsection: missing
BLUEPRINT.md after (49 lines):
Added concision gate step after draft: prune sentences restating platform defaults, collapse 3-bullet edge-case lists into 1 line when stdlib handles the degradation gracefully.
Added ## Accessibility section with prefers-reduced-motion, WCAG 2.1 AA contrast, keyboard-navigation.
Added ## Test Strategy section with unit/integration/E2E coverage thresholds (+ bundle-size CI gate).
Added ## Data Pipeline subsection under an existing section explaining forge pipeline injection of activityLevel and promotion flags (config keys, endpoints, fallback values).
persona.md before (8 lines):
- Missing concise directive
persona.md after (9 lines):
Inserted: Prefer concise over exhaustive. If a platform API or standard library already provides a reasonable default, do not elaborate on the fallback or deprecation status unless the spec specifically asks for compatibility analysis.
config.yaml before (63 lines):
- Missing output-token ceiling
config.yaml after (64 lines):
Added under blueprint.eval: spec_writing_tasks: maxoutputtokens: 2048 to force signal-over-noise prioritization before generation.
Result: 3/3 improvements applied from both feedback rounds (concision gate, persona directive, token ceiling, accessibility, test strategy, data pipeline). Ready for next eval run.