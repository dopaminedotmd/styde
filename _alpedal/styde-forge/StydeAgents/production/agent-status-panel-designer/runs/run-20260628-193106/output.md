Agent Status Panel v1 — Forge Dashboard Mockup
Panel Layout
Two-layer: top bar (global stats) + scrollable agent grid (cards)
Top Stats Bar
Left: "AGENTS" header + count badge (12)
Center: Running 4 | Pending 3 | Completed 5 | Failed 0 | Total 12
Right: View toggle [Grid] [List] + Sort by: Score v
Agent Card — Grid Mode (default)
+-- 280x160px rounded card -----------------------------+
| [status-dot] agent-id: forge-alpha-07   [score: 94]  |
| iteration: 12/15   loop: parallel batch(2)           |
| [===========           ] 62%  ETA: 4m12s             |
| last score: 94   peak: 96   trend: [+2][+1][-1][+3]  |
| health: stable   focus: blueprint.SkillAgent.v1      |
| actions: [Pause] [View Log] [Promote]                |
+------------------------------------------------------+
Agent Card — List Mode (compact)
[green-dot] forge-alpha-07  94  batch(2)/12/15  62%  ETA 4m   trend +1  stable  [>]
[green-dot] forge-beta-03   87  batch(2)/8/15   53%  ETA 6m   trend 0   stable  [>]
[yellow-dot] forge-gamma-11 71  batch(2)/5/15   33%  ETA 8m   trend -2  warning [>]
[red-dot]    forge-delta-02 45  batch(2)/3/15   20%  ETA --   trend -5  critical[>]
[gray-dot]   forge-epsilon-09 --  queued         --   --       --       idle    [>]
Status Dot Colors
green: active, score >= 80, no errors
yellow: active, score 60-79, or one error this run
red: active, score < 60, or stalled (>2x ETA)
gray: idle / queued / completed
blue: promoted to production
Trend Sparkline Format
[+2][+1][-1][+3] — last 4 deltas from previous iteration score
Color: green if delta >= 0, red if delta < 0
Text alternative: "+1" or "-3" with color-coded unicode arrows if space allows
Health States
stable: normal operation
warning: score drop >20% from peak, or timeout rate >10%
critical: score <60 or no improvement in 3+ iterations
idle: not running (queued or done)
Score Ring (optional compact variant)
Replace numeric score with a 40px circular progress ring.
Arc: green (80-100), yellow (60-79), red (0-59)
Center text: score number
Use only when cards are 200px wide minimum
Layout Breakpoints
Wide (>=1200px): 4-column grid, full card
Medium (800-1199px): 3-column grid, compact card (hide ETA, show only last 2 trend deltas)
Narrow (500-799px): 2-column grid, mini card (score ring, status dot, agent name, health only)
Tiny (<500px): single-column list mode only
Promotion Flow (embedded in panel)
When agent qualifies (3 consecutive >=85):
Card border pulses green (2s animation: box-shadow glow #a6e3a1)
"Promote" button turns from ghost to solid green
Click opens confirmation dialog:
  "Promote forge-alpha-07 to production?
   Current score: 94 | Peak: 96 | Trend: stable
   [Cancel] [Promote]"
Empty State
No agents running:
  +-- centered ------------------------------------+
  |  [icon: robot face]                            |
  |  No active agents                              |
  |  Start a forge run to see agents here          |
  |  [New Run -> forge/blueprints/]                |
  +------------------------------------------------+
Error State
Agent process crashed:
  +-- card with red left border -------------------+
  | [red-dot] forge-delta-02  --                   |
  | CRASHED at iteration 3/15                      |
  | error: IndexError('list index out of range')   |
  | timestamps: started 14:32:01 / crashed 14:34:17|
  | traceback: forge/engine/eval.py:142            |
  | actions: [Restart] [View Log] [Archive]        |
  +------------------------------------------------+
Loading State (panel init)
Shimmer skeleton: 4 card outlines with animated gradient stripes
Duration: until first agent status received (max 3s then force-render)
Color Palette (Catppuccin Mocha)
bg panel: #1e1e2e (base)
bg card: #313244 (surface0)
bg card hover: #45475a (surface1)
border card: #585b70 (surface2)
text primary: #cdd6f4 (text)
text secondary: #a6adc8 (subtext0)
text muted: #585b70 (overlay0)
green dot/score: #a6e3a1 (green)
yellow dot/score: #f9e2af (yellow)
red dot/score: #f38ba8 (red)
blue dot: #89b4fa (blue)
shimmer: gradient(#313244, #45475a, #313244)
Interaction States
Card hover: elevate shadow from 0 2px 6px to 0 4px 12px, cursor pointer
Click card: open agent detail slide-out panel (right side, 400px)
Pause button: icon-only pause icon, toggles to play icon when paused
View Log: opens log viewer modal
Promote: only visible when agent qualifies (3 consecutive >=85)
Accessibility
WCAG 2.1 AA minimum
All status dots have aria-label: "Status: running — score 94 — healthy"
Trend deltas wrapped in aria-label: "Score trend: +2, +1, -1, +3"
Progress bar has role="progressbar" with aria-valuenow="62" aria-valuemin="0" aria-valuemax="100"
All action buttons have aria-labels (e.g. "Pause forge-alpha-07", "View log for forge-alpha-07")
Color is never the only indicator — status dots use shape (circle) + text label
Keyboard nav: arrow keys move between cards, Enter to select, Space to toggle pause
Data Schema
interface AgentStatus {
  id: string;
  status: 'running' | 'pending' | 'completed' | 'failed' | 'idle' | 'promoted';
  loopType: 'sequential' | 'parallel';
  batchSize: number;
  iteration: number;
  totalIterations: number;
  progressPercent: number;
  etaSec: number | null;
  score: number | null;
  peakScore: number | null;
  trend: number[];
  health: 'stable' | 'warning' | 'critical' | 'idle';
  focus: string;
  errors: string[];
  errorCount: number;
  startedAt: string;
  crashedAt: string | null;
}
interface AgentPanelState {
  agents: AgentStatus[];
  viewMode: 'grid' | 'list';
  sortBy: 'score' | 'name' | 'progress' | 'health';
  sortOrder: 'asc' | 'desc';
  filter: 'all' | 'running' | 'completed' | 'failed' | 'idle';
}
API Response Shape
GET /api/forge/agents
{
  "total": 12,
  "running": 4,
  "pending": 3,
  "completed": 5,
  "failed": 0,
  "agents": [
    {
      "id": "forge-alpha-07",
      "status": "running",
      "loopType": "parallel",
      "batchSize": 2,
      "iteration": 12,
      "totalIterations": 15,
      "progressPercent": 62,
      "etaSec": 252,
      "score": 94,
      "peakScore": 96,
      "trend": [2, 1, -1, 3],
      "health": "stable",
      "focus": "blueprint.SkillAgent.v1",
      "errors": [],
      "errorCount": 0,
      "startedAt": "2026-06-28T19:21:00Z",
      "crashedAt": null
    }
  ]
}
Edge Cases
Score null: display "--" and treat health as idle
ETA null (unknown): display "--" or "estimating..." with pulsing dots
Trend empty (first run): display "--" or "no history"
Agent name overflow: truncate with ellipsis at 20 chars, full name in aria-label/tooltip
Zero agents: show empty state
All agents completed: banner at top "All runs complete. [View Results]" + confetti optional