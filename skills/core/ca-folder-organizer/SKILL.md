---
name: ca-folder-organizer
description: Manages folder structure. No folders outside defined ones.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-folder-organizer

## Syfte

Hanterar katalogstrukturen och förhindrar skapandet av oauktoriserade mappar.

## Regler

### 1. Inga odefinierade mappar
Skapa aldrig mappar utanför den definierade strukturen utan föregående teamkonsensus.

### 2. Skapa ny kategori
Om en ny kategori av dokument eller mappar behövs, måste en plan först skapas och godkännas i `01_PLAN/` (eller genom uppdatering av `ROADMAP.md`).

### 3. Ta inte bort tomma mappar
Ta aldrig bort tomma mappar i repot. De är fördefinierade och har ett specifikt syfte för framtida faser (t.ex. `03_PROTOTYPES/` eller `04_CLIENTS/_ACTIVE/`).

### 4. Tillåten katalogstruktur

```
consulting.ai/
│
├── .agents/
│   ├── AGENTS.md
│   ├── skills.json
│   └── skills/
│
├── skills/
│   ├── SKILLS_INDEX.md
│   ├── core/
│   ├── planning/
│   ├── building/
│   ├── client-work/
│   └── reusable/
│
└── OBSIDIAN/
    ├── _RULES.md
    ├── _SKILLS/
    ├── _PEOPLE/
    ├── 00_STRATEGY/
    ├── 01_PLAN/
    ├── 02_ARCHITECTURE/
    ├── 03_PROTOTYPES/
    ├── 04_CLIENTS/
    └── 05_OPS/
```
