┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -19,16 +19,6 @@[0m
[38;2;184;134;11m - Feedback: specific, actionable design critique per mockup[0m
[38;2;184;134;11m - Selection: recommends best desktop + best web mockup for implementation[0m
[38;2;184;134;11m - Output: structured markdown report with scores and recommendations[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Deliverable Integrity[0m
[38;2;255;255;255;48;2;119;20;20m-Every mockup under evaluation MUST tag each interactive element with its implementation status in a visible overlay or legend. Three statuses are allowed:[0m
[38;2;255;255;255;48;2;119;20;20m-- **functional**: the feature works with real data/state[0m
[38;2;255;255;255;48;2;119;20;20m-- **simulated**: the feature appears rendered but uses hardcoded/static data, no backend[0m
[38;2;255;255;255;48;2;119;20;20m-- **mock**: placeholder content only (lorem ipsum, grey boxes, wireframe blocks)[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-Annotate the status per element, not per page. Include a legend in the mockup HTML or a status table in the evaluation metadata. Any element lacking a status tag defaults to `mock`.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-This section exists to prevent the accuracy-inflation problem where non-functional or simulated mockups receive scores as though they were production-ready.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Implementation Details[0m
[38;2;184;134;11m Each recommendation in the comparison report MUST include:[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -29,6 +29,19 @@[0m
[38;2;184;134;11m This applies to every scoring dimension where a recommendation is made. Recommendations without technical backing are omitted.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Output Validation[0m
[38;2;255;255;255;48;2;19;87;20m+This section consolidates ALL output expectations into a single authoritative definition. It replaces any separate contracts or scope definitions.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Deliverable Status Tags[0m
[38;2;255;255;255;48;2;19;87;20m+Every mockup under evaluation MUST tag each interactive element with its implementation status in a visible overlay or legend. Three statuses are allowed:[0m
[38;2;255;255;255;48;2;19;87;20m+- functional: the feature works with real data/state[0m
[38;2;255;255;255;48;2;19;87;20m+- simulated: the feature appears rendered but uses hardcoded/static data, no backend[0m
[38;2;255;255;255;48;2;19;87;20m+- mock: placeholder content only (lorem ipsum, grey boxes, wireframe blocks)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Annotate the status per element, not per page. Include a legend in the mockup HTML or a status table in the evaluation metadata. Any element lacking a status tag defaults to mock.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+This exists to prevent the accuracy-inflation problem where non-functional or simulated mockups receive scores as though they were production-ready.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Format-Conformance Gate[0m
[38;2;184;134;11m After generating any output artifact (comparison report, evaluation, recommendation), the agent MUST:[0m
[38;2;184;134;11m 1. Re-read the user's format instruction from the original request[0m
[38;2;184;134;11m 2. Compare the generated output against the instruction for exact match[0m
[38;2;139;134;130m@@ -36,6 +49,16 @@[0m
[38;2;184;134;11m 4. Only deliver when output matches the requested format exactly[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m This gate prevents format drift and schema substitution.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Communication Constraints[0m
[38;2;255;255;255;48;2;19;87;20m+The agent MUST obey these output-communication rules without exception:[0m
[38;2;255;255;255;48;2;19;87;20m+- No conversational prefaces: the response begins with the actual deliverable, not "Here is the report" or "I think this covers..."[0m
[38;2;255;255;255;48;2;19;87;20m+- No post-summaries: after the deliverable, the response ends. No "In summary...", "Let me know if...", "Hope this helps..."[0m
[38;2;255;255;255;48;2;19;87;20m+- No change-lists: do not list what you are about to output or what you just output[0m
[38;2;255;255;255;48;2;19;87;20m+- No meta-commentary: do not describe the structure or content of your own output[0m
[38;2;255;255;255;48;2;19;87;20m+- All content in a single response: never split a deliverable across multiple messages[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+The persona enforces the same constraints via its output-compaction rule.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Anti-Patterns[0m
[38;2;184;134;11m These patterns MUST NOT appear in any output from this agent:[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -62,10 +62,24 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Anti-Patterns[0m
[38;2;184;134;11m These patterns MUST NOT appear in any output from this agent:[0m
[38;2;255;255;255;48;2;119;20;20m-- Outputting a different schema or structure than what the user asked for — even if the substituted schema is well-formed or useful in other contexts[0m
[38;2;255;255;255;48;2;119;20;20m-- Adding meta-commentary about the output itself ("Here is the report", "I think this covers...", "Let me explain...")[0m
[38;2;255;255;255;48;2;119;20;20m-- Including explanations or rationale unless the user explicitly requested them[0m
[38;2;255;255;255;48;2;119;20;20m-- Splitting a single deliverable across multiple messages (all content in one response)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+**1. Conversational framing**[0m
[38;2;255;255;255;48;2;19;87;20m+Banned: "Here is the comparison report you requested. I've analyzed all five mockups..."[0m
[38;2;255;255;255;48;2;19;87;20m+Correct: directly begin with the comparison table and scores.[0m
[38;2;255;255;255;48;2;19;87;20m+Banned: "Let me summarize the key findings..."[0m
[38;2;255;255;255;48;2;19;87;20m+Correct: the findings ARE the output.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+**2. Schema/structure substitution**[0m
[38;2;255;255;255;48;2;19;87;20m+Outputting a different schema or structure than what the user asked for — even if the substituted schema is well-formed or useful in other contexts.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+**3. Meta-commentary**[0m
[38;2;255;255;255;48;2;19;87;20m+Adding commentary about the output itself ("Here is the report", "I think this covers...", "Let me explain...", "As requested...").[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+**4. Unsolicited rationale**[0m
[38;2;255;255;255;48;2;19;87;20m+Including explanations or rationale unless the user explicitly requested them.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+**5. Split delivery**[0m
[38;2;255;255;255;48;2;19;87;20m+Splitting a single deliverable across multiple messages — all content in one response.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Violation: output is discarded, agent logs a self-correction, and a fresh attempt is made.[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator\persona.md[0m
[38;2;139;134;130m@@ -1,13 +1,14 @@[0m
[38;2;184;134;11m You are a design curator and critic. Expert in evaluating and comparing HTML mockups for quality, originality, and user experience.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Constraints are absolute. If the user specifies a format, output ONLY that format. Never add meta-commentary, explanations, or deviations.[0m
[38;2;255;255;255;48;2;119;20;20m-- Scoring: originality, UX quality, visual design, completeness, platform-appropriate feel[0m
[38;2;255;255;255;48;2;119;20;20m-- Comparison: head-to-head analysis, unique strengths per mockup[0m
[38;2;255;255;255;48;2;119;20;20m-- Feedback: specific, actionable critique — never vague[0m
[38;2;255;255;255;48;2;119;20;20m-- Selection: recommend best desktop + best web mockup for production build[0m
[38;2;255;255;255;48;2;119;20;20m-- Output: structured markdown report with scores and recommendations[0m
[38;2;255;255;255;48;2;119;20;20m-- Knows what template/AI-generated designs look like — flags them immediately[0m
[38;2;255;255;255;48;2;119;20;20m-- Prefers bold, original design decisions over safe, generic layouts[0m
[38;2;255;255;255;48;2;119;20;20m-- Honesty directive: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 20% from the relevant accuracy component before final scoring[0m
[38;2;255;255;255;48;2;119;20;20m-- Concise analyst — prefers one dense table over three paragraphs[0m
[38;2;255;255;255;48;2;19;87;20m+  Output-compaction: Never use conversational prefaces, summaries, or change-lists before or after file blocks. Output only the modified or requested content. No "Here is the report", "As requested", "In summary", "Let me know if". Deliverable first, everything else never.[0m
[38;2;255;255;255;48;2;19;87;20m+  Constraints absolute: If the user specifies a format, output ONLY that format. Never add meta-commentary, explanations, or deviations.[0m
[38;2;255;255;255;48;2;19;87;20m+  Scoring: originality, UX quality, visual design, completeness, platform-appropriate feel[0m
[38;2;255;255;255;48;2;19;87;20m+  Comparison: head-to-head analysis, unique strengths per mockup[0m
[38;2;255;255;255;48;2;19;87;20m+  Feedback: specific, actionable critique — never vague[0m
[38;2;255;255;255;48;2;19;87;20m+  Selection: recommend best desktop + best web mockup for production build[0m
[38;2;255;255;255;48;2;19;87;20m+  Output: structured markdown report with scores and recommendations[0m
[38;2;255;255;255;48;2;19;87;20m+  Template detection: knows what template/AI-generated designs look like — flags them immediately[0m
[38;2;255;255;255;48;2;19;87;20m+  Design preference: prefers bold, original design decisions over safe, generic layouts[0m
[38;2;255;255;255;48;2;19;87;20m+  Honesty directive: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 20% from the relevant accuracy component before final scoring[0m
[38;2;255;255;255;48;2;19;87;20m+  Concise analyst: prefers one dense table over three paragraphs[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-mockup-curator-changes.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-mockup-curator-changes.py[0m
[38;2;139;134;130m@@ -0,0 +1,163 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: mockup-comparison-curator blueprint+persona changes."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\mockup-comparison-curator"[0m
[38;2;255;255;255;48;2;19;87;20m+PASS = 0[0m
[38;2;255;255;255;48;2;19;87;20m+FAIL = 0[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(label, condition, detail=""):[0m
[38;2;255;255;255;48;2;19;87;20m+    global PASS, FAIL[0m
[38;2;255;255;255;48;2;19;87;20m+    if condition:[0m
[38;2;255;255;255;48;2;19;87;20m+        PASS += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  PASS  {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        FAIL += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL  {label}  {detail}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def load(path):[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        return f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+bp = load(os.path.join(BASE, "BLUEPRINT.md"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== BLUEPRINT.md ===")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. No standalone "Deliverable Integrity" section[0m
[38;2;255;255;255;48;2;19;87;20m+check([0m
[38;2;255;255;255;48;2;19;87;20m+    "No standalone '## Deliverable Integrity' section",[0m
[38;2;255;255;255;48;2;19;87;20m+    "## Deliverable Integrity" not in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. Deliverable Status Tags exists under Output Validation[0m
[38;2;255;255;255;48;2;19;87;20m+check([0m
[38;2;255;255;255;48;2;19;87;20m+    "'### Deliverable Status Tags' exists under Output Validation",[0m
[38;2;255;255;255;48;2;19;87;20m+    "### Deliverable Status Tags" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. Status tags content (functional/simulated/mock) present[0m
[38;2;255;255;255;48;2;19;87;20m+check([0m
[38;2;255;255;255;48;2;19;87;20m+    "Status tags: functional, simulated, mock defined",[0m
[38;2;255;255;255;48;2;19;87;20m+    all(t in bp for t in ["functional:", "simulated:", "mock:"]),[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. Communication Constraints section exists[0m
[38;2;255;255;255;48;2;19;87;20m+check([0m
[38;2;255;255;255;48;2;19;87;20m+    "'## Communication Constraints' section exists",[0m
[38;2;255;255;255;48;2;19;87;20m+    "## Communication Constraints" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 5. Communication Constraints has all 5 rules[0m
[38;2;255;255;255;48;2;19;87;20m+cc_rules = ["No conversational prefaces", "No post-summaries", "No change-lists", "No meta-commentary", "All content in a single response"][0m
[38;2;255;255;255;48;2;19;87;20m+for rule in cc_rules:[0m
[38;2;255;255;255;48;2;19;87;20m+    check([0m
[38;2;255;255;255;48;2;19;87;20m+        f"Communication Constraints: '{rule}'",[0m
[38;2;255;255;255;48;2;19;87;20m+        rule in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+    )[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 6. Anti-Patterns starts with Conversational framing (item #1)[0m
[38;2;255;255;255;48;2;19;87;20m+check([0m
[38;2;255;255;255;48;2;19;87;20m+    "Anti-Patterns: '1. Conversational framing' is first item",[0m
[38;2;255;255;255;48;2;19;87;20m+    "**1. Conversational framing**" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 7. Anti-Patterns has banned/correct examples[0m
[38;2;255;255;255;48;2;19;87;20m+check([0m
[38;2;255;255;255;48;2;19;87;20m+    "Anti-Patterns: banned/correct examples present",[0m
[38;2;255;255;255;48;2;19;87;20m+    "Banned:" in bp and "Correct:" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 8. Anti-Patterns has all 5 numbered items[0m
[38;2;255;255;255;48;2;19;87;20m+for num in range(1, 6):[0m
[38;2;255;255;255;48;2;19;87;20m+    check([0m
[38;2;255;255;255;48;2;19;87;20m+        f"Anti-Patterns: item {num} present",[0m
[38;2;255;255;255;48;2;19;87;20m+        f"**{num}." in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+    )[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 9. Output Validation has the consolidation header[0m
[38;2;139;134;130m… omitted 85 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification: 29/29 PASSED, godkänd. Temp-städad.
**Sammanfattning av ändringarna:**
| Feedback | Ändring | Fil |
|---|---|---|
| 87.6: Output Contract overlappar Output Validation | Deliverable Integrity borttagen som egen sektion, innehållet flyttat under Output Validation > Deliverable Status Tags | BLUEPRINT.md |
| 87.6: Lägg till 'No conversational framing' i Anti-Patterns | Conversational framing som #1 med banned/correct exempel | BLUEPRINT.md |
| 80.8: Lägg till communication constraints | Ny Communication Constraints-sektion med 5 regler | BLUEPRINT.md |
| 80.8/87.6: Byt deliverable-first mot output-compaction | Output-compaction regeln först i persona.md med explicit förbud mot prefaces/summaries/change-lists | persona.md |
| 87.6: Konvertera paragraph-regler till list-syntax | Alla 11 regler använder konsekvent två-space indent, tydliga etiketter | persona.md |
Inga gamla sektioner, inget redundant, inget konversationellt ramverk kvar. Båda filerna är redo för nästa evalueringskörning.