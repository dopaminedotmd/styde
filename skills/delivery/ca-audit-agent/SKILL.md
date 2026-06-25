---
name: ca-audit-agent
description: Genomför kundaudits för att kartlägga IT-flöden, system, kostnader och identifiera automationsmöjligheter. Används för att samla in strukturerad data om kundens processer.
version: 1.1.0
owner: alpedal
last-updated: 2026-06-25
---

# ca-audit-agent

## Purpose

Conduct thorough customer audits to map IT flows, systems, and identify automation opportunities.

## Workflow

1. **Identify systems and services:**
   - Create a complete list of all SaaS services, local systems, and manual tools that the customer uses (e.g., Fortnox, Google Workspace, Excel).
   - Record costs and number of users per system.

2. **Map manual flows:**
   - Identify and document specific processes that take a lot of time.
   - For each flow, document:
     - **Trigger:** What starts the flow?
     - **Steps:** The exact steps that are performed.
     - **Systems:** Which systems are involved (e.g., Fortnox → Excel → Mail)?
     - **Time:** How many hours per week does the flow take?
     - **Pain:** What is the most inefficient or error-prone aspect of the flow?

3. **Prioritize opportunities:**
   - Evaluate each flow based on ROI (time/cost saved) against complexity (how hard it is to build).
   - Create a prioritized list (e.g., High ROI + Low complexity = Prio 1).

4. **Prepare report data:**
   - Structure all collected data so that it is ready to be consumed by `ca-audit-reporter`.

## Integration with ca-brainstorming

Before finalizing the prioritization, use [[ca-brainstorming]] to:
- Challenge assumptions about why the customer performs the flow in this way.
- Explore at least three different ways to automate or completely eliminate the steps.
- Ensure that the recommended agents solve the underlying problem, not just patch the symptoms.

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
