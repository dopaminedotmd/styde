Jag har läst hela källkodsbasen. Här är dokumentationen.
Styde Forge v3.0 — The Crucible
---
PROJECT OVERVIEW
Styde Forge is a multi-agent orchestration framework. It spawns AI agents defined by blueprints, evaluates their output, automatically improves the blueprint based on eval results, and loops until production readiness. Runs entirely offline through the Hermes CLI bridge.
Version: 3.0.0
Codename: The Crucible
Domain: AI Agent lifecycle management
Language: Python 3.11+
Runtime: Local (Hermes CLI + LLM backend)
---
DIRECTORY STRUCTURE
StydeAgents/
  blueprints/          — Agent definitions: persona.md + BLUEPRINT.md + config.yaml
  blueprints-archive/  — Archived (promoted) blueprints
  refinery/            — Active agent runs in training
  production/          — Production-ready agents
  archive/             — Failed agent runs
  data/                — benchmarks, knowledge, templates
Core/
  forge.py             — Main CLI entry point, all commands
  blueprint.py         — Blueprint loading, validation, caching
  spawn.py             — Subagent spawning via Hermes delegate_task
  evaluate.py          — Self-eval + judge-eval pipeline, composite scoring
  teacher.py           — Teacher agent analysis, improvement proposals
  hermes_bridge.py     — Hermes CLI bridge, persistent process pool, retries
  state.py             — State management, atomic saves, batch writes, activity log
  persistence.py        — Atomic filesystem operations (temp + rename)
  checkpoint.py         — Atomic checkpoints with content hash verification
  recovery.py           — Crash detection + checkpoint restore
  circuit_breaker.py    — Per-blueprint + global failure protection
  caveman.py            — Caveman Ultra mode (token-optimized output)
  markdown_stripper.py  — Markdown to plain text conversion
  smart_cache.py        — SQLite response cache (24h TTL, version invalidation)
  agent_runner.py       — Full agent lifecycle orchestration class
  skill_pipeline.py     — Multi-step skill pipeline engine
  dashboard.py          — Dashboard server (port 8765), SSE, engine control
  detect.py             — Hardware auto-detection (VRAM, RAM, CPU)
  auto_version.py       — Semantic versioning for blueprints
  filestore.py          — S3-compatible file storage, chunked uploads, image pipeline
  quality_gates.py      — Validation + security scanning for agents
  staleness.py          — Review tracking, dependency health, schema drift
  auto_version.py       — Blueprint version bumping by eval score
  __init__.py           — Package marker
  tests/                — Unit tests
CommandCenter/
  server.py             — Command Center (port 8766), live control panel
Dashboard/
  web/                  — Dashboard static files (package.json, tsconfig.json)
scripts/
  forge_pipeline.py     — Full pipeline orchestrator (9 stages)
  parallel_eval.py      — Parallel evaluation of multiple blueprints
  parallel_improve.py   — Parallel teacher analysis
  parallel_spawn.py     — Parallel agent spawning
  promote_production.py — Automatic production promotion
  quality_filter.py     — Detect poor outputs
  rebuild_state.py      — Sync state.yaml from filesystem
  cleanup_cap.py        — Archive old runs, cap at 5 per blueprint
  rerun_failed.py       — Re-spawn failed/archived agents
  find_failed.py        -- Find failed runs in state
  promote_production.py — Move qualified blueprints to production
eval/
  benchmarks/           — Evaluation benchmarks with golden cases + rubrics
logs/
  recovery.log          — Crash recovery log
checkpoints/            — Atomic checkpoints (full state snapshots)
99_INDEXES/
  cache.db              — SQLite response cache
  hardware_profile.json — Auto-detected hardware profile
