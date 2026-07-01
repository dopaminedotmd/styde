Evaluating agent agent-promotion-evaluator at StydeAgents/blueprints/agent-promotion-evaluator
artifactname: agent-promotion-evaluator
artifactpath: StydeAgents/blueprints/agent-promotion-evaluator
verdict: hold
evidence: |-
  Score history: eval id 3/4 composite 90.2 (S:86 J:93) on 2026-06-28T01:28:56Z, then eval id 11/12 composite 44.8 (S:25 J:58) on 2026-06-28T01:38:45Z. delta of -45.4 points, a 50.3% drop.
  Critical regression cause confirmed: FEEDBACK.md at line 15-20 documents agent fabricates factual claims (commit hashes, line numbers, timestamps) without tool call verification. accuracy component scored 25/100.
  Promotion threshold not met: requirement is 3 consecutive >=85 scores. agent has 0 consecutive >=85 scores in its evaluation history. 44.8 and 90.2 are both below the 3-count requirement.
  Drift signal: negative. score dropped from 90.2 (above threshold) to 44.8 (far below). single iteration regression indicates a fundamental process failure, not marginal variance.
  Co-evaluation evidence: low self-score (25) and low judge score (58) on id 11/12 correlate with documented hallucination behavior. scores accurately reflect output quality.
  Ongoing remediation: spawn id 14 at iter 3/5 (status: running, progress: 20%) started 2026-06-28T01:39:05Z after improve id 13 which implemented evidence traceability and pre-output claim verification gates. no evaluation results available from this spawn yet.
  Recommendation: hold for at least 3 completed evaluations after spawn id 14 finishes. require >=85 on all 3 before promotion consideration. if next eval scores <70, downgrade to archive. efficiency improvement from feedback 20260628-012706 (repetitive evidence blocks) is lower priority than hallucination fix.
  No promotion or archive file operation needed for hold verdict. agent-promotion-evaluator remains in refinery at StydeAgents/blueprints/agent-promotion-evaluator pending score recovery.