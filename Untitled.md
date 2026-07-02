Åsikter:
                                                                                                                                                                                                                                           
    Styrkor:
    - Dark factory-idén — input är råmaterial, inte spec. "Bevis för intent, inte instruktioner." Matchar hur människor faktiskt kommunicerar.
    - Eval-spec per skill. Binära checks + golden cases. Instant regression. Det här är bra — Forge borde adoptera detta.
    - Cross-platform installern. 17 plattformar, auto-detection. Slipat.
    - Kvalitetsgrindar på varje skill. Validering + säkerhetsscanning + staleness. Blockera vid fail.
    - Namnkonvention -skill. Enkel signal för "installerbar mjukvara".
                                                                                                                                                                                                                                           
    Svagheter:
    - SKILL.md är monolitiskt. En fil som innehåller ALLT — triggers, workflow, instruktioner, referenser — max 500 rader. Det blir snabbt svåröverskådligt för komplexa agenter. Forges blueprint-format (persona.md + BLUEPRINT.md + config.yaml + skills/) är mer modulärt.
    - Ingen "loop". Skapa-en-gång, använd-många-gånger. Ingen eval → improve → checkpoint-cykel. Det här är hela Forges existensberättigande.
    - Ingen dual-model strategi. Allt körs på samma modell. Forge använder flash för spawn, pro för eval/teacher.
    - Hårt knuten till /skill-name invocation. Forge-agenter spawnas via delegate_task, inte slash-kommandon.
                                                                                                                                                                                                                                           
    Vad Forge kan stjäla:
    1. Eval-spec formatet (evals/<name>.eval.md med binary checks + golden cases). Bättre än nuvarande rubrics.
    2. run_evals.py --rollout — kör agenten på golden inputs, scorar riktig output. Exakt vad Forge behöver för automatiserad eval.
    3. Staleness detection — skills som går ur datum. Relevant för Forges archive-stadie.
    4. -skill suffix-konventionen för naming.
                                                                                                                                                                                                                                           
    Vad som inte passar:
    - Monolitisk SKILL.md vs Forges modulära blueprint-format
    - Slash-invocation vs delegate_task
    - Engångsskapande vs iterativ förbättringsloop
                                                                                                                                                                                                                                           
    Ska jag skriva in eval-spec-formatet i Phase 1-strukturen? Eller tänker du på något annat?