storage/                — Local filesystem storage (S3-compatible fallback)
state.yaml              — Forge state (evergreen)
00_MANIFEST.json        — Project manifest
.forge.lock             — Process lock file
---
PREREQUISITES
- Python 3.11+
- Hermes CLI (hermes-agent) installed and on PATH or HERMES_PATH
- LLM provider (DeepSeek default): deepseek-v4-flash for spawning, deepseek-v4-pro for eval
- pip packages: PyYAML, psutil (optional, for hardware detection + health monitoring)
- nvidia-smi (optional, for GPU monitoring)
- Git (optional, for staleness checks)
---
INSTALLATION
git clone <repo> D:\styde\_alpedal\styde-forge
cd D:\styde\_alpedal\styde-forge
pip install pyyaml psutil
python Core/forge.py init
Init creates directory structure and detects hardware. Initial output:
=== Styde Forge v3.0 — Initializing ===
--- Hardware Detection ---
  Type: B
  VRAM: 8.0 GB
  RAM:  31.8 GB
  Sampling: VI
=== Forge initialized successfully ===
---
QUICK START
1. Check forge status:
python Core/forge.py status
Output example:
Styde Forge v3.0 — The Crucible
Hardware: pontus-main
Caveman Ultra: ON
Loop iterations: 0
Total agents spawned: 0
Total evaluations: 0
Active blueprints: 0
Agents in refinery: 0
Agents in production: 0
Agents archived: 0
2. Create a blueprint:
Blueprint = directory under StydeAgents/blueprints/<name>/ with three files:
  persona.md         — Agent role description and rules
  BLUEPRINT.md       — Purpose, skills, version
  config.yaml        — Blueprint name, domain, agent config, toolsets
Blueprint validation requirements:
  - persona.md >= 50 chars
  - BLUEPRINT.md contains "## Purpose" section
  - config.yaml has blueprint.name and blueprint.domain
3. Spawn an agent:
python Core/forge.py spawn documentation-generator
Runs blueprint through Hermes. Output saved to:
  StydeAgents/refinery/<name>/runs/run-<timestamp>/output.md
4. Evaluate output:
python Core/forge.py eval documentation-generator <run_id>
Runs self-eval + judge-eval, computes composite score (self*0.4 + judge*0.6).
5. Improve blueprint:
python Core/forge.py improve documentation-generator <run_id>
Teacher agent analyzes eval, diagnoses weakest dimension, proposes improvements, bumps version.
6. Run full loop (spawn -> eval -> improve, repeated):
python Core/forge.py loop documentation-generator
Repeats until 3 consecutive scores >= 85 (promotion to production) or max 10 iterations.
7. Parallel loop (multiple blueprints):
python Core/forge.py loop-parallel <name1> <name2> --max-workers 3
---
COMMAND REFERENCE
python Core/forge.py init                    — Initialize forge structure + hardware detect
python Core/forge.py status                  — Current state overview
python Core/forge.py spawn <name> [--benchmark <b>] [--task <t>]
python Core/forge.py eval <name> <run_id> [--benchmark <b>]
python Core/forge.py eval-results <name> <run_id>
python Core/forge.py improve <name> <run_id>
python Core/forge.py apply-improvements <name> <run_id>
python Core/forge.py checkpoint [label]
python Core/forge.py loop <name> [--benchmark <b>] [--max-iterations 10]
python Core/forge.py loop-parallel <names...> [--benchmark <b>] [--max-workers 3] [--max-iterations 5]
python Core/forge.py caveman [on|off]        — Toggle Caveman Ultra mode
Scripts:
python scripts/forge_pipeline.py              — Full 9-stage pipeline
python scripts/quality_filter.py [--list|--fix]
python scripts/parallel_eval.py [--top-n 10] [--max-workers 5]
python scripts/parallel_improve.py
python scripts/parallel_spawn.py
python scripts/rebuild_state.py
python scripts/cleanup_cap.py
Dashboard:
python Core/dashboard.py                      — Opens on http://localhost:8765
Command Center:
python CommandCenter/server.py                — Opens on http://localhost:8766
---
ARCHITECTURE
Component diagram:
+------------------------------------------------------------------+
|                     Styde Forge v3.0                             |
|                    (forge.py CLI)                                |
+------------------------------------------------------------------+
    |           |             |             |              |
    v           v             v             v              v
+-------+ +---------+ +-----------+ +----------+ +------------+
|spawn  | | eval    | | improve   | |checkpoint| | loop       |
+-------+ +---------+ +-----------+ +----------+ +------------+
    |           |             |              |            |
    v           v             v              v            v
