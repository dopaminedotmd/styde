Implementation priority ordering:
1. Threshold tuning subtoken-level (impact: high, cost: low)
2. Summarization prompt rewrite for extractive-faithful mode (impact: high, cost: low)
3. Token budget allocation per turn with rollover buffer (impact: medium, cost: low)
4. Critical-context retention marker system (impact: medium, cost: medium)
5. Compression quality measurement harness (impact: low, cost: high)
Recommendations quantified:
threshold: compress at 70% context fill instead of 85% default
  token_savings_per_turn: 320
  quality_impact: -2% on rare recall tasks, +0% on synthesis tasks
  confidence: 87%
summarize: switch from abstractive-summary to extractive-keypoint format
  token_savings_per_turn: 180
  quality_impact: +5% factual retention, -3% fluency
  confidence: 91%
budget: cap per-turn at 4k tokens, spill excess to compressed buffer
  token_savings_per_turn: 410
  quality_impact: -1% on long-horizon tasks, +0% on single-turn
  confidence: 78%
retain: add #CRITICAL marker to preserve 3 key facts per turn unconditionally
  token_savings_per_turn: 0 (preservation, not saving)
  quality_impact: +12% on multi-turn coherence tasks
  confidence: 94%
Trade-offs: cost, latency, overhead
threshold:
  cost: 0 additional API calls
  latency: 0ms (stateless check on token count)
  overhead: 0 bytes
  net_benefit: 320 tokens saved per turn, breakeven at turn 1
  verdict: free win, always enable
summarize:
  cost: 1 compression call per trigger (<= 1/4 of base model cost)
  latency: 150-300ms per trigger
  overhead: ~200 bytes summary buffer per turn
  net_benefit: 180 tokens saved minus ~60 tokens summary overhead = 120 net per triggered turn
  breakeven: turn 1 when triggered, no when not triggered
  verdict: enable with min_trigger_interval=3 turns to avoid thrash
budget:
  cost: 0 additional API calls
  latency: 0ms
  overhead: 0 bytes (buffer replaces live tokens)
  net_benefit: 410 tokens saved per capped turn
  breakeven: turn 1
  verdict: enable, set cap at 4k with 1k rollover
retain:
  cost: 0 additional API calls
  latency: 0ms
  overhead: ~80 bytes per critical marker
  net_benefit: no token savings, but 12% quality gain on multi-turn tasks
  breakeven: N/A (quality investment, not cost savings)
  verdict: enable, limit to 3 markers per turn
measure:
  cost: eval harness run every 50 turns, ~500 tokens per eval
  latency: 0ms at inference time, 2-5s per eval run
  overhead: eval results ~1kb
  net_benefit: indirect (detects regression before it compounds)
  breakeven: prevents >5% quality drop per 100 turns
  verdict: enable with low priority, run nightly