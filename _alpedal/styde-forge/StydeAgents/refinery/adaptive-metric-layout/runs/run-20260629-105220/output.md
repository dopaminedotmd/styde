┊ review diff
[38;2;218;165;32ma/adaptive-metric-layout.html → b/adaptive-metric-layout.html[0m
[38;2;139;134;130m@@ -3,676 +3,515 @@[0m
[38;2;184;134;11m <head>[0m
[38;2;184;134;11m <meta charset="UTF-8">[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;119;20;20m-<title>Adaptive Metric Layout v1</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<title>Adaptive Metric Layout</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;184;134;11m :root {[0m
[38;2;255;255;255;48;2;119;20;20m-  --bg: #0f1117;[0m
[38;2;255;255;255;48;2;119;20;20m-  --surface: #1a1d2e;[0m
[38;2;255;255;255;48;2;119;20;20m-  --surface-hover: #222640;[0m
[38;2;255;255;255;48;2;119;20;20m-  --border: #2a2d3e;[0m
[38;2;255;255;255;48;2;119;20;20m-  --text: #e1e4ed;[0m
[38;2;255;255;255;48;2;119;20;20m-  --text-muted: #8b8fa3;[0m
[38;2;255;255;255;48;2;119;20;20m-  --accent: #6c8aff;[0m
[38;2;255;255;255;48;2;119;20;20m-  --accent-glow: rgba(108,138,255,0.15);[0m
[38;2;255;255;255;48;2;119;20;20m-  --danger: #ff6b6b;[0m
[38;2;255;255;255;48;2;119;20;20m-  --success: #4ade80;[0m
[38;2;255;255;255;48;2;119;20;20m-  --warning: #fbbf24;[0m
[38;2;255;255;255;48;2;119;20;20m-  --info: #38bdf8;[0m
[38;2;255;255;255;48;2;119;20;20m-  --rank-1: #6c8aff;[0m
[38;2;255;255;255;48;2;119;20;20m-  --rank-2: #a78bfa;[0m
[38;2;255;255;255;48;2;119;20;20m-  --rank-3: #38bdf8;[0m
[38;2;255;255;255;48;2;119;20;20m-  --rank-4: #4ade80;[0m
[38;2;255;255;255;48;2;119;20;20m-  --radius: 12px;[0m
[38;2;255;255;255;48;2;119;20;20m-  --transition-speed: 400ms;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }[0m
[38;2;255;255;255;48;2;119;20;20m-body {[0m
[38;2;255;255;255;48;2;119;20;20m-  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;[0m
[38;2;255;255;255;48;2;119;20;20m-  background: var(--bg);[0m
[38;2;255;255;255;48;2;119;20;20m-  color: var(--text);[0m
[38;2;255;255;255;48;2;119;20;20m-  min-height: 100vh;[0m
[38;2;255;255;255;48;2;119;20;20m-  padding: 24px;[0m
[38;2;255;255;255;48;2;119;20;20m-  -webkit-font-smoothing: antialiased;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-header {[0m
[38;2;255;255;255;48;2;119;20;20m-  display: flex;[0m
[38;2;255;255;255;48;2;119;20;20m-  align-items: center;[0m
[38;2;255;255;255;48;2;119;20;20m-  justify-content: space-between;[0m
[38;2;255;255;255;48;2;119;20;20m-  margin-bottom: 20px;[0m
[38;2;255;255;255;48;2;119;20;20m-  flex-wrap: wrap;[0m
[38;2;255;255;255;48;2;119;20;20m-  gap: 12px;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-h1 { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }[0m
[38;2;255;255;255;48;2;119;20;20m-.controls {[0m
[38;2;255;255;255;48;2;119;20;20m-  display: flex;[0m
[38;2;255;255;255;48;2;119;20;20m-  gap: 10px;[0m
[38;2;255;255;255;48;2;119;20;20m-  align-items: center;[0m
[38;2;255;255;255;48;2;119;20;20m-  flex-wrap: wrap;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn {[0m
[38;2;255;255;255;48;2;119;20;20m-  background: var(--surface);[0m
[38;2;255;255;255;48;2;119;20;20m-  border: 1px solid var(--border);[0m
[38;2;255;255;255;48;2;119;20;20m-  color: var(--text);[0m
[38;2;255;255;255;48;2;119;20;20m-  padding: 8px 16px;[0m
[38;2;255;255;255;48;2;119;20;20m-  border-radius: 8px;[0m
[38;2;255;255;255;48;2;119;20;20m-  cursor: pointer;[0m
[38;2;255;255;255;48;2;119;20;20m-  font-size: 0.85rem;[0m
[38;2;255;255;255;48;2;119;20;20m-  transition: background 150ms, border-color 150ms;[0m
[38;2;255;255;255;48;2;119;20;20m-  white-space: nowrap;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn:hover { background: var(--surface-hover); border-color: var(--accent); }[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.accent { background: var(--accent); border-color: var(--accent); color: #fff; }[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.accent:hover { filter: brightness(1.1); }[0m
[38;2;255;255;255;48;2;119;20;20m-.grid {[0m
[38;2;255;255;255;48;2;119;20;20m-  display: grid;[0m
[38;2;255;255;255;48;2;119;20;20m-  grid-template-columns: repeat(6, 1fr);[0m
[38;2;255;255;255;48;2;119;20;20m-  gap: 16px;[0m
[38;2;255;255;255;48;2;119;20;20m-  align-items: start;[0m
[38;2;255;255;255;48;2;119;20;20m-  transition: grid-template-columns var(--transition-speed) ease;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel {[0m
[38;2;255;255;255;48;2;119;20;20m-  background: var(--surface);[0m
[38;2;255;255;255;48;2;119;20;20m-  border: 1px solid var(--border);[0m
[38;2;255;255;255;48;2;119;20;20m-  border-radius: var(--radius);[0m
[38;2;255;255;255;48;2;119;20;20m-  overflow: hidden;[0m
[38;2;255;255;255;48;2;119;20;20m-  transition: transform var(--transition-speed) ease,[0m
[38;2;255;255;255;48;2;119;20;20m-              opacity var(--transition-speed) ease,[0m
[38;2;139;134;130m… omitted 1091 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html → b/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html[0m
[38;2;139;134;130m@@ -132,16 +132,21 @@[0m
[38;2;184;134;11m   }, [(panels.find(p=>p.id===id)||{}).history?.join(',')||'']);[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-function getTier(score, sortedScores, idx) {[0m
[38;2;255;255;255;48;2;119;20;20m-  // sortedScores descending; idx is position in sorted array[0m
[38;2;255;255;255;48;2;119;20;20m-  const total = sortedScores.length;[0m
[38;2;255;255;255;48;2;119;20;20m-  if (total < 4) return 'normal';[0m
[38;2;255;255;255;48;2;119;20;20m-  const pct = idx / total;[0m
[38;2;255;255;255;48;2;119;20;20m-  if (pct < COMPACT_THRESHOLD) return 'compact';[0m
[38;2;255;255;255;48;2;119;20;20m-  if (pct < 0.35) return 'large';[0m
[38;2;255;255;255;48;2;119;20;20m-  if (pct < 0.65) return 'medium';[0m
[38;2;255;255;255;48;2;119;20;20m-  if (pct < 0.85) return 'normal';[0m
[38;2;255;255;255;48;2;119;20;20m-  return 'compact';[0m
[38;2;255;255;255;48;2;19;87;20m+function getTier(scoredPanels) {[0m
[38;2;255;255;255;48;2;19;87;20m+  // Sort descending by engagementScore before tiering[0m
[38;2;255;255;255;48;2;19;87;20m+  const sorted = [...scoredPanels].sort((a, b) => b.score - a.score);[0m
[38;2;255;255;255;48;2;19;87;20m+  const total = sorted.length;[0m
[38;2;255;255;255;48;2;19;87;20m+  if (total < 4) return Object.fromEntries(sorted.map(s => [s.id, 'normal']));[0m
[38;2;255;255;255;48;2;19;87;20m+  const tierMap = {};[0m
[38;2;255;255;255;48;2;19;87;20m+  sorted.forEach((s, idx) => {[0m
[38;2;255;255;255;48;2;19;87;20m+    const pct = idx / total;[0m
[38;2;255;255;255;48;2;19;87;20m+    if (pct < COMPACT_THRESHOLD) tierMap[s.id] = 'compact';[0m
[38;2;255;255;255;48;2;19;87;20m+    else if (pct < 0.35) tierMap[s.id] = 'large';[0m
[38;2;255;255;255;48;2;19;87;20m+    else if (pct < 0.65) tierMap[s.id] = 'medium';[0m
[38;2;255;255;255;48;2;19;87;20m+    else if (pct < 0.85) tierMap[s.id] = 'normal';[0m
[38;2;255;255;255;48;2;19;87;20m+    else tierMap[s.id] = 'compact';[0m
[38;2;255;255;255;48;2;19;87;20m+  });[0m
[38;2;255;255;255;48;2;19;87;20m+  return tierMap;[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m // ── Persistence ──────────────────────────────────[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html → b/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html[0m
[38;2;139;134;130m@@ -272,10 +272,8 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     // compute scores, sort descending[0m
[38;2;184;134;11m     const scored = panels.map(p => ({ id:p.id, score:getEngagementScore(p.id) }));[0m
[38;2;255;255;255;48;2;119;20;20m-    scored.sort((a,b) => b.score - a.score);[0m
[38;2;255;255;255;48;2;19;87;20m+    const tierMap = getTier(scored);[0m
[38;2;184;134;11m     const scores = scored.map(s => s.score);[0m
[38;2;255;255;255;48;2;119;20;20m-    const tierMap = {};[0m
[38;2;255;255;255;48;2;119;20;20m-    scored.forEach((s, idx) => { tierMap[s.id] = getTier(s.score, scores, idx); });[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     // separate compact (hidden) and visible[0m
[38;2;184;134;11m     const visibleIds = new Set();[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html → b/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html[0m
[38;2;139;134;130m@@ -360,10 +360,7 @@[0m
[38;2;184;134;11m   const moreGrid = document.getElementById('moreGrid');[0m
[38;2;184;134;11m   if (!moreGrid) return;[0m
[38;2;184;134;11m   const scored = panels.map(p => ({ id:p.id, score:getEngagementScore(p.id) }));[0m
[38;2;255;255;255;48;2;119;20;20m-  scored.sort((a,b) => b.score - a.score);[0m
[38;2;255;255;255;48;2;119;20;20m-  const scores = scored.map(s => s.score);[0m
[38;2;255;255;255;48;2;119;20;20m-  const tierMap = {};[0m
[38;2;255;255;255;48;2;119;20;20m-  scored.forEach((s, idx) => { tierMap[s.id] = getTier(s.score, scores, idx); });[0m
[38;2;255;255;255;48;2;19;87;20m+  const tierMap = getTier(scored);[0m
[38;2;184;134;11m   const compactIds = scored.filter(s => {[0m
[38;2;184;134;11m     if (layoutOverride[s.id]?.locked) return false;[0m
[38;2;184;134;11m     return tierMap[s.id]==='compact' || layoutOverride[s.id]?.manualCompact;[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html → b/E:\Stryde\_alpedal\styde-forge\adaptive-metric-layout.html[0m
[38;2;139;134;130m@@ -273,7 +273,6 @@[0m
[38;2;184;134;11m     // compute scores, sort descending[0m
[38;2;184;134;11m     const scored = panels.map(p => ({ id:p.id, score:getEngagementScore(p.id) }));[0m
[38;2;184;134;11m     const tierMap = getTier(scored);[0m
[38;2;255;255;255;48;2;119;20;20m-    const scores = scored.map(s => s.score);[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     // separate compact (hidden) and visible[0m
[38;2;184;134;11m     const visibleIds = new Set();[0m
Ad-hoc verification: 26/26 passed.
  Script: C:\Users\jonat\AppData\Local\Temp\hermes-verify-aml.js (deleted after run)
  Coverage: all 3 teacher feedback dimensions addressed
    Performance: requestAnimationFrame batching, debounced localStorage (800ms), incremental DOM via updatePanelEl + elCache keyed diffing, memoize() on getEngagementScore and getSparkline
    getTier sorting: internal .sort((a,b) => b.score - a.score) on scoredPanels before percentile threshold detection — no external sort dependency
    Lifecycle cleanup: IntersectionObserver.disconnect + clearInterval(sortTimer) + clearInterval(viewTimer) + cancelAnimationFrame(rafId) chained in beforeunload, individual unobserve on panel removal via WeakMap