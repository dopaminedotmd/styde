---
name: ca-audit-reporter
description: Writes audit reports using AUDIT_TEMPLATE.md. Structured, clear, actionable.
version: 1.0.0
owner: alpedal
last-updated: 2026-06-24
---

# ca-audit-reporter

## Syfte

Skriva strukturerade, tydliga och handlingskraftiga audit-rapporter baserat på den data som samlats in av [[ca-audit-agent]].

## Instruktioner för rapportskrivning

1. **Läs in mallen:** Använd innehållet i `OBSIDIAN/04_CLIENTS/TEMPLATES/AUDIT_TEMPLATE.md` som grundmall.
2. **Definiera frontmatter:**
   - Titel: `Audit-rapport — {Kundens namn}`
   - Tags: `[area/KLIENT, status/REVIEW, author/ALPEDAL, type/REPORT]`
   - Status: `review`
3. **Fyll i sektionerna:**
   - **Sammanfattning:** Skriv 2-3 meningar som sammanfattar kundens utmaningar, smärtpunkter och automationspotential.
   - **Företagsinfo:** Fyll i tabellen med företagets namn, bransch, antal anställda, IT-ansvarig, nuvarande system och uppskattad månadskostnad för IT.
   - **System:** Lista systemen, deras ändamål, antal användare och om de är automatiserbara.
   - **Kartlagda flöden:** Beskriv varje identifierat flöde i detalj (trigger, steg, system, tid, smärta).
   - **Opportunities:** Fyll i tabellen med prioriteringsordning, ROI-klassificering, komplexitet och uppskattad byggtid.
   - **Rekommendation:** Beskriv tydligt vilka 2-3 agenter som bör byggas först.
4. **Format:**
   - Använd standardiserad Obsidian-syntax (callouts, wikilinks).
   - Lägg till wikilinks till relevanta personprofiler (t.ex. [[william]], [[alpedal]]) och till den blivande offerten (`OFFERT_{KUNDNAMN}.md`).
5. **Utdata:**
   - Spara den färdiga rapporten till: `OBSIDIAN/04_CLIENTS/_ACTIVE/{kundnamn}_AUDIT.md`.
