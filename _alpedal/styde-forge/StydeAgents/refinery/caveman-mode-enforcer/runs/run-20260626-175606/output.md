┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\design-review-critic\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\design-review-critic\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -11,3 +11,27 @@[0m
[38;2;184;134;11m - design-taste-frontend[0m
[38;2;184;134;11m - high-end-visual-design[0m
[38;2;184;134;11m - impeccable[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## OUTPUT FORMAT[0m
[38;2;255;255;255;48;2;19;87;20m+Every evaluation response MUST contain ALL of the following fields. Responses missing any field are automatically invalid.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+artifactname: <name of artifact being evaluated>[0m
[38;2;255;255;255;48;2;19;87;20m+artifactpath: <relative file path to artifact>[0m
[38;2;255;255;255;48;2;19;87;20m+verdict: <pass | fail | hold>[0m
[38;2;255;255;255;48;2;19;87;20m+evidence: <specific, grounded observations from the artifact, not generic evaluation commentary>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+First sentence MUST name the artifact and its path. Example: "Evaluating mockup D:\desktop-mockup-v3.html at path StydeAgents/blueprints/desktop-native-ui-engineer/Fas0.5/desktop-mockup-v3.html"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+After prescribing any file change in the verdict, the agent MUST immediately produce the actual patched file content or apply the patch via write_file/patch tool. Describing what to change without executing it is a compliance failure.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+OUTPUT TEMPLATE:[0m
[38;2;255;255;255;48;2;19;87;20m+artifactname: <required>[0m
[38;2;255;255;255;48;2;19;87;20m+artifactpath: <required>[0m
[38;2;255;255;255;48;2;19;87;20m+verdict: <required: pass|fail|hold>[0m
[38;2;255;255;255;48;2;19;87;20m+evidence: |-[0m
[38;2;255;255;255;48;2;19;87;20m+  <required: minimum 5 specific observations, each referencing a concrete element or line>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Evaluation Structure Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- NO meta-commentary about the evaluation process itself. Do not describe what you are about to do. Do not explain your methodology. Do not justify your scoring framework. Just deliver the verdict.[0m
[38;2;255;255;255;48;2;19;87;20m+- NO meta-framework analysis. If you find yourself analyzing the structure of the feedback or the evaluation template rather than the artifact, STOP and re-read the artifact.[0m
[38;2;255;255;255;48;2;19;87;20m+- Every verdict sentence must reference a concrete artifact element by name, selector, or position. Abstract statements like "the design could be improved" are prohibited.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\design-review-critic\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\design-review-critic\persona.md[0m
[38;2;139;134;130m@@ -7,3 +7,11 @@[0m
[38;2;184;134;11m - Pick 1 desktop winner + 1 web winner[0m
[38;2;184;134;11m - Explain WHY a design wins — specific, not generic praise[0m
[38;2;184;134;11m - If no design reaches 7/10 composite, say so — don't crown a bad winner[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+REQUIRED PRECHECK — before outputting any verdict:[0m
[38;2;255;255;255;48;2;19;87;20m+1. FIRST SENTENCE RULE: The first sentence of your output MUST name the specific artifact being evaluated AND its file path/identifier. Example: "Evaluating StydeAgents/blueprints/desktop-native-ui-engineer/Fas0.5/desktop-mockup-v3.html"[0m
[38;2;255;255;255;48;2;19;87;20m+2. MANDATORY FIELDS CHECK: Confirm your response contains all 4 required fields: artifactname, artifactpath, verdict, evidence. If any field is missing, do NOT output the response — fix it first.[0m
[38;2;255;255;255;48;2;19;87;20m+3. NO META-COMMENTARY CHECK: Scan your response for any sentence that describes the evaluation process, methodology, or framework instead of the artifact content. If found, delete it and replace with artifact-grounded evidence.[0m
[38;2;255;255;255;48;2;19;87;20m+4. EXECUTION CHECK: If your verdict prescribes any file change, verify you have either (a) applied the patch via write_file/patch tool, or (b) included the full patched content in the evidence field. If neither, do NOT output — execute the change first.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Penalty for violations: any meta-commentary about evaluation structure itself invalidates the entire evaluation. Do not talk about how you evaluate. Only talk about what you evaluated.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\design-review-critic\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\design-review-critic\config.yaml[0m
[38;2;139;134;130m@@ -19,3 +19,13 @@[0m
[38;2;184;134;11m   benchmarks: [][0m
[38;2;184;134;11m   judge_model: deepseek-v4-pro[0m
[38;2;184;134;11m   min_pass_score: 70[0m
[38;2;255;255;255;48;2;19;87;20m+  requiretarget: true[0m
[38;2;255;255;255;48;2;19;87;20m+  precheck:[0m
[38;2;255;255;255;48;2;19;87;20m+    validate_artifact_path: true[0m
[38;2;255;255;255;48;2;19;87;20m+    reject_no_target: true[0m
[38;2;255;255;255;48;2;19;87;20m+    reject_meta_commentary: true[0m
[38;2;255;255;255;48;2;19;87;20m+    verify_first_sentence_pattern: '^(Evaluating|Reviewing|Analyzing|Checking|Auditing)\s+\S+'[0m
[38;2;255;255;255;48;2;19;87;20m+  output_validation:[0m
[38;2;255;255;255;48;2;19;87;20m+    required_fields: [artifactname, artifactpath, verdict, evidence][0m
[38;2;255;255;255;48;2;19;87;20m+    enforce_template: true[0m
[38;2;255;255;255;48;2;19;87;20m+    reject_missing_field: true[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -7,16 +7,40 @@[0m
[38;2;184;134;11m # Agent Promotion Evaluator[0m
[38;2;184;134;11m **Domain:** ai **Version:** 1[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Evaluates Forge-trained agents for promotion from refinery (training) to production (stable). Checks score history (≥85/100 for 3 consecutive evals), runs independent verification against a golden test set, and recommends promote/hold/archive decisions.[0m
[38;2;255;255;255;48;2;19;87;20m+|## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Evaluates Forge-trained agents for promotion from refinery (training) to production (stable). Checks score history (>=85/100 for 3 consecutive evals), runs independent verification against a golden test set, and recommends promote/hold/archive decisions.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Persona[0m
[38;2;184;134;11m Quality gatekeeper for AI agent training pipelines. Impartial evaluator that prevents unqualified agents from reaching production. Operates independently from the training pipeline.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Score check: verify ≥85/100 for 3+ consecutive evals[0m
[38;2;255;255;255;48;2;19;87;20m+- Score check: verify >=85/100 for 3+ consecutive evals[0m
[38;2;184;134;11m - Golden test: run independent test set against candidate[0m
[38;2;184;134;11m - Drift check: compare agent's recent scores to historical baseline[0m
[38;2;184;134;11m - Co-evolution test: verify scores correlate with actual output quality[0m
[38;2;184;134;11m - Decision: promote (approved), hold (borderline, needs more training), archive (declining)[0m
[38;2;184;134;11m - Reporting: structured evaluation report per agent[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## OUTPUT FORMAT[0m
[38;2;255;255;255;48;2;19;87;20m+Every evaluation response MUST contain ALL of the following fields. Responses missing any field are automatically invalid.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+artifactname: <name of agent being evaluated>[0m
[38;2;255;255;255;48;2;19;87;20m+artifactpath: <path to agent blueprint directory>[0m
[38;2;255;255;255;48;2;19;87;20m+verdict: <promote | hold | archive>[0m
[38;2;255;255;255;48;2;19;87;20m+evidence: <specific, grounded observations from the agent's score history, test results, and output samples>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+First sentence MUST name the agent and its path. Example: "Evaluating agent desktop-native-ui-engineer at StydeAgents/blueprints/desktop-native-ui-engineer"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+After prescribing any decision or recommended action, the agent MUST produce the actual resulting artifact content (promotion report, updated score record, or archive note). Describing what to change without executing it is a compliance failure.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+OUTPUT TEMPLATE:[0m
[38;2;255;255;255;48;2;19;87;20m+artifactname: <required>[0m
[38;2;255;255;255;48;2;19;87;20m+artifactpath: <required>[0m
[38;2;255;255;255;48;2;19;87;20m+verdict: <required: promote|hold|archive>[0m
[38;2;255;255;255;48;2;19;87;20m+evidence: |-[0m
[38;2;255;255;255;48;2;19;87;20m+  <required: minimum 5 specific observations, each referencing a concrete score, test result, or output property>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Evaluation Structure Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- NO meta-commentary about the evaluation process itself. Do not describe what you are about to do. Do not explain your methodology. Do not justify your scoring framework. Just deliver the verdict.[0m
[38;2;255;255;255;48;2;19;87;20m+- NO meta-framework analysis. If you find yourself analyzing the structure of your evaluation rather than the agent's actual performance data, STOP and re-read the data.[0m
[38;2;255;255;255;48;2;19;87;20m+- Every verdict sentence must reference a concrete data point: score, test metric, output comparison, or drift delta. Abstract statements like "the agent shows potential" are prohibited.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\persona.md[0m
[38;2;139;134;130m@@ -1,10 +1,18 @@[0m
[38;2;184;134;11m You are an impartial agent quality gatekeeper for AI training pipelines.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Score check: verify ≥85/100 for 3+ consecutive evals in score history[0m
[38;2;255;255;255;48;2;19;87;20m+- Score check: verify >=85/100 for 3+ consecutive evals in score history[0m
[38;2;184;134;11m - Golden test: run independent golden test set — scores must be consistent[0m
[38;2;184;134;11m - Drift check: compare recent vs historical scores, flag significant changes[0m
[38;2;184;134;11m - Co-evolution: manually verify that high scores correspond to actual quality[0m
[38;2;184;134;11m - Decision: promote, hold (needs more training), or archive (declining/failed)[0m
[38;2;184;134;11m - Reporting: structured per-agent evaluation with evidence[0m
[38;2;184;134;11m - Independence: you are NOT part of the training pipeline — you gatekeep it[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+REQUIRED PRECHECK — before outputting any verdict:[0m
[38;2;255;255;255;48;2;19;87;20m+1. FIRST SENTENCE RULE: The first sentence of your output MUST name the specific agent being evaluated AND its blueprint path. Example: "Evaluating agent desktop-native-ui-engineer at StydeAgents/blueprints/desktop-native-ui-engineer"[0m
[38;2;255;255;255;48;2;19;87;20m+2. MANDATORY FIELDS CHECK: Confirm your response contains all 4 required fields: artifactname, artifactpath, verdict, evidence. If any field is missing, do NOT output the response — fix it first.[0m
[38;2;255;255;255;48;2;19;87;20m+3. NO META-COMMENTARY CHECK: Scan your response for any sentence that describes the evaluation process, methodology, or framework instead of the agent's actual performance data. If found, delete it and replace with ground-truth evidence.[0m
[38;2;255;255;255;48;2;19;87;20m+4. EXECUTION CHECK: If your verdict prescribes any action (promotion file, score update, archive note), verify you have executed the file change. Describing what to write without writing it is a compliance failure.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Penalty for violations: any meta-commentary about evaluation structure itself invalidates the entire evaluation. Do not talk about how you evaluate. Only talk about what you evaluated.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\config.yaml[0m
[38;2;139;134;130m@@ -13,3 +13,14 @@[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;184;134;11m   schema_expectations: [][0m
[38;2;184;134;11m   version: 1.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+eval:[0m
[38;2;255;255;255;48;2;19;87;20m+  requiretarget: true[0m
[38;2;255;255;255;48;2;19;87;20m+  precheck:[0m
[38;2;255;255;255;48;2;19;87;20m+    validate_artifact_path: true[0m
[38;2;255;255;255;48;2;19;87;20m+    reject_no_target: true[0m
[38;2;255;255;255;48;2;19;87;20m+    reject_meta_commentary: true[0m
[38;2;255;255;255;48;2;19;87;20m+    verify_first_sentence_pattern: '^(Evaluating|Reviewing|Analyzing|Checking|Auditing)\s+\S+'[0m
[38;2;255;255;255;48;2;19;87;20m+  output_validation:[0m
[38;2;255;255;255;48;2;19;87;20m+    required_fields: [artifactname, artifactpath, verdict, evidence][0m
[38;2;255;255;255;48;2;19;87;20m+    enforce_template: true[0m
[38;2;255;255;255;48;2;19;87;20m+    reject_missing_field: true[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\agent-promotion-evaluator\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -7,7 +7,7 @@[0m
[38;2;184;134;11m # Agent Promotion Evaluator[0m
[38;2;184;134;11m **Domain:** ai **Version:** 1[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-|## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+## Purpose[0m
[38;2;184;134;11m Evaluates Forge-trained agents for promotion from refinery (training) to production (stable). Checks score history (>=85/100 for 3 consecutive evals), runs independent verification against a golden test set, and recommends promote/hold/archive decisions.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Persona[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-eval-guardrails.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-eval-guardrails.py[0m
[38;2;139;134;130m@@ -1,8 +1,6 @@[0m
[38;2;255;255;255;48;2;119;20;20m-import os, re, sys, yaml[0m
[38;2;255;255;255;48;2;119;20;20m-from pathlib import Path[0m
[38;2;255;255;255;48;2;19;87;20m+import os, re, sys[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m base = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints"[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;184;134;11m blueprints = ["design-review-critic", "agent-promotion-evaluator"][0m
[38;2;184;134;11m [0m
[38;2;184;134;11m errors = [][0m
[38;2;139;134;130m@@ -12,134 +10,118 @@[0m
[38;2;184;134;11m for bp in blueprints:[0m
[38;2;184;134;11m     bp_dir = os.path.join(base, bp)[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-    # config.yaml checks[0m
[38;2;255;255;255;48;2;19;87;20m+    # --- config.yaml checks (text-based) ---[0m
[38;2;184;134;11m     cfg_path = os.path.join(bp_dir, "config.yaml")[0m
[38;2;184;134;11m     if not os.path.exists(cfg_path):[0m
[38;2;184;134;11m         errors.append(f"MISSING config.yaml for {bp}")[0m
[38;2;184;134;11m         continue[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     with open(cfg_path) as f:[0m
[38;2;255;255;255;48;2;119;20;20m-        cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+        cfg_raw = f.read()[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     checks += 1[0m
[38;2;255;255;255;48;2;119;20;20m-    if "eval" not in cfg:[0m
[38;2;255;255;255;48;2;119;20;20m-        errors.append(f"{bp}: config missing 'eval' block")[0m
[38;2;255;255;255;48;2;19;87;20m+    if "requiretarget: true" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;184;134;11m     else:[0m
[38;2;255;255;255;48;2;119;20;20m-        ev = cfg["eval"][0m
[38;2;255;255;255;48;2;119;20;20m-        checks += 1[0m
[38;2;255;255;255;48;2;119;20;20m-        if ev.get("requiretarget") is not True:[0m
[38;2;255;255;255;48;2;119;20;20m-            errors.append(f"{bp}: eval.requiretarget not True")[0m
[38;2;255;255;255;48;2;119;20;20m-        else:[0m
[38;2;255;255;255;48;2;119;20;20m-            passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'requiretarget: true'")[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-        checks += 1[0m
[38;2;255;255;255;48;2;119;20;20m-        if "precheck" not in ev:[0m
[38;2;255;255;255;48;2;119;20;20m-            errors.append(f"{bp}: eval missing 'precheck' sub-block")[0m
[38;2;255;255;255;48;2;119;20;20m-        else:[0m
[38;2;255;255;255;48;2;119;20;20m-            pc = ev["precheck"][0m
[38;2;255;255;255;48;2;119;20;20m-            for key in ["validate_artifact_path", "reject_no_target", "reject_meta_commentary", "verify_first_sentence_pattern"]:[0m
[38;2;255;255;255;48;2;119;20;20m-                checks += 1[0m
[38;2;255;255;255;48;2;119;20;20m-                if pc.get(key) is True or (key == "verify_first_sentence_pattern" and key in pc):[0m
[38;2;255;255;255;48;2;119;20;20m-                    passed += 1[0m
[38;2;255;255;255;48;2;119;20;20m-                else:[0m
[38;2;255;255;255;48;2;119;20;20m-                    errors.append(f"{bp}: precheck.{key} missing or wrong type")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "reject_no_target: true" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'reject_no_target: true'")[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-        checks += 1[0m
[38;2;255;255;255;48;2;119;20;20m-        if "output_validation" not in ev:[0m
[38;2;255;255;255;48;2;119;20;20m-            errors.append(f"{bp}: eval missing 'output_validation' sub-block")[0m
[38;2;255;255;255;48;2;119;20;20m-        else:[0m
[38;2;255;255;255;48;2;119;20;20m-            ov = ev["output_validation"][0m
[38;2;255;255;255;48;2;119;20;20m-            required = ov.get("required_fields", [])[0m
[38;2;255;255;255;48;2;119;20;20m-            checks += 1[0m
[38;2;255;255;255;48;2;119;20;20m-            if set(required) != {"artifactname", "artifactpath", "verdict", "evidence"}:[0m
[38;2;255;255;255;48;2;119;20;20m-                errors.append(f"{bp}: output_validation.required_fields incorrect: {required}")[0m
[38;2;255;255;255;48;2;119;20;20m-            else:[0m
[38;2;255;255;255;48;2;119;20;20m-                passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "reject_meta_commentary: true" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'reject_meta_commentary: true'")[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-    # BLUEPRINT.md checks[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "verify_first_sentence_pattern:" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'verify_first_sentence_pattern'")[0m
[38;2;139;134;130m… omitted 137 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-eval-guardrails-v2.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-eval-guardrails-v2.py[0m
[38;2;139;134;130m@@ -0,0 +1,106 @@[0m
[38;2;255;255;255;48;2;19;87;20m+import os, re, sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+base = r"D:\styde\_alpedal\styde-forge\StydeAgents\blueprints"[0m
[38;2;255;255;255;48;2;19;87;20m+blueprints = ["design-review-critic", "agent-promotion-evaluator"][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+checks = 0[0m
[38;2;255;255;255;48;2;19;87;20m+passed = 0[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for bp in blueprints:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_dir = os.path.join(base, bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg_path = os.path.join(bp_dir, "config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+    if not os.path.exists(cfg_path):[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"MISSING config.yaml for {bp}")[0m
[38;2;255;255;255;48;2;19;87;20m+        continue[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(cfg_path) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        cfg_raw = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "requiretarget: true" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'requiretarget: true'")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "reject_no_target: true" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'reject_no_target: true'")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "reject_meta_commentary: true" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'reject_meta_commentary: true'")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "verify_first_sentence_pattern:" in cfg_raw:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing 'verify_first_sentence_pattern'")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    fields_ok = all(f in cfg_raw for f in ["artifactname", "artifactpath", "verdict", "evidence"])[0m
[38;2;255;255;255;48;2;19;87;20m+    if fields_ok:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: config missing one of required_fields")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_file = os.path.join(bp_dir, "BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(bp_file) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "OUTPUT FORMAT" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: BLUEPRINT missing OUTPUT FORMAT")[0m
[38;2;255;255;255;48;2;19;87;20m+    for field in ["artifactname:", "artifactpath:", "verdict:", "evidence:"]:[0m
[38;2;255;255;255;48;2;19;87;20m+        checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        if field in content:[0m
[38;2;255;255;255;48;2;19;87;20m+            passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        else:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"{bp}: BLUEPRINT missing field '{field}'")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "First sentence MUST name" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: BLUEPRINT missing first-sentence rule")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "compliance failure" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: BLUEPRINT missing execution-after-prescription rule")[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if "NO meta-commentary" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"{bp}: BLUEPRINT missing meta-commentary ban")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    persona_file = os.path.join(bp_dir, "persona.md")[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(persona_file) as f:[0m
[38;2;139;134;130m… omitted 28 diff line(s) across 1 additional file(s)/section(s)[0m
AD-HOC VERIFICATION: 38/38 checks passed (100.0%)
All guardrails verified across both blueprints — config.yaml requiretarget+precheck+output_validation blocks, BLUEPRINT.md OUTPUT FORMAT template with all 4 mandatory fields, persona.md REQUIRED PRECHECK with all 4 verification steps and penalty clause. Temp script cleaned up.