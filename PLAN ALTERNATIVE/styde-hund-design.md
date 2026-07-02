# Systemdesign & Specifikation för styde och hund.ai

Detta dokument sammanfattar den brainstormade arkitekturen, affärsmodellen och gränssnittsdesignen för företaget **styde** och dess intelligenta assistent **hund**.

---

## 1. Vision & Koncept

**styde** är en konsult- och SaaS-plattform inriktad på kundanpassade AI-lösningar, agenter och automatisering för företag. Plattformen hjälper kunder att gå igenom hela automationsresan via ett strukturerat trestegsflöde i en och samma dashboard-app:
1.  **Audit**: Kartläggning av flaskhalsar och identifiering av automationspotential.
2.  **Implementation**: Konsultstyrt och transparent bygge av skräddarsydda agenter med testning.
3.  **Subscription**: Driftsatta agenter som kunden prenumererar på, övervakar, styr och interagerar med.

Den centrala assistenten i plattformen heter **hund** (eller **hund.ai**), en vakthund och co-pilot som hjälper kundanvändare att förstå och styra sina agenter samt interagera med sin insamlade data.

---

## 2. Systemarkitektur & GCP-integration

Systemet bygger på en modern, skalbar hybrid-arkitektur som kombinerar Next.js, Supabase och Google Cloud Platform (GCP):

```mermaid
graph TD
    Client[Kundanvändare / Personal] <-->|Next.js WebApp| FE[Next.js Frontend]
    Consultant[styde-konsult] <-->|Next.js WebApp| FE
    
    FE <-->|API / Real-time Sockets| Supabase[(Supabase BaaS)]
    Supabase -->|Auth, Filer, Metadata| DB[(PostgreSQL)]
    
    subgraph Google Cloud Platform (GCP)
        FE <-->|Trigger / Orkestrering| CloudRun[Cloud Run: Agent Runner]
        CloudRun <-->|Event Stream| PubSub[Cloud Pub/Sub]
        CloudRun <-->|Analys & Sökning| BigQuery[(BigQuery Data Warehouse)]
        CloudRun <-->|Dokumentlagring| GCS[(Cloud Storage)]
        CloudRun <-->|AI-hjärna / LLM| VertexAI[Vertex AI: Gemini 1.5]
    end
    
    PubSub -.->|Realtidsloggar & Chatt| Supabase
```

### Arkitekturkomponenter:
*   **Frontend (Next.js)**: Hostas på Vercel. Ger ett snabbt, modernt och mörkt (dark mode) användargränssnitt för både kunder och interna konsulter.
*   **Backend & Realtid (Supabase)**: Sköter autentisering, rollfördelning (konsulter vs. kunder) samt lagring av realtidsmeddelanden i chatten mellan personal, agenter och `hund`.
*   **Agent Runtimes (GCP Cloud Run)**: Agenternas logik och kod (oftast Python med CrewAI/LangChain) driftsätts i isolerade Docker-containrar på GCP Cloud Run. De skalar till noll när de inte används för maximal kostnadseffektivitet.
*   **AI-hjärna (GCP Vertex AI)**: Agenterna anropar Gemini-modeller via Vertex AI. Detta garanterar datasäkerhet (data används ej för träning av allmänna modeller, stannar i EU) och tillåter användning av Geminis massiva kontextfönster (2 miljoner tokens) för RAG-analyser.
*   **Integrationslager (GCS & BigQuery)**: Agenterna kan ansluta direkt till kundens lagrade PDF-dokument i Cloud Storage samt läsa och skriva strukturerad produktionsdata i BigQuery.

---

## 3. Prenumerationsnivåer (Subscription Tiers)

Plattformen erbjuder tre prenumerationsnivåer baserat på kundens storlek och automationsbehov:

| Funktion | Starter | Growth (Rekommenderas) | Enterprise |
| :--- | :--- | :--- | :--- |
| **Målgrupp** | Små bolag (1-2 processer) | Växande produktion/avdelningar | Storföretag / ERP / Kritiskt |
| **Aktiva agenter** | Max 2 st | Max 5 st | Obegränsat antal |
| **Modeller** | Gemini 1.5 Flash (Standard) | Avancerad + Finjusterad Flash | Dedikerade modeller / Fine-tuning |
| **Integrationer** | E-post, Google Drive, Webhooks | Slack, SQL-databaser, CRM/ERP | Skräddarsydda / SAP / On-Prem |
| **Logghistorik** | 30 dagar | 90 dagar | Obegränsad |
| **Audits** | 1 per yr | 2 per yr (halvårsvis) | Löpande / Dedikerad AI-konsult |
| **Driftsform** | Delad infrastruktur (SaaS) | Delad infrastruktur (SaaS) | Möjlighet till eget GCP-projekt |

