# Changelog

All notable changes to Styde Forge are documented here.

Format: [Semantic Versioning 2.0.0](https://semver.org/)
Dates: UTC

---

## [3.0.0] — 2026-06-26

Second major rewrite. Codename: "The Crucible".

### Added
- Full spawn → eval → improve → loop pipeline
- Dual evaluation: self-eval (0.4 weight) + judge-eval (0.6 weight) with 5-dimension scoring
- Teacher agent that diagnoses weakest dimensions and proposes blueprint improvements
- Caveman Ultra mode: strips all markdown from prompts and output for token efficiency
- Circuit breaker per blueprint + global breaker (5 failure limit, 60s cooldown)
- Atomic YAML state persistence with crash recovery
- Checkpoint system with named snapshots
- Command Center dashboard (port 8766) with sidebar + tier panels + subagent status
- Mission Control dashboard (port 8765) with CSP, CSRF, CORS, gzip, health endpoint
- Hardware detection at init time (GPU/VRAM/RAM profiling)
- Blueprint validation with file existence and YAML integrity checks
- Parallel batch spawning/eval/improve scripts
- Quality gate thresholds: 80 pass, 85 production-ready, 95 top-tier
- 210+ blueprints across 10 tier groups (General, Fas 0.5, Fas 1-6)
- Smart caching with LRU for blueprint context loading
- Markdown stripper for caveman-compatible plain text enforcement
- Staleness detection for state drift
- Auto-version bumping on teacher improvement cycles
- Recovery system with forge lock file (`.forge.lock`)
- `run_all_blueprints.py` orchestrator — sequential batches of 3, max 10 iterations
- Full test suite in Core/tests/

### Changed
- Complete rewrite from v2.x spaghetti. Modular pipeline architecture.
- Blueprint format standardized: BLUEPRINT.md + persona.md + config.yaml
- All documentation and blueprint files are in English (transitioned from Swedish)
- State tracking moved from multiple JSON files to single state.yaml

### Removed
- Old styde.ai blueprint format (blueprint.yaml + tools.yaml + prompt_template.md) — kept as reference in StydeAgents/refinery/README.md
- Swedish-language content from all blueprint and documentation files
- Direct database dependencies — forge now uses filesystem + YAML only

---

## [2.0.0] — 2026-06-10

First major rewrite.

### Added
- Agent spawning via Hermes delegate_task
- Basic evaluation pipeline (single-pass, no judge)
- Simple state tracking in JSON format
- Blueprint directory structure

### Changed
- Migrated from styde.ai project structure to Styde Forge
- Ported existing blueprints from old format to new

---

## [1.0.0] — 2026-05-15

Initial release as styde.ai subproject.

### Added
- Basic blueprint definition format (blueprint.yaml, tools.yaml, prompt_template.md)
- Manual agent execution via shell scripts
- Swedish-language documentation and blueprints
- Stub dashboard with port mapping