+----------+ +----------+ +----------+ +----------+ +---------+
|blueprint | |evaluate  | |teacher   | |checkpoint| |agent    |
|.py       | |.py       | |.py       | |.py       | |runner   |
+----------+ +----------+ +----------+ +----------+ |.py      |
    |              |             |              |    +---------+
    v              v             v              v
+----------+ +----------+ +----------+ +----------+
|hermes    | |smart     | |state     | |persist-  |
|bridge    | |cache     | |.py       | |ence     |
|.py       | |.py       | |          | |.py      |
+----------+ +----------+ +----------+ +----------+
    |              |             |              |
    v              v             v              v
+----------+ +----------+ +----------+ +----------+
|Hermes    | |SQLite   | |state    | |filesystem|
|CLI       | |cache.db | |.yaml    | |          |
+----------+ +----------+ +----------+ +----------+
Cross-cutting:
  caveman.py         — Output format enforcement
  circuit_breaker.py — Failure protection
  recovery.py        — Crash detection + restore
  detect.py          — Hardware adaptation
  quality_gates.py   — Validation + security
Data flow (one loop iteration):
User input (blueprint name)
  |
  v
[1] blueprint.py validates + loads persona/BLUEPRINT.md/config.yaml/skills
  |
  v
[2] spawn.py builds agent context (caveman injection, benchmark loading)
  |
  v
[3] hermes_bridge.py calls hermes chat -q with the spawn goal
  |
  v
[4] Agent output -> post-process (caveman enforcement) -> output.md
  |
  v
[5] evaluate.py builds self-eval + judge-eval prompts
  |
  v
[6] hermes_bridge.py runs combined eval (2 YAML blocks in 1 call)
  |
  v
[7] compute_composite() = self*0.4 + judge*0.6
  |
  v
[8] teacher.py analyzes eval, diagnoses weakness, proposes changes
  |
  v
[9] auto_version.py bumps semantic version based on score delta
  |
  v
[10] checkpoint.py saves state atomic snapshot
  |
  v
[11] stage determination: score >= 85 x3 = production, >= 70 = refinery, < 70 = archive
  |
  v
Repeat from [1] with improved blueprint (FEEDBACK.md feeds next spawn)
---
KEY DESIGN DECISIONS
1. Atomic writes everywhere
   Every write uses temp-file + rename pattern (persistence.py). No partial writes
   possible even on USB yank or system crash. Checkpoints use staging-directory
   + atomic rename for multi-file consistency.
2. Caveman Ultra mode
   Agents are instructed to output plain text / YAML only. No markdown, no
   greetings, no sign-offs. This saves ~70% tokens, making runs 2x faster
   and 3x cheaper. Configurable in state.yaml (caveman_ultra: true|false).
3. Combined eval (one call vs two)
   Self-eval + judge-eval run in a single Hermes call (run_eval_combined),
   reducing eval overhead by ~50%. Two YAML blocks separated by ---.
4. Smart response caching
   SQLite cache (99_INDEXES/cache.db) with 24h TTL. Keys on content hash for
   eval/teacher calls — identical agent outputs get cache hits regardless of
   prompt framing. Cache invalidated when blueprint version bumps.
5. Circuit breakers
   Per-blueprint breaker (3 consecutive failures → open, 5min cooldown).
   Global breaker (5 failures in 10min window → open). Half-open state for
   automatic recovery testing. Prevents API cost runaway on broken blueprints.
6. Hardware auto-detection
   Two profiles: Type A (>= 28GB VRAM, NUTS sampling, 3 parallel subagents)
   and Type B (< 28GB VRAM, VI sampling, 1 parallel subagent). Adapts model
   selection, tree depth, Bayesian samples.
7. Blueprint versioning
   Semantic: MAJOR bump on >= 85 (quality gate), MINOR on >= 5 point
   improvement, PATCH otherwise. Version history tracked in config.yaml.
