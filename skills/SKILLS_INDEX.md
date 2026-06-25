---
title: "SKILLS_INDEX — Index över skills i styde"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# Skills Index — styde

| Skill | Kategori | Owner | Version | Beskrivning |
|-------|----------|-------|---------|-------------|
| [[ca-brainstorming\|ca-brainstorming]] | planning | william | 2.1.0 | Måste användas före all form av kodning, projekt-scaffolding eller implementation. Tvingar fram design-first och mini-spec som ska godkännas av William innan kod skrivs. |
| [[skill-creator\|skill-creator]] | external | anthropic | 1.0.0 | Create, modify and improve skills with eval-driven iteration and benchmarking. S-rank. |
| [[brainstorming\|brainstorming]] | external | obra | 1.0.0 | 9-step design-before-code process with visual companion, spec-review and HARD-GATE. S-rank. |
| [[ca-file-organizer\|ca-file-organizer]] | core | william | 1.1.0 | Styr var nya filer ska placeras och kontrollerar namngivningskonventioner (stora bokstäver med understreck) och katalogdjup (max 3 nivåer). |
| [[ca-folder-organizer\|ca-folder-organizer]] | core | william | 1.1.0 | Hanterar katalogstrukturen i repot och förhindrar att odefinierade mappar skapas. |
| [[ca-rules-enforcer\|ca-rules-enforcer]] | core | william | 1.1.0 | Flaggar för överträdelser av repo-regler (fel mapp, fel frontmatter, saknade kommentarer). Loggar avvikelser och lägger till kommentarer under ## Kommentarer. |
| [[ca-plan-creator\|ca-plan-creator]] | planning | william | 1.1.0 | Skapar nya implementationsplaner utifrån PLAN_TEMPLATE.md. Säkerställer korrekt frontmatter, taggar och struktur i OBSIDIAN/01_PLAN/. |
| [[ca-plan-reviewer\|ca-plan-reviewer]] | planning | william | 1.1.0 | Granskar planeringsdokument mot repo-regler och checklista före implementering. Validerar frontmatter, taggar och kommentarssektion. |
| [[ca-agent-builder\|ca-agent-builder]] | delivery | william | 1.1.0 | Standard och mall för att bygga och driftsätta AI-agent-system åt kunder (prompt.md, tools.yaml, config.yaml). |
| [[ca-audit-agent\|ca-audit-agent]] | delivery | alpedal | 1.1.0 | Genomför kundaudits för att kartlägga IT-flöden, system, kostnader och identifiera automationsmöjligheter. |
| [[ca-audit-reporter\|ca-audit-reporter]] | delivery | alpedal | 1.1.0 | Skriver strukturerade och handlingskraftiga audit-rapporter i OBSIDIAN/04_CLIENTS/_ACTIVE/ utifrån AUDIT_TEMPLATE.md. |
| [[ca-offert-writer\|ca-offert-writer]] | delivery | william | 1.1.0 | Skapar formella offerter i OBSIDIAN/04_CLIENTS/_ACTIVE/ utifrån OFFERT_TEMPLATE.md. Följer prissättningsregler för Audit, Build och Operate (SLA-nivåer). |
| [[ca-onboarding-lead\|ca-onboarding-lead]] | delivery | william | 1.1.0 | Guidar kunden steg-för-steg genom onboarding-processen, från kickoff och dashboard-setup till agent-deployment, utbildning och go-live. |
| [[ca-change-logger\|ca-change-logger]] | core | william | 1.1.0 | Loggar alla ändringar i styde-repot. Uppdaterar dagens logg i OBSIDIAN/05_OPS/LOGS/ efter varje genomförd åtgärd. |

## Kommentarer

- 2026-06-25 | hermes: Lagt till frontmatter, uppdaterat alla skill-beskrivningar till svenska, bumpat versioner för de uppdaterade interna skillsen samt lagt till kommentarssektion.

