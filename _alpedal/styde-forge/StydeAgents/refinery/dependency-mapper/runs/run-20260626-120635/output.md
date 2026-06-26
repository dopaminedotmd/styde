Now producing the complete dependency analysis.
---
DEPENDENCY MAP — Styde Forge v3.0 "The Crucible"
project:
  version: 3.0.0
  codename: The Crucible
  created: 2026-06-25
  status: Phase 3 active (Phase 1 core loop built and running)
CRITICAL PATH — Phase 1 (Week 1-6, 22 P0 exit criteria)
  A: FOUNDATION (Days 1-7)
    1. persistence.py -> atomic_write, atomic_write_json, atomic_append
    2. detect.py -> nvidia-smi + psutil -> hardware_profile.json
    3. forge.py init -> USB directory structure + state.yaml
    4. Tauri scaffold + Layout + Dark theme (Dashboard shell)
    5. DeepSeek provider + basic chat (streaming)
    Dependency on: Python 3.11+, Node 20+, Rust+Cargo, Hermes v0.17+, WebView2
    Blocked by: environment verification (nvidia-smi, CUDA, API keys)
  B: SPAWN PIPELINE (Days 8-14)
    6. blueprint_loader.py -> load_blueprint_context()
    7. blueprint_valid.py -> validate_blueprint()
    8. spawn.py -> spawn_agent() wrapping delegate_task
    9. rag.py -> Embed + FAISS + inject (optional, deferred)
    Dependency on: A(1-3)
    Blocked by: persistence, hardware detection, directory structure
  C: EVAL PIPELINE (Days 15-21)
    10. eval_runner.py -> run_self_eval() + run_judge_eval()
    11. composite_scorer.py -> calculate_composite(score)
    12. forge.py eval CLI -> python forge.py eval <agent> <benchmark>
    Dependency on: B(6-8)
    Blocked by: spawn pipeline, blueprint validation
  D: IMPROVEMENT LOOP (Days 22-28)
    13. teacher.py -> analyze_eval(), propose_improvements()
    14. skill_extract.py -> extract_skill_from_success()
    15. forge.py improve CLI
    Dependency on: C(10-12)
    Blocked by: eval pipeline producing scores
  E: SAFETY & POLISH (Days 29-35)
    16. checkpoint.py -> create_checkpoint(), verify_integrity()
    17. recovery.py -> detect_crash(), restore_from_checkpoint()
    18. circuit_breaker.py -> CircuitBreaker class
    19. forge.py loop -> Full loop: DEFINE->SPAWN->EVAL->IMPROVE->CHECKPOINT
    Dependency on: D(13-15)
    Blocked by: teacher agent, evaluation results
  F: DASHBOARD (parallel track, Days 1-28)
    20. Tauri scaffold + Layout + Theme
    21. Provider registry + DeepSeek provider
    22. Chat panel (streaming, markdown)
    23. Chat tools (read_file, write_file, search_files)
    24. Hermes CLI bridge (Rust)
    25. Agent panel (poll agents, status cards)
    26. Start/Stop buttons, System tray, Config panel
    Dependency on: Hermes installed, config.json
    Connects to Forge at: Hermes CLI bridge
  G: INTEGRATION (Days 29-42)
    27. Forge <-> Dashboard bridge
    28. End-to-end test (code-reviewer loop from dashboard Start)
    29. Bug fixes + polish
    Dependency on: E(14-19), F(20-26)
    Blocked by: both Forge loop AND Dashboard working independently
CRITICAL PATH CHAIN:
  forge.py init -> blueprint_loader.py -> spawn.py -> eval_runner.py -> teacher.py -> checkpoint.py -> forge.py loop -> Dashboard Start/Stop
  "If spawn doesn't work, eval can't run. If eval can't run, teacher can't improve. If teacher can't improve, there's no loop."
