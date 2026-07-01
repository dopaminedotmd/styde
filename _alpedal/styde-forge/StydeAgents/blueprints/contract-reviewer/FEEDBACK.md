## Feedback from 20260628-142810 (score: 56.4/100)
**Weakest:** completeness | **Cause:** Agent detects missing input correctly but aborts with an error report instead of fulfilling the user's goal — error messages are not a substitute for the requested deliverable. | **Severity:** critical
**Changes:**
- **persona.md**: Add rule: 'When input is missing or ambiguous, attempt to proceed by offering alternatives (paste input, read from file, accept a format example) rather than returning an error report. The user's goal is a deliverable, not an error message.' _(impact: high)_
- **BLUEPRINT.md**: Add a fallback section: 'MISSING INPUT PROTOCOL — If required data is absent, offer 2-3 concrete alternatives (paste, file path, example scaffold) and proceed with the best available option. Only escalate to abort if all alternatives are explicitly rejected.' _(impact: high)_
- **config.yaml**: Reduce max-turn budget if it is high; increase min-completion threshold if it is low. Ensure the agent has enough iterations to recover from missing input and still produce output. _(impact: medium)_
**Summary:** Agent detects missing input well but aborts instead of delivering — completeness is critically low at 15/100 because error reports replace the required output.

---

---
## Feedback from 20260628-142940 (score: 74.8/100)
**Weakest:** completeness | **Cause:** Agent detects missing input correctly but aborts the request instead of producing partial/placeholder output, scoring zero on completeness for the original task. | **Severity:** critical
**Changes:**
- **persona.md**: Add rule: 'When input is incomplete, produce best-effort output using the available data + explicit placeholders for missing parts, then ask the user to fill gaps. Never return zero output for the original request.' _(impact: high)_
- **BLUEPRINT.md**: Add a 'Missing Input Handler' section that enumerates fallback strategies: (1) scan workspace for supporting files, (2) use sensible defaults/placeholders, (3) produce partial output with [TODO] markers. Only fail if ALL three fail. _(impact: high)_
**Summary:** Agent aborts on partial input instead of producing partial output — fix by encoding a fallback chain that always yields something for the original request.

---

---
## Feedback from 20260628-143349 (score: 90.2/100)
**Weakest:** completeness | **Cause:** Agent stops at offering alternatives when input is missing, rather than first proactively scanning the workspace (codebase, files, git) for the information before falling back to asking the user. | **Severity:** medium
**Changes:**
- **BLUEPRINT.md**: Add a 'proactive discovery' step before the 'fallback alternatives' step: instruct the agent to search the workspace (search_files, git log, read_file) for the missing information before offering alternatives to the user. _(impact: high)_
- **BLUEPRINT.md**: Shift the agent's stance from 'offer options and wait' to 'try the most likely fix, verify it worked, and report what was done'. Replace passive language ('ask the user if they want') with proactive language ('apply the fix, then report the result'). _(impact: medium)_
**Summary:** Composite 90.2 — production-ready. Agent handles missing input gracefully but must become proactively search the workspace before offering fallback alternatives.

---

---
## Feedback from 20260628-143821 (score: 62.8/100)
**Weakest:** completeness | **Cause:** Blueprint produces structured TODO template as the sole output when input is missing, instead of delivering the requested artifact via alternatives (example format, placeholder handling, file-read fallback). | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add a 'missing input fallback' section: when required input is absent, first try reading from a file path, then print a filled-in example as a template the user can edit, then offer to accept pasted data. Never emit TODO blocks as the final output. _(impact: high)_
- **persona.md**: Add directive: 'If you cannot produce the exact artifact due to missing information, output the closest useful approximation — a worked example, a template with realistic placeholders, or a partial result — rather than an error message or TODO skeleton.' _(impact: high)_
- **config.yaml**: Set a minimum-quality gate: if judge-score completeness < 50, force a retry with the missing input handled via a concrete fallback strategy (example output, file-read, format prompt). _(impact: medium)_
**Summary:** Agent correctly detects missing input but outputs TODO templates instead of the requested artifact — a refusal pattern the judge penalizes as effectively zero-value output, dragging completeness to 15 and usefulness to 25.
