HERMES CONFIG OPTIMIZER REPORT
--- MODEL OPTIMIZATION ---
Default model deepseek-v4-flash (1M ctx) is correct for your use case. Good speed/cost ratio. Forge workers both use v4-pro which is wasteful for batch agents. Switch forge workers to v4-flash.
CRITICAL: No fallback providers defined. If deepseek API is down, Hermes stops. Configure at least one fallback.
MOA preset uses gpt-5.5 + claude-opus-4.8 as reference models and aggregator. These are expensive and the benefit for coding work is marginal. Either remove MOA (not used in your current workflow) or switch to v4-flash + v4-pro combos.
All auxiliary provider blocks (vision, compression, curator, etc.) set to 'auto' meaning they piggyback on the main deepseek model. For auxiliary tasks this wastes the 1M context window. Set specific lightweight models for auxiliary services:
- vision: deepseek-v4-flash (keep, good multimodal)
- compression: no separate model needed if using in-context compressor
- curator, monitor, title_generation: use deepseek-v4-flash with shorter timeout
--- CONTEXT TUNING ---
Compression is on: threshold 0.5, target_ratio 0.2. This aggressively compresses to 20% of original. For coding conversations this may lose critical code context. Raise target_ratio to 0.4 (40% of original retained).
context_length_cache shows only 2 entries (v4-flash and v4-pro both at 1M). This is correct — no waste.
context engine is 'compressor'. This is the standard engine. No change needed.
--- TOOL BALANCE ---
Only hermes-cli toolset loaded. This is correct for CLI usage. Additional platform toolsets (telegram, discord, slack etc.) are correctly excluded from CLI profile.
tool_output max_bytes 50000, max_lines 2000, max_line_length 2000. These are reasonable. For code-heavy sessions, max_bytes could be bumped to 100000 to avoid truncating long file outputs.
tool_loop_guardrails: warnings enabled, hard_stop disabled. 2 failures before warning, 5 before hard stop. This is balanced — warnings help without blocking work.
--- MEMORY OPTIMIZATION ---
Current limits: memory_char_limit 2200, user_char_limit 1375. These are extremely tight. Your memory has 581 chars used (26% of 2200), user profile has 411/1375 (29%). But for your style (Swedish, complex task histories), these will hit limits fast during long sessions.
Recommended: memory_char_limit 4000, user_char_limit 3000.
Provider is empty string (local file). This works. No remote memory provider configured. For forge workers, add a dedicated memory provider per profile.
write_approval: false. Good for autonomous operation.
--- PROFILE ARCHITECTURE ---
3 profiles: default, forge-worker-1, forge-worker-2. Forge workers lack profile.yaml files — they use monolithic config.yaml. Each forge worker profile is a full copy of default with model changed to v4-pro. This is bloated and fragile.
Better approach: Create minimal per-worker configs that inherit from default. Each forge worker config only needs:
- model override: deepseek-v4-flash (not pro)
- reduced max_concurrent_children: 5 (avoids resource contention)
- shorter timeout: 600s (worker tasks should be fast)
- memory provider: local (isolated per worker)
- disabled_toolsets: all except hermes-cli
--- SESSION & STORAGE OPTIMIZATION ---
state.db is 189MB. session auto_prune is false. Enable auto_prune with retention 30 days to prevent unbounded growth.
compression.threshold 0.5 means 50% of messages must be compressible before compression triggers. This is fine. hygiene_hard_message_limit 5000 is generous — won't hit it.
protect_last_n 20 protects recent context, protect_first_n 3 protects system prompt start. Good defaults.
--- CONFIG SIZE REDUCTION ---
Current config: 705 lines, 17KB. Many blocks are unused:
- 19 personality definitions (you use 0 — personality: '' )
- 6 TTS provider blocks (only openai used)
- 5 STT provider blocks (only openai used)
- Discord/Telegram/Slack/Mattermost/Matrix/WhatsApp blocks all empty
- bedtime, computer_use, video_gen blocks not relevant on CLI
These can be stripped for maintainability but have no performance impact.
--- TOP 5 RECOMMENDATIONS (by impact) ---
1. Add fallback providers — single provider is a hard failure point. At minimum add openrouter/deepseek as fallback.
2. Forge workers: use deepseek-v4-flash instead of v4-pro. Workers don't need the heavier reasoning model. This cuts cost per spawn by ~60%.
3. Raise memory_char_limit to 4000 and user_char_limit to 3000. Your current caps are 1375-2200 chars which is ~400-700 Swedish words — very constraining for complex sessions.
4. Enable session auto_prune with retention 30 days. 189MB state.db will keep growing without bound.
5. Raise compression target_ratio from 0.2 to 0.4. 80% compression drops code context. 60% keeps more logical continuity.
Want me to apply any of these?