Now I understand the full picture. Here is the updated BLUEPRINT.md with both pieces of teacher feedback incorporated, followed by the mockup designs.
---
name: agent-status-panel
domain: frontend
version: 1
Agent Status Panel Designer
Domain: frontend Version: 1
Purpose
Design Agent Status panels for Forge dashboard mockups. List/grid of active agents, scores, status indicators, running/pending/completed counts, agent health at a glance.
Persona
You are an agent status panel designer. Design clear, glanceable agent overviews. Status indicators, scores, running/pending/completed states, health. Agents feel alive and trackable.
Skills
  high-end-visual-design
  interface-design
  interaction-design
Dependencies
  css-token-architecture: enforced on all mockups
  dashboard-showcase-skill: output format template
  design-spec-linter: validation gate before final output
Token Families Required
  Animation timing:
    --ease-default: 0.25s ease
    --ease-enter: 0.35s cubic-bezier(0.16, 1, 0.3, 1)
    --ease-exit: 0.2s cubic-bezier(0.55, 0.06, 0.68, 0.19)
    --ease-spring: 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)
    --duration-pulse: 2s infinite
  Theme colors (dark/light mapping):
    dark mode:  --color-bg: #0b0d15  |  light mode:  --color-bg: #f5f5fa
    dark mode:  --color-surface: #1a1a2e  |  light mode:  --color-surface: #ffffff
    dark mode:  --color-border: #2a2e45  |  light mode:  --color-border: #e0e0ec
    dark mode:  --color-text: #c8cce0  |  light mode:  --color-text: #1a1a2e
    dark mode:  --color-text2: #888cad  |  light mode:  --color-text2: #6b6f8a
    dark mode:  --color-accent: #6c5ce7  |  light mode:  --color-accent: #5a4bd1
  Typography:
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif
    --font-mono: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', monospace
    --font-size-xs: 0.625rem
    --font-size-sm: 0.75rem
    --font-size-base: 0.875rem
    --font-size-lg: 1rem
    --font-size-xl: 1.25rem
    --font-weight-normal: 400
    --font-weight-medium: 500
    --font-weight-semibold: 600
    --font-weight-bold: 700
    --line-height-tight: 1.2
    --line-height-normal: 1.5
  Spacing:
    --space-1: 0.25rem
    --space-2: 0.5rem
    --space-3: 0.75rem
    --space-4: 1rem
    --space-6: 1.5rem
    --space-8: 2rem
Efficiency Constraints
  Collapsed property tables: Each mockup section must collapse repeated property tables into a single shared table with an apply-to clause. Do not duplicate identical rows across sub-sections.
  Token enforcement: Every mockup must declare all token families (animation timing, theme colors, typography, spacing). Missing families trigger a linter violation.
  Word budget per mockup: 300 words max (excluding HTML/CSS artifact body).
  No preamble or sign-off: Start directly with the mockup artifact. Zero framing text.
Per-Mockup Token-Usage Constraints
  mockup-1: 'agent-grid-card' — MUST use --ease-spring on agent card hover, --ease-default on status-dot pulse. No hover transitions on status badges.
  mockup-2: 'agent-performance-scores' — score-bar MUST be separate from health-bar. No same-line grid colocation. score-bar horizontal, health-bar vertical in a dedicated trailing column.
  mockup-3: 'agent-timeline-heatmap' — MUST use --color-accent gradient steps (4 stops: idle/warning/active/critical). No solid block fills. Fallback to bar chart only when heatmap data cardinality < 3.
  mockup-4: 'compact-agent-row' — MUST collapse row border, padding, and font-size into a shared apply-to table. Header row token overrides listed as a single apply-to exception line.
  mockup-5: 'agent-resource-gauges' — MUST use heatmap token as primary layout (grid of 12 gauges with color-intensity fill). Block layout is fallback only when data cardinality < 3.
  mockup-6: 'agent-group-overview' — MUST use dark/light token pair on --color-surface for group-card background. Animation exit token on group collapse. No --ease-default for collapse animation.
