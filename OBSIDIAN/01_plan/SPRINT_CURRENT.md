---
title: "SPRINT 01 — First Blood"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/APPROVED, author/HERMES, type/PLAN]
status: approved
---

# SPRINT 01 — "First Blood"

> Period: 2026-06-26 — 2026-06-28

---

## Var vi är
- styde.ai har 0 rader produktionskod och 130+ designdokument.
- Denna sprint fokuserar vi på att bygga det absolut minsta som krävs för att möjliggöra sälj och sätta upp vår gemensamma utvecklingsmiljö.

---

## Uppgifter (max 3)
1. **[ ] William:** Bygg Consultant Agent v0.1 (Python CLI som tar en URL och genererar en YAML-rapport).
2. **[ ] Alpedal:** Skriv 3 initiala agent-blueprints (`invoice-reviewer`, `customer-service-triage`, `mail-sorter`).
3. **[ ] William:** Sätt upp den gemensamma fysiska servern (Ubuntu Server + SSH-nycklar + Node.js + PostgreSQL).

---

## Kriterier för klar
- Utförande av `python konsult.py https://[företag].se` genererar en korrekt och välformaterad YAML-rapport på terminalen och sparas till fil.
- 3 blueprint-mappar existerar i `/agent-blueprints/` med filerna `persona.md`, `blueprint.yaml` och `tools.yaml`.
- Både William och Alpedal kan logga in via SSH på servern utan lösenord och köra `git pull`.

---

## Blockeringar
Inga. Sätt igång direkt.

---

## Backlog / Idéer (INTE denna sprint)
- Dashboard i Next.js
- Evaluerings-pipeline (Forge)
- Publik hemsida/landningssida

---

## Comments
- 2026-06-25 | hermes: Sprint 01 upprättad i samband med total reboot.
