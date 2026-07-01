---
name: competitive-brief-generation
description: >
  Generates competitive briefs with rigorous source attribution. Every claim
  must be paired with its provenance and a confidence score. Rejects unsourced
  assertions. Produces weekly briefs in a structured Claim | Source | Confidence
  format that enables rapid verification.
---

## Structure

Every competitive brief MUST use this three-column format for each change:

| Claim | Source | Confidence |
|-------|--------|------------|
| [What changed, including quantitative data] | [File path, URL, report ID, line number] | [0-100 based on source reliability + recency] |

## Rules

- Every row in the brief must have all three columns populated. No empty cells.
- Quantitative values (dates, prices, percentages, counts) must appear inside the Claim column only if the Source column references a verifiable document.
- Confidence scoring: 90-100 = primary source within 24h; 70-89 = primary source within monitoring window; 50-69 = secondary source with corroboration; below 50 = exclude from brief.
- If a claim cannot be sourced, exclude it. Do not insert placeholder sources.
- At least 3 independent sources per claimed change, each with verifiable timestamps.
- Each claimed change must have at least one source timestamped within the current monitoring window (fresh evidence gate).
- After generation, scan the brief for any numeric values not preceded by an inline citation marker. Flag and fix before finalizing.
- If zero independently sourced changes survive validation, output: 'No verifiable changes this cycle — escalated to human review'. Attach the research log.

## Validation Steps

1. For each claim, trace the Source to the actual document. Verify the data matches.
2. Check every Source timestamp is within the current monitoring window.
3. For each quantitative value in Claim, confirm there is a preceding citation marker referencing the Source.
4. Count independent sources per claim. Reject claims with fewer than 3.
5. If the brief would be empty after validation, switch to zero-changes escalation.
