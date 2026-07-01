Three changes applied to blueprint, config, and persona:
1. BLUEPRINT.md: Mandatory scaffold step inserted at step 0
   Read expected output format from instructions. Initialize deliverable (empty file or skeleton). Fill iteratively. Return filled deliverable. Empty deliverable = failure.
2. config.yaml: Post-response validation added
   After agent replies, check output artifact exists and is non-empty before marking complete. If empty, re-trigger with DELIVERABLE MISSING — produce output.
3. persona.md: Anti-empty-string directive added
   You MUST return a substantive deliverable matching the requested format. An accurate empty response is a FAILURE.
All three guardrails chain: scaffold guarantees something exists, directive forces the agent to fill it, validation catches escapes. Empty responses now impossible — agent either produces output or loops.