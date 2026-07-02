Nu har jag kontext. Låt mig spåra alla gap från teacher feedback mot den aktuella BLUEPRINT/persona som är inbäddade i prompten.
Teacher feedback identifierar 5 gap:
1. CAVEMAN-formatregler kommer FÖRST i prompten, före exekveringsinstruktioner
2. persona.md saknar anti-meta-loop guard
3. BLUEPRINT.md saknar execution gate (score >= 80 = applicera fixar)
4. BLUEPRINT.md saknar koncishetsdirektiv (verification cap 3 bullets)
5. BLUEPRINT.md saknar self-consistency check
Här är delta-rapporten:
---
delta-report:
  subject: bug-hunter-core BLUEPRINT.md + persona.md
  total-gaps: 5
  critical: 2
  high: 2
  medium: 1
gaps:
  - id: gap-1
    severity: CRITICAL
    location: prompt preamble (CAVEMAN ULTRA MODE section)
    issue: Formatregler placerade före alla exekveringsinstruktioner. Agenten får 30+ rader formatregler innan den ser en enda instruktion om vad den ska producera. Detta orsakar format-verifieringsloop: agenten fokuserar på att checka format istället för att producera substans.
    root-cause: 40w max. Instruktionsordningen prioriterar presentationsregler före leveranskrav, vilket programmerar agenten att validera format före innehåll.
    impact: HIGH - Agenten fastnar i meta-loop, skriver om sina egna output-regler istället för uppgiftens leverabel.
    fix:
      action: restructure-prompt-order
      description: Flytta CAVEMAN ULTRA MODE-block till slutet av prompten som en "validation checklist", inte som ingress. Sätt EXECUTE/leveransinstruktioner först.
      new-structure:
        - 1: "PERSONA (rollbeskrivning)"
        - 2: "BLUEPRINT (Purpose, Skills, EXECUTE Phase, Verification)"
        - 3: "INSTRUCTIONS: Complete the task. Produce the deliverable."
        - 4: "--- validation checklist below this line ---"
        - 5: "CAVEMAN ULTRA MODE format rules (last, as checklist)"
    verification: Efter omskrivning: kör agenten med samma prompt och verifiera att den producerar sitt faktiska leverabel (kod/diff/analys) innan den nämner YAML-formatregler. Om första 10 rader output handlar om format istället för innehåll = FAIL.
  - id: gap-2
    severity: HIGH
    location: persona.md rule set
    issue: Saknar explicit anti-meta-loop guard. Agenten kan skriva om "jag följer formatreglerna" istället för att skriva själva analysen.
    root-cause: 40w max. Inget varningssystem för självrefererande meta-text; agenten belönas implicit för att recitera regler.
    impact: HIGH - Meta-text ersätter värdefull leverabel, ger noll outputvärde.
    fix:
      action: add-rule-to-persona
      location: after existing "Output: prioritized markdown bug report" line
      new-text: "  Anti-meta-loop: If you catch yourself writing about your own output rules rather than the task output, you are failing. Stop. Delete the meta-text. Write the actual deliverable."
    verification: Skicka en prompt som frestar agenten att skriva om sina formatregler. Om output innehåller "I must follow the format" eller liknande meta-text istället för analys = FAIL.
  - id: gap-3
    severity: CRITICAL
    location: BLUEPRINT.md EXECUTE Phase section
    issue: EXECUTE Phase finns men saknar score-baserad trigger. När composite >=80 och konkreta fixar identifierats tillåts agenten säga "no patches required" vilket underminerar hela analysen.
    root-cause: 40w max. Execution gate är villkorslös istället för score-aktiverad; agenten saknar regel för när den måste applicera egna fixar.
    impact: CRITICAL - Analysen blir ofullständig: fixar preskriberas men aldrig applicerade. Underminerar trovärdighet.
    fix:
      action: add-execution-gate-to-blueprint
      location: end of EXECUTE Phase section
      new-text: "  Score-gated execution: If composite score >= 80 AND analysis identified concrete fixes (patches, config changes, new rules), the agent MUST apply them immediately via patch tool before concluding. The only allowed exception: if the fix requires human judgment, explicitly state why in a 'deferred' note. Never conclude 'no patches required' when fixes are listed in the analysis."
    verification: Simulera eval med score=84 och identifierade fixar. Om agenten säger "no patches required" eller inte anropar patch tool = FAIL.
  - id: gap-4
    severity: MEDIUM
    location: BLUEPRINT.md Evaluation & Feedback section
    issue: Root cause word limit (40w) finns men verification saknar bullet-cap. Agenten kan producera 15-punkts verification lists som översvämmar output.
    root-cause: 40w max. Inget motsvarande cap för verification-sektionen; koncisteskravet implementeras bara delvis.
    impact: MEDIUM - Onödigt verbose verification-sektioner späder ut signal, gör output svårläst.
    fix:
      action: add-conciseness-constraint
      location: after "each root cause limited to 40 words" in Evaluation & Feedback
      new-text: "  Conciseness: Verification section capped at 3 bullet points maximum, 1 line each. Root cause section must state findings directly without repeating dimension descriptions verbatim."
    verification: Mät verification-sektionens längd i en testkörning. Om >3 bullets eller någon bullet >1 rad = FAIL.
  - id: gap-5
    severity: HIGH
    location: BLUEPRINT.md (no existing section for self-consistency)
    issue: Ingen självkonsistenskontroll före slutgiltig slutsats. Agenten kan ha oapplicerade fixar men ändå påstå "all patches applied."
    root-cause: 40w max. Inget obligatoriskt reconciliation step mellan diagnostiserade fixar och utförda patch-anrop.
    impact: HIGH - Möjliggör gap-3:s "no patches"-problem även om execution gate finns; dubbla försvarslager krävs.
    fix:
      action: add-self-consistency-step
      location: new section after Verification, before Clearoutput
      new-text: |
        Self-Consistency Check (Mandatory)
        Before presenting the final output, the agent MUST:
          1. Enumerate every fix prescribed in the analysis phase.
          2. For each fix, state: APPLIED (via patch tool) or DEFERRED (with explicit reason).
          3. If any fix is unaccounted for, the conclusion MUST acknowledge the gap.
          4. If all fixes are applied, state "All prescribed fixes applied."
          5. Never claim "no patches required" if the analysis lists concrete improvements.
    verification: Efter varje agentkörning: jämför analysens fix-lista med outputens "applied/deferred"-status. Om mismatch = FAIL.
