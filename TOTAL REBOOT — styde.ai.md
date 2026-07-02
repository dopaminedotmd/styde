
> One plan to replace them all. ADHD-friendly. Bot-ready. Keeps everything good. Archives everything redundant. Builds what matters.

---

## Context

styde.ai is 1 week old. Two founders with ADHD + autism. Exceptional design skills, zero code. Planning psychosis caught early — now we redirect to building. This plan replaces ALL 6 existing plans with ONE source of truth.

IMPORTANT

William and Alpedal both run bots (Hermes/Antigravity). This plan includes ready-to-paste prompts so the bots can execute alongside their humans.

---

## Part 1: What We Keep (Gold)

These are the things you've done RIGHT. Lifting them higher.

|Gold|Why it's gold|Action|
|---|---|---|
|**Audit → Build → Operate** model|Proven B2B SaaS model. Deduction clause is smart.|Keep as-is|
|**12 ca-skills**|Well-structured, correct format, progressive loading works|Keep all 12|
|**_RULES.md**|Consistent doc format across everything|Update slightly|
|**Alpedal's blueprint format**|`persona.md + BLUEPRINT.md + config.yaml + skills/` is genuinely excellent agent definition format|Adopt as styde.ai standard|
|**Forge eval pipeline concept**|Self-eval → Judge → Composite scoring. This IS your moat.|Build in Phase 3, not Phase 1|
|**Caveman Ultra**|70% token reduction for agent prompts. Real cost savings.|Adopt immediately in all internal prompts|
|**Security thinking** (BUILD_PHASE_2 §3)|Tenant isolation, GDPR, log retention — ahead of schedule|Keep as reference, build when needed|
|**Pricing**|19,900 audit / 99-300k build / 4,900-19,900/mo operate|Keep, test with real prospects|
|**The Consultant Agent concept**|Crawl → classify → diagnose → report. Revenue enabler.|**Build FIRST**|
|**Teacher Agent concept**|Analyze logs → suggest improvements → extract skills|Keep for Phase 3|

---

## Part 2: New File Structure

### Current (messy)

obsidian/

├── INDEX.md

├── SYSTEM_DOCUMENT.md ← and .html duplicate

├── _RULES.md

├── 00_strategy/ (4 files — good)

├── 01_plan/ (8 files — 6 overlapping plans!)

├── 02_architecture/ (5 files — some overlap with brainstorm)

├── 03_prototypes/ (5 subdirs — mixed purposes)

├── 04_clients/ (templates only)

├── 05_ops/ (audits + ops mixed)

└── 99_references/

### New (watertight)

obsidian/

├── _RULES.md                    ← Updated (add §11 Server, §12 Sprints)

├── INDEX.md                     ← Rewritten (single clean entry point)

├── _users/                      ← Keep (william.md, alpedal.md)

├── _templates/                  ← Keep

├── _skills/                     ← Keep

│

├── 00_strategy/                 ← Keep unchanged

│   ├── BUSINESS_CONCEPT.md

│   ├── MARKET.md

│   ├── OFFER.md

│   └── PRICING_MODEL.md

│

├── 01_plan/                     ← CLEANED: one plan + sprints

│   ├── MASTER_PLAN.md           ← [NEW] THE plan. Replaces all 6.

│   ├── SPRINT_CURRENT.md        ← [NEW] This week's tasks only.

│   ├── SPRINT_LOG.md            ← [NEW] Completed sprints log (dopamine).

│   └── _archive/                ← [NEW] Old plans moved here

│       ├── MASTER_PLAN_FINAL.md

│       ├── IMPLEMENTATION_PHASE_1.md

│       ├── BUILD_PHASE_2.md

│       ├── ROADMAP.md

│       ├── PLAN_SUMMARY.md

│       ├── REORG_01.md

│       ├── _PLANNING_RULES.md

│       └── 2026-06-25-hypothetical-agents-design.md

│

├── 02_architecture/             ← CLEANED

