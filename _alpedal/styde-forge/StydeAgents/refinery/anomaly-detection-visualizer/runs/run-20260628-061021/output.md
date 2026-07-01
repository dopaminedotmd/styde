score: 91.4
status: production_ready
weakest_dimension: clarity
cause: Blueprint outputs raw diffs with ANSI escape codes instead of structured human-readable change summary
severity: medium
changes:
  - file: BLUEPRINT.md
    action: add_structured_diff_summary
    description: Add post-processing step that strips ANSI codes and produces bullet-point summary of each change (file, section, delta) before the raw diff block
    impact: high
  - file: BLUEPRINT.md
    action: fix_version_history_default
    description: Ensure version-history append always writes score: 0 or score: null as explicit default when no score provided
    impact: low
  - file: BLUEPRINT.md
    action: consolidate_skills_into_rules
    description: Merge the separate skills list from BLUEPRINT.md into persona.md rules as single source of truth to eliminate redundant token consumption
    impact: high
  - file: config.yaml
    action: add_triminstructions_flag
    description: Add maxtokenprompt or triminstructions flag to strip comment-only metadata lines before injection into agent context
    impact: medium
  - file: persona.md
    action: compress_rules_format
    description: Replace bullet-list examples with compact table or sentence format for rules section keeping same semantic coverage
    impact: medium
edge_cases:
  - condition: "HTML panel exceeds 796 lines"
    behavior: Browser rendering engine clips anomaly pulse animations
    fix: Split output into main panel file and detail overlay file when line count exceeds threshold
  - condition: "Metrics stream exceeds 10000 data points"
    behavior: Live-updating heatmap degrades from 60 fps to sub-10 fps
    fix: Implement automatic downsampling to 2000 points before rendering heatmap slice
  - condition: "Data gap longer than 3 seconds in metric stream"
    behavior: Drift chart must show dashed connector with annotation
    fix: Render dashed connector with tooltip reading 'Data gap -- interpolation paused'
  - condition: "No data within first 10 polling cycles"
    behavior: Dashboard must not crash or show empty state
    fix: Render placeholder state with grey heatmap, 'Awaiting stream...' label, zero pulse rings
  - condition: "Safari 15.x browser"
    behavior: CSS box-shadow with 8 layers collapses after 6 layers
    fix: Emit -webkit- prefixed fallback capping at 6 box-shadow layers, use outline for remaining 2
quick-start:
  header: "# Anomaly Detection Visualizer"
  one_liner: "Run with: forge run anomaly-detection-visualizer"
  output: "anomaly-dashboard.html -- self-contained single-file HTML dashboard"