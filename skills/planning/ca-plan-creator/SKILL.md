---
name: ca-plan-creator
description: Creates plans using PLAN_TEMPLATE.md. Ensures correct frontmatter and tags.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-plan-creator

## Syfte

Skapar nya planeringsdokument med hjälp av mallen `PLAN_TEMPLATE.md` och validerar struktur och metadata vid skapandet.

## Instruktioner för skapande

1. **Läs in mallen:** Använd innehållet i [[PLAN_TEMPLATE]] (`OBSIDIAN/_TEMPLATES/PLAN_TEMPLATE.md`) som bas för det nya dokumentet.
2. **Definiera obligatorisk frontmatter:**
   - Fyll i `title` med en kort beskrivande rubrik.
   - Sätt `date` till dagens datum (format YYYY-MM-DD).
   - Sätt `author` till namnet på den agent/person som skapar planen.
   - Sätt `status: draft`.
3. **Fyll i taggar enligt [[_RULES]] §2:**
   - Varje plan måste innehålla taggar i formatet `tags: [area/PLAN, status/DRAFT, author/*, type/PLAN]` där författaren (`author/*`) anpassas.
4. **Strukturera sektioner:** Fyll i Mål, Bakgrund, Steg-för-steg, Tidslinje, Resurser och Risker.
5. **Skapa kommentarssektion:** Lägg till en `## Kommentarer`-sektion allra sist i dokumentet med formatet `- YYYY-MM-DD | author: skapad`.
6. **Placering:** Spara filen i katalogen `OBSIDIAN/01_PLAN/` (enligt reglerna i [[ca-file-organizer]]).
