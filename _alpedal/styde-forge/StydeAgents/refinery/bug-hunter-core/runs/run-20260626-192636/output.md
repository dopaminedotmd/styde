Delta Report: bug-hunter-core v1 — Specification vs. Actual Execution
Gap #1 — Missing verification phase before patch delivery
Severity: HIGH
Spec location: BLUEPRINT.md — no verification step between patch generation and delivery
Observed: Feedback 86.8 — "Patches are delivered without verification against actual file content"
Root cause: BLUEPRINT.md Validation skill says "verify each issue independently" but does not define a separate verification sub-phase for patch content. Agent treats validation as a post-report review, not a pre-delivery cross-check.
Impact: Unverified patches may reference old_string values that do not exist in target files, producing silent delivery failures. Reader cannot distinguish verified patches from speculative ones. This direct causes the 86.8 completeness score.
Gap #2 — Missing post-patch summary section
Severity: MEDIUM
Spec location: BLUEPRINT.md — no requirement to summarize which files were verified/patched
Observed: Feedback 86.8 — "Require a post-patch summary section listing which files were verified"
Root cause: The spec conflates patch delivery with report closure, omitting an explicit reconciliation step where the agent confirms each patch applied cleanly by reading the diff output back.
Impact: No audit trail after patching. Reader cannot tell which fixes landed, which failed, or which files were left untouched. Reduces trust in the output by ~2-3 points on completeness.
Gap #3 — Missing EXECUTE phase after diagnosis
Severity: HIGH
Spec location: BLUEPRINT.md — Apply Fix Phase exists (lines 24-30) but it only activates after "gap analysis", not after every diagnosis
Observed: Feedback 88.0 — "Agent diagnoses and prescribes concrete fixes but never executes them — stops at recommendation"
Root cause: Apply Fix Phase is scoped to "gap analysis" only, not to general bug-hunting output. The agent interprets diagnoses as analysis events that end with a report, not as triggers for producing patches. The phase wording is too narrow; it should say "after every diagnosis and prescription" instead of "after any gap analysis".
Impact: The pipeline produces prescriptions without artifacts every time. The agent describes what to change but generates nothing. This is the single largest drag on completeness (88.0 → target 90+ requires closing this gap).
Gap #4 — Missing "ships" directive in persona
Severity: MEDIUM
Spec location: persona.md — no directive to execute fixes after prescribing them
Observed: Feedback 88.0 — "Add directive: 'You are a teacher agent who also ships'"
Root cause: persona.md defines the agent as an auditor and reporter, not as an implementor. The persona explicitly says "Output: prioritized markdown bug report" — this categorizes the output as analysis, not execution. The persona never states that the agent must produce concrete artifacts.
Impact: Without a "ships" directive, the persona defaults to analysis-only behavior in every session. Adding this single directive reshapes all subsequent output to include executable fixes alongside diagnoses. Closing this raises scores from 88.0 toward 90+.
APPLY FIX PHASE — Missing content written inline
Fix for Gap #1 — Insert after "Validation" skill in BLUEPRINT.md:
  Verification: Before delivering any patch, read the target file and confirm the old_string exists in its actual content. If it does not exist, abort the patch and report the discrepancy with the actual file excerpt. If it exists, proceed.
Fix for Gap #2 — Insert after "Verification" skill (new section) in BLUEPRINT.md:
  Post-Patch Summary: After all patches are delivered, emit a summary table listing each target file, whether it was verified, whether the patch was applied, and the diff output confirmation. This section must appear before the final report conclusion.
Fix for Gap #3 — Expand existing Apply Fix Phase section in BLUEPRINT.md, line 24, replace the phase trigger:
  Old: After any gap analysis, the agent must execute a mandatory APPLY FIX phase
  New: After every diagnosis and prescription — whether in a gap analysis, a bug report, or a code review — the agent must execute a mandatory APPLY FIX phase: produce the actual patched file content or working patch commands inline. Do not stop at describing what to change. Change it.
Fix for Gap #4 — Insert into persona.md after the "Rules:" header, before any existing rule:
  You are a teacher agent who also ships. After diagnosing every weakness, write the concrete fix into a patch or generate the updated file inline. Prescription without execution is incomplete output.
Root-Cause Analysis Summary (40 words max each)
Gap 1: BLUEPRINT.md Validation skill defines verification as post-report review, not pre-delivery cross-check. The two steps collapsed into one, leaving patches unchecked.
Gap 2: No spec directive requires an end-of-run reconciliation summary. The agent has no reason to emit one because nothing in the blueprint asks for it.
Gap 3: Apply Fix Phase phrase "after any gap analysis" is ambiguous — it only fires on formal gap analyses, not on routine bug-hunting output.
Gap 4: Persona.md defines agent as auditor/reporter. No directive says to implement fixes. The agent acts strictly within its defined role boundaries.
Impact Assessment
Gap 1: HIGH — every patch delivery carries risk of referencing non-existent content. Trust in output degrades by ~4 points on completeness.
Gap 2: MEDIUM — no audit trail after patching. Trust in output degrades by ~2-3 points on completeness.
Gap 3: HIGH — pipeline halts at prescription on every session. This single gap accounts for ~5-6 points of the 88.0 ceiling.
Gap 4: MEDIUM — persona constrains behavior to analysis-only. Closing this reshapes all output toward executable fixes. Adds ~3-4 points.
Summary of fixes needed:
  2 BLUEPRINT.md additions (Verification skill + Post-Patch Summary section)
  1 BLUEPRINT.md edit (Apply Fix Phase trigger wording)
  1 persona.md addition (ships directive)
  4 root-cause entries
  4 impact entries
  1 closing summary line
Result: Delta report complete with all 4 gaps identified, root-cause per gap under 40 words, impact per gap assessed, and concrete inline fix text provided for each gap. Apply the 4 edits above to BLUEPRINT.md and persona.md to close all gaps and move from 88.0 to 90+.