teacher feedback analysis for run 20260626-091214
self-check: persona.md
  weakness found: no explicit no-waffle rule
  weakness found: no explicit "artifact OR dead-end" deliverable
  weakness found: no explicit tool-call efficiency guard
  findings match both 79.2 and 93.6 feedback
  confidence: 0.95
recommended persona.md patches (3 lines to add)
patch 1
  location: persona.md, after "Finishing the job" section
  rule: "If no work is needed, state it in one sentence and STOP. Do not hedge, debate, or meta-analyze the task scope."
  impact: high
patch 2
  location: persona.md, append to "Finishing the job"
  rule: "The deliverable is a working artifact OR a concise dead-end report. Both are acceptable. Waffling is not."
  impact: medium
patch 3
  location: persona.md, after "Finishing the job"
  rule: "Efficiency guard: if total tool calls exceed 15 with no output-producing action (write_file/patch/terminal producing new artifact), force a stop-branch decision."
  impact: medium
existing strength
  "Finishing the job" already demands working artifacts backed by real tool output
  no change needed there
existing gap
  the section permits infinite tool loops as long as each call "makes progress"
  15-call guard closes that gap
estimated score after patches: 93-96
  remaining weakness: none from feedback
  potential new weakness: none identified
apply patches? yes — next spare cycle