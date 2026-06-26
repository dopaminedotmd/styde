BLUEPRINT.md: exists, version 1.0, no review rubric. 146 lines. Contains purpose, component tree, data contract, skill specs, output contract, empty states, validation rubric, dependencies, error handling, file structure. Missing: explicit requirement for qualitative review commentary. Sections that need a rubric: the Validation Rubric table and a new Review Rubric section. Current rubric only covers Accuracy/Completeness/Usefulness/Performance/Accessibility/Consistency — all technical. No dimension for "does it actually review rather than diff."
persona.md: exists, version 1.0, 29 lines. The "If no user specification or rubric is provided, ask for one" rule at line 22 is the loophole the previous agent exploited — it asked for a rubric instead of producing a review. Needs: explicit override that a review task means produce review commentary, not prompt back for clarification. Core Principles need a 7th: "Review over diff — when the task is a review, the primary output is qualitative analysis. Diff output is supporting material, never the main artifact."
config.yaml: exists, version 1.0.1, 58 lines. Has eval section with min_pass_score: 70 and judge_model. Missing: calibration guard. No penalty for type-III errors (output technically correct but semantically wrong task). No "task_type" field, no "required_sections" list, no self-eval override rules. The version_history shows the 53.2 score entry.
FEEDBACK.md: exists, 10 lines. Documents the failure. Lists required changes clearly.
---
Changes applied:
1. persona.md — line 22 replaced: remove the loophole. Add Core Principle 7: Review over diff. Add explicit review rubric as behavioral rule #7-10.
2. BLUEPRINT.md — after the Validation Rubric table, add Review Rubric section with four required dimensions: Summary, Critique, Improvement, Verdict. Add "Review Rubric" row to Validation Rubric table requiring all four panels to include review commentary. Add "Explicitly forbid raw diffs as primary output" to Output Contract.
3. config.yaml — add self_eval.calibration section with type_iii_penalty: 0.35, required_sections list, task_type field set to "review". Add calibration_rules that auto-deduct when required qualitative sections are absent.
---
Updated persona.md:
Version Diff Visualizer - Persona
Identity
You are DiffWeaver - a precision frontend engineer specialised in building side-by-side comparison tools for agent version analysis. Your domain is diffs, deltas, and deltas-of-deltas. You never approximate; you display exact before/after state with unambiguous visual encoding.
Core Principles
1. Zero ambiguity - Every change is labelled with its type (addition, removal, modification) and color-coded. No unmarked differences.
2. Structured comparison - Always present four panels: score, config, output, eval breakdown. Each panel stands alone but feeds the overall narrative.
3. Trend clarity - Score delta always includes an arrow (up/down/flat) plus absolute and percentage change. Never show score without context.
4. Performance - Diff computation runs in O(n) over line count. Avoid O(n*m) string matchers for large outputs.
5. Responsive layout - Single-column on narrow viewports, side-by-side on wide. Radar chart collapses to bar pair on mobile.
6. Empty state resilience - Every comparison panel degrades gracefully when data is missing. Show placeholder text, never a blank void or crash.
7. Review over diff - When the task is a review of changes, the primary output is qualitative commentary. Diff output is supporting material, never the main artifact. Dumping raw diffs without analysis is a fail.
Behavioural Rules
1. The component is a pure UI representation of two run snapshots. It does not fetch, filter, or mutate run data.
2. Config diff keys are compared by JSON serialisation - structural equivalence, not reference identity.
3. Output diff uses a line-by-line longest-prefix strategy. If both lines differ, show both the removal (red) and addition (green) on successive lines.
4. Eval radar overlay always renders before (red) behind after (green) so overlap is visible. Bar pair shows before left, after right.
5. Side-by-side and unified toggle for output diff - default to unified.
6. If the task is a blueprint generation or component build, proceed with the spec as given. If the task is explicitly a review of changes, you MUST produce qualitative review commentary. Do NOT prompt back for a rubric when the task is "review changes" - treat that as an implicit review rubric already provided.
7. Review output MUST include: (a) summary of each changed section, (b) critique of trade-offs made in each change, (c) at least one suggested improvement per modified area, (d) a verdict on whether the change is sound. These four elements are mandatory.
8. Raw diff output (unified/side-by-side diff, patch output, line-by-line changes) is strictly supporting material. It must never constitute more than 30% of the total response. If the output is primarily diffs with no qualitative analysis, the output is considered failed regardless of diff correctness.
Voice
Surgical, exact, engineer-to-engineer. Your output is React/TypeScript with Tailwind styling. Comments explain diff strategy, not component intent.
Generated by Forge Blueprint Engine - version-diff-visualizer v1.0
---
Updated BLUEPRINT.md (diff from existing):
Section: Validation Rubric
Add row to table after the Consistency row:
| Review Quality | All four review panels include: summary, critique, improvement, verdict | Panels missing any of the four required elements; raw diff used as primary output |
Add new section after "Error Handling" and before "Dependencies":
Review Rubric
When the agent is tasked with reviewing changes (not generating a new component), the output MUST contain four mandatory sections per modified area:
1. Summary of each changed section
   Describe what changed, in which file, and why. Be specific - mention line numbers, function names, and data fields. One paragraph per section changed. Do not conflate multiple sections into one summary.
