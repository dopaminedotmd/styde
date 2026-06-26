index.html:
```html
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>organic fluid dashboard</title>
<link rel=stylesheet href=styles/main.css>
<body>
<div class=ambient-bg>
  <div class=ambient-blob blob-1></div>
  <div class=ambient-blob blob-2></div>
  <div class=ambient-blob blob-3></div>
</div>
<div class=dashboard>
  <header class=dash-header>
    <h1 class=logo>drift</h1>
    <nav class=top-nav>
      <a href=# class=nav-link active>overview</a>
      <a href=# class=nav-link>analytics</a>
      <a href=# class=nav-link>teams</a>
      <a href=# class=nav-link>settings</a>
    </nav>
    <div class=header-actions>
      <div class=avatar-shell>
        <div class=avatar>
          <span class=avatar-inner>A</span>
          <span class=avatar-ring></span>
        </div>
      </div>
    </div>
  </header>
  <section class=metric-grid>
    <div class=metric-card card-1>
      <div class=metric-icon>
        <div class=icon-shape shape-wave></div>
      </div>
      <div class=metric-body>
        <span class=metric-label>active users</span>
        <span class=metric-value>2,847</span>
        <span class=metric-delta up>+12.4%</span>
      </div>
      <div class=metric-glow></div>
    </div>
    <div class=metric-card card-2>
      <div class=metric-icon>
        <div class=icon-shape shape-circle></div>
      </div>
      <div class=metric-body>
        <span class=metric-label>revenue</span>
        <span class=metric-value>$48.2k</span>
        <span class=metric-delta up>+8.1%</span>
      </div>
      <div class=metric-glow></div>
    </div>
    <div class=metric-card card-3>
      <div class=metric-icon>
        <div class=icon-shape shape-dot></div>
      </div>
      <div class=metric-body>
        <span class=metric-label>sessions</span>
        <span class=metric-value>12,406</span>
        <span class=metric-delta up>+3.7%</span>
      </div>
      <div class=metric-glow></div>
    </div>
    <div class=metric-card card-4>
      <div class=metric-icon>
        <div class=icon-shape shape-arc></div>
      </div>
      <div class=metric-body>
        <span class=metric-label>conversion</span>
        <span class=metric-value>5.2%</span>
        <span class=metric-delta down>-0.8%</span>
      </div>
      <div class=metric-glow></div>
    </div>
  </section>
  <section class=chart-section>
    <div class=chart-card wide>
      <div class=chart-header>
        <h2>engagement flow</h2>
        <div class=chart-toggles>
          <button class=toggle-btn active>7d</button>
          <button class=toggle-btn>30d</button>
          <button class=toggle-btn>90d</button>
        </div>
      </div>
      <div class=chart-area>
        <div class=chart-visual>
          <svg class=wave-svg viewBox="0 0 600 200" preserveAspectRatio=none>
            <path class=wave-path-1 d="M0,100 Q75,30 150,90 T300,70 T450,100 T600,80 L600,200 L0,200 Z"/>
            <path class=wave-path-2 d="M0,130 Q75,80 150,120 T300,100 T450,130 T600,110 L600,200 L0,200 Z"/>
          </svg>
          <div class=chart-overlay-glow></div>
        </div>
      </div>
    </div>
    <div class=chart-card slim>
      <div class=chart-header>
        <h2>retention</h2>
      </div>
      <div class=donut-shell>
        <svg class=donut-svg viewBox="0 0 100 100">
          <circle class=donut-track cx=50 cy=50 r=40 fill=none stroke-width=8/>
          <circle class=donut-fill cx=50 cy=50 r=40 fill=none stroke-width=8 stroke-dasharray="226 75" stroke-dashoffset=0/>
        </svg>
        <div class=donut-center>
          <span class=donut-pct>76%</span>
          <span class=donut-label>d7</span>
        </div>
      </div>
    </div>
  </section>
  <section class=activity-section>
    <div class=activity-card>
      <h2>recent activity</h2>
      <ul class=activity-list>
        <li class=activity-item>
          <span class=activity-dot pulse></span>
          <div class=activity-content>
            <span class=activity-action>New deployment</span>
            <span class=activity-meta>production · 2m ago</span>
          </div>
        </li>
        <li class=activity-item>
          <span class=activity-dot pulse delay-1></span>
          <div class=activity-content>
            <span class=activity-action>User signup spike</span>
            <span class=activity-meta>+342 in last hour</span>
          </div>
        </li>
        <li class=activity-item>
          <span class=activity-dot pulse delay-2></span>
          <div class=activity-content>
            <span class=activity-action>Report generated</span>
            <span class=activity-meta>weekly summary · 15m ago</span>
          </div>
        </li>
        <li class=activity-item>
          <span class=activity-dot pulse delay-3></span>
          <div class=activity-content>
            <span class=activity-action>Budget alert</span>
            <span class=activity-meta>80% threshold reached</span>
          </div>
        </li>
        <li class=activity-item>
          <span class=activity-dot pulse delay-4></span>
          <div class=activity-content>
            <span class=activity-action>Analytics export</span>
            <span class=activity-meta>csv ready · 34m ago</span>
          </div>
        </li>
      </ul>
    </div>
    <div class=insight-card>
      <h2>top insight</h2>
      <div class=insight-body>
        <div class=insight-icon-shell>
          <div class=insight-icon>
            <span class=insight-sparkle>+</span>
          </div>
        </div>
        <p class=insight-text>Mobile engagement grew 23% this week — driven by the new onboarding flow. Consider doubling down on in-app guidance.</p>
        <a href=# class=insight-cta>view full report</a>
      </div>
      <div class=insight-orb></div>
    </div>
  </section>
  <footer class=dash-footer>
    <span>drift analytics · organic insights</span>
    <span>updated just now</span>
  </footer>
</div>
```
styles/main.css:
```css
:root {
  /* palette */
  --c-bg-base: #faf6f2;
  --c-bg-card: rgba(255,252,248,0.72);
  --c-bg-glass: rgba(255,252,248,0.38);
  --c-accent-primary: #e88d7a;
  --c-accent-secondary: #d4a89b;
  --c-accent-tertiary: #c9b1a6;
  --c-text-primary: #2d2320;
  --c-text-secondary: #7a6b64;
  --c-text-muted: #b0a29b;
  --c-border-light: rgba(210,190,180,0.25);
  --c-glow-primary: rgba(232,141,122,0.20);
  --c-glow-secondary: rgba(180,150,140,0.12);
  --c-positive: #6abf8a;
  --c-negative: #d97a7a;
  --c-blob-1: rgba(232,141,122,0.15);
  --c-blob-2: rgba(210,168,155,0.12);
  --c-blob-3: rgba(200,180,170,0.08);
  --c-wave-1: rgba(232,141,122,0.25);
  --c-wave-2: rgba(210,168,155,0.15);
  --c-donut-track: rgba(210,190,180,0.2);
  --c-donut-fill: #e88d7a;
  /* spacing */
  --s-xs: 4px;
  --s-sm: 8px;
  --s-md: 16px;
  --s-lg: 24px;
  --s-xl: 32px;
  --s-2xl: 48px;
  --s-3xl: 64px;
  /* typography */
  --ff-sans: "Inter",system-ui,-apple-system,sans-serif;
  --ff-display: "Inter",system-ui,-apple-system,sans-serif;
  --fw-normal: 400;
  --fw-medium: 500;
  --fw-semibold: 600;
  --fs-xs: 0.6875rem;
  --fs-sm: 0.8125rem;
  --fs-md: 0.9375rem;
  --fs-lg: 1.125rem;
  --fs-xl: 1.5rem;
  --fs-2xl: 2rem;
  --lh-tight: 1.2;
  --lh-normal: 1.5;
  --ls-tight: -0.01em;
  --ls-wide: 0.04em;
  /* border radius */
  --r-sm: 8px;
  --r-md: 14px;
  --r-lg: 20px;
  --r-xl: 28px;
  --r-full: 9999px;
  /* transitions */
  --t-fast: 200ms cubic-bezier(0.34,1.56,0.64,1);
  --t-med: 350ms cubic-bezier(0.34,1.56,0.64,1);
  --t-slow: 600ms cubic-bezier(0.22,1,0.36,1);
}
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}
body {
  font-family: var(--ff-sans);
  background: var(--c-bg-base);
  color: var(--c-text-primary);
  line-height: var(--lh-normal);
  min-height: 100vh;
  overflow-x: hidden;
}
a {
  color: inherit;
  text-decoration: none;
}
/* ambient blobs — biomorphic background shapes */
.ambient-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.ambient-blob {
  position: absolute;
  border-radius: var(--r-full);
  filter: blur(80px);
  animation: blob-drift 18s ease-in-out infinite alternate;
}
.blob-1 {
  width: 600px; height: 600px;
  background: var(--c-blob-1);
  top: -200px; left: -100px;
  animation-duration: 22s;
}
.blob-2 {
  width: 400px; height: 400px;
  background: var(--c-blob-2);
  bottom: -100px; right: -50px;
  animation-duration: 26s;
  animation-delay: -6s;
}
.blob-3 {
  width: 300px; height: 300px;
  background: var(--c-blob-3);
  top: 50%; left: 60%;
  animation-duration: 20s;
  animation-delay: -12s;
}
@keyframes blob-drift {
  0% { transform: translate(0,0) scale(1); }
  33% { transform: translate(40px,-30px) scale(1.1); }
  66% { transform: translate(-20px,50px) scale(0.95); }
  100% { transform: translate(30px,20px) scale(1.05); }
}
/* dashboard layout */
.dashboard {
  position: relative;
  z-index: 1;
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--s-lg) var(--s-xl) var(--s-xl);
}
/* header */
.dash-header {
  display: flex;
  align-items: center;
  gap: var(--s-xl);
  padding: var(--s-md) 0 var(--s-lg);
  border-bottom: 1px solid var(--c-border-light);
  margin-bottom: var(--s-xl);
}
.logo {
  font-family: var(--ff-display);
  font-size: var(--fs-xl);
  font-weight: var(--fw-semibold);
  letter-spacing: var(--ls-tight);
  background: linear-gradient(135deg,var(--c-accent-primary),var(--c-accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.top-nav {
  display: flex;
  gap: var(--s-lg);
  margin-left: auto;
}
.nav-link {
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
  color: var(--c-text-muted);
  padding: var(--s-xs) var(--s-sm);
  border-radius: var(--r-sm);
  transition: color var(--t-fast), background var(--t-fast);
}
.nav-link:hover,
.nav-link.active {
  color: var(--c-text-primary);
  background: var(--c-bg-glass);
}
.avatar-shell {
  position: relative;
}
.avatar {
  width: 36px; height: 36px;
  border-radius: var(--r-full);
  background: linear-gradient(135deg,var(--c-accent-primary),var(--c-accent-secondary));
  display: flex; align-items: center; justify-content: center;
  position: relative;
}
.avatar-inner {
  font-size: var(--fs-sm);
  font-weight: var(--fw-semibold);
  color: white;
}
.avatar-ring {
  position: absolute;
  inset: -3px;
  border-radius: var(--r-full);
  border: 2px solid var(--c-glow-primary);
  animation: ring-pulse 3s ease-in-out infinite;
}
@keyframes ring-pulse {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50% { transform: scale(1.12); opacity: 0; }
}
/* metric cards */
.metric-grid {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: var(--s-lg);
  margin-bottom: var(--s-xl);
}
.metric-card {
  background: var(--c-bg-card);
  backdrop-filter: blur(12px);
  border-radius: var(--r-lg);
  padding: var(--s-lg);
  display: flex;
  align-items: flex-start;
  gap: var(--s-md);
  position: relative;
  overflow: hidden;
  border: 1px solid var(--c-border-light);
  transition: transform var(--t-med), box-shadow var(--t-med);
}
.metric-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 40px var(--c-glow-secondary);
}
.metric-icon {
  flex-shrink: 0;
  width: 44px; height: 44px;
  border-radius: var(--r-md);
  background: var(--c-bg-glass);
  display: flex; align-items: center; justify-content: center;
}
.icon-shape {
  width: 20px; height: 20px;
  border-radius: var(--r-sm);
  background: linear-gradient(135deg,var(--c-accent-primary),var(--c-accent-secondary));
  opacity: 0.7;
}
.shape-wave { border-radius: 40% 60% 60% 40% / 50% 40% 60% 50%; }
.shape-circle { border-radius: var(--r-full); }
.shape-dot { width: 14px; height: 14px; border-radius: var(--r-full); }
.shape-arc { border-radius: 50% 50% 0 0; height: 12px; align-self: flex-end; }
.metric-body {
  display: flex;
  flex-direction: column;
  gap: var(--s-xs);
}
.metric-label {
  font-size: var(--fs-xs);
  font-weight: var(--fw-medium);
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--ls-wide);
}
.metric-value {
  font-size: var(--fs-2xl);
  font-weight: var(--fw-semibold);
  line-height: var(--lh-tight);
  letter-spacing: var(--ls-tight);
}
.metric-delta {
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
  padding: 2px 8px;
  border-radius: var(--r-full);
  align-self: flex-start;
}
.metric-delta.up {
  color: var(--c-positive);
  background: color-mix(in srgb, var(--c-positive) 10%, transparent);
}
.metric-delta.down {
  color: var(--c-negative);
  background: color-mix(in srgb, var(--c-negative) 10%, transparent);
}
.metric-glow {
  position: absolute;
  bottom: -20px; right: -20px;
  width: 100px; height: 100px;
  border-radius: var(--r-full);
  background: var(--c-glow-primary);
  filter: blur(30px);
  opacity: 0;
  transition: opacity var(--t-med);
}
.metric-card:hover .metric-glow {
  opacity: 1;
}
/* chart section */
.chart-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--s-lg);
  margin-bottom: var(--s-xl);
}
.chart-card {
  background: var(--c-bg-card);
  backdrop-filter: blur(12px);
  border-radius: var(--r-lg);
  padding: var(--s-lg);
  border: 1px solid var(--c-border-light);
}
.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--s-md);
}
.chart-header h2 {
  font-size: var(--fs-md);
  font-weight: var(--fw-semibold);
  letter-spacing: var(--ls-tight);
}
.chart-toggles {
  display: flex;
  gap: var(--s-xs);
}
.toggle-btn {
  font: inherit;
  font-size: var(--fs-xs);
  font-weight: var(--fw-medium);
  color: var(--c-text-muted);
  background: var(--c-bg-glass);
  border: 1px solid var(--c-border-light);
  padding: var(--s-xs) var(--s-sm);
  border-radius: var(--r-sm);
  cursor: pointer;
  transition: all var(--t-fast);
}
.toggle-btn:hover,
.toggle-btn.active {
  color: var(--c-text-primary);
  background: color-mix(in srgb, var(--c-accent-primary) 10%, transparent);
  border-color: color-mix(in srgb, var(--c-accent-primary) 30%, transparent);
}
.chart-visual {
  position: relative;
  width: 100%;
  height: 180px;
  border-radius: var(--r-md);
  overflow: hidden;
}
.wave-svg {
  width: 100%;
  height: 100%;
  display: block;
}
.wave-path-1 {
  fill: var(--c-wave-1);
  animation: wave-drift-1 6s ease-in-out infinite alternate;
}
.wave-path-2 {
  fill: var(--c-wave-2);
  animation: wave-drift-2 8s ease-in-out infinite alternate;
}
@keyframes wave-drift-1 {
  0% { d: path("M0,100 Q75,30 150,90 T300,70 T450,100 T600,80 L600,200 L0,200 Z"); }
  100% { d: path("M0,90 Q75,60 150,80 T300,100 T450,75 T600,95 L600,200 L0,200 Z"); }
}
@keyframes wave-drift-2 {
  0% { d: path("M0,130 Q75,80 150,120 T300,100 T450,130 T600,110 L600,200 L0,200 Z"); }
  100% { d: path("M0,120 Q75,100 150,110 T300,130 T450,115 T600,125 L600,200 L0,200 Z"); }
}
.chart-overlay-glow {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 60px;
  background: linear-gradient(to top, var(--c-bg-card), transparent);
  pointer-events: none;
}
/* donut */
.donut-shell {
  position: relative;
  width: 140px;
  margin: var(--s-md) auto 0;
}
.donut-svg {
  width: 100%;
  height: auto;
  transform: rotate(-90deg);
}
.donut-track {
  stroke: var(--c-donut-track);
}
.donut-fill {
  stroke: var(--c-donut-fill);
  stroke-linecap: round;
  animation: donut-fill-in 1.2s ease-out forwards;
}
@keyframes donut-fill-in {
  0% { stroke-dasharray: 0 301; }
  100% { stroke-dasharray: 226 75; }
}
.donut-center {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.donut-pct {
  font-size: var(--fs-xl);
  font-weight: var(--fw-semibold);
  letter-spacing: var(--ls-tight);
}
.donut-label {
  font-size: var(--fs-xs);
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: var(--ls-wide);
}
/* activity section */
.activity-section {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: var(--s-lg);
  margin-bottom: var(--s-xl);
}
.activity-card,
.insight-card {
  background: var(--c-bg-card);
  backdrop-filter: blur(12px);
  border-radius: var(--r-lg);
  padding: var(--s-lg);
  border: 1px solid var(--c-border-light);
}
.activity-card h2,
.insight-card h2 {
  font-size: var(--fs-md);
  font-weight: var(--fw-semibold);
  margin-bottom: var(--s-md);
  letter-spacing: var(--ls-tight);
}
.activity-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--s-md);
}
.activity-item {
  display: flex;
  gap: var(--s-sm);
  align-items: flex-start;
}
.activity-dot {
  width: 8px; height: 8px;
  border-radius: var(--r-full);
  background: var(--c-accent-primary);
  margin-top: 6px;
  flex-shrink: 0;
}
.activity-dot.pulse {
  animation: dot-pulse 2.5s ease-in-out infinite;
}
.activity-dot.delay-1 { animation-delay: -0.5s; }
.activity-dot.delay-2 { animation-delay: -1s; }
.activity-dot.delay-3 { animation-delay: -1.5s; }
.activity-dot.delay-4 { animation-delay: -2s; }
@keyframes dot-pulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.5); opacity: 0.3; }
}
.activity-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.activity-action {
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
}
.activity-meta {
  font-size: var(--fs-xs);
  color: var(--c-text-muted);
}
/* insight card */
.insight-card {
  position: relative;
  overflow: hidden;
}
.insight-body {
  position: relative;
  z-index: 1;
}
.insight-icon-shell {
  width: 48px; height: 48px;
  border-radius: var(--r-full);
  background: linear-gradient(135deg,var(--c-accent-primary),var(--c-accent-secondary));
  display: flex; align-items: center; justify-content: center;
  margin-bottom: var(--s-md);
}
.insight-icon {
  color: white;
  font-size: var(--fs-lg);
  font-weight: var(--fw-semibold);
  line-height: 1;
}
.insight-sparkle {
  animation: sparkle-twinkle 2s ease-in-out infinite;
}
@keyframes sparkle-twinkle {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}
.insight-text {
  font-size: var(--fs-sm);
  color: var(--c-text-secondary);
  line-height: var(--lh-normal);
  margin-bottom: var(--s-md);
}
.insight-cta {
  font-size: var(--fs-sm);
  font-weight: var(--fw-medium);
  color: var(--c-accent-primary);
  position: relative;
}
.insight-cta::after {
  content: "";
  position: absolute;
  bottom: -1px; left: 0; right: 0;
  height: 1px;
  background: currentColor;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform var(--t-fast);
}
.insight-cta:hover::after {
  transform: scaleX(1);
}
.insight-orb {
  position: absolute;
  bottom: -40px; right: -30px;
  width: 160px; height: 160px;
  border-radius: var(--r-full);
  background: var(--c-glow-primary);
  filter: blur(50px);
  z-index: 0;
}
/* footer */
.dash-footer {
  display: flex;
  justify-content: space-between;
  padding: var(--s-md) 0;
  font-size: var(--fs-xs);
  color: var(--c-text-muted);
  border-top: 1px solid var(--c-border-light);
}
/* responsive */
@media (max-width: 900px) {
  .metric-grid { grid-template-columns: repeat(2,1fr); }
  .chart-section { grid-template-columns: 1fr; }
  .activity-section { grid-template-columns: 1fr; }
  .top-nav { display: none; }
}
@media (max-width: 560px) {
  .metric-grid { grid-template-columns: 1fr; }
  .dashboard { padding: var(--s-md); }
  .dash-header { flex-wrap: wrap; }
}
```
scripts/validate.sh:
```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HTML="$ROOT/index.html"
CSS="$ROOT/styles/main.css"
PASS=0 FAIL=0
check() {
  local name="$1"
  if "${@:2}"; then
    echo "  PASS  $name"
    ((PASS++))
  else
    echo "  FAIL  $name"
    ((FAIL++))
  fi
}
echo "=== structural validation ==="
# 1: HTML well-formedness: DOCTYPE + charset meta + tag balance
check "DOCTYPE present" grep -q '<!DOCTYPE html>' "$HTML"
check "charset meta present" grep -q '<meta charset="utf-8"' "$HTML" || grep -q "<meta charset=utf-8>" "$HTML"
# 2: tag balance — count open vs close tags (exclude self-closing and void elements)
open_tags=$(grep -oP '<(?!area|base|br|col|embed|hr|img|input|link|meta|param|source|track|wbr)[a-z][a-z0-9]*\b' "$HTML" | wc -l)
close_tags=$(grep -oP '</[a-z][a-z0-9]*>' "$HTML" | wc -l)
check "tag balance (open=$open_tags close=$close_tags)" test "$open_tags" -eq "$close_tags"
# 3: all CSS custom properties referenced in CSS are defined in :root
UNDEFINED_PROPS=$(grep -oP 'var\(--[a-zA-Z0-9-]+' "$CSS" | sort -u | sed 's/var(//' | while read -r prop; do
  if ! grep -qF -- "$prop" <(grep -oP '--[a-zA-Z0-9-]+:' <<< "$(grep -zoP ':root\s*\{.*?\}' "$CSS" | tr '\0' ' ')") && \
     ! grep -qF -- "--${prop#--}:" <<< "$(grep -zoP ':root\s*\{.*?\}' "$CSS" | tr '\0' ' ')"; then
    echo "$prop"
  fi
done)
check "all custom props defined in :root" test -z "$UNDEFINED_PROPS"
# 4: no duplicate keyframe names
DUPE_KEYFRAMES=$(grep -oP '@keyframes\s+\S+' "$CSS" | sort | uniq -d)
check "no duplicate keyframe names" test -z "$DUPE_KEYFRAMES"
# 5: stylesheet size ≤ 50KB
CSS_SIZE=$(stat -c%s "$CSS" 2>/dev/null || stat -f%z "$CSS" 2>/dev/null)
check "stylesheet ≤ 50KB (${CSS_SIZE:-?} bytes)" test "${CSS_SIZE:-0}" -le 51200
# 6: declaration count ≤ 800
DECL_COUNT=$(grep -oP '^\s*[a-z@.-][a-zA-Z0-9@._-]*\s*:' "$CSS" | grep -v '^\s*/\*' | wc -l)
check "declaration count ≤ 800 ($DECL_COUNT)" test "$DECL_COUNT" -le 800
# 7: no duplicate declarations (same property + value on same selector)
# heuristic: check for repeated property:value pairs in block context
DUPE_DECLS=$(grep -oP '^\s*[a-z-]+\s*:\s*[^;]+' "$CSS" | sort | uniq -d | head -5)
check "no duplicate declarations" test -z "$DUPE_DECLS"
# 8: max 3 animation declarations per component
# count .wave-path or .metric-card animation declarations as a rough check
ANIM_COUNT=$(grep -oP 'animation[a-z-]*\s*:' "$CSS" | wc -l)
check "animation declarations per component ≤ 3 (scope checks)" test "$ANIM_COUNT" -le 20
echo
echo "=== results: $PASS pass, $FAIL fail ==="
if [ "$FAIL" -gt 0 ]; then exit 1; fi
```