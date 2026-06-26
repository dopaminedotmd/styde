Feedback applied vs missing analysis for bug-hunter-core:
Changes from feedback 20260626-191235:
  triage gate in persona.md (line 10): APPLIED
  validation step in BLUEPRINT.md (line 22): APPLIED
Changes from feedback 20260626-191523:
  ANSI strip instruction in persona.md: MISSING
  format compliance rule in persona.md: MISSING
The persona.md still says "Output: prioritized markdown bug report" which directly contradicts the Caveman Ultra mode you're running now. The agent that ran with this persona produced ANSI-colored diffs and Swedish-language notes because nothing in the persona explicitly forbids that.
Delta needed in persona.md -- two additions:
1. Add after triage gate (line 10): "Strip all ANSI escape sequences and terminal formatting artifacts before presenting output. Output must be plain text only -- no colored diffs, no escape codes."
2. Add: "Strict output format compliance: follow the requested response format exactly. No off-topic commentary, no language switching, no extra formatting."
If you want me to apply these, say "kör på".