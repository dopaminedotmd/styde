CONVERGENCE ANALYSIS: two feedback runs target the same root cause
Root cause: agent produces analysis without acting on it. 20260628-140830 (81.8/100) says fixes are described not applied. The earlier run says claims lack evidence anchoring. Same flaw: the agent outputs a recommendation layer instead of a deliverable layer. Adding more sections to BLUEPRINT.md without addressing this structural issue will increase token cost by ~15-20% with zero quality improvement.
RECOMMENDATIONS
1. Restructure BLUEPRINT.md around a single production gate, not additive sections
Current: 3 rules (evidence anchoring, contingency, two-pass). Each adds 2-4 lines. Total cost delta: +8-12 lines.
Problem: rules accumulate without removing old patterns. The agent will still prescribe instead of produce.
Proposal: merge all three into one "Production Gate" rule:
  Production Gate:
    Before claiming any finding, locate the exact line(s) in tool output or
    transcript that support it. If none exist, report the gap.
    Before ending any task, write the revised file(s) if a concrete fix was
    identified. If the fix requires no file change, state why.
    Both conditions must be met before concluding.
Token cost: +8 lines, replaces 3 separate rules (-6 lines). Net delta: +2 lines.
2. Move contingency analysis into Skills section, not a new section
Current: BLUEPRINT.md has no cross-strategy interaction requirement.
Adding a standalone "contingency analysis" section would add ~6 lines.
Proposal: append one line to each existing Skill entry:
  Threshold: tune compression trigger thresholds. For each setting, state
    interaction with other thresholds and fallback if primary fails.
  Summarize: optimize summarization prompt quality. For each prompt change,
    state interaction with budget settings and fallback.
  Budget: manage token budgets across turns. State interaction with retain
    rules and fallback if budget is exceeded.
  Retain: ensure critical context survives compression. State interaction
    with threshold triggers and fallback.
  Measure: evaluate compression impact on task quality. State confidence
    level for each metric.
Token cost: ~+15 lines total (3 lines added per skill, replacing 0). High cost but directly addresses the contingency gap.
3. Credibility Bounds as a single sentence in Persona, not a new section
Current: persona.md has no credibility constraint.
Proposal: add one line after the existing persona description:
  Credibility: quantify every claim or label it as assumption. No exception.
Token cost: +1 line. Net: +1 line.
4. Two-pass enforcement via a comment in the YAML front matter
Current: no output ordering requirement.
Proposal: add a Pass field to each Skill describing the order:
  Skills:
    - name: Threshold
      pass: 2
      description: tune compression trigger thresholds
Default pass=1 (analysis), pass=2 (production). Agent must complete all pass=1 skills before any pass=2 skill. Automatic block on premature conclusion.
Token cost: +5 lines, no visible change to output density.
TOTAL TOKEN COST OF ALL PROPOSALS
Current BLUEPRINT.md: ~50 lines
Proposed: ~55 lines (+10%)
Current persona.md: ~12 lines
Proposed: ~13 lines (+8%)
Acceptable. The 84.8/100 gap is 0.2 points from production. One more pass resolving the evidence-anchoring issue would push past 85.
IMPLEMENTATION PRIORITY
1. Credibility bounds in persona (+1 line, zero risk) 
2. Production gate in BLUEPRINT.md (+2 lines, replaces 3 rules)
3. Two-pass ordering via pass field (+5 lines, structural)
4. Contingency in skills (+15 lines, highest cost but highest gap coverage)
Cost-to-impact ranking: 1 > 2 > 3 > 4
BREAKEVEN: if this agent scores >=85 on next evaluation, all changes pay for themselves. If not, revert Production Gate and Credibility bounds first (cheapest to revert, highest individual impact).