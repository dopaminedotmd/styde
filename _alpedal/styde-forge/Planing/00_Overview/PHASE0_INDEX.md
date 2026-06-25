# Styde Forge v3.0 — Phase 0 Index

**Codename:** The Crucible
**Type:** Portable Evolutionary Elite Agent Refinery
**Version:** 3.0
**Status:** Phase 0 — Complete ✅ (Updated 2026-06-25)

---

## Dokumentöversikt (54 dokument)

| # | Sektion | Dokument | Beskrivning |
|---|---------|----------|-------------|
| 00 | Overview | `System_Startup_Shutdown.md` | Start- och nedstängningssekvens |
| 00 | Overview | `PHASE0_INDEX.md` | Detta index |
| 00 | Overview | `Master_Architecture_Overview.md` | Hög-nivå arkitektur, lager, dataflöde |
| 00 | Overview | `USB_Directory_Structure.md` | Exakt filmappstruktur på USB |
| 00 | Overview | `Data_Models.md` | Samtliga YAML/JSON-scheman |
| 00 | Overview | `Core_Loop_Detail.md` | Steg-för-steg loop-specifikation |
| 00 | Overview | `Component_Interfaces.md` | Gränssnitt mellan komponenter |
| 00 | Overview | `Phase0_to_Phase1_Transition.md` | Övergångsplan + Phase 1 scope |
| 01 | Vision | `Vision_and_Goals.md` | Vision, mål, innehåll, framgångskriterier |
| 01 | Vision | `Blueprint_Catalog.md` | Samtliga 6 blueprints med specifikationer |
| 02 | Hardware | `Hardware_Adaptation_Layer.md` | Auto-detektering, profilering |
| 02 | Hardware | `Resource_Governor.md` | Resursbegränsning |
| 03 | Eval | `LLM_as_Judge.md` | Oberoende modell-bedömning |
| 03 | Eval | `Cross_Judge_Consensus.md` | Konsensus mellan judges |
| 03 | Eval | `Bias_Calibration.md` | Periodisk kalibrering |
| 03 | Eval | `Bayesian_Weight_Optimization.md` | Adaptiv viktoptimering |
| 03 | Eval | `Self_Evaluation_System.md` | Agent-självutvärdering |
| 03 | Eval | `Automatic_Validation.md` | Valideringspipeline |
| 03 | Eval | `Benchmark_Catalog.md` | Samtliga 6 benchmarks |
| 04 | Sampling | `NUTS_Algorithm.md` | No-U-Turn Sampler |
| 04 | Sampling | `Dual_Averaging.md` | Adaptiv step-size |
| 04 | Sampling | `Hamiltonian_Monte_Carlo.md` | HMC verifikation |
| 04 | Sampling | `Variational_Inference.md` | VI för Machine-B |
| 04 | Sampling | `Tree_Depth_Optimization.md` | Dynamiskt träddjup |
| 05 | Meta | `Dynamic_Model_Selector.md` | Modellval per uppgift |
| 05 | Meta | `Historical_Learning_System.md` | Lärande från historik |
| 05 | Meta | `Automatic_Version_Increment.md` | Versionshantering |
| 05 | Meta | `Self_Monitoring_Health.md` | Hälsoövervakning |
| 06 | Safety | `Filesystem_Transactions.md` | Atomära skrivningar |
| 06 | Safety | `Atomic_Checkpoint_Writes.md` | Säkra checkpoints |
| 06 | Safety | `Automatic_Recovery.md` | Återhämtning |
| 06 | Safety | `Risk_Register.md` | Risker och mitigeringar |
| 07 | Multi-Agent | `Multi_Agent_Collaboration.md` | Kollaborationsmönster |
| 07 | Multi-Agent | `Security_Model.md` | Sandboxing, injection-skydd |
| 08 | Import | `Import_Strategy.md` | En-prompt import |
| 09 | Maintenance | `Maintenance_Cleanup_Strategy.md` | Pruning och underhåll |
| 10 | Operations | `Skill_Loading_Mechanism.md` | Skills → agent |
| 10 | Operations | `Blueprint_Validation.md` | Blueprint-validering |
| 10 | Operations | `Logging_Strategy.md` | JSON-lines loggning |
| 10 | Operations | `Cost_Token_Tracking.md` | Token/kostnad |
| 10 | Operations | `Human_Oversight_Points.md` | Mänskliga granskningspunkter |
| 10 | Operations | `API_Key_Management.md` | API-nycklar, providers, validering |
| 10 | Operations | `Caveman_Ultra_Mode.md` | Maxeffektivt operativt läge — 70% färre tokens, 2× snabbare |
| 11 | Knowledge | `Knowledge_Management.md` | Kunskapshantering, indexering, livscykel |
| 12 | Teacher | `Teacher_Agent.md` | Teacher/coach loop, feedback, skill-extrahering |
| 13 | Hooks | `Hooks_Events.md` | Eventsystem, 17 events, 4 hook-typer |
| 14 | RAG | `RAG_Retrieval.md` | Vector embeddings, FAISS, 3080-accelerated retrieval |
| 00 | Reference | `00_Glossary.md` | Samlad ordlista (A-Ö) |
| 00 | Reference | `DECISIONS.md` | Design Decision Log (15 beslut) |
| 00 | Reference | `State_Machines.md` | Alla state machines (diagram) |
| 00 | Reference | `Config_Reference.md` | Samtliga config-nycklar |
| 00 | Reference | `Testing_Strategy.md` | Teststrategi för Forge-infrastruktur |

---

## Recommended Reading Order

1. `PHASE0_INDEX.md` ← Du är här
2. `Master_Architecture_Overview.md` — Helikopterperspektiv
3. `00_Glossary.md` — Terminologi (bra referens under läsning)
4. `DECISIONS.md` — Varför designen ser ut som den gör
5. `USB_Directory_Structure.md` — Var allt hamnar
6. `Data_Models.md` — Alla datastrukturer
7. `Config_Reference.md` — Alla inställningar
8. `State_Machines.md` — Tillstånd och övergångar
9. `Core_Loop_Detail.md` — Exakt hur loopen går till
10. `Component_Interfaces.md` — Hur komponenter pratar
11. `Phase0_to_Phase1_Transition.md` — Vad händer sen
12. Därefter: Vision → Blueprint Catalog → Hardware → Eval Pipeline → ...

---

**Status:** Phase 0 Complete ✅. 51 design documents.
**Senast uppdaterad:** 2026-06-25
