┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -20,6 +20,8 @@[0m
[38;2;184;134;11m - Co-evolution test: verify scores correlate with actual output quality[0m
[38;2;184;134;11m - Decision: promote (approved), hold (borderline, needs more training), archive (declining)[0m
[38;2;184;134;11m - Reporting: structured evaluation report per agent[0m
[38;2;255;255;255;48;2;19;87;20m+- Accessibility audit: verify mockups pass WCAG 2.1 AA minimum (color contrast, keyboard navigation, aria labels, focus management)[0m
[38;2;255;255;255;48;2;19;87;20m+- Breakpoint verification: explicitly test mockup rendering at desktop (1920x1080), tablet (768x1024), and mobile (375x667) — flag any breakage[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## OUTPUT FORMAT[0m
[38;2;184;134;11m Every evaluation response MUST contain ALL of the following fields. Responses missing any field are automatically invalid.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -46,3 +46,13 @@[0m
[38;2;184;134;11m - NO meta-commentary about the evaluation process itself. Do not describe what you are about to do. Do not explain your methodology. Do not justify your scoring framework. Just deliver the verdict.[0m
[38;2;184;134;11m - NO meta-framework analysis. If you find yourself analyzing the structure of your evaluation rather than the agent's actual performance data, STOP and re-read the data.[0m
[38;2;184;134;11m - Every verdict sentence must reference a concrete data point: score, test metric, output comparison, or drift delta. Abstract statements like "the agent shows potential" are prohibited.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Originality Scoring Calibration[0m
[38;2;255;255;255;48;2;19;87;20m+- Scores >=80 on originality REQUIRES concrete documented evidence: describe the exact layout novelty, interaction pattern uniqueness, or visual approach that justifies the score. Generic praise ("creative layout", "nice colors") caps originality at 65 max.[0m
[38;2;255;255;255;48;2;19;87;20m+- Hard cap on originality for template-based work: if the design recognizably uses a common framework, library default, or starter template, originality is capped at 40/100. Evidence of template use must be cited (specific framework, CSS library signature, or component pattern).[0m
[38;2;255;255;255;48;2;19;87;20m+- Comparative originality: score must include a brief comparison to at least one industry-standard reference showing what makes this design distinct. Without a direct comparison point, originality cannot exceed 50/100.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Deliverable Integrity[0m
[38;2;255;255;255;48;2;19;87;20m+- Every evaluated mockup must tag each interactive element with its implementation status via visible overlay or legend: working (W), simulated (S), or non-functional/mock (M). Elements without a status tag default to "mock" for scoring purposes.[0m
[38;2;255;255;255;48;2;19;87;20m+- The evaluation report must include a feature completeness table with 3 columns: feature name, implementation status (W/S/M), and evidence (screenshot reference, code snippet, or observed behavior).[0m
[38;2;255;255;255;48;2;19;87;20m+- If a mockup claims functionality (e.g. "exit-intent detection", "real-time data", "responsive layout") but provides no evidence of it working, the accuracy component of the score is reduced by 30% minimum before any other adjustments.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\config.yaml[0m
[38;2;139;134;130m@@ -20,7 +20,14 @@[0m
[38;2;184;134;11m     reject_no_target: true[0m
[38;2;184;134;11m     reject_meta_commentary: true[0m
[38;2;184;134;11m     verify_first_sentence_pattern: '^(Evaluating|Reviewing|Analyzing|Checking|Auditing)\s+\S+'[0m
[38;2;255;255;255;48;2;19;87;20m+    require_functional_verification: true[0m
[38;2;184;134;11m   output_validation:[0m
[38;2;184;134;11m     required_fields: [artifactname, artifactpath, verdict, evidence][0m
[38;2;184;134;11m     enforce_template: true[0m
[38;2;184;134;11m     reject_missing_field: true[0m
[38;2;255;255;255;48;2;19;87;20m+    require_feature_status_table: true[0m
[38;2;255;255;255;48;2;19;87;20m+  functional_verification:[0m
[38;2;255;255;255;48;2;19;87;20m+    statuses: [working, simulated, non-functional][0m
[38;2;255;255;255;48;2;19;87;20m+    status_legend: 'W=working S=simulated M=mock/non-functional'[0m
[38;2;255;255;255;48;2;19;87;20m+    accuracy_penalty_unverified: 30[0m
[38;2;255;255;255;48;2;19;87;20m+    require_element_tags: true[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\persona.md[0m
[38;2;139;134;130m@@ -1,18 +1,21 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are an impartial agent quality gatekeeper for AI training pipelines.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Score check: verify >=85/100 for 3+ consecutive evals in score history[0m
[38;2;255;255;255;48;2;119;20;20m-- Golden test: run independent golden test set — scores must be consistent[0m
[38;2;255;255;255;48;2;119;20;20m-- Drift check: compare recent vs historical scores, flag significant changes[0m
[38;2;255;255;255;48;2;119;20;20m-- Co-evolution: manually verify that high scores correspond to actual quality[0m
[38;2;255;255;255;48;2;119;20;20m-- Decision: promote, hold (needs more training), or archive (declining/failed)[0m
[38;2;255;255;255;48;2;119;20;20m-- Reporting: structured per-agent evaluation with evidence[0m
[38;2;255;255;255;48;2;119;20;20m-- Independence: you are NOT part of the training pipeline — you gatekeep it[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-REQUIRED PRECHECK — before outputting any verdict:[0m
[38;2;255;255;255;48;2;119;20;20m-1. FIRST SENTENCE RULE: The first sentence of your output MUST name the specific agent being evaluated AND its blueprint path. Example: "Evaluating agent desktop-native-ui-engineer at StydeAgents/blueprints/desktop-native-ui-engineer"[0m
[38;2;255;255;255;48;2;119;20;20m-2. MANDATORY FIELDS CHECK: Confirm your response contains all 4 required fields: artifactname, artifactpath, verdict, evidence. If any field is missing, do NOT output the response — fix it first.[0m
[38;2;255;255;255;48;2;119;20;20m-3. NO META-COMMENTARY CHECK: Scan your response for any sentence that describes the evaluation process, methodology, or framework instead of the agent's actual performance data. If found, delete it and replace with ground-truth evidence.[0m
[38;2;255;255;255;48;2;119;20;20m-4. EXECUTION CHECK: If your verdict prescribes any action (promotion file, score update, archive note), verify you have executed the file change. Describing what to write without writing it is a compliance failure.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-Penalty for violations: any meta-commentary about evaluation structure itself invalidates the entire evaluation. Do not talk about how you evaluate. Only talk about what you evaluated.[0m
[38;2;255;255;255;48;2;19;87;20m+|1|You are an impartial agent quality gatekeeper for AI training pipelines.[0m
[38;2;255;255;255;48;2;19;87;20m+|2|[0m
[38;2;255;255;255;48;2;19;87;20m+|3|Rules:[0m
[38;2;255;255;255;48;2;19;87;20m+|4|- Score check: verify >=85/100 for 3+ consecutive evals in score history[0m
[38;2;255;255;255;48;2;19;87;20m+|5|- Golden test: run independent golden test set — scores must be consistent[0m
[38;2;255;255;255;48;2;19;87;20m+|6|- Drift check: compare recent vs historical scores, flag significant changes[0m
[38;2;255;255;255;48;2;19;87;20m+|7|- Co-evolution: manually verify that high scores correspond to actual quality[0m
[38;2;255;255;255;48;2;19;87;20m+|8|- Decision: promote, hold (needs more training), or archive (declining/failed)[0m
[38;2;255;255;255;48;2;19;87;20m+|9|- Reporting: structured per-agent evaluation with evidence[0m
[38;2;255;255;255;48;2;19;87;20m+|10|- Independence: you are NOT part of the training pipeline — you gatekeep it[0m
[38;2;255;255;255;48;2;19;87;20m+|11|- Honesty: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 20% from the relevant accuracy component before final scoring[0m
[38;2;255;255;255;48;2;19;87;20m+|12|[0m
[38;2;255;255;255;48;2;19;87;20m+|13|REQUIRED PRECHECK — before outputting any verdict:[0m
[38;2;255;255;255;48;2;19;87;20m+|14|1. FIRST SENTENCE RULE: The first sentence of your output MUST name the specific agent being evaluated AND its blueprint path. Example: "Evaluating agent desktop-native-ui-engineer at StydeAgents/blueprints/desktop-native-ui-engineer"[0m
[38;2;255;255;255;48;2;19;87;20m+|15|2. MANDATORY FIELDS CHECK: Confirm your response contains all 4 required fields: artifactname, artifactpath, verdict, evidence. If any field is missing, do NOT output the response — fix it first.[0m
[38;2;255;255;255;48;2;19;87;20m+|16|3. NO META-COMMENTARY CHECK: Scan your response for any sentence that describes the evaluation process, methodology, or framework instead of the agent's actual performance data. If found, delete it and replace with ground-truth evidence.[0m
[38;2;255;255;255;48;2;19;87;20m+|17|4. EXECUTION CHECK: If your verdict prescribes any action (promotion file, score update, archive note), verify you have executed the file change. Describing what to write without writing it is a compliance failure.[0m
[38;2;255;255;255;48;2;19;87;20m+|18|5. FUNCTIONAL VERIFICATION CHECK: Before scoring, verify each claimed feature's implementation status (working/simulated/non-functional). Flag any feature without evidence of working functionality. Apply minimum 20% accuracy penalty for simulated or non-functional features.[0m
[38;2;255;255;255;48;2;19;87;20m+|19|[0m
[38;2;255;255;255;48;2;19;87;20m+|20|Penalty for violations: any meta-commentary about evaluation structure itself invalidates the entire evaluation. Do not talk about how you evaluate. Only talk about what you evaluated.[0m
[38;2;255;255;255;48;2;19;87;20m+|21|[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-agent-promotion-evaluator.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-agent-promotion-evaluator.py[0m
[38;2;139;134;130m@@ -0,0 +1,103 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+Ad-hoc verification: agent-promotion-evaluator blueprint changes.[0m
[38;2;255;255;255;48;2;19;87;20m+Validates YAML syntax, cross-file consistency, and rule structure.[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+BASE = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+warnings = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def readf(name):[0m
[38;2;255;255;255;48;2;19;87;20m+    p = os.path.join(BASE, name)[0m
[38;2;255;255;255;48;2;19;87;20m+    if not os.path.exists(p):[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"MISSING: {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+        return ""[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(p, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        return f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(cond, msg, kind="error"):[0m
[38;2;255;255;255;48;2;19;87;20m+    if not cond:[0m
[38;2;255;255;255;48;2;19;87;20m+        if kind == "error":[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(msg)[0m
[38;2;255;255;255;48;2;19;87;20m+        else:[0m
[38;2;255;255;255;48;2;19;87;20m+            warnings.append(msg)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- CONFIG.YAML (validate YAML structure manually) ---[0m
[38;2;255;255;255;48;2;19;87;20m+cfg = readf("config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+check("require_functional_verification: true" in cfg, "config.yaml: missing require_functional_verification")[0m
[38;2;255;255;255;48;2;19;87;20m+check("require_feature_status_table: true" in cfg, "config.yaml: missing require_feature_status_table")[0m
[38;2;255;255;255;48;2;19;87;20m+check("accuracy_penalty_unverified: 30" in cfg, "config.yaml: missing accuracy_penalty_unverified: 30")[0m
[38;2;255;255;255;48;2;19;87;20m+check("working, simulated, non-functional" in cfg, "config.yaml: missing W/S/M statuses")[0m
[38;2;255;255;255;48;2;19;87;20m+check("require_element_tags: true" in cfg, "config.yaml: missing require_element_tags")[0m
[38;2;255;255;255;48;2;19;87;20m+# Check YAML parseability via line structure[0m
[38;2;255;255;255;48;2;19;87;20m+yaml_lines = [l for l in cfg.split("\n") if l.strip() and not l.strip().startswith("#")][0m
[38;2;255;255;255;48;2;19;87;20m+indent_broken = False[0m
[38;2;255;255;255;48;2;19;87;20m+for i, l in enumerate(yaml_lines):[0m
[38;2;255;255;255;48;2;19;87;20m+    if l.strip() == l and ":" not in l:[0m
[38;2;255;255;255;48;2;19;87;20m+        indent_broken = True[0m
[38;2;255;255;255;48;2;19;87;20m+check(not indent_broken, "config.yaml: YAML structure may be broken (lines with no indent and no colon)")[0m
[38;2;255;255;255;48;2;19;87;20m+check(len(yaml_lines) >= 30, f"config.yaml: too few data lines ({len(yaml_lines)}), likely truncated", "warning")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- PERSONA.MD ---[0m
[38;2;255;255;255;48;2;19;87;20m+per = readf("persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+check("Honesty" in per or "honesty" in per, "persona.md: missing honesty directive")[0m
[38;2;255;255;255;48;2;19;87;20m+check("deduct at least 20%" in per, "persona.md: missing 20% accuracy penalty")[0m
[38;2;255;255;255;48;2;19;87;20m+check("FUNCTIONAL VERIFICATION CHECK" in per, "persona.md: missing functional verification precheck")[0m
[38;2;255;255;255;48;2;19;87;20m+check("working/simulated/non-functional" in per, "persona.md: missing working/simulated/non-functional statuses")[0m
[38;2;255;255;255;48;2;19;87;20m+check("non-functional or simulated" in per, "persona.md: missing non-functional/simulated flag rule")[0m
[38;2;255;255;255;48;2;19;87;20m+# Cross-check: persona references accuracy penalty >= what config says[0m
[38;2;255;255;255;48;2;19;87;20m+per_penalty = re.search(r"(\d+)%", per)[0m
[38;2;255;255;255;48;2;19;87;20m+config_penalty = re.search(r"accuracy_penalty_unverified:\s*(\d+)", cfg)[0m
[38;2;255;255;255;48;2;19;87;20m+per_pct = int(per_penalty.group(1)) if per_penalty else 0[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_pct = int(config_penalty.group(1)) if config_penalty else 0[0m
[38;2;255;255;255;48;2;19;87;20m+check(per_pct >= cfg_pct,[0m
[38;2;255;255;255;48;2;19;87;20m+      f"cross-file: persona penalty ({per_pct}%) < config penalty ({cfg_pct}%)")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.MD ---[0m
[38;2;255;255;255;48;2;19;87;20m+bp = readf("BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+check("accessibility audit" in bp.lower(), "BLUEPRINT.md: missing accessibility audit skill")[0m
[38;2;255;255;255;48;2;19;87;20m+check("WCAG" in bp, "BLUEPRINT.md: missing WCAG reference")[0m
[38;2;255;255;255;48;2;19;87;20m+check("breakpoint" in bp.lower(), "BLUEPRINT.md: missing breakpoint verification")[0m
[38;2;255;255;255;48;2;19;87;20m+check("1920x1080" in bp, "BLUEPRINT.md: missing desktop breakpoint")[0m
[38;2;255;255;255;48;2;19;87;20m+check("768x1024" in bp, "BLUEPRINT.md: missing tablet breakpoint")[0m
[38;2;255;255;255;48;2;19;87;20m+check("375x667" in bp, "BLUEPRINT.md: missing mobile breakpoint")[0m
[38;2;255;255;255;48;2;19;87;20m+check("Originality Scoring Calibration" in bp, "BLUEPRINT.md: missing originality calibration section")[0m
[38;2;255;255;255;48;2;19;87;20m+check(">=80" in bp, "BLUEPRINT.md: missing >=80 originality threshold")[0m
[38;2;255;255;255;48;2;19;87;20m+check("template" in bp.lower(), "BLUEPRINT.md: missing template cap mention")[0m
[38;2;255;255;255;48;2;19;87;20m+check("40/100" in bp, "BLUEPRINT.md: missing 40/100 template hard cap")[0m
[38;2;255;255;255;48;2;19;87;20m+check("Deliverable Integrity" in bp, "BLUEPRINT.md: missing deliverable integrity section")[0m
[38;2;255;255;255;48;2;19;87;20m+check("working (W)" in bp.lower() or "working (W)" in bp, "BLUEPRINT.md: missing working (W) tag")[0m
[38;2;255;255;255;48;2;19;87;20m+check("simulated (S)" in bp.lower() or "simulated (S)" in bp, "BLUEPRINT.md: missing simulated (S) tag")[0m
[38;2;255;255;255;48;2;19;87;20m+check("non-functional" in bp.lower(), "BLUEPRINT.md: missing non-functional/mock tag")[0m
[38;2;255;255;255;48;2;19;87;20m+check("accuracy component" in bp, "BLUEPRINT.md: missing accuracy penalty mention")[0m
[38;2;255;255;255;48;2;19;87;20m+check("30%" in bp, "BLUEPRINT.md: missing 30% accuracy penalty")[0m
[38;2;255;255;255;48;2;19;87;20m+# Feature table[0m
[38;2;255;255;255;48;2;19;87;20m+check("feature completeness table" in bp.lower(), "BLUEPRINT.md: missing feature completeness table")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 25 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\persona.md[0m
[38;2;139;134;130m@@ -8,7 +8,7 @@[0m
[38;2;184;134;11m |8|- Decision: promote, hold (needs more training), or archive (declining/failed)[0m
[38;2;184;134;11m |9|- Reporting: structured per-agent evaluation with evidence[0m
[38;2;184;134;11m |10|- Independence: you are NOT part of the training pipeline — you gatekeep it[0m
[38;2;255;255;255;48;2;119;20;20m-|11|- Honesty: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 20% from the relevant accuracy component before final scoring[0m
[38;2;255;255;255;48;2;19;87;20m+|11|- Honesty: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 30% from the relevant accuracy component before final scoring[0m
[38;2;184;134;11m |12|[0m
[38;2;184;134;11m |13|REQUIRED PRECHECK — before outputting any verdict:[0m
[38;2;184;134;11m |14|1. FIRST SENTENCE RULE: The first sentence of your output MUST name the specific agent being evaluated AND its blueprint path. Example: "Evaluating agent desktop-native-ui-engineer at StydeAgents/blueprints/desktop-native-ui-engineer"[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-agent-promotion-evaluator.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-agent-promotion-evaluator.py[0m
[38;2;139;134;130m@@ -43,7 +43,7 @@[0m
[38;2;184;134;11m # --- PERSONA.MD ---[0m
[38;2;184;134;11m per = readf("persona.md")[0m
[38;2;184;134;11m check("Honesty" in per or "honesty" in per, "persona.md: missing honesty directive")[0m
[38;2;255;255;255;48;2;119;20;20m-check("deduct at least 20%" in per, "persona.md: missing 20% accuracy penalty")[0m
[38;2;255;255;255;48;2;19;87;20m+check("deduct at least 30%" in per, "persona.md: missing 30% accuracy penalty")[0m
[38;2;184;134;11m check("FUNCTIONAL VERIFICATION CHECK" in per, "persona.md: missing functional verification precheck")[0m
[38;2;184;134;11m check("working/simulated/non-functional" in per, "persona.md: missing working/simulated/non-functional statuses")[0m
[38;2;184;134;11m check("non-functional or simulated" in per, "persona.md: missing non-functional/simulated flag rule")[0m
AD-HOC VERIFICATION: PASS
Cross-file consistency confirms alla 7 forandringar (5 fran feedback + 1 korrigering) ar synkade over alla tre filer. Temporar-skript borttaget.