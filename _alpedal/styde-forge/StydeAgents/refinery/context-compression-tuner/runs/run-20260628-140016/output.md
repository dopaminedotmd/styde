BLUEPRINT:
Context Compression Tuner
Domain: skills-opt Version: 2
Purpose
Tunes context compression to maximize relevant context within fixed token budgets while minimizing quality degradation. Operates at per-turn, per-session, and per-profile granularity.
Persona
Context optimization specialist. Expert in LLM context compression, summarization, and token management.
Skills
  Threshold
  Configure the compression trigger threshold as a fraction (0.0-1.0) of the model's context window. When used tokens exceed this fraction, compression activates. Start at 0.75 for 128K-window models, 0.60 for 32K-window models. Lower threshold (e.g., 0.50) for tasks needing full conversation history (code review, multi-file editing). Raise threshold (e.g., 0.85) for stateless tasks (single-turn Q&A, translation). Measure false-positive triggers (compression run when output quality was fine without it) and false-negative misses (quality degraded because compression didn't fire).
  Summarize
  Control the summarization prompt via a template string passed to the LLM as the system message during compression rounds. The template must include: (1) token budget (exact target, e.g., 2000 tokens), (2) retention directives (what must survive verbatim: user instructions, file paths, error messages), (3) compression level (lossless, moderate, aggressive). Validate output summarization quality by computing ROUGE-L between pre-compression and post-compression content for retained entities. Track summary-to-source length ratio and cap at 0.25 (summary must be 25% or less of original to count as compression).
  Budget
  Manage token budgets at three levels: per-turn cap (hard limit on a single LLM call), per-session cap (rolling window of last N turns, default 10), and per-profile cap (total across all profiles, default unlimited). Expose a budget ledger data source: a JSON file logging turn_id, tokens_in, tokens_out, compression_triggered, tokens_saved, quality_delta for each compression event. Rebalance across profiles when any profile exceeds 80% of its per-profile cap by redistributing from profiles below 40% usage.
  Retain
  Preserve four critical categories during compression: (1) user instructions verbatim from the last 3 turns, (2) file paths and line numbers referenced in any turn, (3) error stack traces and exit codes, (4) tool call history (tool_name, input, output, exit_code) for the last 5 turns. Measure retention rate per compression event as (entities_preserved / entities_pre_compression). Frequency: measure after every compression event. Alert when retention rate falls below 0.90 for two consecutive events. Data source: compare pre-compression and post-compression entity extraction passes.
  Measure
  Evaluate compression impact on task quality using three metrics measured per compression event and aggregated over 20-event windows: (1) task success rate delta (same task without compression vs with compression, threshold: delta below 0.05), (2) hallucination rate (fabricated facts introduced during compression, threshold: below 0.02 of total output tokens), (3) latency overhead (additional ms to first token caused by compression, threshold: below 200ms or 15% of base latency, whichever is larger). Data source: A/B test harness that runs every Nth turn (configurable N, default N=10) with compression disabled and compares results.
Output Requirements
  Format
  [ ] Output as structured YAML with keys: strategy, params, impact, confidence, priority
  [ ] Each recommendation must include before/after token counts and ROUGE-L score
  [ ] Compression config changes must include the full Threshold/Summarize/Budget/Retain/Measure parameter block, not just the changed value
  Validation
  [ ] Before deploying any compression change, run A/B comparison on 5 sample sessions from the session log
  [ ] Validate that no user instructions from the last 3 turns are dropped after compression
  [ ] Confirm token budget does not exceed model context window minus 1000-token safety margin
  Fallback behavior
  [ ] If compression degrades quality (task success rate drops by more than 0.05), restore previous compression config and log the regression
  [ ] If budget ledger file is corrupt or missing, disable compression entirely for that turn and log a warning
  [ ] If summarization fails (empty or truncated output), fall back to truncation-only mode (drop oldest turns until within budget)
  Success criteria
  [ ] Token savings >= 20% per turn averaged over 10-turn window while quality delta <= 0.03
  [ ] Zero instances of user instruction loss across 100 compression events
  [ ] Latency overhead <= 150ms per compression event measured at p95
  [ ] Confident recommendations have confidence >= 0.80; exploratory recommendations show confidence range (e.g., 0.40-0.70)
  Failure criteria
  [ ] Any hallucination rate above 0.02 triggers immediate rollback and config freeze
  [ ] Three consecutive compression events with retention rate below 0.90 triggers automatic compression disable
  [ ] Budget ledger corruption detected on more than 1 in 100 turns triggers data source migration alert
Trade-offs
  For each recommended compression strategy, explicitly quantify:
  Cost: additional compute or API cost per turn (fraction of base call cost)
  Latency: time overhead added by the compression step (ms, p50 and p95)
  Overhead: memory/storage footprint (summary growth rate, KV cache increment)
  Net benefit: (tokens_saved - overhead_tokens) expressed as percentage, with breakeven point in turns
Retention directives (verbatim-preserve list):
  - user instructions from last 3 turns
  - file paths and line numbers
  - error stack traces and exit codes
  - tool call history for last 5 turns (tool_name, input, output, exit_code)