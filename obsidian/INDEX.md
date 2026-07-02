---
title: "INDEX — Planeringshubben för styde.ai"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/APPROVED, author/HERMES, type/PLAN]
status: approved
---

# INDEX — Planeringshubben för styde.ai

> [!note] Planeringshubben
> Välkommen till hjärtat av styde.ai. Här finns all vår planering, affärsstrategi och systemarkitektur samlad.
> Varje bot som ansluter måste läsa [[_RULES]] först.

---

## Huvuddokument

- [[MASTER_PLAN]] — Vår gemensamma, gällande huvudplan för styde.ai.
- [[_RULES]] — Regler för namngivning, format, taggar och kodning. LÄS FÖRST.

---

## Katalogstruktur och Filer

| Sökväg / Fil | Beskrivning | Ansvarig |
|-------------|-------------|-----------|
| [[_RULES]] | Regler för dokument, format och samarbeten | Alla |
| `_users/` | Användarprofiler för teamet | Alla |
| `_templates/` | Mallar för planer, möten och audits | Alla |
| `_skills/` | Obsidian-specifika färdigheter för botar | Alla |
| `00_strategy/` | Affärsstrategi, paketering och prissättning | William |
| - [[BUSINESS_CONCEPT]] | Affärsidé och koncept | William |
| - [[MARKET]] | Marknadsanalys och målgrupp | William |
| - [[OFFER]] | Tjänstepaket (Audit, Build, Operate) | William |
| - [[PRICING_MODEL]] | Prissättningsmodell och avtalsnivåer | William |
| `01_plan/` | Projektets faser och löpande sprintar | Hermes |
| - [[MASTER_PLAN]] | Huvudplanen för samtliga faser | Hermes |
| - [[SPRINT_CURRENT]] | Pågående sprint, uppgifter och delmål | Hermes |
| - [[SPRINT_LOG]] | Loggbok över slutförda sprintar | Hermes |
| `02_architecture/` | Systemdesign och infrastruktur | William + Hermes |
| - [[SYSTEM_OVERVIEW]] | Övergripande systemarkitektur | William |
| - [[SERVER_SETUP]] | Konfiguration av vår gemensamma fysiska server | William |
| - [[DASHBOARD_SPEC]] | Gemensam specifikation för Next.js-dashboarden | William |
| - [[AGENT_FRAMEWORK]] | Specifikation för agenter och blueprints | William |
| `03_forge/` | Referensmaterial och källkodsskisser (Styde Forge) | Alpedal |
| - [[README]] | Syfte och översikt för referensbiblioteket | Alpedal |
| `04_clients/` | Kundarbeten, mallar och historik | Alla |
| - [[AUDIT_TEMPLATE]] | Mall för audit-rapportering | Alpedal |
| - [[OFFERT_TEMPLATE]] | Mall för formella offerter | William |
| `05_ops/` | Drift, rutiner och dagliga loggar | William + Hermes |
| - [[ONBOARDING]] | Steg-för-steg-guide för kundonboarding | William |
| - [[SUBSCRIPTION_TIERS]] | Driftspaket och abonnemangsnivåer | William |
| - [[BOT_PROMPTS]] | Färdiga prompter för Hermes och övriga botar | Hermes |
| - [[AGENT_PATTERNS]] | Kodningsmönster och återanvändbara lösningar | Alpedal |
| - `audits/` | Genomförda audits på företag | Alpedal |
| - `logs/` | Dagliga ändringsloggar (`YYYY-MM-DD.md`) | Hermes |
| `99_references/` | Inspiration, länkar och forskning | Alla |

---

## För nyanlända botar och medlemmar

1. Läs `.agents/AGENTS.md` som pekar hit.
2. Läs [[_RULES]] för att förstå formaterings- och säkerhetsreglerna.
3. Läs din användarprofil under `_users/` för att förstå din roll.
4. Läs [[MASTER_PLAN]] för att se var vi är i faserna.
5. Läs [[SPRINT_CURRENT]] för att börja arbeta på aktiva uppgifter.

---

## Comments
- 2026-06-25 | hermes: Omskriven efter total reboot. Rensat ut gamla dokumentreferenser, uppdaterat kataloger och lagt till de nya sprint- och serverfilerna.
