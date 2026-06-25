---
title: "BUILD_PHASE_2 — System Build"
date: 2026-06-24
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/PLAN]
status: draft
---

# BUILD_PHASE_2 — System Build

> [!warning] Focus on the build
> This is the plan for building a sharp internal system — before we sell.
> The team is onboarded during this time. No sales until the system is proven.

> Last updated: 2026-06-24

---

## Contents

1. [[#1. Agent Flow — how agents work]]
2. [[#2. Agent Improvement — self + by each other]]
3. [[#3. Cyber Security — built-in from the start]]
4. [[#4. Dashboard — features and build order]]
5. [[#5. Website — lead capture and case studies]]

---

## 1. Agent Flow — how agents work

Today's [[AGENT_FRAMEWORK]] describes an agent as an isolated unit. That's not enough. We need to design **the entire flow** from trigger to result — and how agents collaborate.

### 1.1 Agent Types

| Type | Trigger | Example | Usage |
|-----|---------|---------|------------|
| **Manual** | Button in dashboard | "Send the report now" | First deployment, ad-hoc |
| **Scheduled** | Cron | "Check invoices every Monday 08:00" | 80% of agents |
| **Event-driven** | Webhook / email / Slack | "When email from customer X arrives" | Real-time processes |
| **Chained** | Output from another agent | "When Agent A is done → start B with its data" | Complex pipelines |

### 1.2 Agent Lifecycle (per run)

```
TRIGGER → INPUT → PROCESS → OUTPUT → LOG → STORAGE
             ↑                        ↓
           TOOLS                dashboard/NOTIFICATION
```

Each run gets a unique `run_id`. All steps are logged.

| Step | Details | Tech |
|------|----------|--------|
| **TRIGGER** | Cron, webhook, manual button | API Gateway (see [[SYSTEM_OVERVIEW]]) |
| **INPUT** | Agent receives data (from trigger or chain) | JSON in request body |
| **DRY-RUN** | Test mode: no real API calls. Logs what WOULD have happened. Mandatory in dev. | flag `dry_run: true` in config.yaml |
| **PROCESS** | AI calls LLM with system prompt + input | Hermes / OpenAI / provider of choice |
| **TOOLS** | Agent calls APIs during the process | tools.yaml defines what's available |
| **OUTPUT** | Structured result | JSON according to prompt's output format |
| **LOGGING** | All steps logged centrally | Log database, traceable per run_id |
| **STORAGE** | Result saved + displayed in dashboard | API Gateway → Dashboard DB |

### 1.3 Retry State

A run that is retried keeps the same `run_id` with attempt index:

```
run_id: "a1b2c3.attempt=1"  ← first attempt
run_id: "a1b2c3.attempt=2"  ← retry
run_id: "a1b2c3.attempt=3"  ← last retry
```

This makes the log traceable across all attempts for the same event.
Max 3 attempts per run. After that, permanent error.

### 1.4 Chained Agents (Pipelines)

A customer flow may require multiple agents in sequence:

```
Agent A: "Fetch invoices from Fortnox"
    → Result: [list of invoices]
Agent B: "Check each invoice against accounting rules" (takes A's output)
    → Result: [OK, OK, FLAG: missing VAT]
Agent C: "Send email to customer about flagged invoices" (takes B's output)
    → Result: [3 emails sent]
```

**Rule for chains:** Each agent in the chain only knows its own task. The chain's logic is controlled by an **orchestrator** (separate agent or config). The orchestrator:
- Starts the next agent when the previous one is done
- Passes the right data between steps
- Handles errors: if Agent B fails → notify admin, stop the chain

### 1.5 Error Handling

| Error | Behavior |
|-----|----------|
| API timeout (5s) | Retry 2 times, then log + notify |
| LLM timeout | Retry 1 time with shorter prompt, then fail |
| Validation error (output doesn't match schema) | Retry with clearer instructions, then fail |
| Rate limit (429) | Wait + exponential backoff, max 3 retries |
| Permanent error (401, 403, 500) | Fail immediately. Log. Notify. |

All errors are written to the log with `run_id` + `error_code` + `traceback`. Dashboard shows red status.

### 1.6 Orchestrator (Chain Control)

The orchestrator is a **dedicated orchestrator agent** (not a config file). It:

- Receives a pipeline definition (JSON): `{"steps": [{"agent": "A", "input_from": "trigger"}, {"agent": "B", "input_from": "step_0"}]}`
- Triggers the next agent immediately when the previous one is done
- **Partial failure:** If Agent B fails → orchestrator flags the step as failed, notifies admin, and waits for decision: retry, skip, or stop the entire chain
- All orchestrator decisions are logged with their own run_id
- Pipelines can have max 5 steps. If needed → split into sub-pipelines

**Implementation:** The orchestrator is a generic agent that reads the pipeline definition and calls the target agents' APIs. No custom code per pipeline.

**The orchestrator's prompt lives in `skills/delivery/`** — it is internal, not the customer's.

### 1.7 Flow Documentation per Customer

Each customer gets a flow map in [[obsidian/04_clients]] showing:
- Which agents exist
- How they are triggered
- Which chains exist
- Dependencies between agents

**Deliverable:** `{customer_name}_FLOW.md` in the customer's folder. Generated by [[ca-agent-builder]] after audit.

---

## 2. Agent Improvement — self + by each other

This is our major competitive advantage. Agents that get better without us writing new prompts every week.

### 2.1 Feedback Loop (Self-improvement)

After each agent run:

```
RUN → LOG → ANALYSIS → SUGGESTION → (APPROVE) → UPDATED PROMPT
```

| Step | Description | Done by |
|------|-------------|---------|
| **LOG** | All steps logged: input, output, tool calls, time, errors | The system |
| **ANALYSIS** | An analysis agent reviews the log. Questions: Did the output have the right format? Did the agent find the right data? Were there unnecessary steps? Did it take too long? | `<ca-agent-reviewer>` (new skill) |
| **SUGGESTION** | The analysis generates a proposed prompt update | `<ca-agent-reviewer>` |
| **APPROVE** | Human (William/Alpedal) approves or rejects the suggestion | Dashboard notification + button |
| **UPDATE** | The prompt is updated, version is bumped | The system |

**Definition of `ca-agent-reviewer`:**
- Purpose: Analyze agent logs and propose prompt improvements
- Input: Log (run_id, input, output, tool calls, time, errors)
- Output: Suggestion for prompt change or "No improvement needed"
- Prompt: "You review an AI agent's run log. Compare output against expected format. Find patterns in errors. Propose a maximum of 3 prompt changes. Each suggestion must be specific (exact text to add/change) and have a justification."
- Lives in `skills/delivery/` — internal skill, not the customer's

**Versioning:** Every prompt change is saved with version. `tools.yaml` is also versioned — every tool change (new API, changed endpoint, new auth method) is bumped separately.

```
agents/deployed/{customer}/{agent}/
├── prompts/
│   ├── v1.0.0.md   ← original prompt
│   ├── v1.1.0.md   ← first prompt improvement
│   └── current.md  ← active prompt (alias to latest approved)
├── tools/
│   ├── v1.0.0.yaml ← original tools
│   ├── v1.1.0.yaml ← tool change (new endpoint)
│   └── current.yaml← active tools (alias)
└── config/
    └── current.yaml ← active config (customer-specific, not versioned)
```

**Frequency:** Analysis runs every night for agents that have run ≥5 times that day. If no errors → no change.

### 2.2 Cross-agent Review (Improvement by Each Other)

Different agents for different customers review each other's logs anonymously.

```
Agent A (Customer 1): "Handle invoices"
Agent B (Customer 2): "Handle invoices" (similar task, different customer)

Agent A's log → anonymized (remove customer data, keep structure)
             → sent to Agent B
             → "Would you have done differently? Anything I'm missing?"
             → The response is logged as an improvement suggestion
```

**Rules for cross-review:**
- **No customer data is shared.** Only prompt structure, error patterns, approach
- The agent never sees which customer it concerns
- **Anonymization:** Before the log is sent to another agent, an LLM pass runs that scrubs: all email addresses → `[EMAIL]`, personal names → `[NAME]`, company names → `[COMPANY]`, personal ID numbers → `[PNR]`. This is a **mandatory** part of the cross-review flow, not an option.
- Suggestions go into a queue that William/Alpedal approves
- Same agent type (e.g. "invoice processing") compared first
- Different agent types compared when they have ≥10 runs each

**Requires:** `<ca-cross-review>` skill that handles anonymization and matching.

### 2.3 Pattern Library (YAML)

Over time we collect patterns from all customers. Each pattern is stored as YAML blocks, not free text:

```yaml
- type: timeout
  trigger: "Fortnox API returning 408/504"
  agent_type: "invoice-processing"
  fix: "Add retry logic: 3 attempts with exponential backoff, 2s/4s/8s"
  source: "cross-review (customer A + customer B)"
  added: "2026-07-01"
  status: active

- type: output-format
  trigger: "VAT amount missing on export invoices"
  agent_type: "invoice-processing"
  fix: "Add explicit instruction: 'Always include VAT breakdown per line item'"
  source: "feedback-loop (customer A)"
  added: "2026-07-15"
  status: active
```

This makes the library queryable. When a new agent is built → search on `agent_type` to load relevant patterns from the start.

**Deliverable:** `obsidian/05_ops/AGENT_PATTERNS.md` — living document, updated after each interesting observation. Format: YAML block per pattern. `status: active | deprecated | archived`.

### 2.5 The Self-improvement Loop (the system gets smarter over time)

This ties everything together — the loop that makes EVERY NEW CUSTOMER start smarter than the previous one.

```
deployed-agent runs
  → logged
  → ca-agent-reviewer analyzes
  → prompt improvement approved
  → deployed-agent updated (v1.1.0)
  → IS THE IMPROVEMENT GENERIC? (applies to the agent type, not customer-specific)
    → YES: ca-agent-reviewer flags template update
      → William approves
      → agents/templates/{agent_type}/prompt.md updated
      → template version bumped (v1.0.0 → v1.1.0)
      → NEXT CUSTOMER with same agent type starts at v1.1.0
    → NO: stays in deployed-agent's version history
```

**Rule:** At least 2 different customers must have the same improvement before it is moved to templates.
**Owner:** William approves template bumps. ca-agent-reviewer flags.

### 2.6 Improvement Pipeline (Summary)

```
On each agent run:
  → Log (automatic)
  → Analyze if ≥5 runs today (nightly job)
  → Generate prompt suggestion if improvement exists
  → Send to William/Alpedal for approval
  
Each week:
  → Cross-review: match similar agents between customers
  → Update AGENT_PATTERNS.md with new insights

Each month:
  → Review all prompt versions. Are there agents that have never improved?
  → Has the pattern library grown? Are there new reusable skills to create?
```

### 2.7 Cost Guard — Max Cost per Run

Each agent gets a `max_cost_per_run` in config.yaml. If the cost is exceeded:

| Step | Event |
|------|----------|
| **Check** | Before each LLM call: have we reached max_cost? |
| **Threshold 80%** | Logs warning |
| **Threshold 100%** | Aborts run, returns "Aborted — cost limit reached" |
| **Notification** | Sent to admin: "{agent} exceeded max_cost {amount}" |

This prevents a malfunctioning agent in a loop from costing hundreds of kronor.
Cost guard is P1 — implemented in API Gateway, requires no UI.
```

---

## 3. Cyber Security — built-in from the start

Security cannot be added afterwards. It affects architecture, hosting choices, and how we build each agent.

### 3.1 Data Classification

All data passing through the system is classified:

| Level | Example | Requirement |
|------|---------|------|
| **Public** | Marketing materials, case studies | None |
| **Internal** | Agent configuration, prompt versions | Access via login |
| **Sensitive** | Customer invoices, email, process flows | Encrypted at rest+transit, tenant-isolated |
| **Critical** | Personal ID numbers, login credentials, API keys | Encrypted, never in prompt, access logged |

**Rule:** Lowest possible level always. If data is not needed for the agent's task → don't ingest it.

### 3.2 Tenant Isolation

Each customer is its own **tenant**. No tenant can see another's data.

```
API Gateway
├── Tenant A (acme)
│   ├── Agents (isolated)
│   ├── Data (own schema or DB prefix)
│   └── Logs (own namespace)
├── Tenant B (beta)
│   ├── Agents
│   ├── Data
│   └── Logs
└── Admin (us)
    ├── See all tenants (overview, no raw data)
    ├── Manage prompts, deployment
    └── Operations monitoring
```

**Implementation:**
- Each tenant has a unique tenant_id in every API call
- Database uses tenant_id as partition key
- Dashboard session bound to one tenant
- Only admin role can switch tenant

### 3.3 API Key Management

No API keys ever in prompts or source code.

| Storage Method | Where | Access |
|---------------|-----|---------|
| Encrypted configuration | Vault / encrypted file | Only agent's runtime |
| Environment variables | CI/CD + deployment | Only deployment pipeline |
| Never in prompt | — | Prompt references secrets by name |

**Flow:** Agent calls `tools.yaml` → runtime looks up key in encrypted store → calls API → key never visible in prompt or log.

### 3.4 Logging and Audit Trail

All actions are logged:

| Event | Logged | Stored |
|----------|--------|--------|
| Agent run started | run_id, agent, tenant, trigger, time | Log database |
| Each tool call | run_id, tool, status, time, response size | Log database |
| Error | run_id, error_code, message, traceback | Log database |
| Dashboard login | user, time, IP, tenant | Separate auth logs |
| Prompt change | user, agent, version from→to, time | Separate audit logs |
| User button press | user, agent, run_id, time | Log database |

**Requirements for audit trail (GDPR):**
- Must be able to list ALL actions a specific user has performed
- Must be exportable per tenant
- Logs are not deleted — archived (cold storage after 90 days)

### 3.5 GDPR

| Requirement | Solution |
|------|---------|
| **Right to be forgotten** | tenant-level delete: remove all logs, configs, prompts for a tenant |
| **Data portability** | Export tenant data as JSON |
| **Data processing agreement** | Signed with customer before audit (see [[ONBOARDING]]) |
| **Personal data in prompt** | Forbidden. Prompt specifies only roles, not names/personal ID numbers |
| **Storage within EU** | VPS/hosting within EU. No data-sensitive cloud services outside EU |

**William = interim DPO** (according to [[MASTER_PLAN_FINAL]]).

### 3.6 Hosting and Data Storage

| Requirement | Solution |
|------|---------|
| **EU storage** | All customer data stored within EU. Backend on EU-based VPS (Hetzner/Hydrogen). |
| **Vercel** | Used ONLY for frontend (static pages + client-side fetch). No Server Actions, no API Routes that call backend with customer data. All communication with agents/logs goes directly from browser to our VPS. |
| **GDPR-safe** | Backend API on own VPS. Database on same VPS or separate EU-based DB. |
| **Traffic** | Dashboard ↔ API Gateway within EU. No data leaves EU. |

If the first customer requires 99.9% guarantee → SLA data collection (uptime metrics) starts from day 1 in API Gateway, even if SLA UI is built later (P4). Data not collected from the start cannot be recreated.

### 3.7 Log Cleaning (GDPR)

| Type | Retention | Action after |
|-----|-------------|---------------|
| Agent logs (run_id, tools, errors) | 90 days | Archived to cold storage |
| Auth logs (login, IP) | 180 days | Deleted |
| PII in logs (email, personal ID) | 90 days | Anonymized (automatic LLM pass) |
| Prompt versions | Forever | Retained (no PII) |

**Automated purging:** A cron job runs every night and:
1. Marks logs older than 90 days for archiving
2. Anonymizes PII in logs older than 90 days but needed for analysis
3. Deletes auth logs older than 180 days

### 3.8 Access Control (Dashboard)

| Role | Permissions |
|------|-------------|
| **Super Admin** (William) | All tenants, deployment, prompt changes, logs |
| **Admin** (Alpedal) | All tenants, read-only on prompts, view logs |
| **Customer-admin** | Their tenant: see all agents, trigger manually, see history |
| **Customer-operator** | Their tenant: trigger preselected agents, see their history |
| **Customer-viewer** | Their tenant: see status, no trigger |

---

## 4. Dashboard — features and build order

Today's [[DASHBOARD_SPEC]] describes an MVP. Here is the full feature list in the order they should be built.

### 4.1 Build Order (Prioritized)

| Prio | Feature | Build Time | Dependency |
|------|----------|---------------|----------|
| **P1** | Agent list + status indicators | 1 day | API Gateway |
| **P1** | Manual trigger ("Run now" button) | 1 day | API Gateway |
| **P1** | Run history (last 20) | 1 day | Log database |
| **P1** | Login (email + password) | 2 days | Auth system |
| **P1** | Empty state (onboarding view) — first customer sees instructions, not empty page | 0.5 day | — |
| **P1 (backend)** | SLA data collection (uptime metrics) — logged from day 1, UI later | 1 day | API Gateway |
| **P2** | Agent detail view (logs, status, config) | 2 days | API Gateway |
| **P2** | Tenant Admin (create tenant, invite users) | 2 days | Multi-tenant |
| **P2** | Role management (admin/operator/viewer) | 1 day | Auth system |
| **P2** | Error notifications (red status, email notification) | 2 days | Webhook/email |
| **P3** | Agent configuration via dashboard (edit prompt) | 3 days | Versioning |
| **P3** | Improvement suggestion interface (approve/reject) | 2 days | Feedback loop |
| **P3** | Cost analysis per agent (per run, per day) | 2 days | Log data |
| **P4** | White-label (Enterprise) | 3 days | Tenant-config |
| **P4** | SLA dashboard (uptime, response times, uptime %) | 2 days | Monitoring |
| **P4** | Webhooks for custom integrations | 3 days | API Gateway |

### 4.2 Tech Stack (Finalized)

According to [[MASTER_PLAN_FINAL]]:

| Layer | Tech | Reason |
|-------|--------|-----------|
| Frontend | Next.js + Tailwind CSS | Fast development, large community |
| Backend | Node.js Express (REST) | Same language as frontend, easy to deploy |
| Database | PostgreSQL (or Supabase) | Relational, JSON support, good for logs |
| Hosting frontend | Vercel | Free for MVP, easy deployment |
| Hosting backend | VPS of choice (Hetzner/Hydrogen) | Full control, EU-based, GDPR-safe |
| Agent runtime | Hermes (all bots) | Same system we use ourselves |

### 4.3 Dashboard Design Principles

| Principle | Description |
|---------|-------------|
| **1. Status visible immediately** | Eyes see green/red without reading |
| **2. One button per agent** | Customer just presses "Run". No settings |
| **3. History is self-explanatory** | Table: time, status, result. No interpretation |
| **4. Errors are impossible to miss** | Red background, not just red text |
| **5. Mobile first** | Everything works on phone (customers' daily life) |
| **6. Bone White** | #E3E3E4 base. NEVER white (#FFFFFF) |

### 4.4 Dashboard Screens (Complete)

Beyond the MVP screens in [[DASHBOARD_SPEC]]:

**Tenant Admin ($tenant/admin):**
- List users + roles
- Invite new user
- Agent configuration (choose trigger, schedule, pause/activate)

**Agent Config ($tenant/agents/{id}/config):**
- Edit prompt (textarea, versioned)
- Choose trigger (manual/cron/webhook)
- Test run (run with dummy input)
- View latest logs

**Improvement Flow ($admin/improvements):**
- List of unconfirmed prompt suggestions (agent → human)
- Show diff: current prompt → proposed
- Approve / reject / edit manually

**Analytics ($tenant/analytics):**
- Number of runs per day/week/month
- Success rate per agent
- Average run time
- Cost per agent (API calls, LLM tokens)

---

## 5. Website — lead capture and case studies

Built after dashboard MVP. Content written by [[hermes|Hermes]].

### 5.1 Pages

| Page | Purpose | Priority |
|------|-------|-----------|
| **Landing** | Value proposition + CTA | P1 |
| **Services** | Audit → Build → Operate | P1 |
| **Pricing** | Tiers + deduction clause | P2 |
| **Case studies** | (created after first customer) | P2 |
| **Contact** | Lead capture form | P1 |
| **Blog** | SEO, thought leadership | P3 |

### 5.2 Lead Capture (P1)

Form on website:
- Name, company, email, phone
- "What is your biggest IT challenge?" (textarea)
- Sent to William via email + logged in 
- Auto-response: "Thanks, we'll get back to you within 24h"

**Flow:** Form → Webhook → William email + obsidian/04_clients/_active/ new lead file

### 5.3 Case Study Structure (when we have first customer)

| Section | Content |
|---------|----------|
| **Headline** | "How {company} saves {X}h/week with AI agents" |
| **The Challenge** | 2-3 sentences about their IT stress |
| **The Solution** | Which agents were built? What do they do? |
| **The Result** | Hours/month saved, errors reduced, money |
| **Tech** | Brief: Hermes, dashboard, integrations |
| **Quote** | From the customer |

### 5.4 SEO Strategy

Keywords Swedish SME companies search for (according to [[MARKET]]):
- "AI agent automation"
- "automate IT flows"
- "build AI agents"
- "Fortnox automation" (non-existent keyword = low competition)
- "Google Workspace automation"
- "AI for accounting firm"

Each keyword → a blog post. Published after website.

---

## Build Order (Summarized)

```
Week 1-2:
  [Hermes] Build test client in obsidian/04_clients/_active/
  [Hermes] Build ca-agent-reviewer + ca-cross-review skills
  [Hermes] Write website content + SEO articles
  > **Note:** ca-agent-reviewer is built now but cannot be tested until Week 3+ when logs exist. That's OK — implementation first, testing later.

Week 2-3:
  [William] API Gateway (Express, auth, multi-tenant, cost guard, SLA metrics)
  [William] Dashboard P1: agent list, trigger, history, login, empty state
  [Hermes] AGENT_PATTERNS.md + security documentation
  [All] **Dogfood starts** — a simple internal agent (mail-sort) runs on our own platform

Week 3-4:
  [William] Dashboard P2: tenant admin, roles, notifications
  [William + Hermes] First test client's agents built on our own platform

Week 4-5:
  [William] Dashboard P3: agent config (UI), improvement suggestions (UI)
  [Hermes] Build ca-orchestrator (chain control)

Week 5-6:
  [William] Website P1: landing, services, contact
  [William] Dashboard P4: cost analysis
  [All] Continued dogfood + fix bugs revealed
```

---

## Comments

- 2026-06-24 | hermes: Created. Based on conversation with William about system build before sales.
- 2026-06-24 | antigravity: Reviewed. [10 points + ideas — see comments below]
- 2026-06-24 | hermes: Updated after bot review — specified orchestrator (1.5), retry-state (1.3), dry-run (1.2), ca-agent-reviewer definition (2.1), tools versioning (2.1), cross-review anonymization (2.2), patterns YAML (2.3), self-improvement loop (2.5), cost guard (2.7), hosting/GDPR (3.6), log cleaning (3.7), dashboard empty state + SLA data (4.1), adjusted timeline + dogfood earlier (build order).
  1. CRITICAL: Orchestrator (ch 1.3) lacks implementation. "Separate agent or config" is unspecified. What triggers the orchestrator? How does it handle partial failure mid-chain? Blocks Week 1.
  2. CRITICAL: `ca-agent-reviewer` (ch 2.1) should analyze logs but the agent's own prompt doesn't exist. Chicken-and-egg. Must be defined before Week 1 is complete.
  3. Cross-review anonymization (ch 2.2) underspecified. "Remove customer data" is not an algorithm. Embedded customer info in free text? Needed: LLM pass that reviews log before cross-review is sent. GDPR risk until this is solved.
  4. Agent lifecycle (ch 1.2) lacks RETRY_STATE. A run that is retried should keep the same `run_id` with sub-index (e.g. `run_id.attempt=2`). Otherwise the log becomes untraceable.
  5. `tools.yaml` is not versioned (ch 2.1). Prompt versions exist but tool changes aren't visible in audit trail. Add same version bumping for tools.
  6. Dashboard P1 (ch 4.1) lacks empty state. First customer sees empty agent list. Needed: onboarding state with instructions.
  7. The Week 3-4 timeline is unrealistic: Elb gets 9-11 days of work in 5-7 days (Dashboard P2 + Website P1 in parallel). Move website to Week 5-6.
- 2026-06-24 | antigravity: IDEAS missing from the plan:
  A. Dogfood earlier: run own agents on own platform from Week 2, not Week 4. Bugs found 2 weeks earlier.
  B. Cost guard P1 (backend, no UI): set `max_cost_per_run` in agent-config from the start. A malfunctioning agent in a loop can cost hundreds of kronor without this.
  C. `AGENT_PATTERNS.md` should be YAML blocks (type/trigger/fix/source) not free markdown. Queryable when library grows to 50+ patterns.
  D. SLA data collection (uptime metrics) should be P1-backend even if SLA UI is P4. If the first customer requires 99.9% guarantee it's too late to start collecting data then.
- 2026-06-24 | antigravity: THE SELF-IMPROVEMENT SYSTEM (missing as explicit loop in both plans): deployed-agent improves → approved → if generic → updates agents/templates/ → next customer starts smarter. Today, individual customers' agents improve. What we want: the system as a whole improves — each new customer starts at a higher baseline than the previous one. That connection must be owned by someone (suggestion: ca-agent-reviewer + William approves template bumps).
- 2026-06-24 | antigravity: Additional review of architecture and GDPR:
  8. GDPR/Hosting: Vercel can route traffic outside EU. If we handle sensitive customer data, EU-specific hosting or Next.js hosted on our own VPS is required for full regulatory compliance.
  9. Local sandbox: Development and testing needs a "Dry-run" mode in Agent Lifecycle to avoid sending real email or calling live Fortnox APIs during tests.
  10. Log cleaning (GDPR): Automated purging or anonymization of raw data (PII) in the log database after 90 days must be defined in the data classification.
- 2026-06-25 | hermes: Translated to English per new language policy.
