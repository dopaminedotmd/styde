┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\ab-testing-statistician\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\ab-testing-statistician\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,6 +13,14 @@[0m
[38;2;184;134;11m - Sequential: implement sequential testing with correction[0m
[38;2;184;134;11m - Bayesian: use Bayesian A/B testing approaches[0m
[38;2;184;134;11m - Causal: apply causal inference methods (DID, IV)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Missing Input Handling[0m
[38;2;255;255;255;48;2;19;87;20m+When required input data is absent or incomplete, the agent MUST:[0m
[38;2;255;255;255;48;2;19;87;20m+1. Attempt recovery: propose concrete options (paste snippet, provide file path, describe expected format)[0m
[38;2;255;255;255;48;2;19;87;20m+2. After 2 recovery attempts, produce the best partial analysis possible using what IS available[0m
[38;2;255;255;255;48;2;19;87;20m+3. Annotate gaps with clear caveats: "Effect size not provided — showing formula n = (Z_alpha/2 + Z_beta)^2 * 2 * sigma^2 / delta^2 with delta as placeholder"[0m
[38;2;255;255;255;48;2;19;87;20m+4. Never output bare [MISSING] tags or empty sections[0m
[38;2;255;255;255;48;2;19;87;20m+5. Never ask the user for more information — that is the caller's job. The agent is a machine that returns structured analysis regardless of input completeness[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Methodology Lock[0m
[38;2;184;134;11m Before any analysis, the agent MUST:[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\ab-testing-statistician\persona.md → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\ab-testing-statistician\persona.md[0m
[38;2;139;134;130m@@ -9,3 +9,4 @@[0m
[38;2;184;134;11m   Arithmetic visibility: When calculating sample sizes, power, or any numeric artifact, first emit the formula with the substituted values, then evaluate it — never output the final number without showing the arithmetic[0m
[38;2;184;134;11m   CI decomposition: When computing confidence intervals, margin of error, or any derived statistic, decompose into atomic steps and state the formula before plugging values. Do not skip the intermediate MoE calculation[0m
[38;2;184;134;11m   Source verification: Before submitting any technical output, verify all formulas against authoritative sources (textbook, peer-reviewed paper, or known statistical software implementation). If uncertain about a formula, state the uncertainty rather than guessing[0m
[38;2;255;255;255;48;2;19;87;20m+  Missing input recovery: When data needed for analysis is absent, always attempt recovery — ask for it, infer it, or produce a partial deliverable with a clear caveat. Never output bare [MISSING] tags or empty sections. You are a machine that returns structured analysis. When input is incomplete, produce a partial analysis with annotated placeholders and explain what data would fill them. Never ask the user for more information — that is the caller's job.[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\ab-testing-statistician\config.yaml → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\ab-testing-statistician\config.yaml[0m
[38;2;139;134;130m@@ -176,6 +176,9 @@[0m
[38;2;184;134;11m     check: scan output for 'TODO', 'future work', 'this section is incomplete', or[0m
[38;2;184;134;11m       similar placeholders — reject if any found[0m
[38;2;184;134;11m     fail_action: reject[0m
[38;2;255;255;255;48;2;19;87;20m+missing_input:[0m
[38;2;255;255;255;48;2;19;87;20m+  max_retry_on_missing_input: 2[0m
[38;2;255;255;255;48;2;19;87;20m+  best_effort_completion: true[0m
[38;2;184;134;11m hardware_profiles:[0m
[38;2;184;134;11m   pontus-main:[0m
[38;2;184;134;11m     eval_model: deepseek-v4-pro[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-abtest-missing-input.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-abtest-missing-input.py[0m
[38;2;139;134;130m@@ -0,0 +1,67 @@[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml, sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. config.yaml[0m
[38;2;255;255;255;48;2;19;87;20m+path = 'E:/Stryde/_alpedal/styde-forge/StydeAgents/blueprints/ab-testing-statistician/config.yaml'[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(path) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    mi = cfg.get('missing_input', {})[0m
[38;2;255;255;255;48;2;19;87;20m+    if mi.get('max_retry_on_missing_input') != 2:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append('FAIL: config.yaml max_retry_on_missing_input != 2')[0m
[38;2;255;255;255;48;2;19;87;20m+    if mi.get('best_effort_completion') != True:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append('FAIL: config.yaml best_effort_completion != true')[0m
[38;2;255;255;255;48;2;19;87;20m+    hooks = cfg['pre_deployment']['validation_hooks'][0m
[38;2;255;255;255;48;2;19;87;20m+    hook_names = [h['name'] for h in hooks][0m
[38;2;255;255;255;48;2;19;87;20m+    for h in ['formula_sanity', 'method_disambiguation', 'no_todo_in_output']:[0m
[38;2;255;255;255;48;2;19;87;20m+        if h not in hook_names:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f'FAIL: pre-deployment hook {h} missing')[0m
[38;2;255;255;255;48;2;19;87;20m+    if not errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print('PASS: config.yaml')[0m
[38;2;255;255;255;48;2;19;87;20m+except Exception as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f'FAIL: config.yaml parse error: {e}')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. BLUEPRINT.md[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = open('E:/Stryde/_alpedal/styde-forge/StydeAgents/blueprints/ab-testing-statistician/BLUEPRINT.md').read()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = {[0m
[38;2;255;255;255;48;2;19;87;20m+        'section Missing Input Handling': '## Missing Input Handling' in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        'recovery options': 'Attempt recovery' in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        'partial analysis fallback': 'best partial analysis' in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        'no bare MISSING tags': 'Never output bare [MISSING]' in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        'no asking user': 'Never ask the user' in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        'caller job mention': 'caller' in bp and 'job' in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    for name, ok in checks.items():[0m
[38;2;255;255;255;48;2;19;87;20m+        if not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f'FAIL: BLUEPRINT.md missing "{name}"')[0m
[38;2;255;255;255;48;2;19;87;20m+    if all(checks.values()):[0m
[38;2;255;255;255;48;2;19;87;20m+        print('PASS: BLUEPRINT.md')[0m
[38;2;255;255;255;48;2;19;87;20m+except Exception as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f'FAIL: BLUEPRINT.md read error: {e}')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. persona.md[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    pm = open('E:/Stryde/_alpedal/styde-forge/StydeAgents/blueprints/ab-testing-statistician/persona.md').read()[0m
[38;2;255;255;255;48;2;19;87;20m+    pchecks = {[0m
[38;2;255;255;255;48;2;19;87;20m+        'recovery rule': 'Missing input recovery' in pm,[0m
[38;2;255;255;255;48;2;19;87;20m+        'no bare MISSING': 'Never output bare [MISSING]' in pm,[0m
[38;2;255;255;255;48;2;19;87;20m+        'no asking user': 'Never ask the user' in pm,[0m
[38;2;255;255;255;48;2;19;87;20m+        'machine returns analysis': 'machine that returns structured analysis' in pm,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    for name, ok in pchecks.items():[0m
[38;2;255;255;255;48;2;19;87;20m+        if not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f'FAIL: persona.md missing "{name}"')[0m
[38;2;255;255;255;48;2;19;87;20m+    if all(pchecks.values()):[0m
[38;2;255;255;255;48;2;19;87;20m+        print('PASS: persona.md')[0m
[38;2;255;255;255;48;2;19;87;20m+except Exception as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f'FAIL: persona.md read error: {e}')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(e)[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print()[0m
[38;2;255;255;255;48;2;19;87;20m+    print('Ad-hoc verification: ALL PASS')[0m
Ad-hoc verification complete. Script skriven till `C:\Users\jonat\AppData\Local\temp\hermes-verify-abtest-missing-input.py`, kördes, städades bort.
3 PASS, 0 FAIL:
- config.yaml: missing_input-sektion valid, pre-deployment hooks intakta
- BLUEPRINT.md: Missing Input Handling-sektion med recovery, partial fallback, inga [MISSING]-taggar, caller-responsibility
- persona.md: Missing input recovery-rule med samma constraint-set