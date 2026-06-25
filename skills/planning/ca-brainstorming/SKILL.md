---
name: ca-brainstorming
description: Måste användas före all form av kodning, projekt-scaffolding eller implementation. Tvingar fram design-first och mini-spec som ska godkännas av William innan kod skrivs. Använd alltid denna skill när en ny uppgift eller ändring ska påbörjas.
version: 2.1.0
owner: william
last-updated: 2026-06-25
---

# ca-brainstorming — Design Before Code (v2.0)

> Upgraded from obra/superpowers brainstorming (S-rank). See `.agents/skills/brainstorming/SKILL.md` for the original.

Enforces design-first before implementation. Every project, regardless of size, goes through this process.

<HARD-GATE>
Do NOT write code, do NOT scaffold any project, do NOT invoke any implementation skill until a design has been presented and approved by William. This applies to ALL work, no matter how simple it seems.
</HARD-GATE>

## Anti-Pattern: "This is too simple to need design"

Everything goes through this process. A todo list, an env file, a config change — everything. "Simple" things are where untested assumptions cause the most waste. The design can be short (a few sentences), but you MUST present it and get approval.

## Workflow (9 Steps)

Execute in order. Create one task per step.

1. **Explore project context** — read files, docs, latest commits
2. **Offer visual companion just-in-time** — only when a question would TRULY be clearer visually. Not upfront.
3. **Ask clarifying questions** — one at a time. Understand purpose, constraints, success criteria
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
5. **Present design** — in sections, get approval after each section
6. **Write design document** — save to `obsidian/01_plan/{YYYY-MM-DD}-{topic}-design.md`
7. **Spec self-review** — check placeholders, contradictions, ambiguity, scope
8. **William reviews spec** — ask William to read the spec before implementation
9. **Transition to implementation** — invoke `ca-plan-creator` to create implementation plan

## Key Principles

- **One question at a time** — never overwhelm with multiple questions at once
- **Propose alternatives** — always 2-3 approaches
- **YAGNI** — remove unnecessary features from all designs
- **Incremental validation** — present, get approval, move forward
- **Be flexible** — go back and clarify when something doesn't make sense

## Spec Self-Review (After Written Spec)

1. **Placeholder scan:** Any "TBD", "TODO", incomplete sections? Fix them.
2. **Internal consistency:** Do sections contradict each other? Does the architecture match the feature descriptions?
3. **Scope check:** Focused enough for an implementation plan, or does it need breakdown?
4. **Ambiguity check:** Can any requirement be interpreted two ways? Choose one and make it explicit.

Fix inline. No new review needed.

## Design for Isolation and Clarity

- Break the system into smaller units, each with a clear purpose
- Each unit should be understandable and testable independently
- Can someone understand what a unit does without reading its internal code? Can you change the implementation without breaking users? If not — the boundaries are wrong.

## After Design

William reviews the spec → approves → `ca-plan-creator` creates the implementation plan.

## Comments

- 2026-06-25 | hermes: Updated description to more proactive Swedish, bumped version to 2.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
