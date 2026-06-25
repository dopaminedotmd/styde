---
title: "Subscription Tiers"
date: 2026-06-24
author: william
tags: [area/OPS, status/APPROVED, author/WILLIAM, type/CONCEPT]
status: approved
---

# Subscription Tiers

> [!info] Subscription
> Detaljerad beskrivning av subscription-nivåer.
> Senast uppdaterad: 2026-06-24

## Nivåer (se [[PRICING_MODEL]] & [[OFFER]])

| Nivå | Pris | Agenter | Support | Uppdateringar | Dashboard | Möten |
|------|------|---------|---------|---------------|-----------|-------|
| Basic | 4 900 kr/mån | 1-3 | Mail, 24h svar | Månadsvis | Standard | Kvartal |
| Pro | 9 900 kr/mån | 4-8 | Mail+telefon, 8h | Varannan vecka | Anpassad färg | Månad |
| Enterprise | 19 900 kr/mån | Obegränsat | Priority, 2h svar | Löpande | Vitmärkt | Vecka |

## Vad ingår i ALLA nivåer

- Drift och hosting av agenterna (se [[SYSTEM_OVERVIEW]])
- Övervakning (agenterna fungerar)
- Loggning och historik (30 dagar) (se [[DASHBOARD_SPEC]])
- Backup av agent-konfiguration (se [[AGENT_FRAMEWORK]])
- Säkerhetsuppdateringar
- Email-support under kontorstid

## Basic — 4 900 kr/mån

Passar: Småföretag med 1-3 enkla processer som ska automatiseras.

- Upp till 3 agenter
- Mail-support, svar inom 24h (vardagar)
- Månatliga uppdateringar (buggfixar)
- Standard dashboard (vår design, kundens logo)
- Kvartalsmöte (15 min)

## Pro — 9 900 kr/mån

Passar: Medelstora företag med flera processer och behov av mer support.

- Upp till 8 agenter
- Mail + telefon, svar inom 8h (vardagar)
- Uppdateringar varannan vecka (nya features)
- Anpassad dashboard (kundens färger och logo)
- Månadsmöte (30 min)
- Prioriterad felhantering

## Enterprise — 19 900 kr/mån

Passar: Större företag med komplexa flöden och höga krav på uptime.

- Obegränsat antal agenter
- Priority support, svar inom 2h (alla dagar)
- Löpande uppdateringar och optimering
- Fullskalig, vitmärkt dashboard (kundens eget varumärke)
- Veckomöte (30 min): strategisk uppföljning
- Dedikerad kontaktperson ([[william|William]])
- SLA: 99,5% uptime

## Uppsägning

- 30 dagars uppsägningstid (Basic och Pro)
- 90 dagar (Enterprise)
- Vid uppsägning: alla agenter stängs av. Data exporteras till kund inom 14 dagar (se [[ONBOARDING]] Steg 5).
- Ingen bindningstid efter första 3 månaderna (Basic och Pro)
- 12 månaders bindning (Enterprise)

## Kommentarer

- 2026-06-24 | william: skapad
- 2026-06-24 | hermes: Länkat till team, prismodeller, specar, och onboarding.
