# Styde Forge — Architecture Document

Version 3.0 (The Crucible)
Last updated: 2026-06-26

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HERMES AGENT RUNTIME                        │
│  delegate_task(goal, context, model, toolsets) → output             │
│  Hermes executes the agent in a sandboxed session                   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          FORGE PIPELINE                             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  CLI (forge.py)                                              │    │
│  │  init | status | spawn | eval | improve | checkpoint | loop  │    │
│  └───────┬───────────┬──────────┬──────────┬────────────────────┘    │
│          │           │          │          │                          │
│  ┌───────▼───┐ ┌─────▼────┐ ┌──▼─────┐ ┌─▼───────────┐             │
│  │ SPAWN     │ │ EVAL     │ │TEACHER │ │CHECKPOINT   │             │
│  │           │ │          │ │        │ │   RECOVERY  │             │
│  │ spawn.py  │ │evaluate.py│ │teacher │ │checkpoint.py│             │
│  │ agent_run │ │          │ │.py     │ │recovery.py  │             │
│  │ ner.py    │ │ quality_ │ │ auto_  │ │filestore.py │             │
│  │ hermes_   │ │ gates.py │ │version │ │persistence  │             │
│  │ bridge.py │ │          │ │.py     │ │.py          │             │
│  └─────┬─────┘ └────┬─────┘ └───┬────┘ └──────┬───────┘             │
│        │            │           │              │                      │
│  ┌─────▼────────────▼───────────▼──────────────▼───────┐             │
│  │                   STATE LAYER                        │             │
│  │  state.py (yaml read/write)                         │             │
│  │  persistence.py (atomic writes)                     │             │
│  │  staleness.py (drift detection)                     │             │
│  │  smart_cache.py (LRU caching)                       │             │
│  │  circuit_breaker.py (rate limits)                   │             │
│  └─────────────────────────────────────────────────────┘             │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  CROSS-CUTTING                                                 │ │
│  │  caveman.py (markdown stripping)                               │ │
│  │  markdown_stripper.py (plain text enforcement)                 │ │
│  │  detect.py (hardware profiling)                                │ │
│  │  blueprint.py (validation + loading)                           │ │
│  │  skill_pipeline.py (skill processing)                          │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        STORAGE LAYER                                │
│                                                                     │
│  state.yaml      ── Forge-wide persistent state                     │
│  .forge.lock     ── Crash recovery mutex                            │
│  00_MANIFEST.json ── Integrity manifest                             │
│                                                                     │
│  StydeAgents/                                                        │
│  ├── blueprints/     ── Source definitions (read-only at runtime)   │
│  │   └── <name>/                                                     │
│  │       ├── BLUEPRINT.md                                            │
│  │       ├── persona.md                                              │
│  │       ├── config.yaml                                             │
│  │       └── skills/                                                 │
│  ├── refinery/       ── Active training runs                         │
│  │   └── <name>/runs/<run-id>/output.md                              │
│  ├── production/     ── Deployed agents                              │
│  ├── archive/         ── Retired agents                              │
│  └── data/            ── Benchmarks, knowledge bases                 │
│                                                                     │
│  99_INDEXES/          ── Cache (hardware profile, cache.db)         │
│  logs/                ── Runtime logging                            │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DASHBOARDS                                     │
│                                                                     │
│  Command Center (port 8766)       Mission Control (port 8765)       │
│  ┌─────────────────────────┐     ┌─────────────────────────────┐    │
│  │ server.py               │     │ server_8765.py              │    │
│  │ Single-file HTML + API  │     │ CSP, CSRF, CORS, gzip      │    │
│  │ Sidebar + tier panels   │     │ Forge control buttons       │    │
│  │ 3-second polling         │     │ Activity feed + telemetry  │    │
│  │ Reads state.yaml direct  │     │ Skill detail + health      │    │
│  └─────────────────────────┘     └─────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow: spawn → eval → improve Loop

