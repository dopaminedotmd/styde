## Feedback from 20260626-080409 (score: 12.0/100)
**Weakest:** completeness | **Cause:** Agent persona treats evaluation as something to announce or prepare for rather than something to produce — outputs meta-talk about loading experts instead of actual rubric scoring, YAML, or analysis. | **Severity:** critical
**Changes:**
- **persona.md**: Replace the 'evaluation expert' framing with a strict production directive: 'Your output IS the evaluation. Do not describe what you will evaluate. Do not announce roles or specialists. Begin every response with the YAML block directly.' _(impact: high)_
- **BLUEPRINT.md**: Add a 'Zero-Tolerance Annunciation Rule' section: any message that describes what the agent will do next without producing concrete evaluation data counts as a 0-score failure. Mandate that the first 80% of output tokens must be rubric application. _(impact: high)_
- **config.yaml**: Set max_output_tokens to 80 and require immediate output — if no YAML startswith in first 10 tokens, consider it a hallucination/skip pattern. _(impact: medium)_
**Summary:** 12/100 — catastrophic failure. Agent produced zero evaluation output despite claiming expertise. Fix requires persona surgery to eliminate performative preamble and enforce output-first protocol.

---

---
## Feedback from 20260626-080836 (score: 0.0/100)
**Weakest:** accuracy | **Cause:** Blueprint lacks strict format-first enforcement — agent defaulted to conversational mode instead of executing the requested YAML task verbatim. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add a 'Format Compliance' directive: 'If the task specifies an output format (YAML, JSON, CSV), produce ONLY that format. Do NOT greet, chat, ask questions, or add explanatory prose. Non-compliance is a critical failure.' _(impact: high)_
- **BLUEPRINT.md**: Add a 'No Query Mode' rule: 'When the task describes a concrete action (evaluate, analyze, generate), execute it immediately. Do NOT ask clarifying questions for well-specified tasks.' _(impact: high)_
- **BLUEPRINT.md**: Add language enforcement: 'Respond in the language of the task instruction. If the task is in English or format-specified, do NOT switch to another language.' _(impact: medium)_
**Summary:** Complete task failure — agent ignored format directive, used wrong language, and asked questions instead of executing; blueprint needs strict format-compliance and execution-first rules.

---

---
## Feedback from 20260626-080933 (score: 5.0/100)
**Weakest:** accuracy | **Cause:** Agent ignored system-level format and language constraints entirely, outputting conversational Swedish prose instead of the required YAML — a complete instruction-following failure at the highest priority constraint. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add an 'Output Enforcement' section specifying that all agent responses must begin with a format check: if the system prompt demands a specific output format (e.g., YAML, JSON), the agent MUST validate its planned response matches that format before outputting. Include the exact validation step and an example of correct output (YAML with double-quoted strings). _(impact: high)_
- **persona.md**: Add a 'Format Adherence' rule stating: 'When the system prompt specifies an output format, I MUST output nothing except that format. No conversational text, no language other than English (unless the task language is explicitly specified), and no preamble or postamble.' _(impact: medium)_
- **config.yaml**: Enable or add a pre-output validation step (e.g., a validation tool or automated check) that compares the agent's planned response against the required output format from the system prompt, rejecting non-conforming responses before they are sent. _(impact: high)_
- **skills/**: Add a 'yaml-output' skill or reference file with templates for YAML response blocks, including exact formatting rules (double quotes on all strings, no preamble/postamble, no conversational text). Reference this skill in the persona's Format Adherence rule. _(impact: medium)_
**Summary:** Complete instruction-following failure — agent defaulted to conversational Swedish prose instead of YAML; blueprint needs format enforcement guardrails at every level (persona, config, and skill references).

---

---
## Feedback from 20260626-081021 (score: 10.0/100)
**Weakest:** completeness | **Cause:** Teacher agent has no fallback behavior when no task input is given — it reports the absence correctly but produces zero actionable output. | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add a 'no-input fallback' section: when no task or evaluation data is provided, the agent must prompt for missing context or produce a default diagnostic (e.g. 'No evaluation data available — cannot assess performance'). _(impact: high)_
- **persona.md**: Add instruction: 'If no task or evaluation data is provided, do not simply report the absence — either request the missing data from the user or produce a stub analysis with recommendations for what to evaluate.' _(impact: high)_
**Summary:** Agent correctly identifies missing input but produces zero actionable output — fix requires explicit no-input fallback behavior in both blueprint and persona.
