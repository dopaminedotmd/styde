---
title: "FULL SYSTEM AUDIT — styde.ai (Opus)"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/DRAFT, author/HERMES, type/REPORT]
status: draft
---

# Full System Audit — styde.ai

> Opus audit. 30+ documents read. 0 lines of code. 0 customers.
> Brutally honest. English. Short.

---

## 1. STATE OF THE UNION

**What styde.ai is today:** A meticulously documented hypothesis. 130+ design documents across 3 systems. 12 internal skills (all markdown instructions). 37 external skills installed. 0 lines of production code. 0 customers. 0 revenue.

**Strengths:**
- Business concept is sharp. Audit → Build → Operate is a proven model.
- Documentation discipline is exceptional. Frontmatter, tags, comments — all consistent.
- The skill system works. Progressive loading, ca-prefix convention, clear ownership.
- Security thinking is ahead of where it needs to be (good — GDPR matters for Swedish SMEs).
- Self-improvement loop (Forge eval → template upgrade → next customer starts smarter) is the real moat if built.

**Weaknesses:**
- Planning paralysis. 6 plans with overlapping scope. MASTER_PLAN_FINAL has 33 tasks, 0 checked. IMPLEMENTATION_PHASE_1 exists but isn't approved. BUILD_PHASE_2 is 587 lines with 0 checkboxes.
- Over-documentation. The ratio of docs-to-code is infinite. You have more design documents for Forge alone (86) than most startups have total files. 
- No sales activity. ROADMAP says "20 outreach/day" — not started.
- William's hardware (GTX 980 Ti, 4GB VRAM) can't run anything Alpedal designed. The Forge RAG spec assumes 10GB VRAM minimum.
- ROADMAP marks "Dashboard MVP" and "first system delivered" as done ([x]). They're not. 0 code exists.

**Score: 3/10.**
Thinking is 8/10. Execution is 0/10. Average: the thinking doesn't ship.

---

## 2. ARCHITECTURE COHERENCE — Three Dashboards

Three dashboards spec'd:

| Dashboard | Spec | Tech | Users | Status |
|-----------|------|------|-------|--------|
| **Customer Dashboard** | DASHBOARD_SPEC.md | Next.js + Tailwind | Customer staff | Wireframes only |
| **Admin Dashboard** | BUILD_PHASE_2 §4 | Next.js + Tailwind | William + Alpedal | Feature list only |
| **StydeForge Desktop** | 35 docs in styde-forge-dashboard/ | Tauri v2 + Rust | Alpedal only | Design complete, 0 code |

**Are they correctly separated?** Partially.

- Customer + Admin dashboards share a backend (API Gateway + PostgreSQL). Correct separation: same codebase, different auth roles. DASHBOARD_SPEC.md conflates them — the audit from Hermes caught this.
- StydeForge Desktop is a completely separate application for a completely different purpose (local agent refinery control). It should NOT share any code with styde.ai dashboards. This separation is correct.

**Conflicts:**
- FORGE_INTEGRATION.md says "Admin Dashboard must pull data from BOTH sources" (API Gateway + Forge health API). This creates a runtime dependency on Alpedal's local desktop app — which may be off, disconnected, or unbuilt. Bad coupling.
- IMPLEMENTATION_PHASE_1 §1D specs a THIRD internal dashboard (test audit runner + wardrobe browser) that overlaps with Admin Dashboard. Unnecessary — fold into Admin Dashboard.
- No shared component library or design system between Customer and Admin dashboards. Will lead to inconsistency.

**Verdict:** Merge Customer + Admin into one Next.js app with role-based views. Keep StydeForge Desktop separate. Kill the Phase 1D mini-dashboard — it's the Admin Dashboard.

---

## 3. FORGE AS RAG ENGINE

FORGE_INTEGRATION.md positions Styde Forge as styde.ai's intelligence backend. Alpedal specified: FAISS + all-MiniLM-L6-v2, 512-token chunks, top-3 retrieval, ~90% token reduction with Caveman Ultra.

**Does the architecture hold?**

The *concepts* hold. RAG for agent context injection is sound. Eval pipeline with composite scoring (self 30% + judge 50% + consensus 20%) is well-designed. Teacher Agent feedback loop is the core IP.