```
┌──────────────────────────────────────────────────────────────────┐
│                     LOOP ITERATION                                │
│                                                                  │
│  Start: blueprint exists in StydeAgents/blueprints/<name>/       │
│                                                                  │
│  ┌──────────┐                                                    │
│  │ 1. SPAWN │──── blueprint context ──► Hermes delegate_task     │
│  │          │◄──── agent output ──► refinery/<name>/runs/<id>/   │
│  └────┬─────┘                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────┐                                                    │
│  │ 2. EVAL  │──── output ──► self-eval prompt ──► same session   │
│  │          │──── output ──► judge-eval prompt ──► new session    │
│  │          │──── composite = self * 0.4 + judge * 0.6           │
│  │          │──── composite >= 85? ─► production                 │
│  └────┬─────┘                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────┐                                                    │
│  │3.TEACHER │──── eval results ──► diagnose weakest dimension    │
│  │          │──── propose change to persona.md / BLUEPRINT.md    │
│  │          │──── bump version in config.yaml                    │
│  └────┬─────┘                                                    │
│       │                                                          │
│       ▼                                                          │
│  ┌──────────┐                                                    │
│  │4.IMPROVE │──── apply changes to blueprint files                │
│  │          │──── write FEEDBACK.md                             │
│  │          │──── create checkpoint                              │
│  └────┬─────┘                                                    │
│       │                                                          │
│       └──→ LOOP (max N iterations or production-ready)           │
└──────────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. Caveman Ultra Protocol

Decision: All communication between forge and agents uses plain text. No markdown allowed.

Rationale:
- Reduces token consumption by 30-40% compared to markdown-wrapped prompts
- Eliminates parsing ambiguity — YAML blocks embedded directly in text are extracted by regex
- Forces agents to be concise (no decorative formatting)
- Compatible with all Hermes-supported models regardless of markdown rendering quality

Implementation: `Core/caveman.py` injects rules at spawn time. `Core/markdown_stripper.py` has a `strip_markdown()` function used during spawn context construction.

Trade-off: Agent output is less readable for humans. The dashboards render it anyway.

### 2. Dual Evaluation (Self + Judge)

Decision: Every eval runs two separate Hermes delegate_task calls — one self-evaluation (same agent context) and one judge-evaluation (fresh context, no blueprint personality).

Rationale:
- Self-eval catches agent's own awareness of its limitations
- Judge eval provides unbiased external scoring
- Weighted composite (0.4 self / 0.6 judge) balances introspection with objectivity
- Both use the same rubric dimensions for apples-to-apples comparison

Risk: Self-eval can be overconfident. Judge can miss domain-specific nuance. The weights can be tuned per-blueprint in Phase 2 (Bayesian optimization).

### 3. Subagent Parallelism

Decision: 46 agents grouped into 10 tiers (General, Fas 0.5, Fas 1-6), each tier handled by one subagent. Subagents run sequentially per tier, but tiers can run in parallel.

Rationale:
- Prevents API rate limits from single-thread floods
- Each subagent has its own circuit breaker
- Clear ownership: tier subagent #1 handles General agents, etc.
- Progress tracking per tier in Command Center dashboard

Implementation: Hardcoded TIERS dict in `CommandCenter/server.py` and `server_8765.py`. Each tier has a target score and a subagent status tracker.

### 4. YAML State Persistence

Decision: All forge state stored in `state.yaml` with atomic writes. No database.

Rationale:
- Human-readable and git-diffable
- No external dependencies (no SQLite, no PostgreSQL)
- Simple crash recovery: read → modify → atomic write
- Checkpoints are just copies of state.yaml with a name

Trade-off: Not suitable for concurrent writers. The `.forge.lock` mechanism prevents concurrent forge instances. At the scale of 210 blueprints and ~1000 evaluations, YAML I/O is not a bottleneck (state.yaml is ~350 KB).

### 5. Blueprint as Filesystem Directory

Decision: Each blueprint is a directory containing exactly three files: BLUEPRINT.md, persona.md, config.yaml. No database registry.

Rationale:
- Easy to add/remove/modify — just create or delete a directory
- Version control native: git tracks every change
- Skills are optional .md files in a skills/ subdirectory
- Validation is a filesystem check: `os.path.exists()`

### 6. No External Dependencies

Decision: The forge core (Core/*.py) imports only stdlib modules plus pyyaml.

Rationale:
- Zero-install on any Python 3.11+ environment
- Hermes provides the model execution layer — forge doesn't need to manage model servers
- Portability: the forge can run on any machine that has Python and Hermes

Exceptions: pyyaml is required for YAML parsing. It is a standard-adjacent dependency available in virtually every Python environment.

### 7. Quality Gates as Hard Thresholds

Decision: Fixed numerical thresholds for quality gate (80) and production-readiness (85/95).

Rationale:
- Clear, unambiguous promotion criteria
- Dashboard shows progress bars toward known targets
- Teacher agent has clear success/failure signal

Future: Phase 2 introduces Bayesian optimization to tune threshold weights per dimension per blueprint.

## Scoring Pipeline

```
Agent Output (markdown-free text)
        │
        ▼
┌────────────────┐
│ SELF-EVAL      │  Same model, same session
│ Score: 0-100   │  5 dimensions (accuracy, clarity,
│ Dimensions     │  completeness, efficiency, usefulness)
│ Notes          │  Returns YAML block
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ JUDGE-EVAL     │  Different session, no blueprint context
│ Score: 0-100   │  Same 5 dimensions
│ Dimensions     │  Returns YAML block
│ Notes          │
└───────┬────────┘
        │
        ▼
┌─────────────────────────────────┐
│ COMPOSITE                       │
│ composite = self * 0.4 + judge * 0.6
│                                 │
│ Quality gates:                  │
│   70  = passed                  │
│   80  = quality gate            │
│   85  = production-ready        │
│   95  = General/Fas 0.5 target  │
└─────────────────────────────────┘
```

## Version Strategy

Built on `Core/auto_version.py`:
- Config files track `version: <semver>` in config.yaml
- Teacher agent bumps version on each improvement cycle
- Patch bump for minor improvements, minor bump for significant rewrites
- No major bumps yet (v1 baseline for all blueprints)

## Circuit Breaker Pattern

Each blueprint has its own circuit breaker circuit. Global breaker tracks system-wide health.

States: CLOSED (normal) → OPEN (failure limit reached, cool down) → HALF_OPEN (test after cooldown) → CLOSED or OPEN

Configuration:
- Failure threshold: 5 consecutive failures
- Cooldown period: 60 seconds
- Half-open max tests: 1

## Security Architecture

Mission Control dashboard (port 8765):
- CSP headers (Content-Security-Policy)
- CORS locked to localhost origins
- CSRF tokens with HMAC signing (30-minute expiry)
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- Request body size limiting (64 KB)
- Blueprint name validation (regex, no path traversal)
- Run ID validation (regex, no path traversal)

Command Center (port 8766): No security headers (internal read-only dashboard).

## Hardware Detection

`Core/detect.py` runs at `forge init` time:
- Detects GPU type, VRAM, RAM, CPU cores
- Profiles: "pontus-main" (workstation) or "pontus-beast" (server)
- Auto-selects sampling method and quantization level
- Profile saved to `99_INDEXES/hardware_profile.json`
