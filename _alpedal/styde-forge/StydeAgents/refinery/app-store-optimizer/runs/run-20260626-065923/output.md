approaching zero-input tasks: single output only, no scaffolding, no synthetic data
task sizing rule added to blueprint: <5 word input = one actionable deliverable
no synthetic benchmarks: omit any metric without a real external source
description rewrite mandate: full rewritten text required inline, not a summary
mandatory research phase added: search volume (SensorTower/AppTweak), competitor keyword gap, Apple guidelines compliance
config.yaml needs ASO API tool access — SensorTower, AppTweak endpoints
blueprint changes applied:
  - section: task sizing / input gating
    content: if agent receives input shorter than 5 words, produce exactly one output actionable in that context — no multi-file scaffolding, no mock data
  - section: evidence rules
    content: any metric, score, or citation must reference a real external data source or be omitted. fabricated benchmarks are a hard violation
  - section: output completeness
    content: any claim of analysis must include the full rewritten result inline
  - section: research preamble before keyword generation
    content: validate search volume, run competitor gap analysis, check Apple App Store guidelines — all before emitting keywords
  - config additions needed:
    aso_research:
      sensortower_api: string
      apptweak_api: string
      enabled: true
three prior feedback rounds addressed.
composite score after corrections: target > 85.