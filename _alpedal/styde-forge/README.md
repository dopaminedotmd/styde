# Styde Forge v3.0 — The Crucible

AI agent factory: spawn, evaluate, improve, and promote blueprint-defined agents from concept to production. Uses Hermes `delegate_task` as the execution backend with a Caveman Ultra plain-text protocol, dual self/judge evaluation, teacher-driven improvement loop, and tiered subagent orchestration.

## Badges

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Status](https://img.shields.io/badge/status-production-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Blueprint Count](https://img.shields.io/badge/blueprints-210%2B-orange)

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
  - [CLI Commands](#cli-commands)
  - [Pipeline: run_all_blueprints.py](#pipelinerun_all_blueprintspy)
  - [Dashboards](#dashboards)
- [Blueprint System](#blueprint-system)
- [Agent Lifecycle](#agent-lifecycle)
- [Scoring & Quality Gates](#scoring--quality-gates)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

Styde Forge is an automated agent training and deployment system. It treats AI agent specifications as "blueprints" — composable, versioned, and iterable. The forge pipeline (spawn → eval → improve → checkpoint) runs in loops, using a Teacher agent to analyse evaluation results and propose concrete blueprint improvements.

Key features:
- 210+ blueprint-defined agents across 10 tiered subagent groups
- Dual evaluation: self-evaluation (agent rates own output) + judge evaluation (fresh context, no bias)
- Teacher agent diagnoses weak dimensions and proposes targeted improvements
- Caveman Ultra mode strips all markdown from prompts and output for maximum token efficiency
- Circuit breakers prevent runaway API costs
- Atomic state persistence with YAML checkpointing
- Two live dashboards: Command Center (port 8766) and Mission Control (port 8765)

## Prerequisites

- Python 3.11+
- Hermes Agent runtime (provides `delegate_task`)
- DeepSeek v4 Flash or compatible model
- At least 16 GB RAM; 8 GB VRAM recommended
- Required Python packages: `pyyaml`, `json` (stdlib), `pathlib` (stdlib)

## Installation

```bash
# Clone or navigate to the forge root
cd D:/styde/_alpedal/styde-forge

# No external pip dependencies beyond what Hermes provides.
# The forge uses stdlib modules only: pathlib, json, yaml, subprocess, hashlib, time, datetime.
# Verify:
python --version  # Need 3.11+
python -c "import yaml; print('pyyaml OK')"

# Initialize the forge state and directory structure
python Core/forge.py init
```

## Quick Start

```bash
# View forge status
python Core/forge.py status

# Spawn one agent manually
python Core/forge.py spawn documentation-generator

# Spawn with a task override
python Core/forge.py spawn code-reviewer --task "Review D:/path/to/file.py"

# Run eval on last spawned agent
python Core/forge.py eval code-reviewer

# Improve blueprint based on eval results
python Core/forge.py improve code-reviewer

# Full loop: spawn → eval → improve (repeats until production-ready)
python Core/forge.py loop code-reviewer

# Run ALL blueprints to production (batches of 3, parallel subagents)
python run_all_blueprints.py
```

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Styde Forge v3.0                         │
│                                                              │
│  ┌──────────┐   ┌────────────┐   ┌───────────────────────┐  │
│  │ Hermes    │   │ CLI        │   │ Dashboards             │  │
│  │ Bridge    │◄──│ forge.py   │──►│ Port 8765 / 8766       │  │
│  │           │   │            │   │ Command Center         │  │
│  └─────┬─────┘   └─────┬──────┘   └───────────────────────┘  │
│        │               │                                      │
│  ┌─────▼───────────────▼────────────────────────────────┐     │
│  │                    Core Pipeline                       │     │
│  │  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌────────┐  │     │
│  │  │ Spawn   │─►│ Evaluate │─►│ Teacher │─►│Improve │  │     │
│  │  │(Hermes) │  │Self/Judge│  │Analyse  │  │Blueprint│  │     │
│  │  └─────────┘  └──────────┘  └─────────┘  └────────┘  │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              Storage Layer                            │     │
│  │  state.yaml │ blueprints/ │ refinery/ │ production/  │     │
│  │  archive/   │ 99_INDEXES/ │ logs/     │ scripts/     │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐     │
│  │              Safety Systems                           │     │
│  │  Circuit Breakers │ Checkpoints │ Recovery │ Lock    │     │
│  └──────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

Data flow through the pipeline:

1. User runs `spawn <blueprint>` → forge loads persona.md + BLUEPRINT.md + config.yaml → builds delegate_task payload → Hermes executes agent → output written to refinery/<bp>/runs/<run-id>/output.md

2. User runs `eval <blueprint>` → forge reads agent output → sends SELF_EVAL prompt to same agent → sends JUDGE_EVAL prompt to new Hermes task (no blueprint context) → computes composite = self * 0.4 + judge * 0.6 → saves eval.yaml

3. User runs `improve <blueprint>` → Teacher agent analyses eval results → identifies weakest dimension → proposes concrete change to persona.md, BLUEPRINT.md, or config.yaml → auto-version bump → writes FEEDBACK.md

4. Loop repeats until composite >= 85 (production-ready threshold)

## Usage

### CLI Commands

All commands are run via `python Core/forge.py <command> [args]`.

| Command | Arguments | Description |
|---------|-----------|-------------|
| `init` | — | Create directory structure and initialise state |
| `status` | — | Display forge health, agent counts, latest checkpoint |
| `spawn` | `<blueprint>` [`--benchmark`] [`--task`] | Spawn agent via Hermes delegate_task |
| `eval` | `<blueprint>` | Run self-eval + judge-eval on latest agent output |
| `improve` | `<blueprint>` | Teacher analyses evals and applies blueprint improvements |
| `checkpoint` | `<name>` | Create a named checkpoint of current state |
| `recover` | — | Recover from last checkpoint |
| `loop` | `<blueprint>` [`--max N`] | Full spawn → eval → improve cycle, repeats until composite >= 85 or max iterations |

### Pipeline: run_all_blueprints.py

Orchestrates all 210+ blueprints through the forge loop in parallel subagent batches:

```bash
python run_all_blueprints.py
```

Default: batches of 3, max 10 iterations per blueprint. Uses 10 subagent tiers matching the tier groups defined in CommandCenter/server.py (General, Fas 0.5, Fas 1-6).

### Dashboards

Two live HTTP dashboards for monitoring forge progress:

**Command Center (port 8766)**
```bash
python CommandCenter/server.py
# → http://localhost:8766
```
Minimalist sidebar + grid view. Shows all agents with XP bars, tier panels, subagent status, and live 3-second polling from state.yaml.

**Mission Control (port 8765)**
```bash
python Dashboard/web/server_8765.py
# → http://localhost:8765
```
Production-grade dashboard with CSP, CSRF, CORS security headers. Shows blueprint scores, skill details, activity feed, hardware telemetry. Includes forge control buttons (spawn, eval, improve), gzip compression, and health endpoint.

## Blueprint System

Each blueprint is a directory under `StydeAgents/blueprints/<name>/` containing three required files:

**persona.md** — Agent personality, tone, role description, behaviour rules. Written in English (caveman-compatible plain text).

**BLUEPRINT.md** — Purpose, domain, version, skills list. Describes what the agent does and what it knows.

**config.yaml** — Metadata, model override, toolset configuration, cost estimates, target score thresholds.

```
StydeAgents/blueprints/<blueprint-name>/
├── BLUEPRINT.md          # Required: agent purpose + skills
├── persona.md            # Required: agent personality + behaviour
├── config.yaml           # Required: metadata + thresholds
└── skills/               # Optional: reusable skill definitions
    └── <skill-name>.md
```

Blueprint validation enforces all three files exist and config.yaml contains valid YAML with `name` and `domain` fields.

## Agent Lifecycle

```
BLUEPRINT.md + config.yaml + persona.md
            │
            ▼
┌─────────────────────┐
│  REFINERY           │  Active training ground
│  (spawn → eval →   │  Agents here are being iterated
│   improve → loop)   │  Output in refinery/<bp>/runs/
└─────────┬───────────┘
          │ composite >= 85
          ▼
┌─────────────────────┐
│  PRODUCTION         │  Deployed, ready to use
│  (ready for tasks)  │  Output in production/<bp>/
└─────────────────────┘
          │
          ▼
┌─────────────────────┐
│  ARCHIVE            │  Retired or superseded
│  (historical only)  │
└─────────────────────┘
```

Promotion from refinery to production occurs automatically when the composite score reaches the tier target threshold (default: 85 for most tiers, 95 for General and Fas 0.5 design agents).

## Scoring & Quality Gates

Each evaluation produces scores on five dimensions, each 0-100:

| Dimension | Description |
|-----------|-------------|
| accuracy   | Correctness of the output |
| clarity    | Readability and structure |
| completeness | Coverage of all requirements |
| efficiency | Token economy, conciseness |
| usefulness | Practical value of the output |

Composite score = self_score * 0.4 + judge_score * 0.6

Quality thresholds:
- **Quality gate passed**: composite >= 80
- **Production-ready**: composite >= 85
- **Tier targets**: General/Fas 0.5 = 95, other tiers = 85

## Project Structure

```
D:/styde/_alpedal/styde-forge/
├── Core/                        # Pipeline engine
│   ├── forge.py                 # Main CLI (init, status, spawn, eval, improve, loop)
│   ├── spawn.py                 # Build delegate_task payload from blueprint
│   ├── evaluate.py              # Self-eval + judge-eval + composite scoring
│   ├── teacher.py               # Teacher agent: analyse + propose improvements
│   ├── blueprint.py             # Blueprint loading, validation, caching
│   ├── caveman.py               # Caveman Ultra mode toggle/injection
│   ├── state.py                 # State.yaml read/write
│   ├── persistence.py           # Atomic file writes
│   ├── hermes_bridge.py         # Hermes delegate_task wrapper
│   ├── circuit_breaker.py       # Rate limiting, failure backoff
│   ├── auto_version.py          # Semantic version bumping
│   ├── recovery.py              # Crash recovery + lock system
│   ├── checkpoint.py            # Named checkpoint create/list
│   ├── staleness.py             # Staleness detection
│   ├── quality_gates.py         # Quality threshold definitions
│   ├── smart_cache.py           # LRU cache for blueprint context
│   ├── detect.py                # Hardware detection
│   ├── filestore.py             # File storage abstraction
│   ├── agent_runner.py          # Agent execution wrapper
│   ├── markdown_stripper.py     # Markdown removal for caveman mode
│   ├── dashboard.py             # Dashboard data aggregation
│   ├── skill_pipeline.py        # Skill pipeline processing
│   └── tests/                   # Test suite
│       ├── test_forge.py
│       ├── test_spawn.py
│       ├── test_blueprint.py
│       ├── test_state.py
│       ├── test_persistence.py
│       ├── test_skill_pipeline.py
│       └── test_detect.py
├── CommandCenter/               # Port 8766 dashboard
│   └── server.py                # HTTP server: / and /api/state
├── Dashboard/web/               # Port 8765 dashboard
│   ├── server_8765.py           # Production-grade HTTP server
│   └── mission_control_8765.html
├── StydeAgents/                 # Agent storage
│   ├── blueprints/              # 210+ blueprint directories (<name>/BLUEPRINT.md, persona.md, config.yaml)
│   │   └── <name>/
│   │       ├── BLUEPRINT.md
│   │       ├── persona.md
│   │       ├── config.yaml
│   │       └── skills/          # Optional skill definitions
│   ├── refinery/                # Running evaluations per blueprint
│   ├── production/              # Production-ready agents
│   ├── archive/                 # Retired agents
│   └── data/                    # Benchmarks, knowledge, templates
├── scripts/                     # Automation scripts
│   ├── forge_pipeline.py        # Full pipeline orchestration
│   ├── parallel_spawn.py        # Parallel batch spawn
│   ├── parallel_eval.py         # Parallel batch eval
│   ├── parallel_improve.py      # Parallel batch improve
│   ├── promote_production.py    # Promote qualifying agents
│   ├── rerun_failed.py          # Retry failed tasks
│   ├── rebuild_state.py         # Reconstruct state.yaml from disk
│   ├── quality_filter.py        # Filter by quality thresholds
│   ├── find_failed.py           # Find failed operations
│   └── cleanup_cap.py           # Storage cleanup
├── Planing/                     # Design documents (Phases 1-2)
│   ├── v1.0_Phase1/
│   └── v2.0_Phase2/
├── eval/                        # Evaluation benchmarks
│   └── benchmarks/
├── run_all_blueprints.py        # Main runner: sequential batch processing
├── state.yaml                   # Persistent forge state (YAML)
├── .forge.lock                  # Lock file for crash recovery
├── 00_MANIFEST.json             # Forge manifest with SHA-256 integrity
├── 99_INDEXES/                  # Cache indexes (hardware profile, cache DB)
└── logs/                        # Runtime logs
```

## Development

```bash
# Run tests
python -m pytest Core/tests/

# Run a specific test
python -m pytest Core/tests/test_blueprint.py -v

# Create a new blueprint
mkdir StydeAgents/blueprints/my-new-agent
# Create BLUEPRINT.md, persona.md, config.yaml (see existing for reference)

# Run single blueprint through full loop
python Core/forge.py loop my-new-agent --max 5

# View state
python Core/forge.py status

# Start command center
python CommandCenter/server.py

# Start mission control dashboard
python Dashboard/web/server_8765.py
```

### Caveman Ultra Mode

Enabled by default. Strips all markdown (`#`, `**`, `` ` ``, `-`, `>`, `---`) from all prompts and agent output. Agents receive explicit rules: "NO markdown. EVER." This reduces token consumption by approximately 30-40% and enforces pure plain-text YAML output.

Toggle: `python Core/forge.py caveman-toggle`

### Adding a New Blueprint

1. Create directory: `StydeAgents/blueprints/<name>/`
2. Write `BLUEPRINT.md` — purpose, domain, version (1-5 skills max)
3. Write `persona.md` — role description, expertise, behaviour rules
4. Write `config.yaml` — name, domain, version, model_override (optional), toolsets
5. Run: `python Core/forge.py loop <name>`
6. Once composite >= 85, agent is production-ready

### New Blueprint Template

**BLUEPRINT.md:**
```
name: my-agent
domain: coding
version: 1

Purpose
One paragraph describing the agent's job.

Persona
One paragraph describing the agent's expertise and behaviour.

Skills
- Skill one: short description
- Skill two: short description (max 5 skills)
```

**config.yaml:**
```yaml
name: my-agent
domain: coding
version: 1
model_override: ""
toolsets:
  - filesystem
  - code
```

**persona.md:**
```
Expert in specific domain. Follows all instructions precisely.
Output format: pure text, no markdown.
Keeps responses concise and actionable.
```

## Troubleshooting

### Common Issues

**Forge state.yaml becomes corrupted after crash**

Run recovery: `python Core/forge.py recover`. If recovery fails, run `python scripts/rebuild_state.py` to reconstruct state from disk contents.

**`hermes` executable not found**

Set the `HERMES_PATH` environment variable to the full path of the Hermes agent executable. The forge searches common install locations (`AppData/Local/hermes/`, `~/.local/bin/`) but will use `HERMES_PATH` if set.

**Dashboard fails to start (port already in use)**

Kill the existing process: `taskkill /PID <pid>` on Windows or `lsof -ti:8765 | xargs kill` on Linux. Then restart the server.

**Subagent spawn hangs forever**

Check the Hermes circuit breaker status with `python Core/forge.py status`. If the breaker is OPEN, wait 60 seconds for the cooldown to expire. Use `python scripts/find_failed.py` to locate stuck runs.

### Dependency Conflicts

The forge Core imports only stdlib modules plus pyyaml:

- `pathlib`, `json`, `yaml`, `subprocess`, `hashlib`
- `time`, `datetime`, `os`, `re`, `tempfile`, `typing`
- `contextlib`, `shutil`, `functools`, `threading`

No external packages beyond pyyaml are required. Hermes provides the model execution layer. If you encounter import errors, verify pyyaml is installed:

```bash
python -c "import yaml; print('pyyaml OK')"
```

### Known Gotchas

- **Windows path length limit**: Very deep blueprint paths (>260 chars) can fail on Windows. Keep blueprint names short (<20 chars) and avoid nested directories.
- **Caveman mode strips all markdown**: Agent output in caveman mode has no formatting. Use the dashboards (ports 8765/8766) for human-readable views.
- **State.yaml is not thread-safe**: The `.forge.lock` prevents concurrent forge processes. Do not run two forge instances on the same state.yaml simultaneously.
- **Spawn + eval in the same second**: Run IDs use second-level timestamps. Two spawns within the same second will collide. The pipeline waits 1 second between spawns.

## Contributing

1. Read existing blueprints to understand the format convention.
2. Blueprint files are written in English (not Swedish).
3. All documentation files use English. The `_RULES.md` Swedish-only rule is deprecated.
4. Commit messages can be in Swedish or English.
5. Before making risky edits, commit uncommitted work. Do not use `git checkout` on uncommitted changes.
6. When editing HTML files (mission_control dashboard), do not use `replace_all=true` operations — they can corrupt the file.
7. If modifying the forge pipeline, run `python Core/forge.py init` after state.yaml changes.
8. For new features, add corresponding test files under `Core/tests/`.

## License

This project is licensed under the MIT License. See the `LICENSE` file in the repository root for full terms.

Copyright 2026 Styde Labs. All rights reserved.
