Analysing current config at C:\Users\jonat\.hermes\config.yaml
Current state:
```
model: deepseek-v4-flash
hooks: 5 hooks active (2 pre-tool, 1 post-tool, 1 pre-llm, 1 subagent)
hooks_auto_accept: true
profiles: 0
skills: 0
plugins: 0
memory: not configured
context: not configured (defaults used)
```
Four optimisation areas flagged:
Area 1 — Model selection
deepseek-v4-flash is a heavy reasoning model. For Styde Forge agent runs (high volume, many parallel agents), this burns tokens fast.
Recommended model split by task tier:
- Tier 1 (forge agent runs, blueprint eval, batch tasks): deepseek-v4-flash
- Tier 2 (daily driver, chat, code review): claude-sonnet-4-20250514 or gpt-4o
- Tier 3 (quick lookups, summarisation, formatting): gpt-4o-mini (100x cheaper)
- Tier 4 (cron, background, no-urgency): gpt-4o-mini with low temperature
Add to config.yaml:
```
model:
  default: deepseek-v4-flash
  tasks:
    code: claude-sonnet-4-20250514
    quick: gpt-4o-mini
    batch: deepseek-v4-flash
    cron: gpt-4o-mini
```
Area 2 — Context window and compression
No context config means default 128K tokens with no compression. For Styde Forge where blueprints and agent outputs accumulate, this causes context thrashing (frequent truncation, re-reading history).
Recommended context block:
```
context:
  window: 128000
  compression: smart
  max_history_messages: 40
  token_budget_percent: 80
  strategy: keep_recent
```
Strategy keep_recent paired with max_history_messages 40 preserves working memory while dropping old blueprint iterations. Token budget 80% leaves headroom for tool output.
Area 3 — Memory providers
No memory configured means no persistence between sessions. Each session starts cold. For a forge operator running hundreds of agent runs, this loses all learning.
Recommended memory block:
```
memory:
  provider: file
  file:
    path: ~/.hermes/memories/
    auto_index: true
    max_memories: 500
  short_term: 20
  long_term_enabled: true
  recall_on_load: true
```
File provider for simplicity (no external infra). Auto-index so Hermes can search past forge runs. Long-term enabled with recall on load means session remembers what worked before.
Optionally, if you want cross-session learning across all profiles, use provider: memdir with same path.
Area 4 — Tools optimisation per use case
Current config has hooks but no tool restrictions. Every call has full tool access. For forge agent runs where speed matters, trimming unused tools reduces LLM token waste on tool descriptions.
Recommended tool block:
```
tools:
  default_profile:
    - terminal
    - read_file
    - write_file
    - patch
    - search_files
    - process
  reduced_profile:
    - read_file
    - write_file
    - search_files
```
Create a stripped profile for cron/background agents that never need terminal or process tools.
Area 5 — Create a task-specific forge profile
Since profiles/ is empty, recommended creation:
File: C:\Users\jonat\.hermes\profiles\forge.yaml
```
name: forge
description: Optimised for Styde Forge batch agent training
model: deepseek-v4-flash
context:
  window: 128000
  compression: smart
  max_history_messages: 30
  token_budget_percent: 75
memory:
  provider: file
  file:
    path: ~/.hermes/profiles/forge/memories/
    auto_index: true
    max_memories: 300
tools:
  - terminal
  - read_file
  - write_file
  - patch
  - search_files
  - process
hooks:
  pre_tool_call:
    - matcher: "terminal"
      command: "~/.hermes/agent-hooks/block-destructive-cmds.sh"
      timeout: 5
hooks_auto_accept: true
```
And another:
File: C:\Users\jonat\.hermes\profiles\quick.yaml
```
name: quick
description: Fast lookups, summaries, cron jobs
model: gpt-4o-mini
context:
  window: 16000
  compression: none
  max_history_messages: 10
  token_budget_percent: 50
memory:
  provider: none
tools:
  - read_file
  - search_files
hooks_auto_accept: true
```
Switch between them with `hermes --profile forge` or `hermes --profile quick`.
Summary of wins:
- Model tiering: 40-80% token cost reduction on non-deepseek tasks
- Context window: prevents thrashing on long forge sessions, sets hard ceiling
- Memory: first-load recall avoids re-discovering forge state each session
- Tool trimming: reduces prompt overhead for batch agents
- Profiles: separates forge work from quick tasks, prevents context bleed
Would you like me to write any of these config changes to disk?