Existing Onboarding_Flow.md covers the Tauri Dashboard first-run only. It misses CLI Forge onboarding, progressive disclosure, activation metrics, aha moments, tooltips, and checklists. Here is the complete onboarding system.
--- ONBOARDING EXPERIENCE — COMPLETE SPEC ---
## 1. ONBOARDING CHECKLIST FOR NEW USERS
Displayed in Dashboard right panel on first 3 sessions. 5 linear steps.
Step 1: INIT the forge
  hermes forge init
  Creates USB directory tree. Writes state.yaml. Hardware detection runs.
  UNLOCK: forge CLI commands
Step 2: SPAWN your first agent
  hermes forge spawn --blueprint <name> or "Spawn First Agent" button in Dashboard
  Picks the simplest blueprint (onboarding-experience-designer or similar).
  ~30s for agent to produce output.md.
  UNLOCK: refinery directory, agent monitoring, eval pipeline
Step 3: EVAL the output
  hermes forge eval --blueprint <name> or "Evaluate" button
  Self-eval + judge-eval against loaded rubric.
  See score. See what "80/100" means.
  UNLOCK: teacher/improvement loop
Step 4: IMPROVE and checkpoint
  hermes forge improve --blueprint <name>
  Teacher reviews. Saves improved prompt.
  hermes forge checkpoint --blueprint <name>
  Saves state for rollback.
  UNLOCK: loop command, recovery, circuit breaker
Step 5: LOOP
  hermes forge loop --blueprint <name> --iterations 3
  Full automated cycle: spawn -> eval -> improve -> checkpoint -> repeat.
  UNLOCK: batch spawning, production deployment, dashboard analytics
Completion badge: "Forged" — shows on profile. Progress bar updates per step.
## 2. GUIDED PRODUCT TOUR WITH TOOLTIPS
Dashboard tooltip system. 8 tooltip slots, one per panel element. Each tooltip fires once, can be replayed from Help menu. Tooltips stack in lower-right corner if user is mid-task. Dismiss (X), Next (->), or Remind Later (clock icon).
TOOLTIP SLOT 1: Agent Monitor Panel (after first spawn)
  "This is your agent refinery. Each agent you spawn appears here.
  Click any agent to see its score, output, and eval history.
  Agents that score 80+ are promoted to Production."
TOOLTIP SLOT 2: Forge Control Bar (after init)
  "The Forge loop runs here. Start/pause/stop the automated pipeline.
  Iterations, interval, and model selection are configurable."
TOOLTIP SLOT 3: Chat Panel (first chat open)
  "Chat with any configured AI model. Type /skills to see available tools.
  Ctrl+K focuses input. Chat is persistent across sessions."
TOOLTIP SLOT 4: Benchmark Panel (first eval completed)
  "Your agent's benchmark results appear here. Track quality over time
  across multiple spawns. Green = 80+, Yellow = 60-79, Red = <60."
TOOLTIP SLOT 5: Blueprint Catalog (first catalog view)
  "149 blueprints available. Filter by domain (web, data, trading, etc.)
  or search by name. Each blueprint defines a specialist agent persona."
TOOLTIP SLOT 6: System Health (first hardware tab view)
  "Real-time GPU/CPU/memory gauges. Forge auto-adapts to available hardware.
  Thermal auras change color when components run hot."
TOOLTIP SLOT 7: Promotion Ceremony (first agent hitting 80+)
  "Your first production-ready agent! Agents scoring 80+ are promoted.
  Promoted agents are moved to StydeAgents/production/.
  High scores unlock multi-agent collaboration."
TOOLTIP SLOT 8: Settings (first settings open)
  "Configure providers, Hermes path, model defaults, and auto-start behavior.
  Re-run the onboarding wizard from here anytime."
Tooltip state stored in localStorage config under onboarding.tooltips_seen[]. Each tooltip has a version field so doc changes re-trigger.
## 3. PROGRESSIVE FEATURE DISCLOSURE
Features unlock in tiers based on user actions, not time. This prevents overwhelm on first launch.
TIER 0 - WELCOME (state.yaml absent)
  Only visible: "Get Started" splash screen.
  Actions available: Run init.
  Hidden: Everything else.
