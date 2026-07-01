The BLUEPRINT.md is at 2 iterations of feedback and both address one root: token waste. The 87.6 run flagged missing structure. The 86.8 run hit the same root — inline content bloating beyond the verbosity budget.
ROOT CAUSE ANALYSIS
Primary failure mode: Blueprint carries verbosity budget constraints but violates them itself. Self-referential meta-commentary and inline code are the biggest token sinks. The compression setting (threshold) is set too permissive for the output format.
Secondary failure mode: Missing structural sections (Integration & Test Strategy) force the blueprint to compensate with inline prose that should live in a separate artifact. This is a summarization quality issue — the blueprint tries to be both spec and implementation reference.
RANKED RECOMMENDATIONS
rank: 1
recommendation: Set hard verbosity cap at 2500 tokens for BLUEPRINT.md output
domain: Budget
rationale: Blueprint consistently exceeds its own budget by 15-22% in last two runs
token_saving: direct — caps overshoot entirely
quality_impact: positive — enforces structural discipline
cost: 0 (strict truncation at generation)
confidence: 85
rank: 2
recommendation: Ban all inline code stubs longer than 5 lines; enforce path-only references to scripts/
domain: Threshold
rationale: Inline Python blocks consume 40-60 lines each; removing them recovers ~800 tokens per stub
token_saving: 1200-1800 tokens per blueprint iteration
quality_impact: neutral — code is structurally identical by path reference
cost: 0 (already have a scripts/ directory structure)
confidence: 92
rank: 3
recommendation: Replace ROUGE-L with compression ratio + BERTScore semantic equivalence
domain: Measure
rationale: ROUGE-L penalizes compression-optimized output structure; compression ratio directly measures the Budget dimension
token_saving: indirect — correct measurement drives better compression behavior
quality_impact: positive — measures what matters instead of n-gram overlap
cost: low — BERTScore call per evaluation (API cost negligible per eval)
latency: +200ms per eval
confidence: 85
rank: 4
recommendation: Strip Internal Meta-Commentary section; fold metadata into YAML frontmatter (version, domain, persona)
domain: Summarize
rationale: The section serves no downstream consumer; frontmatter is machine-readable and shorter
token_saving: 300-500 tokens per document
quality_impact: positive — reduces self-referential noise
cost: 0
confidence: 90
rank: 5
recommendation: Add Integration & Test Strategy section with explicit section-header-only anchor points
domain: Retain
rationale: Missing section causes blueprint to scatter integration details throughout prose, inflating token count
token_saving: -50 (section adds tokens) but enables -300 elsewhere by consolidating
quality_impact: positive — eliminates scattered references
cost: 0
confidence: 80
rank: 6
recommendation: Define Affirmative vs Detailed output mode based on query depth heuristic (<=3 keywords = affirmative)
domain: Budget
rationale: Current format always defaults to detailed, wasting tokens on shallow queries
token_saving: variable, 40-60% on shallow queries
quality_impact: neutral if well-calibrated
cost: 0 (heuristic, no API call)
confidence: 75
TRADE-OFF SUMMARY
| Strategy | Tokens Saved | Latency | Cost | Confidence |
|----------|-------------|---------|------|-----------|
| Hard verbosity cap | 300-600 | 0 | 0 | 85 |
| Ban inline stubs | 1200-1800 | 0 | 0 | 92 |
| BERTScore metrics | indirect | +200ms/ev | low | 85 |
| Strip meta-commentary | 300-500 | 0 | 0 | 90 |
| Add Integration section | -50 (net +250) | 0 | 0 | 80 |
| Affirmative/detailed modes | 40-60% shallow | 0 | 0 | 75 |
Recommended execution order: 2, 4, 1, 5, 3, 6
Apply inline stub ban and meta-commentary strip first (zero cost, highest token savings). Then set verbosity cap to prevent regression. Add Integration section to absorb scattered prose. Swap metrics last since it requires evaluation infra changes. Affirmative/detailed modes are low-confidence secondary optimization — skip unless token budget remains tight after first four.