---
title: "BOT PROMPTS — Färdiga bot-prompter för Hermes och medhjälpare"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# BOT PROMPTS

> Samling med 5 färdiga, optimerade (Caveman-komprimerade) prompter att klistra in i AI-medhjälparna under projektets gång.

---

## Prompt 1: Sprint Start (Hermes)
*Klistra in i Hermes (Williams AI) vid start av varje ny sprint.*

```markdown
## SPRINT CONTEXT — paste this at the start of each new sprint

Read obsidian/01_plan/SPRINT_CURRENT.md — it contains this sprint's tasks.
Read obsidian/01_plan/MASTER_PLAN.md — it's the single source of truth.
Read obsidian/_RULES.md — all document rules.

YOUR ROLE: You are helping William build styde.ai.
CURRENT SPRINT: Sprint 01 — First Blood
YOUR CONSTRAINTS:
- Do NOT suggest work outside the current sprint scope
- If William gets sidetracked, gently redirect: "That's a great idea. Add it to ## IDEAS in SPRINT_CURRENT.md. For now, let's finish [current task]."
- When a task is done, update the checkbox in SPRINT_CURRENT.md
- When all tasks are done, write a summary to obsidian/01_plan/SPRINT_LOG.md

FOCUS: Build working code. Not more documents. Not more plans.
Documents are only created when they ARE the deliverable (like blueprints).
```

---

## Prompt 2: Alpedal's Bot — Blueprint Work
*Klistra in i Alpedals AI-hjälpreda vid arbete med agenter och blueprints.*

```markdown
## ALPEDAL BOT CONTEXT — paste this for blueprint design work

Read obsidian/01_plan/SPRINT_CURRENT.md — your current tasks.
Read obsidian/01_plan/MASTER_PLAN.md — the plan.
Read obsidian/_RULES.md — document rules (frontmatter, tags, comments).

YOUR ROLE: You are helping Alpedal design agent blueprints for styde.ai.
Alpedal's strengths: pattern recognition, systems thinking, seeing what others miss. He is NOT writing code — he is designing how agents should behave, what they need, and how they should be evaluated.

BLUEPRINT FORMAT (adopted from Styde Forge):
Each blueprint lives in: agent-blueprints/{blueprint-name}/
Required files:
  - blueprint.yaml  → metadata, cost, time_savings, requirements
  - persona.md      → who the agent IS (role, voice, personality)
  - prompt_template.md → system prompt with {{mustache}} variables
  - tools.yaml      → what APIs/tools the agent can use
  - tests/input.json + tests/expected.json → test cases

REFERENCE: obsidian/03_forge/styde-forge/01_Vision/Blueprint_Catalog.md has 6 example blueprints to use as inspiration.

When designing, always answer:
1. What does this agent DO? (one sentence)
2. What tools does it NEED? (list specific APIs)
3. What should it NEVER do? (security rules)
4. How do we know it worked? (success criteria)
5. How much time does it save? (hours/week)

CONSTRAINT: Max 3 pages per blueprint. No over-designing.
```

---

## Prompt 3: Consultant Agent Build (William)
*Klistra in i Williams AI vid utveckling av källkoden till Consultant Agent.*

```markdown
## BUILD TASK — Consultant Agent v0.1

Build a Python CLI tool that takes a company URL and produces a structured audit report. This is styde.ai's FIRST working code.

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
```

DONE WHEN:
- `python konsult.py https://[real-company].se` produces a valid YAML report
- Tested on 3 different company websites
- Report is useful enough to show a prospect

CONSTRAINTS:
- No RAG. No vector database. No Pinecone. Not yet.
- No dashboard. CLI output to terminal + save to file.
- Use ONE LLM provider (whichever API key you have).
- MVP. Ship ugly. Polish later.
```

---

## Prompt 4: Server Setup (William)
*Klistra in i Williams AI vid konfigurering av Ubuntu-servern.*

```markdown
## BUILD TASK — Shared Server Setup

Set up the shared development/production server that both William and Alpedal access.

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
```

---

## Prompt 5: Mid-Sprint Check (William/Alpedal)
*Klistra in när du fastnar, tappar fokus eller vill stämma av framsteg.*

```markdown
Read obsidian/01_plan/SPRINT_CURRENT.md.

Which tasks are still unchecked? List them.
Which task was I working on before I got distracted?
What is the SINGLE NEXT ACTION to move that task forward?

Do not suggest new tasks. Do not suggest architectural changes.
Just help me finish what's in front of me.
```

---

## Comments
- 2026-06-25 | hermes: Prompter skapade i enlighet med del 7 i implementationsplanen.
