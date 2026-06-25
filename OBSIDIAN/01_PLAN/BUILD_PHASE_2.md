---
title: "BUILD_PHASE_2 — Systembyggnad"
date: 2026-06-24
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/PLAN]
status: draft
---

# BUILD_PHASE_2 — Systembyggnad

> [!warning] Fokusera på bygget
> Detta är planen för att bygga ett skarpt internt system — innan vi säljer.
> Teamet onboardas under tiden. Inget sälj förrän systemet är bevisat.

> Senast uppdaterad: 2026-06-24

---

## Innehåll

1. [[#1. Agent Flow — hur agenter jobbar]]
2. [[#2. Agentförbättring — själv + av varandra]]
3. [[#3. Cyber Security — inbyggt från start]]
4. [[#4. Dashboard — funktioner och byggordning]]
5. [[#5. Hemsida — lead capture och case studies]]

---

## 1. Agent Flow — hur agenter jobbar

Dagens [[AGENT_FRAMEWORK]] beskriver en agent som en isolerad enhet. Det räcker inte. Vi måste designa **hela flödet** från trigger till resultat — och hur agenter samverkar.

### 1.1 Agenttyper

| Typ | Trigger | Exempel | Användning |
|-----|---------|---------|------------|
| **Manuell** | Knapp i dashboard | "Skicka rapporten nu" | Första deployment, ad-hoc |
| **Schemalagd** | Cron | "Kolla fakturor varje måndag 08:00" | 80% av agenter |
| **Event-driven** | Webhook / email / Slack | "När mail från kund X anländer" | Realtidsprocesser |
| **Kedjad** | Output från annan agent | "När Agent A är klar → starta B med dess data" | Komplexa pipelines |

### 1.2 Agent Lifecycle (per körning)

```
TRIGGER → INPUT → PROCESS → OUTPUT → LOGG → LAGRING
             ↑                        ↓
          VERKTYG                DASHBOARD/NOTIS
```

Varje körning får ett unikt `run_id`. Alla steg loggas.

| Steg | Detaljer | Teknik |
|------|----------|--------|
| **TRIGGER** | Cron, webhook, manuell knapp | API Gateway (se [[SYSTEM_OVERVIEW]]) |
| **INPUT** | Agenten får data (från trigger eller kedja) | JSON i request body |
| **DRY-RUN** | Testläge: inga riktiga API-anrop. Logger vad som HADE hänt. Obligatoriskt i dev. | flagga `dry_run: true` i config.yaml |
| **PROCESS** | AI anropar LLM med system prompt + input | Hermes / OpenAI / valfri provider |
| **VERKTYG** | Agenten anropar API:er under processen | tools.yaml definierar vad som finns |
| **OUTPUT** | Strukturerat resultat | JSON enligt promptens output-format |
| **LOGG** | Alla steg loggas centralt | Loggdatabas, spårbart per run_id |
| **LAGRING** | Resultat sparas + visas i dashboard | API Gateway → Dashboard DB |

### 1.3 Retry-state

En körning som retryas behåller samma `run_id` med attempt-index:

```
run_id: "a1b2c3.attempt=1"  ← första försöket
run_id: "a1b2c3.attempt=2"  ← retry
run_id: "a1b2c3.attempt=3"  ← sista retry
```

Detta gör att loggen går att följa över alla försök för samma händelse.
Max 3 attempts per körning. Därefter permanent fel.

### 1.4 Kedjade agenter (pipelines)

Ett kundflöde kan kräva flera agenter i sekvens:

```
Agent A: "Hämta fakturor från Fortnox"
    → Resultat: [lista fakturor]
Agent B: "Kontrollera varje faktura mot bokföringsregler" (tar A's output)
    → Resultat: [OK, OK, FLAG: saknar moms]
Agent C: "Skicka mail till kund om flaggade fakturor" (tar B's output)
    → Resultat: [3 mail skickade]
```

**Regel för kedjor:** Varje agent i kedjan vet bara sitt eget uppdrag. Kedjans logik styrs av en **orchestrator** (separat agent eller config). Orchestratorn:
- Startar nästa agent när föregående är klar
- Skickar rätt data mellan stegen
- Hanterar fel: om Agent B failar → notifiera admin, stoppa kedjan

### 1.5 Error handling

| Fel | Beteende |
|-----|----------|
| API timeout (5s) | Retry 2 gånger, sedan logga + notifiera |
| LLM timeout | Retry 1 gång med kortare prompt, sedan faila |
| Valideringsfel (output matchar inte schema) | Retry med tydligare instruktion, sedan faila |
| Rate limit (429) | Vänta + exponentiell backoff, max 3 retries |
| Permanent fel (401, 403, 500) | Faila direkt. Logga. Notifiera. |

Alla fel skrivs till loggen med `run_id` + `error_code` + `traceback`. Dashboard visar röd status.

### 1.6 Orchestrator (kedjestyrning)

Orchestratorn är en **dedikerad orchestrator-agent** (inte en config-fil). Den:

- Tar emot en pipeline-definition (JSON): `{"steps": [{"agent": "A", "input_from": "trigger"}, {"agent": "B", "input_from": "step_0"}]}`
- Triggar nästa agent omedelbart när föregående är klar
- **Partial failure:** Om Agent B failar → orchestratorn flaggar steget som failat, notifierar admin, och väntar på beslut: försök igen, hoppa över, eller stoppa hela kedjan
- Alla orchestrator-beslut loggas med eget run_id
- Pipelines kan ha max 5 steg. Vid behov → bryt isär i sub-pipelines

**Implementation:** Orchestratorn är en generisk agent som läser pipeline-definitionen och anropar målagenternas API:er. Ingen custom-kod per pipeline.

**Orchestratorns prompt ligger i `skills/delivery/`** — den är intern, inte kundens.

### 1.7 Flödesdokumentation per kund

Varje kund får en flödeskarta i [[OBSIDIAN/04_CLIENTS]] som visar:
- Vilka agenter som finns
- Hur de triggas
- Vilka kedjor som finns
- Beroenden mellan agenter

**Leverabel:** `{kundnamn}_FLOW.md` i kundens mapp. Genereras av [[ca-agent-builder]] efter audit.

---

## 2. Agentförbättring — själv + av varandra

Detta är vår stora konkurrensfördel. Agenter som blir bättre utan att vi skriver ny prompt varje vecka.

### 2.1 Feedback loop (självförbättring)

Efter varje agentkörning:

```
KÖRNING → LOGG → ANALYS → FÖRSLAG → (GODKÄNN) → UPPDATERAD PROMPT
```

| Steg | Beskrivning | Görs av |
|------|-------------|---------|
| **LOGG** | Alla steg loggas: input, output, tools-anrop, tid, fel | Systemet |
| **ANALYS** | En analys-agent granskar loggen. Frågor: Gav output rätt format? Hittade agenten rätt data? Fanns onödiga steg? Tog det för lång tid? | `<ca-agent-reviewer>` (ny skill) |
| **FÖRSLAG** | Analysen genererar en föreslagen prompt-uppdatering | `<ca-agent-reviewer>` |
| **GODKÄNN** | Människa (William/Alpedal) godkänner eller avvisar förslaget | Dashboard-notis + knapp |
| **UPPDATERA** | Prompten uppdateras, version bumpas | Systemet |

**Definition av `ca-agent-reviewer`:**
- Syfte: Analysera agent-loggar och föreslå prompt-förbättringar
- Input: Logg (run_id, input, output, tools-anrop, tid, fel)
- Output: Förslag på prompt-ändring eller "Ingen förbättring behövs"
- Prompt: "Du granskar en AI-agents körningslogg. Jämför output mot förväntat format. Hitta mönster i fel. Föreslå maximalt 3 prompt-ändringar. Varje förslag ska vara specifik (exakt text som ska läggas till/ändras) och ha en motivering."
- Ligger i `skills/delivery/` — intern skill, inte kundens

**Versionshantering:** Varje promptändring sparas med version. Även `tools.yaml` versionshanteras — varje verktygsändring (nytt API, ändrad endpoint, ny auth-metod) bumpas separat.

```
agents/deployed/{kund}/{agent}/
├── prompts/
│   ├── v1.0.0.md   ← original prompt
│   ├── v1.1.0.md   ← första prompt-förbättringen
│   └── current.md  ← aktiv prompt (alias till senaste godkända)
├── tools/
│   ├── v1.0.0.yaml ← original tools
│   ├── v1.1.0.yaml ← tools-ändring (ny endpoint)
│   └── current.yaml← aktiv tools (alias)
└── config/
    └── current.yaml ← aktiv config (kundspecifik, versionshanteras inte)
```

**Frekvens:** Analys körs varje natt för agenter som körts ≥5 gånger den dagen. Om inget fel → ingen ändring.

### 2.2 Cross-agent review (förbättring av varandra)

Olika agenter för olika kunder granskar varandras loggar anonymt.

```
Agent A (Kund 1): "Hantera fakturor"
Agent B (Kund 2): "Hantera fakturor" (liknande uppdrag, annan kund)

Agent A's logg → anonymiseras (ta bort kunddata, behåll struktur)
             → skickas till Agent B
             → "Hade du gjort annorlunda? Något jag missar?"
             → Svaret loggas som förbättringsförslag
```

**Regler för cross-review:**
- **Ingen kunddata delas.** Endast prompt-struktur, felmönster, approach
- Agenten ser aldrig vilken kund det gäller
- **Anonymisering:** Innan loggen skickas till en annan agent körs ett LLM-pass som skrubbar: alla e-postadresser → `[EMAIL]`, personnamn → `[NAMN]`, företagsnamn → `[FÖRETAG]`, personnummer → `[PNR]`. Detta är en **obligatorisk** del av cross-review-flödet, inte en option.
- Förslagen hamnar i en kö som William/Alpedal godkänner
- Samma agenttyp (t.ex. "fakturahantering") jämförs först
- Olika agenttyper jämförs när de har ≥10 körningar var

**Kräver:** `<ca-cross-review>` skill som hanterar anonymisering och matchning.

### 2.3 Pattern library (YAML)

Över tid samlar vi mönster från alla kunder. Varje mönster lagras som YAML-block, inte fri text:

```yaml
- type: timeout
  trigger: "Fortnox API returning 408/504"
  agent_type: "invoice-processing"
  fix: "Add retry logic: 3 attempts with exponential backoff, 2s/4s/8s"
  source: "cross-review (kund A + kund B)"
  added: "2026-07-01"
  status: active

- type: output-format
  trigger: "Momsbelopp saknas på exportfakturor"
  agent_type: "invoice-processing"
  fix: "Add explicit instruction: 'Always include VAT breakdown per line item'"
  source: "feedback-loop (kund A)"
  added: "2026-07-15"
  status: active
```

Detta gör biblioteket querybart. När en ny agent byggs → sök på `agent_type` för att ladda relevanta mönster från start.

**Leverabel:** `OBSIDIAN/05_OPS/AGENT_PATTERNS.md` — levande dokument, uppdateras efter varje intressant observation. Format: YAML-block per mönster. `status: active | deprecated | archived`.

### 2.5 Självförbättringsloopen (systemet blir smartare över tid)

Detta kopplar ihop allt — den loop som gör att VARJE NY KUND startar smartare än den förra.

```
deployed-agent körs
  → loggas
  → ca-agent-reviewer analyserar
  → prompt-förbättring godkänns
  → deployed-agent uppdateras (v1.1.0)
  → ÄR FÖRBÄTTRINGEN GENERELL? (gäller agenttypen, inte kundspecifik)
    → JA: ca-agent-reviewer flaggar template-uppdatering
      → William godkänner
      → agents/templates/{agenttyp}/prompt.md uppdateras
      → template-version bumpas (v1.0.0 → v1.1.0)
      → NÄSTA KUND med samma agenttyp startar på v1.1.0
    → NEJ: stannar i deployed-agentens versionshistorik
```

**Regel:** Minst 2 olika kunder måste ha samma förbättring innan den flyttas till templates.
**Ägare:** William godkänner template-bump. ca-agent-reviewer flaggar.

### 2.6 Förbättrings-Pipeline (sammanfattning)

```
Vid varje agentkörning:
  → Logga (automatiskt)
  → Analysera om ≥5 körningar idag (nattjobb)
  → Generera prompt-förslag om förbättring finns
  → Skicka till William/Alpedal för godkännande
  
Varje vecka:
  → Cross-review: matcha liknande agenter mellan kunder
  → Uppdatera AGENT_PATTERNS.md med nya insikter

Varje månad:
  → Granska alla prompt-versioner. Finns agenter som aldrig förbättrats?
  → Har mönster-biblioteket vuxit? Finns nya reusable skills att skapa?
```

### 2.7 Cost guard — maxkostnad per körning

Varje agent får ett `max_cost_per_run` i config.yaml. Om kostnaden överskrids:

| Steg | Händelse |
|------|----------|
| **Check** | Före varje LLM-anrop: har vi nått max_cost? |
| **Tröskel 80%** | Logger varning |
| **Tröskel 100%** | Avbryter körningen, returnerar "Avbruten — kostnadsgräns nådd" |
| **Notis** | Skickas till admin: "{agent} överskred max_cost {belopp}" |

Detta förhindrar att en felande agent i loop kostar hundratals kronor.
Cost guard är P1 — implementeras i API Gateway, kräver ingen UI.
```

---

## 3. Cyber Security — inbyggt från start

Säkerhet kan inte läggas på efteråt. Det påverkar arkitektur, val av hosting, och hur vi bygger varje agent.

### 3.1 Dataklassificering

All data som passerar systemet klassificeras:

| Nivå | Exempel | Krav |
|------|---------|------|
| **Publik** | Marknadsmaterial, case studies | Inga |
| **Intern** | Agent-konfiguration, prompt-versioner | Åtkomst via inloggning |
| **Känslig** | Kundens fakturor, mail, process-flöden | Krypterat i vila+transit, tenant-isolerat |
| **Kritisk** | Personnummer, inloggningsuppgifter, API-nycklar | Krypterat, aldrig i prompt, åtkomstloggad |

**Regel:** Lägsta möjliga nivå alltid. Om data inte behövs för agentens uppdrag → ta inte in den.

### 3.2 Tenant-isolering

Varje kund är en egen **tenant**. Ingen tenant kan se en annans data.

```
API Gateway
├── Tenant A (acme)
│   ├── Agenter (isolerade)
│   ├── Data (eget schema eller DB-prefix)
│   └── Loggar (eget namespace)
├── Tenant B (beta)
│   ├── Agenter
│   ├── Data
│   └── Loggar
└── Admin (vi)
    ├── Se alla tenants (översikt, ingen rådata)
    ├── Hantera prompts, deployment
    └── Driftövervakning
```

**Implementation:**
- Varje tenant har unik tenant_id i varje API-anrop
- Databasen använder tenant_id som partition key
- Dashboard-sessionen bundet till en tenant
- Endast admin-rollen kan byta tenant

### 3.3 API-nyckelhantering

Inga API-nycklar någonsin i prompts eller källkod.

| Lagringsmetod | Var | Åtkomst |
|---------------|-----|---------|
| Krypterad konfiguration | Vault / krypterad fil | Endast agentens runtime |
| Miljövariabler | CI/CD + deployment | Endast deployment-pipeline |
| Aldrig i prompt | — | Prompten refererar till secrets via namn |

**Flöde:** Agenten anropar `tools.yaml` → runtime slår upp nyckeln i krypterad store → anropar API → nyckeln syns aldrig i prompt eller logg.

### 3.4 Loggning och audit trail

Alla åtgärder loggas:

| Händelse | Loggas | Lagras |
|----------|--------|--------|
| Agentkörning startad | run_id, agent, tenant, trigger, tid | Loggdatabas |
| Varje tools-anrop | run_id, tool, status, tid, responsstorlek | Loggdatabas |
| Fel | run_id, error_code, meddelande, traceback | Loggdatabas |
| Dashboard-inloggning | user, tid, IP, tenant | Separata auth-logs |
| Prompt-ändring | user, agent, version från→till, tid | Separata audit-logs |
| Användares knapptryck | user, agent, run_id, tid | Loggdatabas |

**Krav för audit trail (GDPR):**
- Går att lista ALLA åtgärder en specifik användare har gjort
- Går att exportera per tenant
- Loggar raderas inte — arkiveras (cold storage efter 90 dagar)

### 3.5 GDPR

| Krav | Lösning |
|------|---------|
| **Rätt att bli bortglömd** | tenant-level delete: radera alla loggar, configs, prompts för en tenant |
| **Dataportabilitet** | Exportera tenantens data som JSON |
| **Dataprocessing-avtal** | Signeras med kund före audit (se [[ONBOARDING]]) |
| **Personuppgifter i prompt** | Förbjudet. Prompten specificerar endast roller, inte namn/personnummer |
| **Lagring inom EU** | VPS/värd inom EU. Inga dataskylda molntjänster utanför EU |

**William = interim DPO** (enligt [[MASTER_PLAN_FINAL]]).

### 3.6 Hosting och datalagring

| Krav | Lösning |
|------|---------|
| **EU-lagring** | All kunddata lagras inom EU. Backend på EU-baserad VPS (Hetzner/Hydrogen). |
| **Vercel** | Används ENDAST för frontend (statiska sidor + client-side fetch). Inga Server Actions, inga API Routes som anropar backend med kunddata. All kommunikation med agenter/loggar går direkt från webbläsaren till vår VPS. |
| **GDPR-safe** | Backend API på egen VPS. Databas på samma VPS eller separat EU-baserad DB. |
| **Trafik** | Dashboard ↔ API Gateway inom EU. Ingen data lämnar EU. |

Om första kunden kräver 99,9%-garanti → SLA-datainsamling (uptime metrics) börjar från dag 1 i API Gateway, även om SLA-UI byggs senare (P4). Data som inte samlas in från start går inte att återskapa.

### 3.7 Loggrensning (GDPR)**

| Typ | Lagringstid | Åtgärd efter |
|-----|-------------|---------------|
| Agent-loggar (run_id, tools, fel) | 90 dagar | Arkiveras till cold storage |
| Auth-loggar (inloggning, IP) | 180 dagar | Raderas |
| PII i loggar (e-post, personnummer) | 90 dagar | Anonymiseras (automatiskt LLM-pass) |
| Prompt-versioner | Evigt | Behålls (ingen PII) |

**Automatiserad gallring:** Ett cron-jobb körs varje natt och:
1. Markerar loggar äldre än 90 dagar för arkivering
2. Anonymiserar PII i loggar som är äldre än 90 dagar men behövs för analys
3. Raderar auth-loggar äldre än 180 dagar

### 3.8 Åtkomstkontroll (dashboard)

| Roll | Rättigheter |
|------|-------------|
| **Super Admin** (William) | Alla tenants, deployment, prompt-ändringar, loggar |
| **Admin** (Alpedal) | Alla tenants, read-only på prompt, se loggar |
| **Kund-admin** | Sin tenant: se alla agenter, trigga manuellt, se historik |
| **Kund-operator** | Sin tenant: trigga förvalda agenter, se sin historik |
| **Kund-viewer** | Sin tenant: se status, ingen trigger |

---

## 4. Dashboard — funktioner och byggordning

Dagens [[DASHBOARD_SPEC]] beskriver en MVP. Här är hela funktionslistan i den ordning de ska byggas.

### 4.1 Byggordning (prioriterad)

| Prio | Funktion | Byggtid | Beroende |
|------|----------|---------------|----------|
| **P1** | Agentlista + statusindikatorer | 1 dag | API Gateway |
| **P1** | Manuell trigger ("Kör nu"-knapp) | 1 dag | API Gateway |
| **P1** | Run-historik (senaste 20) | 1 dag | Loggdatabas |
| **P1** | Inloggning (email + lösenord) | 2 dagar | Auth-system |
| **P1** | Empty state (onboarding-vy) — första kunden ser instruktioner, inte tom sida | 0,5 dag | — |
| **P1 (backend)** | SLA-datainsamling (uptime metrics) — loggas från dag 1, UI senare | 1 dag | API Gateway |
| **P2** | Agentdetaljvy (loggar, status, config) | 2 dagar | API Gateway |
| **P2** | Tenant-Admin (skapa tenant, bjud in användare) | 2 dagar | Multi-tenant |
| **P2** | Rollhantering (admin/operator/viewer) | 1 dag | Auth-system |
| **P2** | Felnotifikationer (röd status, email-notis) | 2 dagar | Webhook/email |
| **P3** | Agentkonfiguration via dashboard (redigera prompt) | 3 dagar | Versionshantering |
| **P3** | Förbättringsförslag-gränssnitt (godkänn/avvisa) | 2 dagar | Feedback loop |
| **P3** | Kostnadsanalys per agent (per körning, per dag) | 2 dagar | Loggdata |
| **P4** | White-label (Enterprise) | 3 dagar | Tenant-config |
| **P4** | SLA-dashboard (uptime, svarstider, uptime %) | 2 dagar | Monitoring |
| **P4** | Webbhooks för egna integrationer | 3 dagar | API Gateway |

### 4.2 Teknisk stack (fastställd)

Enligt [[MASTER_PLAN_FINAL]]:

| Lager | Teknik | Anledning |
|-------|--------|-----------|
| Frontend | Next.js + Tailwind CSS | Snabb utveckling, stor community |
| Backend | Node.js Express (REST) | Samma språk som frontend, enkel att deploya |
| Databas | PostgreSQL (eller Supabase) | Relationell, JSON-stöd, bra för loggar |
| Hosting frontend | Vercel | Gratis för MVP, enkel deployment |
| Hosting backend | Valfri VPS (Hetzner/Hydrogen) | Full kontroll, EU-baserad, GDPR-safe |
| Agent runtime | Hermes (alla botar) | Samma system som vi själva använder |

### 4.3 Dashboard-designprinciper

| Princip | Beskrivning |
|---------|-------------|
| **1. Status syns direkt** | Ögonen ser grönt/rött utan att läsa |
| **2. En knapp per agent** | Kunden trycker bara på "Kör". Inga inställningar |
| **3. Historik är självförklarande** | Tabell: tid, status, resultat. Ingen tolkning |
| **4. Fel är omöjliga att missa** | Röd bakgrund, inte bara röd text |
| **5. Mobil först** | Allt fungerar på telefon (kunders vardag) |
| **6. Bone White** | #E3E3E4 bas. ALDRIG vit (#FFFFFF) |

### 4.4 Dashboard-skärmar (komplett)

Utöver MVP-skärmarna i [[DASHBOARD_SPEC]]:

**Tenant Admin ($tenant/admin):**
- Lista användare + roller
- Bjud in ny användare
- Agentkonfiguration (välj trigger, schedule, pausa/aktivera)

**Agent Config ($tenant/agents/{id}/config):**
- Redigera prompt (textarea, versionshanterad)
- Välj trigger (manuell/cron/webhook)
- Testkörning (kör med dummy-input)
- Visa senaste loggar

**Förbättringsflöde ($admin/improvements):**
- Lista på obekräftade prompt-förslag (agent → människa)
- Visa diff: nuvarande prompt → föreslagen
- Godkänn / avvisa / redigera manuellt

**Analytics ($tenant/analytics):**
- Antal körningar per dag/vecka/månad
- Success rate per agent
- Genomsnittlig körtid
- Kostnad per agent (API-anrop, LLM-tokens)

---

## 5. Hemsida — lead capture och case studies

Byggs efter dashboard MVP. Innehållet skrivs av [[hermes|Hermes]].

### 5.1 Sidor

| Sida | Syfte | Prioritet |
|------|-------|-----------|
| **Landing** | Value proposition + CTA | P1 |
| **Tjänster** | Audit → Build → Operate | P1 |
| **Pris** | Tiers + avräkningsklausul | P2 |
| **Case studies** | (skapas efter första kunden) | P2 |
| **Kontakt** | Lead capture-formulär | P1 |
| **Blogg** | SEO, tankeledarskap | P3 |

### 5.2 Lead capture (P1)

Formulär på hemsidan:
- Namn, företag, email, telefon
- "Vad är din största IT-utmaning?" (textarea)
- Skickas till William via email + loggas i 
- Automatiskt svar: "Tack, vi återkommer inom 24h"

**Flöde:** Formulär → Webhook → William mail + OBSIDIAN/04_CLIENTS/_ACTIVE/ ny lead-fil

### 5.3 Case study-struktur (när vi har första kunden)

| Sektion | Innehåll |
|---------|----------|
| **Rubrik** | "Hur {företag} sparar {X}h/vecka med AI-agenter" |
| **Utmaningen** | 2-3 meningar om deras IT-stress |
| **Lösningen** | Vilka agenter byggdes? Vad gör de? |
| **Resultatet** | Timmar/månad sparade, fel minskade, pengar |
| **Teknik** | Kort: Hermes, dashboard, integrationer |
| **Citat** | Från kunden |

### 5.4 SEO-strategi

Sökord som svenska SME-företag söker på (enligt [[MARKET]]):
- "AI agent automation"
- "automatisera IT-flöden"
- "bygg AI agenter"
- "Fortnox automation" (icke-existerande sökord = låg konkurrens)
- "Google Workspace automation"
- "AI för redovisningsbyrå"

Varje sökord → en bloggpost. Publiceras efter hemsida.

---

## Byggordning (sammanfattad)

```
Vecka 1-2:
  [Hermes] Bygg testklient i OBSIDIAN/04_CLIENTS/_ACTIVE/
  [Hermes] Bygg ca-agent-reviewer + ca-cross-review skills
  [Hermes] Skriv hemside-content + SEO-artiklar
  > **Not:** ca-agent-reviewer byggs nu men kan inte testas förrän Vecka 3+ när loggar finns. Det är OK — implementation först, testning senare.

Vecka 2-3:
  [William] API Gateway (Express, auth, multi-tenant, cost guard, SLA metrics)
  [William] Dashboard P1: agentlista, trigger, historik, login, empty state
  [Hermes] AGENT_PATTERNS.md + säkerhetsdokumentation
  [Alla] **Dogfood startar** — en simpel intern agent (mail-sort) körs på vår egen plattform

Vecka 3-4:
  [William] Dashboard P2: tenant admin, roller, notifikationer
  [William + Hermes] Första testklientens agenter byggs i vår egen plattform

Vecka 4-5:
  [William] Dashboard P3: agent-config (UI), förbättringsförslag (UI)
  [Hermes] Bygg ca-orchestrator (kedjestyrning)

Vecka 5-6:
  [William] Hemsida P1: landing, tjänster, kontakt
  [William] Dashboard P4: kostnadsanalys
  [Alla] Fortsatt dogfood + åtgärda buggar som avslöjas
```

---

## Kommentarer

- 2026-06-24 | hermes: Skapad. Baserad på samtal med William om systembyggnad före försäljning.
- 2026-06-24 | antigravity: Granskat. [10 punkter + idéer — se kommentarer nedan]
- 2026-06-24 | hermes: Uppdaterad efter bot-granskning — specificerade orchestrator (1.5), retry-state (1.3), dry-run (1.2), ca-agent-reviewer definition (2.1), tools-versionering (2.1), cross-review anonymisering (2.2), patterns YAML (2.3), självförbättringsloopen (2.5), cost guard (2.7), hosting/GDPR (3.6), loggrensning (3.7), dashboard empty state + SLA-data (4.1), justerad tidsplan + dogfood earlier (byggordning).
  1. KRITISK: Orchestrator (kap 1.3) saknar implementation. "Separat agent eller config" är ospecat. Vad triggar orchestratorn? Hur hanterar den partial failure mitt i kedja? Blockar Vecka 1.
  2. KRITISK: `ca-agent-reviewer` (kap 2.1) ska analysera loggar men agentens egna prompt finns inte. Kyckling-och-ägg. Måste definieras före Vecka 1 är klar.
  3. Cross-review anonymisering (kap 2.2) underspecificerad. "Ta bort kunddata" är inte en algoritm. Embedded kundinfo i fri text? Behövs: LLM-pass som granskar logg innan cross-review skickas. GDPR-risk tills detta är löst.
  4. Agent lifecycle (kap 1.2) saknar RETRY_STATE. En körning som retryas borde behålla samma `run_id` med sub-index (t.ex. `run_id.attempt=2`). Annars blir loggen ospårbar.
  5. `tools.yaml` versionshanteras inte (kap 2.1). Prompt-versioner finns men verktygsändringar syns inte i audit trail. Lägg till samma versions-öppning för tools.
  6. Dashboard P1 (kap 4.1) saknar empty state. Första kunden ser tom agentlista. Behövs: onboarding-state med instruktion.
  7. Tidsplanen Vecka 3-4 är orealistisk: Elb får 9-11 dagars arbete på 5-7 dagar (Dashboard P2 + Hemsida P1 parallellt). Flytta hemsida till Vecka 5-6.
- 2026-06-24 | antigravity: IDEER som saknas i planen:
  A. Dogfood earlier: kör egna agenter på egen plattform från Vecka 2, inte Vecka 4. Buggar hittas 2 veckor tidigare.
  B. Cost guard P1 (backend, ingen UI): sätt `max_cost_per_run` i agent-config från start. En felande agent i loop kan kosta hundratals kronor utan detta.
  C. `AGENT_PATTERNS.md` bör vara YAML-block (type/trigger/fix/source) inte fri markdown. Querybar när biblioteket växer till 50+ mönster.
  D. SLA-datainsamling (uptime metrics) bör vara P1-backend även om SLA-UI är P4. Om första kunden kräver 99.9%-garanti är det för sent att börja samla data då.
- 2026-06-24 | antigravity: SJÄLVFÖRBÄTTRINGSSYSTEMET (saknas som explicit loop i båda planeringarna): deployed-agent förbättras → godkänns → om generell → uppdaterar agents/templates/ → nästa kund startar smartare. Idag förbättras enskilda kunders agenter. Vad vi vill: systemet som helhet förbättras — varje ny kund startar på högre baseline än den förra. Den kopplingen måste ägas av någon (förslag: ca-agent-reviewer + William godkänner template-bump).
- 2026-06-24 | antigravity: Ytterligare granskning av arkitektur och GDPR:
  8. GDPR/Hosting: Vercel kan routa trafik utanför EU. Om vi hanterar känsliga kunddata krävs EU-specifik hosting eller Next.js hostat på vår egen VPS för full regelefterlevnad.
  9. Lokal sandbox: Utveckling och testning behöver ett "Dry-run"-läge i Agent Lifecycle för att undvika att skicka riktig e-post eller anropa skarpa Fortnox API:er under tester.
  10. Loggrensning (GDPR): Automatiserad gallring eller anonymisering av rådata (PII) i loggdatabasen efter 90 dagar måste definieras i dataklassificeringen.

