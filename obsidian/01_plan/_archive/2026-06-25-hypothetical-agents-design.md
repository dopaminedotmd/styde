---
title: "Design — Hypotetiska Agenter & Automationsmöjligheter"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/DESIGN]
status: draft
---

# Design — Hypotetiska Agenter & Automationsmöjligheter

> [!note] Syfte
> Detta dokument kartlägger högförsäljningsbara, hypotetiska AI-agenter och automationsflöden för SME-företag med hög betalningsvilja och tydliga administrativa flaskhalsar.

---

## 1. Målgrupper & Betalningsvilja

Vi fokuserar på branscher med följande egenskaper:
1. **Hög transaktionsvolym** av dokument, mail eller data.
2. **Många fristående SaaS-system** som saknar bra integrationer.
3. **Hög kostnad för felaktig inmatning** (t.ex. felaktiga fakturor, missade leveranser).
4. **Tydlig ROI:** Om en agent sparar 20 timmar i veckan för en administratör är betalningsviljan för en prenumeration på 10-20k kr/månad extremt lätt att motivera.

---

## 2. Bransch 1: Redovisnings- & Revisionsbyråer

Redovisningsbyråer drunknar i manuell dokumenthantering och avstämning. De har hög betalningsvilja eftersom deras tid debiteras per timme, och automatisering frigör direkt debiterbar tid till rådgivning.

### Vanliga SaaS-system
- Fortnox, Visma, Capego, Kivra, Skatteverket, BankID, Excel, Outlook/Gmail.

### Flaskhalsar & Manuella processer
- Sortering och matchning av inkommande kvitton/fakturor mot banktransaktioner.
- Manuell registrering av leverantörsfakturor som saknar e-faktura.
- Påminnelser till kunder som inte skickat in sina underlag i tid.

### Hypotetiska Agenter

#### Agent A: "Underlags-Jägaren" (Trigger: Schemalagd / Veckovis)
- **Uppdrag:** Identifiera saknade verifikationer för en viss period och kontakta kunden för att samla in dem.
- **Flöde:**
  1. Läser banktransaktioner i Fortnox/Visma.
  2. Hittar transaktioner som saknar kopplat kvitto/faktura.
  3. Skriver ett personligt, trevligt mail till kunden med en lista på exakta datum och belopp som saknas.
  4. Tar emot svar, tolkar bifogade filer (PDF/JPG) med OCR/Vision, och laddar upp dem till rätt transaktion i Fortnox.

#### Agent B: "Faktura-Tolken" (Trigger: Event-driven / Webhook eller Mail)
- **Uppdrag:** Tolka komplexa eller utländska leverantörsfakturor som standard-OCR missar, och bokföra dem på rätt kostnadskonto.
- **Flöde:**
  1. Bevakar en specifik inkorg (t.ex. `faktura@byra.se`).
  2. Analyserar PDF-fakturan med LLM (förstår sammanhang, utländsk moms, omvända skattskyldigheter).
  3. Matchar mot tidigare bokförda liknande fakturor.
  4. Skapar ett utkast till leverantörsfaktura i Fortnox med förslag på kontering och momskod.
  5. Skickar en notifiering till dashboarden för snabbt godkännande (knapptryck).

---

## 3. Bransch 2: Fastighetsbolag & Förvaltning

Fastighetsbolag har ofta komplexa flöden kring felanmälningar, hyresaviseringar och leverantörsavtal. De är villiga att betala eftersom felaktig hantering leder till missnöjda hyresgäster och onödiga utryckningskostnader.

### Vanliga SaaS-system
- Vitec, Pigello, RealPortal, BankID, Outlook, Slack/Teams, Excel.

### Flaskhalsar & Manuella processer
- Triagering av felanmälningar (avgöra om det kräver rörmokare, elektriker eller om hyresgästen kan lösa det själv).
- Manuell matchning av hyresinbetalningar som saknar OCR-nummer.
- Uppföljning av offerter och avtal med underentreprenörer.

### Hypotetiska Agenter

#### Agent C: "Felanmälnings-Triageraren" (Trigger: Event-driven / Webhook från formulär eller mail)
- **Uppdrag:** Ta emot felanmälningar, kategorisera allvarlighetsgrad, ge felsökningsinstruktioner till hyresgästen, och boka rätt hantverkare vid behov.
- **Flöde:**
  1. Läser inkommande felanmälan (mail eller webbformulär).
  2. Analyserar problemet: Är det akut (t.ex. vattenläcka) eller icke-akut (t.ex. droppande kran)?
  3. Om icke-akut: Skriver ett svar till hyresgästen med enkla steg de kan testa själva (t.ex. "rensa vattenlåset").
  4. Om hantverkare krävs: Matchar problemet mot godkända underentreprenörer (t.ex. VVS-firma A i område X), skapar ett utkast till arbetsorder i fastighetssystemet (t.ex. Pigello) och skickar en förfrågan till hantverkaren.

