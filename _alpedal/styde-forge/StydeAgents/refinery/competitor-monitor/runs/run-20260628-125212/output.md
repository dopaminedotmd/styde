┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\competitor-monitor\BLUEPRINT.md → b/StydeAgents\blueprints\competitor-monitor\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,3 +13,18 @@[0m
[38;2;184;134;11m - Filter: signal from noise — what actually matters[0m
[38;2;184;134;11m - Report: weekly brief with top 5 changes and implications[0m
[38;2;184;134;11m - Track: trends over time, not just point-in-time snapshots[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Source Integrity[0m
[38;2;255;255;255;48;2;19;87;20m+Every quantitative claim (dates, prices, metrics, percentages, financial figures) MUST be explicitly attributed to a source file or market report. Inline citation markers required before any numeric claim. Cross-check all citations against source material before final output. Claims without a verifiable source reference MUST be excluded. Format: [Claim] (Source: [filename/path], line [line-number]).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Fresh Evidence Gate[0m
[38;2;255;255;255;48;2;19;87;20m+Each claimed significant change MUST cite at least one source timestamped within the current monitoring window. Sources older than the current window are inadmissible as primary evidence for a new change. If every candidate change depends exclusively on sources outside the window, exclude those changes from the brief.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Zero-Changes Escalation[0m
[38;2;255;255;255;48;2;19;87;20m+If zero independently sourced, in-window changes are found after full research, do NOT carry forward old data. Output a 'No verifiable changes this cycle' brief. State the date range searched, the sources checked, and why no changes qualified. Escalate to human review immediately with the research log attached.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Completion Threshold[0m
[38;2;255;255;255;48;2;19;87;20m+A task is not complete unless concrete artifacts have been produced: files written, outputs generated, or side-effects executed. Flagging underspecification or requesting clarification without delivering work is a failure mode. The brief artifact must exist on disk before the task is considered done.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Bias to Action[0m
[38;2;255;255;255;48;2;19;87;20m+When a task is underspecified, make one reasonable assumption per ambiguity, proceed with execution immediately, and note the assumption as a comment in the output. Do not request clarification from the user. Self-correct from self-eval feedback if the assumption proves wrong.[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\competitor-monitor\config.yaml → b/StydeAgents\blueprints\competitor-monitor\config.yaml[0m
[38;2;139;134;130m@@ -82,7 +82,22 @@[0m
[38;2;184;134;11m   - terminal[0m
[38;2;184;134;11m   - file[0m
[38;2;184;134;11m   - web[0m
[38;2;255;255;255;48;2;19;87;20m+  max_clarification_rounds: 0[0m
[38;2;184;134;11m eval:[0m
[38;2;184;134;11m   benchmarks: [][0m
[38;2;184;134;11m   judge_model: deepseek-v4-pro[0m
[38;2;184;134;11m   min_pass_score: 70[0m
[38;2;255;255;255;48;2;19;87;20m+  source_citation_validator:[0m
[38;2;255;255;255;48;2;19;87;20m+    enabled: true[0m
[38;2;255;255;255;48;2;19;87;20m+    scan_for_unquoted_numeric: true[0m
[38;2;255;255;255;48;2;19;87;20m+    citation_marker_pattern: '\(Source:'[0m
[38;2;255;255;255;48;2;19;87;20m+    fail_on_missing_citation: true[0m
[38;2;255;255;255;48;2;19;87;20m+    check_types:[0m
[38;2;255;255;255;48;2;19;87;20m+    - dates[0m
[38;2;255;255;255;48;2;19;87;20m+    - prices[0m
[38;2;255;255;255;48;2;19;87;20m+    - percentages[0m
[38;2;255;255;255;48;2;19;87;20m+    - financial_figures[0m
[38;2;255;255;255;48;2;19;87;20m+    - metrics[0m
[38;2;255;255;255;48;2;19;87;20m+    min_sources_per_claim: 3[0m
[38;2;255;255;255;48;2;19;87;20m+    require_verifiable_timestamps: true[0m
[38;2;255;255;255;48;2;19;87;20m+    output_report_path: source-citation-report.txt[0m
  ┊ review diff
[38;2;218;165;32ma/skills\competitive-brief-generation\SKILL.md → b/skills\competitive-brief-generation\SKILL.md[0m
[38;2;139;134;130m@@ -0,0 +1,35 @@[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+name: competitive-brief-generation[0m
[38;2;255;255;255;48;2;19;87;20m+description: >[0m
[38;2;255;255;255;48;2;19;87;20m+  Generates competitive briefs with rigorous source attribution. Every claim[0m
[38;2;255;255;255;48;2;19;87;20m+  must be paired with its provenance and a confidence score. Rejects unsourced[0m
[38;2;255;255;255;48;2;19;87;20m+  assertions. Produces weekly briefs in a structured Claim | Source | Confidence[0m
[38;2;255;255;255;48;2;19;87;20m+  format that enables rapid verification.[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Structure[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Every competitive brief MUST use this three-column format for each change:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+| Claim | Source | Confidence |[0m
[38;2;255;255;255;48;2;19;87;20m+|-------|--------|------------|[0m
[38;2;255;255;255;48;2;19;87;20m+| [What changed, including quantitative data] | [File path, URL, report ID, line number] | [0-100 based on source reliability + recency] |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Rules[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+- Every row in the brief must have all three columns populated. No empty cells.[0m
[38;2;255;255;255;48;2;19;87;20m+- Quantitative values (dates, prices, percentages, counts) must appear inside the Claim column only if the Source column references a verifiable document.[0m
[38;2;255;255;255;48;2;19;87;20m+- Confidence scoring: 90-100 = primary source within 24h; 70-89 = primary source within monitoring window; 50-69 = secondary source with corroboration; below 50 = exclude from brief.[0m
[38;2;255;255;255;48;2;19;87;20m+- If a claim cannot be sourced, exclude it. Do not insert placeholder sources.[0m
[38;2;255;255;255;48;2;19;87;20m+- At least 3 independent sources per claimed change, each with verifiable timestamps.[0m
[38;2;255;255;255;48;2;19;87;20m+- Each claimed change must have at least one source timestamped within the current monitoring window (fresh evidence gate).[0m
[38;2;255;255;255;48;2;19;87;20m+- After generation, scan the brief for any numeric values not preceded by an inline citation marker. Flag and fix before finalizing.[0m
[38;2;255;255;255;48;2;19;87;20m+- If zero independently sourced changes survive validation, output: 'No verifiable changes this cycle — escalated to human review'. Attach the research log.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Validation Steps[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+1. For each claim, trace the Source to the actual document. Verify the data matches.[0m
[38;2;255;255;255;48;2;19;87;20m+2. Check every Source timestamp is within the current monitoring window.[0m
[38;2;255;255;255;48;2;19;87;20m+3. For each quantitative value in Claim, confirm there is a preceding citation marker referencing the Source.[0m
[38;2;255;255;255;48;2;19;87;20m+4. Count independent sources per claim. Reject claims with fewer than 3.[0m
[38;2;255;255;255;48;2;19;87;20m+5. If the brief would be empty after validation, switch to zero-changes escalation.[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py[0m
[38;2;139;134;130m@@ -0,0 +1,91 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: checks BLUEPRINT.md sections, config.yaml keys, and skill template structure."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, re, sys, tempfile[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = r"E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\competitor-monitor\BLUEPRINT.md"[0m
[38;2;255;255;255;48;2;19;87;20m+cfg_path = r"E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\competitor-monitor\config.yaml"[0m
[38;2;255;255;255;48;2;19;87;20m+sk_path = r"E:\Stryde\_alpedal\styde-forge\skills\competitive-brief-generation\SKILL.md"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. BLUEPRINT.md — check all 5 new sections exist[0m
[38;2;255;255;255;48;2;19;87;20m+if os.path.exists(bp_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = open(bp_path).read()[0m
[38;2;255;255;255;48;2;19;87;20m+    sections = [[0m
[38;2;255;255;255;48;2;19;87;20m+        "## Source Integrity",[0m
[38;2;255;255;255;48;2;19;87;20m+        "## Fresh Evidence Gate",[0m
[38;2;255;255;255;48;2;19;87;20m+        "## Zero-Changes Escalation",[0m
[38;2;255;255;255;48;2;19;87;20m+        "## Completion Threshold",[0m
[38;2;255;255;255;48;2;19;87;20m+        "## Bias to Action",[0m
[38;2;255;255;255;48;2;19;87;20m+    ][0m
[38;2;255;255;255;48;2;19;87;20m+    for s in sections:[0m
[38;2;255;255;255;48;2;19;87;20m+        if s not in bp:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"MISSING section in BLUEPRINT.md: {s}")[0m
[38;2;255;255;255;48;2;19;87;20m+    # Check key directives[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = {[0m
[38;2;255;255;255;48;2;19;87;20m+        "inline citation": "inline citation marker" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "cross-check step": "Cross-check all citations" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "timestamped source": "timestamped within the current monitoring window" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "no carry forward old data": "carry forward old data" not in bp and "do NOT carry forward" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "zero-changes brief text": "No verifiable changes this cycle" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "escalate to human review": "human review" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "concrete artifacts": "concrete artifacts" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "bias to action directive": "make one reasonable assumption per ambiguity" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    for label, passed in checks.items():[0m
[38;2;255;255;255;48;2;19;87;20m+        if not passed:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT.md missing directive: {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  BLUEPRINT.md: {len(sections)}/5 sections present, {sum(checks.values())}/{len(checks)} directives OK")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING file: {bp_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. config.yaml — check new keys[0m
[38;2;255;255;255;48;2;19;87;20m+if os.path.exists(cfg_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg = yaml.safe_load(open(cfg_path))[0m
[38;2;255;255;255;48;2;19;87;20m+    agent = cfg.get("agent", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    if agent.get("max_clarification_rounds") != 0:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"config.yaml agent.max_clarification_rounds should be 0, got {agent.get('max_clarification_rounds')}")[0m
[38;2;255;255;255;48;2;19;87;20m+    validator = cfg.get("eval", {}).get("source_citation_validator", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    if not validator.get("enabled"):[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append("config.yaml source_citation_validator.enabled should be true")[0m
[38;2;255;255;255;48;2;19;87;20m+    if validator.get("min_sources_per_claim") != 3:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"config.yaml min_sources_per_claim should be 3, got {validator.get('min_sources_per_claim')}")[0m
[38;2;255;255;255;48;2;19;87;20m+    if not validator.get("require_verifiable_timestamps"):[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append("config.yaml require_verifiable_timestamps should be true")[0m
[38;2;255;255;255;48;2;19;87;20m+    if not validator.get("scan_for_unquoted_numeric"):[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append("config.yaml scan_for_unquoted_numeric should be true")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  config.yaml: max_clarification_rounds={agent.get('max_clarification_rounds')}, "[0m
[38;2;255;255;255;48;2;19;87;20m+          f"validator_enabled={validator.get('enabled')}, min_sources={validator.get('min_sources_per_claim')}, "[0m
[38;2;255;255;255;48;2;19;87;20m+          f"timestamps={validator.get('require_verifiable_timestamps')}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"MISSING file: {cfg_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. SKILL.md — check three-column structure[0m
[38;2;255;255;255;48;2;19;87;20m+if os.path.exists(sk_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    sk = open(sk_path).read()[0m
[38;2;255;255;255;48;2;19;87;20m+    skill_checks = {[0m
[38;2;255;255;255;48;2;19;87;20m+        "name frontmatter": "name: competitive-brief-generation" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "description frontmatter": "description:" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "claim column": "Claim" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "source column": "Source" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "confidence column": "Confidence" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "three-column table": "| Claim | Source | Confidence |" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "fresh evidence gate ref": "fresh evidence gate" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "zero-changes escalation": "No verifiable changes" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "validation steps section": "## Validation Steps" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+        "min 3 sources": "3 independent sources" in sk,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    for label, passed in skill_checks.items():[0m
[38;2;139;134;130m… omitted 13 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py[0m
[38;2;139;134;130m@@ -22,12 +22,12 @@[0m
[38;2;184;134;11m             errors.append(f"MISSING section in BLUEPRINT.md: {s}")[0m
[38;2;184;134;11m     # Check key directives[0m
[38;2;184;134;11m     checks = {[0m
[38;2;255;255;255;48;2;119;20;20m-        "inline citation": "inline citation marker" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "inline citation markers": "inline citation marker" in bp,[0m
[38;2;184;134;11m         "cross-check step": "Cross-check all citations" in bp,[0m
[38;2;184;134;11m         "timestamped source": "timestamped within the current monitoring window" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "no carry forward old data": "carry forward old data" not in bp and "do NOT carry forward" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "do NOT carry forward": "do NOT carry forward" in bp,[0m
[38;2;184;134;11m         "zero-changes brief text": "No verifiable changes this cycle" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "escalate to human review": "human review" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "escalate to human review": "escalate to human review" in bp,[0m
[38;2;184;134;11m         "concrete artifacts": "concrete artifacts" in bp,[0m
[38;2;184;134;11m         "bias to action directive": "make one reasonable assumption per ambiguity" in bp,[0m
[38;2;184;134;11m     }[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-changes.py[0m
[38;2;139;134;130m@@ -21,15 +21,16 @@[0m
[38;2;184;134;11m         if s not in bp:[0m
[38;2;184;134;11m             errors.append(f"MISSING section in BLUEPRINT.md: {s}")[0m
[38;2;184;134;11m     # Check key directives[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_lower = bp.lower()[0m
[38;2;184;134;11m     checks = {[0m
[38;2;255;255;255;48;2;119;20;20m-        "inline citation markers": "inline citation marker" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "cross-check step": "Cross-check all citations" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "timestamped source": "timestamped within the current monitoring window" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "do NOT carry forward": "do NOT carry forward" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "zero-changes brief text": "No verifiable changes this cycle" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "escalate to human review": "escalate to human review" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "concrete artifacts": "concrete artifacts" in bp,[0m
[38;2;255;255;255;48;2;119;20;20m-        "bias to action directive": "make one reasonable assumption per ambiguity" in bp,[0m
[38;2;255;255;255;48;2;19;87;20m+        "inline citation markers": "inline citation marker" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "cross-check step": "cross-check all citations" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "timestamped source": "timestamped within the current monitoring window" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "do NOT carry forward": "do not carry forward" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "zero-changes brief text": "no verifiable changes this cycle" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "escalate to human review": "escalate to human review" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "concrete artifacts": "concrete artifacts" in bp_lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "bias to action directive": "make one reasonable assumption per ambiguity" in bp_lower,[0m
[38;2;184;134;11m     }[0m
[38;2;184;134;11m     for label, passed in checks.items():[0m
[38;2;184;134;11m         if not passed:[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-all.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-all.py[0m
[38;2;139;134;130m@@ -0,0 +1,82 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: BLUEPRINT.md sections, config.yaml keys, skill template structure."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+base = r"E:\Stryde\_alpedal\styde-forge"[0m
[38;2;255;255;255;48;2;19;87;20m+bp = os.path.join(base, r"StydeAgents\blueprints\competitor-monitor\BLUEPRINT.md")[0m
[38;2;255;255;255;48;2;19;87;20m+cfg = os.path.join(base, r"StydeAgents\blueprints\competitor-monitor\config.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+sk  = os.path.join(base, r"skills\competitive-brief-generation\SKILL.md")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md ---[0m
[38;2;255;255;255;48;2;19;87;20m+if os.path.exists(bp):[0m
[38;2;255;255;255;48;2;19;87;20m+    text = open(bp).read()[0m
[38;2;255;255;255;48;2;19;87;20m+    lower = text.lower()[0m
[38;2;255;255;255;48;2;19;87;20m+    sections = ["## Source Integrity","## Fresh Evidence Gate","## Zero-Changes Escalation","## Completion Threshold","## Bias to Action"][0m
[38;2;255;255;255;48;2;19;87;20m+    for s in sections:[0m
[38;2;255;255;255;48;2;19;87;20m+        if s not in text:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT: missing section {s}")[0m
[38;2;255;255;255;48;2;19;87;20m+    directives = {[0m
[38;2;255;255;255;48;2;19;87;20m+        "inline citation marker": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "cross-check all citations": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "timestamped within the current monitoring window": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "do not carry forward": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "no verifiable changes this cycle": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "escalate to human review": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "concrete artifacts": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+        "make one reasonable assumption per ambiguity": lower,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    for d, src in directives.items():[0m
[38;2;255;255;255;48;2;19;87;20m+        if d not in src:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"BLUEPRINT: missing directive '{d}'")[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_ok = f"{len(sections)}/5 sections, {len(directives)}/8 directives"[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("BLUEPRINT.md not found")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- config.yaml ---[0m
[38;2;255;255;255;48;2;19;87;20m+if os.path.exists(cfg):[0m
[38;2;255;255;255;48;2;19;87;20m+    import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+    c = yaml.safe_load(open(cfg))[0m
[38;2;255;255;255;48;2;19;87;20m+    a = c.get("agent", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    if a.get("max_clarification_rounds") != 0:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append("CFG: max_clarification_rounds != 0")[0m
[38;2;255;255;255;48;2;19;87;20m+    v = c.get("eval", {}).get("source_citation_validator", {})[0m
[38;2;255;255;255;48;2;19;87;20m+    if not v.get("enabled"):       errors.append("CFG: validator not enabled")[0m
[38;2;255;255;255;48;2;19;87;20m+    if v.get("min_sources_per_claim") != 3: errors.append("CFG: min_sources_per_claim != 3")[0m
[38;2;255;255;255;48;2;19;87;20m+    if not v.get("require_verifiable_timestamps"): errors.append("CFG: timestamps not required")[0m
[38;2;255;255;255;48;2;19;87;20m+    if not v.get("scan_for_unquoted_numeric"): errors.append("CFG: numeric scan disabled")[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg_ok = f"clarify_rounds={a.get('max_clarification_rounds')}, min_src={v.get('min_sources_per_claim')}, ts={v.get('require_verifiable_timestamps')}"[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("config.yaml not found")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- SKILL.md ---[0m
[38;2;255;255;255;48;2;19;87;20m+if os.path.exists(sk):[0m
[38;2;255;255;255;48;2;19;87;20m+    skt = open(sk).read()[0m
[38;2;255;255;255;48;2;19;87;20m+    skl = skt.lower()[0m
[38;2;255;255;255;48;2;19;87;20m+    checks = {[0m
[38;2;255;255;255;48;2;19;87;20m+        "name: competitive-brief-generation": skt,[0m
[38;2;255;255;255;48;2;19;87;20m+        "three-column table": "| claim | source | confidence |" in skl,[0m
[38;2;255;255;255;48;2;19;87;20m+        "fresh evidence gate ref": "fresh evidence gate" in skl,[0m
[38;2;255;255;255;48;2;19;87;20m+        "zero-changes escalation": "no verifiable changes" in skl,[0m
[38;2;255;255;255;48;2;19;87;20m+        "validation steps section": "## validation steps" in skl,[0m
[38;2;255;255;255;48;2;19;87;20m+        "min 3 sources": "3 independent sources" in skl,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    for lbl, ok in checks.items():[0m
[38;2;255;255;255;48;2;19;87;20m+        if isinstance(ok, str):[0m
[38;2;255;255;255;48;2;19;87;20m+            if lbl not in ok: errors.append(f"SKILL: missing '{lbl}'")[0m
[38;2;255;255;255;48;2;19;87;20m+        elif not ok:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"SKILL: missing {lbl}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sk_ok = f"{sum(1 for v in checks.values() if v)}/{len(checks)} checks"[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("SKILL.md not found")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- result ---[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  BLUEPRINT.md: {bp_ok}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  config.yaml:  {cfg_ok}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  SKILL.md:     {sk_ok}")[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;139;134;130m… omitted 4 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification complete. 3 files, 19 checks, all passed. Temp script cleaned.