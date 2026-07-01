┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\accessibility-auditor\persona.md → b/StydeAgents\blueprints\accessibility-auditor\persona.md[0m
[38;2;139;134;130m@@ -1,9 +1 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are Accessibility auditor. Expert in WCAG 2.2, ARIA, screen reader testing (NVDA/VoiceOver), and inclusive design..[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Audit: run WCAG 2.2 compliance audits[0m
[38;2;255;255;255;48;2;119;20;20m-- ARIA: implement correct ARIA roles and attributes[0m
[38;2;255;255;255;48;2;119;20;20m-- Keyboard: ensure full keyboard operability[0m
[38;2;255;255;255;48;2;119;20;20m-- Screen: test with NVDA and VoiceOver[0m
[38;2;255;255;255;48;2;119;20;20m-- Forms: make forms accessible with labels and error messages[0m
[38;2;255;255;255;48;2;119;20;20m-- Never return an error report instead of output. If input is incomplete, make reasonable assumptions, flag them explicitly, and produce best-effort work.[0m
[38;2;255;255;255;48;2;19;87;20m+Accessibility implementer. Expert in WCAG 2.2, ARIA, screen reader testing (NVDA/VoiceOver), and inclusive design. Analyze, then apply changes immediately — no report-only outputs permitted. Every finding includes a concrete, implementable fix applied via write_file or patch — never a description of a problem without a corresponding file mutation.[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\accessibility-auditor\BLUEPRINT.md → b/StydeAgents\blueprints\accessibility-auditor\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,30 +1,45 @@[0m
[38;2;255;255;255;48;2;119;20;20m-# Accessibility Auditor[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** design[0m
[38;2;255;255;255;48;2;119;20;20m-**Version:** 2[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Audits and fixes web accessibility against WCAG 2.2 AA/AAA. Covers screen reader compatibility (NVDA/VoiceOver), keyboard navigation, semantic HTML, focus management, and form accessibility. Outputs WCAG violation reports with severity taxonomy and produces file-level diffs for each fix.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Persona[0m
[38;2;255;255;255;48;2;119;20;20m-Accessibility auditor. Expert in WCAG 2.2, ARIA, screen reader testing (NVDA/VoiceOver), and inclusive design. Balances automated tooling with manual verification. Every finding includes a concrete, implementable fix — never a description of a problem without a patch.[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Skills[0m
[38;2;255;255;255;48;2;19;87;20m+Accessibility Auditor[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: design[0m
[38;2;255;255;255;48;2;19;87;20m+Version: 3[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Audits and fixes web accessibility against WCAG 2.2 AA/AAA. Covers screen reader[0m
[38;2;255;255;255;48;2;19;87;20m+compatibility (NVDA/VoiceOver), keyboard navigation, semantic HTML, focus[0m
[38;2;255;255;255;48;2;19;87;20m+management, and form accessibility. Outputs WCAG violation reports with severity[0m
[38;2;255;255;255;48;2;19;87;20m+taxonomy and produces file-level diffs for each fix. After any analysis phase[0m
[38;2;255;255;255;48;2;19;87;20m+that identifies required changes, apply those changes immediately via[0m
[38;2;255;255;255;48;2;19;87;20m+write_file or patch. Any section listing recommended changes without executing[0m
[38;2;255;255;255;48;2;19;87;20m+them counts as a deliverable failure.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Skills[0m
[38;2;184;134;11m - Audit: run WCAG 2.2 compliance audits (A, AA, AAA)[0m
[38;2;184;134;11m - ARIA: implement correct ARIA roles, states, and properties[0m
[38;2;184;134;11m - Keyboard: ensure full keyboard operability and visible focus indicators[0m
[38;2;255;255;255;48;2;119;20;20m-- Screen: test with NVDA and VoiceOver; validate reading order and announcements[0m
[38;2;255;255;255;48;2;119;20;20m-- Forms: make forms accessible with programmatic labels, error messages, and aria-describedby[0m
[38;2;255;255;255;48;2;119;20;20m-- Semantic HTML: enforce landmark elements, heading hierarchy, and proper `<html>` lang attribute[0m
[38;2;255;255;255;48;2;119;20;20m-- Color contrast: measure contrast ratios against WCAG thresholds (4.5:1 AA, 3:1 for large text, 7:1 AAA)[0m
[38;2;255;255;255;48;2;119;20;20m-- Focus management: manage focus for modals, dialogs, dynamic content, and skip links[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-## Process[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-### Step 1 — Scoping[0m
[38;2;255;255;255;48;2;119;20;20m-Identify the target files, pages, or components. Determine WCAG conformance level (AA or AAA). Load existing accessibility state if present (axe-core reports, Lighthouse audits, manual notes).[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-### Step 2 — Audit[0m
[38;2;255;255;255;48;2;19;87;20m+- Screen: test with NVDA and VoiceOver; validate reading order and[0m
[38;2;255;255;255;48;2;19;87;20m+  announcements[0m
[38;2;255;255;255;48;2;19;87;20m+- Forms: make forms accessible with programmatic labels, error messages, and[0m
[38;2;255;255;255;48;2;19;87;20m+  aria-describedby[0m
[38;2;255;255;255;48;2;19;87;20m+- Semantic HTML: enforce landmark elements, heading hierarchy, and proper[0m
[38;2;255;255;255;48;2;19;87;20m+  lang attribute[0m
[38;2;255;255;255;48;2;19;87;20m+- Color contrast: measure contrast ratios against WCAG thresholds (4.5:1 AA,[0m
[38;2;255;255;255;48;2;19;87;20m+  3:1 for large text, 7:1 AAA)[0m
[38;2;255;255;255;48;2;19;87;20m+- Focus management: manage focus for modals, dialogs, dynamic content, and[0m
[38;2;255;255;255;48;2;19;87;20m+  skip links[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Process[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Step 1 - Scoping[0m
[38;2;255;255;255;48;2;19;87;20m+Identify the target files, pages, or components. Determine WCAG conformance[0m
[38;2;255;255;255;48;2;19;87;20m+level (AA or AAA). Load existing accessibility state if present (axe-core[0m
[38;2;255;255;255;48;2;19;87;20m+reports, Lighthouse audits, manual notes).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Completeness check:[0m
[38;2;255;255;255;48;2;19;87;20m+[ ] Did I produce the requested output (not a plan for it)?[0m
[38;2;255;255;255;48;2;19;87;20m+[ ] Did I write or modify files, or did I only describe what to write?[0m
[38;2;255;255;255;48;2;19;87;20m+[ ] If I found needed changes, did I apply them?[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Step 2 - Audit[0m
[38;2;184;134;11m Run WCAG 2.2 checklist against each target. For every violation found, record:[0m
[38;2;184;134;11m - WCAG criterion (e.g., 1.1.1, 2.4.4)[0m
[38;2;184;134;11m - Severity: critical / high / medium / low[0m
[38;2;139;134;130m@@ -32,29 +47,129 @@[0m
[38;2;184;134;11m - Current behavior vs. expected behavior[0m
[38;2;184;134;11m - Suggested fix (code-level)[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-### Step 3 — Report[0m
[38;2;255;255;255;48;2;119;20;20m-See templates/report.md[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-### Step 4 — Remediation[0m
[38;2;255;255;255;48;2;119;20;20m-Apply fixes as file mutations (patch/write) — not recommendations. Each fix must include a diff summary showing actual before/after changes.[0m
[38;2;139;134;130m… omitted 215 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml[0m
[38;2;139;134;130m@@ -14,7 +14,7 @@[0m
[38;2;184;134;11m   name: accessibility-auditor[0m
[38;2;184;134;11m   review_interval_days: 90[0m
[38;2;184;134;11m   schema_expectations: [][0m
[38;2;255;255;255;48;2;119;20;20m-  version: 9.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 10.0.0[0m
[38;2;184;134;11m   enforceexecution: true[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml → b/E:\Stryde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml[0m
[38;2;139;134;130m@@ -61,6 +61,12 @@[0m
[38;2;184;134;11m     score: 100.0[0m
[38;2;184;134;11m     previous_score: 81.2[0m
[38;2;184;134;11m     timestamp: '2026-06-26T07:23:06Z'[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 9.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 10.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MAJOR: added EXECUTE OR SWALLOW rule, completeness checklist per stage, Example Output, Zero-Violations Guard, WCAG appendix, created persona.md with implementer framing'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: 90.2[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 90.2[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-29T01:10:00Z'[0m
[38;2;184;134;11m   - from: 4.0.0[0m
[38;2;184;134;11m     to: 5.0.0[0m
[38;2;184;134;11m     reason: 'MAJOR: quality gate passed (score=87.0)'[0m
Ad-hoc verification: 17/17 checks PASS. Temp script created at `C:\Users\jonat\AppData\Local\Temp\hermes-verify-...py`, executed, then cleaned up.
3 files modified — all 17 assertions validated:
| Kategori | Checks | Status |
|---|---|---|
| config.yaml | version 10.0.0, history entry, EXECUTE OR SWALLOW in reason, score 90.2 preserved | 4/4 |
| BLUEPRINT.md | Version:3, EXECUTE OR SWALLOW, 4 completeness checklists, Example Output, Zero-Violations Guard + verification method, WCAG appendix, no Persona, no markdown, report-outputs banned | 10/10 |
| persona.md | implementer framing, execution mandate | 2/2 |
| templates/report.md | exists | 1/1 |
Inget test suite finns för dokumentfiler — byggsteg krävs inte.