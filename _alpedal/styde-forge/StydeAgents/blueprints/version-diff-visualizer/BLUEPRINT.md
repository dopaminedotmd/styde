# Version Diff Visualizer — Blueprint

## Purpose
Side-by-side agent version comparison. Compare any two runs of the same blueprint. Shows: score delta, config changes, output diff (unified or side-by-side), and evaluation breakdown comparison with radar chart overlay and bar pair comparison. Color-coded additions/removals throughout. Score trend arrow.

## Requirements Gathering

Before generating the component, the calling context MUST provide:

- **Run data**: Array of at least two `RunMeta` objects, each containing id, label, timestamp, score, config, output, and evaluations array
- **Max score**: Upper bound for score display and radar/bar chart domain (default 100)
- **Ref style**: UI theme direction (optional — defaults to dark gray Tailwind palette)

If any of the above are absent, request clarification — never fabricate missing requirements.

## Component Tree

```
VersionDiff (root)
├── Header — Title + subtitle
├── DropdownPicker — Before/after run selectors
├── ScoreCard — Before / Delta arrow / After layout
├── MetaInfo — Run labels, timestamps, score delta row
├── ConfigDiff — Side-by-side table, changed keys highlighted
├── OutputDiff — Shared line diff, toggle Unified/Side-by-side
└── EvalBreakdown
    ├── RadarChart — Overlay comparison
    └── BarChart — Paired bar comparison
```

## Data Contract

```ts
interface EvalCategory {
  name: string;
  before: number;
  after: number;
  max?: number;
}

interface RunMeta {
  id: string;
  label: string;
  timestamp: string;
  score: number;
  config: Record<string, unknown>;
  output: string;
  evaluations: EvalCategory[];
}

interface VersionDiffProps {
  runs: RunMeta[];
  maxScore?: number;
}
```

## Skill Specifications

### 1. Dropdown Picker — Select two runs of the same blueprint
- Two `<select>` elements: "Before" and "After"
- Each dropdown lists all runs by `label — timestamp`
- An arrow (→) visually connects the two selectors
- Changing either dropdown updates the comparison state

### 2. Score Comparison Card — Before/after scores, delta with trend arrow
- Three-column layout: Before value (left), Delta (center), After value (right)
- Delta column shows:
  - Arrow character: ▲ (up, green), ▼ (down, red), — (flat, gray)
  - Numeric delta with sign (+3.2, -1.5, 0.0)
  - Percentage change relative to maxScore
- Score values rendered in monospace font at 2xl size with "/ maxScore" suffix

### 3. Config Diff — Side-by-side or unified with color-coded lines
- Table with three columns: Key, Before, After
- Changed rows highlighted with yellow/amber background tint
- Before value of changed keys gets strikethrough decoration
- After value of changed keys gets green background tint
- Values color-coded by type: boolean (green/red), number (cyan), null (gray), string (yellow)

### 4. Output Diff — Line-level diff of agent output between versions
- Toggle between Unified and Side-by-side views
- **Unified view**: Single scrollable column, each line prefixed with + (green), − (red), or space (gray)
- **Side-by-side**: Two-column grid. Left column shows only unchanged + removed lines (red for removals). Right column shows only unchanged + added lines (green for additions)
- Max height of 320px with overflow scroll
- Diff strategy: line-by-line LCS (longest common subsequence) alignment. When two consecutive lines differ, show removal before addition

### 5. Eval Breakdown Comparison — Radar chart overlay or bar pair comparison
- Two visualisations side by side:
  - **Radar chart** (recharts `RadarChart`): Before (red, fillOpacity 0.15) overlaid with After (green, fillOpacity 0.15). Polar grid, angle axis with category names, radius axis 0–maxScore
  - **Bar chart** (recharts `BarChart`): Paired bars per category. Before (red), After (green). Cartesian grid, X/Y axes, tooltip on hover
- Both charts wrapped in `ResponsiveContainer` at 260px height
- Show empty state message if evalData is empty

## Output Contract

- Deliver a single **React/TypeScript component** (`VersionDiff`) as default export
- All styling via **Tailwind CSS utility classes** — no separate CSS files
- Uses **recharts** for radar and bar charts
- Uses React hooks: `useState`, `useMemo` only
- Component must be pure — receives `runs` and `maxScore` props, renders comparison
- No external API calls, no side effects, no state mutations

## Empty States

| Region | Empty Condition | Display |
|--------|----------------|---------|
| Root | runs.length === 0 | "No runs available for comparison" |
| Picker | before or after not selected | "Select both a before and after run to compare" |
| Config | No config keys | "No config keys to compare" |
| Output | No output lines | "No output to compare" |
| Eval | No eval data | "No evaluation data to compare" |

## Validation Rubric

| Dimension | Pass | Fail |
|-----------|------|------|
| Accuracy | Score delta matches Math.round(r1.score - r2.score); diff lines represent actual line-level changes | Delta off by rounding; diff shows wrong lines |
| Completeness | All four panels render with real data when provided; empty states for missing data | Panel missing or empty with no placeholder |
| Usefulness | Color encoding is unambiguous; trend arrow immediately readable; charts show meaningful comparison | Colors confusing; arrow missing; charts empty or off-scale |
| Performance | Diff runs in O(n); no unnecessary re-renders; memoised computations | O(n*m) diff; re-render on every keystroke |
| Accessibility | Select elements have labels; charts have aria-labels; color not the only differentiator | Missing labels; no accessible chart descriptions |
| Consistency | Tailwind classes use consistent palette (gray-900/800/700/500/400/300); before=red, after=green across all panels | Mixed color systems; before/after colors swapped between panels |

If any dimension fails, correct the output before delivery. If input data is empty or malformed, emit appropriate empty state — never throw or render broken UI.

## Dependencies

- `react` (v18+)
- `recharts` (v2+) — RadarChart, BarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, Legend, ResponsiveContainer
- `tailwindcss` (v3+) — utility classes only

## Error Handling

- Missing/invalid run data → render root empty state: "No runs available for comparison"
- Single run provided → show empty state on picker: "Select both a before and after run to compare"
- Config value serialisation → use `String(value ?? '—')` for display; never throw on undefined values
- All comparisons are pure computations — no side effects, no network calls

## File Structure

```
blueprints/version-diff-visualizer/
├── BLUEPRINT.md      # This file
├── config.yaml        # Visualizer configuration
└── persona.md         # Agent persona for this blueprint
```
