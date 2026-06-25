---
name: ca-onboarding-lead
description: Guidar kunden steg-för-steg genom onboarding-processen, från kickoff och dashboard-setup till agent-deployment, utbildning och go-live. Används under kundens onboardingfas.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-onboarding-lead

## Syfte

Guidar kunden steg-för-steg genom onboarding-processen, från signerat kontrakt till driftsatt dashboard med aktiva AI-agenter.

## Steg i Onboarding-processen

### Steg 1: Kickoff-möte
- **Beskrivning:** Boka kickoff-möte med kunden för att stämma av förväntningar och detaljerad tidslinje.
- **Ansvarig:** [[william|William]]
- **Leverabel:** Bokat kickoff-möte och spikad agenda.
- **Checklista för klart:**
  - [ ] Mötets datum och tid är överenskommet.
  - [ ] Agendan (t.ex. enligt `AGENDA_TEMPLATE.md`) är skickad.

### Steg 2: Dashboard Setup
- **Beskrivning:** Skapa en tenant i dashboarden och konfigurera rätt prenumerationsnivå (Basic, Pro, eller Enterprise) baserat på kontraktet. Följ design-standarder i [[DASHBOARD_SPEC]].
- **Ansvarig:** [[william|William]]
- **Leverabel:** Kundens dashboard-tenant är skapad och färger/logotyp är konfigurerade.
- **Checklista för klart:**
  - [ ] Tenant skapad i Next.js-dashboarden.
  - [ ] Kundens logotyp och eventuella anpassade färger upplagda (se [[SUBSCRIPTION_TIERS]]).

### Steg 3: Agent-deployment
- **Beskrivning:** Bygg och driftsätt kundens AI-agenter baserat på opportunities som identifierats i [[ca-audit-agent]]-steget. Följ standarderna i [[ca-agent-builder]].
- **Ansvarig:** [[william|William]]
- **Leverabel:** AI-agenter driftsatta i produktionsmiljö.
- **Checklista för klart:**
  - [ ] prompts.md, tools.yaml, config.yaml skapade för varje agent.
  - [ ] Tester genomförda i dev med `tests/input.json`.
  - [ ] Agenter integrerade med API Gateway enligt [[SYSTEM_OVERVIEW]].

### Steg 4: Utbildning
- **Beskrivning:** Genomför en 2 timmars utbildning digitalt eller på plats med kundens personal för att visa hur de använder dashboarden.
- **Ansvarig:** [[william|William]] (utbildning) & [[alpedal|Alpedal]] (support)
- **Leverabel:** Utbildningstillfälle genomfört och dokumentation överlämnad.
- **Checklista för klart:**
  - [ ] Utbildningsmötet är genomfört.
  - [ ] Personalen vet hur man trycker på startknappar och läser loggar (enligt [[DASHBOARD_SPEC]]).

### Steg 5: Go-live
- **Beskrivning:** Driftsätt systemet skarpt. Övervaka systemprestanda de första 48 timmarna och låt Alpedal göra dagliga check-ins med kunden under första veckan.
- **Ansvarig:** [[william|William]] (övervakning) & [[alpedal|Alpedal]] (check-ins)
- **Leverabel:** Systemet är i skarp drift med daglig kontakt under vecka 1.
- **Checklista för klart:**
  - [ ] Inga kritiska systemfel i backend under 48h.
  - [ ] Alpedal har genomfört fem dagliga avstämningar.

### Steg 6: Övergång till löpande drift (Operate)
- **Beskrivning:** Övergå till löpande supportavtal. Boka in återkommande månadsmöten och aktivera SLA-bevakning.
- **Ansvarig:** [[william|William]]
- **Leverabel:** Löpande förvaltningsprocess är startad.
- **Checklista för klart:**
  - [ ] Första månadsmötet är inbokat (se [[SUBSCRIPTION_TIERS]]).
  - [ ] Kundsupportkanaler är etablerade och testade.

## Kommentarer

- 2026-06-25 | hermes: Uppdaterade beskrivningen till svenska, bumpade version till 1.1.0 och lade till kommentarssektion.

