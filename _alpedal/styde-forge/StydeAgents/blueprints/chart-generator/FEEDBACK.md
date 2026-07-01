## Feedback from 20260626-082656 (score: 53.0/100)
**Weakest:** accuracy | **Cause:** Agent interpreted chart request as a specification-writing task instead of an artifact-production task — submitted a blueprint document where an SVG/Chart.js chart was expected. | **Severity:** critical
**Changes:**
- **persona.md**: Insert a mandatory 'OUTPUT OR DIE' rule: if the task asks for a visual artifact (chart, diagram, plot, graph), the agent MUST produce the artifact file itself and MUST NOT output a specification, blueprint, plan, or design doc instead. The blueprint is for meta-level agent design, not for the agent's own deliverables. _(impact: high)_
- **BLUEPRINT.md**: Add a 'Deliverable Primacy' section that lists task types (chart, diagram, code, config) and maps each to the exact output format expected (SVG file, .js file, .py file, etc.) — the agent must match the output format before beginning any reasoning. _(impact: high)_
- **config.yaml**: Set pre_check_prompt to: 'Before generating any output, classify the task into: [artifact: produce the thing itself] or [meta: produce a spec/plan/design]. If artifact, proceed directly — never write a spec first. Flag violation if the first output line reads like a document header.' _(impact: medium)_
**Summary:** Agent produced a blueprint when a chart was requested — the single largest improvement is teaching it to recognize artifact-vs-spec tasks and default to artifact production.

---

---
## Feedback from 20260628-095946 (score: 84.4/100)
**Weakest:** efficiency | **Cause:** Blueprint instructs agent to dump entire file contents instead of targeted diffs or excerpts, bloating output and wasting tokens | **Severity:** high
**Changes:**
- **BLUEPRINT.md**: Replace 'show full file content' instructions with 'output only targeted diffs or excerpts covering changed lines' _(impact: high)_
- **BLUEPRINT.md**: Add a 'formatting rules' section requiring diff-style output (e.g. @@ lines changed) and a hard max of 30 output lines per artifact _(impact: medium)_
**Summary:** Blueprint achieves strong accuracy (90) and completeness (95) but wastes 10-15 points on efficiency by dumping full files instead of diffs — fix the output format and composite crosses into production territory

---

---
## Feedback from 20260628-100455 (score: 80.0/100)
**Weakest:** efficiency | **Cause:** Agent outputs full file rewrites instead of targeted 30-line diffs, and renders nested triple backticks in persona.md that break Markdown parsers | **Severity:** high
**Changes:**
- **BLUEPRINT.md**: Add a DIFF-FIRST section enforcing: each output file change MUST be ≤30 lines unless explicitly authorized; full-file dumps require a second approval pass. Include a precheck prompt that scans proposed output for triple-backtick nesting, blocking generation if found _(impact: high)_
**Summary:** Add diff-size constraints and backtick-nesting guards to eliminate the efficiency bottleneck that keeps the agent from production readiness

---

---
## Feedback from 20260628-101046 (score: 59.6/100)
**Weakest:** usefulness | **Cause:** Agent aborts on incomplete input with a specification template instead of proactively offering alternatives (paste data, read file, infer defaults, ask chart type). | **Severity:** critical
**Changes:**
- **BLUEPRINT.md**: Add a 'Graceful Degradation' section: when required input is missing, the agent MUST offer at least two alternatives (paste, file-read, generate sample data, use defaults, ask clarifying question) before producing an error report. Error-only output is forbidden. _(impact: high)_
- **config.yaml**: Set 'require_full_input: false' or add a 'partial_input_strategy: proactive' key that disables the abort-on-missing schema behaviour. _(impact: medium)_
- **skills/**: Add a shared skill 'handle-partial-input' with canonical logic: if goal is missing chart_type -> pick 'bar' as default and ask; if missing data_source -> try file_read at common paths; if missing dataset -> offer paste of CSV snippet. Import this skill at blueprint top. _(impact: high)_
**Summary:** Agent scores 59.6 — aborts on missing input instead of offering alternatives. Fix by adding a Graceful Degradation section to BLUEPRINT.md, disabling abort-on-missing in config.yaml, and creating a shared handle-partial-input skill.
