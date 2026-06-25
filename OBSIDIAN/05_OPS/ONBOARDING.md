---
title: "Onboarding — Kundprocess"
date: 2026-06-24
author: william
tags: [area/OPS, status/APPROVED, author/WILLIAM, type/PLAN]
status: approved
---

# Onboarding — Kundprocess

> [!info] Process
> Steg-för-steg från första kontakt till live system.
> Senast uppdaterad: 2026-06-24

## Steg 1: Första kontakt

- Lead kommer in (LinkedIn, call, referens, hemsida) (se [[MARKET]])
- [[william|William]] bokar 30-min intro-möte
- Mål: Förstå deras situation. Är dom en kandidat för audit? (se [[OFFER]])
- Om ja → boka audit. Om nej → avsluta eller hänvisa.

## Steg 2: Audit (Paket 1)

- [[alpedal|Alpedal]] (+ [[william|William]] på första mötet) genomför audit
- Kartläggning: system, flöden, smärtpunkter
- 1-2 dagar (on-site eller distans)
- Delivery: audit-rapport + prioriteringslista (se [[AUDIT_TEMPLATE]])
- Presentera för kundens ledning
- Offert på Paket 2 (se [[OFFERT_TEMPLATE]])

## Steg 3: Implementation (Paket 2)

- [[william|William]]: kontrakt påskrivet (se [[PRICING_MODEL]])
- [[william|William]]: bygger agenter (se [[AGENT_FRAMEWORK]]) + dashboard (se [[DASHBOAD_SPEC]])
- [[alpedal|Alpedal]]: support, testning, kundkommunikation
- [[Hermes]]: projektledning, deadlines, uppföljning (se [[ROADMAP]])
- 2-4 veckor (beroende på komplexitet)
- Demo för kund → godkännande
- Deploy till produktion (se [[SYSTEM_OVERVIEW]])

## Steg 4: Go live

- 2h utbildning för kundens personal
- [[william|William]]: "här är eran dashboard, här är era agenter"
- [[alpedal|Alpedal]]: support första veckan (daglig check-in)
- [[william|William]]: övervakning första 48h
- Övergång till subscription (se [[SUBSCRIPTION_TIERS]])

## Steg 5: Löpande (Paket 3)

- Månadsmöte (Pro/Enterprise) (se [[SUBSCRIPTION_TIERS]])
- Löpande uppdateringar
- Nya agenter vid behov
- Årlig "state of automation" — vad har vi gjort, vad är nästa?

## Checklista per kund

```
Kund: [NAMN]
Status: [Lead / Audit / Bygg / Live / Aktiv]

☐ Intro-möte bokat
☐ Audit genomförd
☐ Audit-rapport levererad (se [[AUDIT_TEMPLATE]])
☐ Offert skickad (se [[OFFERT_TEMPLATE]])
☐ Kontrakt påskrivet
☐ Dashboard skapad
☐ Agenter byggda (lista:)
☐ Testade och godkända
☐ Go live
☐ Utbildning genomförd
☐ Första månaden aktiv
```

## Kommentarer

- 2026-06-24 | william: skapad
- 2026-06-24 | hermes: Länkat till teammedlemmar, templates, strategidokument och prismodeller.
