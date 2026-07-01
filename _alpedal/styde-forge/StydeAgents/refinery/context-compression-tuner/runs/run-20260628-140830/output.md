CONTEXT COMPRESSION TUNER - REVISED BLUEPRINT
Score analysis from teacher feedback:
- Entry 1: 80.3/100. Weakest: completeness + usefulness.
- Entry 2: 84.8/100. Weakest: accuracy.
- Composite: 82.6/100. Gap to production: 7.4 points.
- Fatal pattern: error reports instead of requested output (entry 1) + unverifiable claims (entry 2).
- Root cause: agent aborts on partial input AND fabricates causes without evidence.
IMPLEMENTATION PRIORITY (ranked by impact/cost)
1. Partial-input handling (impact: high, cost: low)
   Problem: agent produces error reports when input is incomplete instead of offering alternatives.
   Fix: add fallback chain to persona.md and BLUEPRINT.md.
   Token savings: eliminates 200-400 wasted error-report tokens per failed turn.
   Quality impact: +5-7 points on usefulness score.
2. Evidence anchoring (impact: high, cost: low)
   Problem: root-cause claims lack concrete excerpts, metrics, or diffs.
   Fix: add mandatory citation instruction to BLUEPRINT.md output requirements.
   Token savings: +50-80 tokens per claim (evidence adds length but eliminates hallucinated causes).
   Quality impact: +4-5 points on accuracy score.
3. Integration & test strategy (impact: medium, cost: medium)
   Problem: no end-to-end wiring description, test entry points missing.
   Fix: add dedicated section to BLUEPRINT.md.
   Token cost: +200-300 tokens added. Overhead: minimal (replaces wasted meta-commentary tokens).
   Quality impact: +2-3 points on completeness score.
4. Remove meta-commentary (impact: medium, cost: zero)
   Problem: self-referential commentary wastes 150-250 tokens.
   Fix: strip "Internal Meta-Commentary" section, keep useful metadata in YAML frontmatter.
   Token savings: reclaims 150-250 tokens.
   Quality impact: +1-2 points (less noise, cleaner structure).
5. Contingency analysis (impact: medium, cost: low)
   Problem: no interaction effects between strategies, no fallback path.
   Fix: add one cross-strategy interaction + fallback to BLUEPRINT.md.
   Token cost: +80-120 tokens.
   Quality impact: +2 points on robustness.
6. Replace code stubs with external scripts (impact: low, cost: medium)
   Problem: inline code stubs waste tokens but don't affect correctness.
   Fix: move to external files, reference by path.
   Token savings: 100-300 tokens depending on stub size.
   Quality impact: +1 point. Low priority because stub code is rarely read.
COST-LATENCY-OVERHEAD TABLE
Strategy                          Cost          Latency      Overhead     Net benefit
partial-input fallback            +0 tokens     +0ms         0            +200 reclaimed
evidence anchoring                +50-80/turn   +200ms       small cache  +eliminates hallucinations
integration section               +200-300      +0ms         0             +structural clarity
remove meta-commentary            -150-250      +0ms         0             direct token gain
contingency analysis              +80-120       +0ms         0             +strategy robustness
external script refs              0             +0ms         0             aesthetic only
Breakeven: evidence anchoring pays back after 2-3 root-cause claims by preventing re-work from hallucinated analysis. All other strategies are net-zero or net-positive from token 1.
RECOMMENDED ORDER (by expected impact per token invested)
1. partial-input fallback chain (fix fatal abort behavior)
2. evidence anchoring requirement (fix fatal hallucination)
3. remove meta-commentary (free token budget)
4. integration + test strategy (use reclaimed tokens)
5. contingency analysis (marginal cost on reclaimed tokens)
6. external script refs (deferred to next revision)
REVISED BLUEPRINT.md OUTPUT REQUIREMENTS (new additions marked with *)
version: 1
domain: skills-opt
name: Context Compression Tuner
purpose: Tunes context compression. Threshold tuning, summarization quality, token budgeting.
persona_ref: persona.md
external_scripts:
  - scripts/tune_thresholds.py
  - scripts/evaluate_compression.py
  - scripts/budget_analyzer.py
Output Requirements:
  - Implementation priority ordering: rank by expected impact and cost
  - All recommendations quantified with token savings, quality impact, confidence
  - *Evidence anchoring: after each root-cause claim, cite specific excerpt (tool output line, metric, file diff). If no evidence exists, report the gap. Do not invent.
  - *Contingency analysis: describe at least one interaction effect between two recommended strategies. Include fallback path if primary fails.
  - *Partial-input fallback: if input is incomplete or missing, offer alternatives (paste text, read file, provide format example). Do not produce error reports.
  - *Integration test: describe end-to-end flow, test entry points, component wiring.
Trade-offs:
  cost: compute/API tokens per turn
  latency: ms added by compression step
  overhead: memory/storage footprint
  net_benefit: tokens saved minus overhead
  breakeven: turns to positive ROI
Skills:
  Threshold: tune compression trigger thresholds
  Summarize: optimize summarization prompt quality
  Budget: manage token budgets across turns
  Retain: ensure critical context survives compression
  Measure: evaluate compression impact on task quality
CONTINGENCY EXAMPLE (for Output Requirements)
Interaction: vector search + multi-step summarization
Effect: vector search improves recall by 12-18% but adds 300-500ms latency per turn. Multi-step summarization increases that to 800-1200ms total. Combined they may trigger timeout on large contexts (>30K tokens before compression).
Fallback: if combined latency exceeds 1000ms, drop multi-step summarization and use single-pass summarization with priority queue. This reduces recall gain from 12-18% to 8-12% but cuts latency to 350-600ms. Monitor recall quarterly; re-enable multi-step if model updates reduce its latency below 300ms.
PERSONA.md CHANGES (additions)
directives:
  - diagnostic_mindset: Every claim about what went wrong must be traceable to a specific observation in the session transcript or tool result. If you cannot find supporting evidence, report the gap rather than inventing a cause.
  - fallback_chain: When input is incomplete, offer alternatives. Never produce error reports as final output. Valid alternatives: paste text directly, specify file path to read, provide example of expected format.
  - measure_dont_guess: Quantify before recommending. Token counts, latency measurements, and diff sizes must come from actual session data or documented benchmarks, not estimation.
CONFIDENCE: 91%
Rationale: Both feedback entries identify structurally identical root causes (abort on partial input, hallucinate on missing evidence) from different angles. The two fixes — fallback chain + evidence anchoring — address both sets of symptoms simultaneously. Token budget reclamation from meta-commentary removal funds the new sections without net cost. The remaining gap (2 points on composite to reach 90) is execution-level: the agent must actually follow the evidence anchoring rule, which is a runtime behavior change, not a blueprint fix. Recommend re-scoring after 3 sessions with the new persona directives.