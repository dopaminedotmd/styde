Agent Status Panel Designer v1
Design language:
  Compact card grid -- 3 columns, auto-flow rows
  Each card: 280px wide, 160px tall
  Color palette: status backgrounds, not text colors
  No decorative flourishes -- pure data density
Card anatomy (top to bottom):
[AGENT NAME]     [STATE BADGE]
[ROLE LABEL]
[MODEL TAG]
------------------------------------
SCORE BAR    [###--------] 32/100
HEALTH DOTS  o o o o .    4/5
------------------------------------
JOBS: 7 run  3 pend  12 done
State badge colors:
  IDLE    -- bg:gray, text:white         "IDLE"
  RUNNING -- bg:blue pulse, text:white   "RUN 2/7"
  PENDING -- bg:amber, text:black        "PEND 5"
  FAILED  -- bg:red, text:white          "FAIL"
  DONE    -- bg:green, text:white        "DONE"
Score bar:
  Unscored: [-----....] N/A
  Low:  [##-------] 22/100  bar:red
  Med:  [#####----] 54/100  bar:amber
  High: [########-] 87/100  bar:green
  Peak: [#########] 93/100  bar:green + star char
Health dots -- 5 wide, fixed width:
  Healthy:   o   o   o   o   o   5/5
  Degraded:  o   o   o   .   .   3/5
  Critical:  o   .   .   .   .   1/5
Job counters:
  Format: NN run  NN pend  NN done
  run=blue, pend=amber, done=green
  Zeroes render as 0, not hidden
Dashboard layout:
  Header bar
    "AGENT STATUS"  |  [FILTER: ALL/IDLE/RUNNING/FAILED]  |  HEALTH: 89%
  Grid -- 3 columns, cards flow left-to-right
    Card 1: [candidate-analyzer] [RUN 3/7]
            [Candidate Filtering]
            [gpt-4o]
            [########-] 87/100
            o o o o o  5/5
            7 run  3 pend  12 done
    Card 2: [code-reviewer] [PEND 2]
            [Code Quality]
            [claude-4]
            [#####----] 54/100
            o o o o .  4/5
            0 run  2 pend  8 done
    Card 3: [prompt-engineer] [IDLE]
            [Prompt Design]
            [gpt-4o-mini]
            [-----....] N/A
            o o o . .  3/5
            0 run  0 pend  0 done
    Card 4: [artifact-builder] [FAIL]
            [Blueprint Compile]
            [claude-4]
            [##-------] 22/100
            o . . . .  1/5
            1 run  0 pend  2 done
  Footer
    Summary bar:
    TOTAL: 12 agents  |  RUN: 3  PEND: 5  IDLE: 3  FAIL: 1
    AVG SCORE: 63/100  |  AVG HEALTH: 3.8/5
Empty state:
  No agents configured
  Message: "NO AGENTS. ADD AGENTS IN SETTINGS TO BEGIN."
  Button placeholder: [+ ADD AGENT]
Loading state:
  Card skeletons -- 3 ghost cards with pulse animation
  Each skeleton: gray block rows matching card height
  No text, no icons, just shape silhouette
  [=====]
  [===]
  [================]
  [====  ==]
  o o o o o
Edge cases:
  Agent name overflow: ellipsis at 22 chars, title attr for full name
  Long role label: truncate at 30 chars, no wrap
  Model tag overflow: shrink font, never overflow card
  Score 0/100: show bar empty, text "0/100", no N/A
  Health 0/5: all dots gray, text "0/5"
  Job counter overflow: cap displayed count at 999+, tooltip for exact
Accessibility:
  Status badges include aria-label matching state name
  Score bars have aria-valuenow, aria-valuemin=0, aria-valuemax=100
  Health dots: each dot has aria-label "Healthy" or "Degraded"
  Color is never the only indicator -- text labels accompany all states
  WCAG AA: contrast ratio 4.5:1 on all text, 3:1 on all interactive elements
  Color-blind safe palette: o=checkmark, .=dot, no green/red only states
Build guidance:
  Implementation: React component library, one component per card
  Data source: WebSocket stream from Forge orchestrator
  Refresh: live-updating via SSE, fallback poll every 10s
  Card click: navigates to agent detail view
  Filter dropdown: updates render, no page reload
  Score bar animation: width transitions over 300ms ease-out
  Health dot positions: fixed 12px spacing, monospace character grid