---
title: "Design för styde.ai dashboard-prototyp"
date: 2026-06-25
author: hermes
tags: [area/ARKITEKTUR, status/APPROVED, author/HERMES, type/SPEC]
status: approved
---

# Design för styde.ai dashboard-prototyp

> Detta dokument beskriver den tekniska och visuella designen för frontend-prototypen av styde.ai. Följer specifikationen i _william/DASHBOARD_SPEC.md med revideringar godkända av William gällande ljus/mörkt läge, kornig abstrakt bakgrund, lyxig spring-animation och skjutbara paneler.

## 1. Teknisk setup & Mappstruktur

### Stack för prototyp
* **Ramverk:** Next.js 14 (App Router)
* **Styling:** Tailwind CSS v4
* **Ikoner:** Lucide React + anpassade SVG:er för agenter och Slack
* **Animationer:** Framer Motion (för den filmiska inloggningen, flikar och skjutbara paneler)
* **Placering:** `apps/dashboard/`

### Projektstruktur i apps/dashboard
* `app/login/page.tsx` — Inloggningsskärmen med kornig abstrakt bakgrund och inloggningskort.
* `app/(dashboard)/layout.tsx` — Dashboard-layout med svävande sidebar-navigationskolumn, gap-marginaler och Apple-stil på paneler.
* `app/(dashboard)/page.tsx` — Centrala chatten (Command Center) med flytande chattbox, flik-menyer och en skjutbar agentpanel.
* `app/(dashboard)/agents/page.tsx` — Agent-översikt med lyxiga geometriska SVG-ikoner och statusindikatorer.
* `app/(dashboard)/integrations/page.tsx` — Integrationsöversikt.
* `app/(dashboard)/reports/page.tsx` — Rapportlista och viewer med strikt tidskriftstypografi.
* `components/` — Modulära komponenter för chat, login, sidebar och statusar.

## 2. Visuell Design & Animationer (Login till Dashboard)

### Dynamiskt Färg- och Temasystem (Ljust & Mörkt läge)
Temat styrs via klassen `.dark` på `html`-taggen. CSS-variabler i `globals.css` uppdateras automatiskt:
* **Mörkt läge (Standard):** Bakgrund `#0A0B0E`, ytor `#141519`, text `#F0EDE8`.
* **Ljust läge:** Bakgrund `#F3F4F6`, ytor `#FFFFFF`, text `#111827`.
* **Accentfärger (Monokrom lyx):**
  * Primär: `#A98C6D` (Dämpad lyxig brons/varm sand).
  * Hover: `#C3A27D` (Ljusare sandton).
  * Kanter: `rgba(255,255,255,0.07)` (mörkt) och `rgba(0,0,0,0.06)` (ljust).

### Stilren inloggningsskärm (Fold 1)
* **Bakgrund:** Kornig (grainy) och mjukt oskarp (blurred) gradient i nyanser av violett, lila, djup indigo och kolsvart.
* **Kort:** Innehåller enbart det nödvändiga inmatningsfältet för e-post (en rundad kapsel `rounded-full`) samt inloggningsknappen märkt med texten "Login" (`rounded-full`).
* **Varumärke:** Texten `"styde"` i stor Playfair Display (`italic text-4xl md:text-5xl`) placeras uppe till vänster. Inget annat brus.

### Trög och lyxig scrollövergång (Login → Chat)
* **Animation:** Triggad av Framer Motion `spring`-övergång för att ge en tung, premium känsla med en svag, elegant studs vid dockning:
  `transition={{ type: "spring", stiffness: 18, damping: 12, mass: 2.2 }}`

## 3. Interaktivitet & Funktioner (Chatt & Dashboard)

### Svävande Sidebar & Gömbar Navigeringspanel
* **Primär bar (Ikon-bar):** Svävar fritt på vänsterkanten (`rounded-2xl`, marginaler från kant) och innehåller endast ikoner.
* **Sekundär panel:** Innehåller dokumentträd och användarprofil. Kan döljas helt av användaren för att ge en distraktionsfri arbetsyta. Den visas inte per automatik under alla flikar för att hålla chatten helt ren.

### Agent-rad ovanför chatten (ersätter drawer)
* **Medarbetarstatus:** Agenter visas som en horisontell **rad av kort direkt ovanför chatt-canvas** — inte i en dold sidopanel. Varje kort har geometrisk SVG-ikon, agentnamn och statuspunkt (`●` aktiv / `○` idle).
* **Interaktion:** Klick på ett agent-kort startar eller återupptar en dedikerad chatttråd med den agenten. Aktiv agent markeras tydligt (tjockare kant eller accentfärg).
* **Detaljvy:** Den tidigare skjutbara drawern från höger kant är borttagen. Vid behov av detaljvy för en agent öppnas en modal istället.
* **Flera agenter:** Vid 5+ agenter scrollas raden horisontellt (fast enradig layout).

### Flytande Chattbox & Flik-menyer
* **Full bredd, dominant:** Chatt-canvas fyller hela bredden under agent-raden — en stor kritvit yta (`rounded-3xl`) som dominerar dashboarden. Den tidigare gråskalebilden bredvid är borttagen (flyttad till login).
* **Inputfält:** Chatt-input är lyft från botten (`bottom-6`) och flyter i en centrerad glassmorphism-låda (`max-w-2xl mx-auto rounded-3xl`) inuti den stora canvasen.
* **Flikar:** Knappar för `"Plan"` och `"Kör"` samt val av modell (`"Hermes Pro"`) fästs direkt ovanpå chattboxen.
* **Geometriska Ikoner:** Vi skapar rena, stilrena geometriska SVG-ikoner för alla agenter (används både i agent-raden och i chatten) för att ersätta standard-emojis.

### Typografilyft i Rapporter
* **Rapportvy:** Vi formaterar rapportläsaren med strikt typografi:
  * Titlar och rubriker i Playfair Display (Serif, kursiv, med generösa avstånd).
  * Brödtext i Inter med ökat radavstånd (`leading-relaxed`).
  * Tabeller och kodblock får extra tunna, stilrena kanter och rundade hörn.

## Comments
- 2026-06-25 | hermes: Design-dokument för dashboard-prototypen skapat och godkänt av William.
- 2026-06-25 | hermes: Uppdaterat designen med ljus/mörkt läge, dämpad bronsaccent, kornig gradientbakgrund, spring-övergång och skjutbara paneler.
