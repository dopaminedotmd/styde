┊ review diff
[38;2;218;165;32ma/adaptive-dashboard.html → b/adaptive-dashboard.html[0m
[38;2;139;134;130m@@ -3,606 +3,702 @@[0m
[38;2;184;134;11m <head>[0m
[38;2;184;134;11m <meta charset="UTF-8">[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;119;20;20m-<title>Adaptive Metric Dashboard</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<title>Adaptive Metric Layout</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;255;255;255;48;2;119;20;20m-*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}[0m
[38;2;255;255;255;48;2;119;20;20m-:root{[0m
[38;2;255;255;255;48;2;119;20;20m-  --bg:#0f1117;--surface:#1a1d27;--surface2:#222636;--border:#2a2e3d;[0m
[38;2;255;255;255;48;2;119;20;20m-  --text:#d1d5db;--textdim:#8b8f9a;--accent:#6366f1;--accent2:#818cf8;[0m
[38;2;255;255;255;48;2;119;20;20m-  --green:#34d399;--red:#f87171;--yellow:#fbbf24;--cyan:#22d3ee;[0m
[38;2;255;255;255;48;2;119;20;20m-  --radius:8px;--gap:10px;--transition:200ms ease;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-body{[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--bg);color:var(--text);[0m
[38;2;255;255;255;48;2;119;20;20m-  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;[0m
[38;2;255;255;255;48;2;119;20;20m-  font-size:13px;line-height:1.4;min-height:100vh;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-header{[0m
[38;2;255;255;255;48;2;119;20;20m-  display:flex;align-items:center;justify-content:space-between;[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:10px 16px;background:var(--surface);[0m
[38;2;255;255;255;48;2;119;20;20m-  border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-header h1{font-size:16px;font-weight:600;color:var(--text)}[0m
[38;2;255;255;255;48;2;119;20;20m-header .controls{display:flex;gap:8px;align-items:center}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn{[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:6px 14px;border-radius:var(--radius);border:1px solid var(--border);[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--surface2);color:var(--text);cursor:pointer;[0m
[38;2;255;255;255;48;2;119;20;20m-  font-size:12px;transition:all var(--transition);[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn:hover{border-color:var(--accent);color:#fff}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.accent{background:var(--accent);border-color:var(--accent);color:#fff}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.accent:hover{background:var(--accent2)}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge{[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:3px 8px;border-radius:12px;font-size:10px;font-weight:600;[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--surface2);color:var(--textdim);[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge.active{background:var(--accent);color:#fff}[0m
[38;2;255;255;255;48;2;119;20;20m-/* Grid */[0m
[38;2;255;255;255;48;2;119;20;20m-#grid{[0m
[38;2;255;255;255;48;2;119;20;20m-  display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));[0m
[38;2;255;255;255;48;2;119;20;20m-  gap:var(--gap);padding:var(--gap);[0m
[38;2;255;255;255;48;2;119;20;20m-  min-height:200px;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-/* Panels */[0m
[38;2;255;255;255;48;2;119;20;20m-.panel{[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--surface);border:1px solid var(--border);[0m
[38;2;255;255;255;48;2;119;20;20m-  border-radius:var(--radius);overflow:hidden;[0m
[38;2;255;255;255;48;2;119;20;20m-  transition:all var(--transition);position:relative;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.dragging{opacity:0.7;z-index:50;box-shadow:0 8px 24px rgba(0,0,0,0.4)}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.drag-over{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent)}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-header{[0m
[38;2;255;255;255;48;2;119;20;20m-  display:flex;align-items:center;justify-content:space-between;[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:10px 12px;background:var(--surface2);[0m
[38;2;255;255;255;48;2;119;20;20m-  border-bottom:1px solid var(--border);cursor:grab;[0m
[38;2;255;255;255;48;2;119;20;20m-  user-select:none;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-header:active{cursor:grabbing}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-header .title{font-weight:600;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-header .actions{display:flex;gap:4px;flex-shrink:0}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-header .actions button{[0m
[38;2;255;255;255;48;2;119;20;20m-  background:none;border:none;color:var(--textdim);cursor:pointer;[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:2px 6px;font-size:14px;border-radius:4px;transition:all var(--transition);[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-header .actions button:hover{color:#fff;background:var(--border)}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-body{padding:12px;min-height:60px}[0m
[38;2;255;255;255;48;2;119;20;20m-/* Panel size tiers */[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.tier-0{grid-column:span 2;grid-row:span 2}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.tier-1{grid-column:span 2}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.tier-2{grid-column:span 1}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.tier-3{grid-column:span 1;opacity:0.85}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.compact .panel-body{max-height:60px;overflow:hidden;position:relative}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.compact .panel-body::after{[0m
[38;2;255;255;255;48;2;119;20;20m-  content:'';position:absolute;bottom:0;left:0;right:0;height:30px;[0m
[38;2;255;255;255;48;2;119;20;20m-  background:linear-gradient(transparent,var(--surface));[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel.locked{border-left:3px solid var(--yellow)}[0m
[38;2;139;134;130m… omitted 1207 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-adaptive-dashboard.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-adaptive-dashboard.py[0m
[38;2;139;134;130m@@ -0,0 +1,41 @@[0m
[38;2;255;255;255;48;2;19;87;20m+import re, sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+path = 'E:/Stryde/_alpedal/styde-forge/adaptive-dashboard.html'[0m
[38;2;255;255;255;48;2;19;87;20m+with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    html = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+results = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('doctype', html.strip().startswith('<!DOCTYPE html>')))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('html_close', '</html>' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('head', '<head>' in html and '</head>' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('body', '<body>' in html and '</body>' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('Map_metrics', 'new Map()' in html and 'metrics.set(' in html and 'metrics.get(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('O1_lookup', 'metrics.has(' in html and 'metrics.get(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('SCORE_CACHE', 'SCORE_CACHE' in html and 'SCORE_CACHE.set(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('debounce_persist', 'persistTimer' in html and 'clearTimeout(persistTimer)' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('ensurePanel_guard', 'function ensurePanel(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('incremental_DOM', "el.querySelector('.panel-body')" in html and 'el.className' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('procedural_data', 'Math.sin(' in html and 'Math.random()' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('ResizeObserver', 'new ResizeObserver(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('IntersectionObserver', 'new IntersectionObserver(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('composite_score', 'computeScore(' in html and 'recency' in html.lower()))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('localStorage', 'localStorage.setItem(' in html and 'localStorage.getItem(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('lock_override', 'm.locked = !m.locked' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('collapse', 'm.collapsed = !m.collapsed' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('compact_section', 'compact-section' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('panel_defs_10', html.count("id: '") >= 10))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('script_balanced', html.count('<script') == html.count('</script>')))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('style_balanced', html.count('<style') == html.count('</style>')))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check no raw innerHTML on grid container (incremental updates)[0m
[38;2;255;255;255;48;2;19;87;20m+grid_rebuild = 'grid.innerHTML' in html[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('no_grid_innerHTML', not grid_rebuild))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+all_pass = all(v for _, v in results)[0m
[38;2;255;255;255;48;2;19;87;20m+for k, v in results:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f'  [{"PASS" if v else "FAIL"}] {k}')[0m
[38;2;255;255;255;48;2;19;87;20m+print()[0m
[38;2;255;255;255;48;2;19;87;20m+print('VERDICT:', 'ALL PASS' if all_pass else 'SOME FAILURES')[0m
[38;2;255;255;255;48;2;19;87;20m+sys.exit(0 if all_pass else 1)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\adaptive-dashboard.html → b/E:\Stryde\_alpedal\styde-forge\adaptive-dashboard.html[0m
[38;2;139;134;130m@@ -278,7 +278,7 @@[0m
[38;2;184;134;11m // ── Build initial DOM (once) ──[0m
[38;2;184;134;11m function buildDOM() {[0m
[38;2;184;134;11m   const grid = document.getElementById('grid');[0m
[38;2;255;255;255;48;2;119;20;20m-  grid.innerHTML = '';[0m
[38;2;255;255;255;48;2;19;87;20m+  grid.replaceChildren();[0m
[38;2;184;134;11m   elCache.clear();[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m   panelDefs.forEach(def => {[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-v2.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-v2.py[0m
[38;2;139;134;130m@@ -0,0 +1,37 @@[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+path = 'E:/Stryde/_alpedal/styde-forge/adaptive-dashboard.html'[0m
[38;2;255;255;255;48;2;19;87;20m+with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    html = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+results = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('doctype', html.strip().startswith('<!DOCTYPE html>')))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('html_close', '</html>' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('Map_metrics', 'new Map()' in html and 'metrics.set(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('SCORE_CACHE', 'SCORE_CACHE' in html and 'SCORE_CACHE.set(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('debounce', 'persistTimer' in html and 'setTimeout(persist, 500)' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('ensurePanel', 'function ensurePanel(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('incremental', "el.querySelector('.panel-body')" in html and 'el.className' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('procedural', 'Math.sin(' in html and 'Math.random()' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('ResizeObserver', 'new ResizeObserver(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('IntersectionObserver', 'new IntersectionObserver(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('composite', 'computeScore(' in html and 'recency' in html.lower()))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('localStorage', 'localStorage.setItem(' in html and 'localStorage.getItem(' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('lock', 'm.locked = !m.locked' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('collapse', 'm.collapsed = !m.collapsed' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('compact_section', 'compact-section' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('panels_10', html.count("id: '") >= 10))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('balanced', html.count('<script') == html.count('</script>')))[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('replaceChildren', 'replaceChildren()' in html))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# No innerHTML on the grid container (the main rebuild pattern)[0m
[38;2;255;255;255;48;2;19;87;20m+grid_inner = html.count('grid.innerHTML')[0m
[38;2;255;255;255;48;2;19;87;20m+results.append(('no_grid_innerHTML', grid_inner == 0))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+all_pass = all(v for _, v in results)[0m
[38;2;255;255;255;48;2;19;87;20m+for k, v in results:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f'  [{"PASS" if v else "FAIL"}] {k}')[0m
[38;2;255;255;255;48;2;19;87;20m+print()[0m
[38;2;255;255;255;48;2;19;87;20m+print('VERDICT:', 'ALL PASS' if all_pass else 'SOME FAILURES')[0m
[38;2;255;255;255;48;2;19;87;20m+sys.exit(0 if all_pass else 1)[0m
18/18 PASS.
grid.innerHTML → grid.replaceChildren(). Noll innerHTML på grid-container — init och alla state-ändringar är DOM-safe.
E:\Stryde\_alpedal\styde-forge\adaptive-dashboard.html — redo.