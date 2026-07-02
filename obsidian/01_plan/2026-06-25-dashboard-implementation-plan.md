---
title: "Plan: Dashboard-prototyp för styde.ai"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/APPROVED, author/HERMES, type/PLAN]
status: approved
---

# Plan: Dashboard-prototyp för styde.ai

> [!info] Beskrivning
> Denna plan beskriver stegen för att bygga en frontend-fokuserad Next.js 14-prototyp av styde.ai-dashboarden i apps/dashboard/ med kornig gradientbakgrund, lyxig spring-animation och skjutbara paneler för ljus- och mörkt läge.

## Mål

Skapa en fungerande, interaktiv frontend-prototyp av kundportalen för styde.ai enligt kraven i _william/DASHBOARD_SPEC.md med de senaste revideringarna:
* Kornig (grainy) och mjukt oskarp (blurred) lila/violett gradientbakgrund för inloggningsskärmen.
* Trög och lyxig spring-animation vid inloggning med en subtil, elegant studs.
* Stöd för ljus- och mörkt läge (Ljust läge: `#F3F4F6` bg, `#FFFFFF` yta, `#111827` text; Mörkt läge: `#0A0B0E` bg, `#141519` yta, `#F0EDE8` text).
* Dämpad monokrom brons/sand-accent (`#A98C6D`) istället för skarp orange.
* Dold sekundär navigeringspanel som kan togglas vid behov, samt medarbetarstatus placerad i en skjutbar sidopanel (drawer) från höger kant.
* Geometriska SVG-ikoner för AI-medarbetare.
* Strikt typografi i rapporter (Playfair Display + Inter).

## Bakgrund

Vi bygger en webbapplikation för styde.ai. För att snabbt validera det nya monokroma designspråket, den flytande chattboxen, den uppdaterade tröga spring-animationen och den korniga gradientbakgrunden, bygger vi en ren frontend-prototyp med mockad data och lokala tillstånd.

## Steg-för-steg

1. **Bakgrundsbild:** Generera den korniga, oskarpa lila gradientbilden via `generate_image` och spara som `public/login_background.png`.
2. **Setup & Global CSS:** Uppdatera färgvariabler i `globals.css` för att stödja automatisk växling mellan ljus- och mörkt läge. Lägg till bronsaccenten `#A98C6D` och ta bort den orangea accenten.
3. **Login (Fold 1):** Uppdatera login-sidan med den nya bakgrunden och implementera den tröga spring-övergången (stiffness: 18, damping: 12, mass: 2.2).
4. **Dubbel Gömbar Sidebar:** Justera `components/sidebar.tsx` så att navigeringspanelen (sekundära sidebaren) är stängd som standard eller kan togglas helt via ikon-baren till vänster.
5. **Skjutbar Agent-låda (Drawer):** Skapa den högra sidopanelen som en skjutbar drawer på `/`-sidan och lägg till en öppningsknapp i Topbar.
6. **Flytande Chattbox & Ikoner:** Implementera de nya geometriska SVG-ikonerna för agenter och integrera dem i chatten.
7. **Rapporter & Inställningar:** Uppdatera typografin i rapportläsaren samt lägg till switch-knappen för ljus/mörkt läge i Inställningar.
8. **Verifiering:** Provköra och säkerställa att allt fungerar perfekt.

## Tidslinje

| Steg | Deadline | Ansvarig |
|------|----------|----------|
| 1-3 (Bakgrund, Styling & Animation) | 2026-06-25 | hermes |
| 4-6 (Sidebar, Drawer & Ikoner) | 2026-06-25 | hermes |
| 7-8 (Subpages & Verifiering) | 2026-06-25 | hermes |

## Resurser

- [[_RULES]] — Bot-regler för styde
- [[2026-06-25-dashboard-design]] — Design för prototypen
- [DASHBOARD_SPEC.md](file:///c:/Users/William/styde.ai/_william/DASHBOARD_SPEC.md) — Produktspecifikation

## Risker

- Äldre webbläsare kan lagga med `backdrop-filter` och `spring`-övergångar samtidigt → Använda CSS `will-change: transform, opacity` för att säkerställa hög bildfrekvens.

## Comments

- 2026-06-25 | hermes: Plan skapad för prototyp-byggande av dashboarden.
- 2026-06-25 | hermes: Reviderad plan baserad på Williams återkoppling (långsammare scroll, rundare former, flytande chattbox och dubbel sidebar).
- 2026-06-25 | hermes: Ytterligare revidering för ljus/mörkt läge, bronsaccent, kornig bakgrund, spring-övergång och skjutbara paneler.