│   ├── SYSTEM_OVERVIEW.md       ← [REWRITE] Clean architecture picture

│   ├── SERVER_SETUP.md          ← [NEW] Shared server architecture

│   ├── DASHBOARD_SPEC.md        ← [UPDATE] Merged customer+admin

│   ├── AGENT_FRAMEWORK.md       ← [UPDATE] Adopt Forge blueprint format

│   └── _archive/

│       ├── FORGE_INTEGRATION.md ← Reference (concepts adopted into plan)

│       └── SYSTEM_BRAINSTORM.md ← Reference (absorbed into SYSTEM_OVERVIEW)

│

├── 03_forge/                    ← RENAMED from 03_prototypes

│   ├── README.md                ← [NEW] "Alpedal's design reference"

│   ├── styde-forge/             ← Keep as reference (86 docs, read-only)

│   ├── styde-forge-dashboard/   ← Keep as reference (35 docs, deprioritized)

│   └── styde-forge-phase1/      ← Keep as reference

│

├── 04_clients/                  ← Keep structure

│   ├── _active/

│   └── templates/

│

├── 05_ops/                      ← Keep, add sprint logs

│   ├── ONBOARDING.md

│   ├── SUBSCRIPTION_TIERS.md

│   ├── AGENT_PATTERNS.md

│   ├── audits/                  ← [NEW] Move audits here

│   │   ├── AUDIT_OPUS_2026-06-25.md

│   │   ├── AUDIT_DASHBOARD_2026-06-25.md

│   │   └── AUDIT_STYDEFORGE_2026-06-25.md

│   └── logs/

│

└── 99_references/               ← Keep

### Key Changes

|Change|Why|
|---|---|
|8 plan files → 1 `MASTER_PLAN.md` + sprints|Kill planning paralysis. One truth.|
|Sprint system (`SPRINT_CURRENT.md`)|ADHD needs: short goals, clear done-criteria, visible progress|
|`_archive/` folders|Nothing deleted. Just moved. Can always go back.|
|`03_prototypes/` → `03_forge/`|Clearer name. It's Alpedal's reference material.|
|Audit files → `05_ops/audits/`|Ops folder was getting cluttered|
|`SERVER_SETUP.md`|New file for shared server architecture|
|`SYSTEM_DOCUMENT.md` + `.html` removed from root|Folded into `INDEX.md`|

---

## Part 3: The Master Plan

This goes into `obsidian/01_plan/MASTER_PLAN.md`. Replaces all 6 old plans.

### Structure of MASTER_PLAN.md:

markdown

# MASTER PLAN — styde.ai

## 1. What We Are

AI agent systems for Swedish SMEs. Audit → Build → Operate.

## 2. Team

- William: Builder + Seller. Owns platform, code, customers.

- Alpedal: Auditor + Blueprint Designer. Owns agent quality, patterns, audits.

## 3. The Phases (sequential, not parallel)

### Phase 1: FIRST BLOOD (Weeks 1-3)

Goal: Build Consultant Agent + get first sales meeting.

- [sprint tasks...]

### Phase 2: FIRST CUSTOMER (Weeks 4-8)

Goal: Land audit + deliver first agent system.

- [sprint tasks...]

### Phase 3: THE MOAT (Weeks 9-16)

Goal: Eval pipeline + self-improving agents + dashboard.

- [sprint tasks...]

### Phase 4: SCALE (Months 4-12)

Goal: 5+ customers, 1.5M ARR.

## 4. Architecture (one diagram)

## 5. Server Setup

## 6. Decisions That Apply

## 7. What We Explicitly Don't Build Yet

---

## Part 4: Server Architecture

William mentioned: "vi har en dator som vi tänkte sätta detta på och styra en server."

### Proposed Setup

┌─────────────────────────────────────────────────┐

│              SHARED SERVER (fysisk dator)        │

│              (accessible via local network/VPN)  │

│                                                  │

│  ┌──────────────────────────────────────────┐   │

│  │  styde.ai PLATFORM                      │   │

