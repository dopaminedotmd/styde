---
title: "FORGE_INTEGRATION — Styde Forge som styde.ai:s intelligensmotor"
date: 2026-06-25
author: hermes
tags: [area/ARKITEKTUR, status/DRAFT, author/HERMES, type/SPEC]
status: draft
---

# Forge Integration — styde.ai's Intelligence Engine

> Styde Forge = the RAG system + the evolution engine.
> Here agents fetch their intelligence. Here they self-update. Here they get better.
> This is not a separate system — it is the backend of styde.ai.

---

## 1. Corrected Architecture

### 1.1 Previous (Incorrect) Picture

```
Styde Forge (Alpedal)          styde.ai (William)
───────────────────            ──────────────────
USB-based lab                  Cloud platform
Agent refinery                 Customer dashboard
                           →   Export/import of blueprints
```

### 1.2 Correct Picture

```
┌─────────────────────────────────────────────────────────┐
│                   styde.ai PLATFORM                     │
│                                                         │
│  ┌──────────────────┐       ┌─────────────────────────┐ │
│  │  CUSTOMER DASH   │       │    ADMIN PANEL          │ │
│  │  (Next.js)       │       │    (Next.js)            │ │
│  │                  │       │                         │ │
│  │ • View agents    │       │ • All customers         │ │
│  │ • Press "Run"    │       │ • Agent status          │ │
│  │ • View history   │       │ • Prompt editor         │ │
│  └────────┬─────────┘       │ • System health         │ │
│           │                 └────────────┬────────────┘ │
│           │                              │              │
│  ┌────────┴──────────────────────────────┴────────────┐ │
│  │                API GATEWAY                         │ │
│  │  Auth · Routing · Tenant-isolation · Logging       │ │
│  └────────┬──────────────────────────────┬────────────┘ │
│           │                              │              │
│  ┌────────┴──────────┐    ┌──────────────┴────────────┐ │
│  │  AGENT RUNTIME    │    │   STYDE FORGE (RAG)       │ │
│  │  (per customer)   │    │   (intelligence engine)   │ │
│  │                   │    │                           │ │
│  │ • Customer agents │◄───│ • Blueprint database      │ │
│  │ • Trigger/schedule│    │ • Eval pipeline           │ │
│  │ • Tool execution  │───►│ • Teacher Agent           │ │
│  │ • Prompt loading  │    │ • Historical Learning     │ │
│  └───────────────────┘    │ • RAG index (per domain)  │ │
│                           │ • Version management      │ │
│                           │ • Checkpoint/Recovery     │ │
│                           └───────────────────────────┘ │
│                                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │              POSTGRESQL + PINECONE                 │ │
│  │  Customer data · Agent logs · RAG vectors          │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 1.3 Data Flow — How Forge Feeds the Agents

```
1. Alpedal designs blueprint in Forge
   ↓
2. Forge spawns + evaluates agents in loop
   ↓
3. When blueprint reaches ≥85/100 → "promoted to production"
   ↓
4. Blueprint + skills + historical context → RAG index (Pinecone)
   ↓
5. Customer agent at spawn: loads prompt from blueprint + RAG context from Forge
   ↓
6. Customer agent runs → logs back to Forge
   ↓
7. Teacher Agent analyzes logs → suggests improvements
   ↓
8. Improvements → updated blueprint → new version → RAG index updated
   ↓
