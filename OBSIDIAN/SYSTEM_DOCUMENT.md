---
title: "styde — Systemöversikt"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/APPROVED, author/WILLIAM, type/SPEC]
status: approved
aliases:
  - System Document
  - Systemöversikt
---

# styde — Systemöversikt

> En komplett beskrivning av vad vi byggt, hur det fungerar, och hur du haka på.
> Skriven för Alpedal — men även som referens för William.
>
> *Senast uppdaterad: 24 juni 2026*

---

> [!important] Läs detta först
> Detta är inte ett färdigt system — det är en **hypotes under test**.
> Roller, priser och struktur är prototyp tills verkligheten säger annat.
> Allt kan och ska ifrågasättas.

---

## 1. Grundidén

Vi bygger **AI-agentsystem** åt svenska SME-företag.

Inte konsulttimmar. Inte ett engångsprojekt. Ett **produktiserat system**:

| Vad | Hur |
|-----|-----|
| Vi kliver in i ett företag | Genomför en strukturerad audit |
| Vi kartlägger deras IT-flöden | Identifierar bottlenecks och manuellt arbete |
| Vi bygger AI-agenter | Automatiserar det repetitiva |
| Vi levererar en dashboard | Personalen trycker på knappar — ingen kod krävs |
| Vi fakturerar månadsvis | Subscription — inte timmar |

Modellen är **audit → build → operate**. Kunden betalar för resultatet, inte för vår tid.

---

## 2. Vad vi har byggt

### Mappstrukturen

```
consulting.ai/
├── MASTER_PLAN_FINAL.md    ← Hela hypotesen nedskriven
├── OBSIDIAN/               ← All dokumentation (du är här)
│   ├── _RULES.md           ← Regler för alla bottar
│   ├── SYSTEM_DOCUMENT.md  ← Den här filen
│   ├── _USERS/             ← Onboarding-filer per person
│   └── _TEMPLATES/         ← Mallar för planer och rapporter
├── skills/                 ← 11 ca-skills (interna)
└── .agents/                ← Antigravitys system + externa skills
    ├── AGENTS.md           ← Pekar på _RULES.md
    ├── skills/             ← Externa skills (addyosmani + kepano)
    └── skills.json         ← Registrerar skills/-mappen
```

### De 11 interna skills (ca-prefix)

Dessa är **verktygen** som styr hur vår AI-agent (Hermes) beter sig. Varje skill är en instruktionsfil som aktiveras automatiskt vid rätt uppgift.

| Skill | Vad den gör | När den används |
|-------|-------------|-----------------|
| `ca-brainstorming` | Tvingar design-first innan bygge | Innan varje ny feature |
| `ca-file-organizer` | Styr var filer läggs | Vid alla filoperationer |
| `ca-folder-organizer` | Håller mappstruktur ren | Vid skapande av mappar |
| `ca-rules-enforcer` | Flaggar brott mot regler | Kontinuerligt |
| `ca-plan-creator` | Skapar planer enligt mall | Vid planering |
| `ca-plan-reviewer` | Granskar planer mot standard | Innan godkännande |
| `ca-agent-builder` | Mall för att bygga AI-agenter åt kunder | I byggfasen |
| `ca-audit-agent` | Genomför kundaudit strukturerat | Med ny kund |
| `ca-audit-reporter` | Skriver audit-rapporten | Efter audit |
| `ca-offert-writer` | Genererar offert från rapport | Direkt efter audit |
| `ca-onboarding-lead` | Guidar kunden från kontrakt till go-live | I driftsfasen |

### Externa skills installerade

Utöver våra egna skills har vi installerat externa paket:

- **addyosmani/agent-skills** — 24 skills för disciplin, kod-kvalitet, testning, review m.m.
- **kepano/obsidian-skills** — 5 skills för Obsidian-syntax och canvas

> [!tip] Hur skills fungerar
> En skill är en `.md`-fil med instruktioner. Antigravity läser den automatiskt när du ber om en uppgift som matchar. Du behöver inte säga "använd skill X" — det sker automatiskt.

---

## 3. Verktyget: Antigravity (Hermes)

Alla i teamet kör **samma setup** — det är beslutat och allas miljöer klarar det.

| Verktyg | Vad det är |
|---------|------------|
| **VS Code** | Editor — alla kör detta |
| **Antigravity** | VS Code-branch med inbyggd AI-agent (Google DeepMind) |
| **Hermes CLI** | Kommandoradsverktyg vid sidan om — för scripting och automation |

