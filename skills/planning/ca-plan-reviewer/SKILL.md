---
name: ca-plan-reviewer
description: Reviews plans. Checks frontmatter, tags, folder, comments, placeholders.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-plan-reviewer

## Syfte

Granskar planeringsdokument mot uppsatta repo-regler och säkerställer kvaliteten före implementering påbörjas.

## Checklista vid granskning

1. **Frontmatter OK?**
   - Innehåller title, date, author, tags och status?
2. **Taggar rätt?**
   - Följer de strukturen `[area/*, status/*, author/*, type/*]` enligt [[_RULES]]?
3. **Mapp rätt?**
   - Är filen sparad i rätt underkatalog enligt [[ca-file-organizer]]?
4. **Kommentarssektion finns?**
   - Finns sektionen `## Kommentarer` allra längst ner i dokumentet?
5. **Inga placeholders?**
   - Finns det några textstycken innehållande tillfälliga markeringar som "TBD", "TODO", "implement later" eller liknande?

## Agerande vid resultat

### Om granskningen misslyckas (avvikelser hittas)
- Skriv en kommentar under `## Kommentarer`-sektionen i dokumentet med specifik feedback om vad som behöver åtgärdas.
- Sätt dokumentets status till `status: draft`.

### Om granskningen lyckas (inga avvikelser)
- Uppdatera dokumentets status till `status: review` (och tagg till `status/REVIEW`).
- Logga godkännandet i kommentarerna: `- YYYY-MM-DD | author: granskad och godkänd för review`.