#### Agent D: "Avtals-Vakten" (Trigger: Schemalagd / Månadsvis)
- **Uppdrag:** Hålla koll på löpande leverantörsavtal, indexuppräkningar och uppsägningstider.
- **Flöde:**
  1. Skannar avtalsarkivet (t.ex. i Sharepoint/Google Drive).
  2. Extraherar slutdatum, uppsägningstid och indexklausuler (t.ex. KPI-justeringar).
  3. Jämför med nuvarande priser i ekonomisystemet.
  4. Varnar förvaltaren 3 månader innan ett avtal förlängs automatiskt om priset har stigit mer än index, eller skapar ett utkast till omförhandling.

---

## 4. Bransch 3: Logistik, Grossister & E-handel

Dessa företag lever på marginaler och snabbhet. Manuella fel i orderhantering eller lagersaldon kostar direkt pengar i form av returer, missade leveranser och förlorade kunder.

### Vanliga SaaS-system
- Shopify, WooCommerce, Fortnox, Visma, TA-system (nShift, Sendify), WMS-system, Excel.

### Flaskhalsar & Manuella processer
- Manuell överföring av orderdata mellan e-handel och affärssystem/TA-system.
- Hantering av tullhandlingar och fraktdokument för internationella sändningar.
- Kundtjänstfrågor av typen "Var är min order?" och returhantering.

### Hypotetiska Agenter

#### Agent E: "Tull- & Fraktdokumenteraren" (Trigger: Event-driven / Ny order utanför EU)
- **Uppdrag:** Generera korrekta tullhandlingar (proformafakturor, HS-koder) baserat på orderinnehåll och destination.
- **Flöde:**
  1. Upptäcker en ny internationell order i Shopify/WooCommerce.
  2. Slår upp produkternas HS-koder (tullkoder) i en databas eller söker upp dem via AI om de saknas.
  3. Skapar tullfakturan (Commercial Invoice) med korrekta vikter, värden och ursprungsland.
  4. Laddar upp dokumentet till TA-systemet (t.ex. nShift) och bokar frakten.
  5. Notifierar lagret om att skriva ut tullhandlingarna tillsammans med plocksedeln.

#### Agent F: "Lagersaldo-Detektiven" (Trigger: Schemalagd / Dagligen)
- **Uppdrag:** Upptäcka och utreda avvikelser i lagersaldon mellan e-handel, WMS och fysiskt lager.
- **Flöde:**
  1. Jämför lagersaldon i Shopify mot WMS/Fortnox.
  2. Identifierar differenser (t.ex. 5 st i Shopify men 2 st i Fortnox).
  3. Spårar historiken för de berörda produkterna (senaste ordrar, returer, leveranser) för att hitta felkällan.
  4. Skriver en rapport till lagerchefen med förslag på korrigering: "Differensen på produkt X beror troligen på att retur #1234 inte registrerades i Fortnox."

---

## 5. Generella "Quick Wins" (Alla branscher)

Dessa agenter löser problem som nästan alla SME-företag har, vilket gör dem till perfekta "dörröppnare" i en säljprocess.

### Agent G: "Mötes- & Action-Tracker" (Trigger: Event-driven / Avslutat möte)
- **Uppdrag:** Transkribera möten, sammanfatta beslut och lägga in action-items direkt i projektverktyg (Trello/Jira/Asana) och CRM.
- **Flöde:**
  1. Hämtar ljudfil/transkription från Teams/Zoom/Meet.
  2. Skapar en strukturerad sammanfattning (Beslut, Diskussion, Action-items).
  3. Identifierar vem som ska göra vad.
  4. Skapar uppgifter i Trello/Jira med deadline och tilldelar rätt person.
  5. Skickar sammanfattningen till mötesdeltagarna via Slack/mail.

### Agent H: "Lead-Berikaren" (Trigger: Event-driven / Nytt lead i CRM)
- **Uppdrag:** Göra research på nya leads, berika CRM-kortet med bolagsdata och skriva ett skräddarsytt säljmail.
- **Flöde:**
  1. Upptäcker ett nytt lead i HubSpot/Salesforce (t.ex. endast namn och domän).
  2. Söker på Allabolag.se efter omsättning, antal anställda och nyckelpersoner.
  3. Läser av företagets hemsida för att förstå vad de säljer.
  4. Uppdaterar CRM-kortet med denna data.
  5. Skriver ett utkast till ett personligt säljmail baserat på företagets profil och sparar det som ett utkast i säljarens Outlook/Gmail.

---

## Kommentarer

- 2026-06-25 | hermes: Skapade dokumentet med strukturerade branschvertikaler och hypotetiska agenter baserat på hög betalningsvilja och tydlig ROI.
