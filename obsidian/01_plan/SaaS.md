# StydeForge — B2B SaaS Implementation Plan
**Från lokalt raffinaderi till skalbar molntjänst**

Detta dokument beskriver den fullständiga arkitekturen, datamodellen, säkerhetsisoleringen och produktplanen för att kommersialisera **StydeForge** som en högpresterande B2B SaaS-plattform för företagskunder.

---

## 1. Översikt & Vision
Affärsmodellen bygger på en trestegsraket:
1. **Audit (20 000 kr)**: En djupgående, automatiserad analys av kundens digitala mognad och flaskhalsar med hjälp av `consultant-auditor`.
2. **Custom Build (99 000 - 399 000 kr)**: Skräddarsydd utveckling och optimering av specifika agenter i vårt lokala raffinaderi mot kundens egna data.
3. **SaaS Dashboard (Månadsprenumeration)**: En premium Next.js-applikation med ett ultra-rent glassmorfiskt gränssnitt där kunden kan styra, övervaka, chatta med och få leveranser från sina unika agenter.

---

## 2. Arkitektur (Moln-Infrastruktur)

För att garantera högsta säkerhet, skalbarhet och skydd mot dataläckage mellan kunder byggs molnplattformen på följande sätt:

```
┌────────────────────────────────────────────────────────┐
│               KUNDENS DASHBOARD (Next.js)              │
└───────────────────────────┬────────────────────────────┘
                            │ (HTTPS / WebSockets)
                            ▼
┌────────────────────────────────────────────────────────┐
│             BACKEND API GATEWAY (FastAPI)              │
└──────┬────────────────────┬────────────────────┬───────┘
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Auth &     │     │  Sandboxed   │     │  Enterprise  │
│  Postgres    │     │  Agent Run   │     │   LLM API    │
│  (Supabase)  │     │  (AWS Fargate│     │  (Zero Data  │
│              │     │  / Docker)   │     │  Retention)  │
└──────────────┘     └──────────────┘     └──────────────┘
```

### A. Databas & Lagring
*   **Huvuddatabas**: **Supabase (PostgreSQL)** för användarautentisering, prenumerationsstatus (Stripe), chatt-historik och metadata för agenter.
    *   *Säkerhetskrav*: Row-Level Security (RLS) aktiveras strikt på alla tabeller. Kund A:s konto kan aldrig exekvera frågor mot eller se Kund B:s data.
*   **Objektlagring**: **AWS S3** eller **Google Cloud Storage** för kundspecifika dokument, uppladdade CSV-filer och genererade PDF-rapporter.
    *   *Säkerhetskrav*: Alla filer sparas i krypterade hinkar (Buckets) med unika ID-strukturer (`/company_id/agent_id/file_id`). Åtkomst sker enbart via tidsbegränsade, säkra URL:er (Presigned URLs).

