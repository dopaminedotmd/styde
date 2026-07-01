
---

---
## Feedback from 20260629-222250 (score: 49.2/100)
**Weakest:** completeness | **Cause:** Agent triggered caveman-mode boilerplate instead of processing the evaluation task, producing zero of the requested YAML output — mode-switching overrode all task comprehension. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add a mandatory pre-response checkpoint: before any mode-switch or persona activation, the agent must restate the task in its own words and confirm it has understood what output format is required — if the restatement doesn't match, abort the mode-switch. _(impact: high)_
- **BLUEPRINT.md**: Add an explicit blacklist rule: caveman-mode is forbidden when the task requires structured output (YAML, JSON, specific rubric evaluation). Mode-switching is only permitted for open-ended or conversational tasks. _(impact: high)_
- **persona.md**: Add a fallback instruction: when the agent detects it has no task content to work with (e.g. user provided no SRE task), it must ask clarifying questions or offer example tasks instead of filling the void with irrelevant mode boilerplate. _(impact: medium)_
**Summary:** Catastrophic mode-switch failure: caveman activation consumed the entire evaluation task — gating mode-switches behind task-comprehension checks and blacklisting structured-output tasks from lossy personas is the minimal fix to prevent zero-output failures.
