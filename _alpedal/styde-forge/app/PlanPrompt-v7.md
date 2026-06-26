# PrecisionForge — Sammanställd Analys & Åtgärdsplan v7
## 6 agenter analyserade, 20 subagenter tillgängliga — 2026-06-26
### v4: +3 selektiva förbättringar från granskningsrunda 3 — circular spawn guard, aktiv checkpoint-resume, dispatcher rate-limiting
### v5: ingen ändring — planen mognade. v6: +3 selektiva lyft från HybridStruktur-v5 + förbättringsförslag-v2 (innehållsförteckning, SSE backoff, graceful degradation)
### v7: +Fas 0.5 Design Mockups (10 unika, innan kod byggs), kapacitet uppdaterad till 20 subagenter, +2M tokens budget

---

## INNEHÅLLSFÖRTECKNING

1. [Sammanfattning](#sammanfattning-6-agenter-analyserade-koden)
2. [🔴 Kritiska buggar](#-kritiska-buggar--måste-fixas-först)
3. [🟠 Höga buggar](#-höga-buggar)
4. [🟡 Medium buggar](#-medium-buggar)
5. [🟢 Låga / Strukturella](#-låga--strukturella)
6. [Åtgärdsplan — Prioriterad ordning](#åtgärdsplan--prioriterad-ordning)
   - [Infrastruktur & Säkerhetsåtgärder](#-infrastruktur--säkerhetsåtgärder--görs-före-fas-1)
   - [Fas 0.5: Design Mockups](#fas-05-design-mockups-1-dag)
   - [Fas 1: Kritiska buggar + Död kod + Infrastruktur](#fas-1-kritiska-buggar--död-kod--infrastruktur-1-2-dagar)
   - [Fas 1.5: State-migrering](#fas-15-state-migrering-05-dagar)
   - [Fas 2: Refaktorering](#fas-2-refaktorering-2-3-dagar)
   - [Fas 2.5: Test Hardening](#fas-25-test-hardening-1-2-dagar)
   - [Fas 3: Dashboard Control Plane](#fas-3-dashboard-control-plane-3-4-dagar)
   - [Fas 4: Workflow & Automation](#fas-4-workflow--automation-2-dagar)
   - [Fas 5: Agent-träning](#fas-5-agent-träning-2-3-dagar)
   - [Fas 6: Hardening & Release](#fas-6-hardening--release-2-dagar)
7. [Git-strategi & Rollback](#git-strategi--rollback)
8. [State Management](#state-management--konkreta-förbättringar)
9. [Hermes Orchestrator](#hermes-orchestrator--arkitektur--regler)
10. [Oberoende Evaluator-agent](#oberoende-evaluator-agent-ny--införs-pre-fas-1)
11. [Dokumentationskrav](#dokumentationskrav-nytt)
12. [Tidsestimat](#tidsestimat-uppdaterad)
13. [Bilaga: Bug → Fas → Batch snabbreferens](#bilaga-bug--fas--batch-snabbreferens)

---

## SAMMANFATTNING: 6 agenter analyserade koden parallellt — 2026-06-26

**Kapacitet:** Hermes har tillgång till upp till **20 subagenter** samtidigt via `delegate_task` (`max_concurrent_children: 20`). Subagenter är leaf-only (kan inte skapa egna subagenter), isolerade, och efemära.

### Analyserat:
- **Delegate 1:** Core Python (31 filer, ~15,000 LOC) — 13 API-anrop, 164s
- **Delegate 2:** Dashboard (server + HTML, 1,755 LOC) — 7 API-anrop, 205s
- **Delegate 3:** State management + dataflöde (state.yaml 220KB, 7990 rader) — 11 API-anrop, 193s
- **Forge:** code-reviewer (87.8/100), consultant-auditor (84.6), dependency-mapper (86.4) — pågår

---

## 🔴 KRITISKA BUGGAR — MÅSTE FIXAS FÖRST

| # | Bug | Fil | Impact |
|---|-----|-----|--------|
| 1 | Cache-inkonsekvens i hermes_bridge.py | hermes_bridge.py:83-97 | Cache gör lookup med otrunkerad prompt, API får trunkerad → ständiga cache-missar |
| 2 | Inverterad markdown-logik i agent_runner.py | agent_runner.py:116 | Strippar markdown när caveman ÄR PÅ — tvärtom mot forge.py |
| 3 | test_spawn.py importerar 7 ej existerande funktioner | tests/test_spawn.py:8-15 | Hela testfilen (376 rader) är död kod |
| 4 | state["evaluations"] = [] men total_evaluations = 146 | forge.py:724 | ALL eval-data försvinner från state — sparas bara i individuella eval.yaml |
| 5 | Race condition i parallel loop | state.py + forge.py | Varje tråd gör load→modify→save utan trådskydd → datakorruption |
| 6 | XSS: unsafe-inline CSP + innerHTML utan escaping | server_8765.py:67 + HTML | Godtycklig JS-exekvering möjlig via blueprint-namn, detaljer etc. |

## 🟠 HÖGA BUGGAR

| # | Bug | Impact |
|---|-----|--------|
| 7 | forge.py: spawn+eval-logik duplicerad 3 gånger | Kodduplicering → buggar synkas inte mellan kopior |
| 8 | isinstance(list) saknas på 3+ state.get("agents") | TypeError om state.yaml har int istället för list |
| 9 | nvidia-smi blockerar HTTP-servern synkront | Dashboard fryser 1-3s vid varje GPU-poll |
| 10 | subprocess.Popen utan PID-spårning | Zombie-processer, ingen cleanup |
| 11 | CSRF-token förfaller efter 30min utan renewal | POST-anrop slutar fungera |
| 12 | blueprint.py + quality_gates.py: ~80% identisk validering | Duplicerad logik |
| 13 | _count_consecutive_passes: except Exception: pass | Sväljer ALLA fel — PermissionError, YAML-fel, etc. |

## 🟡 MEDIUM BUGGAR

| # | Bug |
|---|-----|
| 14 | 62 av 751 agents saknar spawned_at — omöjligt spåra historik |
| 15 | 0 av 751 agents har composite_score i state — scores finns bara i eval.yaml per run |
| 16 | termSeen Set växer obegränsat — minnesläcka |
| 17 | fetchState(): catch(e) {} — fel döljs helt, auto-refresh fortsätter vid serverfel |
| 18 | dashboard.py: 1069 LOC med ~500 rader HTML inbäddad i Python-sträng |
| 19 | generate.py saknas — refereras men existerar inte i projektet |
| 20 | 15 hårdkodade "deepseek-v4-flash" i forge.py |
| 21 | FORGE_ROOT duplicerad i 17 av 22 moduler |

## 🟢 LÅGA / STRUKTURELLA

| # | Problem |
|---|---------|
| 22 | forge.py: 1574 LOC monolit — borde vara 5-8 moduler |
| 23 | filestore.py: ~800 rader död kod (S3/R2/GCS-backends oanvända) |
| 24 | agent_runner.py anropas ALDRIG från forge.py — död kod |
| 25 | Inga WCAG/ARIA-attribut i dashboard-HTML |
| 26 | prefers-reduced-motion ignoreras — animationer körs alltid |
| 27 | Färgkontrast: --text-faint #3A3A5C → 2.5:1 (WCAG AA kräver 4.5:1) |
| 28 | 16 av 22 Core-moduler har 0 tester (27% modultäckning, ~15% kodtäckning) |
| 29 | localhost-bindning → kan inte nås från mobil/andra enheter |
| 30 | Ingen rate-limiting → kan starta 100+ subprocesser via snabba POST |

---

## ÅTGÄRDSPLAN — PRIORITERAD ORDNING

### ⚠️ INFRASTRUKTUR & SÄKERHETSÅTGÄRDER — GÖRS FÖRE FAS 1

**A. Git-init + branch-strategi:**
- `git init` + första commit av nuvarande state på `main`
- Skapa `feature/` branches för riskabla ändringar (state-migration, forge-splittring)
- Merge till main först efter verifierad batch — ingen linjär historik på riskabla operationer
- `git tag` per fas: `v0.2.0-fas1`, `v0.3.0-fas2`, etc.

**B. Secrets scanning — pre-commit hook:**
- Installera `git-secrets` eller motsvarande — skanna efter API-nycklar, tokens, lösenord före varje commit
- Förhindrar att secrets läcker in i git-historik — komplement till Fas 6

**C. DRY-RUN-läge för destruktiva operationer:**
- State-migration, massändringar, `git rm` — kör ALLTID dry-run först
- Skriv vad som SKULLE ändras → verifiera manuellt → kör sedan
- Gäller särskilt: Fas 1.5 (migration), Fas 2 (refaktorering), borttagning av död kod

**D. Död kod: beroendeanalys före borttagning:**
- Innan `git rm` på agent_runner.py, filestore.py-backends: kör `rg "import agent_runner|from agent_runner|from filestore import"` över HELA kodbasen
- Bekräfta 0 importer → radera. Vid träff → utred först

**E. Oberoende evaluator-agent + golden test set:**
- Skapa EN agent som INTE deltar i träning — körs mot fast "golden test set" med kända svar
- Kalibreras EN gång, ändras aldrig. Används för att detektera score-drift över tid
- Utan denna → co-evolution garanterad: agenter lär sig vad andra agenter vill ha, inte vad uppgiften kräver
- Golden test set: 20-30 uppgifter med facit — täcker spawn, eval, kodgranskning, säkerhet

**F. Disk quota-övervakning — från dag 1:**
- Max 10GB för state/ + backups/ + logs/ + .git/
- Vid 80% → alert till Hermes. Vid 95% → auto-cleanup äldsta backups
- State.yaml backups behålls (max 10), men äldre eval.yaml per run kan roteras

**G. Modell-abstraktionslager (Core/config.py):**
- ALLA modellnamn i EN fil: `Core/config.py`
- ALLA API-anrop går genom EN adapter — vid modellbyte: ändra 1 rad, inte 15+
- Inkludera: modellnamn, provider, API-endpoint, timeout, max_tokens

**H. Kostnadsprognos per fas:**
- Estimera $ per fas baserat på token-budget × provider-pris (deepseek: ~$0.14/1M input, ~$0.28/1M output)
- Fas 1 (500K): ~$0.10-0.20 | Fas 2 (800K): ~$0.15-0.30 | Fas 3 (1.2M): ~$0.25-0.45 | Totalt ~$1.50-3.00
- Beslut om "värt det?" fattas INNAN körning — inte efter

---

### Fas 0.5: Design Mockups (0.5 dag) — INNAN NÅGON KOD BYGGS

**Syfte:** Skapa 5 unika, extremt väldesignade mockups för Styde/Forge-gränssnittet innan implementation påbörjas. **Inga templates. Inga named themes. Inga "i stil med X".** Varje subagent skapar något helt eget och originellt.

**Två målytor — 2 desktop + 3 web:**
- **2 mockups för Styde-Forge.exe** — native desktop-app (Tauri-baserad, Windows-native känsla)
- **3 mockups för https://Styde.se/Forge** — web-app, del av större styde.se-sajt. Varje web-mockup ska inkludera grundläggande styde.se-navigering/header för att visa hur Forge passar in i den större sajtstrukturen.

**Metod:** Hermes dispatchar 5 specialiserade design-subagenter. Varje subagent får INTE en fördefinierad stil — de ska själva skapa något unikt och originellt. Subagenterna är hybrid-subagenter som kombinerar StydeAgents (frontend-component-builder, dashboard-themer, motion-design-spec-writer, dark-mode-architect) med externa skills (high-end-visual-design, frontend-design, ui-ux-pro-max, web-design-guidelines).

**Hermes använder ALLA tillgängliga verktyg:**
- **StydeAgents:** dashboard-layout-architect (92), frontend-component-builder (92), dashboard-themer (93), dark-mode-architect (94), motion-design-spec-writer (93), color-system-designer (91), typography-systems-designer (91), animation-design-engineer, design-system-architect (89)
- **Skills (Hermes):** high-end-visual-design, frontend-design, ui-ux-pro-max, web-design-guidelines, minimalist-ui, design-taste-frontend, swiss-design, industrial-brutalist-ui, interface-design, interaction-design, transitions-dev, make-interfaces-feel-better, oklch-skill, excalidraw, p5js, popular-web-designs, tauri-development
- **Verktyg:** delegate_task (upp till 20 subagenter samtidigt efter sessionsomstart), hybrid-subagenter som slår ihop 2+ design-agenter

**5 mockups — alla originella, inga templates, inga named themes:**

| # | Målyta | Instruktion till subagent |
|---|--------|--------------------------|
| 1 | **Styde-Forge.exe** | Skapa en helt originell desktop-app design. Inga referenser till kända stilar. Native-känsla. |
| 2 | **Styde-Forge.exe** | Skapa en HELT ANNAN originell desktop-app design. Får inte likna #1. Native-känsla. |
| 3 | **Styde.se/Forge** | Skapa en helt originell web-app design med styde.se-header. Inga referenser. |
| 4 | **Styde.se/Forge** | Skapa en HELT ANNAN originell web-app design med styde.se-header. Får inte likna #3. |
| 5 | **Styde.se/Forge** | Skapa en HELT ANNAN originell web-app design med styde.se-header. Får inte likna #3 eller #4. |

**Definition of Done — Fas 0.5:**
- [ ] 5 HTML-filer i `D:\mockups\` — alla öppningsbara i webbläsare
- [ ] 2 desktop-mockups (exe-känsla, native gränssnitt, titlebar, system tray-ikon)
- [ ] 3 web-mockups med styde.se-header/navigering för att visa sajtstruktur
- [ ] Varje mockup har minst: System Overview, Agent Status, Activity Feed, GPU Monitor
- [ ] **ALLA 5 är HELT olika varandra** — ingen named theme, ingen "i stil med", inget template-tänk
- [ ] Alla mockups är självständiga HTML-filer (inline CSS/JS)
- [ ] Hermes granskar alla 5 och väljer 1 desktop + 1 web som favoriter för vidareutveckling
- [ ] Token-budget: max 1M tokens (~$0.20-0.40)

**Leverans:** `D:\mockups\` med 5 HTML-filer. Hermes väljer topp 1 desktop + 1 web som grund för implementation.

---

### Fas 1: Kritiska buggar + Död kod + Infrastruktur (1-2 dagar)

**Åtgärder:**
1. Fixa cache-inkonsekvens i hermes_bridge.py (#1)
2. Fixa inverterad markdown-logik i agent_runner.py (#2)
3. Radera/skriv om test_spawn.py (#3)
4. Återställ evaluations.append i cmd_loop (#4)
5. Inför trådsäkert state-access — threading.Lock (#5)
6. Ta bort unsafe-inline från CSP + byt innerHTML → textContent (#6)
7. Radera död kod: filestore.py S3-backends, agent_runner.py — EFTER beroendeanalys (se Infrastruktur D)
8. PID-register i forge.py + `atexit.register(cleanup_zombies)` (#10)
9. Rate-limiting: token-bucket i servern, max 5 spawn/minut (#30)

**Infrastruktur (görs FÖRE första buggfixen):**
- `requirements.txt` med låsta versioner (Python 3.11+)
- `D:\API_SPEC.md` — definiera alla endpoints, metoder, payloads, felkoder för Fas 3

**Definition of Done — Fas 1:**
- [ ] Alla 6 kritiska buggar har patch + verifierats av Hermes
- [ ] Död kod borttagen — `git rm` genomfört EFTER beroendeanalys
- [ ] Rate-limiting + PID-spårning på plats
- [ ] `requirements.txt` existerar med låsta versioner
- [ ] `Core/config.py` existerar — alla modellnamn + provider-konfig samlade (modell-abstraktionslager)
- [ ] `API_SPEC.md` ifylld med alla endpoints
- [ ] `python -m pytest tests/` — 0 failures (exklusive test_spawn.py)
- [ ] Systemet startar och är körbart
- [ ] Git commit + tag `v0.2.0-fas1`
- [ ] Token-budget Fas 1: max 500K tokens (~$0.10-0.20)

### Fas 1.5: State-migrering (0.5 dagar)

**Varför:** state.yaml måste migreras innan refaktorering — ny struktur kan inte samexistera med gammal kod.

**Åtgärder:**
1. **Stoppa forge.py helt** — verifiera att inga forge-processer körs (`ps aux | grep forge`). Döda eventuella kvarvarande.
2. Backup: `state.yaml → state.yaml.backup-YYYYMMDD-HHMM` (behåll senaste 10)
3. **Ta semantisk checksumma FÖRE migration:** antal agents, total_evaluations, medelscore, antal runs
4. **Kör DRY-RUN först** — visa vad som kommer ändras, verifiera manuellt
5. Kör migrationsscript: flerfils-arkitektur (agents.yaml, evaluations.yaml, activity.yaml)
6. Lägg till `composite_score` + `version` i varje agent-post
7. Bygg `run_id → agent` index för O(1) lookup
8. Räkna om composite_score för alla 751 agents från eval.yaml-filer
9. Skriv `state_version: 2` i state.yaml
10. **Verifiera semantisk ekvivalens:** jämför checksummor EFTER migration — antal agents, total_evaluations, medelscore. Alla måste matcha. Vid avvikelse → rollback från backup
11. Verifiera: `python -m pytest tests/test_state_migration.py`
12. Starta om forge.py — verifiera att spawn + eval fungerar

**Definition of Done — Fas 1.5:**
- [ ] State.yaml migrerad till version 2 utan datakorruption
- [ ] Semantisk verifiering passerad — nyckeltal identiska före/efter
- [ ] Alla 751 agents har composite_score + version
- [ ] run_id-index fungerar — O(1) lookup verifierad
- [ ] Backup sparad, senaste 10 behållna
- [ ] Git commit + tag `v0.2.5-state-migration`
- [ ] Token-budget Fas 1.5: max 200K tokens

### Fas 2: Refaktorering (2-3 dagar)

**Åtgärder:**
1. Extrahera duplicerad spawn/eval-logik från forge.py (3 kopior → 1) (#7)
2. isinstance-skydd på ALLA state.get() i forge.py + dashboard (#8)
3. Byt localhost → 0.0.0.0 + lägg CORS-headers (#29)
4. **Core/config.py utökas:** extrahera ALLA 15+ hårdkodade värden — modellnamn, FORGE_ROOT, paths, defaults (#20, #21). Modell-abstraktionslager: alla API-anrop via adapter, en rad vid modellbyte
5. Fixa CSRF-token renewal i dashboard-JS (#11)
6. Splittra forge.py (1574 LOC → kommandon/ + engine/) (#22)
7. Slå ihop duplicerad validering (blueprint + quality_gates) (#12)
8. Flytta dashboard-HTML till separat fil (#18)
9. Byt nvidia-smi till async — dashboard fryser inte längre (#9)
10. Fixa _count_consecutive_passes — specifika exceptions, inte bare except (#13)
11. **Prompt injection-skydd:** sanitera agent-output innan den skickas som context till subagenter. Stryp "IGNORE ALL PREVIOUS INSTRUCTIONS" och liknande mönster

**Definition of Done — Fas 2:**
- [ ] forge.py < 400 LOC huvudfil — resten i kommandon/ + engine/
- [ ] Dashboard-HTML i egen fil, inte i Python-sträng
- [ ] `python -m pytest tests/` — 0 failures
- [ ] Dashboard svarar inom 200ms (mätt med `time curl`)
- [ ] Alla 15+ hårdkodade värden i Core/config.py — modell-abstraktionslager aktivt
- [ ] Prompt injection-sanitization på plats
- [ ] Git commit + tag `v0.3.0-fas2`
- [ ] Token-budget Fas 2: max 800K tokens (~$0.15-0.30)

### Fas 2.5: Test Hardening (1-2 dagar)

**Mål:** Höj modultäckning från 27% → 60%+. Minimum 1 test per fixad bugg. Regressionstester för kritiska flöden.

**Åtgärder:**
1. Skriv tester för alla 6 kritiska buggfixar från Fas 1
2. Skriv tester för state-migration (Fas 1.5)
3. Skriv tester för Core/config.py + validering
4. Rök-testsvit: `spawn → eval → loop` på en känd agent — verifiera konsekvent resultat
5. Regressionstest: kör rök-testsviten — jämför output före/efter Fas 2
6. Dokumentera testinstruktioner i `tests/README.md`

**Definition of Done — Fas 2.5:**
- [ ] ≥60% modultäckning (`pytest --cov` rapporterar)
- [ ] Alla kritiska buggfixar har minst 1 verifierande test
- [ ] Rök-testsvit passerar — output identisk före/efter refaktorering
- [ ] `tests/README.md` beskriver hur man kör testerna
- [ ] Git commit + tag `v0.3.5-test-hardening`
- [ ] Token-budget Fas 2.5: max 400K tokens

### Fas 3: Dashboard Control Plane (3-4 dagar)

**Förarbete:** `API_SPEC.md` skapades i Fas 1 — följ den specen.

**Åtgärder:**
1. Bygg API-endpoints enligt API_SPEC.md (spawn, loop, kill, edit blueprint)
2. Dashboard-kontroller (knappar, blueprint-editor)
3. PWA-stöd (manifest.json, service worker) — inkludera cache-busting + "ny version tillgänglig"-notis vid deployment (#12)
4. SSE istället för polling (sse-stream-engineer) — med exponential backoff + jitter vid återanslutning för att förhindra reconnection storm (#11)
5. Basic auth på dashboard — skydda mot obehörig åtkomst
6. Input-validering på alla API-endpoints
7. WCAG/ARIA-attribut i dashboard-HTML (#25)
8. prefers-reduced-motion respekteras (#26)
9. Färgkontrast fixad → minst 4.5:1 (#27)

**Definition of Done — Fas 3:**
- [ ] Alla endpoints i API_SPEC.md implementerade + testade
- [ ] Dashboard-kontroller fungerar: spawna, loopa, döda, editera blueprint
- [ ] SSE levererar realtidsuppdateringar — ingen polling kvar
- [ ] PWA installerbart — manifest.json + service worker fungerar
- [ ] Basic auth aktivt — dashboard kräver inloggning
- [ ] Lighthouse accessibility score ≥ 90
- [ ] Graceful degradation: dashboard visar cachelagrat senaste state + "System unavailable"-indikator när forge.py är nere (#33)
- [ ] Git commit + tag `v0.4.0-fas3`
- [ ] Token-budget Fas 3: max 1.2M tokens (~$0.25-0.45)

### Fas 4: Workflow & Automation (2 dagar)

**Konkreta leveranser:**
1. **Agent pipeline:** Automatisera spawn → eval → improve → promote (refinery→production vid ≥85/100 i 3 konsekutiva)
2. **Scheduled audits:** Cron-liknande schema — code-review var 4h, security-scan var 12h
3. **Alert-hooks:** Webhook/logg vid kritiska fel (state-korruption, agent-krasch, >3 konsekutiva fails)
4. **Dashboard-notiser:** Visa alerts i realtid via SSE
5. **Anomaly detection på agent-scores:** Moving average + threshold — alert om score förändras >2 standardavvikelser på en vecka. Fånga divergens tidigt, inte först i Fas 5

**Definition of Done — Fas 4:**
- [ ] `forge.py pipeline <agent-name>` — kör hela spawn→eval→improve→promote i ett kommando
- [ ] Schemalagda audits körs automatiskt — verifiera via logg
- [ ] Alert-hook triggar vid simulerat state-fel
- [ ] Anomaly detection aktivt — alert vid score-fall
- [ ] Dashboard visar alert-notiser
- [ ] Git commit + tag `v0.5.0-fas4`
- [ ] Token-budget Fas 4: max 600K tokens

### Fas 5: Agent-träning (2-3 dagar)

**Viktigt:** Forge loop-parallel startas SOM BAKGRUNDSPROCESS redan i Fas 1. När Fas 5 börjar har agenterna redan 5-7 dagars träning. Anomaly detection (Fas 4) övervakar under tiden — alert vid score-ras >20 poäng.

**Åtgärder:**
1. Starta `forge.py loop-parallel` på alla refinery-agenter i bakgrunden (Fas 1)
2. Övervaka träningen via dashboard + anomaly detection (Fas 3-4)
3. Fas 5: Slututvärdera — vilka agenter nådde ≥85/100?
4. **Oberoende evaluator-agent granskar:** kör golden test set mot promotionskandidater — verifiera att scores inte är co-evolution-drivna
5. Promota agenter från refinery → production (endast om oberoende evaluator godkänner)
6. Skapa nya blueprints för saknade specialiseringar
7. Hybrid-agent-validering: A/B-testa hybrid mot original-agenterna

**Hybrid-validering (förbättrad — kräver statistisk signifikans):**
- **Minst 10 olika uppgifter** (inte en enda — en jämförelse är brus)
- Samma 10 uppgifter → original agent A, original agent B, hybrid
- Jämför medelvärde + standardavvikelse
- Hybrid måste vara ≥ bästa original MED signifikant marginal (≥0.5 standardavvikelser bättre, eller likvärdig med lägre token-åtgång)
- Underkänd hybrid → iterera blueprint eller förkasta

**Agent lifecycle management:**
- **Max agenter:** 2000 totalt (refinery + production)
- **Retirement:** Agenter med score <70 i >14 dagar → arkiveras automatiskt
- **Cleanup:** Runs äldre än 90 dagar → komprimeras
- Förhindrar agent-explosion och evig tillväxt

**Definition of Done — Fas 5:**
- [ ] ≥3 agenter har promoterats från refinery → production (verifierade av oberoende evaluator)
- [ ] Alla hybrider har validerats via A/B-testning (minst 10 uppgifter, statistisk signifikans)
- [ ] Inga agenter kvar i refinery med score < 70 i >14 dagar — antingen förbättrade eller arkiverade
- [ ] Agent-antal under 2000 — retirement-policy aktiv
- [ ] Git commit + tag `v0.6.0-fas5`
- [ ] Token-budget Fas 5: max 2M tokens (inkl. bakgrundsträning)

### Fas 6: Hardening & Release (2 dagar)

**Konkreta leveranser:**
1. **Säkerhetsgenomgång:** Granska alla API-nycklar — flytta till env-variabler. Kolla hårdkodade secrets. Input-validering på alla endpoints.
2. **Prompt injection-sanitization (slutlig):** Verifiera att ALL agent-output saniteras innan den skickas som context. Logga saniteringshändelser.
3. **Prestanda-checklista:** Kör `cProfile` på forge.py — identifiera topp 5 flaskhalsar. Åtgärda de 3 värsta.
4. **Dokumentation:** Uppdatera README.md. Docstrings på alla publika funktioner i Core/. Arkitekturdokument i `docs/architecture.md`.
5. **Minnesläckor:** Fixa termSeen obegränsad tillväxt (#16). Lägg till max-storlek + LRU-eviction.
6. **Slutlig regression:** Kör hela rök-testsviten. Kör `pytest --cov` — bekräfta ≥60% modultäckning.
7. **Oberoende evaluator — slutkontroll:** Kör golden test set mot ALLA production-agenter. Scores från oberoende evaluator blir "source of truth" för release.

**Definition of Done — Fas 6:**
- [ ] 0 hårdkodade secrets kvar — alla i env-variabler (verifierat med pre-commit secrets scan)
- [ ] Topp 3 prestanda-flaskhalsar åtgärdade (mätt med cProfile före/efter)
- [ ] README.md uppdaterad — installation, användning, utveckling
- [ ] `docs/architecture.md` existerar — komponentdiagram + dataflöde
- [ ] Docstrings på alla publika funktioner i Core/
- [ ] termSeen har max-gräns + eviction
- [ ] Rök-testsvit + full testsvit — 0 failures
- [ ] Oberoende evaluator har kört golden test set mot alla production-agenter
- [ ] Git commit + tag `v1.0.0-release`
- [ ] Token-budget Fas 6: max 500K tokens

---

## GIT-STRATEGI — ROLLBACK

**Commit-regler:**
- En commit per avslutad batch — commit-meddelande: `batch-X: <vad gjordes>`
- Tag per avslutad fas: `v0.2.0-fas1`, `v0.3.0-fas2`, etc.
- **Branch-strategi:** Riskabla ändringar (state-migration, forge-splittring) → `feature/` branch → merge till main först efter verifiering
- `git diff --stat` före varje batch — Hermes granskar
- Backup av state.yaml före varje batch: `state.yaml.backup-YYYYMMDD-HHMM`
- **Pre-commit hook:** `git-secrets` skannar efter API-nycklar, tokens, lösenord — blockerar commit vid träff

**Rollback-procedur:**
- Vid batch-fel: `git reset --hard HEAD~1` + återställ state från senaste backup
- Vid fas-fel: `git checkout <föregående-fas-tag>`
- Hermes checkpoint: efter varje batch loggas `batch_num`, `status`, `timestamp` i `orchestrator_checkpoint.txt`

---

## STATE MANAGEMENT — KONKRETA FÖRBÄTTRINGAR

1. **Trådsäker kö för activity-loggning** — samla i minnet, flusha en gång
2. **run_id → agent index** — O(1) lookup istället för O(n) över 751 agents
3. **composite_score + version i agent-posten** — ingen disk-läsning per lookup
4. **Inkrementell sparning** — append-only JSON-lines istället för full YAML-dump varje gång
5. **Hardlinks för checkpoints** — MB istället för hundratals MB
6. **Flerfils-arkitektur** — agents.yaml, evaluations.yaml, activity.yaml separata

**Migration (Fas 1.5):** Existerande state.yaml migreras via script. `state_version: 2`. Rollbackbart via backup.
**Semantisk verifiering:** Checksummor före/efter — antal agents, total_evaluations, medelscore. Alla måste matcha.
**Före migration:** Verifiera att forge.py är STOPPAD — `ps aux | grep forge` — döda eventuella processer.

---

## HERMES ORCHESTRATOR — Arkitektur & Regler

### Kapacitet
Hermes (denna agent) agerar som **Meta-Coordinator / Orchestrator** med kapacitet att dispatche **upp till 20 subagenter samtidigt** via `delegate_task`.

- `max_concurrent_children: 20`
- `max_async_children: 20`
- Subagenter är **efemära (engångs)** — de lever bara under sin task, returnerar resultat, och försvinner
- Hermes kan dispatche i batcher — kör 20, vänta på resultat, dispatcha 20 nya med andra uppgifter

### ⚡ Dispatcher Rate-Limiting (NY v4)
**Token-bucket för dispatch-frekvens:**
- Max 20 samtidiga — men även dispatch-hastigheten begränsas: max 1 batch per 30 sekunder (bucket: 3 tokens, refill 1 token per 10s)
- Vid full bucket → tasks köas med position, timeout 300s. Tasks som överskrider timeout → avvisas med felmeddelande
- **Syfte:** Skydda mot API rate-limit från deepseek. Utan denna → teoretiskt möjligt att dispatcha 20+20+20 subagenter på under en minut → 403/429 från provider
- Gäller batch-dispatch (delegate_task) — inte forge.py spawn (som redan har rate-limiting via Fas 1)

### Subagent-egenskaper
- **LEAF-only** — subagenter kan inte skapa egna subagenter (`max_spawn_depth: 1`)
- **Isolerade** — ingen delad state, inget minne av varandra, ingen kommunikation mellan subagenter
- **Verktyg:** terminal, file, web, search (kan begränsas via toolsets)
- **Output:** returnerar text till Hermes för syntes

### ⚡ Circular Spawn Guard — Gäller ALLA agenttyper (NY v4)
`max_spawn_depth: 1` gäller **både** delegate_task-subagenter **och** forge.py spawn:
- En forge-agent som spawnas via `forge.py spawn` får INTE i sin tur spawna andra forge-agenter
- En forge-agent får INTE anropa `delegate_task` för att kringgå spawn-förbudet
- **Validering:** forge.py kontrollerar `spawn_depth` före varje spawn — vid depth ≥1 → avvisa med felmeddelande
- **Syfte:** Förhindra infinite spawn-loopar. Utan denna → Agent A spawnar Agent B som spawnar Agent C som spawnar Agent A → token-tsunami, state-korruption, oändlig rekursion

### Subagent-felhantering
- **Timeout:** 300s per subagent
- **Retries:** Max 3 per subagent
- **Eskalering:** Vid 3 failures → Hermes tar över uppgiften själv
- **Loggning:** Alla failures loggas med subagent-typ, uppgift, och felorsak

### ⚡ Aktiv Checkpoint-Resume — Hermes Crash Recovery (NY v4)
`orchestrator_checkpoint.txt` uppgraderas från passiv logg till **aktiv återupptagningsmekanism:**
- **Vid Hermes-start:** Läs checkpoint → identifiera pågående batch (status: `in_progress`) → återuppta från senaste slutförda steg
- **Checkpoint-format per rad:** `batch_num|status|step_completed|timestamp|git_commit_hash`
- **Status-värden:** `in_progress`, `completed`, `failed`
- **Återupptagningslogik:** Om batch 4 har status `in_progress` och `step_completed=2` → hoppa över steg 1-2, börja på steg 3
- **Säkerhetskontroll:** Vid återupptagning — verifiera att git HEAD matchar `git_commit_hash` i checkpoint. Vid mismatch → alert, manuell granskning krävs
- **Syfte:** 14-20 dagars projekt utan auto-resume → varje Hermes-krasch kräver manuell återhämtning. Med aktiv checkpoint → Hermes återupptar automatiskt där den var

### Caveman-regler — Differentierad per subagent-typ

**Caveman Ultra (70% färre tokens):**
- Implementation, buggfixar, refaktorering, enkel kodanalys
- Inga artighetsfraser, inga onödiga tabeller/emoji

**Full verbose:**
- Audit/analys (kräver detaljer och nyanser)
- Kreativa subagenter (idé, visionär — behöver utrymme)
- Säkerhetsgranskning (detaljnivå avgörande)
- Dokumentation (kräver fullständiga förklaringar)

**Regel:** Caveman-regler från `D:\styde\_alpedal\styde-forge\skills\event-cleanup-pattern\caveman\SKILL.md` inkluderas ENDAST för implementation/fix-subagenter. Audit- och analys-subagenter får full verbose.

**Fallback:** Om caveman-filen saknas → använd inbäddad fallback: "Kort, direkt, inga artighetsfraser, inga onödiga tabeller/emoji, fokus på handling."

### Agent-typer & Katalogstruktur

**StydeAgents** — Alla Forge-agenter finns i två kataloger:

```
D:\styde\_alpedal\styde-forge\StydeAgents\
├── refinery\     ← Under träning (<85/100)
└── production\   ← Produktionsredo (≥85/100, 3+ godkända i rad)
```

Hermes läser agenter från båda katalogerna. En agent kan flyttas från refinery → production när den når ≥85/100 i 3 konsekutiva evals OCH godkänns av oberoende evaluator-agent.

| Typ | Verktyg | Livslängd | Syfte |
|-----|---------|-----------|-------|
| **delegate_task subagenter** | `delegate_task` (efemära) | Engångsjobb | Snabba analyser, isolerade buggfixar, granskningar. Försvinner efter task. |
| **Forge-agenter (StydeAgents)** | `forge.py spawn` + `loop-parallel` | Persistenta | Långsiktig träning, specialisering, team-samarbete via delad state.yaml |

**Mönster: Hermes orchestrator + StydeAgents för persistenta team, delegate_task-subagenter för engångsjobb.**

- **Persistenta team** (StydeAgents): code-reviewer, bug-hunter, architecture-critic, audit-agent — tränas tills de når production, återanvänds över tid, delar state
- **Engångsjobb** (delegate_task): "läs X och hitta buggar", "fixa denna specifika funktion", "granska denna PR" — engångs, inget bestående

**Hermes roll:** Orchestrator som:
1. Väljer rätt agent-typ för rätt jobb
2. Dispatchar delegate_task-subagenter för engångsanalyser
3. Spawnar + kör Forge-agenter för långsiktig träning
4. Syntetiserar resultat från båda
5. Skapar nya Forge-blueprints när en specialiserad agent saknas
6. Skapar hybrid-subagenter genom att slå ihop kunskap från flera StydeAgents
7. Skapar hybrid-blueprints och kör genom Forge vid behov av permanent specialiserad hybrid-agent

### Special-subagenter — Nyttjas löpande genom projektet

Utöver de ordinarie arbets-subagenterna ska Hermes **då och då** deploya specialiserade subagenter för att höja kvaliteten och bredda perspektiven:

**Idé-subagenter** — Kreativt tänkande, "outside the box" (FULL VERBOSE):
- Genererar oväntade lösningar och alternativa angreppssätt
- Ifrågasätter grundantaganden — "måste vi verkligen göra så här?"
- Kommer med feature-idéer som ingen tänkt på
- Används: mellan faser, när utvecklingen känns linjär

**Optimerings-subagenter** — Pressa ut maximal prestanda/kvalitet (CAVEMAN):
- Hittar onödig komplexitet och föreslår förenklingar
- Token-optimerar prompts, kontext, och agent-kommunikation
- Pressar ner responstider och resursanvändning
- Används: efter varje större förändring, före varje audit

**Visionär-subagenter** — Framtidsblick, skalbarhet (FULL VERBOSE):
- Tänker 6-12 månader framåt — "vad kommer vi ångra att vi inte byggde?"
- Identifierar framtida flaskhalsar innan de uppstår
- Föreslår arkitekturella förberedelser för kommande features
- Används: i början av varje fas, vid större designbeslut

**Problemlösnings-subagenter** — Djupgående problemlösning (FULL VERBOSE):
- Tar sig an de svåraste buggarna och mest komplexa utmaningarna
- Angriper problem från 3+ olika vinklar samtidigt
- Dokumenterar INTE BARA lösningen utan också vägen dit
- Används: vid blockerande buggar, arkitekturella dilemman, återkommande problem

**Regel:** Dessa special-subagenter ska INTE ersätta de ordinarie arbets-subagenterna — de kompletterar. Hermes avgör när i projektet de gör mest nytta.

### Hybrid-subagenter — Kombinera flera agenters kunskap

Hermes kan skapa en subagent som besitter sammanslagen kunskap från flera StydeAgents, eller från StydeAgents kombinerat med externa källor (skills, icke-StydeAgents, dokumentation, etc).

**Engångs-hybrid (delegate_task):**
1. Hermes läser `persona.md` + `runs/*/output.md` från Agent A och Agent B (StydeAgents eller externa)
2. Slår ihop regeluppsättningar + beprövade arbetsmönster
3. Skickar som `context` till EN subagent — EFTER prompt injection-sanitization
4. Subagenten agerar som hybrid — t.ex. bygga komponenter OCH auditera säkerhet samtidigt

**Permanent hybrid (Forge):**
Om Hermes bedömer att kombinationen behövs återkommande:
1. Hermes skapar en ny blueprint i `blueprints/<hybrid-name>/`
2. Slår ihop personas + skills från källorna (StydeAgents + externa)
3. Kör genom Forge: `spawn → eval → improve` tills agenten når production
4. Hybrid-agenten blir en permanent specialiserad StydeAgent

**Hybrid-validering — A/B-test (FÖRBÄTTRAD):**
- **Minst 10 olika uppgifter** — inte en enda (en jämförelse är statistiskt brus)
- Samma 10 uppgifter → original agent A, original agent B, hybrid
- Jämför medelvärde + standardavvikelse
- Hybrid måste vara ≥ bästa original — med signifikant marginal (≥0.5σ bättre, eller likvärdig med lägre token-åtgång)
- Underkänd hybrid → iterera blueprint eller förkasta

**Exempel:**
- `web-component-builder` + `web-security-engineer` → subagent som bygger säkra komponenter
- `code-reviewer` (StydeAgent) + OWASP-skills (extern) → subagent med säkerhetsgranskning
- `accessibility-auditor` + WCAG 2.2-dokumentation → subagent med uppdaterad tillgänglighetsstandard
- `dashboard-themer` + design-system-docs → subagent som bygger enligt designspec

**Regel:** Hermes avgör om hybriden ska vara engångs (delegate_task) eller permanent (Forge) baserat på:
- Kommer kombinationen behövas fler gånger? → Forge
- Är det ett unikt engångsbehov? → delegate_task

### Saknad agent — Sök, Skapa, Träna, Jämför

Om Hermes behöver en agent som inte finns bland StydeAgents:

1. **Sök externt** — Hermes söker på nätet (web_search / skills repositories) efter agenter, skills, eller blueprints som matchar behovet
2. **Skapa blueprint** — Hermes skapar en egen blueprint i `blueprints/<agent-name>/` baserat på bästa tillgängliga kunskap
3. **Träna genom Forge** — Kör `forge.py spawn` → `eval` → `improve` tills agenten når ≥85/100 i 3 konsekutiva evals
4. **Jämför** — Om steg 1 hittade en extern agent/skill: jämför den externa agentens output mot den Forge-tränade agentens output
5. **Välj bäst** — Hermes avgör vilken som är bäst (högst kvalitet, bäst anpassad för uppgiften) och använder den
6. **Importera vid behov** — Om den externa agenten är bättre: importera som skill/blueprint. Om Forge-agenten är bättre: behåll i StydeAgents

**Fallback-regel:** Om sökning (steg 1) inte hittar relevant innehåll → gå direkt till steg 2 (skapa egen blueprint). Lita inte på att externa repositories har rätt innehåll.

**Exempel på flöde:**
```
Behov: "Behöver en agent som kan granska Docker säkerhet"
↓
Steg 1: Sök → Hittar "docker-security-auditor" skill på skills.sh
Steg 2: Skapa blueprint → blueprints/docker-security-auditor/
Steg 3: Forge → spawn → eval → improve → 89/100
Steg 4: Jämför → extern skill vs Forge-agent (89/100)
Steg 5: Hermes: "Forge-agenten bättre — djupare analys, Forge-specifik"
Steg 6: Behåll Forge-agenten i StydeAgents
```

### Kollisionsregler — Subagenter får ALDRIG förstöra för varandra

**Regel 1: Fil-ägarskap.** Varje fil har EXAKT EN subagent som äger den per batch.
- Samma fil → samma subagent. Punkt.
- 2 subagenter får ALDRIG editera samma fil i samma batch.
- **Ny fil:** Subagenten som SKAPAR en ny fil äger den — ingen annan rör den i samma batch.

**Regel 2: Oberoende filer först.** Gruppera tasks efter filer, inte efter buggtyp.
- Rätt: Sub 1 äger `forge.py`, Sub 2 äger `server_8765.py`, Sub 3 äger `mission_control_8765.html`
- Fel: Sub 1 fixar XSS i HTML, Sub 2 fixar WCAG i HTML, Sub 3 fixar CSS i HTML

**Regel 3: Sekventiell batch vid beroenden.**
- Om bugg B beror på att bugg A är fixad → B väntar till nästa batch
- Exempel: State-race-condition måste fixas innan evaluations.append kan testas

**Regel 4: Read-only för analys.** Subagenter som bara LÄSER kod (analys, audit, granskning) kan dela filer — de modifierar inget.

**Regel 5: Differentierad verifiering — Hermes granskar inte allt lika djupt.**
- **Kritiska ändringar** (state.py, forge.py, datafiler): Hermes verifierar ALLTID manuellt — läser filen, kör tester
- **Medel-risk** (server_8765.py, dashboard.py): Hermes kör automatiska tester + stickprov
- **Låg-risk** (CSS, HTML-struktur, färger): Hermes gör stickprov — litar på subagenten om testerna passerar. **OBS:** Även låg-risk-ändringar kan introducera säkerhetshål (onclick=, eval(), etc) — översiktlig säkerhetsgranskning görs alltid
- Subagent-resultat är **självrapportering**, inte verifierad sanning — verifieringsdjup proportionellt mot risk

### Batch-planering för PlanPrompt.md

| Batch | Antal | Subagenter | Filer | Typ | Beroenden |
|-------|-------|-----------|-------|-----|-----------|
| 1 | 4 | XSS-fix, CSP-fix, accessibility-audit, rate-limiting | `mission_control_8765.html`, `server_8765.py` | Skriv (olika ägare per fil) | Inga — körs parallellt med batch 2 |
| 2 | 3 | Cache-fix, markdown-fix, test_spawn-borttagning | `hermes_bridge.py`, `agent_runner.py`, `tests/test_spawn.py` | Skriv (olika filer) | Inga — körs parallellt med batch 1 |
| 3 | 2 | State-race-condition, evaluations.append | `state.py`, `forge.py` | Skriv | MÅSTE ske EFTER batch 1+2 — state-beroenden |
| 4 | 3 | isinstance-skydd, config.py, modellnamn | `forge.py`, `Core/config.py` (ny), `dashboard.py` | Skriv | MÅSTE ske EFTER batch 3 — rör forge.py |
| 5 | 4 | Refaktorering: splittra forge.py, slå ihop validering, ta bort död kod, dashboard-HTML | Flera | Skriv (olika moduler) | MÅSTE ske EFTER batch 4 |
| 6 | 3 | API-endpoints, dashboard-kontroller, PWA | `server_8765.py`, `mission_control_8765.html` | Skriv | MÅSTE ske EFTER batch 5 |

**Regel:** Max 4-5 subagenter per batch som SKRIVER. Fler subagenter OK om de bara LÄSER/ANALYSERAR.

### Utvecklingsloop — Iterera tills perfektion

Efter varje fas kör Hermes en utvecklingsloop för att säkerställa kvalitet och inte missa något:

**Loop-struktur:**
```
LOOP START
  ↓
1. IMPROVE — Hermes slänger ALLA relevanta subagenter på projektet:
   - Bug-hunters (hitta kvarvarande buggar)
   - Code-reviewers (granska kodkvalitet)
   - Performance-optimizers (prestandaförbättringar)
   - Accessibility-auditors (WCAG/tillgänglighet)
   - Security-engineers (säkerhetsgranskning)
   - Refactoring-specialists (strukturförbättringar)
   - Documentation-standardizers (dokumentationskvalitet)
   - Design-critics (UI/UX-granskning)
   - Architecture-critics (arkitekturgranskning)
   ↓
2. FINAL AUDIT — FLERA olika granskare gör en rå, detaljerad audit:
   - 3+ olika perspektiv (kritiker, analytiker, reviewer, kvalitetshöjare)
   - Varje audit är OBARMHÄRTIG — pekar på ALLA brister, även små
   - Hermes sammanställer och ger ett samlat betyg (0-100)
   ↓
3. BESLUT:
   - Score < 85 → Gå tillbaka till IMPROVE (fixa bristerna)
   - Score ≥ 85 → Räkna som godkänd iteration
   ↓
4. EXIT VILLKOR:
   - 3 konsekutiva audits ≥ 85/100 → EXIT LOOP
   - Max 10 iterationer → om ≥85 ej nås: Hermes rapporterar "MANUELL GRANSKNING KRÄVS"
   - Annars → FORTSÄTT LOOPA
```

---

## OBEROENDE EVALUATOR-AGENT (NY — INFÖRS PRE-FAS 1)

**Syfte:** Enda skyddet mot co-evolution — agenter som utvärderar varandra driver scores mot vad andra agenter vill ha, inte vad uppgiften kräver.

**Implementation:**
- EN agent skapas före Fas 1 — deltar ALDRIG i träning, ändras ALDRIG
- Körs mot fast "golden test set": 20-30 uppgifter med facit (spawn, eval, kodgranskning, säkerhet)
- Kalibreras EN gång mot facit — därefter låst
- Används vid: promotion-beslut (Fas 5), release (Fas 6), misstänkt score-drift

**Regel:** Om oberoende evaluator ger signifikant lägre score än Forge-evaluatorerna → co-evolution misstänks → stoppa promotion, utred.

---

## DOKUMENTATIONSKRAV (NYTT)

**Minimum per fas:**
- Uppdaterad `README.md` — installation, användning, bidragande
- Docstrings på alla nya/ändrade funktioner (Google style)
- `docs/CHANGELOG.md` — version, datum, vad som ändrades

**Slutleverans (Fas 6):**
- `docs/architecture.md` — komponentdiagram, dataflöde, designbeslut
- `docs/API.md` — genererat från API_SPEC.md + implementation
- `tests/README.md` — hur man kör testerna, coverage-krav

---

## TIDSESTIMAT (uppdaterad)

| Fas | Tid | Status | Subagenter per batch | Token-budget | Est. kostnad |
|-----|-----|--------|---------------------|-------------|-------------|
| 0: Deep Audit | 1-2 dagar | **100% KLAR** | 3 (gjort) | — | — |
| ⚠️ Infrastruktur | 0.5 dag | **NY** | 2-3 | 150K | ~$0.03-0.05 |
| 0.5: Design Mockups | 0.5 dag | **NY — 5 unika mockups** | 5 (design-subagenter) | 1M | ~$0.20-0.40 |
| 1: Kritiska buggar + Infra | 1-2 dagar | Ej påbörjad | 3-4 | 500K | ~$0.10-0.20 |
| 1.5: State-migrering | 0.5 dagar | Ej påbörjad | 1-2 | 200K | ~$0.04-0.08 |
| 2: Refaktorering | 2-3 dagar | Ej påbörjad | 3-4 | 800K | ~$0.15-0.30 |
| 2.5: Test Hardening | 1-2 dagar | Ej påbörjad | 2-3 | 400K | ~$0.08-0.15 |
| 3: Dashboard Control | 3-4 dagar | Ej påbörjad | 3-4 | 1.2M | ~$0.25-0.45 |
| 4: Workflow | 2 dagar | Ej påbörjad | 2-3 | 600K | ~$0.12-0.22 |
| 5: Agent-träning | 2-3 dagar | Bakgrund från Fas 1 | Forge loop-parallel | 2M | ~$0.40-0.75 |
| 6: Hardening | 2 dagar | Ej påbörjad | 3-4 | 500K | ~$0.10-0.20 |

**Total: 15-20.5 dagar** | **Total token-budget: ~7.35M** | **Est. totalkostnad: ~$1.50-2.80**

---

## BILAGA: BUG → FAS → BATCH SNABBREFERENS

| # | Bug | Severity | Fas | Batch |
|---|-----|----------|-----|-------|
| 1 | Cache-inkonsekvens hermes_bridge.py | 🔴 CRIT | 1 | 2 |
| 2 | Inverterad markdown-logik agent_runner.py | 🔴 CRIT | 1 | 2 |
| 3 | test_spawn.py död kod | 🔴 CRIT | 1 | 2 |
| 4 | state["evaluations"] = [] | 🔴 CRIT | 1 | 3 |
| 5 | Race condition parallel loop | 🔴 CRIT | 1 | 3 |
| 6 | XSS unsafe-inline CSP + innerHTML | 🔴 CRIT | 1 | 1 |
| 7 | forge.py spawn/eval duplicerad 3× | 🟠 HIGH | 2 | 4–5 |
| 8 | isinstance(list) saknas | 🟠 HIGH | 2 | 4 |
| 9 | nvidia-smi blockerar synkront | 🟠 HIGH | 2 | 5 |
| 10 | subprocess.Popen utan PID | 🟠 HIGH | 1 | 2 |
| 11 | CSRF-token förfaller 30min | 🟠 HIGH | 2 | 4 |
| 12 | blueprint + quality_gates duplicering | 🟠 HIGH | 2 | 5 |
| 13 | except Exception: pass | 🟠 HIGH | 2 | 5 |
| 14 | 62/751 agents saknar spawned_at | 🟡 MED | 1.5 | — |
| 15 | 0/751 agents har composite_score | 🟡 MED | 1.5 | — |
| 16 | termSeen växer obegränsat | 🟡 MED | 6 | — |
| 17 | fetchState catch(e) {} | 🟡 MED | 3 | 6 |
| 18 | dashboard.py HTML i Python-sträng | 🟡 MED | 2 | 5 |
| 19 | generate.py saknas | 🟡 MED | 1 | — |
| 20 | 15 hårdkodade modellnamn | 🟡 MED | 2 | 4 |
| 21 | FORGE_ROOT duplicerad 17/22 moduler | 🟡 MED | 2 | 4 |
| 22 | forge.py 1574 LOC monolit | 🟢 LOW | 2 | 5 |
| 23 | filestore.py ~800 rader död kod | 🟢 LOW | 1 | 2 |
| 24 | agent_runner.py död kod | 🟢 LOW | 1 | 2 |
| 25 | Inga WCAG/ARIA-attribut | 🟢 LOW | 3 | 6 |
| 26 | prefers-reduced-motion ignoreras | 🟢 LOW | 3 | 6 |
| 27 | Färgkontrast 2.5:1 | 🟢 LOW | 3 | 6 |
| 28 | 16/22 moduler 0 tester | 🟢 LOW | 2.5 | — |
| 29 | localhost-bindning | 🟢 LOW | 2 | 4 |
| 30 | Ingen rate-limiting | 🟢 LOW | 1 | 1 |

---

## VILL DU ATT JAG BÖRJAR FIXA DE KRITISKA BUGGARNA?

Nästa steg: Infrastruktur-setup (git, secrets scanning, golden evaluator, dry-run-ramverk) → sedan Fas 1 med batch 1+2 parallellt (XSS/CSP/rate-limiting + cache/markdown/död-kod).
