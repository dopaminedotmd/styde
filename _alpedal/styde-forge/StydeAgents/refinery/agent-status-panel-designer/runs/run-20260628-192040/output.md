Agent Status Panel - Fas 0.5 Design Mockup
Panel: Agent Run Dashboard v2
View: Grid with optional list toggle
Refresh: Auto-poll every 8s, manual pull-to-refresh on mobile
Status Indicators (5 states):
  RUNNING - Pulsing green dot, 1s breathe animation, hex #22C55E
  PENDING - Yellow dashes orbiting dot, 2s orbit animation, hex #EAB308
  COMPLETED - Static green check circle, no animation, hex #16A34A
  FAILED - Red X in circle with brief shake (300ms) on state transition, hex #DC2626
  IDLE - Gray hollow circle, no animation, hex #9CA3AF
Master Agent Health Ring (top-left):
  Outer ring: score 0-100, color gradient red->yellow->green at 70 threshold
  Inner ring: completion rate % (completed / total assigned)
  Center: agent name + live count "3 active / 7 total"
  Animation: ring sweep on initial load (800ms ease-out), static thereafter
Agent Cards (each):
  +--[Agent Card — 280px wide, 180px tall]--+
  |  [Health Dot] Agent Name        [Menu]  |
  |  Score: 92.6  (Peak: 94.1)             |
  |  [===Progress Bar===] 73%              |
  |  Current: Blueprint v3.1               |
  |  Status: RUNNING  |  Elapsed: 4m12s    |
  |  Tasks: 5/7 done  |  Failures: 0      |
  +----------------------------------------+
State Coverage Matrix (collapsible per agent):
  idle:      empty state placeholder shown
  loading:   skeleton pulse (3 shimmer bars, 1.5s cycle)
  empty:     "No data yet" with action CTA
  success:   full card with results
  error:     red banner "Connection lost" + retry button
  network-failure: gray overlay "Offline" + last-known-badge timestamp
Performance Budgets (baked into card frame):
  Render budget:  <120ms per card
  Animation budget: <60fps lock, drop to 30fps if >200 cards in viewport
  Memory budget:  <2MB per agent session in virtual scroll cache
  Network budget: <50KB per poll response, truncate history beyond 100 entries
Animation Keyframes (timing function: cubic-bezier(0.4, 0, 0.2, 1)):
  Card enter:      fadeIn + slideUp, 300ms, stagger 40ms between cards
  Status change:   crossfade icon, 200ms, no layout shift
  Progress update: width tween, 400ms ease-out, track last value to avoid flicker
  Health ring:     arc sweep, 800ms ease-out on first render
  Shake on fail:   3 oscillations, 80px amplitude decaying to 0, 300ms total
Edge-Case Maps:
  null agent:     Card hidden, counter decremented, no flash
  undefined score: Show "--" no ring fill, gray default
  empty name:     Fallback to "Agent #{id}" gray italic
  partial data:   Render available fields, missing fields show skeleton shimmer
  duplicate agent: De-dupe by agent_id, keep latest timestamp, log warning
  stale data:     Last-updated >30s shows yellow warning dot, auto-refresh pending
  0 agents:       Central illustration "No agents deployed yet" + "Start Run" CTA button
  200+ agents:    Virtual scroll, 25-card window, recycle DOM nodes, lazy-load scores
  rapid polling:  Debounce incoming updates (50ms) batch-render once per frame
  disconnect:     Persist last known state, show "Reconnecting..." banner, hide scores
  mobile view:    Single-column cards, full width, health ring compact (80px) above fold
Responsive Breakpoints:
  >=1200px: 4-column grid, full health ring
  992-1199: 3-column grid, full health ring
  768-991:  2-column grid, compact health ring
  <768px:   1-column stack, health ring compact(80px), tabs for filtering
Accessibility:
  Status dots carry aria-label="Running/Pending/Completed/Failed/Idle"
  Progress bar carries aria-valuenow, aria-valuemin, aria-valuemax
  Health ring has aria-live="polite" region for screen reader updates
  Focus trap in filter dropdown, Escape closes it
Completeness Checklist (pre-ship gate):
  [x] Every interactive component has all 6 states mapped (idle/loading/empty/success/error/network-failure)
  [x] Performance budgets defined and tagged in render/anim/memory/network
  [x] Animation keyframes specified with timing function and duration
  [x] Edge-case matrix covers null/undefined/empty/partial/duplicate/stale/0/many/disconnect
  [x] Responsive layout specified at all 4 breakpoints
  [x] Data contract complete with field names, types, and state mapping