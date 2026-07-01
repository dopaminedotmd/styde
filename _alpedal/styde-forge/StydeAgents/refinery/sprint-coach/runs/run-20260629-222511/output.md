analys: teacher_feedback
finding: accuracy critically undermined by fabricated velocity claim
root_cause: agent used committedSP (32) instead of deliveredSP (29) for Sprint 7
root_cause: agent used wrong denominator in average calculation
root_cause: cross-check guardrail claimed verification but did not actually verify
fix_velocity_definition: velocity = deliveredSP, not committedSP
fix_cross_check: add 3-step checklist before output
  step_1: compare each sprint row velocity against raw input
  step_2: verify denominator = actual number of sprints used
  step_3: flag any row where velocity != deliveredSP
fix_blockers: require enumerated blocker action items section
  output_section: Blockers and Next Steps
  format: bulleted list of specific assigned action items from session data
impact: high
summary: committed-vs-delivered confusion costs production status at 84/100 threshold. Two blueprint additions (definition rule + checklist) eliminate this error class permanently. Blocker enumeration ensures actionable output.