Now I have complete data. Here is the context compression analysis and optimization report.
---
COMPRESSION CONFIGURATION ANALYSIS
runtime compression (config.yaml lines 149-158):
  enabled: true
  threshold: 0.5
  target_ratio: 0.2
  protect_last_n: 20
  protect_first_n: 3
  hygiene_hard_message_limit: 5000
  abort_on_summary_failure: false
  codex_gpt55_autoraise: true
  in_place: true
context.engine: compressor (line 442)
auxiliary.compression (lines 204-210): provider/auto, model empty - falls through to main model
trajectory_compressor.py (CompressionConfig):
  target_max_tokens: 15250
  summary_target_tokens: 750
  protect_last_n_turns: 4
  summarization_model: google/gemini-3-flash-preview
  temperature: 0.3
  max_concurrent_requests: 50
context_length_cache.yaml:
  deepseek/deepseek-v4-flash: 1048576
  deepseek/deepseek-v4-pro: 1048576
ISSUES AND OPTIMIZATIONS BY DIMENSION
Threshold:
  issue: runtime threshold 0.5 triggers at 512K tokens on 1M context.
  risk: at 50% utilization, 512K tokens remain before hard cap.
    compression + summarization must complete within that window or context is
    lost. for agent trajectories with large tool outputs, 512K can be consumed
    in 5-10 turns.
  recommendation: lower to 0.35 (trigger at 360K tokens) to give more runway
    for multi-pass or incremental compression. for non-1M models (e.g. 32K
    context models), threshold should be 0.25.
  recommendation: add secondary threshold - if context_pct exceeds 0.75 in a
    single turn, trigger immediate compression regardless of threshold.
Summarize:
  issue: summarization prompt uses same temperature (0.3) for all content.
    factual tool outputs need lower temperature (0.1). creative reasoning
    benefits from higher (0.5). one-size-fits-all reduces quality.
  issue: summarization prompt instructs 4 bullet points but does not enforce
    structure or require key verbatim data. numbers, file paths, and command
    outputs are easily lost.
  issue: content truncation in _extract_turn_content_for_summary cuts at 3000
    chars. for large tool responses this discards more than it keeps.
  recommendation: split summarization prompt into two templates:
    - factual mode (for tool-response-heavy regions): temperature 0.1,
      instruct to preserve exact file paths, error messages, return codes,
      data values.
    - reasoning mode (for gpt-turn-heavy regions): temperature 0.4,
      instruct to preserve decision chain and conclusions.
  recommendation: add "preserve verbatim" section to prompt for outputs under
    500 chars. extend truncation window from 3000 to 10000 chars given 1M
    context budget.
  recommendation: set auxiliary.compression.model explicitly instead of auto.
    recommend google/gemini-3-flash-preview (same as trajectory compressor)
    or deepseek/deepseek-v4-flash for consistency.
Budget:
  issue: runtime target_ratio 0.2 means compress to 204K tokens. for 1M
    context this is very aggressive - losing 80% of context per compression
    event. a single compression destroys most conversation history.
  issue: trajectory_compressor target_max_tokens 15250 is incompatible with
    1M context trajectories. this value seems calibrated for 32K training
    contexts, not the current 1M runtime.
  issue: summary_target_tokens 750 is fixed. with 1M context, a summary can
    safely be 2000-4000 tokens without meaningful cost.
  recommendation: change runtime target_ratio to 0.5 (compress to 512K tokens
    instead of 204K) for 1M context models. this preserves recent conversation
    history better.
  recommendation: change trajectory_compressor target_max_tokens to 65536 for
    the 1M context model, or derive it dynamically from context_length_cache.
  recommendation: increase summary_target_tokens to 2000 for runtime
    compression and 1500 for trajectory compression.
Retain:
  issue: runtime protect_last_n 20 is adequate for 1M context but problematic
    for smaller models. it is hardcoded rather than proportional.
  issue: protect_first_n 3 protects first 3 turns unconditionally. if the
    first 3 turns are all system messages with long tool definitions, the
    protection wastes budget.
  issue: trajectory compressor protect_last_n_turns 4 is too low for training
    signal quality. the last 4 turns frequently contain the final answer and
    reward signal.
  issue: protection does not distinguish between high-value and low-value
    turns within the protected zone. all tool calls are treated equally.
  recommendation: change protect_last_n to a function of total turn count:
    max(protect_last_n, total_turns * 0.1) - proportional protection.
  recommendation: increase trajectory_compressor protect_last_n_turns to 8.
  recommendation: add content-aware protection for turns containing
    <result>, <answer>, <final>, or reward/score markers.
Measure:
  issue: runtime compression has no metrics logging. no feedback loop exists
    to evaluate compression quality or adjust thresholds.
  issue: trajectory compressor metrics are comprehensive but only collected
    post-hoc. no online monitoring of summarization quality.
  recommendation: add runtime metric tracking:
    - tokens_before, tokens_after per compression event
    - compression ratio distribution
    - summary generation success rate
    - number of times still_over_limit after compression
  recommendation: store metrics in state.db or a dedicated metrics file for
    dashboard/curator consumption.
  recommendation: trajectory compressor should log summary quality score
    (token count deviation from target, truncation events, fallback count).
CURRENT VALUES VS RECOMMENDED VALUES
setting                          current         recommended
threshold                        0.50            0.35
target_ratio                     0.20            0.50 (1M ctx)
protect_last_n                   20              20 (but proportional fallback)
protect_first_n                  3               3
traj.target_max_tokens           15250           65536
traj.summary_target_tokens       750             1500
traj.protect_last_n_turns        4               8
traj.summarization_model         gemini-3-flash   gemini-3-flash (keep)
traj.turn_truncation_chars       3000            10000
auxiliary.compression.model      auto            explicit (same as main or gemini)
summarization temperature        0.3 uniform     0.1 factual / 0.4 reasoning
BLOCKER: ablator/cache
corrupt cache.db (memory note at session start) kills all hermes_bridge calls
silently. runtime compression depends on hermes_bridge for the summarization
call. if cache is corrupt, compression fails silently and the agent loses
context summarization entirely. verify cache health before tuning compression.
delete 99_INDEXES/cache.db (if exists in styde-forge) or the main
state.db-wal/shm trio can be trimmed.