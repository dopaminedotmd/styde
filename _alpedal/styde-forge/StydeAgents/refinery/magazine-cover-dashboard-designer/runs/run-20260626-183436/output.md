STYDE FORGE — MAGAZINE COVER DASHBOARD v6
Fas 0.5 Design Mockup
Blueprint: Magazine Cover Dashboard Designer v1
---
LAYOUT PHILOSOPHY
Every screen is a magazine cover spread. Metrics are headlines. Sections are stories. Whitespace is the binding.
No sidebar. No tabs. Single continuous editorial scroll with a floating masthead.
---
MASTHEAD (persistent top bar, transparent, 48px)
```
+------------------------------------------------------------------+
|  STYDE FORGE          EDITORIAL BOARD      v6.0     ● 14:32 UTC  |
|  ▲ Running            4 engines active     85.3 AVG              |
+------------------------------------------------------------------+
```
Magazine title left-aligned. Status as dateline. Engine count as issue number. Clock as time of press. All uppercased, widely tracked, small caps for secondary.
---
COVER STORY — Hero Metrics Section
Full-bleed width, max 1200px content, enormous scale contrast
```
+------------------------------------------------------------------+
|                                                                   |
|              85.3                                                  |
|              COMPOSITE SCORE                                       |
|              ▲ 2.4 pts from last 60 evals                         |
|                                                                   |
|        ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   |
|        │  1,247   │  │   46     │  │   38     │  │  94.7%   │   |
|        │ AGENTS   │  │ REFINERY │  │ PRODUCE  │  │ UP-TIME  │   |
|        └──────────┘  └──────────┘  └──────────┘  └──────────┘   |
|                                                                   |
+------------------------------------------------------------------+
```
The composite score is the COVER LINE — 64px bold weight, editorial serif (Playfair Display or similar). Smaller numbers below are 18px semibold, treated as secondary cover lines (like "Also in this issue"). The labels are 9px uppercase tracked 3px, like magazine section headers.
---
SECTION ONE — THE AGENCY (agents as editorial contributors)
```
+------------------------------------------------------------------+
|  THE AGENCY                        see page 12 ▸                  |
|  A roster of AI agents in various stages of training              |
|                                                                   |
|  RUNNER: Expert Coder · Production · 92.4 · ████████████ 100%    |
|  BYLINE: v2.1.0 · trained on 47 evals · 32s avg response          |
|                                                                   |
|  Riser: Content Architect · Refinery · 78.1 · ████████░░░ 78%    |
|  BYLINE: v1.3.0 · 18 evals · "showing promise in coherence"      |
|                                                                   |
|  Rookie: Code Reviewer · Refinery · 62.5 · ██████░░░░░ 55%       |
|  BYLINE: v0.9.0 · 6 evals · "needs structural improvements"      |
|                                                                   |
+------------------------------------------------------------------+
```
Each agent is styled like a magazine contributor listing. Large vertical spacing between entries. The XP bar is a gutter rule — thin line with color fill. Agent name is the headline, blueprint is the category, score is the pull-quote number. Teacher diagnosis is the editor's note.
---
SECTION TWO — THE CHARTS (infographic spread)
```
+------------------------------------------------------------------+
|  THE CHARTS                       infographic                     |
|                                                                   |
|  SCORE TREND                                                     |
|                                                                   |
|  █▀▁▂▃▄▅▆▇██▇▆▅▄▃▂▁▀▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▀███▇▆▅▄▃▂▁▀▁▂▃▄▅▆▇██▇      |
|  ↑ Trending upward across last 60 scores                         |
|                                                                   |
|  ┌────────────────────────────┐  ┌────────────────────────────┐  |
|  │  LEADERBOARD               │  │  SYSTEM HEALTH             │  |
|  │  1. Expert Coder     92.4  │  │  CPU ██████░░░░ 62%        │  |
|  │  2. Content Arch.    78.1  │  │  RAM ████████░░ 81%        │  |
|  │  3. Code Reviewer    62.5  │  │  GPU ██████░░░░ 58%        │  |
|  │  4. Prompt Engineer  59.3  │  │  DISK ██░░░░░░░░ 23%       │  |
|  │  5. Data Analyst     48.7  │  │                             │  |
|  └────────────────────────────┘  └────────────────────────────┘  |
|                                                                   |
+------------------------------------------------------------------+
```
Score trend as a sparkline with editorial art treatment. Leaderboard styled as a "Top 10" magazine list. System health as technical specs sidebar.
---
SECTION THREE — THE ENGINE ROOM (for readers who like technical details)
```
+------------------------------------------------------------------+
|  THE ENGINE ROOM                  ⚙️ technical                     |
|                                                                   |
|  4 engines running · 8 python processes                          |
|                                                                   |
|  PID       BLUEPRINT          BENCHMARK           STATUS          |
|  12844     Expert Coder       swe-bench           ● RUNNING      |
|  12892     Content Architect  creative-writing    ● RUNNING      |
|  12931     Code Reviewer      code-review         ● RUNNING      |
|  12967     Prompt Engineer    prompt-craft        ● RUNNING      |
|                                                                   |
|  START ENGINE: [Expert Coder ▾]  [benchmark ▾]  [▶ DEPLOY]      |
|  CONCURRENCY: ●━━━━━○━━━━━━━━━ MAX: 4                            |
|                                                                   |
+------------------------------------------------------------------+
```
Engine control styled as editorial production desk. Tabular layout like a printing press schedule. Start/stop as publishing controls.
---
SECTION FOUR — BENCHMARKS & BLUEPRINTS (the back-of-book reference)
```
+------------------------------------------------------------------+
|  BLUEPRINTS & BENCHMARKS             reference                    |
|                                                                   |
|  BLUEPRINT CATALOG                                                |
|  Expert Coder · v2.0 · swe-bench ▸ 3 versions in production       |
|  Content Architect · v1.3 · creative-writing ▸ 2 in refinery      |
|  Code Reviewer · v0.9 · code-review ▸ rookie                      |
|  Prompt Engineer · v1.1 · prompt-craft ▸ archived                 |
|                                                                   |
|  RECENT CHECKPOINTS                                               |
|  checkpoint-20260626 · loop #47 · "stable expert coder"           |
|  checkpoint-20260625 · loop #42 · "improved architect coherence" |
|  checkpoint-20260624 · loop #38 · "refinery batch complete"       |
|                                                                   |
+------------------------------------------------------------------+
```
Magazine reference section style — small, dense, informative.
---
FOOTER — Colophon
```
+------------------------------------------------------------------+
|  Styde Forge · Issue #1247 · Published by Alpedal                 |
|  Built on Hermes Agent · DeepSeek V4 · Last eval 14:32 UTC       |
|  ● Running · 0.3s TTFB · 94.7% Uptime                            |
+------------------------------------------------------------------+
```
---
TYPOGRAPHY SYSTEM
HEADLINE: Playfair Display 64px/1.0 weight 800 (composite score)
SECTION TITLE: Inter 10px uppercase tracking 3px weight 700 (like magazine department headers)
AGENT NAME: Inter 16px weight 600
METRIC NUMBERS: Inter 22px weight 700
BYLINE TEXT: Inter 11px weight 400, secondary color
BODY: Inter 13px weight 400
COLOR PALETTE (DARK)
bg-page: #050508 (deep almost-black)
bg-card: #0c0c18 (barely lighter)
bg-masthead: rgba(5,5,8,0.85) with backdrop-blur
text-primary: #e0e0ee (not pure white — paper-toned)
text-secondary: #707090 (muted editorial)
text-headline: #ffffff
accent: #6070f0 (editorial accent blue)
accent-alt: #c0a030 (gold for features)
green: #40c868
red: #e05040
border: rgba(255,255,255,0.06) (barely visible)
border-card: rgba(255,255,255,0.03) (almost invisible — rely on whitespace)
WHITESPACE RULES
Section padding: 48px vertical between sections
Card padding: 20px inside
Line height: 1.6 for reading text, 1.0 for headlines
No borders between metrics — use generous gaps (20-24px) instead
Card backgrounds only for data density sections (charts, tables)
Cover metrics float on the page background
---
SPECIAL EFFECTS
Particle canvas: subtle, opacity capped at 0.15, only visible on cover section
Hover state: cards lift 2px with a glow that matches accent color (box-shadow 0 8px 24px rgba(96,112,240,0.12))
Transition speeds: 250ms for any state change
No animations that pulse or shimmer for data elements — magazine aesthetic is static and weighty
Only animation: page load entrance (cards fade in with 100ms stagger)
Score chart bars animate height on data change (600ms ease)
---
RESPONSIVE BREAKPOINTS
>=1200px: Full editorial spread — two-column layout for sections 2-4
900-1199px: Single column, smaller hero (48px headline)
<900px: 32px headline, stacked metrics, hamburger masthead