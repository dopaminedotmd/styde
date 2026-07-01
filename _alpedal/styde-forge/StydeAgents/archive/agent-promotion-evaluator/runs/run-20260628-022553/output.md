MISSING INPUT: agent name, artifact name, artifact path, and score history.
REQUIRED FORMAT:
- A specific agent name (from StydeAgents/blueprints/ directory)
- The agent's blueprint path
- The agent's score history (last 3+ evals with dates and scores)
- The agent's golden test results (if any)
- The agent's mockup/deliverable (if applicable)
Without any of these, I cannot produce artifactname, artifactpath, verdict, or evidence grounded in real data.
I have read the feedback and the blueprint. Here is what I CAN deliver from available information:
The persona and blueprint contain structural issues that need resolving before any agent evaluation can proceed:
1. Blueprint conflict: The REQUIRED PRECHECK (lines 13-18) mandates hard refusal on missing input, but the latest Teacher Feedback mandates the opposite — graceful partial evaluation with confidence markers. These are incompatible as written.
2. Blueprint conflates two domains: agent-promotion-evaluator (score-history gatekeeping) and mockup-deliverable-auditor (WCAG, breakpoint, feature-completeness table). The accessibility audit and breakpoint verification skills on lines 7-8 are out of scope for an agent promotion evaluator and should live in a separate mockup-review blueprint.
3. Originality Scoring Calibration: references "mockup" scoring in what is supposed to be an agent-promotion blueprint. The originality section on lines 36-42 is designed for visual design review, not agent quality gating. Domain mismatch.
4. Deliverable Integrity (lines 44-50): requires interactive element tagging (W/S/M) and feature completeness tables — these apply to UI mockups, not agent evaluation reports. Another domain mismatch.
I can apply fixes to the blueprint and persona files if you provide the file paths and confirm you want those changes made.
What specific agent shall I evaluate?