*   **Analys: Supabase vs. Bygga själv från grunden**
    Det går absolut att undvika Supabase och bygga allt själv. Många större företag gör detta för att slippa leverantörslåsning (vendor lock-in) och ha 100% kontroll. Här är stegen du hoppar över genom att välja Supabase, samt hur du bygger dem själv:
    
    | System | Vad Supabase ger dig direkt | Vad du måste bygga/konfigurera själv | Svårighetsgrad |
    | :--- | :--- | :--- | :--- |
    | **Databas** | Färdigkonfigurerad PostgreSQL med automatisk backup och webb-UI. | Installera och säkra en egen PostgreSQL-server (t.ex. på en VPS), konfigurera brandväggar, sätta upp automatisk backup till molnet (t.ex. pg_dump till S3) och optimera prestanda/indexering. | 🟡 Medium |
    | **Autentisering** | Säker inloggning, registrering, sessioner, JWT-tokens och Magic Links med färdiga API:er. | Implementera sessionshantering och JWT-generering i ditt backend (t.ex. med FastAPI Security eller Lucian-auth). Sätta upp en SMTP-server eller koppla en e-posttjänst (t.ex. Resend eller SendGrid) för att manuellt generera och validera Magic Link-tokens. Skydda mot brute-force-attacker. | 🔴 Svår |
    | **Filhantering** | Säker filuppladdning (Storage Buckets) med inbyggda RLS-säkerhetsregler. | Sätta upp en egen S3-kompatibel filserver (t.ex. MinIO) eller skriva egna API-endpoints i ditt backend för att ta emot filer, spara dem på disk/moln, generera tidsbegränsade nedladdningslänkar och kontrollera behörighet. | 🟡 Medium |
    | **Realtid** | Direkt synkning av databashändelser via WebSockets (för chatten). | Sätta upp en WebSocket-server (t.ex. med Socket.io eller FastAPIs inbyggda WebSockets) och bygga ett pub/sub-system (ofta med Redis under huven) för att strömma meddelanden och statusar från agenterna till klienten. | 🔴 Svår |
    
    *Slutsats*: Att bygga allt själv tar ca **2–3 veckor extra utvecklingstid** och ökar komplexiteten för drift och underhåll. Supabase låter dig driftsätta en säker, produktionsklar bakgrund på **några timmar**. För en MVP rekommenderas Supabase starkt, men arkitekturen i detta dokument gör det enkelt att migrera till en helt egen PostgreSQL/Redis-stack senare.


### B. Isolerad Agentexekvering (Sandboxing)
Eftersom kundens agenter kommer att köra kod och hantera stora mängder känslig information kan de inte köras direkt på huvudservern.
*   **Lösning**: Varje gång en agent kör en uppgift som kräver verktyg (t.ex. kör Python-kod, söker på webben eller genererar PDF) startas en isolerad **Docker-container** via **AWS ECS Fargate** eller **GCP Cloud Run**.
*   Containern har en tidsgräns (Timeout) på max 5 minuter, är helt strypt från att nå andra containrar på nätverket, och raderas permanent så fort uppgiften är slutförd.
*   **Detaljerad plan för Isolerad Agentexekvering (Sandboxing)**
    Det absolut säkraste och mest effektiva sättet att köra godtycklig kod och terminalverktyg från kunder är jag att använda **MicroVMs (t.ex. Firecracker)** eller **isolerade serverless Docker-containrar**.
    
    ##### Bästa lösningen: AWS ECS Fargate med tidsbegränsade containrar
    1.  **Triggning**: När en agent exekverar ett verktyg som kräver kodkörning (t.ex. Python-tolk eller filmanipulering) skickar vårt backend-API en begäran till AWS ECS API.
    2.  **Container-uppstart**: En minimal Docker-container (t.ex. baserad på Alpine Linux med endast Python och nödvändiga CLI-verktyg installerade) startas på 1–2 sekunder.
    3.  **Fil-inmatning**: De filer som agenten behöver bearbeta laddas ner från S3 till containerns temporära minne via en säker engångslänk.
    4.  **Isolerad exekvering**: Agenten kör sina beräkningar. Containern saknar åtkomst till AWS metadata-tjänster och kan inte nå databasen eller andra servrar. Den har en hård gräns på max 5 minuters körtid och 0.5 GB RAM för att undvika överbelastning (DDoS).
    5.  **Resultat & Nedstängning**: Det genererade resultatet (t.ex. en PDF eller JSON-data) laddas upp till S3. Containern stängs ner och allt temporärt minne skrivs över och raderas.
    
    ##### Tidsåtgång & Kostnad
    *   **Tidsestimat**: **5 arbetsdagar** för att bygga Docker-mallarna, konfigurera AWS ECS Fargate, skriva API-kopplingen i FastAPI samt testa isoleringen.
    *   **Kostnad**: 
        *   *Utveckling*: Ca 40 timmars arbete.
        *   *Drift*: AWS Fargate tar endast betalt per sekund containern körs. Med en genomsnittlig körtid på 10 sekunder per uppgift kostar 10 000 agentkörningar mindre än **50 SEK per månad**. Extremt kostnadseffektivt.

