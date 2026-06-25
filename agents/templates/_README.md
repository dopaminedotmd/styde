---
title: "_README — Agents Templates"
date: 2026-06-24
author: agy
tags: [area/OPS, status/APPROVED, author/AGY, type/TEMPLATE]
status: approved
---

# _README — Agents Templates

Detta är mallar för AI-agenter som vi levererar till kunder.

## Struktur

Varje template är en mapp med:
- `prompt.md` — Agentens system prompt. STERIL. Inga interna referenser.
- `tools.yaml` — API-verktyg agenten har tillgång till
- `config.yaml` — Mall för kundspecifik konfiguration
- `tests/` — input.json + expected.json för testning

## Regler

- Ingenting i templates/ refererar till Hermes, ca-skills, OBSIDIAN eller våra interna system
- Allt kundspecifikt (e-post, mapp-ID, max_cost) ligger i config.yaml, ALDRIG i prompt.md
- ca-agent-builder använder dessa mallar för att generera agents/deployed/{kund}/

## Användning

1. ca-agent-builder läser template för rätt agenttyp
2. Fyller i kundspecifik data från audit
3. Skriver till agents/deployed/{kund}/{agent}/
4. Skapar tests/input.json + expected.json från template
