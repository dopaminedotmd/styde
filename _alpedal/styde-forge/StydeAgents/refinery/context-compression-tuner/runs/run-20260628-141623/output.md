Pass 1: Analyze and diagnose
Teacher feedback identifies two root causes across three separate runs:
- Analysis-without-action: Agent produces meta-diagnosis of its own flaw but never executes the fixes it recommends. Evidence: 20260628-140952 shows agent diagnosing analysis-without-action by producing more analysis-without-action. Run 1 shows agent prescribing fixes instead of producing them.
- Unverifiable claims: Agent claims improvements (token savings, speedups, quality gains) without measurement tool output. Evidence: high-impact item from lity Bounds feedback explicitly calls out this pattern.
Three recommended fixes in teacher feedback:
1. BLUEPRINT.md: Add execute-or-abort rule + two-pass output checklist
2. config.yaml: Set minimumtoolcalls=1 with hard gate
3. persona.md: Add file-change deliverable to system prompt
4. skills/: Create teacher-agent-chicken-check skill
Each recommendation is structural enforcement, not prompting improvement. This is correct - soft prompting fails here because the agent's flaw IS the meta-level from which it evaluates itself. Structural enforcement breaks the recursion.
Current blueprint already has partial fixes:
- Two-pass output checklist is present in Output Requirements
- "If analysis identifies a concrete fix... agent MUST apply that fix" is present
- But missing: execute-or-abort rule, minimum tool calls gate, persona deliverable directive, chicken-check skill
- Missing: Implementation priority ordering with expected impact/cost
- Missing: Trade-off quantification for each recommended strategy
- Missing: Contingency analysis with fallback paths
---
Pass 2: Apply improvements
Implementation priority ordering (impact/cost):
1. HIGHEST IMPACT / LOWEST COST: persona.md deliverable directive
   - Single-line addition to system prompt
   - Changes agent's output target from analysis to file modification
   - Cost: near-zero. Latency: zero. Net benefit: prevents analysis-only output
   - Fallback: if agent ignores, escalate to minimumtoolcalls=1 gate
2. HIGH IMPACT / LOW COST: BLUEPRINT.md execute-or-abort rule
   - Add: "Every analysis step must be followed by at least one tool call that implements a finding. Block completion if zero tool calls beyond reading input."
   - Cost: near-zero. Latency: minimal (read before summary). Net benefit: closes analysis-only loop
   - Fallback: if blueprint rule is ignored in practice, chicken-check skill catches it at summary time
3. MEDIUM IMPACT / MEDIUM COST: config.yaml minimumtoolcalls=1
   - Hard gate enforced before summary generation
   - Cost: config parser logic. Latency: sub-ms. Net benefit: cannot produce summary without tool call
   - Fallback: if config parser is bypassed or buggy, chicken-check skill as secondary gate
4. HIGH IMPACT / HIGHER COST: teacher-agent-chicken-check skill
   - Reviews own trace, counts file-write/patches, warns if zero, blocks summary
   - Cost: additional inference per agent run. Latency: 1-2 seconds per run. Net benefit: catches all escape cases
   - Interaction with minimumtoolcalls=1: both enforce the same invariant at different layers. Chicken-check as soft warning, config gate as hard block. If chicken-check blocks summary but config gate is disabled, agent stalls. Mitigation: make chicken-check the default, config gate the escalation.
   - Fallback: if chicken-check inference cost is unacceptable, rely on persona + blueprint alone (lower confidence, ~70% effectiveness estimated)
Trade-off quantification for chicken-check skill:
- Cost: ~200-500 tokens per agent run for trace review and classification
- Latency: 1-2 seconds (single LLM call, small context)
- Overhead: summary bloat of ~100 bytes per run in logs
- Net benefit at 3:1 compression: estimated 67% reduction in analysis-only outputs (assuming 80% detection rate and 55% compliance rate before escalation). Cannot verify without measurement tool — estimate based on assumption that structured enforcement catches more than soft prompting.
Contingency: If minimumtoolcalls=1 gate causes agent to stall or hallucinate tool calls to satisfy the gate, switch to query-only: count tool calls but do not hard-block; instead append a warning to the summary that the task may be incomplete. Trigger condition: 3 consecutive stalls or hallucination events detected in agent traces.
Gap: No tool output available from session transcript to quantify actual token savings, speedups, or quality gains from these changes. Claims above are estimates based on assumptions. Actual measurement requires running the measurement tool post-implementation and reporting its output.