### C. LLM & Integritet (Privacy Routing)
*   **Extern routing**: Alla anrop till DeepSeek, OpenAI eller Anthropic går via Enterprise-kontrakt med **Zero Data Retention** (ingen loggning eller träning hos tredjepart).
*   **Intern routing (Enterprise-kunder)**: För kunder med extrema sekretesskrav driftsätts privata modeller (t.ex. *Llama-3-70B* eller *DeepSeek-Coder*) på egna virtuella maskiner i kundens egna moln (VPC) via **vLLM** eller **Ollama**.

---

## 3. Kundens Dashboard (Next.js + Glassmorphism)

Gränssnittet ska bygga vidare på din Next.js-prototyp i `C:/Users/William/styde.ai/apps/dashboard` men lyftas till en ultra-premium designnivå med **minimalistisk glassmorfism**.
*   **Arkitektur för hög anpassningsbarhet (Högst Customizable)**
    För att webbappen ska vara extremt enkel att redigera och anpassa efter hand bygger vi den med en **modulär komponentstruktur**:
    *   **Tailwind CSS v4 & CSS-variabler**: Alla färger (inklusive accenten `#C65D26` och glas-effekterna) styrs via globala CSS-variabler i `globals.css`. Vill du ändra färgtema eller glaseffekter ändrar du på ett enda ställe.
    *   **shadcn/ui + Tailwind-anpassning**: UI-komponenter (knappar, inputfält, paneler) hålls helt oberoende och frikopplade från affärslogiken. De byggs som "rena" gränssnittet-komponenter i mappen `components/ui`.
    *   **Designplanering**: Innan vi skriver en enda rad kod kommer vi att göra en fullständig analys av dina inspirationsbilder, spika layouten och definiera alla UI-komponenter för att säkerställa att designen är 100% spikad.

### Designestetik (UI/UX)
*   **Bakgrund**: Djup, mörk rymdgrå/svart (`#030307` till `#080810`) med subtila, roterande färgglober i bakgrunden (blurrade mesh-gradients).
*   **Glas-paneler**: Halvtransparenta ytor (`backdrop-filter: blur(20px)`) med mycket tunna, ljusa kanter (`border: 1px solid rgba(255, 255, 255, 0.05)`) och runda hörn (`border-radius: 16px` eller `24px`).
*   **Typografi**: Modern sans-serif (t.ex. *Geist Sans*, *Inter* eller *Outfit*) med gott om luft (whitespace).
*   **Micro-animations**: Mjuka hover-effekter och transitions (t.ex. `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`).

### Dashboardens Nyckelfunktioner
1.  **Agent Hub (Startskärmen)**: En visuell översikt över företagets tillgängliga agenter. Varje agent visas som ett premium "kort" i glas med dess nuvarande status (t.ex. *Idle*, *Analyzing*, *Generating Report*).
    *   **Login-bakgrund (Konst & Anpassning)**: Login-skärmen använder en full-bleed bakgrundsbild. I admin-panelen (William Only) bygger vi ett enkelt gränssnitt där du kan ladda upp egna högupplösta bilder eller konstverk. Bilderna sparas i en offentlig Supabase Storage-bucket, och login-sidan laddar dynamiskt in den senast aktiverade bilden med en mjuk fade-in vid sidladdning. 
2.  **Live Workspace (Chattgränssnitt)**:
    *   **Mjuk scroll-animation vid login**: När användaren anger sin e-post/magic link och loggar in, döljs inte bara login-kortet. Sidan rullar mjukt och sömlöst nedåt (JS-animerat) och avslöjar den mörka, exklusiva kontrollpanelen under.
    *   **Clean Chat Canvas (Högkontrast)**: Själva chattrutan där AI-svar visas är en stor, minimalistisk, kritvit eller ljusbeige yta (`#FFFFFF` eller `#F9F9FB`) med generösa runda hörn (`border-radius: 24px`). Detta bryter av dramatiskt mot den djupa skiffergrå bakgrunden och ger en oerhört ren och premium läsupplevelse.
    *   **Rundad Chat-input**: Inuti den ljusa chattrutan (snyggt svävande eller placerad i botten) ligger ett helt runt inputfält med glas-effekt, utrustat med genvägar (t.ex. för att kalla in specifika agenter eller bifoga dokument).
    *   **Agent-bubblor**: Klickbara, runda bubblor i gränssnittet visar vilka agenter som är tillgängliga, deras specifika uppgifter och deras status (aktiv/inaktiv). Genom att klicka på en agent-bubbla startas en dedikerad chatttråd direkt med just den agenten.
    *   **Live Work Log**: När en agent arbetar med en uppgift visas en snygg tidslinje (t.ex. *🔍 Hämtar data...* -> *📊 Kör analys...* -> *✍️ Genererar PDF...*) så att kunden ser exakt vad den gör i realtid. 
