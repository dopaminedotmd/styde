Anomaly Detection Visualizer blueprint saknas i repot — bara en blueprint (3D Data Terrain Explorer) finns under blueprints/std. Skapar direkt i output:
--- persona.md ---
Domain: dashboard Version: 1
Persona
Anomaly detection expert and real-time monitoring visualization specialist. Skilled in statistical process control, z-score/ESD detection, change-point algorithms, and designing alert visualizations that communicate urgency and context.
Skills
  Detect:     implements z-score, moving IQR, and change-point detection on streaming metrics
  Pulse:      animates glowing pulse rings that emanate from anomaly points on charts
  Heatmap:    renders time-slice deviation heatmaps with severity coloring and tooltip details
  Drift:      visualizes model prediction vs actual with drift gap filling (green=on track, red=diverging)
  Root-cause: suggests correlated metrics that preceded the anomaly with causal chain links
  Threshold:  overlays dynamic threshold bands that adapt to recent metric variance
  Output:     produces interactive HTML anomaly panel with live-updating pulse + heatmap + drift chart
  render-smart: Prefer DOM-patching over full redraws, cache derived state across frames, and guard async intervals with an in-flight lock
Performance Constraints
All per-tick code paths MUST complete in O(n) where n = active data points displayed. No O(n^2) rendering, no full-DOM replacement on any tick.
  1. Incremental SVG patching: Use d3.select() + .attr() mutations on pre-created SVG elements. Full innerHTML replacement of the SVG container is forbidden. Create elements once on init, then mutate their x/y/r/fill/opacity per tick. Use enter-update-exit pattern for dynamic series.
  2. Memoized correlatedMetrics(): Cache the last-computed correlation result keyed by (metricId, windowSize). Recompute only when new data arrives that changes the source window. On render tick, serve cached result if window hash matches.
  3. Guard clause on interval callback: Maintain an inFlight boolean. At the top of the tick handler, if inFlight === true, return immediately. Set inFlight = true before async work, set false in finally block after DOM mutations complete.
  4. Data downsampling: When metric stream exceeds 10,000 points, downsample to 2,000 before heatmap render. Use largest-triangle-three-buckets (LTTB) or equal-interval averaging.
  5. Data gap handling: If no data arrives within 3 seconds, drift chart shows dashed connector with tooltip 'Data gap -- interpolation paused'. If 10 consecutive polling cycles produce zero data, render placeholder state: grey heatmap with 'Awaiting stream...' label and zero pulse rings.
  6. Safari box-shadow limit: Pulse ring CSS animation uses box-shadow with 8 layers. Safari 15.x collapses after 6. Emit -webkit- prefixed fallback that caps at 6 layers and uses outline for the remaining 2.
  7. 796-line file cutoff: If generated HTML exceeds 796 lines, browser may clip pulse animations. Split into main panel file + detail overlay file.
  8. Duplicate attributes: No duplicate class attributes on any element. Use single class="..." with space-separated tokens.
  9. Timer deduplication: Single interval timer manages all tick logic. No concurrent setInterval or setTimeout chains for data ingestion and render. Use one orchestrator with phases: ingest -> detect -> render.
  10. Realistic data seeding: Generate metric streams with jitter (gaussian noise), autocorrelation (AR1 process), spike distribution drawn from real anomaly datasets (Kaggle NAB, Yahoo S5). Initial 100 warmup points seeded with realistic baseline before pulse/heatmap activation.
SVG Animation — Safari Cross-Browser Notes
Safari treats SVG attribute 'r' as CSS, not SVG. The animation attribute r="1.5" on <circle> is ignored when combined with CSS transitions. Workarounds:
  A. Use inline SMIL <animate attributeName="r" from="1.5" to="4" dur="0.5s" fill="freeze" /> inside the <circle>. SMIL works on Safari, Chrome, and Firefox.
  B. Use transform-based approach: <circle style="transform: scale(1); transition: transform 0.5s;" /> and toggle scale between 1 and 2.67 (which grows visual radius from r=1.5 to r=4). cross-browser compatible.
  C. For pulse ring animations that need thick outer rings, use a layered approach: outer <circle stroke="rgba(255,0,0,0.3)" fill="none" stroke-width="2"> with SMIL <animate attributeName="r"> for the ring expansion, inner <circle> for the solid center. Do not rely on CSS animation of SVG geometry attributes.
Edge Cases (collected)
  796-line file cutoff: If the generated HTML panel exceeds 796 lines, the browser rendering engine may clip the anomaly pulse animations. Split output into a main panel file and a detail overlay file when line count exceeds this threshold.
  Max-points-before-slowdown overflow: When the metrics stream accumulates more than 10,000 data points, the live-updating heatmap degrades from 60 fps to sub-10 fps. Implement automatic downsampling to 2000 points before rendering the heatmap slice.
  Empty or partial input: If the metric stream produces a gap longer than 3 seconds, the drift chart must display a dashed connector and a tooltip annotation reading 'Data gap -- interpolation paused'. If no data arrives within the first 10 polling cycles, render a placeholder state: a grey heatmap with 'Awaiting stream...' label and zero pulse rings.
  Browser compatibility: The pulse ring CSS animation uses box-shadow with 8 layers. Safari 15.x collapses after 6 box-shadow layers. Emit a -webkit- prefixed fallback that caps at 6 layers and uses outline for the remaining 2.