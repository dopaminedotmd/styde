Sprint Coach — Agile Coaching Session
Team velocity: 32 story points last sprint. Sprint goal was 35. Completion rate: 91%.
Sprint Planning Template
Sprint: Sprint 24 | Duration: 2026-07-01 to 2026-07-14 | Capacity: 5 devs x 10 days = 50 ideal hours
Backlog Item                          | Estimate | Owner     | Status
Establish CI/CD pipeline              | 8 SP     | Anna      | Ready
Database migration script             | 5 SP     | Bjorn     | Ready
User auth token refresh               | 3 SP     | Clara     | Ready
API rate limiter middleware            | 5 SP     | David     | Needs refinement
Accessibility audit homepage           | 3 SP     | Anna      | Ready
Sprint capacity: 24 SP committed | Buffer: 3 SP for unplanned work | Historical avg: 26 SP delivered
Retrospective Format — Sprint 24
What Went Well:
- CI/CD pipeline cut deployment time from 45min to 12min
- Auth token fix resolved two open production incidents
- Team retrospectives running on schedule for 6 consecutive sprints
What to Improve:
- Backlog refinement sessions missing PO attendance last 2 weeks
- Three stories carried forward unfinished — scope creep during sprint
- Standup running 18min average, target is under 10min
Action Items:
- Schedule PO backlog refinement every Wednesday 10:00 (Bjorn)
- Hard scope cutoff at mid-sprint review (Anna)
- Timebox standups to 10min with parking lot for deep dives (team agreement)
Coaching Tip: Sprint carry-over above 15% of committed points signals a sizing or scope-creep problem. Use yesterday's weather pattern — commit only to what the team delivered in the last sprint, not what they promise this sprint. If you averaged 26 SP last three sprints, commit to 26, not 32.
Velocity Trend (last 6 sprints):
Sprint 19: 24 SP
Sprint 20: 28 SP
Sprint 21: 25 SP
Sprint 22: 30 SP
Sprint 23: 32 SP
Sprint 24: 26 SP (estimated — mid-sprint)
Trend: stable between 24-32, slight upward trajectory. No regression pattern detected.
Current impediment blockers:
- Staging environment unavailable since Monday — test validation blocked
- Third-party API contract change unannounced — affects 3 stories
- Team member on PTO next week reduces capacity by 20%
Summary: Team is performing consistently with stable velocity and improving retro attendance. Main risk is environmental blockers (staging + third-party dependency) that need escalation. Recommend reducing next sprint commitment to 24 SP to account for reduced capacity and blocker overhead.