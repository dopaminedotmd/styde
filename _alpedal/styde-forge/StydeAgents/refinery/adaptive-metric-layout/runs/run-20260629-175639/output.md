┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -16,6 +16,26 @@[0m
[38;2;184;134;11m - Persist: save layout preferences to localStorage and restore on return[0m
[38;2;184;134;11m - Output: interactive HTML dashboard with adaptive layout engine + usage tracking + manual override[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+## Structure & Comments[0m
[38;2;255;255;255;48;2;19;87;20m+- Template-based HTML generation: all DOM construction MUST use JavaScript template literals or dedicated helper functions (createPanel(), renderGrid(), buildCompactPreview()). No raw innerHTML string interpolation.[0m
[38;2;255;255;255;48;2;19;87;20m+- Docstring-style comments: every major function block (panel scoring, grid arrangement, tracking handlers, render pipeline) MUST have a JSDoc comment describing inputs, outputs, and side effects.[0m
[38;2;255;255;255;48;2;19;87;20m+- Example:[0m
[38;2;255;255;255;48;2;19;87;20m+  /**[0m
[38;2;255;255;255;48;2;19;87;20m+   * Score a panel by composite attention metric.[0m
[38;2;255;255;255;48;2;19;87;20m+   * @param {PanelData} panel - The panel to score[0m
[38;2;255;255;255;48;2;19;87;20m+   * @param {TrackingState} state - Current tracking state[0m
[38;2;255;255;255;48;2;19;87;20m+   * @returns {number} Composite score (higher = more important)[0m
[38;2;255;255;255;48;2;19;87;20m+   */[0m
[38;2;255;255;255;48;2;19;87;20m+  function scorePanel(panel, state) { ... }[0m
[38;2;255;255;255;48;2;19;87;20m+- Section markers: group related functions under banner comments (/* === TRACKING ENGINE === */) for readability.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Performance Constraints[0m
[38;2;255;255;255;48;2;19;87;20m+- Per-frame cost: every interaction handler (click, scroll, resize) MUST be O(n) or better. No nested loops over panel arrays inside event handlers.[0m
[38;2;255;255;255;48;2;19;87;20m+- Memoization/caching: rank scores, grid positions, and compact-zone boundaries MUST be cached and recomputed only when tracking data changes (dirty flag pattern). Accessing a panel's score is O(1) lookup, never O(n) scan.[0m
[38;2;255;255;255;48;2;19;87;20m+- Batched render cycles: all DOM mutations in a single arrange pass MUST be batched via requestAnimationFrame or a microtask queue. Multiple panel moves in one cycle = one layout recalculation + one paint.[0m
[38;2;255;255;255;48;2;19;87;20m+- Score clamp floor: after computing adaptive scores, normalize top-N visible panels to a minimum floor using clamp(durScore, 3, 10) to prevent briefly-viewed panels from dropping to near-zero before they accumulate interaction data.[0m
[38;2;255;255;255;48;2;19;87;20m+- Hot-path profiling: before submitting, identify the hottest code path (typically the arrange/render cycle), document its big-O cost in a comment, and verify no inner loop exceeds O(n).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;184;134;11m ## Constraints / Quality Gates[0m
[38;2;184;134;11m ### Efficiency[0m
[38;2;184;134;11m - Targeted DOM updates only: never re-render the full grid wrapper when one panel moves; mutate individual panel elements (position, size, class) via direct property assignment or classList changes[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout\persona.md → b/E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout\persona.md[0m
[38;2;139;134;130m@@ -8,4 +8,7 @@[0m
[38;2;184;134;11m - Override: allow manual panel lock and position override that takes priority over auto-layout[0m
[38;2;184;134;11m - Persist: save layout preferences to localStorage and restore on return[0m
[38;2;184;134;11m - Output: interactive HTML dashboard with adaptive layout engine + usage tracking + manual override[0m
[38;2;255;255;255;48;2;19;87;20m+- Visible context: always place a visible title, rubric header, or context summary above the fold so the user immediately understands what they are looking at. No dashboard renders without an H1 or equivalent header in the initial viewport.[0m
[38;2;255;255;255;48;2;19;87;20m+- Score floor: after computing adaptive scores, normalize the top-N visible panels to a minimum score floor using clamp(durScore, 3, 10) to prevent briefly-viewed panels from dropping to near-zero before they accumulate interaction data.[0m
[38;2;255;255;255;48;2;19;87;20m+- Profile before submit: before submitting, profile one hot path and document its big-O cost in a JSDoc comment. If any inner loop is O(n²), refactor to O(n) or prove it cannot be avoided. The arrange/render cycle is the default candidate for profiling.[0m
[38;2;184;134;11m - Efficiency: for every feature, implement the cheapest possible DOM update — never re-render the whole grid when one panel moves; mutate only the changed elements via direct property assignment[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout\config.yaml → b/E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout\config.yaml[0m
[38;2;139;134;130m@@ -17,6 +17,10 @@[0m
[38;2;184;134;11m   version_history: [][0m
[38;2;184;134;11m eval:[0m
[38;2;184;134;11m   benchmarks: [][0m
[38;2;255;255;255;48;2;19;87;20m+  dimensions:[0m
[38;2;255;255;255;48;2;19;87;20m+    optimisation:[0m
[38;2;255;255;255;48;2;19;87;20m+      description: "Computational efficiency: O(n) per-frame, memoized derived state, no O(n²) inner loops"[0m
[38;2;255;255;255;48;2;19;87;20m+      weight: 70[0m
[38;2;184;134;11m   judge_model: deepseek-v4-pro[0m
[38;2;184;134;11m   min_pass_score: 70[0m
[38;2;184;134;11m hardware_profiles:[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-adaptive-blueprint.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-adaptive-blueprint.py[0m
[38;2;139;134;130m@@ -0,0 +1,46 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Verify Teacher Feedback changes applied to adaptive-metric-layout blueprint."""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml, sys, os[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+base = r"E:\Stryde\_alpedal\styde-forge\checkpoints\checkpoint-20260627-224414-parallel-loop-2bp\blueprints\adaptive-metric-layout"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. config.yaml: parse + check optimisation dimension[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(os.path.join(base, "config.yaml")) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+    dims = cfg.get("eval", {}).get("dimensions", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    assert "optimisation" in dims, "missing optimisation dimension"[0m
[38;2;255;255;255;48;2;19;87;20m+    assert dims["optimisation"]["weight"] == 70, f"weight should be 70, got {dims['optimisation']['weight']}"[0m
[38;2;255;255;255;48;2;19;87;20m+    print("PASS config.yaml: optimisation dimension present, weight=70")[0m
[38;2;255;255;255;48;2;19;87;20m+except Exception as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"config.yaml: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. BLUEPRINT.md: check new sections[0m
[38;2;255;255;255;48;2;19;87;20m+with open(os.path.join(base, "BLUEPRINT.md")) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+for section in ["Structure & Comments", "Performance Constraints", "Template-based HTML generation",[0m
[38;2;255;255;255;48;2;19;87;20m+                "docstring-style", "O(n)", "memoization/caching", "Batched render",[0m
[38;2;255;255;255;48;2;19;87;20m+                "Score clamp floor", "Hot-path profiling"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if section.lower() not in bp.lower():[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"BLUEPRINT.md: missing '{section}'")[0m
[38;2;255;255;255;48;2;19;87;20m+if not errors or all("BLUEPRINT" not in e for e in errors):[0m
[38;2;255;255;255;48;2;19;87;20m+    print("PASS BLUEPRINT.md: all required sections present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. persona.md: check new rules[0m
[38;2;255;255;255;48;2;19;87;20m+with open(os.path.join(base, "persona.md")) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    pm = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+for rule in ["Visible context", "Score floor", "Profile before submit", "clamp(durScore, 3, 10)",[0m
[38;2;255;255;255;48;2;19;87;20m+             "big-O cost", "O(n²)"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if rule.lower() not in pm.lower():[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"persona.md: missing '{rule}'")[0m
[38;2;255;255;255;48;2;19;87;20m+if not errors or all("persona" not in e for e in errors):[0m
[38;2;255;255;255;48;2;19;87;20m+    print("PASS persona.md: all required rules present")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"\nFAIL: {len(errors)} error(s):")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  - {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("\nALL CHECKS PASSED — 3 files verified")[0m
Ad-hoc verifikation godkand: YAML parse + strukturella sökningar pa alla 3 filer.
Verifikationsscript: C:\Users\jonat\AppData\Local\Temp\hermes-verify-adaptive-blueprint.py (kort, raderad efter pass)
Resultat:
  config.yaml  — optimiseringsdimension med weight=70 narvarande
  BLUEPRINT.md — Structure & Comments + Performance Constraints bada sektioner verifierade
  persona.md  — Visible context, Score floor, Profile before submit samtliga narvarande
Inga fel. Alla 6 Teacher Feedback-andringar applicerade och bekraftade.