```tsx
import React, { useState, useMemo } from 'react';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from 'recharts';
// ─── Types ──────────────────────────────────────────────────────────────────
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
// ─── Helpers ────────────────────────────────────────────────────────────────
function lineDiff(a: string, b: string): { type: 'same' | 'add' | 'remove'; line: string }[] {
  const linesA = a.split('\n');
  const linesB = b.split('\n');
  const max = Math.max(linesA.length, linesB.length);
  const result: { type: 'same' | 'add' | 'remove'; line: string }[] = [];
  for (let i = 0; i < max; i++) {
    const la = linesA[i];
    const lb = linesB[i];
    if (la === undefined) {
      result.push({ type: 'add', line: lb ?? '' });
    } else if (lb === undefined) {
      result.push({ type: 'remove', line: la });
    } else if (la !== lb) {
      result.push({ type: 'remove', line: la });
      result.push({ type: 'add', line: lb });
    } else {
      result.push({ type: 'same', line: la });
    }
  }
  return result;
}
function colorForConfigValue(value: unknown): string {
  if (value === null || value === undefined) return 'text-gray-400';
  if (typeof value === 'boolean') return value ? 'text-green-400' : 'text-red-400';
  if (typeof value === 'number') return 'text-cyan-300';
  return 'text-yellow-200';
}
// ─── Sub-Components ─────────────────────────────────────────────────────────
const DropdownPicker: React.FC<{
  runs: RunMeta[];
  beforeId: string;
  afterId: string;
  onBeforeChange: (id: string) => void;
  onAfterChange: (id: string) => void;
}> = ({ runs, beforeId, afterId, onBeforeChange, onAfterChange }) => (
  <div className="flex items-center gap-4 mb-6 flex-wrap">
    <div className="flex items-center gap-2">
      <span className="text-xs uppercase tracking-wider text-gray-500 font-semibold">Before</span>
      <select
        className="bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        value={beforeId}
        onChange={(e) => onBeforeChange(e.target.value)}
      >
        {runs.map((r) => (
          <option key={r.id} value={r.id}>
            {r.label} — {r.timestamp}
          </option>
        ))}
      </select>
    </div>
    <span className="text-gray-600 text-lg">→</span>
    <div className="flex items-center gap-2">
      <span className="text-xs uppercase tracking-wider text-gray-500 font-semibold">After</span>
      <select
        className="bg-gray-800 border border-gray-700 rounded px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:ring-2 focus:ring-cyan-500"
        value={afterId}
        onChange={(e) => onAfterChange(e.target.value)}
      >
        {runs.map((r) => (
          <option key={r.id} value={r.id}>
            {r.label} — {r.timestamp}
          </option>
        ))}
      </select>
    </div>
  </div>
);
const ScoreCard: React.FC<{ before: number; after: number; maxScore: number }> = ({
  before,
  after,
  maxScore,
}) => {
  const delta = after - before;
  const pct = maxScore > 0 ? ((delta / maxScore) * 100).toFixed(1) : '0.0';
  const arrow = delta > 0 ? '▲' : delta < 0 ? '▼' : '—';
  const color = delta > 0 ? 'text-green-400' : delta < 0 ? 'text-red-400' : 'text-gray-400';
  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-5 flex items-center justify-between">
      <div className="space-y-1">
        <div className="text-xs uppercase tracking-wider text-gray-500">Before</div>
        <div className="text-2xl font-mono font-bold text-gray-300">
          {before.toFixed(1)}
          <span className="text-sm text-gray-600 ml-1">/ {maxScore}</span>
        </div>
      </div>
      <div className={`text-center ${color}`}>
        <div className="text-3xl font-bold">{arrow}</div>
        <div className="text-lg font-mono font-semibold">
          {delta >= 0 ? '+' : ''}{delta.toFixed(1)}
        </div>
        <div className="text-xs opacity-70">{pct}%</div>
      </div>
      <div className="space-y-1 text-right">
        <div className="text-xs uppercase tracking-wider text-gray-500">After</div>
        <div className="text-2xl font-mono font-bold text-gray-300">
          {after.toFixed(1)}
          <span className="text-sm text-gray-600 ml-1">/ {maxScore}</span>
        </div>
      </div>
    </div>
  );
};
const EmptyState: React.FC<{ message: string }> = ({ message }) => (
  <div className="flex items-center justify-center h-32 text-gray-500 text-sm italic border border-dashed border-gray-700 rounded">
    {message}
  </div>
);
const StringRecord: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="text-sm">
    <span className="text-gray-500 mr-2">{label}:</span>
    <span className="text-gray-200">{value}</span>
  </div>
);
// ─── Main Component ─────────────────────────────────────────────────────────
const VersionDiff: React.FC<VersionDiffProps> = ({ runs, maxScore = 100 }) => {
  const [beforeId, setBeforeId] = useState<string>(runs[0]?.id ?? '');
  const [afterId, setAfterId] = useState<string>(runs[1]?.id ?? '');
  const [diffView, setDiffView] = useState<'unified' | 'side-by-side'>('unified');
  const before = useMemo(() => runs.find((r) => r.id === beforeId), [runs, beforeId]);
  const after = useMemo(() => runs.find((r) => r.id === afterId), [runs, afterId]);
  const diffLines = useMemo(() => {
    if (!before || !after) return [];
    return lineDiff(before.output, after.output);
  }, [before, after]);
  const configKeys = useMemo(() => {
    if (!before || !after) return [];
    const all = new Set([...Object.keys(before.config), ...Object.keys(after.config)]);
    return Array.from(all).sort();
  }, [before, after]);
  const evalData = useMemo(() => {
    if (!before || !after) return [];
    const cats = new Map<string, EvalCategory>();
    for (const e of before.evaluations) cats.set(e.name, { name: e.name, before: e.score, after: 0, max: e.max ?? maxScore });
    for (const e of after.evaluations) {
      const existing = cats.get(e.name);
      if (existing) existing.after = e.score;
      else cats.set(e.name, { name: e.name, before: 0, after: e.score, max: e.max ?? maxScore });
    }
    return Array.from(cats.values());
  }, [before, after, maxScore]);
  if (runs.length === 0) return <EmptyState message="No runs available for comparison" />;
  return (
    <div className="bg-gray-900 text-gray-200 font-sans p-6 rounded-xl max-w-7xl mx-auto space-y-8">
      {/* ── Header ── */}
      <div className="border-b border-gray-700 pb-3">
        <h1 className="text-xl font-semibold tracking-tight">Version Diff Visualizer</h1>
        <p className="text-xs text-gray-500 mt-1">Compare two runs of the same blueprint</p>
      </div>
      {/* ── Run Picker ── */}
      <DropdownPicker
        runs={runs}
        beforeId={beforeId}
        afterId={afterId}
        onBeforeChange={setBeforeId}
        onAfterChange={setAfterId}
      />
      {(!before || !after) ? (
        <EmptyState message="Select both a before and after run to compare" />
      ) : (
        <>
          {/* ── Score Comparison Card ── */}
          <ScoreCard before={before.score} after={after.score} maxScore={maxScore} />
          {/* ── Meta Info ── */}
          <div className="grid grid-cols-2 gap-4 text-xs bg-gray-800/50 rounded-lg p-4 border border-gray-700">
            <StringRecord label="Before Run" value={`${before.label} — ${before.timestamp}`} />
            <StringRecord label="After Run" value={`${after.label} — ${after.timestamp}`} />
            <StringRecord label="Score Δ" value={`${(after.score - before.score).toFixed(1)} pts`} />
          </div>
          {/* ── Config Diff ── */}
          <section>
            <div className="text-xs uppercase tracking-wider text-gray-500 mb-3 font-semibold">Config Diff</div>
            {configKeys.length === 0 ? (
              <EmptyState message="No config keys to compare" />
            ) : (
              <div className="overflow-x-auto rounded border border-gray-700">
                <table className="w-full text-sm font-mono">
                  <thead>
                    <tr className="bg-gray-800 text-gray-400 text-xs uppercase tracking-wide">
                      <th className="text-left px-4 py-2 border-b border-gray-700">Key</th>
                      <th className="text-left px-4 py-2 border-b border-gray-700">Before</th>
                      <th className="text-left px-4 py-2 border-b border-gray-700">After</th>
                    </tr>
                  </thead>
                  <tbody>
                    {configKeys.map((key) => {
                      const vBefore = before.config[key];
                      const vAfter = after.config[key];
                      const changed =
                        JSON.stringify(vBefore) !== JSON.stringify(vAfter);
                      return (
                        <tr
                          key={key}
                          className={`border-b border-gray-800 last:border-b-0 ${
                            changed ? 'bg-yellow-900/10' : ''
                          }`}
                        >
                          <td className="px-4 py-2 text-gray-400 whitespace-nowrap">{key}</td>
                          <td
                            className={`px-4 py-2 whitespace-nowrap ${
                              colorForConfigValue(vBefore)
                            } ${changed ? 'line-through decoration-red-400/60' : ''}`}
                          >
                            {String(vBefore ?? '—')}
                          </td>
                          <td
                            className={`px-4 py-2 whitespace-nowrap ${
                              colorForConfigValue(vAfter)
                            } ${changed ? 'bg-green-900/20' : ''}`}
                          >
                            {String(vAfter ?? '—')}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </section>
          {/* ── Output Diff ── */}
          <section>
            <div className="flex items-center justify-between mb-3">
              <div className="text-xs uppercase tracking-wider text-gray-500 font-semibold">Output Diff</div>
              <div className="flex items-center gap-2">
                <button
                  className={`text-xs px-2.5 py-1 rounded ${
                    diffView === 'unified'
                      ? 'bg-cyan-600/30 text-cyan-300 border border-cyan-600'
                      : 'bg-gray-800 text-gray-400 border border-gray-700'
                  }`}
                  onClick={() => setDiffView('unified')}
                >
                  Unified
                </button>
                <button
                  className={`text-xs px-2.5 py-1 rounded ${
                    diffView === 'side-by-side'
                      ? 'bg-cyan-600/30 text-cyan-300 border border-cyan-600'
                      : 'bg-gray-800 text-gray-400 border border-gray-700'
                  }`}
                  onClick={() => setDiffView('side-by-side')}
                >
                  Side-by-side
                </button>
              </div>
            </div>
            {diffLines.length === 0 ? (
              <EmptyState message="No output to compare" />
            ) : diffView === 'unified' ? (
              <div className="bg-gray-950 rounded border border-gray-700 overflow-auto max-h-80 text-xs font-mono leading-5">
                {diffLines.map((entry, i) => (
                  <div
                    key={i}
                    className={`px-4 ${
                      entry.type === 'add'
                        ? 'bg-green-900/30 text-green-300 border-l-2 border-green-500'
                        : entry.type === 'remove'
                        ? 'bg-red-900/30 text-red-300 border-l-2 border-red-500'
                        : 'text-gray-400'
                    }`}
                  >
                    <span className="inline-block w-6 text-gray-600 select-none">
                      {entry.type === 'add' ? '+' : entry.type === 'remove' ? '−' : ' '}
                    </span>
                    {entry.line || ' '}
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-0 rounded border border-gray-700 overflow-auto max-h-80 text-xs font-mono">
                <div className="border-r border-gray-700">
                  <div className="bg-gray-800 px-4 py-1.5 text-xs text-gray-500 uppercase tracking-wider sticky top-0">
                    Before
                  </div>
                  {diffLines
                    .filter((e) => e.type !== 'add')
                    .map((entry, i) => (
                      <div
                        key={i}
                        className={`px-4 ${
                          entry.type === 'remove'
                            ? 'bg-red-900/30 text-red-300'
                            : 'text-gray-400'
                        }`}
                      >
                        {entry.line || ' '}
                      </div>
                    ))}
                </div>
                <div>
                  <div className="bg-gray-800 px-4 py-1.5 text-xs text-gray-500 uppercase tracking-wider sticky top-0">
                    After
                  </div>
                  {diffLines
                    .filter((e) => e.type !== 'remove')
                    .map((entry, i) => (
                      <div
                        key={i}
                        className={`px-4 ${
                          entry.type === 'add'
                            ? 'bg-green-900/30 text-green-300'
                            : 'text-gray-400'
                        }`}
                      >
                        {entry.line || ' '}
                      </div>
                    ))}
                </div>
              </div>
            )}
          </section>
          {/* ── Eval Breakdown Comparison ── */}
          <section>
            <div className="text-xs uppercase tracking-wider text-gray-500 mb-3 font-semibold">
              Eval Breakdown
            </div>
            {evalData.length === 0 ? (
              <EmptyState message="No evaluation data to compare" />
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Radar Overlay */}
                <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                  <div className="text-xs text-gray-500 mb-2">Radar Comparison</div>
                  <ResponsiveContainer width="100%" height={260}>
                    <RadarChart data={evalData} cx="50%" cy="50%" outerRadius="75%">
                      <PolarGrid stroke="#374151" />
                      <PolarAngleAxis
                        dataKey="name"
                        tick={{ fill: '#9CA3AF', fontSize: 11 }}
                      />
                      <PolarRadiusAxis
                        domain={[0, (maxScore)]}
                        tick={{ fill: '#6B7280', fontSize: 10 }}
                        tickCount={5}
                      />
                      <Radar
                        name="Before"
                        dataKey="before"
                        stroke="#F87171"
                        fill="#F87171"
                        fillOpacity={0.15}
                        strokeWidth={2}
                      />
                      <Radar
                        name="After"
                        dataKey="after"
                        stroke="#34D399"
                        fill="#34D399"
                        fillOpacity={0.15}
                        strokeWidth={2}
                      />
                      <Legend
                        wrapperStyle={{ fontSize: 11, color: '#D1D5DB' }}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
                {/* Bar Pair Comparison */}
                <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
                  <div className="text-xs text-gray-500 mb-2">Bar Comparison</div>
                  <ResponsiveContainer width="100%" height={260}>
                    <BarChart
                      data={evalData}
                      margin={{ top: 8, right: 8, left: -16, bottom: 4 }}
                      barCategoryGap="20%"
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                      <XAxis
                        dataKey="name"
                        tick={{ fill: '#9CA3AF', fontSize: 10 }}
                        axisLine={{ stroke: '#4B5563' }}
                        tickLine={false}
                      />
                      <YAxis
                        domain={[0, maxScore]}
                        tick={{ fill: '#6B7280', fontSize: 10 }}
                        axisLine={false}
                        tickLine={false}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1F2937',
                          border: '1px solid #374151',
                          borderRadius: '6px',
                          fontSize: 12,
                          color: '#D1D5DB',
                        }}
                      />
                      <Bar dataKey="before" name="Before" radius={[3, 3, 0, 0]} maxBarSize={28}>
                        {evalData.map((_, idx) => (
                          <Cell key={idx} fill="#F87171" fillOpacity={0.7} />
                        ))}
                      </Bar>
                      <Bar dataKey="after" name="After" radius={[3, 3, 0, 0]} maxBarSize={28}>
                        {evalData.map((_, idx) => (
                          <Cell key={idx} fill="#34D399" fillOpacity={0.7} />
                        ))}
                      </Bar>
                      <Legend
                        wrapperStyle={{ fontSize: 11, color: '#D1D5DB' }}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
};
export default VersionDiff;
```