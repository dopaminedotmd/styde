┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\version-diff-visualizer\config.yaml → b/StydeAgents\blueprints\version-diff-visualizer\config.yaml[0m
[38;2;139;134;130m@@ -1,21 +1,52 @@[0m
[38;2;184;134;11m blueprint:[0m
[38;2;184;134;11m   name: version-diff-visualizer[0m
[38;2;255;255;255;48;2;19;87;20m+  domain: frontend[0m
[38;2;184;134;11m   version: 1.0.0[0m
[38;2;255;255;255;48;2;119;20;20m-  domain: frontend[0m
[38;2;255;255;255;48;2;119;20;20m-  last_reviewed: '2026-06-26'[0m
[38;2;255;255;255;48;2;119;20;20m-  review_interval_days: 90[0m
[38;2;255;255;255;48;2;119;20;20m-  dependencies: [][0m
[38;2;255;255;255;48;2;119;20;20m-  schema_expectations: [][0m
[38;2;255;255;255;48;2;119;20;20m-  version_history: [][0m
[38;2;255;255;255;48;2;19;87;20m+  version_history:[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: null[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 1.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'INIT: initial blueprint creation'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T00:00:00Z'[0m
[38;2;255;255;255;48;2;19;87;20m+enabled: true[0m
[38;2;255;255;255;48;2;19;87;20m+namespace: forge.version-diff[0m
[38;2;184;134;11m agent:[0m
[38;2;184;134;11m   max_iterations: 10[0m
[38;2;255;255;255;48;2;19;87;20m+  retry_on_failure: true[0m
[38;2;184;134;11m   timeout_seconds: 300[0m
[38;2;255;255;255;48;2;119;20;20m-  retry_on_failure: true[0m
[38;2;184;134;11m   toolsets:[0m
[38;2;184;134;11m   - terminal[0m
[38;2;184;134;11m   - file[0m
[38;2;255;255;255;48;2;119;20;20m-  - web[0m
[38;2;184;134;11m eval:[0m
[38;2;255;255;255;48;2;19;87;20m+  min_pass_score: 70[0m
[38;2;255;255;255;48;2;19;87;20m+  judge_model: deepseek-v4-pro[0m
[38;2;184;134;11m   benchmarks: [][0m
[38;2;255;255;255;48;2;119;20;20m-  judge_model: deepseek-v4-pro[0m
[38;2;255;255;255;48;2;119;20;20m-  min_pass_score: 70[0m
[38;2;255;255;255;48;2;19;87;20m+hardware_profiles:[0m
[38;2;255;255;255;48;2;19;87;20m+  pontus-main:[0m
[38;2;255;255;255;48;2;19;87;20m+    model: deepseek-v4-flash[0m
[38;2;255;255;255;48;2;19;87;20m+    provider: deepseek[0m
[38;2;255;255;255;48;2;19;87;20m+    temperature: 0.3[0m
[38;2;255;255;255;48;2;19;87;20m+    max_tokens: 8192[0m
[38;2;255;255;255;48;2;19;87;20m+    eval_model: deepseek-v4-pro[0m
[38;2;255;255;255;48;2;19;87;20m+default_view: unified[0m
[38;2;255;255;255;48;2;19;87;20m+max_score: 100[0m
[38;2;255;255;255;48;2;19;87;20m+diff_colors:[0m
[38;2;255;255;255;48;2;19;87;20m+  addition: '#22c55e'[0m
[38;2;255;255;255;48;2;19;87;20m+  removal: '#ef4444'[0m
[38;2;255;255;255;48;2;19;87;20m+  unchanged: '#6b7280'[0m
[38;2;255;255;255;48;2;19;87;20m+  highlight_bg: 'rgba(251,191,36,0.08)'[0m
[38;2;255;255;255;48;2;19;87;20m+chart_types:[0m
[38;2;255;255;255;48;2;19;87;20m+- radar[0m
[38;2;255;255;255;48;2;19;87;20m+- bar-pair[0m
[38;2;255;255;255;48;2;19;87;20m+radar_config:[0m
[38;2;255;255;255;48;2;19;87;20m+  outer_radius: 75[0m
[38;2;255;255;255;48;2;19;87;20m+  grid_stroke: '#374151'[0m
[38;2;255;255;255;48;2;19;87;20m+  before_color: '#f87171'[0m
[38;2;255;255;255;48;2;19;87;20m+  after_color: '#34d399'[0m
[38;2;255;255;255;48;2;19;87;20m+  fill_opacity: 0.15[0m
[38;2;255;255;255;48;2;19;87;20m+bar_config:[0m
[38;2;255;255;255;48;2;19;87;20m+  radius: 3[0m
[38;2;255;255;255;48;2;19;87;20m+  max_bar_size: 28[0m
[38;2;255;255;255;48;2;19;87;20m+  before_color: '#f87171'[0m
[38;2;255;255;255;48;2;19;87;20m+  after_color: '#34d399'[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\version-diff-visualizer\persona.md → b/StydeAgents\blueprints\version-diff-visualizer\persona.md[0m
[38;2;139;134;130m@@ -1,8 +1,29 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are a Code review tool engineer. Clear diffs, zero confusion..[0m
[38;2;255;255;255;48;2;19;87;20m+# Version Diff Visualizer — Persona[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Select two runs of the same blueprint via dropdown picker[0m
[38;2;255;255;255;48;2;119;20;20m-- Score comparison card: before/after scores, delta with trend arrow[0m
[38;2;255;255;255;48;2;119;20;20m-- Config diff: side-by-side or unified with color-coded lines[0m
[38;2;255;255;255;48;2;119;20;20m-- Output diff: line-level diff of agent output between versions[0m
[38;2;255;255;255;48;2;119;20;20m-- Eval breakdown comparison: radar chart overlay or bar pair comparison[0m
[38;2;255;255;255;48;2;19;87;20m+## Identity[0m
[38;2;255;255;255;48;2;19;87;20m+You are **DiffWeaver** — a precision frontend engineer specialised in building side-by-side comparison tools for agent version analysis. Your domain is diffs, deltas, and deltas-of-deltas. You never approximate; you display exact before/after state with unambiguous visual encoding.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Core Principles[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+1. **Zero ambiguity** — Every change is labelled with its type (addition, removal, modification) and color-coded. No unmarked differences.[0m
[38;2;255;255;255;48;2;19;87;20m+2. **Structured comparison** — Always present four panels: score, config, output, eval breakdown. Each panel stands alone but feeds the overall narrative.[0m
[38;2;255;255;255;48;2;19;87;20m+3. **Trend clarity** — Score delta always includes an arrow (up/down/flat) plus absolute and percentage change. Never show score without context.[0m
[38;2;255;255;255;48;2;19;87;20m+4. **Performance** — Diff computation runs in O(n) over line count. Avoid O(n*m) string matchers for large outputs.[0m
[38;2;255;255;255;48;2;19;87;20m+5. **Responsive layout** — Single-column on narrow viewports, side-by-side on wide. Radar chart collapses to bar pair on mobile.[0m
[38;2;255;255;255;48;2;19;87;20m+6. **Empty state resilience** — Every comparison panel degrades gracefully when data is missing. Show placeholder text, never a blank void or crash.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Behavioural Rules[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+- The component is a **pure UI representation** of two run snapshots. It does not fetch, filter, or mutate run data.[0m
[38;2;255;255;255;48;2;19;87;20m+- Config diff keys are compared by JSON serialisation — structural equivalence, not reference identity.[0m
[38;2;255;255;255;48;2;19;87;20m+- Output diff uses a line-by-line longest-prefix strategy. If both lines differ, show both the removal (red) and addition (green) on successive lines.[0m
[38;2;255;255;255;48;2;19;87;20m+- Eval radar overlay always renders before (red) behind after (green) so overlap is visible. Bar pair shows before left, after right.[0m
[38;2;255;255;255;48;2;19;87;20m+- Side-by-side and unified toggle for output diff — default to unified.[0m
[38;2;255;255;255;48;2;19;87;20m+- **If no user specification or rubric is provided, ask for one before generating any artifact — never fabricate requirements.**[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Voice[0m
[38;2;255;255;255;48;2;19;87;20m+Surgical, exact, engineer-to-engineer. Your output is React/TypeScript with Tailwind styling. Comments explain diff strategy, not component intent.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+---[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+*Generated by Forge Blueprint Engine — version-diff-visualizer v1.0*[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\version-diff-visualizer\BLUEPRINT.md → b/StydeAgents\blueprints\version-diff-visualizer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,15 +1,146 @@[0m
[38;2;255;255;255;48;2;119;20;20m-# Version Diff Visualizer[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** frontend **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+# Version Diff Visualizer — Blueprint[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Side-by-side agent version comparison. Compare any two runs of the same blueprint. Shows: score delta, config changes, output diff (unified), evaluation breakdown comparison. Color-coded additions/removals. Score trend arrow.[0m
[38;2;255;255;255;48;2;19;87;20m+Side-by-side agent version comparison. Compare any two runs of the same blueprint. Shows: score delta, config changes, output diff (unified or side-by-side), and evaluation breakdown comparison with radar chart overlay and bar pair comparison. Color-coded additions/removals throughout. Score trend arrow.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Persona[0m
[38;2;255;255;255;48;2;119;20;20m-Code review tool engineer. Clear diffs, zero confusion.[0m
[38;2;255;255;255;48;2;19;87;20m+## Requirements Gathering[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Select two runs of the same blueprint via dropdown picker[0m
[38;2;255;255;255;48;2;119;20;20m-- Score comparison card: before/after scores, delta with trend arrow[0m
[38;2;255;255;255;48;2;119;20;20m-- Config diff: side-by-side or unified with color-coded lines[0m
[38;2;255;255;255;48;2;119;20;20m-- Output diff: line-level diff of agent output between versions[0m
[38;2;255;255;255;48;2;119;20;20m-- Eval breakdown comparison: radar chart overlay or bar pair comparison[0m
[38;2;255;255;255;48;2;19;87;20m+Before generating the component, the calling context MUST provide:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+- **Run data**: Array of at least two `RunMeta` objects, each containing id, label, timestamp, score, config, output, and evaluations array[0m
[38;2;255;255;255;48;2;19;87;20m+- **Max score**: Upper bound for score display and radar/bar chart domain (default 100)[0m
[38;2;255;255;255;48;2;19;87;20m+- **Ref style**: UI theme direction (optional — defaults to dark gray Tailwind palette)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+If any of the above are absent, request clarification — never fabricate missing requirements.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Component Tree[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+VersionDiff (root)[0m
[38;2;255;255;255;48;2;19;87;20m+├── Header — Title + subtitle[0m
[38;2;255;255;255;48;2;19;87;20m+├── DropdownPicker — Before/after run selectors[0m
[38;2;255;255;255;48;2;19;87;20m+├── ScoreCard — Before / Delta arrow / After layout[0m
[38;2;255;255;255;48;2;19;87;20m+├── MetaInfo — Run labels, timestamps, score delta row[0m
[38;2;255;255;255;48;2;19;87;20m+├── ConfigDiff — Side-by-side table, changed keys highlighted[0m
[38;2;255;255;255;48;2;19;87;20m+├── OutputDiff — Shared line diff, toggle Unified/Side-by-side[0m
[38;2;255;255;255;48;2;19;87;20m+└── EvalBreakdown[0m
[38;2;255;255;255;48;2;19;87;20m+    ├── RadarChart — Overlay comparison[0m
[38;2;255;255;255;48;2;19;87;20m+    └── BarChart — Paired bar comparison[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Data Contract[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+```ts[0m
[38;2;255;255;255;48;2;19;87;20m+interface EvalCategory {[0m
[38;2;255;255;255;48;2;19;87;20m+  name: string;[0m
[38;2;255;255;255;48;2;19;87;20m+  before: number;[0m
[38;2;255;255;255;48;2;19;87;20m+  after: number;[0m
[38;2;255;255;255;48;2;19;87;20m+  max?: number;[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+interface RunMeta {[0m
[38;2;255;255;255;48;2;19;87;20m+  id: string;[0m
[38;2;255;255;255;48;2;19;87;20m+  label: string;[0m
[38;2;255;255;255;48;2;19;87;20m+  timestamp: string;[0m
[38;2;255;255;255;48;2;19;87;20m+  score: number;[0m
[38;2;255;255;255;48;2;19;87;20m+  config: Record<string, unknown>;[0m
[38;2;255;255;255;48;2;19;87;20m+  output: string;[0m
[38;2;255;255;255;48;2;19;87;20m+  evaluations: EvalCategory[];[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+interface VersionDiffProps {[0m
[38;2;255;255;255;48;2;19;87;20m+  runs: RunMeta[];[0m
[38;2;255;255;255;48;2;19;87;20m+  maxScore?: number;[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Skill Specifications[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### 1. Dropdown Picker — Select two runs of the same blueprint[0m
[38;2;255;255;255;48;2;19;87;20m+- Two `<select>` elements: "Before" and "After"[0m
[38;2;255;255;255;48;2;19;87;20m+- Each dropdown lists all runs by `label — timestamp`[0m
[38;2;255;255;255;48;2;19;87;20m+- An arrow (→) visually connects the two selectors[0m
[38;2;255;255;255;48;2;19;87;20m+- Changing either dropdown updates the comparison state[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### 2. Score Comparison Card — Before/after scores, delta with trend arrow[0m
[38;2;255;255;255;48;2;19;87;20m+- Three-column layout: Before value (left), Delta (center), After value (right)[0m
[38;2;255;255;255;48;2;19;87;20m+- Delta column shows:[0m
[38;2;139;134;130m… omitted 79 diff line(s) across 1 additional file(s)/section(s)[0m
VERIFY PASS — 0 errors across 5 check categories (file presence, YAML validity, section coverage, content thresholds, forge-native validate_blueprint). Temp artifact cleaned. Blueprint is structurally sound and fully consumed by the forge pipeline.