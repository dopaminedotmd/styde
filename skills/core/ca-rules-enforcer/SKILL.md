---
name: ca-rules-enforcer
description: Flaggar för överträdelser av repo-regler (fel mapp, fel frontmatter, saknade kommentarer). Loggar avvikelser och lägger till kommentarer under ## Kommentarer utan att blockera körningen. Körs före granskning.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-rules-enforcer

## Syfte

Flaggar för överträdelser av uppsatta repo-regler. Den blockerar inte utförandet, utan loggar avvikelser och kommenterar.

## Kontroller som utförs

1. **Fel mapp:** Kontrollerar om dokument har lagts i en katalog som inte matchar dess dokumenttyp (enligt [[ca-file-organizer]]).
2. **Fel frontmatter:** Validerar att YAML frontmatter innehåller alla obligatoriska fält baserat på filtyp:
   - För dokument i `OBSIDIAN/`: `title`, `date`, `author`, `tags`, `status` (enligt [[_RULES]]).
   - För skills i `skills/`: `name`, `description`, `version`, `owner`, `last-updated` (enligt [[_README]] under `skills/`).
3. **Fel taggar:** Verifierar att taggar följer det definierade systemet (`[area/*, status/*, author/*, type/*]`) enligt [[_RULES]] (gäller endast dokument i `OBSIDIAN/`).
4. **Saknad kommentarssektion:** Kontrollerar att filen har en `## Kommentarer`-sektion längst ner.

## Agerande vid regelöverträdelse

- Skriv en kommentar under `## Kommentarer`-sektionen i det aktuella dokumentet med specifik beskrivning av regelfelet.
- Notifiera ägaren (t.ex. William eller Hermes) genom att logga avvikelsen tydligt i botens körrapport.
- **Blockera INTE:** Agenten tillåts fortsätta sitt arbete även om det innehåller regelfel. Granskningen och blockeringen sker i `ca-plan-reviewer`-steget.

## Kommentarer

- 2026-06-25 | hermes: Uppdaterade beskrivningen till svenska, bumpade version till 1.1.0, justerade frontmatter-validering för att stödja skills separat samt lade till kommentarssektion.

