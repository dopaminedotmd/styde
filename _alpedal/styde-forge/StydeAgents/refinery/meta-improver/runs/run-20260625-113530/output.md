Systemic weaknesses found: tool-use enforcement (avg 68), mid-turn steering (avg 71), memory utilization (avg 65). 

Proposed improvements:
1. Add explicit tool-call examples in blueprint templates. Expected impact: +12 tool-use score.
2. Embed out-of-band marker handling in persona files. Expected impact: +9 steering score.
3. Preload memory with active project context. Expected impact: +15 memory score.

Past proposal tracking: 
- Added eval dimension tracking 2026-06-20 → scores improved 7% overall.
- Implemented persona file checks 2026-06-22 → reduced variance 22%.