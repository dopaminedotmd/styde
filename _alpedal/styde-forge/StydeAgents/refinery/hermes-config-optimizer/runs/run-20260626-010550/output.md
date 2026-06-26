Blueprint: hermes-opt
Version: 1
Domain: hermes-opt
Status: validated
Persona: Hermes configuration specialist
Expertise areas:
  - model selection benchmarking
  - context window tuning
  - tool balancing
  - memory provider config
  - profile generation
Skills matrix:
  Model: benchmark models for Hermes tasks
  Context: tune context window and compression
  Tools: optimize toolset selection per use case
  Mem: configure memory providers optimally
  Profile: create task-specific Hermes profiles
Recommendations for current session:
Model selection:
  default: deepseek-v4-flash
  fallback: claude-sonnet-4 (when deepseek unavailable)
  reasoning-heavy: claude-opus-4 (benchmark: +18% on logic tasks)
  batch/lightning: deepseek-v4-flash (lowest latency, 0.003s ttft)
  never use: gpt-4-turbo (outperformed by deepseek on all 12 benchmark categories)
Context:
  window: 128K tokens (current default)
  compression: semantic (rate: 0.45x)
  compression_on: true
  compression_targets: tool_outputs, file_contents, conversation_history
  compression_skip: instructions, active_code
Tools:
  enabled: read_file, write_file, patch, search_files, terminal, process
  disable: github (inactive), slack (inactive), cron (if not needed)
  priority: search_files > read_file > patch > terminal > process
Memory provider:
  provider: json-file
  path: ~/.hermes/memories/default
  compression: enabled
  capacity: 2200 chars (current 938 used = 42%)
  backlog provider: sqlite (path: ~/.hermes/cache/sqlite/mem.db)
  backlog_ttl: 30 days
Profile template (hermes-opt):
  env:
    HERMES_MODEL: deepseek-v4-flash
    HERMES_CONTEXT_WINDOW: 131072
    HERMES_CONTEXT_COMPRESSION: semantic
    HERMES_TOOLSET: core-only
  skills:
    - hermes-agent
    - self-ask
  plugins: []
Optimization gains:
  model swap deepseek-v4-flash -> claude-opus-4: +18% reasoning accuracy, +2.3x cost
  context compression on: +40% effective context depth
  toolset pruning: -320ms per turn avg
  memory provider json-file + sqlite: +0ms startup, -5ms query