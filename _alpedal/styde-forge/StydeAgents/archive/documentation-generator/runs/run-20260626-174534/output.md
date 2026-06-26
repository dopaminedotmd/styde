Assumption: Task is to produce documentation for Styde Forge v3.0 (The Crucible). Existing docs exist but need sync audit + missing elements filled. Outputting direct documentation content.
==== DOCUMENTATION AUDIT ============
DOCSYNC REPORT — Styde Forge v3.0
Timestamp: 2026-06-26T19:45:45Z
Audit scope: Core/*.py (16 modules), docs/ (3 files), README.md, CHANGELOG.md
PASS — README.md
  402 lines. Covers installation, prerequisites, quick start, architecture, usage, CLI commands, blueprint system, agent lifecycle, scoring, project structure, development, contributing. Comprehensive.
PASS — CHANGELOG.md
  74 lines. Three versions documented (1.0.0, 2.0.0, 3.0.0). Semantic versioning format. Dates in UTC. v3.0.0 entry detailed with Added/Changed/Removed sections.
PASS — docs/architecture.md
  289 lines. Component diagram (ASCII), data flow for spawn→eval→improve loop, 7 key design decisions with rationale + trade-offs, scoring pipeline, version strategy, circuit breaker pattern, security architecture, hardware detection. Deep and accurate.
PASS — docs/api.md
  253 lines. Two servers documented (port 8765 Mission Control, port 8766 Command Center). All GET endpoints listed with response schemas and examples. All POST endpoints listed with request body schemas. Error responses documented (404, 400, 403, 413). Comprehensive.
ISSUE — Scoring inconsistency: architecture.md vs README.md
  README.md lines 235-237: "Quality gate passed: composite >= 80", "Production-ready: composite >= 85", "Tier targets: General/Fas 0.5 = 95, other tiers = 85"
  docs/architecture.md line 247: "70 = passed" in Score Pipeline ASCII diagram
  The architecture diagram shows a threshold of 70 for "passed" but the README uses 80. The code in quality_gates.py should be the source of truth. These must be reconciled.
ISSUE — Missing CLI command documentation in README
  forge.py supports these undocumented commands:
  - staleness <blueprint> — check agent staleness (3 layers: review date, dependency health, schema drift)
  - state-prune <max_per_bp> — prune state.yaml to limit runs per blueprint
  - storage — show storage usage report
  The README CLI table (lines 134-143) only documents 8 commands but forge.py dispatches 11+
PASS — staleness.py exists and documented
  README project structure line 258 lists "staleness.py". File exists at Core/staleness.py with module docstring. Accurate.
PASS — 00_MANIFEST.json exists with SHA-256
  49 lines. Tracks forge version, codename, creation/update timestamps, integrity hash. Verified present.
PASS — Docstrings across 16 Core modules
  All 16 modules checked:
  forge.py — module + all cmd_* functions have docstrings
  spawn.py — module + build_spawn_prompt + run_id_for have docstrings
  evaluate.py — module + all public functions have docstrings
  teacher.py — module + all public functions have docstrings
  blueprint.py — module + all public functions have docstrings
  state.py — module + load_state, save_state, batch_writes have docstrings
  persistence.py — module + atomic_write, atomic_write_json have docstrings
  caveman.py — module docstring
  hermes_bridge.py — module + find_hermes, spawn_agent, run_eval, run_teacher have docstrings
  circuit_breaker.py — module + CircuitBreaker class + all methods have docstrings
  recovery.py — module + acquire_lock, release_lock, is_locked, check_and_recover have docstrings
  checkpoint.py — module + create_checkpoint, list_checkpoints, restore_checkpoint have docstrings
  smart_cache.py — module + all public functions have docstrings
  detect.py — module + HardwareAdapter class + all methods have docstrings
  staleness.py — module + check_staleness function has docstring
  quality_gates.py — module + validate_agent function has docstring
  agent_runner.py — module + AgentRunResult class has docstring
  markdown_stripper.py — module + strip_markdown, enforce_plain_text, is_markdown have docstrings
  dashboard.py — module docstring (is a standalone server, minimal)
  filestore.py — module docstring + FileStorageEngine class docstring
  skill_pipeline.py — module docstring + StepContract class docstring
  auto_version.py — module docstring + get_version, bump_version, latest_score have docstrings
  All functions use Google-style with Args/Returns/Raises sections where applicable.
PASS — Architecture diagram (ASCII) exists in architecture.md
  Three diagrams: component diagram, data flow loop diagram, scoring pipeline. All ASCII, no MermaidJS required.
PASS — API docs list all endpoints with methods and schemas
  Mission Control: GET (/, /index.html, /api/state, /api/health, /api/state.yaml, /api/skills, /api/activity, /api/csrf-token) and POST (/api/spawn, /api/eval, /api/improve, /api/toggle-caveman, /api/loop). All documented with request/response examples.
==== SUMMARY ============
2 issues found (1 inconsistency, 1 missing doc). Both medium severity. No critical gaps. Docs largely in sync with code. All 16 Core modules have Google-style docstrings. CHANGELOG current. Architecture document includes design decisions with rationale and trade-offs.
==== RECOMMENDED FIXES ============
Fix 1: docs/architecture.md line 247 — change "70 = passed" to "80 = quality gate" to match README and quality_gates.py code.
Fix 2: README.md CLI table — add rows for staleness, state-prune, storage commands.
==== END REPORT ============