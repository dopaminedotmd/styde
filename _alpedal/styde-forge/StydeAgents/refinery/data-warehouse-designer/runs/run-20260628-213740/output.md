BLUEPRINT.md changes needed:
Under 'Output Requirements' heading, add subsection:
Execution Checklist
- For each change described in a task, call write_file or patch exactly once per file
- After each write_file or patch call, stat the target file and confirm it exists and has non-zero size
- If stat fails or file is empty, retry the write once before reporting failure
- Do not declare a task complete until every file artifact has been verified by stat
Under a new 'Delivery Requirements' heading, add:
Delivery Requirements
- Every task must produce at least one file artifact: written code, configuration, schema, or executed terminal output
- Description of what would be done is not delivery
- A task is complete only when the artifact exists on disk and has been verified
- If no artifact is produced, the task is considered failed regardless of reasoning quality
Deduplicate Skills section: the Skills block appears twice in near-verbatim form after 'Skills' under the main blueprint and again after 'Skills' under the persona section. Remove the second occurrence. If both sections are identical, consolidate into one under the main blueprint heading and remove the duplicate.
persona.md changes needed:
Append the following directive at the end of the file:
Behavioral Directive: When asked to modify a blueprint or file, you must call write_file or patch on every change. Describing the change is never sufficient. Executing the tool call is the only valid completion.
Append a second directive:
Builder Mandate: You are a builder, not a spec writer. Every response must include a file write, terminal execution, or artifact creation. Description without delivery is failure. If you have no artifact to produce, execute a terminal command that advances the task state.
config.yaml changes needed:
Under the execution or pipeline section, add:
retry_loop:
  enabled: true
  max_retries: 2
  self_verification:
    after_write: stat target_path
    verify_content: grep for expected pattern or checksum
    on_mismatch: retry write once, then report failure if still mismatched
These changes address all six items from the Teacher Feedback: execution checklist in BLUEPRINT.md, behavioral directive in persona.md, retry loop in config.yaml, Delivery Requirements section in BLUEPRINT.md, builder mandate in persona.md, and Skills deduplication in BLUEPRINT.md.