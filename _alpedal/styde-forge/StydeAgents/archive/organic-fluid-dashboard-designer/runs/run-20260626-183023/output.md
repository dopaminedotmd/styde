scripts/validate.sh
#!/usr/bin/env bash
set -euo pipefail
PASS=0 FAIL=0
check() {
  local label=$1 desc=$2
  if [ $? -eq 0 ]; then
    echo "PASS: $label"
    PASS=$((PASS+1))
  else
    echo "FAIL: $label ($desc)"
    FAIL=$((FAIL+1))
  fi
}
echo "=== Validation Gate ==="
# 1 - HTML well-formedness
xmllint --noout index.html 2>/dev/null
check "HTML well-formedness" "tag balance, no unclosed elements"
# 2 - DOCTYPE present
head -1 index.html | grep -q '<\!DOCTYPE html>'
check "DOCTYPE html" "first line must be doctype"
# 3 - charset meta present
grep -qi 'charset' index.html
check "Charset meta" "charset declaration required"
# 4 - :root custom properties exist
grep -q ':root' styles/main.css
check ":root block" "custom properties must be defined in :root"
# 5 - no duplicate keyframe names
dup=$(grep -oP '@keyframes\s+\K[a-zA-Z0-9_-]+' styles/main.css | sort | uniq -d)
if [ -z "$dup" ]; then check "No duplicate keyframes" ""; else FAIL=$((FAIL+1)); echo "FAIL: Duplicate keyframes: $dup"; fi
# 6 - stylesheet size <= 50KB
size=$(wc -c < styles/main.css)
if [ "$size" -le 51200 ]; then check "Stylesheet size <= 50KB" "actual: $size bytes"; else FAIL=$((FAIL+1)); echo "FAIL: Stylesheet $size bytes > 50KB"; fi
# 7 - declaration count <= 800
decl=$(grep -o '{' styles/main.css | wc -l)
if [ "$decl" -le 800 ]; then check "Declaration count <= 800" "actual: $decl"; else FAIL=$((FAIL+1)); echo "FAIL: $decl declarations > 800"; fi
# 8 - no hardcoded colors outside :root
hits=$(grep -n '#[0-9a-fA-F]\{3,6\}\|rgb\|hsl\|rgba\|hsla' styles/main.css | grep -v ':root' || true)
if [ -z "$hits" ]; then check "No hardcoded colors outside :root" ""; else FAIL=$((FAIL+1)); echo "FAIL: Hardcoded colors found"; echo "$hits"; fi
echo "=== Results: $PASS pass, $FAIL fail ==="
---
styles/main.css
:root {
  --bg-page: #faf4f0;
  --bg-card: rgba(255, 248, 242, 0.75);
  --bg-glass: rgba(255, 255, 255, 0.45);
  --surface-elevated: rgba(255, 243, 235, 0.85);
  --accent-soft: #e8a87c;
  --accent-core: #d48c6b;
  --accent-warm: #f5cdb0;
  --accent-amber: #e0b094;
  --ink-primary: #4a3e37;
  --ink-secondary: #7a6b62;
  --ink-muted: #b5a69b;
  --ink-inverse: #fcf6f0;
  --glow-highlight: rgba(232, 168, 124, 0.18);
  --glow-ambient: rgba(245, 205, 176, 0.08);
  --blur-depth: 18px;
  --radius-blob: 28px;
  --radius-card: 20px;
  --radius-pill: 100px;
  --radius-input: 14px;
  --font-body: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'SF Mono', 'Cascadia Code', monospace;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  --shadow-card: 0 4px 24px rgba(74, 62, 55, 0.06), 0 1px 4px rgba(74, 62, 55, 0.04);
  --shadow-float: 0 8px 40px rgba(74, 62, 55, 0.08);
  --transition-organic: 0.45s cubic-bezier(0.34, 1.0, 0.64, 1.0);
  --blob-1: 42% 58% 54% 46% / 38% 62% 38% 62%;
  --blob-2: 38% 62% 48% 52% / 52% 48% 52% 48%;
  --blob-3: 44% 56% 52% 48% / 36% 64% 36% 64%;
}
*, *::before, *::after {
  box-sizing: border-box; margin: 0; padding: 0;
}
html {
  font-size: 16px; -webkit-font-smoothing: antialiased;
}
body {
  background: var(--bg-page);
  color: var(--ink-primary);
  font-family: var(--font-body);
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}
body::before {
  content: ''; position: fixed; inset: 0;
  background: radial-gradient(ellipse 80% 60% at 20% 10%, var(--glow-highlight) 0%, transparent 60%),
              radial-gradient(ellipse 60% 50% at 80% 90%, var(--glow-ambient) 0%, transparent 50%);
  pointer-events: none; z-index: 0;
}
.app-container {
  position: relative; z-index: 1;
  max-width: 1280px; margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-lg);
}
/* biomorphic blobs */
.blob-decor {
  position: fixed; border-radius: var(--radius-blob); filter: blur(40px); opacity: 0.35; z-index: 0;
  animation: blob-drift 18s ease-in-out infinite alternate;
}
.blob-decor--a {
  width: 520px; height: 480px;
  background: radial-gradient(ellipse, var(--accent-warm), var(--accent-amber) 70%);
  top: -120px; right: -80px;
  border-radius: var(--blob-1);
  animation-duration: 22s;
}
.blob-decor--b {
  width: 400px; height: 420px;
  background: radial-gradient(ellipse, var(--accent-soft), var(--accent-core) 65%);
  bottom: -60px; left: -100px;
  border-radius: var(--blob-2);
  animation-duration: 26s; animation-delay: -4s;
}
.blob-decor--c {
  width: 300px; height: 280px;
  background: radial-gradient(ellipse, #f2d5c0, #dcb69c);
  top: 45%; left: 55%;
  border-radius: var(--blob-3);
  animation-duration: 20s; animation-delay: -10s; opacity: 0.2;
}
@keyframes blob-drift {
  0%   { transform: translate(0, 0) scale(1) rotate(0deg); }
  33%  { transform: translate(18px, -24px) scale(1.04) rotate(3deg); border-radius: var(--blob-2); }
  66%  { transform: translate(-12px, 16px) scale(0.96) rotate(-2deg); border-radius: var(--blob-3); }
  100% { transform: translate(10px, -8px) scale(1.02) rotate(1deg); border-radius: var(--blob-1); }
}
/* header */
.dash-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: var(--spacing-2xl);
  padding: var(--spacing-lg) 0;
  border-bottom: 1px solid rgba(180, 166, 155, 0.2);
}
.dash-header h1 {
  font-size: 1.75rem; font-weight: 500;
  letter-spacing: -0.02em; color: var(--ink-primary);
  background: linear-gradient(135deg, var(--ink-primary) 40%, var(--accent-core));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.dash-header time {
  color: var(--ink-muted); font-size: 0.875rem;
}
/* stat cards grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}
.stat-card {
  background: var(--bg-glass);
  backdrop-filter: blur(var(--blur-depth));
  -webkit-backdrop-filter: blur(var(--blur-depth));
  border: 1px solid rgba(255, 248, 242, 0.5);
  border-radius: var(--radius-card);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
  transition: var(--transition-organic);
  cursor: default;
  position: relative; overflow: hidden;
}
.stat-card::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, transparent 60%, rgba(232, 168, 124, 0.06));
  opacity: 0; transition: opacity 0.6s ease;
}
.stat-card:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: var(--shadow-float);
}
.stat-card:hover::before { opacity: 1; }
.stat-card__icon {
  font-size: 1.75rem; margin-bottom: var(--spacing-sm);
  display: inline-block;
  animation: icon-breathe 3s ease-in-out infinite;
}
.stat-card__icon--pulse { animation-delay: 0s; }
.stat-card__icon--pulse2 { animation-delay: 0.6s; }
.stat-card__icon--pulse3 { animation-delay: 1.2s; }
.stat-card__icon--pulse4 { animation-delay: 1.8s; }
@keyframes icon-breathe {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.08); opacity: 1; }
}
.stat-card__value {
  font-size: 1.8rem; font-weight: 500;
  letter-spacing: -0.02em; color: var(--ink-primary);
  line-height: 1.2;
}
.stat-card__label {
  font-size: 0.8rem; color: var(--ink-secondary);
  text-transform: uppercase; letter-spacing: 0.06em;
  margin-top: var(--spacing-xs);
}
.stat-card__trend {
  display: inline-flex; align-items: center; gap: var(--spacing-xs);
  font-size: 0.75rem; margin-top: var(--spacing-sm);
  padding: 2px 10px; border-radius: var(--radius-pill);
  background: rgba(180, 166, 155, 0.08);
}
.stat-card__trend--up { color: #7aaa7a; background: rgba(122, 170, 122, 0.1); }
.stat-card__trend--down { color: #c4877a; background: rgba(196, 135, 122, 0.1); }
/* main content 2-col */
.dash-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}
.card {
  background: var(--bg-card);
  backdrop-filter: blur(var(--blur-depth));
  -webkit-backdrop-filter: blur(var(--blur-depth));
  border: 1px solid rgba(255, 248, 242, 0.5);
  border-radius: var(--radius-card);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
  transition: var(--transition-organic);
}
.card:hover {
  box-shadow: var(--shadow-float);
  border-color: rgba(245, 205, 176, 0.3);
}
.card--wide { grid-column: 1 / -1; }
.card__title {
  font-size: 1rem; font-weight: 500;
  color: var(--ink-primary); margin-bottom: var(--spacing-md);
  display: flex; align-items: center; gap: var(--spacing-sm);
}
.card__title::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(180, 166, 155, 0.3), transparent);
}
/* mood bar */
.mood-bar {
  display: flex; gap: var(--spacing-sm);
  align-items: flex-end; height: 120px;
  padding: var(--spacing-sm) 0;
}
.mood-bar__segment {
  flex: 1; border-radius: 8px 8px 4px 4px;
  background: var(--accent-soft);
  min-height: 6px; opacity: 0.6;
  transition: var(--transition-organic);
  animation: mood-rise 0.8s ease-out both;
  cursor: pointer;
}
.mood-bar__segment:hover {
  opacity: 1; transform: scaleY(1.03);
  background: var(--accent-core);
}
.mood-bar__segment--h60  { height: 60%;  animation-delay: 0.05s; }
.mood-bar__segment--h75  { height: 75%;  animation-delay: 0.10s; }
.mood-bar__segment--h85  { height: 85%;  animation-delay: 0.15s; }
.mood-bar__segment--h55  { height: 55%;  animation-delay: 0.20s; }
.mood-bar__segment--h70  { height: 70%;  animation-delay: 0.25s; }
.mood-bar__segment--h90  { height: 90%;  animation-delay: 0.30s; }
.mood-bar__segment--h45  { height: 45%;  animation-delay: 0.35s; }
@keyframes mood-rise {
  0%   { height: 0; opacity: 0; }
  100% { opacity: inherit; }
}
/* activity list */
.activity-list {
  list-style: none;
}
.activity-list li {
  display: flex; align-items: center; gap: var(--spacing-md);
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid rgba(180, 166, 155, 0.1);
}
.activity-list li:last-child { border-bottom: none; }
.activity-dot {
  width: 10px; height: 10px; border-radius: 50%;
  flex-shrink: 0;
  background: var(--accent-soft);
  animation: dot-pulse 2s ease-in-out infinite;
}
.activity-dot--amber { background: var(--accent-amber); }
.activity-dot--core { background: var(--accent-core); }
@keyframes dot-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(232, 168, 124, 0.3); }
  50% { box-shadow: 0 0 0 6px rgba(232, 168, 124, 0.05); }
}
.activity-text { flex: 1; font-size: 0.875rem; color: var(--ink-secondary); }
.activity-text strong { color: var(--ink-primary); font-weight: 500; }
.activity-time { font-size: 0.75rem; color: var(--ink-muted); }
/* progress ring row */
.progress-row {
  display: flex; gap: var(--spacing-xl);
  justify-content: center; padding: var(--spacing-md) 0;
}
.progress-ring-wrap {
  display: flex; flex-direction: column; align-items: center; gap: var(--spacing-sm);
}
.progress-ring {
  width: 80px; height: 80px; border-radius: 50%;
  position: relative; display: flex; align-items: center; justify-content: center;
}
.progress-ring__track { position: absolute; inset: 0; }
.progress-ring__track svg { transform: rotate(-90deg); width: 100%; height: 100%; }
.progress-ring__track circle {
  fill: none; stroke-width: 4; cx: 40; cy: 40; r: 34;
}
.progress-ring__bg { stroke: rgba(180, 166, 155, 0.12); }
.progress-ring__fill {
  stroke: var(--accent-core); stroke-linecap: round;
  stroke-dasharray: 213.63; stroke-dashoffset: 213.63;
  transition: stroke-dashoffset 0.8s ease; animation: ring-fill 1.2s ease forwards;
}
.progress-ring__fill--alt { stroke: var(--ink-primary); animation-delay: 0.15s; }
.progress-ring__value { position: relative; z-index: 1; font-size: 0.9rem; font-weight: 500; }
@keyframes ring-fill {
  0%   { stroke-dashoffset: 213.63; }
  100% { stroke-dashoffset: var(--offset, 42.73); }
}
.progress-ring__label { font-size: 0.72rem; color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.05em; }
/* timeline */
.timeline { position: relative; padding-left: 20px; }
.timeline::before {
  content: ''; position: absolute; left: 5px; top: 0; bottom: 0;
  width: 2px; background: linear-gradient(to bottom, var(--accent-soft), var(--accent-amber), transparent);
}
.timeline-item {
  position: relative; padding: var(--spacing-sm) 0 var(--spacing-sm) var(--spacing-md);
}
.timeline-item::before {
  content: ''; position: absolute; left: -16px; top: 16px;
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--accent-soft); border: 3px solid var(--bg-page);
  box-shadow: 0 0 0 2px var(--accent-soft);
}
.timeline-item__title { font-weight: 500; font-size: 0.875rem; }
.timeline-item__meta { font-size: 0.75rem; color: var(--ink-muted); margin-top: 2px; }
/* quick-action buttons */
.action-group {
  display: flex; gap: var(--spacing-sm); flex-wrap: wrap;
}
.action-btn {
  display: inline-flex; align-items: center; gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--bg-glass);
  border: 1px solid rgba(255, 248, 242, 0.4);
  border-radius: var(--radius-pill);
  font-size: 0.85rem; color: var(--ink-secondary);
  cursor: pointer;
  transition: var(--transition-organic);
  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
  animation: action-in 0.5s ease both;
}
.action-btn:nth-child(1) { animation-delay: 0.05s; }
.action-btn:nth-child(2) { animation-delay: 0.12s; }
.action-btn:nth-child(3) { animation-delay: 0.19s; }
.action-btn:nth-child(4) { animation-delay: 0.26s; }
.action-btn:nth-child(5) { animation-delay: 0.33s; }
@keyframes action-in {
  0%   { opacity: 0; transform: scale(0.92) translateY(6px); }
  100% { opacity: 1; transform: none; }
}
.action-btn:hover {
  background: var(--surface-elevated);
  border-color: var(--accent-soft);
  color: var(--ink-primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px var(--glow-highlight);
}
/* priority: merge all @keyframes related to same target */
@keyframes card-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
/* responsive */
@media (max-width: 900px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-content { grid-template-columns: 1fr; }
}
@media (max-width: 520px) {
  .stats-grid { grid-template-columns: 1fr; }
  .progress-row { flex-wrap: wrap; }
  .dash-header { flex-direction: column; align-items: flex-start; gap: var(--spacing-sm); }
}
/* utility: smooth full-page load */
.app-container > * { animation: fade-slide-up 0.7s ease both; }
.app-container > *:nth-child(1) { animation-delay: 0.05s; }
.app-container > *:nth-child(2) { animation-delay: 0.15s; }
.app-container > *:nth-child(3) { animation-delay: 0.25s; }
@keyframes fade-slide-up {
  0%   { opacity: 0; transform: translateY(16px); }
  100% { opacity: 1; transform: none; }
}
---
index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>flow state &mdash; organic dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles/main.css">
</head>
<body>
<div class="blob-decor blob-decor--a"></div>
<div class="blob-decor blob-decor--b"></div>
<div class="blob-decor blob-decor--c"></div>
<div class="app-container">
  <header class="dash-header">
    <h1>flow state</h1>
    <time datetime="2026-06-26">26 june 2026 &middot; week 26</time>
  </header>
  <section class="stats-grid">
    <div class="stat-card">
      <span class="stat-card__icon stat-card__icon--pulse">&#9830;</span>
      <div class="stat-card__value">87</div>
      <div class="stat-card__label">energy</div>
      <div class="stat-card__trend stat-card__trend--up">+4%</div>
    </div>
    <div class="stat-card">
      <span class="stat-card__icon stat-card__icon--pulse2">&#9678;</span>
      <div class="stat-card__value">24m</div>
      <div class="stat-card__label">deep focus</div>
      <div class="stat-card__trend stat-card__trend--up">+12%</div>
    </div>
    <div class="stat-card">
      <span class="stat-card__icon stat-card__icon--pulse3">&#9673;</span>
      <div class="stat-card__value">6.2</div>
      <div class="stat-card__label">mood avg</div>
      <div class="stat-card__trend stat-card__trend--up">+0.4</div>
    </div>
    <div class="stat-card">
      <span class="stat-card__icon stat-card__icon--pulse4">&#9675;</span>
      <div class="stat-card__value">3</div>
      <div class="stat-card__label">journal entries</div>
      <div class="stat-card__trend stat-card__trend--down">-1</div>
    </div>
  </section>
  <div class="dash-content">
    <div class="card">
      <div class="card__title">mood rhythm</div>
      <div class="mood-bar">
        <div class="mood-bar__segment mood-bar__segment--h60" style="--h:60%"></div>
        <div class="mood-bar__segment mood-bar__segment--h75" style="--h:75%"></div>
        <div class="mood-bar__segment mood-bar__segment--h85" style="--h:85%"></div>
        <div class="mood-bar__segment mood-bar__segment--h55" style="--h:55%"></div>
        <div class="mood-bar__segment mood-bar__segment--h70" style="--h:70%"></div>
        <div class="mood-bar__segment mood-bar__segment--h90" style="--h:90%"></div>
        <div class="mood-bar__segment mood-bar__segment--h45" style="--h:45%"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:var(--ink-muted);padding:0 4px;margin-top:-6px">
        <span>mon</span><span>tue</span><span>wed</span><span>thu</span><span>fri</span><span>sat</span><span>sun</span>
      </div>
    </div>
    <div class="card">
      <div class="card__title">recent activity</div>
      <ul class="activity-list">
        <li><span class="activity-dot"></span><span class="activity-text"><strong>Morning reflection</strong> &middot; 12 min</span><span class="activity-time">08:12</span></li>
        <li><span class="activity-dot activity-dot--amber"></span><span class="activity-text"><strong>Deep work block</strong> &middot; focus mode</span><span class="activity-time">09:30</span></li>
        <li><span class="activity-dot activity-dot--core"></span><span class="activity-text"><strong>Walk break</strong> &middot; 15 min outdoors</span><span class="activity-time">11:15</span></li>
        <li><span class="activity-dot"></span><span class="activity-text"><strong>Midday journal</strong> &middot; check-in</span><span class="activity-time">12:40</span></li>
        <li><span class="activity-dot activity-dot--amber"></span><span class="activity-text"><strong>Creative session</strong> &middot; sketching</span><span class="activity-time">14:00</span></li>
      </ul>
    </div>
    <div class="card card--wide">
      <div class="card__title">weekly progress</div>
      <div class="progress-row">
        <div class="progress-ring-wrap">
          <div class="progress-ring">
            <svg class="progress-ring__track" viewBox="0 0 80 80">
              <circle class="progress-ring__bg" cx="40" cy="40" r="34"/>
              <circle class="progress-ring__fill" cx="40" cy="40" r="34" style="--offset:42.73"/>
            </svg>
            <span class="progress-ring__value">80%</span>
          </div>
          <span class="progress-ring__label">focus</span>
        </div>
        <div class="progress-ring-wrap">
          <div class="progress-ring">
            <svg class="progress-ring__track" viewBox="0 0 80 80">
              <circle class="progress-ring__bg" cx="40" cy="40" r="34"/>
              <circle class="progress-ring__fill" cx="40" cy="40" r="34" style="--offset:64.09"/>
            </svg>
            <span class="progress-ring__value">70%</span>
          </div>
          <span class="progress-ring__label">rest</span>
        </div>
        <div class="progress-ring-wrap">
          <div class="progress-ring">
            <svg class="progress-ring__track" viewBox="0 0 80 80">
              <circle class="progress-ring__bg" cx="40" cy="40" r="34"/>
              <circle class="progress-ring__fill progress-ring__fill--alt" cx="40" cy="40" r="34" style="--offset:106.82"/>
            </svg>
            <span class="progress-ring__value">50%</span>
          </div>
          <span class="progress-ring__label">journal</span>
        </div>
        <div class="progress-ring-wrap">
          <div class="progress-ring">
            <svg class="progress-ring__track" viewBox="0 0 80 80">
              <circle class="progress-ring__bg" cx="40" cy="40" r="34"/>
              <circle class="progress-ring__fill progress-ring__fill--alt" cx="40" cy="40" r="34" style="--offset:149.55"/>
            </svg>
            <span class="progress-ring__value">30%</span>
          </div>
          <span class="progress-ring__label">social</span>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card__title">today&rsquo;s timeline</div>
      <div class="timeline">
        <div class="timeline-item"><div class="timeline-item__title">wake + breathe</div><div class="timeline-item__meta">06:30 &middot; 10 min</div></div>
        <div class="timeline-item"><div class="timeline-item__title">journal &amp; intention</div><div class="timeline-item__meta">07:00 &middot; 20 min</div></div>
        <div class="timeline-item"><div class="timeline-item__title">deep work block</div><div class="timeline-item__meta">09:00 &middot; 90 min</div></div>
        <div class="timeline-item"><div class="timeline-item__title">midday reset</div><div class="timeline-item__meta">12:00 &middot; 30 min</div></div>
        <div class="timeline-item"><div class="timeline-item__title">creative flow</div><div class="timeline-item__meta">14:30 &middot; 60 min</div></div>
      </div>
    </div>
    <div class="card">
      <div class="card__title">quick actions</div>
      <div class="action-group">
        <button class="action-btn">+ journal entry</button>
        <button class="action-btn">start focus timer</button>
        <button class="action-btn">log mood</button>
        <button class="action-btn">view insights</button>
        <button class="action-btn">settings</button>
      </div>
      <p style="margin-top:var(--spacing-md);font-size:0.8rem;color:var(--ink-muted)">each action creates a ripple &mdash; small steps shape your day.</p>
    </div>
  </div>
</div>
</body>
</html>