The *implementation* doesn't hold:
- **FAISS runs locally.** Alpedal designs for his RTX 3080 (10GB VRAM). William has a GTX 980 Ti (4GB). FAISS flat index with all-MiniLM-L6-v2 needs ~1GB VRAM. William's card can technically run it — but barely, and alongside nothing else.
- **Pinecone migration is feasible** and straightforward. Same chunking, same embedding model (hosted), same top-k retrieval. Cost: ~$70/month for the free tier → paid tier. This is the right move for cloud.
- **Over-engineered for where you are?** Yes. Massively. You have 0 agents, 0 customers, 0 blueprints in production. The RAG layer is solving a problem you don't have yet. A flat markdown file with 10 industry patterns (as IMPLEMENTATION_PHASE_1 §1A.1 step 4 already suggests) is sufficient for months.
- **The 90% token reduction claim is misleading.** Caveman Ultra reduces output tokens by ~70% (verified in skill spec). RAG reduces input context by ~67%. These are different axes — you don't multiply them. Real reduction: ~70% on input context (RAG), ~70% on output (Caveman). Still excellent. But "90%" is marketing math.

**Verdict:** Sound concepts, premature implementation. Use a markdown file for patterns now. Add Pinecone when you have ≥3 customers generating real data. Skip FAISS entirely — it's a local optimization for hardware you don't have.

---

## 4. BUILD PRIORITY

IMPLEMENTATION_PHASE_1 proposes:
```
1A.1 Consultant Agent (crawl → classify → diagnostics) — 4 days
1A.2 Agent Wardrobe (3 blueprints) — 2 days
1B   Architect Agent (match → generate prompt → proposal) — 4 days
1C   Security (data isolation) — 3 days parallel
1D   Dashboard (test audit + wardrobe) — 3 days
Total: ~12 working days
```

**Challenge:**

The order is almost right. But security (1C) on day 1 is premature — you have 0 customers and 0 data to isolate. And 12 working days is optimistic for William building solo. Realistic: 3-4 weeks.

**Can Alpedal's Tauri build run in parallel?**

No. Wrong question. Alpedal's desktop app serves ONE user (Alpedal) and enables ZERO revenue. William's Consultant Agent enables the first sale. These are not parallel priorities — they compete for the same limited attention.

**Shortest path to revenue:**

```
Week 1-2:  Consultant Agent (Python CLI: URL → crawl → LLM classify → YAML report)
           THIS generates the first demo you can show prospects.
Week 2-3:  Manual audit + manual proposal (no Architect Agent needed — William writes it)
Week 3-4:  First sales outreach (20/day) using Consultant Agent output as proof
Week 4-6:  Land audit. Conduct audit. Write proposal. Get paid.
Week 6-8:  Build first customer's agents. Deliver.
Week 8+:   THEN build dashboard. THEN Agent Wardrobe. THEN Architect Agent.
```

The Architect Agent is elegant but unnecessary. William can match audit → blueprints manually for the first 5 customers. Automation before you have a process to automate is premature.

---

## 5. ALPEDAL'S CONTRIBUTION

**What he delivered:** 86 design documents across 3 systems:
- Styde Forge v3.0: 51 docs (14 sections, 6 blueprints, eval pipeline, Teacher Agent, RAG, hardware profiles)
- StydeForge Dashboard: 35 docs (10 sections, Tauri app spec, chat tools, provider system)
- Phase 1 Roadmap: 1 doc (50 features catalogued)

**Quality:** Exceptional. Design-decision log with alternatives + rationale. Component interfaces as contracts. Data models as YAML schemas. Circuit breaker patterns. This is senior-level systems design.

**But:** 0 code. 0 lines. Every document is prose and pseudocode.

**Is 6 weeks for Tauri realistic?**

The Phase 0→1 transition doc estimates 23 days for P0 MVP. That's ~5 weeks full-time. For someone who:
- Has never written Rust
- Has never used Tauri
- Has 0 shipped applications
- Is described as "fairly new to AI" and "needs structure and guides initially"

No. 6 weeks is not realistic. 12-16 weeks is more likely, and the result would still need significant polish.

**Optimal role going forward:**

Alpedal's superpower is systems thinking and pattern recognition. His optimal role is NOT coding a Tauri app. It's:

1. **Audit delivery partner.** His pattern-recognition ability + structured thinking = perfect for customer audits. This generates revenue.
2. **Blueprint designer.** The Forge blueprint format he designed IS the Agent Wardrobe format. He should write the first 5 blueprints (customer-service-triage, invoice-reviewer, mail-sorter, report-writer, calendar-assistant) as structured markdown — not code.
3. **Quality reviewer.** Use his eval pipeline thinking to review William's agent output quality.

Stop the Tauri build. Redirect to revenue-generating activities.

---

## 6. RISK ASSESSMENT — Top 3 Nobody Mentioned

**Risk 1: Hardware mismatch kills Forge integration.**

Alpedal designs for RTX 3080 (10GB) + RTX 3070 Ti (8GB) = 18GB VRAM, 32GB DDR5 RAM. William has GTX 980 Ti (4GB VRAM). Forge's RAG layer, embedding model, and hardware adaptation layer are all specced for hardware William doesn't own. Cloud migration (Pinecone) solves this — but nobody has acknowledged that William literally cannot run the system Alpedal designed. If Forge stays USB-based, William can never test it.

**Risk 2: Two people, three systems, zero customers = entropy.**

William building styde.ai platform (Next.js). Alpedal designing Forge (USB/Tauri). Both also maintaining 130+ design documents. Every hour spent on system 2 or 3 is an hour NOT spent on getting the first customer. The trap: it feels productive to design. It's not. You're building inventory for a store with no customers and no location.

**Risk 3: The Consultant Agent is a commodity.**

The test audit (crawl website → LLM classify → report) is a 50-line Python script anyone can build in a day. There's no moat here. The moat is supposed to be the self-improving agent system (Forge eval → better agents over time). But that requires RUNNING agents for REAL customers generating REAL logs. Without customers, the self-improvement loop never starts, and the commodity Consultant Agent is all you have.

---

## 7. DASHBOARD MVP — Which One First?

**Not StydeForge Desktop.** Serves one user. Enables 0 revenue. Alpedal can control Forge via CLI.

**Not Admin Dashboard.** You have 0 customers. Nothing to administer. Build when you have ≥2 customers.

**Not even Customer Dashboard** (as first priority). Build the Consultant Agent first. Deliver a PDF report manually. The dashboard is what you show AFTER the customer pays for Build.

**The right first dashboard:** A simple internal tool for William.

```
1 page. Next.js.
- Input: company URL
- Output: test audit report (from Consultant Agent)
- Button: "Run audit"
- Display: last 10 audits with results

That's it. No auth. No multi-tenant. No roles. No Agent Wardrobe UI.
Deploy on Vercel. Use it for demos. Takes 2 days after Consultant Agent works.
```

Build the Customer Dashboard (DASHBOARD_SPEC.md) only when the first customer signs. Build the Admin Dashboard only when you have ≥2 paying customers.

---

## 8. SINGLE RECOMMENDATION

**Stop designing. Start selling.**

The Consultant Agent is a weekend project. Build it in Python. Run it on 5 test company websites. Take the output, put it in a PDF. Start doing 20 cold outreach per day. Use the test audit report as your sales hook: "We ran our AI on your website. Here's what we found. Want to discuss?"

Everything else — Forge, dashboards, eval pipelines, RAG engines, Tauri apps, Teacher Agents, Architect Agents, Bayesian weight optimization — is procrastination until you have a customer who pays money.

You have a well-designed car on paper. Nobody has turned the ignition key. Turn it.

---

## Summary Scorecard

| Dimension | Score |
|-----------|-------|
| Vision & business concept | 8/10 |
| Documentation quality | 9/10 |
| Architecture coherence | 5/10 (three overlapping dashboard specs) |
| Execution (code) | 0/10 |
| Revenue & customers | 0/10 |
| Team utilization | 3/10 (Alpedal designing, not delivering) |
| Planning clarity | 4/10 (6 overlapping plans) |
| Risk awareness | 6/10 (good on GDPR, blind on hardware + priorities) |
| **Overall** | **3/10** |

---

## Comments

- 2026-06-25 | Antigravity (Opus): Full system audit. 30+ documents read across all 8 steps. Scoring reflects reality: exceptional thinking, zero execution. The single biggest risk is continuing to plan instead of building and selling.