9. Next time agent runs → new prompt version → better results
```

---

## 2. Forge's Role in Each Agent Lifecycle

### 2.1 Agent Spawn (Acquiring Intelligence)

When a customer agent starts:

```
┌─────────────────────────────────────────────────────┐
│                 AGENT SPAWN                          │
│                                                     │
│  1. Load blueprint from Forge (latest ≥85)          │
│  2. Load blueprint-specific skills                  │
│  3. Load RAG context from Pinecone:                 │
│     - Historical successful patterns (pattern lib)  │
│     - Customer-specific knowledge (tenant-isolated) │
│     - Industry-specific domain knowledge            │
│  4. Load historical learning:                       │
│     - What has worked for similar agents?           │
│     - Which anti-patterns to avoid?                 │
│  5. Build spawn_context → agent runs                │
└─────────────────────────────────────────────────────┘
```

### 2.2 Agent Evaluation (Getting Better)

After each agent run:

```
┌─────────────────────────────────────────────────────┐
│              FORGE EVAL LOOP                         │
│                                                     │
│  Agent output + logs                                │
│       ↓                                             │
│  Self-Eval (the agent itself)                       │
│       ↓                                             │
│  LLM-as-Judge (deepseek-v4-pro)                     │
│       ↓                                             │
│  Composite Score                                    │
│       ↓                                             │
│  ≥80? → Teacher analyzes → suggests improvement     │
│  <80? → Anti-pattern logged → blueprint flagged     │
│       ↓                                             │
│  Human oversight (William/Alpedal approves)          │
│       ↓                                             │
│  Prompt updated → new version → RAG index sync      │
└─────────────────────────────────────────────────────┘
```

### 2.3 Self-Improvement (Evolving)

Continuous loop over time:

```
Week 1: Agent A runs 50 times → 3 improvement suggestions → 1 approved
Week 2: Agent A runs 50 times → prompt v1.1 → score +2.3
Week 3: Agent B (different customer, same blueprint) → starts on v1.1 → immediately better
Week 4: Pattern detected → ≥2 customers have same improvement → template upgrade
```

---

## 3. What Must Be Built — Correct Order

### 3.0 IMMEDIATELY — Adopt Forge Concepts in Existing Plans

| Action | Effect |
|--------|--------|
| Update `IMPLEMENTATION_PHASE_1` — Forge is the RAG backend, not a separate Agent Wardrobe | All build planning starts from Forge as the engine |
| Update `BUILD_PHASE_2` — Agent improvement (§2) is driven by Forge's eval pipeline | Clearer architecture |
| Create `ca-forge-rag` — new skill that controls how agents fetch context from Forge | The bridge between runtime and intelligence |

### 3.1 Phase 1A — Blueprint → RAG (Week 1-2)

Build the system that makes Forge blueprints available as RAG:

```
Blueprint (Forge) → Pinecone index → Agent runtime query
```

**Components:**
1. `forge-ingest` — Python script that takes a blueprint + history → Pinecone vectors
2. `ca-forge-rag` — Skill that loads RAG context at agent spawn
3. Blueprint validator — ensures the blueprint is ≥85/100 before ingest

### 3.2 Phase 1B — Eval Loop (Week 2-4)

Build the eval pipeline that continuously improves agents:

```
Agent run → Logs → Self-Eval → Judge-Eval → Teacher → Improvement
```

**Components:**
1. `eval-runner` — Runs self-eval + judge-eval after each agent run
2. `teacher-agent` — Analyzes eval results, suggests prompt improvements
3. `improvement-queue` — Queue of approved/rejected improvements
4. Dashboard view — Show improvement suggestions for William/Alpedal

### 3.3 Phase 1C — Historical Learning (Week 3-5)

Build the system that learns over time:

```
All runs → Pattern database → New agents start smarter
```

**Components:**
1. `pattern-detector` — Finds recurring success patterns
2. `anti-pattern-log` — Logs recurring errors
3. `cost-optimizer` — Caveman Ultra + model selection per blueprint

### 3.4 Phase 1D — Admin Dashboard (Week 4-6)

The dashboard that gives William/Alpedal overview:

| View | Content |
|------|---------|
| **Forge Health** | Number of blueprints, eval scores, RAG index size, active loops |
| **Agents per Customer** | Status, latest score, prompt version, improvement queue |
| **Improvement Queue** | Approve/reject prompt changes, see diff, bump version |
| **Pattern Library** | Successful patterns, anti-patterns, cost analysis |
| **RAG Status** | Index size per domain, latest ingest, vector statistics |

---

## 4. Alpedal's Role — Clear Responsibility Division

| Alpedal (Styde Forge) | William (styde.ai) |
|------------------------|---------------------|
| Designs blueprints (persona + skills + config) | Builds API Gateway + dashboard |
| Runs eval loops → improves prompt quality | Builds agent runtime (spawn, trigger, tools) |
| Responsible for blueprints reaching ≥85/100 | Responsible for customers getting the right agent deployed |
| Manages pattern library + historical learning | Manages customer relations + tenant isolation |
| Caveman Ultra + token optimization | GDPR + security + hosting |
| Experiments with new agent types | Sells + onboards customers |

**Interface:** Forge exports blueprints as RAG index. styde.ai consumes RAG index at agent spawn. Both see the same dashboard (admin panel).

---

## 5. Technical Implementation — Forge in the Cloud

Styde Forge was designed for USB. It must be adapted for cloud:

| Forge USB Concept | Cloud Equivalent |
|-------------------|------------------|
| USB (48 GB) | Pinecone + PostgreSQL |
| `02_AGENTS/` (spawned agents) | API Gateway agent runtime |
| `01_KNOWLEDGE/` (domain knowledge) | Pinecone namespaces per domain |
| `04_SKILLS/` (modular skills) | styde.ai `skills/` + `.agents/skills/` |
| `09_CHECKPOINTS/` (snapshots) | PostgreSQL backups + point-in-time recovery |
| `99_INDEXES/master_index.json` | Dashboard API: `GET /api/forge/status` |
| `logs/forge.log` (JSON-lines) | PostgreSQL `agent_logs` table |
| Hardware Adaptation Layer | Resource Governor in VPS environment (CPU/RAM/disk limits) |
| Atomic writes (temp→rename) | Database transactions |

**Kept unchanged:**
- Eval pipeline (6 layers)
- Teacher Agent (feedback loop)
- Blueprint format (persona.md + BLUEPRINT.md + config.yaml)
- Caveman Ultra
- Dual-model strategy (Flash for spawn, Pro for eval)
- 6 domains + 6 blueprints

### 5.1 RAG Engine — Concrete Implementation

Alpedal has specified the RAG layer in `14_RAG_Retrieval/RAG_Retrieval.md`:

| Component | Implementation | Details |
|-----------|---------------|---------|
| Chunker | 512-token chunks, 10% overlap | ~2000 chars per chunk |
| Embedder | `all-MiniLM-L6-v2` | 384-dim vectors, ~80 MB, runs on RTX 3080 |
| Vector Store | FAISS (in-memory) or ChromaDB (disk) | <100K chunks, flat L2 index |
| Retrieval | Top-3 chunks per query | ~5ms inference time |
| VRAM Usage | ~1 GB | Leaves 9 GB free on 3080 |

**Combined with Caveman Ultra:**
```
8000 tokens → 2400 (Caveman) → 800 (Caveman + RAG) = 90% reduction
$0.002/spawn → $0.0006 → $0.0002
```

**Cloud equivalent:** Replace local FAISS with Pinecone. Replace `all-MiniLM-L6-v2` with Pinecone's hosted embeddings. Same chunking strategy, same retrieval logic.

### 5.2 Dashboard Alignment

Alpedal's `Dashboard_Phase0/` specifies a **desktop application** (Tauri v2, Rust backend) for controlling StydeForge locally. This is SEPARATE from styde.ai's customer/admin web dashboards:

| Dashboard | Owner | Tech | Users |
|-----------|-------|------|-------|
| StydeForge Desktop | Alpedal | Tauri + Rust + HTML/CSS | Alpedal (control Forge locally) |
| Customer Dashboard | William | Next.js + Tailwind | Customers (see agents, press buttons) |
| Admin Dashboard | William | Next.js + Tailwind | William + Alpedal (customer overview) |

The Admin Dashboard must pull data from BOTH sources:
- Customer agent status → API Gateway
- Forge blueprint status → Forge health API (from desktop or cloud Forge)

---

## 6. Immediate Next Steps

| Prio | Action | Responsible | Time |
|------|--------|-------------|------|
| **P0** | Update `IMPLEMENTATION_PHASE_1` — Forge as RAG backend | Hermes | Now |
| **P0** | Update `BUILD_PHASE_2` §2 — Forge-integrated eval loop | Hermes | Now |
| **P0** | Create `ca-forge-rag` skill — blueprint → Pinecone → agent context | Hermes | 1 day |
| **P1** | Build `forge-ingest` script — blueprint → Pinecone vectors | William | 2 days |
| **P1** | Adopt Caveman Ultra in all ca-skills prompts | Hermes | 1 day |
| **P2** | Alpedal reviews this plan — confirm that Forge can be adapted to cloud | Alpedal | — |
| **P2** | Design admin dashboard with Forge health view | Hermes + William | — |

---

## 7. Rules That Change (Updated)

### _RULES.md

| § | Change |
|---|--------|
| §9 (System Architecture) | Add: "Styde Forge is styde.ai's RAG engine. All agents fetch context from Forge via `ca-forge-rag`." |
| §10 (Logging) | JSON-lines format. `ca-change-logger` updated with Forge-compatible schema. |
| New §11 | "Forge Blueprints: All agents are built from blueprints in Forge. A blueprint must be ≥85/100 to be deployed to a customer. Blueprints are versioned in Forge, consumed by styde.ai." |

### IMPLEMENTATION_PHASE_1

The entire plan is rewritten with Forge as the RAG backend. Agent Wardrobe (§1A.2) becomes the Forge blueprint catalog. Architect Agent (§1B) matches audit results → Forge blueprints.

### BUILD_PHASE_2

§2 (Agent Improvement) completely rewritten — Forge's eval pipeline replaces the simpler feedback loop. Caveman Ultra becomes §2.8.

---

## Comments

- 2026-06-25 | hermes: Rewritten after William's correction. Styde Forge is NOT a separate lab — it is styde.ai's RAG engine and intelligence layer. Agents fetch their intelligence from here. Self-updating and evolution occur through Forge's eval pipeline. The dashboard must show Forge health as a central view.

> *Translated from Swedish to English by Hermes on 2026-06-25.*