3.  **Deliverables Library (Dokumentbank)**: En dedikerad flik där alla genererade rapporter, CSV-filer och dataanalyser listas chronologiskt med direktlänk för nedladdning.
4.  **Integrations Center**: Enkel hantering av anslutningar till kundens egna verktyg (Google Drive, SharePoint, Slack, Salesforce, SQL-databaser).
5.  **Analytics & ROI**: Enkel visualisering av hur mycket tid och pengar agenterna sparar åt företaget (baserat på körtid och utförda uppgifter).

---

## 4. Prenumerationsnivåer (3 Tiers)

För att driva återkommande månadskostnader (MRR) delas tjänsten in i tre tydliga abonnemang:

| Funktion | Basic | Pro | Enterprise |
| :--- | :--- | :--- | :--- |
| **Pris** | ~4 900 kr / mån | ~14 900 kr / mån | Offert (39 000+ kr/mån) |
| **Målgrupp** | Mindre bolag / Startskott | Mellanstora bolag | Storföretag / Bank / Finans |
| **Antal Agenter** | Upp till 2 standardagenter | Upp till 5 anpassade agenter | Obegränsat / Helt skräddarsydda |
| **Antal Körningar** | 200 per månad | 1 500 per månad | Obegränsat |
| **Dataisolering** | Delad molndatabas (RLS) | Delad molndatabas (RLS) | Helt dedikerad databas & lagring |
| **LLM-avtal** | Enterprise API | Enterprise API | Egen lokal LLM i privat moln (VPC) |
| **Support & Optimering**| E-postsupport (24h) | Prioriterad support (4h) | Personlig AI-tekniker & SLA |
| **Smarter-over-time** | Månadsvis uppdatering | Veckovis uppdatering | Realtidsoptimering via Forge |

---

## 5. Kopplingen till StydeForge (Continuous Learning)

Det är här du levererar på löftet om att kunden får **"system som blir smartare med tiden"** helt automatiskt:

```
[ Dashboard (Kund upptäcker fel) ]
               │
               ▼ (1. Felrapport skickas till molnet)
[ Molndatabas (Lagrar felaktigt indata + förväntat utdata) ]
               │
               ▼ (2. Hämtas vid nästa synk)
[ StydeForge lokalt (Lägger till nytt benchmark och kör Forge-loop) ]
               │
               ▼ (3. Lärar-agenten fixar instruktionerna och verifierar)
[ Ny blueprint skapas & versionsbumpas (t.ex. v1.1.0) ]
               │
               ▼ (4. Laddas upp till Moln-Registry)
[ Dashboard (Kundens agent uppdateras direkt till den smartare versionen) ]
```

