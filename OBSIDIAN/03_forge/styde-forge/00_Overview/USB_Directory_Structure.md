# USB Directory Structure

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Purpose

Define the exact file and folder layout on the 48 GB USB drive. Every file
has exactly one logical home. No catch-all directories. No redundancy.

---

## 2. Root Structure

```
HermesForge/
│
├── 00_MANIFEST.json                  # Master manifest: SHA256, version, generation date
├── FORGE.md                          # Human-readable forge description
├── state.yaml                        # Global forge state
│
├── 01_KNOWLEDGE/                     # Indexed, sourced knowledge bases
│   └── <domain>/                     #   One folder per knowledge domain
│       ├── corpus.md                 #   Synthesized knowledge
│       ├── index.json                #   Searchable index
│       └── sources/                  #   Source references with links
│
├── 02_AGENTS/                        # Spawned agent instances
│   └── <agent-id>/                   #   One folder per agent
│       ├── AGENT.md                  #   Metadata, lineage, status
│       ├── spawn_context.md          #   Full context used at spawn
│       ├── spawn_task.md             #   Task the agent was given
│       ├── checkpoints/              #   Per-agent checkpoints
│       └── runs/                     #   Execution history
│           └── <run-id>/
│               ├── input.md          #   Task and context
│               ├── output.md         #   Agent's response
│               ├── self_eval.yaml    #   Self-evaluation
│               ├── judge_eval.yaml   #   LLM-as-Judge evaluation
│               └── eval.yaml         #   Composite result
│
├── 03_HOOKS/                         # Minimal, focused integrations
│   ├── integrations/                 #   System integrations
│   └── events/                       #   Event handlers
│
├── 04_SKILLS/                        # Reusable, modular skills
│   ├── modular/                      #   General-purpose skills
│   └── composable/                   #   Composable skill chains
│
├── 05_LOOPS/                         # Self-improvement loop artifacts
│   └── self_improvement/
│       ├── v1/
│       ├── v2/
│       └── metrics/                  #   Loop performance metrics
│
├── 06_IMPROVEMENTS/                  # Tracked improvements
│   ├── global/                       #   Forge-wide improvements
│   ├── version_decisions/            #   Version increment logs
│   ├── health_history/               #   Health monitoring history
│   └── validation_summaries/         #   Validation reports
│
├── 07_GENERATIONS/                   # Agent lineage and history
│   ├── version_history.json          #   Complete version tree
│   └── archive/                      #   Archived old generations
│
├── 08_TEACHER_LOGS/                  # Teacher/coach agent logs
│   └── <cycle>/                      #   Per loop cycle
│       ├── teacher_feedback.md       #   Feedback given
│       └── extracted_patterns.md     #   Patterns identified
│
├── 09_CHECKPOINTS/                   # Atomic state snapshots
│   └── checkpoint-YYYYMMDD-HHMMSS/
│       ├── state.yaml
│       ├── blueprints/
│       ├── agents/
│       └── eval/
│
├── 10_IMPORT/                        # Import instructions
│   └── IMPORT_INSTRUCTIONS.md        #   Single-prompt import guide
│
├── 99_INDEXES/                       # Global indexes
│   ├── master_index.json             #   Complete content index
│   ├── hardware_profile.json         #   Current hardware profile
│   ├── cost_summary.json             #   Token/cost tracking
│   └── historical_knowledge.db       #   SQLite learning database
│
├── hardware/                         # Hardware profiles (reference)
│   ├── profiles.yaml
│   └── detect.py
│
└── logs/                             # Operational logs
    ├── forge.log                     #   Main log (JSON-lines)
    ├── loops/                        #   Per-iteration logs
    ├── agents/                       #   Per-agent logs
    ├── errors/                       #   Crash/incident logs
    ├── security/                     #   Security event logs
    ├── validation/                   #   Blueprint validation logs
    ├── costs/                        #   Cost tracking logs
    └── recovery/                     #   Recovery event logs
```

---

## 3. Inclusion/Exclusion Rules

### Included
- Structured, non-redundant content
- Every file has a clear purpose
- All content is machine-readable and versioned

### Excluded
- Redundant copies (use links/index instead)
- Unstructured raw material
- Temporary or cache files
- Low-quality or unoptimized content (< 80/100)

---

## 4. Storage Budget (48 GB)

| Category | Budget | Path |
|----------|--------|------|
| Agents | 25 GB | `02_AGENTS/` |
| Knowledge | 8 GB | `01_KNOWLEDGE/` |
| Skills & Hooks | 5 GB | `04_SKILLS/`, `03_HOOKS/` |
| Eval Results & Lineage | 4 GB | `07_GENERATIONS/`, agent runs |
| Checkpoints | 3 GB | `09_CHECKPOINTS/` |
| Logs & Teacher Data | 2 GB | `08_TEACHER_LOGS/`, `logs/` |
| Overhead & Indexes | 1 GB | `00_MANIFEST.json`, `99_INDEXES/` |

---

## 5. Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Agent ID | `agent-<blueprint>-<YYYYMMDD>-<HHMMSS>` | `agent-code-reviewer-20260625-123000` |
| Run ID | `run-<YYYYMMDD>-<HHMMSS>` | `run-20260625-123500` |
| Checkpoint | `checkpoint-<YYYYMMDD>-<HHMMSS>` | `checkpoint-20260625-130000` |
| Loop cycle | `loop-<YYYYMMDD>-<HHMMSS>` | `loop-20260625-124500` |

---

**Status:** Defined. Foundation for all USB writes.
