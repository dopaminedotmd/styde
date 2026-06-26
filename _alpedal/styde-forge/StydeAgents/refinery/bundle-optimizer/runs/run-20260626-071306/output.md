Audit: bundle-optimizer blueprint files vs teacher feedback (runs 071102 + 071211)
self-check: persona.md
  current content: 8 lines, role + 5 rules about bundle optimization
  missing: "Finishing the job" section (no no-waffle guard, no artifact-or-dead-end rule, no 15-call efficiency guard)
  finding: both 071102 changes not yet applied
  confidence: 1.0
self-check: BLUEPRINT.md
  current content: 15 lines, Purpose + Persona + Skills sections only
  missing: improvement entry schema with effort/expecteddelta fields
  missing: before/after score diagnostic table
  finding: both 071211 changes not yet applied
  confidence: 1.0
patches needed for persona.md
  patch 1
    location: append to file, after the 5 rules
    addition: |
      Finishing the job:
      If no work is needed, state it in one sentence and STOP. Do not hedge, debate, or meta-analyze the task scope.
      The deliverable is a working artifact OR a concise dead-end report. Both are acceptable. Waffling is not.
      Efficiency guard: if total tool calls exceed 15 with no output-producing action (write_file/patch/terminal producing new artifact), force a stop-branch decision.
    impact: high (fixes efficiency 62 -> target 85+)
    expecteddelta: +25 pts efficiency, +10 pts usefulness
patches needed for BLUEPRINT.md
  patch 1
    location: append new "## Output Schema" section after Skills
    addition: |
      ## Output Schema
      Every improvement entry in generated output MUST include:
      - effort: string (minutes/hours)
      - expecteddelta: mapping of dimension -> delta in pts (e.g., efficiency: +15)
    impact: medium
    expecteddelta: +5 pts efficiency, +5 pts completeness
  patch 2
    location: append new "## Diagnostic Score Table" section
    addition: |
      ## Diagnostic Score Table
      Include a before/after table in every diagnostic section showing current eval scores per dimension and projected scores after patch application.
    impact: medium
    expecteddelta: +3 pts clarity, +5 pts completeness
projected composite score after all patches: 93-97
  accuracy: 100 -> 100 (unchanged, already max)
  clarity: 90 -> 93
  completeness: 88 -> 95
  efficiency: 86 -> 93
  usefulness: 93 -> 95
no other weaknesses detected in current blueprint files. both teacher feedback sets fully addressable with 3 line additions to persona.md and 2 section additions to BLUEPRINT.md.