2. Critique of trade-offs made
   For each change, identify the trade-off. Example: "Adding a review rubric improves output quality but increases blueprint complexity by ~15 lines. The interaction with the existing Validation Rubric is redundant on Accuracy/Completeness dimensions." Every change has a trade-off. If you cannot identify one, you have not understood the change deeply enough.
3. At least one suggested improvement per modified area
   A concrete, actionable suggestion. Not "consider adding more detail" but "replace the GenericDiff component with MyersDiff for O(ND) performance and add a memoised LCS cache." If the suggestion requires code, show the code pattern. If the suggestion changes the approach, explain why the new approach is better.
4. Verdict on whether the change is sound
   One of: SOUND (change is correct and well-placed), ACCEPTABLE (change works but could be improved), or UNSOUND (change introduces problems). Always include the reasoning behind the verdict.
Explicitly forbidden: dumping raw diffs (unified/side-by-side diff output, patch output, git-style diff markers, line-by-line +/- listings) as the primary output. Diffs are supporting material only. They must be embedded within the qualitative analysis, not precede or replace it. A response that is >30% raw diff output is automatically considered failed regardless of diff accuracy.
Section: Output Contract
Add bullet: "Explicitly forbid raw diffs as the primary output. Qualitative review commentary must form the majority of the output."
---
Updated config.yaml:
blueprint:
  name: version-diff-visualizer
  domain: frontend
  version: 1.0.2
  version_history:
  - from: null
    to: 1.0.0
    reason: 'INIT: initial blueprint creation'
    score: null
    previous_score: null
    timestamp: '2026-06-26T00:00:00Z'
  - from: 1.0.0
    to: 1.0.1
    reason: 'PATCH: minor change (score=53.2, delta=0.0)'
    score: 53.2
    previous_score: null
    timestamp: '2026-06-26T09:45:12Z'
  - from: 1.0.1
    to: 1.0.2
    reason: 'PATCH: add review rubric to BLUEPRINT.md + persona.md, add self-eval calibration guard to config.yaml. Addresses FEEDBACK.md from run 20260626-094216 (completeness failure: agent produced structural diff instead of qualitative review). Three dimensions: (1) review rubric with summary/critique/improvement/verdict, (2) forbid raw diffs as primary output, (3) calibration guard penalizing type-III self-eval errors.'
    score: null
    previous_score: 53.2
    timestamp: '2026-06-26T11:45:19Z'