TIER 1 - INIT DONE (state.yaml exists, 0 agents spawned)
  Revealed: Forge status panel, Settings (basic), System Health.
  Hidden: Agent Monitor (empty state: "Spawn your first agent to see it here"),
          Chat (empty: "Configure a provider in Settings to chat"),
          Benchmarks (empty: "Complete an eval to see data"),
          Blueprint Catalog (show grid but dimmed — "Init complete, ready to spawn"),
          Forge loop controls (show but disabled — "Spawn an agent first").
TIER 2 - FIRST SPAWN (1 agent run exists in refinery)
  Revealed: Agent Monitor list view (1 agent entry),
            Blueprint Catalog fully active,
            Chat (if provider configured).
  Hidden: Eval results (agent not evaluated yet),
          Improve/Teacher loop (eval needed first),
          Loop/automation controls (manual cycle only),
          Production promotion (score unknown),
          Multi-agent features.
TIER 3 - FIRST EVAL (1 eval result exists)
  Revealed: Benchmark Panel (first data point),
            Score display on agent card,
            "Improve" button activates.
  Hidden: Teacher loop (need improvement decision),
          Loop automation (manual improvement first),
          Agent comparison (need multiple agents).
TIER 4 - TEACHER/IMPROVEMENT COMPLETE (improved prompt saved)
  Revealed: "Loop" button activates,
            Checkpoint/Rollback controls,
            Version history on agent detail view.
  Hidden: Batch operations (multiple blueprints).
TIER 5 - PRODUCTION PROMOTION (first agent scores 80+)
  Revealed: Production tab in Monitor,
            Promotion Ceremony animation,
            "Promoted" badge on agent card.
  Hidden: Multi-agent orchestration.
TIER 6 - VETERAN (5+ production agents, 10+ eval runs)
  Revealed: Multi-agent collaboration panel,
            Cross-agent benchmarking,
            Export/Import tools,
            Knowledge management.
  Nothing hidden beyond this point.
Disclosure gating is soft: any feature can be accessed directly via URL/command even if not "revealed." The UI just doesn't show the navigation or button for locked tiers. Users who know the feature exists can use it. Settings always has a "Show all features" toggle to bypass disclosure entirely.
## 4. ACTIVATION METRICS
Core activation event: User successfully spawns, evaluates, and scores 80+ on their first agent within the same session.
METRIC: Time-to-First-Spawn (TTFS)
  Target: < 60 seconds from forge CLI invocation to agent output.
  Measurement: timestamp of spawn command start vs output.md file creation.
  Optimizer: Pre-select simplest blueprint. Pre-warm model cache.
  Display: Dashboard shows "First agent spawned in Xs" badge.
METRIC: Time-to-First-Eval (TTFE)
  Target: < 120 seconds from spawn completion to eval score.
  Measurement: spawn output timestamp vs eval result saved.
  Optimizer: Auto-trigger eval after spawn (no manual step).
  Display: "First evaluation in Xs" on benchmark panel.
METRIC: Time-to-Aha (TTA)
  Definition: Time from first spawn to user seeing a score >= 80 AND the agent output being useful enough to keep.
  Target: < 10 minutes total.
  Aha moment definition: User sees an agent produce output that makes them think "this saves me hours of work."
  Proxy signal: User keeps the agent (no archive/delete), spawns a second agent in a different domain.
METRIC: Activation Rate
  Definition: % of new users who complete the 5-step checklist within 3 days.
  Target: > 60%.
  Tracking: dashboard events logged to timestamped JSON in logs/onboarding_events.json.
METRIC: Feature Adoption Per Tier
  Definition: % of users who reach Tier X who use each feature in that tier at least once.
  Target: > 80% for Tier 1-3, > 50% for Tier 4-6.
  Tracking: Per-feature first-use timestamps in state.onboarding.feature_usage.
METRIC: Drop-off by Step
  Definition: % of users who start but don't complete each checklist step.
  Target: < 20% per step.
  Alerts: If init-to-spawn drop-off exceeds 40%, show inline help.
          If eval-to-improve drop-off exceeds 50%, offer to auto-improve.
METRIC: Re-engagement Rate
  Definition: % of users who return within 7 days of first activation.
  Target: > 40%.
  Trigger: If user spawned agents but hasn't run the loop, Dashboard shows "Your agents are ready. Run the forge loop to improve them."
