## Algo Execution Engine — Blueprint Complete
**Blueprint:** algo_execution_engine  
**Domain:** day-trading  
**Persona:** Execution Specialist  
**Core Components:**
**TWAP Slicer** — divides parent order into N equal time slices. Each slice placed at fixed interval. Price drifts with market. Benchmark: arrival price vs executed average.
**VWAP Slicer** — aligns child orders with historical volume profile. Front-loads during high-volume periods. Back-loads during low volume. Benchmark: VWAP of trading day. Slippage = executed avg / market VWAP.
**Iceberg Handler** — displays only 1/N of total size to the market. Refresh trigger: last visible fill, time decay, or passive refresh. Prevents information leakage on large orders.
**Smart Order Router** — maintains venue priority list (cost, latency, fill rate, rebates). Routes each child slice to best venue. Fallback chain on rejection/timeout. Dark pool first for large prints, lit venues for small.
**Execution Quality Dashboard** — metrics per algo run: slippage bps, fill rate %, time to completion, venue distribution, market impact estimate. Taught to agents via ExecutionQualityReport schema.
**Trade-offs hardcoded in persona:**
- Aggression slider: TWAP uses 1.0 (passive) — VWAP uses 1.5 (moderate) — Market uses 3.0 (aggressive)
- Venue selection: cost-sensitive for small orders, liquidity-sensitive for large
- Iceberg display size: parentSize / sqrt(timeSlices) — more slices = smaller visibility
**Agent loop:** receive parent order -> validate -> select algo -> slice -> route child orders -> aggregate fills -> report ExecutionQualityReport -> loop until done.