---

## 4. Gränssnitt & Anpassningsmöjligheter (Customization)

### Dashboardens Layout
1.  **Sidebar (Vänster)**: Innehåller logotypen `styde` (små bokstäver), genvägar till Dashboard, Project Flow (Audit/Implementation/Active), Agent Hub samt Inställningar.
2.  **Huvudvy (Mitten)**: Visar den valda sidan. I Agent Hub listas alla aktiva agenter med genvägar till deras individuella inställningar, loggar och chattar.
3.  **Co-pilot Pane (Höger, utfällbar)**: Dedikerad chatt med **hund** (`hund.ai` i små bokstäver). `hund` har koll på allt som händer i dashboarden och kan svara på frågor om agenternas arbete eller ge support.

### Anpassning i de olika stegen
*   **Audit-steget**:
    *   *Department Mapping*: Kunden ritar upp sin organisationsstruktur.
    *   *Custom Context*: Kunden laddar upp interna policyer och ordlistor som grund för auditen.
*   **Implementations-steget**:
    *   *Agent Identity*: Kunden namnger agenten och väljer/genererar en avatar.
    *   *Personality Sliders*: Styr agentens beteende (Strikt vs. Flexibel, Kortfattad vs. Utförlig).
    *   *Trigger Setup*: Konfigurera scheman (t.ex. "Kör varje vardag kl 08:00") eller webhooks.
*   **Subscription-steget**:
    *   *Cost Guard*: Sätt budgetgränser i dollar per dag/månad för varje enskild agent.
    *   *Prompt Overrides (Regler)*: Lägg till ad-hoc regler (t.ex. "Skicka fakturor över 50 000 kr direkt till chef Y").

---

## 5. Databas-schema (Supabase / PostgreSQL)

För att stödja dessa funktioner används följande relationella schema:

### Tabeller & Fält:
*   `organizations`
    *   `id` (UUID, PK)
    *   `name` (Text)
    *   `tier` (Enum: starter, growth, enterprise)
    *   `created_at` (Timestamp)
*   `users`
    *   `id` (UUID, PK)
    *   `org_id` (UUID, FK -> organizations.id)
    *   `email` (Text)
    *   `name` (Text)
    *   `role` (Enum: client_admin, client_staff, styde_consultant)
*   `audits`
    *   `id` (UUID, PK)
    *   `org_id` (UUID, FK -> organizations.id)
    *   `status` (Enum: pending, in_progress, completed)
    *   `report_url` (Text)
    *   `created_at` (Timestamp)
*   `implementations`
    *   `id` (UUID, PK)
    *   `org_id` (UUID, FK -> organizations.id)
    *   `name` (Text)
    *   `status` (Enum: planning, building, testing, approved)
    *   `budget` (Numeric)
    *   `approved_by` (UUID, FK -> users.id)
*   `agents`
    *   `id` (UUID, PK)
    *   `org_id` (UUID, FK -> organizations.id)
    *   `name` (Text)
    *   `avatar_url` (Text)
    *   `status` (Enum: active, paused)
    *   `gcp_endpoint` (Text)
    *   `config` (JSONB - sparar sliders, triggers, system prompt overrides)
    *   `daily_budget_limit` (Numeric)
*   `agent_logs`
    *   `id` (UUID, PK)
    *   `agent_id` (UUID, FK -> agents.id)
    *   `status` (Enum: success, error, running)
    *   `input_data` (JSONB)
    *   `output_data` (JSONB)
    *   `error_message` (Text)
    *   `run_duration_ms` (Integer)
    *   `cost` (Numeric)
    *   `created_at` (Timestamp)
*   `chats`
    *   `id` (UUID, PK)
    *   `org_id` (UUID, FK -> organizations.id)
    *   `agent_id` (UUID, FK -> agents.id, NULL för chatt med `hund`)
    *   `title` (Text)
    *   `created_at` (Timestamp)
*   `messages`
    *   `id` (UUID, PK)
    *   `chat_id` (UUID, FK -> chats.id)
    *   `sender_type` (Enum: user, agent, hund)
    *   `sender_id` (UUID, FK -> users.id, NULL om sender_type är agent/hund)
    *   `content` (Text)
    *   `created_at` (Timestamp)