│  │                                          │   │

│  │  Next.js App (customer + admin views)    │   │

│  │  Express API (agent runtime, auth)       │   │

│  │  PostgreSQL (customers, logs, agents)    │   │

│  │  Forge Engine (eval, RAG — when ready)   │   │

│  └──────────────────────────────────────────┘   │

│                                                  │

│  ┌──────────────────────────────────────────┐   │

│  │  ACCESSIBLE VIA                          │   │

│  │                                          │   │

│  │  William  ──→ SSH + VS Code Remote       │   │

│  │  Alpedal  ──→ SSH + VS Code Remote       │   │

│  │  Customers ──→ HTTPS (when dashboard     │   │

│  │               is ready, via Cloudflare   │   │

│  │               Tunnel or reverse proxy)   │   │

│  └──────────────────────────────────────────┘   │

│                                                  │

│  OS: Ubuntu Server 24.04 LTS                    │

│  Runtime: Node.js 20 LTS + Python 3.12          │

│  Database: PostgreSQL 16                         │

│  Reverse proxy: Caddy (auto HTTPS)              │

└─────────────────────────────────────────────────┘

IMPORTANT

**Question for William:** What hardware does this server have? GPU? RAM? CPU? This determines whether Forge's RAG engine can run on it.

### Why Server > Cloud (for now)

|Factor|Own Server|Cloud (Vercel+VPS)|
|---|---|---|
|GDPR|Data stays on your hardware. Perfect.|VPS in EU works but adds vendor trust.|
|Cost|Electricity only (~200 SEK/mo)|VPS ~400-800 SEK/mo + Vercel costs|
|GPU for RAG|If server has GPU → run embeddings locally|Need Pinecone (~$70+/mo)|
|Reliability|Your internet/power = your uptime|99.9% uptime guaranteed|
|Both access|SSH + VS Code Remote. Both code on same machine.|Both deploy to same cloud.|

**Recommendation:** Start on own server. Add Cloudflare Tunnel when customers need HTTPS access. Move to cloud only if uptime becomes critical (SLA customers).

---

## Part 5: Sprint System (ADHD-Optimized)

### Why This Works for ADHD

|ADHD Challenge|Sprint Solution|
|---|---|
|Can't start big tasks|Each sprint = max 3 tasks, max 3 days|
|Lose track of progress|`SPRINT_LOG.md` = visible history of wins|
|Context loss between sessions|Each sprint starts with "WHERE WE ARE" summary|
|Hyperfocus on wrong thing|Sprint scope is locked. New ideas → backlog, not sprint.|
|Need dopamine|Each completed task = checkbox ✓. Each completed sprint = entry in victory log.|
|Parallel planning temptation|ONE sprint active. Period. Next sprint planned only when current is done.|

### Sprint Format

markdown

# SPRINT 01 — "First Blood"

> Started: 2026-06-26 | Due: 2026-06-28

## WHERE WE ARE

- styde.ai has 0 code, 130+ docs

- This sprint: build the thing that enables sales

## TASKS (max 3)

- [ ] **William:** Build Consultant Agent v0.1 (Python CLI: URL → report)

- [ ] **Alpedal:** Write 3 agent blueprints (invoice-reviewer, customer-service-triage, mail-sorter)

- [ ] **William:** Set up shared server (Ubuntu + Node + PostgreSQL)

## DONE WHEN

- [ ] `python konsult.py https://example.se` → prints structured YAML report

- [ ] 3 blueprint folders exist with persona.md + blueprint.yaml + tools.yaml

- [ ] Both William and Alpedal can SSH into server

## BLOCKED BY

Nothing. Start immediately.

## IDEAS (NOT this sprint — backlog)

- Dashboard

- Forge eval pipeline

- Website

### Sprint Rules

1. **Max 3 tasks per sprint.** Not 5. Not 7. Three.
2. **Max 3 days per sprint.** Then review + new sprint.
3. **New ideas go to backlog, not sprint.** Write them in `## IDEAS` section.
4. **No sprint change mid-sprint** unless William explicitly says so.
5. **Sprint starts with bot prompt** (see Part 7) so bots know what's happening.