---
API — Hermes Bridge Endpoints
All agent execution goes through hermes_bridge.py:
spawn_agent(goal, context="", model="deepseek-v4-flash", toolsets=["terminal","file","web"], timeout=300)
  Returns: {success: bool, output: str, exit_code: int, stderr: str}
  Executes a full spawn goal through hermes chat -q
  Retries up to 3x on transient failures with exponential backoff
run_eval(prompt, model, timeout=60)
  Returns: {success: bool, output: str, exit_code: int, stderr: str}
  Runs eval with caveman eval rules, temperature=0.1, no tools
  Content-hash caching enabled
run_eval_combined(self_prompt, judge_prompt, model, timeout=120)
  Returns: {success, self_output, judge_output, exit_code, stderr}
  Both evals in one Hermes call, split by --- separator
run_teacher(prompt, model, timeout=90)
  Returns: {success, output, exit_code, stderr}
  Teacher analysis with caveman teacher rules (YAML structure enforced)
is_available() -> bool
  Checks hermes CLI is on PATH
---
CHANGELOG
3.0.0 — 2026-06-26 — The Crucible
  Major rewrite. New features:
  - Parallel loop support (loop-parallel command)
  - Combined eval (50% less API calls)
  - Smart response caching (SQLite, 24h TTL, version invalidation)
  - Circuit breaker system (per-blueprint + global)
  - Hardware auto-detection (Type A/B profiles)
  - Caveman Ultra mode default ON
  - Atomic checkpoint system (staging + rename)
  - Crash recovery (lock file + checkpoint restore)
  - Dashboard v5 with SSE, engine control panel
  - Skill Pipeline engine (multi-step workflows)
  - Quality gates and security scanning
  - Staleness detection (review tracking, dependency health, schema drift)
  - S3-compatible file storage with chunked uploads
  - Auto-versioning (semantic bumps based on eval scores)
  - AgentRunner class for programmatic lifecycle
  - Command Center server (port 8766) for live monitoring
  - 46+ blueprints across 10 tiers (General through Fas 6)
  - Batch writes for reduced I/O in loops
  - FEEDBACK.md system for cross-run context
2.0.0 — earlier
  Teacher agent, eval pipeline, stage transitions
1.0.0 — initial
  Basic spawn + checkpoint functionality
---
TESTING
Core tests in Core/tests/:
  test_blueprint.py   — Blueprint validation
  test_spawn.py       — Spawn prompt building
  test_forge.py       — Forge commands
  test_state.py       — State management
  test_persistence.py — Atomic writes
  test_detect.py      — Hardware detection
  test_skill_pipeline.py — Pipeline execution
Run tests:
  python -m pytest Core/tests/
---
DEVELOPMENT
Adding a new blueprint:
1. Create StydeAgents/blueprints/<name>/
2. Write persona.md (role + rules, >= 50 chars)
3. Write BLUEPRINT.md (must have ## Purpose section)
4. Write config.yaml (blueprint.name, blueprint.domain required)
5. Optional: add skills/ directory with .md skill files
6. Optional: add pipeline.yaml for multi-step workflows
7. Run: python Core/forge.py spawn <name>
8. Iterate through loop until production-ready
Adding a new benchmark:
1. Create eval/benchmarks/<name>/
2. Write task.md (task description)
3. Write rubric.md (evaluation criteria)
4. Optionally add golden/case-N/input.py (reference outputs)
Modifying core modules:
- Always use atomic_write/atomic_write_json for file writes
- Use batch_writes() context manager for multiple state updates
- Add circuit breaker support for new API-heavy commands
- Ensure caveman compatibility (no markdown in agent-facing content)
- Run existing tests before committing
---
CONTRIBUTING
1. Fork the repo and create a feature branch
2. Follow the existing module structure (Core/<module>.py)
3. Use atomic writes for all file operations
4. Add caveman mode support for any new agent-facing output
5. Update state.yaml schema if adding new state fields
6. Include unit tests in Core/tests/
7. Run existing tests to verify no regressions
8. Commit with descriptive messages (Swedish or English)
9. Submit a pull request
All documentation is in English (see _RULES.md translation notes 2026-06-25).
Documentation must be kept in sync with code on every significant change.