Antigravity + Hermes CLI kompletterar varandra: Antigravity för interaktivt arbete i editorn, Hermes CLI för körning utanför.

### Varför samma verktyg för alla?

|- **Skills är portabla** — en skill Alpedal skriver fungerar direkt för William
- **Dokumentformat är delat** — samma frontmatter, samma mappar, samma konventioner
- **Ingen "min bot gör X annorlunda"** — en gemensam standard

> [!note] Setup
> VS Code + Antigravity installeras som vanlig VS Code-branch. Hermes CLI installeras separat.
> Skills läses automatiskt från `.agents/`-mappen — inget manuellt konfigurationssteg krävs.

---

## 4. Hur du haka på

### Steg 1 — Klona repot

```bash
git clone [repo-url]
cd styde
```

### Steg 2 — Öppna i VS Code / Cursor

Antigravity aktiveras automatiskt. Skills laddas vid start.

### Steg 3 — Kör onboarding-prompten

Kopiera innehållet i [[PROMPT_ONBOARD_TEAM]] och klistra in det i din Antigravity-chatt.

Din bot gör sedan tre saker automatiskt:

1. **Läser hela systemet** — MASTER_PLAN_FINAL, denna fil, _RULES, alla skills
2. **Scannar din historik** — vilka projekt, verktyg, och erfarenheter du har
3. **Skriver en rapport** till `OBSIDIAN/_USERS/[ditt-namn].md`

William läser rapporten → vi diskuterar → roller spikas.

> [!warning] Viktig detalj
> Rapporten skrivs av **din** bot om **dig**. Det är avsiktligt.
> Din bot känner dina projekt, dina styrkor och dina blinda fläckar bättre än du gör.
> Lita på den.

---

## 5. Affärsmodell (hypotes)

```
AUDIT ──→ BUILD ──→ OPERATE
```

| Fas | Pris (prototyp) | Vad ingår |
|-----|-----------------|-----------|
| **Audit** | 19 900 kr | Kartläggning av IT-flöden + strukturerad rapport |
| **Build** | 99 000–300 000 kr | Agenter byggda + dashboard levererad |
| **Operate** | 4 900–19 900 kr/mån | Drift, updates, support, ny automatisering |

> [!caution] Dessa siffror är inte testade
> Ingen kund har betalat än. Priset justeras efter de första 5 leads.
> Ingen i teamet ska citera dessa siffror externt utan att stämma av med William.

---

## 6. Teamet (hypotes)

| Person | Tänkt roll | Bekräftad? |
|--------|-----------|------------|
| **William** | Founder · Builder · Allt | William bygger allt själv (beslutat 2026-06-24) |
| **Alpedal** | Solutions Architect · Audits | Hypotes — avgörs via onboarding |

Onboarding-rapporterna avgör rollerna. Inget är bestämt i förväg.

---

## 7. Beslut som gäller (kan omförhandlas)

| Beslut | Gäller tills... |
|--------|----------------|
| `skills/` på rotnivå | Någon har en konkret bättre struktur |
| `ca-`-prefix för skills | Det skapar förvirring |
| Alla kör VSCode + Antigravity + Hermes CLI | Allas setup klarar det — spikat |
| Next.js + Tailwind för dashboard | Beslutat — fastställt |
| William = GDPR-ansvarig | Annan person tar formellt ansvar |

> [!note] Hur du omförhandlar ett beslut
> Skriv ett förslag under `## Kommentarer` i relevant dokument med datum och author-tagg.
> Vi diskuterar — ingen ändrar utan konsensus.

---

## 8. Vad som återstår

Innan vi kan ta första kunden:

- [x] William bygger allt själv (beslutat 2026-06-24, se BUILD_PHASE_2)
- [ ] Kör [[PROMPT_ONBOARD_TEAM]] — få Alpedals onboarding-rapport
- [ ] Analysera rapporterna — justera roller och plan
- [ ] Land första kund — testa hela hypotesen mot verkligheten
- [ ] Iterera — allt är prototyp tills motsatsen bevisats

---

## Kommentarer

- 2026-06-24 | william: Grunddokumentet. Allt är prototyp. Alpedals rapport avgör nästa steg.
- 2026-06-24 | hermes: Omstrukturerat för onboarding — klarare steg, Obsidian-callouts, wikilinks.
- 2026-06-24 | william: Williams roll är också hypotes. Försäljning är inte spikat. Tech-setup (VSCode + Antigravity + Hermes CLI) är spikat — allas setup klarar det.
