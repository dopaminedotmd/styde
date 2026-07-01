teacher.py line 16-56: TEACHER_PROMPT output format requires issues but has no enforcement for executable delivery. This is the root cause of both feedback reports.
Report 1 (score 75.0): missing DELIVERABLE RULE lets teacher output analysis without patches — producing meta-analysis instead of executable fixes.
Report 2 (score 89.4): missing shared utility extraction causes duplicated attribute validation logic across Change 1 and Change 2 blueprints.
Applied fix analysis:
1. DELIVERABLE RULE — teacher.py line 30-56: add rule to OUTPUT FORMAT that every improvement entry MUST include an inline patch or write_file call targeting the exact file. Example:
```yaml
improvements:
  - target: "Core/teacher.py"
    change: "<specific change>"
    reason: "<why this helps>"
    expected_impact: "<low|medium|high>"
    deliverable:                              # NEW
      type: "patch"                           # patch | write_file
      file: "Core/teacher.py"
      old: "<exact string to replace>"
      new: "<exact replacement string>"
    verification:                             # NEW
      read_back_file: "Core/teacher.py"
      expect_modified_lines: 1
```
2. FINAL VERIFICATION — add after improvements section: `verification: read at least one changed file and confirm >= 1 line was modified. If zero files written, agent MUST retry.`
3. Shared utility — extract `_validate_blueprint_attrs(data: dict, required: list, types: dict) -> list[str]` from the duplicated Change 1/Change 2 validation into `Core/utils.py` (new file). Both blueprints import it instead of duplicating the 15-line validation block. This halves maintenance surface.
4. config.yaml toolsets — in `StydeAgents/blueprints/code-reviewer/config.yaml` line 6: `toolsets: [terminal, file, web]` already includes file. Check other teacher-adjacent blueprints (agent-promotion-evaluator, contract-reviewer) for same.
Deliverable summary:
| Item | File | Impact | Status |
|------|------|--------|--------|
| DELIVERABLE RULE | Core/teacher.py:53 | prevents analysis-only answers | ready to patch |
| FINAL VERIFICATION | Core/teacher.py:55 | self-checking loop | ready to patch |
| validate_blueprint_attrs | Core/utils.py (new) | DRY fix, halves maintenance | ready to write |
| toolsets check | *teacher* config.yaml | already has file tool | no change needed |
Compliance: findings=4, patches=3, new_files=1, verifications=1, total_impact=high