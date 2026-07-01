artifactname: N/A
artifactpath: N/A
verdict: cannot evaluate
evidence: |-
  Required input missing: no candidate agent name, no blueprint path, no score history, no golden test set, no evaluation data of any kind provided in the prompt
  PRECHECK 1 FAILED: cannot name the agent being evaluated or its blueprint path because no candidate was specified
  PRECHECK 5 FAILED: no features to verify, no implementation status to assess
  The persona configuration, blueprint definition, and output format rules are all instructions for an evaluator role, not evaluation data. Running an evaluation against zero data would constitute fabrication — the exact failure flagged in the teacher feedback as highest-impact finding
  Provide: agent name, blueprint path, score history (3+ consecutive evals), golden test results, and any mockups or output to evaluate