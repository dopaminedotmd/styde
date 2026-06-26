┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-visualization-expert\BLUEPRINT.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\data-visualization-expert\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,5 +1,5 @@[0m
[38;2;184;134;11m # Data Visualization Expert[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** data-science **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: data-science Version: 1[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;184;134;11m Creates data visualizations. D3.js, Observable, Vega-Lite, interactive dashboards.[0m
[38;2;139;134;130m@@ -13,3 +13,13 @@[0m
[38;2;184;134;11m - Dashboard: create interactive analytics dashboards[0m
[38;2;184;134;11m - Perception: apply visual perception principles[0m
[38;2;184;134;11m - Accessible: ensure accessible data viz patterns[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Clarification[0m
[38;2;255;255;255;48;2;19;87;20m+When request is ambiguous, clarify each field on one compact line:[0m
[38;2;255;255;255;48;2;19;87;20m+  [ ? ] data source: [CSV|JSON|Live API|None provided][0m
[38;2;255;255;255;48;2;19;87;20m+  [ ? ] chart type: [bar|line|scatter|heatmap|area|donut|custom][0m
[38;2;255;255;255;48;2;19;87;20m+  [ ? ] interactivity: [static|tooltips|zoom|filter|brush|drill-down][0m
[38;2;255;255;255;48;2;19;87;20m+  [ ? ] output format: [HTML|SVG|PNG|Vega spec|iframes][0m
[38;2;255;255;255;48;2;19;87;20m+  [ ? ] color palette: [categorical|sequential|diverging|custom][0m
[38;2;255;255;255;48;2;19;87;20m+If the user has a strong opinion, they reply in one word. If not, pick the[0m
[38;2;255;255;255;48;2;19;87;20m+most common default and proceed — do not re-ask unless critical.[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-blueprint.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-blueprint.py[0m
[38;2;139;134;130m@@ -0,0 +1,65 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: BLUEPRINT.md for data-visualization-expert.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Checks:[0m
[38;2;255;255;255;48;2;19;87;20m+1. Required sections exist (Purpose, Persona, Skills, Clarification)[0m
[38;2;255;255;255;48;2;19;87;20m+2. Clarification uses compact [ ? ] format (not verbose 'specify one of')[0m
[38;2;255;255;255;48;2;19;87;20m+3. Markdown structure is parseable[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, re[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+bp_path = os.path.expanduser([0m
[38;2;255;255;255;48;2;19;87;20m+    "D:/styde/_alpedal/styde-forge/StydeAgents/blueprints/data-visualization-expert/BLUEPRINT.md"[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(bp_path):[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAIL: BLUEPRINT.md not found at {bp_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(bp_path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check required sections[0m
[38;2;255;255;255;48;2;19;87;20m+for section in ["## Purpose", "## Persona", "## Skills", "## Clarification"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    if section not in content:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing section: {section}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check no verbose 'specify one of' phrasing remains[0m
[38;2;255;255;255;48;2;19;87;20m+verbose_patterns = [[0m
[38;2;255;255;255;48;2;19;87;20m+    r"specify one of",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"specify which",[0m
[38;2;255;255;255;48;2;19;87;20m+    r"please indicate",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for pat in verbose_patterns:[0m
[38;2;255;255;255;48;2;19;87;20m+    matches = re.findall(pat, content, re.IGNORECASE)[0m
[38;2;255;255;255;48;2;19;87;20m+    if matches:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Verbose clarification phrasing found: {matches}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check compact [ ? ] format is present[0m
[38;2;255;255;255;48;2;19;87;20m+if not re.search(r"\[\s*\?\s*\].+\[.+\|.+\]", content):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("Missing compact [ ? ] field: [A|B|C] format in Clarification")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check structure: sections should be h2 headings (##)[0m
[38;2;255;255;255;48;2;19;87;20m+h2s = re.findall(r"^## (.+)$", content, re.MULTILINE)[0m
[38;2;255;255;255;48;2;19;87;20m+expected = {"Purpose", "Persona", "Skills", "Clarification"}[0m
[38;2;255;255;255;48;2;19;87;20m+found = set(h2s)[0m
[38;2;255;255;255;48;2;19;87;20m+missing = expected - found[0m
[38;2;255;255;255;48;2;19;87;20m+if missing:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"Missing h2 sections: {missing}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFY FAIL")[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  - {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    n_lines = content.count("\n") + 1[0m
[38;2;255;255;255;48;2;19;87;20m+    n_chars = len(content)[0m
[38;2;255;255;255;48;2;19;87;20m+    print("VERIFY PASS")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  File: {bp_path}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  Lines: {n_lines}, Chars: {n_chars}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  Sections: {', '.join(h2s)}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  Clarification format: compact [ ? ] field: [A|B|C]")[0m
[38;2;255;255;255;48;2;19;87;20m+    print("  No verbose 'specify one of' phrasing detected")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(0)[0m
Ad-hoc verification: PASS (no temp file left behind this time).
- All 4 required sections present: Purpose, Persona, Skills, Clarification
- Clarification uses compact `[ ? ] field: [A|B|C]` format — zero verbose "specify one of" phrasing
- 26 lines, 1045 chars total
- This is an ad-hoc structural check, not a full test suite pass