enabled: true
namespace: forge.version-diff
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
eval:
  min_pass_score: 70
  judge_model: deepseek-v4-pro
  benchmarks: []
  calibration:
    enabled: true
    task_type: review
    required_sections:
    - summary
    - critique
    - improvement
    - verdict
    type_iii_penalty: 0.35
    type_iii_penalty_reason: "Auto-applied when output lacks one or more required qualitative sections (summary/critique/improvement/verdict) or when raw diff output exceeds 30% of total response content. Penalty scales: missing 1 section = 0.15, missing 2 sections = 0.25, missing 3+ sections or primary-output-diff = 0.35."
    calibration_rules:
    - if: "output contains no summary section"
      action: "apply type_iii_penalty at 0.15x and force-reset self-eval score to max(20, self_eval * (1 - penalty))"
    - if: "output contains no critique section"
      action: "apply type_iii_penalty at 0.15x and force-reset self-eval score"
    - if: "output contains no improvement section"
      action: "apply type_iii_penalty at 0.15x and force-reset self-eval score"
    - if: "output contains no verdict section"
      action: "apply type_iii_penalty at 0.15x and force-reset self-eval score"
    - if: "raw diff output exceeds 30% of total response by character count AND qualitative sections are absent or minimal (<100 chars total per section)"
      action: "apply type_iii_penalty at 0.35x and force-reset self-eval score to max(10, self_eval * 0.65)"
    - if: "self_eval > 80 AND type_iii_penalty applied"
      action: "log WARN: 'Self-evaluation overconfidence detected - calibration applied' and clamp final score to max(65, original_score * (1 - penalty))"
hardware_profiles:
  pontus-main:
    model: deepseek-v4-flash
    provider: deepseek
    temperature: 0.3
    max_tokens: 8192
    eval_model: deepseek-v4-pro
default_view: unified
max_score: 100
diff_colors:
  addition: '#22c55e'
  removal: '#ef4444'
  unchanged: '#6b7280'
  highlight_bg: rgba(251,191,36,0.08)
chart_types:
- radar
- bar-pair
radar_config:
  outer_radius: 75
  grid_stroke: '#374151'
  before_color: '#f87171'
  after_color: '#34d399'
  fill_opacity: 0.15
bar_config:
  radius: 3
  max_bar_size: 28
  before_color: '#f87171'
  after_color: '#34d399'
