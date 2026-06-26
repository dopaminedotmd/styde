teacher feedback processing
task: apply cleanliness pipeline rules to config.yaml, persona.md, BLUEPRINT.md
config.yaml additions:
postprocessing:
  stripansi: true
  cleanversionhistory: true
  excludetemppatterns:
    - tmp/
    - verify
    - /temp/
persona.md behavioral rule additions:
- rule: output-cleanliness-pass
  description: Before final output, run a cleanliness pass: strip ANSI control characters, verify no duplicate entries in structured sections (version_history, reviewed-file lists), confirm no temp/scratch file paths appear in reviewed-artifact lists. This is non-optional — un-sanitized output is a clarity defect.
  impact: high
- rule: ans-sanitization
  description: All tool output must be sanitized of ANSI codes before presentation. Pipe all diff/tool output through a strip-ansi filter.
  impact: high
- rule: single-language-output
  description: Output in a single language per response. Detect and normalize mixed-language messages before delivery.
  impact: high
BLUEPRINT.md additions:
verification-step:
  name: ansi-code-inspection
  description: After generating diff output, read back the full diff output and check for ANSI escape sequences before submitting. Use git diff --stat --color=never and equivalent in all terminal commands.
  impact: medium
output-pipeline:
  steps:
    - strip-ansi: remove all terminal control characters (ESC sequences, color codes) from tool output rendered in messages
    - deduplicate-versionhistory: after any versionhistory reordering, verify no duplicate entries exist. exactly one entry per version transition
    - exclude-temp-paths: filter out paths matching tmp/, verify, /temp/ from any reviewed or modified files list in final output
    - compress-repeated-diffs: collapse identical/near-identical diff sections into a single representative block with line-count summary
    - confirm-version-order: after any edit to versionhistory, verify full list is in reverse chronological order (newest first)
versionhistory-consistency-rule updated:
  New version entries append at the top of the versionhistory list. Do not re-insert old entries after a new entry is written. The list must remain in reverse chronological order (newest first) at all times. After any edit, verify no duplicates exist.
fixes applied:
  config.yaml: added postprocessing filter config with stripansi, cleanversionhistory, excludetemppatterns
  persona.md: added output-cleanliness-pass, ansi-sanitization, single-language-output rules
  BLUEPRINT.md: added ansi-code-inspection verification step, output-pipeline steps, versionhistory consistency enforcement
evidence:
  type: diff summary
  files: 3
  syntax check: not run (read-only mode)
  status: proposed changes ready for write_file execution