CRITICAL PATH — Phase 2 (Week 1-12, 34 features)
  P0: EVAL DEPTH (Weeks 1-2)
    1. bias_calibrator.py -> calibrate_judge() -> bias_profile
    2. cross_judge.py -> CrossJudgePanel (primary+secondary+tertiary)
    3. bayesian_weights.py -> NUTS sampler, optimized_weights.yaml
    4. eval_runner.py upgrade -> use bayesian + cross-judge + bias cal
    Dependency on: Phase 1 complete (working loop, 50+ eval history)
    Blocked by: sufficient eval history for Bayesian convergence
  P1: LEARNING SYSTEMS (Weeks 3-4)
    5. historical_learning.py -> SQLite schema, pattern extraction
    6. auto_version.py -> MAJOR.MINOR.PATCH versioning
    7. model_selector.py -> cost/quality decision matrix
    8. self_monitor.py -> z-score anomaly detection, health endpoint
    Dependency on: P0(1-4)
    Blocked by: Bayesian weights producing stable results
  P2: RESOURCE MANAGEMENT (Weeks 5-6)
    9. resource_governor.py -> per-agent limits, soft/hard kill
    10. gpu_balancer.py -> dual-GPU (3080 + 3070 Ti) assignment
    11. task_queue.py -> priority levels, FIFO, batching
    Dependency on: P1(8), detect.py
    Blocked by: self_monitor and hardware profile
  P3: MULTI-AGENT (Weeks 7-8)
    12. phase_gates.py -> PLAN->CODE->REVIEW->TEST->DEPLOY gates
    13. agent_comms.py -> file-based message passing
    14. task_decomposer.py -> LLM-based sub-task decomposition
    15. specialized_roles.py -> 6 role definitions
    Dependency on: P0(1-4), P1(5-6)
    Blocked by: eval pipeline and historical learning
  P4: AUTOMATION + DASHBOARD (Weeks 9-12)
    16. smart_cache.py -> hash-keyed SQLite cache (no deps, quick win)
    17. batch_eval.py -> N-up eval grouping (no deps, quick win)
    18. auto_benchmarks.py -> LLM-generated benchmark variations
    19. prompt_optimizer.py -> A/B test prompt variations
    20. curriculum.py -> EASY/MEDIUM/HARD/EXPERT progression
    21. knowledge_graph.py -> SQLite adjacency, nodes and edges
  DASHBOARD P1/P2 (parallel, Weeks 5-12):
    22-27: OpenAI/Anthropic/Ollama providers
    28-31: Benchmark panel, Health monitoring, System tray, Spawn from UI
    32-34: Auto-update, Config polish, Error states
Phase 2 CRITICAL PATH CHAIN:
  bias_calibrator -> cross_judge -> bayesian_weights -> historical_learning -> teacher.py (upgraded) -> phase_gates -> agent_comms -> task_decomposer
  "Bayesian weights block historical learning. Historical learning blocks multi-agent."
BOTTLENECK ANALYSIS
  Bottleneck-1: Spawn pipeline (blueprint_loader -> spawn -> delegate_task)
    Why: Gatekeeper for ALL evaluation and improvement. No spawn = no eval = no loop.
    Current status: BUILT (spawn.py exists, agent_runner.py exists)
    Risk: delegate_task failure cascades to everything downstream
    Mitigation: retry with backoff, timeout=300s, circuit breaker per blueprint
  Bottleneck-2: Teacher agent
    Why: Only component that can improve blueprints. Without it, loop is a flat evaluate-and-store.
    Current status: BUILT (teacher.py exists, Core/teacher.py)
    Risk: If teacher produces non-actionable feedback, improvements stall
    Mitigation: tight prompt template, structured YAML output requirement
  Bottleneck-3: Bayesian weight convergence
    Why: Requires 30+ evals to converge. Blocks all Phase 2 features.
    Current status: NOT BUILT (Phase 2)
    Risk: may never converge on Machine-B (fewer workers, less data)
    Mitigation: VI fallback (faster, less precise), minimum 30 evals before first run
IMPLEMENTATION STATUS (actual code found)
  BUILT (Core/):
    forge.py, persistence.py, detect.py, spawn.py, evaluate.py, teacher.py
    checkpoint.py, recovery.py, circuit_breaker.py, blueprint.py, state.py
    agent_runner.py, caveman.py, smart_cache.py, auto_version.py
    quality_gates.py, skill_pipeline.py, hermes_bridge.py
    filestore.py, markdown_stripper.py, staleness.py, dashboard.py
    Tests: 7 test files
  NOT YET BUILT:
    rag.py (FAISS embedding injection)
    blueprint_valid.py (standalone validator)
    skill_extract.py
    Phase 2: bias_calibrator, cross_judge, bayesian_weights
    Phase 2: historical_learning, model_selector, self_monitor
    Phase 2: resource_governor, gpu_balancer, task_queue
    Phase 2: phase_gates, agent_comms, task_decomposer, specialized_roles
    Phase 2: auto_benchmarks, prompt_optimizer, curriculum, knowledge_graph