1.  **Felrapportering**: Om en agent gör fel i kundens dashboard kan kunden klicka på *"Korrigera"* och skriva vad som blev fel (t.ex. *"Momsen blev felberäknad för utländsk valuta"*).
2.  **Benchmark-generering**: Detta felaktiga indata (fakturan) och korrigeringen sparas i molnet.
3.  **Forge-raffinering**: Du synkar ner dessa felrapporter till ditt lokala **StydeForge-raffinaderi** där de automatiskt läggs till som nya testfall under `eval/benchmarks/`.
4.  **Automatisk träning**: Du kör [Core/forge.py](file:///C:/Users/William/styde.ai/_alpedal/styde-forge/Core/forge.py) i en loop. [Core/teacher.py](file:///C:/Users/William/styde.ai/_alpedal/styde-forge/Core/teacher.py) hittar rotorsaken, skriver om blueprintens instruktioner och verifierar att agenten nu klarar det nya fallet utan att förstöra de gamla testerna.
5.  **Uppdatering**: Den uppdaterade blueprinten (`v1.1.0`) laddas upp till molnet och kunden har direkt tillgång till en smartare agent i sin dashboard – helt utan manuellt kodarbete för dig.

---

## 6. Implementation Roadmap (6 veckor)

### Vecka 1: Infrastruktur & Databas (Supabase)
*   Sätt upp Supabase-projektet med strikta Row-Level Security (RLS) regler.
*   Bygg databas-scheman för företag, användare, agenter, chatt-sessioner och dokumentlagring.
*   Konfigurera Supabase Auth för säker inloggning.

'Supabase is an open-source, "Backend-as-a-Service" (BaaS) that ==replaces the need to build and manage a backend from scratch==. It provides developers with a complete, production-ready backend suite consisting of five main tools: [](https://www.newline.co/@zaoyang/what-is-supabase-and-how-it-can-replace-your-entire-backend--62b84205)

- **Database:** A full, managed [PostgreSQL](https://supabase.com/docs/guides/database) instance that gives you the power and flexibility of a traditional SQL database.
- **Authentication:** Built-in [Authentication](https://supabase.com/docs/guides/auth) for managing user sign-ups, logins, and access control, supporting email, magic links, social OAuth (Google, GitHub, etc.), and multi-factor authentication.
- **Storage:** [Storage](https://supabase.com/docs/guides/storage) buckets for organizing and serving large files (images, videos, or documents) with secure access rules
- **Edge Functions:** [Edge Functions](https://supabase.com/docs/guides/functions) that let you run custom backend code securely without needing to provision or manage servers.
- **Realtime:** Features for building multiplayer, collaborative, or instant-update experiences using [Realtime](https://supabase.com/docs/guides/realtime) data synchronization. [](https://supabase.com/)

==Developers primarily use Supabase to ship modern web and mobile applications incredibly fast== without getting bogged down in infrastructure, complex database management, or creating their own authentication and API layers.


### Vecka 2: Skalbart API & Chatt-streaming
*   Bygg backend-API (FastAPI) i molnet.
*   Implementera strömmande textsvar (Server-Sent Events eller WebSockets) för chatten.
*   Sätt upp kopplingar för Enterprise API:er (OpenAI/DeepSeek) med noll datalagring.

### Vecka 3: Sandboxing & Verktygskörning
*   Skapa Docker-mallar för agenternas verktygskörning (filhantering, Python-analys).
*   Sätt upp AWS Fargate/GCP Cloud Run för att starta och stänga containrar dynamiskt på säkert avstånd från databasen.
*   Sätt upp säker S3/GCS-lagring för genererade dokument.

### Vecka 4: UI/UX (Next.js Premium Glassmorphism)
*   Migrera din Next.js-prototyp från [apps/dashboard](file:///C:/Users/William/styde.ai/apps/dashboard) till det nya premium-temat.
*   Implementera glassmorfiska komponenter, transitions, samt live-laddningsindikatorer för agenternas verktygskörning (Work Log).
*   Bygg inloggningssidan och Agent Hub-vyn.

### Vecka 5: StydeForge-bron (Continuous Learning)
*   Bygg export- och synkskript mellan det lokala raffinaderiet och moln-Registryt.
*   Bygg flödet för felrapportering: från kundens dashboard -> sparas i molnet -> laddas ner till lokal `eval/benchmarks/` -> körs i Forge-loop -> pushas upp igen.

### Vecka 6: Stripe-koppling & Lansering
*   Koppla Stripe Billing för att hantera prenumerationsnivåerna (Basic, Pro, Enterprise).
*   Gör E2E-säkerhetstester för att garantera att ingen data kan läcka mellan konton.
*   Lansera Beta till de första audit-kunderna!