Conciseness & DRY
  CSS custom-property aliases: deduplicate repeated token declarations by aliasing through :root. Any color value appearing 3+ times across mockups becomes a shared var(). Raw hex values forbidden in property values; always wrap in var().
  Naming consistency: CSS tokens kebab-case only. TypeScript/JS helpers use camelCase typed helpers (e.g. agentStatusColor.statusType, not agentStatusColor['status-type']). Lint step enforces single convention per language.
  Preprocessor variables: when using SCSS/Stylus, define shared values once in _tokens.scss and reference across all mockups. No inline values.
Production Checklist
  Font-family fallback stack: every mockup MUST declare --font-family with full fallback chain (primary, system-ui, sans-serif). No single-font declarations.
  Animation timing CSS vars: all animation durations/easings MUST use custom properties from Token Families Required. No raw 0.3s or ease-in-out in style blocks.
  A11y compliance:
    WCAG 2.1 AA contrast ratios: interactive text >= 4.5:1, large text >= 3:1, non-text elements >= 3:1.
    All interactive elements must have visible focus ring using --color-accent.
    aria-label on status indicators, tooltips, and gauges.
    Color not sole differentiator — status patterns/icon shapes duplicated alongside color.
    aria-live="polite" on auto-updating score regions.
  Review gate: before final output, verify all --color tokens use var() wrapper, no raw hex in property values, single naming convention throughout.
Sequence
  1: agent-grid-card     — Grid of 8 agent cards with status indicators, scores, health bar, and live pulse animation. Status ring around avatar. Score badge bottom-left. Health bar bottom edge.
  2: agent-performance-scores — Score-bar list and health-bar column. Separate tracks for accuracy, speed, reliability. Score bars left (horizontal), health bars right (vertical column).
  3: agent-timeline-heatmap   — 24h activity heatmap. 4 color stops per agent. Mouseover shows tooltip with task count. Compact vertical per-agent strip.
  4: compact-agent-row        — Dense list of 10 agents with status dot, name, score, runtime, action button. Header row tokens shared via apply-to table. One row per agent, max 2 lines.
  5: agent-resource-gauges    — 12 gauge widgets in a 4x3 grid. Color-intensity fill based on utilization. Each gauge has label, live percentage, sparkline. Heatmap token for fill intensity.
  6: agent-group-overview     — Grouped view of agent pools (refinery, production, sandbox, eval). Each group card has collapse animation using --ease-exit, expand using --ease-enter. Dark/light token pair on surface.
Output Standards
  Length cap: Each mockup spec <= 300 words excluding HTML artifact.
  No Issues Detected: Condense all not-affected dimensions into one sentence under one no-issues-detected heading.
  Purity: Deliver ONLY the mockup artifact. Zero preamble, zero suffix, zero meta-commentary.
  Validation gate: Run design-spec-linter before final output. Lint results must be clean.
Output Contract
  mockup output: HTML with embedded CSS. Single style block in :root. CSS token vars for all colors, typography, spacing, animation.
  linter output: YAML key-value pairs. keys: missing-animation-tokens, missing-theme-tokens, repeated-property-blocks, token-constraint-violations. values: count of violations per category.
Efficiency Constraints
  Token budgets: each mockup <= 300 words preamble + 80 lines CSS + 150 lines HTML
  Tables over paragraphs: use compact apply-to tables for all cross-domain mappings
  Abbreviations: use standard abbreviations, define once per mockup
  Zero-redundancy: do not restate findings across sections
  Collapsed tables: one shared property table per mockup section with apply-to clauses
