---
name: ca-onboarding-lead
description: Guidar kunden steg-för-steg genom onboarding-processen, från kickoff och dashboard-setup till agent-deployment, utbildning och go-live. Används under kundens onboardingfas.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-onboarding-lead

## Purpose

Guides the customer step-by-step through the onboarding process, from signed contract to deployed dashboard with active AI agents.

## Steps in the Onboarding Process

### Step 1: Kickoff Meeting
- **Description:** Book a kickoff meeting with the customer to align expectations and detailed timeline.
- **Responsible:** [[william|William]]
- **Deliverable:** Booked kickoff meeting and finalized agenda.
- **Completion Checklist:**
  - [ ] Meeting date and time agreed upon.
  - [ ] Agenda (e.g., according to `AGENDA_TEMPLATE.md`) sent.

### Step 2: Dashboard Setup
- **Description:** Create a tenant in the dashboard and configure the correct subscription tier (Basic, Pro, or Enterprise) based on the contract. Follow design standards in [[DASHBOARD_SPEC]].
- **Responsible:** [[william|William]]
- **Deliverable:** Customer's dashboard tenant created and colors/logo configured.
- **Completion Checklist:**
  - [ ] Tenant created in the Next.js dashboard.
  - [ ] Customer's logo and any custom colors uploaded (see [[SUBSCRIPTION_TIERS]]).

### Step 3: Agent Deployment
- **Description:** Build and deploy the customer's AI agents based on opportunities identified in the [[ca-audit-agent]] step. Follow the standards in [[ca-agent-builder]].
- **Responsible:** [[william|William]]
- **Deliverable:** AI agents deployed in the production environment.
- **Completion Checklist:**
  - [ ] prompts.md, tools.yaml, config.yaml created for each agent.
  - [ ] Tests conducted in dev with `tests/input.json`.
  - [ ] Agents integrated with API Gateway according to [[SYSTEM_OVERVIEW]].

### Step 4: Training
- **Description:** Conduct a 2-hour training session digitally or on-site with the customer's staff to show how to use the dashboard.
- **Responsible:** [[william|William]] (training) & [[alpedal|Alpedal]] (support)
- **Deliverable:** Training session completed and documentation handed over.
- **Completion Checklist:**
  - [ ] Training meeting conducted.
  - [ ] Staff know how to press start buttons and read logs (according to [[DASHBOARD_SPEC]]).

### Step 5: Go-Live
- **Description:** Deploy the system live. Monitor system performance for the first 48 hours and have Alpedal do daily check-ins with the customer during the first week.
- **Responsible:** [[william|William]] (monitoring) & [[alpedal|Alpedal]] (check-ins)
- **Deliverable:** System is live with daily contact during week 1.
- **Completion Checklist:**
  - [ ] No critical system errors in the backend during 48h.
  - [ ] Alpedal has conducted five daily check-ins.

### Step 6: Transition to Ongoing Operations (Operate)
- **Description:** Transition to the ongoing support agreement. Schedule recurring monthly meetings and activate SLA monitoring.
- **Responsible:** [[william|William]]
- **Deliverable:** Ongoing management process started.
- **Completion Checklist:**
  - [ ] First monthly meeting booked (see [[SUBSCRIPTION_TIERS]]).
  - [ ] Customer support channels established and tested.

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
