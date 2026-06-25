# Design Decision Log

**Styde Forge v3.0 — "The Crucible"**
**Phase 0 — Reference**

Every design decision logged with date, alternatives considered, and rationale.
Prevents the same discussions from recurring months later.

---

## D01 — Meta-Layer over Docker Swarm

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Use Meta-layer (in-process) instead of Docker Swarm for orchestration |
| **Alternatives** | Docker Swarm with 6+ parallel workers |
| **Rationale** | Machine-B has only 18 GB VRAM. Docker would load the same model 2× = 16-20 GB gone. Meta-layer loads 1 model at a time. Eliminates Docker dependency for portability. |
| **Impact** | Sequential agent execution. Quality focus over throughput. |

## D02 — Quality Gate ≥ 80/100

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | All agents must score ≥ 80/100 on eval to be saved to USB |
| **Alternatives** | Save everything (quantity), or ≥ 90 (elite only) |
| **Rationale** | Prevents USB from filling with mediocre agents. 80 is high enough for quality but achievable. 90 would be too strict initially. |
| **Impact** | ~30-40% of agent runs rejected. Historical Learning captures lessons from failures. |

## D03 — VI as Default on Machine-B

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Variational Inference instead of NUTS on Machine-B (18 GB VRAM) |
| **Alternatives** | NUTS for everything (precision), or always VI (speed) |
| **Rationale** | NUTS requires more VRAM and time. Machine-B has limited resources. VI gives adequate precision in seconds vs minutes for NUTS. NUTS used on Machine-A where compute allows. |
| **Impact** | Slightly less precise weight optimization on Machine-B. Verified against NUTS periodically. |

## D04 — Dual-Model Strategy (Flash + Pro)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Use deepseek-v4-flash for agent spawn, deepseek-v4-pro for eval/teacher |
| **Alternatives** | Single model for everything, or local models |
| **Rationale** | Flash is fast and cheap ($0.14/M output), good enough for 80% of calls. Pro is higher quality ($0.28/M output), essential for eval accuracy. Saves 60% cost vs Pro-only. |
| **Impact** | Agent spawn: ~$0.001. Judge/Teacher: ~$0.002. Total per iteration: ~$0.003. |

## D05 — Caveman Ultra Default Mode

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Caveman Ultra ON by default. No markdown, no fluff, data only. |
| **Alternatives** | Standard verbose output, or toggle per agent |
| **Rationale** | 70% token reduction. Machine-parseable output. Faster inference. Combined with RAG: 90% token reduction vs baseline. |
| **Impact** | Every agent spawn uses ~800 tokens instead of ~8000. Toggle off for human-readable output only. |

## D06 — Atomic Writes for Everything

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | All USB writes use temp-file + rename pattern |
| **Alternatives** | Direct writes, write-ahead log, journaling filesystem |
| **Rationale** | USB disconnect is the #1 corruption risk. Atomic writes guarantee either old or new file exists, never a partial write. |
| **Impact** | Slightly more I/O (temp file + rename). Guaranteed data integrity. |

## D07 — JSON-Lines Logging

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | All logs in JSON-lines format (one JSON object per line) |
| **Alternatives** | Plain text, structured syslog, SQLite |
| **Rationale** | Machine-readable (grep + jq), space-efficient, append-only (safe for USB), no database dependency. |
| **Impact** | Easy to query, rotate, and compress. Compatible with log aggregation. |

## D08 — YAML State (Not Database)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Forge state stored as YAML files, not SQLite/Postgres |
| **Alternatives** | SQLite (single-file DB), PostgreSQL (robust but heavy) |
| **Rationale** | YAML is human-readable, diffable, version-controllable. No database dependency. Works after unzip. Historical Learning uses SQLite internally for query performance — the exception. |
| **Impact** | Simpler import/export. Slower queries for large datasets (mitigated by SQLite for Historical Learning). |

## D09 — Sequential Loop (v3.0)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Single sequential loop in v3.0, not parallel |
| **Alternatives** | Parallel loops for multiple blueprints simultaneously |
| **Rationale** | Machine-B VRAM limits. Teacher feedback benefits from focused attention. Parallelism added in Phase 1+ when proven. |
| **Impact** | Longer time to evaluate all 6 blueprints. Higher quality per agent due to focused teacher attention. |

## D10 — Per-Blueprint Skill Loading

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Subagents load only their blueprint's skills (3-5), not all 85+ built-in |
| **Alternatives** | Load all skills, or load none |
| **Rationale** | Cleaner context = sharper focus = better output. 85 skills in context would be noise. |
| **Impact** | Agents are narrower but deeper. New skills must be explicitly added to blueprints. |

## D11 — Circuit Breaker Pattern

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Implement circuit breaker per blueprint + global |
| **Alternatives** | Retry indefinitely, or manual intervention |
| **Rationale** | Prevents wasted API costs on broken loops. After 3-5 consecutive failures, halts and alerts. Auto-resets after timeout. |
| **Impact** | Prevents runaway costs. Requires human review after breaker trips. |

## D12 — RAG on RTX 3080

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Run embeddings on idle RTX 3080 using all-MiniLM-L6-v2 |
| **Alternatives** | API-based embeddings (cost), or no RAG (slow) |
| **Rationale** | 3080 is idle during API calls. Embeddings cost nothing locally. 67% token reduction. Combined with Caveman: 90% reduction. |
| **Impact** | Agents get relevant context instead of everything. Faster, cheaper, better. |

## D13 — Phase 0 as Pure Design

| Field | Value |
|-------|-------|
| **Date** | 2026-06-25 |
| **Decision** | Phase 0 contains only design documentation. No executable code. |
| **Alternatives** | Build code during design (risk of premature implementation) |
| **Rationale** | Design the complete system before building anything. Prevents rework. All interfaces specified before implementation. |
| **Impact** | 54 documents, 14 sections. Phase 1 starts with clear contracts. |

---

## Design Principles (PrecisionForge)

| Principle | Meaning |
|-----------|---------|
| **One logical home** | Every piece of data has exactly one canonical location |
| **Atomicity first** | All writes are transactional — never partial |
| **Hardware aware** | System auto-adapts to available resources |
| **Full traceability** | Every decision, eval, and version change is logged |
| **Quality gate** | Nothing below 80/100 is saved |
| **Caveman default** | 70% fewer tokens, 2× faster, 3× cheaper |
| **Self-contained** | The USB is the entire system |

---

**Status:** 13 decisions documented with alternatives and rationale.
