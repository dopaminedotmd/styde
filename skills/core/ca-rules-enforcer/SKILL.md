---
name: ca-rules-enforcer
description: Flags rule violations. Does NOT block. Logs + comments.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-rules-enforcer

## Syfte

Flaggar för överträdelser av uppsatta repo-regler. Den blockerar inte utförandet, utan loggar avvikelser och kommenterar.

## Kontroller som utförs

1. **Fel mapp:** Kontrollerar om dokument har lagts i en katalog som inte matchar dess dokumenttyp (enligt [[ca-file-organizer]]).
2. **Fel frontmatter:** Validerar att YAML frontmatter innehåller alla obligatoriska fält (title, date, author, tags, status).
3. **Fel taggar:** Verifierar att taggar följer det definierade systemet (`[area/*, status/*, author/*, type/*]`) enligt [[_RULES]].
4. **Saknad kommentarssektion:** Kontrollerar att filen har en `## Kommentarer`-sektion längst ner.

## Agerande vid regelöverträdelse

- Skriv en kommentar under `## Kommentarer`-sektionen i det aktuella dokumentet med specifik beskrivning av regelfelet.
- Notifiera ägaren (t.ex. William eller Hermes) genom att logga avvikelsen tydligt i botens körrapport.
- **Blockera INTE:** Agenten tillåts fortsätta sitt arbete även om det innehåller regelfel. Granskningen och blockeringen sker i `ca-plan-reviewer`-steget.
