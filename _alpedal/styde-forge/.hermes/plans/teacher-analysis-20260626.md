```yaml
diagnosis:
  weakest_dimension: "accuracy"
  root_cause: "Agent made claims about code structure, error handling, and parallelism without reading any source files — claims were plausible but unverified, and the fix proposal was generic rather than referencing actual code locations."
  severity: "high"

improvements:
  - target: "BLUEPRINT.md"
    change: "Add a mandatory 'evidence gathering' phase before analysis: the agent must read and cite specific source files (paths + line numbers) for every claim about current code behavior, error handling, or architecture."
    reason: "Prevents hallucinated code-state claims; forces the agent to ground analysis in actual source code rather than inference from prompt context alone."
    expected_impact: "high"
  - target: "BLUEPRINT.md"
    change: "Add a structured fix template requiring three fields per recommendation: (1) exact file path, (2) current behavior quote/snippet, (3) specific proposed change with implementation sketch. Reject generic suggestions like 'add validation' without file-level detail."
    reason: "The judge noted the fix suggestion was 'brief and lacks implementation detail' — a template enforces the specificity needed for the fix to be actionable."
    expected_impact: "high"
  - target: "config.yaml"
    change: "Set a minimum confidence threshold for claims about code state: if the agent hasn't read the relevant file, confidence is automatically 'low' and flagged as unverified. Optionally add a tool-use requirement (e.g., must use read_file or search_files before any code-state assertion)."
    reason: "Self-eval accuracy was 65 specifically because claims were unverified. A config-level guardrail codifies the methodology and prevents the pattern from recurring."
    expected_impact: "medium"

summary: "Accuracy (65) is the critical weakness — the agent's claims about code state were unverified because it never read the source files. Fix: add mandatory evidence-gathering phase and structured fix template to BLUEPRINT.md."
```
