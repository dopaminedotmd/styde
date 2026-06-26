Full coverage analysis complete. Here is the report:
---
TEST COVERAGE REPORT — Styde Forge v3.0
Date: 2026-06-26
Command: pytest --cov=Core --cov-report=term-missing --ignore=Core/tests/test_spawn.py
Result: 9 failed, 86 passed, 1 skipped
Total coverage: 34% (3178 missed / 4804 statements)
MODULE COVERAGE BREAKDOWN
ABOVE 60% TARGET — 5 modules
  Core/__init__.py: 100%
  Core/tests/__init__.py: 100%
  Core/detect.py: 85%
  Core/skill_pipeline.py: 74%
  Core/blueprint.py: 73%
  Core/persistence.py: 71%
NEAR TARGET (40-59%) — 2 modules
  Core/caveman.py: 47%
  Core/state.py: 40%
WELL BELOW TARGET (10-39%) — 9 modules
  Core/circuit_breaker.py: 24%
  Core/filestore.py: 23%
  Core/evaluate.py: 21%
  Core/smart_cache.py: 19%
  Core/recovery.py: 17%
  Core/hermes_bridge.py: 16%
  Core/spawn.py: 15%
  Core/auto_version.py: 15%
  Core/checkpoint.py: 13%
  Core/teacher.py: 12%
  Core/forge.py: 10%
  Core/markdown_stripper.py: 9%
ZERO COVERAGE — 4 modules (CRITICAL)
  Core/agent_runner.py: 0% (121 stmts)
  Core/dashboard.py: 0% (290 stmts)
  Core/quality_gates.py: 0% (89 stmts)
  Core/staleness.py: 0% (98 stmts)
TEST FILE COVERAGE (the tests themselves)
  Core/tests/test_blueprint.py: 100%
  Core/tests/test_state.py: 100%
  Core/tests/test_forge.py: 98% (1 miss)
  Core/tests/test_detect.py: 97% (2 misses)
  Core/tests/test_persistence.py: 94% (10 misses)
  Core/tests/test_skill_pipeline.py: 88% (52 misses)
  Core/tests/test_spawn.py: 0% — entire file broken (import error)
FAILURES ANALYSIS — 9 tests failing
test_spawn.py — CRITICAL
  ImportError: 'extract_self_eval' does not exist in Core/spawn.py
  Function was documented in planning docs but never implemented in code
  All 158 lines of test_spawn.py are dead code
  Root cause: source module refactored without updating tests
test_blueprint.py::test_missing_directory — MINOR
  Assertion checks for 'not found' in error string
  Actual error: 'Missing required file: persona.md'
  Fix: change assertion to match real error message
test_forge.py::test_init_creates_directory_structure — MODERATE
  Expects 'blueprints' directory in FORGE_ROOT
  cmd_init() does not create blueprints dir (only creates it when FORGE_ROOT has a specific structure)
  Fix: update expected dirs or fix cmd_init
test_forge.py::test_status_after_init — MODERATE
  Expects 'Loop iterations: 0' in status output
  Real status output uses different format with actual production data
  Test runs against real state.yaml, not isolated tmp_path
test_skill_pipeline.py::test_simple_pipeline_ok — MODERATE
  PermissionError on D:\styde\_alpedal\styde-forge\output
  Pipeline tries to write to real output dir instead of tmp_path
  Needs monkeypatch or tmp_path isolation
test_skill_pipeline.py — 5 blueprint integration tests — MODERATE
  Expect blueprint directory 'skill-pipeline-architect' under blueprints/
  This blueprint does not exist in the repo
  Tests assume a blueprint that was never created or was removed
MISSING: conftest.py
  No shared fixtures exist
  Each test file reinvents tmp_path and monkeypatch patterns
  Missing fixtures: mock_forge_root, mock_state, mock_hermes_bridge
PRIORITY ACTIONS
1. Fix test_spawn.py import error — add extract_self_eval to spawn.py or remove
2. Fix test_skill_pipeline.py blueprint path test — create mock or skip integration tests that depend on nonexistent blueprints
3. Add zero-coverage tests for agent_runner.py, dashboard.py, quality_gates.py, staleness.py
4. Write conftest.py with shared fixtures
5. Bring caveman.py, state.py, forge.py, evaluate.py, hermes_bridge.py to 60%+
Coverage target 60%+ total requires covering approximately 1900 more statements across 15 modules. Fastest path: cover the 4 zero-coverage modules (598 stmts) + heavy-hitters forge.py (937 stmts at 10%) and dashboard.py (290 stmts at 0%). That alone moves total from 34% to ~62%.