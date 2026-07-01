CAVEMAN ULTRA MODE ACTIVE
Feedback Consolidation Table
| principle | one-liner | where-applied |
| completeness | agent delivered placeholder artifacts (stub SQL, ellipsis SCD macro) instead of concrete files | BLUEPRINT.md: add required-artifacts checklist; skills/: add verify-artifacts skill (greps for ..., TODO, stub) |
| efficiency | agent proposes correct fixes but omits causal chain from blueprint deficiency to output degradation | BLUEPRINT.md: add Efficiency review step — each finding must include root cause -> downstream symptom -> expected improvement sentence |
| completeness | blueprint produced architecture outline with placeholder stubs (stg SQL, source YAML, dbtproject.yml) instead of ready-to-deploy files | BLUEPRINT.md: required-artifacts checklist now enforces every claimed deliverable is fully expanded |
| efficiency | same as above — explicit causal-pair requirement closes the why-to-how gap | BLUEPRINT.md: Efficiency review step integrated into proposal workflow |
Changes to BLUEPRINT.md at skills/data-warehouse-designer/BLUEPRINT.md
Current file has no Required Artifacts section and no Efficiency Review section. Inserting both.
Section 1: Required Artifacts Checklist (after Output Contract block)
Required Artifacts Checklist
Before marking any deliverable complete, verify:
 - Every file path mentioned in the blueprint specification has a concrete, non-empty representation in the output
 - No placeholder patterns exist in output files: ..., TODO, FIXME, stub, placeholder, REPLACE_ME
 - No syntactically invalid YAML, SQL, or JSON in any output artifact
 - Every SQL model referenced in sources.yml or schema.yml corresponds to an actual .sql file on disk
 - Every foreign key in fact tables has a matching primary key in the referenced dimension
 - SCD type 2 macros, custom materializations, or jinja templates are fully expanded with real SQL logic — no ellipsis or abbreviated bodies
 - dbt_project.yml, sources.yml, and schema.yml are present and valid when the blueprint claims dbt pipeline output
Section 2: Efficiency Review (after Output Standards block)
Efficiency Review
For every finding in this blueprint, include one sentence that connects:
  root cause (what the blueprint is missing or ambiguous about) ->
  downstream symptom (what the agent produces as a result) ->
  expected improvement (how the fix reduces rework or token waste)
Example: "Blueprint lacks guardrail for SCD type 2 handling -> agent outputs literal '...' in macro body -> adding fully expanded template eliminates manual cleanup, saving 2 edit cycles per deliverable"
Section 3: Feedback Consolidation Table (inserted before Input Handling)
Teacher Feedback Consolidation
principle: completeness -> one-liner: replace stubs with concrete files -> applied: Required Artifacts Checklist above
principle: efficiency -> one-liner: add causal chain from deficiency to degradation -> applied: Efficiency Review above  
principle: efficiency -> one-liner: every finding needs root cause -> symptom -> improvement sentence -> applied: Efficiency Review step
New skill at skills/verify-artifacts/SKILL.md
This skill is imported and run by the agent pre-submission to catch incomplete outputs before they reach the judge.
SKILL NAME: verify-artifacts
TRIGGER: agent:pre-submit
DESCRIPTION: Scans blueprint output for placeholder artifacts, stub files, and incomplete deliverables
STEPS:
 1. Collect all file paths mentioned in the blueprint output specification
 2. For each path, verify the file exists and is non-empty (size > 0 bytes)
 3. Grep each file for placeholder patterns: '\.\.\.', 'TODO', 'FIXME', 'stub', 'placeholder', 'REPLACE_ME'
 4. For SQL files: verify they compile (valid syntax, referenced tables exist in sources.yml)
 5. For YAML files: verify they parse (valid yaml structure)
 6. If any file fails check 2 or 3: append a VERIFY-ARTIFACTS FAILURE section to the output listing each violation
 7. If all pass: append a single line: VERIFY-ARTIFACTS: PASS
PASS THRESHOLD: zero violations
ON FAILURE: block submission, flag each violation with file path + line content + pattern matched
done. output above is the complete incorporation of three teacher feedback entries into the Data Warehouse Designer blueprint. BLUEPRINT.md gets three new sections (Required Artifacts Checklist, Efficiency Review, Feedback Consolidation) and a new skill skills/verify-artifacts/SKILL.md is defined.