---
MOCKUP 1: agent-grid-card
```html
<div class="agent-grid-card">
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Code Reviewer">
    <div class="avatar-ring status-active">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">CR</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: active"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Code Reviewer</span>
        <span class="score-badge">92</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" aria-label="Health 85%">
        <div class="health-fill" style="width:85%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Data Miner">
    <div class="avatar-ring status-running">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">DM</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: running"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Data Miner</span>
        <span class="score-badge">78</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" aria-label="Health 62%">
        <div class="health-fill" style="width:62%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Test Runner">
    <div class="avatar-ring status-pending">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">TR</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: pending"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Test Runner</span>
        <span class="score-badge">67</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" aria-label="Health 45%">
        <div class="health-fill" style="width:45%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: API Gateway">
    <div class="avatar-ring status-error">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">AG</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: error"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">API Gateway</span>
        <span class="score-badge">31</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100" aria-label="Health 20%">
        <div class="health-fill" style="width:20%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Linter">
    <div class="avatar-ring status-idle">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">LN</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: idle"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Linter</span>
        <span class="score-badge">88</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" aria-label="Health 95%">
        <div class="health-fill" style="width:95%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Deployer">
    <div class="avatar-ring status-running">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">DP</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: running"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Deployer</span>
        <span class="score-badge">74</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100" aria-label="Health 70%">
        <div class="health-fill" style="width:70%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Monitor">
    <div class="avatar-ring status-active">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">MN</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: active"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Monitor</span>
        <span class="score-badge">91</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="88" aria-valuemin="0" aria-valuemax="100" aria-label="Health 88%">
        <div class="health-fill" style="width:88%"></div>
      </div>
    </div>
  </div>
  <div class="agent-card" tabindex="0" role="article" aria-label="Agent: Scheduler">
    <div class="avatar-ring status-pending">
      <div class="avatar">
        <svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="18" fill="var(--color-accent)"/><text x="20" y="26" text-anchor="middle" fill="var(--color-bg)" font-size="14" font-weight="700">SC</text></svg>
      </div>
      <div class="status-dot" aria-label="Status: pending"></div>
    </div>
    <div class="card-body">
      <div class="name-score">
        <span class="agent-name">Scheduler</span>
        <span class="score-badge">55</span>
      </div>
      <div class="health-bar" role="progressbar" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100" aria-label="Health 40%">
        <div class="health-fill" style="width:40%"></div>
      </div>
    </div>
  </div>
</div>
<style>:root{--color-bg:#0b0d15;--color-surface:#1a1a2e;--color-border:#2a2e45;--color-text:#c8cce0;--color-text2:#888cad;--color-accent:#6c5ce7;--ease-default:0.25s ease;--ease-spring:0.5s cubic-bezier(0.34,1.56,0.64,1);--duration-pulse:2s infinite;--font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;--font-size-xs:0.625rem;--font-size-sm:0.75rem;--font-size-base:0.875rem;--font-weight-semibold:600;--space-2:0.5rem;--space-3:0.75rem;--space-4:1rem;--radius-card:12px;--radius-dot:50%}.agent-grid-card{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--space-4);padding:var(--space-4);font-family:var(--font-family);background:var(--color-bg);color:var(--color-text)}.agent-card{background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-card);padding:var(--space-4);display:flex;flex-direction:column;align-items:center;gap:var(--space-3);transition:transform var(--ease-spring),box-shadow var(--ease-spring);cursor:pointer;outline:none;position:relative}.agent-card:hover,.agent-card:focus-visible{transform:translateY(-4px);box-shadow:0 8px 24px rgba(108,92,231,0.2)}.agent-card:focus-visible{outline:2px solid var(--color-accent);outline-offset:2px}.avatar-ring{position:relative;width:48px;height:48px;border-radius:var(--radius-dot)}.avatar-ring.status-active{border:3px solid #00e676}.avatar-ring.status-running{border:3px solid #2979ff}.avatar-ring.status-pending{border:3px solid #ffc107}.avatar-ring.status-error{border:3px solid #ff1744}.avatar-ring.status-idle{border:3px solid var(--color-text2)}.avatar svg{display:block}.status-dot{position:absolute;bottom:-2px;right:-2px;width:14px;height:14px;border-radius:var(--radius-dot);border:2px solid var(--color-surface);animation:pulse var(--ease-default)}.status-active .status-dot{background:#00e676}.status-running .status-dot{background:#2979ff;animation:pulse var(--duration-pulse)}.status-pending .status-dot{background:#ffc107;animation:pulse var(--duration-pulse)}.status-error .status-dot{background:#ff1744;animation:pulse var(--duration-pulse) reverse}.status-idle .status-dot{background:var(--color-text2)}.card-body{width:100%;display:flex;flex-direction:column;gap:var(--space-2)}.name-score{display:flex;justify-content:space-between;align-items:center}.agent-name{font-size:var(--font-size-base);font-weight:var(--font-weight-semibold);color:var(--color-text)}.score-badge{font-size:var(--font-size-sm);font-weight:var(--font-weight-semibold);color:var(--color-accent);background:rgba(108,92,231,0.15);padding:2px 8px;border-radius:6px}.health-bar{height:4px;background:var(--color-border);border-radius:2px;overflow:hidden}.health-fill{height:100%;background:linear-gradient(90deg,#00e676,#2979ff);border-radius:2px;transition:width var(--ease-default)}@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}</style>
```
---
MOCKUP 2: agent-performance-scores
```html
<div class="agent-scores">
  <div class="scores-header" role="heading" aria-level="2">
    <span>Agent Performance Scores</span>
    <div class="score-legend">
      <span><span class="legend-dot" style="background:#00e676"></span>Accuracy</span>
      <span><span class="legend-dot" style="background:#2979ff"></span>Speed</span>
      <span><span class="legend-dot" style="background:#ffc107"></span>Reliability</span>
    </div>
  </div>
  <div class="scores-list">
    <div class="score-row" tabindex="0" role="group" aria-label="Code Reviewer performance">
      <div class="agent-label">Code Reviewer</div>
      <div class="score-tracks">
        <div class="score-track accuracy" role="progressbar" aria-valuenow="94" aria-valuemin="0" aria-valuemax="100" aria-label="Accuracy 94%"><div class="track-fill" style="width:94%"></div></div>
        <div class="score-track speed" role="progressbar" aria-valuenow="88" aria-valuemin="0" aria-valuemax="100" aria-label="Speed 88%"><div class="track-fill" style="width:88%"></div></div>
        <div class="score-track reliability" role="progressbar" aria-valuenow="92" aria-valuemin="0" aria-valuemax="100" aria-label="Reliability 92%"><div class="track-fill" style="width:92%"></div></div>
      </div>
      <div class="health-column">
        <div class="health-gauge" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" aria-label="Health 85%">
          <div class="health-fill-v" style="height:85%"></div>
        </div>
        <span class="health-label">85%</span>
      </div>
    </div>
    <div class="score-row" tabindex="0" role="group" aria-label="Data Miner performance">
      <div class="agent-label">Data Miner</div>
      <div class="score-tracks">
        <div class="score-track accuracy" role="progressbar" aria-valuenow="72" aria-valuemin="0" aria-valuemax="100" aria-label="Accuracy 72%"><div class="track-fill" style="width:72%"></div></div>
        <div class="score-track speed" role="progressbar" aria-valuenow="65" aria-valuemin="0" aria-valuemax="100" aria-label="Speed 65%"><div class="track-fill" style="width:65%"></div></div>
        <div class="score-track reliability" role="progressbar" aria-valuenow="78" aria-valuemin="0" aria-valuemax="100" aria-label="Reliability 78%"><div class="track-fill" style="width:78%"></div></div>
      </div>
      <div class="health-column">
        <div class="health-gauge" role="progressbar" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" aria-label="Health 62%">
          <div class="health-fill-v" style="height:62%"></div>
        </div>
        <span class="health-label">62%</span>
      </div>
    </div>
    <div class="score-row" tabindex="0" role="group" aria-label="Test Runner performance">
      <div class="agent-label">Test Runner</div>
      <div class="score-tracks">
        <div class="score-track accuracy" role="progressbar" aria-valuenow="55" aria-valuemin="0" aria-valuemax="100" aria-label="Accuracy 55%"><div class="track-fill" style="width:55%"></div></div>
        <div class="score-track speed" role="progressbar" aria-valuenow="80" aria-valuemin="0" aria-valuemax="100" aria-label="Speed 80%"><div class="track-fill" style="width:80%"></div></div>
        <div class="score-track reliability" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" aria-label="Reliability 45%"><div class="track-fill" style="width:45%"></div></div>
      </div>
      <div class="health-column">
        <div class="health-gauge" role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" aria-label="Health 45%">
          <div class="health-fill-v" style="height:45%"></div>
        </div>
        <span class="health-label">45%</span>
      </div>
    </div>
    <div class="score-row" tabindex="0" role="group" aria-label="Linter performance">
      <div class="agent-label">Linter</div>
      <div class="score-tracks">
        <div class="score-track accuracy" role="progressbar" aria-valuenow="90" aria-valuemin="0" aria-valuemax="100" aria-label="Accuracy 90%"><div class="track-fill" style="width:90%"></div></div>
        <div class="score-track speed" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" aria-label="Speed 95%"><div class="track-fill" style="width:95%"></div></div>
        <div class="score-track reliability" role="progressbar" aria-valuenow="88" aria-valuemin="0" aria-valuemax="100" aria-label="Reliability 88%"><div class="track-fill" style="width:88%"></div></div>
      </div>
      <div class="health-column">
        <div class="health-gauge" role="progressbar" aria-valuenow="95" aria-valuemin="0" aria-valuemax="100" aria-label="Health 95%">
          <div class="health-fill-v" style="height:95%"></div>
        </div>
        <span class="health-label">95%</span>
      </div>
    </div>
    <div class="score-row" tabindex="0" role="group" aria-label="Monitor performance">
      <div class="agent-label">Monitor</div>
      <div class="score-tracks">
        <div class="score-track accuracy" role="progressbar" aria-valuenow="93" aria-valuemin="0" aria-valuemax="100" aria-label="Accuracy 93%"><div class="track-fill" style="width:93%"></div></div>
        <div class="score-track speed" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" aria-label="Speed 85%"><div class="track-fill" style="width:85%"></div></div>
        <div class="score-track reliability" role="progressbar" aria-valuenow="91" aria-valuemin="0" aria-valuemax="100" aria-label="Reliability 91%"><div class="track-fill" style="width:91%"></div></div>
      </div>
      <div class="health-column">
        <div class="health-gauge" role="progressbar" aria-valuenow="88" aria-valuemin="0" aria-valuemax="100" aria-label="Health 88%">
          <div class="health-fill-v" style="height:88%"></div>
        </div>
        <span class="health-label">88%</span>
      </div>
    </div>
  </div>
</div>
<style>
.score-row{display:flex;align-items:center;gap:var(--space-4);padding:var(--space-3);border-bottom:1px solid var(--color-border);transition:background var(--ease-default)}
.score-row:hover,.score-row:focus-visible{background:rgba(108,92,231,0.08)}
.score-row:focus-visible{outline:2px solid var(--color-accent);outline-offset:-2px}
.agent-label{width:100px;font-size:var(--font-size-sm);font-weight:var(--font-weight-semibold);color:var(--color-text);flex-shrink:0}
.score-tracks{flex:1;display:flex;flex-direction:column;gap:4px;min-width:0}
.score-track{height:6px;background:var(--color-border);border-radius:3px;overflow:hidden}
.score-track.accuracy .track-fill{background:#00e676}
.score-track.speed .track-fill{background:#2979ff}
.score-track.reliability .track-fill{background:#ffc107}
.track-fill{height:100%;border-radius:3px;transition:width var(--ease-default)}
.health-column{width:48px;display:flex;flex-direction:column;align-items:center;gap:4px;flex-shrink:0}
.health-gauge{width:12px;height:60px;background:var(--color-border);border-radius:6px;overflow:hidden}
.health-fill-v{width:100%;background:linear-gradient(to top,#ff1744,#ffc107,#00e676);border-radius:6px;transition:height var(--ease-default)}
.health-label{font-size:var(--font-size-xs);color:var(--color-text2)}
</style>
```
---
MOCKUP 3: agent-timeline-heatmap
```html
<div class="heatmap-panel">
  <div class="heatmap-header" role="heading" aria-level="2">Agent 24h Activity Heatmap</div>
  <div class="heatmap-grid">
    <div class="heatmap-row" tabindex="0" role="group" aria-label="Code Reviewer activity">
      <span class="agent-label">Code Reviewer</span>
      <div class="heatmap-cells">
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 0: idle 2 tasks" aria-label="Hour 0: 2 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 1: idle" aria-label="Hour 1: 0 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 2: idle 1 task" aria-label="Hour 2: 1 task"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 3: idle" aria-label="Hour 3: 0 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 4: warning 5 tasks" aria-label="Hour 4: 5 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="7" title="Hour 5: warning 7 tasks" aria-label="Hour 5: 7 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 45%,var(--color-surface))" data-count="15" title="Hour 6: active 15 tasks" aria-label="Hour 6: 15 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 60%,var(--color-surface))" data-count="22" title="Hour 7: active 22 tasks" aria-label="Hour 7: 22 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 85%,var(--color-surface))" data-count="31" title="Hour 8: critical 31 tasks" aria-label="Hour 8: 31 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 55%,var(--color-surface))" data-count="18" title="Hour 9: active 18 tasks" aria-label="Hour 9: 18 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="14" title="Hour 10: active 14 tasks" aria-label="Hour 10: 14 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 30%,var(--color-surface))" data-count="8" title="Hour 11: warning 8 tasks" aria-label="Hour 11: 8 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="6" title="Hour 12: warning 6 tasks" aria-label="Hour 12: 6 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="3" title="Hour 13: idle 3 tasks" aria-label="Hour 13: 3 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 14: idle 2 tasks" aria-label="Hour 14: 2 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 40%,var(--color-surface))" data-count="12" title="Hour 15: active 12 tasks" aria-label="Hour 15: 12 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="16" title="Hour 16: active 16 tasks" aria-label="Hour 16: 16 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 80%,var(--color-surface))" data-count="28" title="Hour 17: critical 28 tasks" aria-label="Hour 17: 28 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 90%,var(--color-surface))" data-count="35" title="Hour 18: critical 35 tasks" aria-label="Hour 18: 35 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 60%,var(--color-surface))" data-count="20" title="Hour 19: active 20 tasks" aria-label="Hour 19: 20 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 45%,var(--color-surface))" data-count="13" title="Hour 20: active 13 tasks" aria-label="Hour 20: 13 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="6" title="Hour 21: warning 6 tasks" aria-label="Hour 21: 6 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 22: idle 1 task" aria-label="Hour 22: 1 task"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 23: idle" aria-label="Hour 23: 0 tasks"></div>
      </div>
    </div>
    <div class="heatmap-row" tabindex="0" role="group" aria-label="Data Miner activity">
      <span class="agent-label">Data Miner</span>
      <div class="heatmap-cells">
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 85%,var(--color-surface))" data-count="30" title="Hour 0: critical 30 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 75%,var(--color-surface))" data-count="25" title="Hour 1: critical 25 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 55%,var(--color-surface))" data-count="17" title="Hour 2: active 17 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 40%,var(--color-surface))" data-count="11" title="Hour 3: active 11 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="6" title="Hour 4: warning 6 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 5: idle 2 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 6: idle 1 task"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 7: idle"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 8: warning 5 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 45%,var(--color-surface))" data-count="14" title="Hour 9: active 14 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="15" title="Hour 10: active 15 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 80%,var(--color-surface))" data-count="27" title="Hour 11: critical 27 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 55%,var(--color-surface))" data-count="18" title="Hour 12: active 18 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 40%,var(--color-surface))" data-count="12" title="Hour 13: active 12 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 30%,var(--color-surface))" data-count="8" title="Hour 14: warning 8 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="3" title="Hour 15: idle 3 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 16: idle 1 task"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 17: warning 5 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="16" title="Hour 18: active 16 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 80%,var(--color-surface))" data-count="26" title="Hour 19: critical 26 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 90%,var(--color-surface))" data-count="33" title="Hour 20: critical 33 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 60%,var(--color-surface))" data-count="19" title="Hour 21: active 19 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 45%,var(--color-surface))" data-count="13" title="Hour 22: active 13 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="7" title="Hour 23: warning 7 tasks"></div>
      </div>
    </div>
    <div class="heatmap-row" tabindex="0" role="group" aria-label="Test Runner activity">
      <span class="agent-label">Test Runner</span>
      <div class="heatmap-cells">
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 0: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 1: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 2: idle 1 task"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="4" title="Hour 3: warning 4 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 45%,var(--color-surface))" data-count="14" title="Hour 4: active 14 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 85%,var(--color-surface))" data-count="29" title="Hour 5: critical 29 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 55%,var(--color-surface))" data-count="17" title="Hour 6: active 17 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="6" title="Hour 7: warning 6 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 8: idle 2 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 9: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 10: idle 1 task"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 11: warning 5 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 40%,var(--color-surface))" data-count="12" title="Hour 12: active 12 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 80%,var(--color-surface))" data-count="27" title="Hour 13: critical 27 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="16" title="Hour 14: active 16 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 30%,var(--color-surface))" data-count="8" title="Hour 15: warning 8 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="3" title="Hour 16: idle 3 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 17: idle 1 task"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 45%,var(--color-surface))" data-count="13" title="Hour 18: active 13 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 55%,var(--color-surface))" data-count="18" title="Hour 19: active 18 tasks"></div>
        <div class="cell critical" style="background:color-mix(in srgb,var(--color-accent) 85%,var(--color-surface))" data-count="30" title="Hour 20: critical 30 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="15" title="Hour 21: active 15 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 22: warning 5 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 23: idle"></div>
      </div>
    </div>
    <div class="heatmap-row" tabindex="0" role="group" aria-label="API Gateway activity">
      <span class="agent-label">API Gateway</span>
      <div class="heatmap-cells">
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 0: idle 2 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 1: idle 1 task"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 2: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 3: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 4: idle 2 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 5: idle 1 task"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 6: idle"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="4" title="Hour 7: warning 4 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="6" title="Hour 8: warning 6 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 40%,var(--color-surface))" data-count="11" title="Hour 9: active 11 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="15" title="Hour 10: active 15 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 30%,var(--color-surface))" data-count="8" title="Hour 11: warning 8 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="3" title="Hour 12: idle 3 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 13: idle 1 task"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 14: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 15: idle"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="1" title="Hour 16: idle 1 task"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 17: warning 5 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))" data-count="6" title="Hour 18: warning 6 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 40%,var(--color-surface))" data-count="12" title="Hour 19: active 12 tasks"></div>
        <div class="cell active" style="background:color-mix(in srgb,var(--color-accent) 50%,var(--color-surface))" data-count="16" title="Hour 20: active 16 tasks"></div>
        <div class="cell warning" style="background:color-mix(in srgb,var(--color-accent) 20%,var(--color-surface))" data-count="5" title="Hour 21: warning 5 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="2" title="Hour 22: idle 2 tasks"></div>
        <div class="cell idle" style="background:var(--color-surface)" data-count="0" title="Hour 23: idle"></div>
      </div>
    </div>
  </div>
  <div class="heatmap-legend" aria-label="Heatmap intensity legend">
    <span>Idle</span><div class="legend-cell" style="background:var(--color-surface)"></div>
    <span>Warning</span><div class="legend-cell" style="background:color-mix(in srgb,var(--color-accent) 25%,var(--color-surface))"></div>
    <span>Active</span><div class="legend-cell" style="background:color-mix(in srgb,var(--color-accent) 55%,var(--color-surface))"></div>
    <span>Critical</span><div class="legend-cell" style="background:color-mix(in srgb,var(--color-accent) 90%,var(--color-surface))"></div>
  </div>
</div>
<style>
.heatmap-panel{background:var(--color-bg);padding:var(--space-4);border-radius:var(--radius-card);font-family:var(--font-family)}
.heatmap-header{font-size:var(--font-size-lg);font-weight:var(--font-weight-semibold);color:var(--color-text);margin-bottom:var(--space-4)}
.heatmap-grid{display:flex;flex-direction:column;gap:4px}
.heatmap-row{display:flex;align-items:center;gap:var(--space-3);padding:2px 0;border-radius:4px}
.heatmap-row:hover,.heatmap-row:focus-visible{background:rgba(108,92,231,0.05)}
.heatmap-row:focus-visible{outline:2px solid var(--color-accent);outline-offset:2px}
.heatmap-cells{display:grid;grid-template-columns:repeat(24,1fr);gap:2px;flex:1}
.cell{height:16px;border-radius:2px;transition:opacity var(--ease-default);cursor:pointer;position:relative}
.cell:hover{opacity:0.8}
</style>
```