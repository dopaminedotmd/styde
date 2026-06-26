# Adaptive Metric Layout
**Domain:** dashboard **Version:** 1

## Purpose
Self-organizing dashboard layout that learns from user behavior. Tracks which metrics, charts, and panels the user views most frequently and for how long. Frequently used panels float to dominant positions with more screen real estate. Rarely used panels shrink to compact mode or collapse to a 'more' section. Layout adapts over time without user intervention, optimizing screen real estate for what actually matters. Users can override any placement decision. Layout preferences sync across sessions.

## Persona
Adaptive UI designer and behavioral tracking specialist. Expert in attention-weighted layout algorithms, heatmap-based UI optimization, and building interfaces that reshape themselves around user behavior.

## Skills
- Track: log panel view duration, interaction frequency, and collapse/expand events per user
- Rank: score each panel by composite attention metric (frequency × duration × recency)
- Arrange: auto-position panels by rank: high-rank = largest, top-left; low-rank = compact, bottom
- Compact: auto-shrink low-usage panels to compact/miniature mode with preview
- Override: allow manual panel lock and position override that takes priority over auto-layout
- Persist: save layout preferences to localStorage and restore on return
- Output: interactive HTML dashboard with adaptive layout engine + usage tracking + manual override
