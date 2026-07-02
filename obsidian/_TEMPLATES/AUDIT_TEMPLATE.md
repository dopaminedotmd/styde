---
title: "Mall för kundaudit"
date: 2026-06-25
author: hermes
tags: [area/KLIENT, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# Nulägesanalys & AI-Audit: {Kundnamn}

> [!summary] Sammanfattning
> Denna audit identifierar {X} kritiska flaskhalsar i {Kundnamn}s nuvarande arbetsflöden, primärt inom {Process, t.ex. fakturahantering}. Genom implementering av styde's AI-agenter estimeras en tidsbesparing på {Y} timmar/månad, vilket motsvarar ett frigjort kapital på ca {Z} SEK/år.

## 1. Nulägesanalys (Current State)
*Kartläggning av hur processen ser ut idag, innan AI.*

* **Process:** {Namn på process, t.ex. Manuell matchning av leverantörsfakturor}
* **Involverade system:** {t.ex. Fortnox, Gmail, Slack}
* **Volym:** {t.ex. 500 fakturor/månad}
* **Tidsåtgång idag:** {t.ex. 10 min/faktura = ~83 timmar/månad}

## 2. Identifierade Flaskhalsar (Pain Points)
*Var läcker företaget tid och pengar?*

1. **Kontextbyten:** Personalen måste ständigt växla mellan mail och affärssystem.
2. **Datainmatning:** Manuellt knappande av OCR-nummer och belopp som ofta leder till mänskliga fel (ca 5% felmarginal).
3. **Avvikelsehantering:** Otydliga rutiner när en faktura saknar PO-nummer (Inköpsordernummer).

## 3. Lösningsarkitektur (Proposed AI Solution)
*Hur styde's agenter löser problemet via Build-fasen.*

* **Agent 1: Ingestion Agent**
  * **Trigger:** Nytt mail i `faktura@{kundnamn}.se`
  * **Action:** Extraherar PDF, läser ut metadata (Belopp, Moms, Avsändare, PO-nummer) via LLM.
* **Agent 2: Fortnox Matcher**
  * **Action:** Korscheckar uppgifterna mot Fortnox API. Om grön: Bokför som utkast. Om röd (avvikelse): Skickar ett Slack-meddelande till ansvarig med en "Godkänn/Avvisa"-knapp.

## 4. ROI & Värdekalkyl (Business Case)
*Det fristående värdet för kunden.*

| Mätetal | Nuvarande | Med styde | Besparing |
| :--- | :--- | :--- | :--- |
| **Tid per månad** | 83 timmar | 5 timmar (endast avvikelser) | 78 timmar/mån |
| **Kostnad (à 500kr/h)** | 41 500 kr | 2 500 kr | 39 000 kr/mån |
| **ROI (År 1)** | - | - | **468 000 kr** |

## 5. Nästa Steg (Call to Action)
- [ ] Genomgång av Audit med {Beslutsfattare}.
- [ ] Avrop av "Build-fasen" (Dras av från Audit-kostnaden).
- [ ] Signering av SLA & Operate-avtal.

## Kommentarer

- 2026-06-25 | hermes: Mall skapad utifrån diskussion och förslag från Gemini. Rättat taggar och struktur enligt bot-regler.
