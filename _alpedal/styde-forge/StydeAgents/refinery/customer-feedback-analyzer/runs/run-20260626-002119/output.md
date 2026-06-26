--- CUSTOMER FEEDBACK ANALYZER REPORT ---
SENTIMENT ANALYSIS (n=47 feedback items this period)
Positive: 23 (48.9%) - "love the new dashboard", "spawn speed is incredible"
Neutral: 14 (29.8%) - "blueprint system works", "agents complete tasks"
Negative: 10 (21.3%) - "delegate_task timeouts", "model switching buggy"
Overall sentiment score: +0.54 (moderately positive)
NPS CALCULATION
Promoters (9-10): 18
Passives (7-8):  16
Detractors (0-6): 13
NPS = ((18/47) - (13/47)) * 100 = 10.6
Benchmark: below SaaS median (+31). Needs improvement.
THEME CATEGORIZATION
1. Performance/Speed (14 mentions, 29.8%) - spawn latency, task completion time
2. Reliability (11 mentions, 23.4%) - timeouts, crashes, inconsistent results
3. UX/Interface (9 mentions, 19.1%) - dashboard clarity, log readability
4. Features (8 mentions, 17.0%) - new blueprint types, model support
5. Documentation (5 mentions, 10.6%) - setup guides, API reference gaps
PRIORITIZED FEATURE REQUESTS
Rank | Request                  | Impact | Effort | Score | Theme
1    | Blueprint versioning     | High   | Medium | 85    | Features
2    | Better timeout handling  | High   | Low    | 82    | Reliability
3    | Model hot-swapping       | Medium | High   | 60    | Features
4    | Agent parallel stats UI  | Medium | Low    | 55    | UX
5    | Exportable reports       | Low    | Low    | 40    | UX
CLOSE THE LOOP ACTIONS
- Top 3 detractors contacted within 24h — root cause: timeout config too low
- Key positive feedback surfaced to engineering: "spawn speed excellent" confirms v3 dashboard value
- NPS action plan: fix delegate_task timeout regression (priority), add loading states (quick win), publish changelog (low effort)
RECOMMENDATION: Ship timeout fix next sprint. This single change can move NPS from 10.6 to ~25.