RISK ASSESSMENT (from Risk_Register.md + analysis)
  R10 CRITICAL HIGH: API provider changes (pricing, deprecation, outage)
    Probability: High  Impact: High
    Mitigation: Multi-provider support, local Ollama fallback, cost tracking
    Status: OpenAI/Anthropic/Ollama providers in Phase 2 Dashboard
  R03 CRITICAL HIGH: VRAM exhaustion on Machine-B (18GB total)
    Probability: High  Impact: Medium
    Mitigation: Hardware Adapter + Resource Governor
    Status: Phase 2 P2, not yet built
  R01/R06 MEDIUM HIGH: USB corruption / Lost state on machine move
    Probability: Medium  Impact: High
    Mitigation: Atomic Transactions + Checkpoints + Auto Recovery
    Status: BUILT (persistence.py, checkpoint.py, recovery.py)
  R05 MEDIUM HIGH: Eval bias over time
    Probability: Medium  Impact: High
    Mitigation: Bias Calibration + Cross-Consensus
    Status: Phase 2 P0, not yet built
  R02 MEDIUM HIGH: Divergent learning
    Probability: Medium  Impact: High
    Mitigation: 80/100 eval gate, >=85x3 production gate, Bayesian Opt
    Status: Phase 2 P0, quality_gates.py exists
  R10 HIGH HIGH: API provider changes
    Probability: High  Impact: High
    Mitigation: Multi-provider support, Ollama fallback
    Status: NOT BUILT (Phase 2 Dashboard)
SCHEDULE OPTIMIZATION
  Parallel tracks already identified:
    Week 1: Forge Foundation + Dashboard Shell
    Week 2: Forge Spawn + Dashboard Chat Core
    Week 3: Forge Eval + Dashboard Chat Tools
    Week 4: Forge Improve+Safety + Dashboard Monitor
    Week 5-6: Integration + Hardening
  Optimizations available:
    1. smart_cache.py and batch_eval.py have ZERO dependencies — build immediately for 30% token savings and 3-5x cheaper evals. Already built (smart_cache.py exists).
    2. auto_version.py also has no external deps — can be built anytime. Already built (auto_version.py exists).
    3. Dashboard providers (OpenAI, Anthropic, Ollama) have no dependencies on Forge — parallel build with Forge Phase 2 P0.
    4. Resource governor could be MVP from detect.py + config limits without needing full multi-agent system — pull forward to Phase 1.
TECHNICAL STACK DEPENDENCIES
  RUNTIME:
    Python 3.11+ -> pip -> psutil, torch, faiss-cpu, pyyaml
    Node.js 20+ -> npm -> typescript, @types/node, vite, chart.js, marked, highlight.js
    Rust + Cargo -> cargo -> tauri 2, tauri-plugin-shell, serde, serde_json, sysinfo, nvml-wrapper, keyring, tokio
    Hermes Agent v0.17+ -> Hermes CLI bridge -> process list, cronjob list, status
  BUILD PIPELINE (StydeForge.exe):
    npm install -> npm run build (Vite -> dist/) -> cargo tauri build -> StydeForge.exe + .msi
    Estimated .exe size: 3-5MB (Tauri runtime: ~2MB, Frontend: ~500KB, Libs: ~200KB, Icons: ~200KB)
  INTEGRATION POINTS:
    Forge -> Hermes CLI bridge -> Dashboard (scripts call hermes, dashboard polls hermes process list)
    Spawn -> delegate_task -> DeepSeek API (flash for spawn, pro for eval/teacher)
    State -> state.yaml (single source of truth) -> checkpoint -> USB directory
EXIT CRITERIA STATUS (22 P0 checks)
  FORGE (12):
    F1 init USB structure: UNKNOWN
    F2 detect.py hardware_profile: BUILT
    F3 blueprint validation: BUILT (blueprint.py)
    F4 forge.py spawn delegate_task: BUILT (spawn.py, agent_runner.py)
    F5 self-eval YAML: BUILT (evaluate.py)
    F6 judge-eval deepseek-v4-pro: BUILT (evaluate.py)
    F7 composite scoring: BUILT (evaluate.py)
    F8 teacher actionable proposals: BUILT (teacher.py)
    F9 code-reviewer 10 iterations improving: state.yaml shows activity
    F10 at least one agent >=85: state.yaml shows S:89 J:90 C:89.6 (web-security-engineer)
    F11 checkpoint->crash->recovery: BUILT (checkpoint.py, recovery.py)
    F12 atomic writes no partial files: BUILT (persistence.py)
  DASHBOARD (10):
    D1 StydeForge.exe launches: Dashboard/web/mission_control_8765.html exists (web-based, not .exe yet)
    D2 Dark theme 3 panels: dashboard runs on :8765
    D3 Custom title bar: UNKNOWN
    D4 DeepSeek chat streaming: UNKNOWN
    D5 read_file tool: UNKNOWN
    D6 write_file with confirmation: UNKNOWN
    D7 Agent panel poll 5s: dashboard.py exists
    D8 Start/Stop Forge process: UNKNOWN
    D9 System tray: NOT BUILT (Tauri not scaffolded)
    D10 Config persistence: UNKNOWN