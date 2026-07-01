teacher-feedback analysis for session 20260628_124805
findings:
1. blueprint.md: evidence-typing fix needed
   action: replace vague category refs with specific eval suite filenames
   diff: {file: BLUEPRINT.md, change: "replace 'math' with 'gsm8k.yaml', replace 'coding' with 'humanevalv2.json'", lines: depend-on-current-version}
   validation: grep for remaining non-filename evidence refs after patch
2. blueprint.md: missing config anchors
   action: ensure each change-block includes anchor+mode fields; deduplicate across summary and per-file sections
   validation: grep for .anchor: and .mode: in every change block
3. blueprint.md: add output-length constraint
   action: insert rule "Output MUST contain exactly the requested data plus a one-line verdict — no digest, no summary table, no verification protocol section."
   validation: lint pass on blueprint structure
4. persona.md: add CONSISTENCY quality-gate dimension
   action: append dimension: 'CONSISTENCY - verify all self-imposed rules are followed in same output'
   validation: grep persona.md for CONSISTENCY
5. blueprint.md: replace subjective impact labels with numeric scale
   action: swap 'high'/'medium' labels for 1-5 numeric scale in Impact column; add validation step
   validation: yaml schema check on Impact values
6. blueprint.md: add ANTI-PATTERN section against inlining
   action: add section 'ANTI-PATTERN: Do not inline file contents where persona requires separate REASONING section'
   validation: grep for ANTI-PATTERN in blueprint
current composite score trajectory: 79.0 -> target 80.0+ with items 3-6
verdict: apply items 3,4,5,6 together — they address the 1-point gap
post-fix verification pending read of current BLUEPRINT.md and persona.md before patches can be applied