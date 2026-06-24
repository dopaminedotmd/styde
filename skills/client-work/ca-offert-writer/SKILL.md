---
name: ca-offert-writer
description: Generates client offers using OFFERT_TEMPLATE.md. Pricing, scope, terms.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-offert-writer

## Syfte

Skriva formella och strukturerade offerter baserat på audit-resultat och de prissättningsregler som slagits fast i [[MASTER_PLAN_FINAL]] och [[PRICING_MODEL]].

## Instruktioner för offertskrivning

1. **Läs in mallen:** Använd innehållet i `OBSIDIAN/04_CLIENTS/TEMPLATES/OFFERT_TEMPLATE.md` som grundmall.
2. **Definiera frontmatter:**
   - Titel: `Offert — {Kundens namn}`
   - Tags: `[area/KLIENT, status/REVIEW, author/WILLIAM, type/REPORT]`
   - Status: `review`
3. **Prissättningsregler (MASTER_PLAN_FINAL §4):**
   - **Audit:** Fast pris 19 900 kr.
   - **Build (Paket 2):** Från 99 000 kr upp till 300 000 kr (offereras baserat på antal agenter och komplexitet).
     - *Avräkningsklausul (Obligatorisk):* Vid köp av Build (Paket 2) inom 30 dagar dras kostnaden för Audit (19 900 kr) av från det totala Build-beloppet.
   - **Operate (Paket 3):** Löpande månadskostnad baserat på supportnivå (SLA):
     - **Basic:** 4 900 kr/mån (Mail-support, 24h svarstid vardagar).
     - **Pro:** 9 900 kr/mån (Mail + telefon, 8h svarstid vardagar).
     - **Enterprise:** 19 900 kr/mån (Priority support, 2h svarstid alla dagar).
4. **Skriv till fil:**
   - Spara offerten till: `OBSIDIAN/04_CLIENTS/_ACTIVE/{kundnamn}_OFFERT.md`.
5. **Format:**
   - Använd standardiserad Obsidian-syntax och wikilinks.
   - Lägg till en wikilink till den genomförda rapporten (`{kundnamn}_AUDIT.md`).