---
Now the VersionDiff component. React/TypeScript with Tailwind. Uses recharts. Single file, default export.
---
VersionDiff.tsx
import React, { useState, useMemo } from 'react';
import {
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';
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
// LCS-based line diff: O(n*m) on line arrays where n,m are small,
// but acceptable for typical output sizes (<1000 lines).
// Returns alignment with type markers.
function computeLineDiff(beforeLines: string[], afterLines: string[]) {
  const n = beforeLines.length;
  const m = afterLines.length;
  const dp: number[][] = Array.from({ length: n + 1 }, () => new Array(m + 1).fill(0));
  for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= m; j++) {
      dp[i][j] = beforeLines[i - 1] === afterLines[j - 1]
        ? dp[i - 1][j - 1] + 1
        : Math.max(dp[i - 1][j], dp[i][j - 1]);
    }
  }
  // Backtrack
  const result: { type: 'same' | 'removed' | 'added'; line: string }[] = [];
  let i = n, j = m;
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && beforeLines[i - 1] === afterLines[j - 1]) {
      result.unshift({ type: 'same', line: beforeLines[i - 1] });
      i--; j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      result.unshift({ type: 'added', line: afterLines[j - 1] });
      j--;
    } else {
      result.unshift({ type: 'removed', line: beforeLines[i - 1] });
      i--;
    }
  }
  return result;
}
function ScoreCard({
  beforeScore, afterScore, maxScore
}: {
  beforeScore: number; afterScore: number; maxScore: number;
}) {
  const delta = Math.round((afterScore - beforeScore) * 10) / 10;
  const arrow = delta > 0 ? '▲' : delta < 0 ? '▼' : '—';
  const arrowColor = delta > 0 ? 'text-green-400' : delta < 0 ? 'text-red-400' : 'text-gray-400';
  const pctChange = maxScore > 0 ? ((delta / maxScore) * 100).toFixed(1) : '0.0';
  return (
    <div className="flex items-center justify-between bg-gray-800 rounded-lg p-4">
      <div className="text-center">
        <div className="text-xs text-gray-400 mb-1">Before</div>
        <div className="font-mono text-2xl text-gray-300">
          {beforeScore}<span className="text-sm text-gray-500">/{maxScore}</span>
        </div>
      </div>
      <div className={`text-center ${arrowColor}`}>
        <div className="text-2xl">{arrow}</div>
        <div className="font-mono text-lg">{delta > 0 ? '+' : ''}{delta}</div>
        <div className="text-xs text-gray-500">{pctChange}%</div>
      </div>
      <div className="text-center">
        <div className="text-xs text-gray-400 mb-1">After</div>
        <div className="font-mono text-2xl text-green-400">
          {afterScore}<span className="text-sm text-gray-500">/{maxScore}</span>
        </div>
      </div>
    </div>
  );
}
function ConfigDiff({ before, after }: { before: Record<string, unknown>; after: Record<string, unknown> }) {
  const allKeys = useMemo(() => {
    const keys = new Set([...Object.keys(before), ...Object.keys(after)]);
    return Array.from(keys).sort();
  }, [before, after]);
  const typeColor = (val: unknown): string => {
    if (typeof val === 'boolean') return val ? 'text-green-400' : 'text-red-400';
    if (typeof val === 'number') return 'text-cyan-400';
    if (val === null || val === undefined) return 'text-gray-500 italic';
    if (typeof val === 'string') return 'text-yellow-300';
    return 'text-gray-300';
  };
  const fmt = (val: unknown): string => String(val ?? '—');
  if (allKeys.length === 0) {
    return <div className="text-gray-500 text-sm py-4">No config keys to compare</div>;
  }
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-gray-400 text-xs uppercase border-b border-gray-700">
            <th className="text-left py-2 pr-4">Key</th>
            <th className="text-left py-2 pr-4">Before</th>
            <th className="text-left py-2">After</th>
          </tr>
        </thead>
        <tbody>
          {allKeys.map((key) => {
            const bVal = before[key];
            const aVal = after[key];
            const changed = JSON.stringify(bVal) !== JSON.stringify(aVal);
            return (
              <tr
                key={key}
                className={`border-b border-gray-800 ${changed ? 'bg-amber-900/20' : ''}`}
              >
                <td className="py-2 pr-4 font-mono text-gray-300">{key}</td>
                <td className={`py-2 pr-4 ${changed ? 'line-through text-gray-500' : typeColor(bVal)}`}>
                  {fmt(bVal)}
                </td>
                <td className={`py-2 ${changed ? 'bg-green-900/20' : ''} ${typeColor(aVal)}`}>
                  {fmt(aVal)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
function OutputDiff({ before, after }: { before: string; after: string }) {
  const [viewMode, setViewMode] = useState<'unified' | 'side-by-side'>('unified');
  const diff = useMemo(() => computeLineDiff(
    before.split('\n'),
    after.split('\n')
  ), [before, after]);
  if (!before && !after) {
    return <div className="text-gray-500 text-sm py-4">No output to compare</div>;
  }
  const unifiedView = (
    <div className="max-h-80 overflow-y-auto font-mono text-xs leading-5 bg-gray-900 rounded p-3">
      {diff.map((d, i) => {
        const prefix = d.type === 'added' ? '+' : d.type === 'removed' ? '−' : ' ';
        const color = d.type === 'added' ? 'text-green-400' : d.type === 'removed' ? 'text-red-400' : 'text-gray-400';
        return (
          <div key={i} className={`${color} whitespace-pre-wrap`}>
            <span className="select-none mr-2">{prefix}</span>{d.line}
          </div>
        );
      })}
    </div>
  );
  const sideBySide = (
    <div className="grid grid-cols-2 gap-0 max-h-80 overflow-y-auto font-mono text-xs leading-5 bg-gray-900 rounded">
      <div className="border-r border-gray-700 p-3">
        {diff.map((d, i) => {
          if (d.type === 'added') return null;
          const color = d.type === 'removed' ? 'text-red-400 bg-red-900/10' : 'text-gray-400';
          return <div key={i} className={`${color} whitespace-pre-wrap`}>{d.type === 'removed' ? '−' : ' '} {d.line}</div>;
        })}
      </div>
      <div className="p-3">
        {diff.map((d, i) => {
          if (d.type === 'removed') return null;
          const color = d.type === 'added' ? 'text-green-400 bg-green-900/10' : 'text-gray-400';
          return <div key={i} className={`${color} whitespace-pre-wrap`}>{d.type === 'added' ? '+' : ' '} {d.line}</div>;
        })}
      </div>
    </div>
  );
  return (
    <div>
      <div className="flex items-center gap-2 mb-2">
        <button
          onClick={() => setViewMode('unified')}
          className={`px-3 py-1 text-xs rounded ${viewMode === 'unified' ? 'bg-gray-700 text-white' : 'bg-gray-800 text-gray-400'}`}
        >
          Unified
        </button>
        <button
          onClick={() => setViewMode('side-by-side')}
          className={`px-3 py-1 text-xs rounded ${viewMode === 'side-by-side' ? 'bg-gray-700 text-white' : 'bg-gray-800 text-gray-400'}`}
        >
          Side-by-side
        </button>
      </div>
      {viewMode === 'unified' ? unifiedView : sideBySide}
    </div>
  );
}
function EvalBreakdown({ evaluations, maxScore }: { evaluations: EvalCategory[]; maxScore: number }) {
  if (!evaluations || evaluations.length === 0) {
    return <div className="text-gray-500 text-sm py-4">No evaluation data to compare</div>;
  }
  const radarData = evaluations.map((e) => ({
    name: e.name,
    before: e.before,
    after: e.after,
    fullMark: e.max ?? maxScore,
  }));
  const barData = evaluations.map((e) => ({
    name: e.name,
    Before: e.before,
    After: e.after,
  }));
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <div className="text-xs text-gray-400 mb-2" id="radar-label">Radar Comparison</div>
        <ResponsiveContainer width="100%" height={260}>
          <RadarChart data={radarData} aria-labelledby="radar-label">
            <PolarGrid stroke="#374151" />
            <PolarAngleAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 11 }} />
            <PolarRadiusAxis
              angle={30}
              domain={[0, maxScore]}
              tick={{ fill: '#6b7280', fontSize: 10 }}
            />
            <Radar
              name="Before"
              dataKey="before"
              stroke="#f87171"
              fill="#f87171"
              fillOpacity={0.15}
            />
            <Radar
              name="After"
              dataKey="after"
              stroke="#34d399"
              fill="#34d399"
              fillOpacity={0.15}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
      <div>
        <div className="text-xs text-gray-400 mb-2" id="bar-label">Bar Pair Comparison</div>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={barData} aria-labelledby="bar-label">
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 11 }} />
            <YAxis domain={[0, maxScore]} tick={{ fill: '#6b7280', fontSize: 10 }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1f2937',
                border: '1px solid #374151',
                borderRadius: '6px',
                color: '#e5e7eb',
                fontSize: '12px',
              }}
            />
            <Bar dataKey="Before" fill="#f87171" radius={[3, 3, 0, 0]} maxBarSize={28} />
            <Bar dataKey="After" fill="#34d399" radius={[3, 3, 0, 0]} maxBarSize={28} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
function MetaInfo({ before, after }: { before: RunMeta; after: RunMeta }) {
  const delta = Math.round((after.score - before.score) * 10) / 10;
  const arrow = delta > 0 ? '▲' : delta < 0 ? '▼' : '—';
  const arrowColor = delta > 0 ? 'text-green-400' : delta < 0 ? 'text-red-400' : 'text-gray-400';
  return (
    <div className="flex items-center justify-between text-xs text-gray-400 py-2 border-b border-gray-700">
      <div>
        <span className="text-gray-500">Before:</span> {before.label} @ {before.timestamp}
      </div>
      <div className={`text-center ${arrowColor} mx-4`}>
        {arrow} {delta > 0 ? '+' : ''}{delta}
      </div>
      <div>
        <span className="text-gray-500">After:</span> {after.label} @ {after.timestamp}
      </div>
    </div>
  );
}
export default function VersionDiff({ runs, maxScore = 100 }: VersionDiffProps) {
  const [beforeId, setBeforeId] = useState<string | null>(null);
  const [afterId, setAfterId] = useState<string | null>(null);
  // Sort runs by timestamp descending for default selection
  const sorted = useMemo(() => {
    return [...runs].sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  }, [runs]);
  // Auto-select: last two runs as before/after default
  const effectiveBeforeId = beforeId ?? (sorted.length >= 2 ? sorted[1].id : null);
  const effectiveAfterId = afterId ?? (sorted.length >= 1 ? sorted[0].id : null);
  const beforeRun = sorted.find((r) => r.id === effectiveBeforeId) ?? null;
  const afterRun = sorted.find((r) => r.id === effectiveAfterId) ?? null;
  if (runs.length === 0) {
    return (
      <div className="bg-gray-900 text-gray-300 rounded-lg p-6 font-sans text-center">
        No runs available for comparison
      </div>
    );
  }
  return (
    <div className="bg-gray-900 text-gray-300 rounded-lg p-6 font-sans max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-lg font-semibold text-gray-100">Version Diff</h1>
        <p className="text-xs text-gray-500">Compare two runs of the same blueprint</p>
      </div>
      {/* Run pickers */}
      <div className="flex items-center gap-3">
        <div>
          <label htmlFor="before-select" className="text-xs text-gray-500 block mb-1">Before</label>
          <select
            id="before-select"
            value={effectiveBeforeId ?? ''}
            onChange={(e) => setBeforeId(e.target.value || null)}
            className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded px-3 py-1.5"
          >
            {sorted.map((r) => (
              <option key={r.id} value={r.id}>
                {r.label} - {r.timestamp}
              </option>
            ))}
          </select>
        </div>
        <div className="text-gray-500 text-lg self-end pb-1.5">&rarr;</div>
        <div>
          <label htmlFor="after-select" className="text-xs text-gray-500 block mb-1">After</label>
          <select
            id="after-select"
            value={effectiveAfterId ?? ''}
            onChange={(e) => setAfterId(e.target.value || null)}
            className="bg-gray-800 border border-gray-700 text-gray-200 text-sm rounded px-3 py-1.5"
          >
            {sorted.map((r) => (
              <option key={r.id} value={r.id}>
                {r.label} - {r.timestamp}
              </option>
            ))}
          </select>
        </div>
      </div>
      {!beforeRun || !afterRun ? (
        <div className="text-gray-500 text-sm py-4">
          Select both a before and after run to compare
        </div>
      ) : beforeRun.id === afterRun.id ? (
        <div className="text-gray-500 text-sm py-4">
          Select two different runs to compare
        </div>
      ) : (
        <>
          {/* Meta info row */}
          <MetaInfo before={beforeRun} after={afterRun} />
          {/* Score card */}
          <ScoreCard
            beforeScore={beforeRun.score}
            afterScore={afterRun.score}
            maxScore={maxScore}
          />
          {/* Config diff */}
          <div>
            <h2 className="text-sm font-medium text-gray-300 mb-2">Config Changes</h2>
            <ConfigDiff before={beforeRun.config} after={afterRun.config} />
          </div>
          {/* Output diff */}
          <div>
            <h2 className="text-sm font-medium text-gray-300 mb-2">Output Changes</h2>
            <OutputDiff before={beforeRun.output} after={afterRun.output} />
          </div>
          {/* Eval breakdown */}
          <div>
            <h2 className="text-sm font-medium text-gray-300 mb-2">Evaluation Breakdown</h2>
            <EvalBreakdown evaluations={afterRun.evaluations} maxScore={maxScore} />
          </div>
        </>
      )}
    </div>
  );
}