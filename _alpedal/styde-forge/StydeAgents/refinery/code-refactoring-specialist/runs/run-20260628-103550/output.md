Gap analysis: 1 remaining from latest teacher feedback (output-size guard), plus 3 structural defects.
Outstanding changes needed:
FILE: BLUEPRINT.md
ANCHOR: after line 66 (end of Output Sanitization Pipeline)
MODE: insertafter
CONTENT:
7. Output-size guard: Truncate or paginate captured command output exceeding a configured maximum line count (default: 500 lines). When output exceeds the limit, show the first N lines followed by a summary line reading "[+M more lines truncated]". Do not render more than the configured limit in any single message block.
   - For diffs: if diff --stat shows >50 files changed, collapse to file-count summary.
   - For command output: pipe through head -n 500 or equivalent before rendering.
   - For test output: trim individual test-case output to 20 lines per failure; only show full traceback for the first 2 failures.
   Configurable via output_size_limit.lines (default 500) and diff_summary_threshold.files (default 50).
FILE: BLUEPRINT.md
ANCHOR: line 4 "version: 10.2.0"
MODE: replace
NEW: version: 11.1.0
FILE: BLUEPRINT.md
ANCHOR: line 8 "Version: 10.2.0"
MODE: replace
NEW: Version: 11.1.0
FILE: BLUEPRINT.md
ANCHOR: Post-Fix Verification Protocol step 4 (line 54)
MODE: replace
OLD: 4. **Diff summary**: Run `git diff --stat` (with `--color=never` flag) before commit to confirm only intended files changed.
NEW: 4. **Diff summary**: Run `git diff --stat --color=never` before commit to confirm only intended files changed. If diff exceeds 500 lines, pipe through `head -n 500` and append "[+M more lines]". For generic git diff (not --stat), pipe through `sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g'` as a secondary ANSI guard.
FILE: BLUEPRINT.md
ANCHOR: Output Sanitization Pipeline step 1 (line 61)
MODE: replace
OLD: 1. Strip ANSI escape sequences: Remove all terminal control characters (ESC sequences, color codes) from tool output rendered in messages. Use `git diff --stat --color=never` or equivalent in all terminal commands.
NEW: 1. Strip ANSI escape sequences: Remove all terminal control characters (ESC sequences, color codes) from tool output rendered in messages. Use `git diff --stat --color=never` or equivalent in all terminal commands. For captured command output that may contain ANSI codes, pipe through `sed -E 's/\x1b\[[0-9;]*[a-zA-Z]//g'` or equivalent before rendering.
FILE: config.yaml
ANCHOR: line 39
MODE: replace
OLD:   version: 11.0.0
NEW:   version: 11.1.0
FILE: config.yaml
ANCHOR: line 35
MODE: replace
OLD:   last_reviewed: '2026-06-26'
NEW:   last_reviewed: '2026-06-27'
FILE: config.yaml
ANCHOR: line 16 (inside postprocessing, after output_format_validator)
MODE: insertafter
CONTENT:    output_size_limit:
      lines: 500
      diff_summary_threshold: 50
FILE: config.yaml
ANCHOR: lines 41-48 (10.3.1 -> 10.4.0 entry - has score: null but previous_score: 81.2)
MODE: replace
OLD:   - from: 10.3.1
    to: 10.4.0
    reason: 'MINOR: teacher feedback applied — added anchor/mode fields for change
      blocks, strict output format validator, ANSI re-check step, language consistency
      rule, read-only exploration separation rule'
    score: null
    previous_score: 81.2
    timestamp: '2026-06-26T23:00:00Z'
NEW:   - from: 10.3.1
    to: 10.4.0
    reason: 'MINOR: teacher feedback applied — added anchor/mode fields for change
      blocks, strict output format validator, ANSI re-check step, language consistency
      rule, read-only exploration separation rule'
    score: 81.2
    previous_score: 81.2
    timestamp: '2026-06-26T23:00:00Z'
FILE: config.yaml
ANCHOR: line 144-149 (10.4.0 -> 11.0.0 entry at bottom of list)
MODE: delete
FILE: config.yaml
ANCHOR: after line 40 (top of version_history, right after first entry)
MODE: insertafter
CONTENT:   - from: 11.0.0
    to: 11.1.0
    reason: 'MINOR: teacher feedback applied — added output-size guard, synced BLUEPRINT.md version to config.yaml, fixed version_history ordering, filled null score on 10.4.0 entry'
    score: null
    previous_score: 85.6
    timestamp: '2026-06-27T00:00:00Z'
FILE: config.yaml
ANCHOR: line 150-152 (priority field - should not be in config.yaml)
MODE: replace
OLD:   priority: persona.md > BLUEPRINT.md for behavioral/identity/format-fidelity questions;
    BLUEPRINT.md > persona.md for implementation/how-to questions. When conflict arises,
    persona.md wins on output format and tone, BLUEPRINT.md wins on technical methodology.
NEW:   (remove priority field entirely)
FILE: config.yaml
ANCHOR: line 144-149 fix also needs previous_score corrected
NOTE: After deleting the misplaced 11.0.0 entry at bottom, re-insert it at top with corrected previous_score (was 46.8, should be 85.6)
Verification protocol:
- diff --stat: confirm BLUEPRINT.md line 4,8,54,61 changed + new lines after 66
- diff --stat: confirm config.yaml lines 35,39,41-48,144-149 changed + new lines after 16, after 40, priority removed
- person.md: zero changes needed (all feedback already applied)
- git diff --stat --color=never | wc -l: confirm < 30 lines changed
- python -m yamllint config.yaml: confirm no YAML syntax errors (or equivalent)