root-cause-summary:
  theme: "Instructions structure prioritizes format over delivery, creating meta-loop trap."
  primary: "CAVEMAN-formatregler som ingress programmerar agenten att validera format före innehåll"
  secondary: "Saknade guardrails (execution gate, self-consistency check, anti-meta-loop) tillåter ofullständig leverans"
  tertiary: "Partiell koncisteskrav (root cause cap finns, verification cap saknas) skapar inkonsekvent outputkvalitet"
aggregate-impact: HIGH
  all-5-gaps-combined: "Agenten producerar strukturellt korrekt men ofullständig analys med noll verklig leverans. Format checkas, fixar identifieras men appliceras inte, meta-text flödar, verification-sektioner svämmar över. Systemet simulerar kvalitet utan att leverera den."
fix-priority-order:
  1: gap-1 (CRITICAL - orsakar meta-loop)
  2: gap-3 (CRITICAL - låter fixar vara oapplicerade)
  3: gap-2 (HIGH - anti-meta-loop guard)
  4: gap-5 (HIGH - self-consistency check)
  5: gap-4 (MEDIUM - conciseness)
Result: 5 gap identifierade, 2 CRITICAL (format-ordning, execution gate), 2 HIGH (anti-meta-loop guard, self-consistency check), 1 MEDIUM (conciseness). Alla fixar specificerade med exakt infogningspunkt och verifieringssteg. Applicering kräver omskrivning av prompt-strukturen (gap-1 är den enda som kräver global omstrukturering snarare än lokal editering).