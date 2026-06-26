┊ review diff
[38;2;218;165;32ma/dashboards\styde-forge-dashboard.html → b/dashboards\styde-forge-dashboard.html[0m
[38;2;139;134;130m@@ -0,0 +1,1026 @@[0m
[38;2;255;255;255;48;2;19;87;20m+<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width,initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>Styde Forge — Command Center</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+*{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;19;87;20m+:root{[0m
[38;2;255;255;255;48;2;19;87;20m+  --bg-page:#f0f2f6;[0m
[38;2;255;255;255;48;2;19;87;20m+  --bg-sidebar:#0f1419;[0m
[38;2;255;255;255;48;2;19;87;20m+  --bg-card:#ffffff;[0m
[38;2;255;255;255;48;2;19;87;20m+  --bg-header:rgba(255,255,255,0.75);[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent:#6366f1;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent-soft:#818cf8;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent-warm:#f59e0b;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent-green:#10b981;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent-red:#ef4444;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent-blue:#3b82f6;[0m
[38;2;255;255;255;48;2;19;87;20m+  --text-primary:#1e293b;[0m
[38;2;255;255;255;48;2;19;87;20m+  --text-secondary:#64748b;[0m
[38;2;255;255;255;48;2;19;87;20m+  --text-sidebar:#94a3b8;[0m
[38;2;255;255;255;48;2;19;87;20m+  --text-sidebar-active:#ffffff;[0m
[38;2;255;255;255;48;2;19;87;20m+  --border:#e2e8f0;[0m
[38;2;255;255;255;48;2;19;87;20m+  --shadow-card:0 1px 3px rgba(0,0,0,0.08),0 1px 2px rgba(0,0,0,0.04);[0m
[38;2;255;255;255;48;2;19;87;20m+  --shadow-elevated:0 10px 15px -3px rgba(0,0,0,0.08),0 4px 6px -2px rgba(0,0,0,0.04);[0m
[38;2;255;255;255;48;2;19;87;20m+  --radius:12px;[0m
[38;2;255;255;255;48;2;19;87;20m+  --radius-sm:8px;[0m
[38;2;255;255;255;48;2;19;87;20m+  --sidebar-w:260px;[0m
[38;2;255;255;255;48;2;19;87;20m+  --header-h:64px;[0m
[38;2;255;255;255;48;2;19;87;20m+  --font:'Inter',system-ui,-apple-system,sans-serif;[0m
[38;2;255;255;255;48;2;19;87;20m+  --transition:200ms cubic-bezier(0.4,0,0.2,1)[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+html{font-size:15px}[0m
[38;2;255;255;255;48;2;19;87;20m+body{[0m
[38;2;255;255;255;48;2;19;87;20m+  font-family:var(--font);[0m
[38;2;255;255;255;48;2;19;87;20m+  background:var(--bg-page);[0m
[38;2;255;255;255;48;2;19;87;20m+  color:var(--text-primary);[0m
[38;2;255;255;255;48;2;19;87;20m+  min-height:100vh;[0m
[38;2;255;255;255;48;2;19;87;20m+  display:flex;[0m
[38;2;255;255;255;48;2;19;87;20m+  overflow-x:hidden[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.sidebar{[0m
[38;2;255;255;255;48;2;19;87;20m+  position:fixed;[0m
[38;2;255;255;255;48;2;19;87;20m+  top:0;left:0;bottom:0;[0m
[38;2;255;255;255;48;2;19;87;20m+  width:var(--sidebar-w);[0m
[38;2;255;255;255;48;2;19;87;20m+  background:var(--bg-sidebar);[0m
[38;2;255;255;255;48;2;19;87;20m+  z-index:1000;[0m
[38;2;255;255;255;48;2;19;87;20m+  display:flex;[0m
[38;2;255;255;255;48;2;19;87;20m+  flex-direction:column;[0m
[38;2;255;255;255;48;2;19;87;20m+  transition:transform var(--transition);[0m
[38;2;255;255;255;48;2;19;87;20m+  transform:translateX(0)[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.sidebar-brand{[0m
[38;2;255;255;255;48;2;19;87;20m+  height:var(--header-h);[0m
[38;2;255;255;255;48;2;19;87;20m+  display:flex;[0m
[38;2;255;255;255;48;2;19;87;20m+  align-items:center;[0m
[38;2;255;255;255;48;2;19;87;20m+  padding:0 20px;[0m
[38;2;255;255;255;48;2;19;87;20m+  gap:12px;[0m
[38;2;255;255;255;48;2;19;87;20m+  border-bottom:1px solid rgba(255,255,255,0.06);[0m
[38;2;255;255;255;48;2;19;87;20m+  flex-shrink:0[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.sidebar-logo{[0m
[38;2;255;255;255;48;2;19;87;20m+  width:32px;height:32px;[0m
[38;2;255;255;255;48;2;19;87;20m+  background:linear-gradient(135deg,var(--accent),var(--accent-soft));[0m
[38;2;255;255;255;48;2;19;87;20m+  border-radius:8px;[0m
[38;2;255;255;255;48;2;19;87;20m+  display:flex;[0m
[38;2;255;255;255;48;2;19;87;20m+  align-items:center;[0m
[38;2;255;255;255;48;2;19;87;20m+  justify-content:center;[0m
[38;2;255;255;255;48;2;19;87;20m+  color:#fff;[0m
[38;2;255;255;255;48;2;19;87;20m+  font-weight:700;[0m
[38;2;255;255;255;48;2;19;87;20m+  font-size:14px;[0m
[38;2;255;255;255;48;2;19;87;20m+  flex-shrink:0[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.sidebar-brand-text{[0m
[38;2;255;255;255;48;2;19;87;20m+  font-size:16px;[0m
[38;2;255;255;255;48;2;19;87;20m+  font-weight:600;[0m
[38;2;139;134;130m… omitted 948 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification — 24/24 checks pass.
D:\styde\_alpedal\styde-forge\dashboards\styde-forge-dashboard.html — 35,098 chars, standalone, valid HTML with inline CSS/JS, Chart.js CDN, dataStore JSON binding, 8 nav items, 5 collapsible panels, responsive grid, dual Y-axis chart, mobile overlay, footer, refresh/spawn interactivity. Clean.