## 5. AHA MOMENT ACCELERATION
Aha moment = user sees an agent output that is clearly better/faster/cheaper than doing it manually. For Styde Forge the aha is: "I described a specialist and an AI built it and delivered production-quality output in under a minute."
5 accelerators:
ACCELERATOR 1: Cherry-pick the first blueprint
  Don't use alphabetical first blueprint. Use highest-impact, lowest-effort domain for the user.
  Detection: User's shell history, open projects, or explicit domain selection.
  Fallback: "onboarding-experience-designer" — produces a concrete deliverable (an onboarding plan) that any user can immediately evaluate as "useful" or not.
ACCELERATOR 2: Skip the blank startup
  forge spawn --demo
  Launches a pre-canned agent run from cache. User sees a complete output.md immediately without waiting 30s for model inference.
  Then: "That was a demo. Spawn your own to see it work with your context."
ACCELERATOR 3: Live-stream agent thinking
  During spawn, show agent output token-by-token (stream mode).
  Seeing the agent reason through the problem in real-time creates the "it's really working" feeling.
  Fallback: Progress indicator with step labels: "Loading persona... Loading blueprint... Generating output... Done."
ACCELERATOR 4: Instant comparison
  After first eval, show: "Without Styde Forge: 4 hours. With Styde Forge: 47 seconds. That's 306x faster."
  Concrete time-savings calculation based on average human completion time for the task vs actual agent wall-clock time.
  Sources per blueprint domain in config.yaml under meta.savings_estimate_hours.
ACCELERATOR 5: Promote early, promote often
  If first agent scores 70-79, auto-trigger a teacher improvement pass (no user action needed).
  If score climbs to 80+, trigger Promotion Ceremony immediately — even if user hasn't manually clicked "improve" yet.
  The ceremony animation (sparkle effect, fanfare sound, "AGENT PROMOTED TO PRODUCTION" banner) creates emotional attachment to the output.
## 6. TOOLTIP IMPLEMENTATION IN CLI
No GUI? Tooltips still work as CLI hints.
CLI first-run messages (printed once, not repeated):
After forge init:
  NEXT: hermes forge spawn --blueprint <name>
  List available blueprints: hermes forge blueprints
After first forge spawn:
  NEXT: hermes forge eval --blueprint <name>
  See agent output in: StydeAgents/refinery/<name>/runs/<run-id>/output.md
After first forge eval (score displayed):
  SCORE: X/100. Quality gate: 80/100.
  NEXT: hermes forge improve --blueprint <name> (raises score)
  OR: hermes forge checkpoint --blueprint <name> (save this version)
After first improvement:
  Loops: hermes forge loop --blueprint <name> --iterations 3
  This automates everything: spawn -> eval -> improve -> checkpoint
CLI hints respect Caveman Ultra mode: if user has caveman=true in config, hints are 1 line each, no decoration. If caveman=false, hints are 3-4 lines with ascii arrows.
Hint state persisted in state.onboarding.hints_shown[] so hints don't repeat across sessions.
## 7. INTEGRATION POINTS
All onboarding state lives in state.yaml under top-level key:
onboarding:
  version: 2
  started_at: "2026-06-26T00:00:00Z"
  completed_at: null
  checklist:
    init: true
    first_spawn: true
    first_eval: true
    first_improve: false
    first_loop: false
  tier: 3
  activation_metrics:
    ttfs_seconds: 34
    ttfe_seconds: 89
    tta_seconds: null
    aha_moment: false
  tooltips_seen:
    - id: agent-monitor
      version: 1
      seen_at: "2026-06-26T00:01:00Z"
  hints_shown:
    - key: post-spawn-hint
      count: 1
  feature_usage:
    spawn: "2026-06-26T00:00:34Z"
    eval: "2026-06-26T00:01:23Z"
    chat: null
    loop: null
Migration path: Onboarding_Flow.md v1 (Dashboard-only) -> this v2 (Dashboard + CLI + metrics). Existing users who completed Dashboard wizard get tier=6 unlocked and all tooltips marked seen, so no replay for v1 graduates.
---
END. 149 blueprints, ~188 agents, Caveman Ultra. All five skills delivered: Tour (8 tooltip slots), Progressive (6 tiers), Activation (6 metrics), Checklist (5 steps), Aha (5 accelerators).