---

## Part 6: Role Clarity

### William — Builder + Seller

|Responsibility|Priority|When|
|---|---|---|
|Write code (Python, Next.js, Express)|P0|Always|
|Sales outreach (20/day)|P0|Starting Sprint 02|
|Server setup + maintenance|P1|Sprint 01|
|Customer relations|P1|When leads exist|
|GDPR (interim DPO)|P2|Before first customer data|

**William does NOT:** Design blueprints (Alpedal does). Write 587-line plan documents (bot does). Build Tauri apps.

### Alpedal — Auditor + Blueprint Designer

|Responsibility|Priority|When|
|---|---|---|
|Design agent blueprints (Forge format)|P0|Sprint 01 onward|
|Conduct customer audits (in-person or remote)|P0|When first audit is booked|
|Test Consultant Agent output (quality review)|P1|Sprint 02|
|Write patterns for AGENT_PATTERNS.md|P1|After first agents run|
|Design eval rubrics for agent quality|P2|Phase 3|

**Alpedal does NOT:** Write production code (learns over time). Build Tauri desktop app (deprioritized). Manage server infrastructure.

### Alpedal's Growth Path

Month 1-2:  Blueprint designer + audit partner (NO CODE)

Month 3-4:  Start coding: simple Python scripts for audit automation

Month 5-6:  Build Forge eval scripts (Python) on the shared server

Month 7+:   Independent builder — if Tauri still relevant, start then

---

## Part 7: Bot Prompts

### Prompt 1: Sprint Start (paste into Hermes at sprint start)

markdown

## SPRINT CONTEXT — paste this at the start of each new sprint

Read obsidian/01_plan/SPRINT_CURRENT.md — it contains this sprint's tasks.

Read obsidian/01_plan/MASTER_PLAN.md — it's the single source of truth.

Read obsidian/_RULES.md — all document rules.

YOUR ROLE: You are helping William build styde.ai.

CURRENT SPRINT: [Sprint number and name from SPRINT_CURRENT.md]

YOUR CONSTRAINTS:

- Do NOT suggest work outside the current sprint scope

- If William gets sidetracked, gently redirect: "That's a great idea.

  Add it to ## IDEAS in SPRINT_CURRENT.md. For now, let's finish [current task]."

- When a task is done, update the checkbox in SPRINT_CURRENT.md

- When all tasks are done, write a summary to obsidian/01_plan/SPRINT_LOG.md

FOCUS: Build working code. Not more documents. Not more plans.

Documents are only created when they ARE the deliverable (like blueprints).

### Prompt 2: Alpedal's Bot — Blueprint Work

markdown

## ALPEDAL BOT CONTEXT — paste this for blueprint design work

Read obsidian/01_plan/SPRINT_CURRENT.md — your current tasks.

Read obsidian/01_plan/MASTER_PLAN.md — the plan.

Read obsidian/_RULES.md — document rules (frontmatter, tags, comments).

YOUR ROLE: You are helping Alpedal design agent blueprints for styde.ai.

Alpedal's strengths: pattern recognition, systems thinking, seeing what

others miss. He is NOT writing code — he is designing how agents should

behave, what they need, and how they should be evaluated.

BLUEPRINT FORMAT (adopted from Styde Forge):

Each blueprint lives in: agent-blueprints/{blueprint-name}/

Required files:

  - blueprint.yaml  → metadata, cost, time_savings, requirements

  - persona.md      → who the agent IS (role, voice, personality)

  - prompt_template.md → system prompt with {{mustache}} variables

  - tools.yaml      → what APIs/tools the agent can use

  - tests/input.json + tests/expected.json → test cases

REFERENCE: obsidian/03_forge/styde-forge/01_Vision/Blueprint_Catalog.md

has 6 example blueprints to use as inspiration.

When designing, always answer:

1. What does this agent DO? (one sentence)

2. What tools does it NEED? (list specific APIs)

3. What should it NEVER do? (security rules)

4. How do we know it worked? (success criteria)

5. How much time does it save? (hours/week)

CONSTRAINT: Max 3 pages per blueprint. No over-designing.

### Prompt 3: Consultant Agent Build (William's main Sprint 01 task)

markdown

## BUILD TASK — Consultant Agent v0.1

Build a Python CLI tool that takes a company URL and produces a

structured audit report. This is styde.ai's FIRST working code.

PATH: apps/konsult-agent/

REQUIREMENTS:

1. Input: company URL (e.g., https://example.se)

2. Crawl: fetch all subpages (requests + BeautifulSoup, or Firecrawl)

3. Classify: LLM prompt → industry, size, tech stack

4. Diagnose: LLM prompt → find manual processes, bottlenecks

5. Output: structured YAML report

TECH:

- Python 3.12

- requests + beautifulsoup4 (or firecrawl-py)

- openai or anthropic SDK for LLM calls

- pyyaml for output

- No framework. No server. CLI only.

OUTPUT FORMAT:

```yaml

test_audit:

  company: "Example AB"

  url: "https://example.se"

  industry: "accounting"

  estimated_size: "10-20 employees"

  tech_stack: ["Fortnox", "Slack", "Google Workspace"]

  automation_potential:

    - process: "invoice management"

      signal: "About page mentions manual invoice handling"

      priority: 1

      time_savings_hours_per_week: 8

    - process: "customer support"

      signal: "FAQ with 40+ questions, no chat"

      priority: 2

      time_savings_hours_per_week: 5

DONE WHEN:

- `python konsult.py https://[real-company].se` produces a valid YAML report
- Tested on 3 different company websites
- Report is useful enough to show a prospect

CONSTRAINTS:

- No RAG. No vector database. No Pinecone. Not yet.
- No dashboard. CLI output to terminal + save to file.
- Use ONE LLM provider (whichever API key you have).
- MVP. Ship ugly. Polish later.

### Prompt 4: Server Setup (William)

```markdown

## BUILD TASK — Shared Server Setup

Set up the shared development/production server that both William and

Alpedal access.

REQUIREMENTS:

1. Ubuntu Server 24.04 LTS installed and updated

2. SSH access for both William and Alpedal (key-based auth, no password)

3. Git installed, styde.ai repo cloned

4. Node.js 20 LTS (via nvm)

5. Python 3.12 (via pyenv or system)

6. PostgreSQL 16 installed, user created for styde

7. Caddy web server installed (for future HTTPS reverse proxy)

8. Firewall configured (UFW: allow SSH, HTTP, HTTPS only)

DONE WHEN:

- Both users can SSH in and run `git pull` on the repo

- `node --version` shows 20.x

- `python3 --version` shows 3.12.x

- `psql -U styde -d styde` connects successfully

- Server is accessible from both William's and Alpedal's networks

OPTIONAL (if server has GPU):

- Install NVIDIA drivers + CUDA

- Test: `nvidia-smi` shows GPU info

- This enables local embeddings for RAG later (Phase 3)

### Prompt 5: Mid-Sprint Check (paste when stuck or losing focus)

markdown

Read obsidian/01_plan/SPRINT_CURRENT.md.

Which tasks are still unchecked? List them.

Which task was I working on before I got distracted?

What is the SINGLE NEXT ACTION to move that task forward?

Do not suggest new tasks. Do not suggest architectural changes.

Just help me finish what's in front of me.

---

## Part 8: Phases — The Path Forward

### Phase 1: FIRST BLOOD (Weeks 1-3)

**Goal:** Working Consultant Agent + server running + blueprints ready.

|Sprint|Duration|William|Alpedal|
|---|---|---|---|
|Sprint 01|3 days|Consultant Agent v0.1 (Python CLI)|3 agent blueprints|
|Sprint 02|3 days|Test on 5 real websites + fix bugs|Review output quality + write patterns|
|Sprint 03|3 days|Sales prep: PDF report template from output|Audit process doc (how to run an audit)|

**Phase 1 DONE when:** You can run `python konsult.py https://company.se` → get a report → email it as PDF to a prospect.

### Phase 2: FIRST CUSTOMER (Weeks 4-8)

**Goal:** 20 outreach/day → land audit → deliver first agent.

|Sprint|Duration|William|Alpedal|
|---|---|---|---|
|Sprint 04-05|1 week|Sales: 20 outreach/day|Support with audit prep|
|Sprint 06-07|1 week|Land first audit + conduct with Alpedal|First real customer audit|
|Sprint 08-09|1 week|Build first customer's agents|Write audit report|
|Sprint 10-11|1 week|Deploy agents on server|Review + propose improvements|

**Phase 2 DONE when:** First customer pays. First agent is running.

### Phase 3: THE MOAT (Weeks 9-16)

**Goal:** Dashboard + eval pipeline + self-improving agents.

|Component|What|Who|
|---|---|---|
|Customer Dashboard|Next.js. Agent list, status, "Run" button, history.|William|
|Admin Dashboard|Same app, admin role. All customers, all agents.|William|
|Eval Pipeline v1|Self-eval + Judge eval after each agent run|William + Alpedal|
|Agent Patterns|Collected from first customer. YAML blocks.|Alpedal|
|RAG Engine v1|Pinecone (or local if server has GPU)|William|

**Phase 3 DONE when:** Dashboard shows agents, eval pipeline scores them, patterns grow.

### Phase 4: SCALE (Months 4-12)

- 5+ customers
- Reusable agent library growing
- 1.5-2M SEK ARR target
- Each new customer starts smarter (template upgrades from eval)
- Website + case studies
- Alpedal coding independently

---

## Part 9: Execution Order — What I Will Do

When William approves this plan, I will:

### Step 1: Create new files

-  `obsidian/01_plan/MASTER_PLAN.md` — THE plan
-  `obsidian/01_plan/SPRINT_CURRENT.md` — Sprint 01
-  `obsidian/01_plan/SPRINT_LOG.md` — Empty, ready for wins
-  `obsidian/02_architecture/SERVER_SETUP.md` — Server architecture
-  `obsidian/03_forge/README.md` — Context note for Forge reference docs
-  `obsidian/05_ops/BOT_PROMPTS.md` — All bot prompts from Part 7

### Step 2: Archive old plans

-  Move all 8 files from `01_plan/` → `01_plan/_archive/`
-  Move `FORGE_INTEGRATION.md` and `SYSTEM_BRAINSTORM.md` → `02_architecture/_archive/`
-  Move `SYSTEM_DOCUMENT.md` + `.html` from obsidian root → `_archive/` or fold into INDEX

### Step 3: Update existing files

-  Rewrite `INDEX.md` — clean entry point
-  Update `_RULES.md` — add §11 (Server), §12 (Sprints)
-  Update `DASHBOARD_SPEC.md` — merge customer+admin into one spec

### Step 4: Rename

-  `03_prototypes/` → `03_forge/`

### Step 5: Create app skeleton

-  `apps/konsult-agent/` — folder + requirements.txt + konsult.py skeleton
-  `agent-blueprints/` — folder structure for blueprints

---

## Open Questions for William

IMPORTANT

1. **Server hardware?** What CPU/RAM/GPU does the shared server have? This determines whether RAG runs locally or needs Pinecone.
2. **LLM provider?** Which API do you have access to? (OpenAI, Anthropic, DeepSeek, other?) This determines what the Consultant Agent calls.
3. **Approve archive?** OK to move old plans to `_archive/`? Nothing is deleted — just organized.
4. **Rename `03_prototypes/` → `03_forge/`?** Or keep as `03_prototypes/`?
5. **Language policy?** _RULES.md says Swedish, but all docs are now English. Which do we standardize on?