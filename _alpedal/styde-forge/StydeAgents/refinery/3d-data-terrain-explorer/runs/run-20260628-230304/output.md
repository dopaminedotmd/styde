BLUEPRINT.md currently describes Data Sonification Console (audio dashboard). Teacher feedback references 3D terrain concepts (terrain geometry, WebGL, computeVertexNormals, BufferAttribute) that don't match the current file. This indicates the evaluations ran against a prior 3D-terrain version that was since replaced with the audio blueprint.
I will apply the GENERIC feedback items (Data Contract, expanded Error Handling, Data Loading lifecycle) that are universally applicable to any blueprint, and adapt 3D-specific feedback items into audio equivalents where a mapping exists. The pure 3D-terrain items (terrain resolution tiers, WebGL fallback, computeVertexNormals dedup, BufferAttribute caching) are incompatible with the current audio-domain blueprint and will be noted as skipped.
Edits to apply to BLUEPRINT.md (E:\Stryde\_alpedal\styde-forge\BLUEPRINT.md):
---
EDIT 1 — Add Data Contract section before Data Ingestion (insert after line 60, before line 62):
```
## Data Contract
### Input Metric Schema
All metric payloads MUST conform to the following schema:
```
{
  "timestamp": number,          // Unix epoch ms, required, integer, >= 0
  "metrics": [
    {
      "id": string,              // required, non-empty, matches /^[a-zA-Z0-9_-]{1,64}$/
      "value": number | null,    // required, finite number or null (null = missing data point)
      "unit": string | null,     // optional, e.g. "ms", "rpm", "count"
      "tags": {                  // optional, max 16 key-value pairs
        "<string>": string
      }
    }
  ]
}
```
Constraints:
  - Max payload size: 256 KB uncompressed
  - Array cardinality: 1 <= metrics.length <= 64 per tick
  - Null values: propagate to the channel with gain = 0; do not skip or break the channel
  - Unknown fields: silently ignored, never thrown
### Valid Example Payload
```
{
  "timestamp": 1719000000000,
  "metrics": [
    {"id": "revenue", "value": 48300.5, "unit": "USD"},
    {"id": "error-rate", "value": 2.1, "unit": "percent"},
    {"id": "active-users", "value": 1423, "unit": "count"}
  ]
}
```
### Malformed Payload Examples
Scenario A — missing field:
```
{"timestamp": 1719000000000, "metrics": [{"id": "revenue"}]}
```
Expected: revenue channel receives null value → gain set to 0, no crash, no UI blink.
Scenario B — invalid type:
```
{"timestamp": "now", "metrics": [{"id": "revenue", "value": 100}]}
```
Expected: MetricBus rejects the tick, keeps last valid values for all channels, logs validation error to diagnostic panel.
Scenario C — overflow value:
```
{"timestamp": 1719000000000, "metrics": [{"id": "revenue", "value": Infinity}]}
```
Expected: clamp to channel max range boundary via isFinite check before mapping. Infinity and NaN are never passed to the mapping formula.
Scenario D — empty array:
```
{"timestamp": 1719000000000, "metrics": []}
```
Expected: the tick is valid but produces no audio output. Previous channel values persist. The diagnostic panel shows "silent tick" counter.
```
---
EDIT 2 — Expand Error-Handling Edge Cases (after line 301, append):
```
### Empty Dataset
When MetricBus receives its first tick and metrics array contains zero entries, or when all channels have null values simultaneously:
  1. All gain nodes remain at their current value (or initial 0 if no prior state)
  2. The ambient drone continues if active
  3. A "no data" indicator appears in the dashboard header
  4. On next valid tick, the indicator clears and normal audio resumes
  5. No errors, no tears, no console noise
### Missing Required Fields in Payload
For each metric in the incoming payload array:
  1. Validate metric.id exists, is non-empty string, and matches /^[a-zA-Z0-9_-]{1,64}$/
  2. If id is missing or invalid: skip that metric entry, log a warning with the entry index to the diagnostic panel, continue processing remaining entries
  3. Validate metric.value is a finite number or null
  4. If value is missing entirely: treat as null (same as missing data point)
  5. If value is present but not a number (string, object, array): log a type-error warning, skip that metric, continue
  6. The channel corresponding to a skipped metric retains its last known value
  7. After processing all entries, if zero metrics were valid, the entire tick is treated as empty tick (see Empty Dataset above)
### Numeric Overflow and NaN in Metric Values
Mapping formulas MUST guard against non-finite inputs:
  1. Before any call to LinearSlopeMapping, ExponentialSlopeMapping, or PowerLawNoiseMapping:
     a. v = Number(v) — coerce
     b. if !Number.isFinite(v): set v = channel's default value (configurable per channel, default 0)
     c. Increment a per-channel NaN/Infinity counter visible in the diagnostic panel
  2. If a channel receives 3 or more non-finite values within a 10-second sliding window:
     a. Reset the channel's gain to 0
     b. Flash the channel's UI panel red
     c. Set a 5-second cooldown timer before accepting new values from that metric
     d. Log "channel X: excessive non-finite values, cooling down" to diagnostic panel
  3. After cooldown expires, accept the next valid finite value and restore normal operation
### Network Failure on Data Ingestion
Ingestion paths MUST handle connection loss gracefully:
  1. WebSocket disconnect:
     a. Show a "connection lost" indicator (yellow banner, not a blocking modal)
     b. Start a 10-second reconnection timer using exponential backoff: 1s, 2s, 4s, 8s, 10s (cap)
     c. Each reconnect attempt increments a reconnect-count displayed in the diagnostic panel
     d. On reconnect success: clear the yellow banner, set reconnect-count back to 0, resume processing buffered metrics if buffer < 1000 entries, discard oldest if exceeded
     e. After 10 consecutive failed attempts: switch to "offline mode" — all channels continue at their last known values, ambient drone shifts to a lower register, UI shows persistent red banner. User must manually re-enable streaming or drop a file.
  2. POST endpoint timeout (> 5 seconds):
     a. Return HTTP 202 Accepted to the caller immediately
     b. Queue the payload for deferred processing
     c. If queue grows beyond 500 unprocessed payloads, start dropping oldest entries with a counter
  3. File-drop handler read error:
     a. Show a file-error overlay on the drop zone with the specific error message
     b. Allow re-drop without full page reload
     c. Supported formats: CSV, JSON. Unsupported formats show "unsupported format" message and are rejected without side effects
```
---
EDIT 3 — Add Data Loading subsection after Data Ingestion (after line 70):
```
## Data Loading Lifecycle
Every data ingestion cycle follows a four-phase pipeline:
  Fetch -> Parse -> Validate -> Render
### Phase 1 — Fetch
  - WebSocket: onmessage event pushes raw payload to a buffered queue. Queue depth = 1024 entries. If exceeded, oldest entry is dropped.
  - POST: request body is read as text, pushed to parse queue.
  - File-drop: FileReader reads the dropped file as text (readAsText), pushes to parse queue.
  - UI state during fetch: no visible indicator for WebSocket (always-connected). POST and file-drop show a brief spinner (max 200 ms blue pulse on the ingestion status dot).
### Phase 2 — Parse
  - All payloads are parsed via JSON.parse inside a try/catch.
  - On parse failure: the raw text is silently discarded. The diagnostic panel increments a parse-error counter.
  - If 5 consecutive parse failures occur within 1 second: show a "payload format error" warning in the dashboard header. User could check the diagnostic panel for details.
### Phase 3 — Validate
  - Each parsed metric entry runs through the Data Contract validation rules (see Data Contract section).
  - Invalid entries are skipped individually — one bad metric entry does not invalidate the entire payload.
  - After validation, the valid metric set is pushed to MetricBus for audio processing.
### Phase 4 — Render (Audio)
  - MetricBus fans out values to each channel's audio processing pipeline (mapping formula -> gain node -> master bus -> destination).
  - Channels process all updates from the same tick synchronously before the audio graph renders the next frame.
  - If no valid metrics arrived for more than 5 seconds while connected: a "stale data" indicator appears and the ambient drone fades to a lower volume by 3 dB over 1 second.
### Loading-State UI Requirements
  - Initial load (before first valid tick):
    Dashboard renders in full layout with all channel panels visible but dimmed. Each channel shows a skeleton bar (pulsing gray rectangle) where the volume slider would be. Center of dashboard shows a pulsing "awaiting data" indicator.
  - Data arriving:
    Skeletons dissolve to full controls with a 300 ms CSS fade. The "awaiting data" indicator disappears.
  - Timeout:
    If no data arrives within 30 seconds of dashboard load (or within 5 seconds of a connection re-establishment), the "awaiting data" indicator turns red and shows "no data received". Channel controls remain dimmed. User is prompted to check their data source or drop a file.
  - Reconnection:
    During reconnection, channels retain their last known values. Skeletons do NOT reappear. Only a thin yellow bar at the top of the dashboard indicates connection state.
```
---
EDIT 4 — Consolidate mute/solo routing into a decision tree (replace lines 24-35 with a mermaid-compatible decision table):
```
## Mute/Solo Routing Invariant — Decision Table
State combination and action after any mute or solo toggle:
  | Channel toggles | Current soloCount | Action |
  |---|---|---|
  | mute ON | any | Set channel gain = 0 immediately. No ramp. |
  | mute OFF | > 0 | If channel.solo == false: keep gain = 0 (soloed-out). If channel.solo == true: ramp gain to target via setTargetAtTime(tc=0.02). |
  | mute OFF | == 0 | Ramp gain to target via setTargetAtTime(tc=0.02). |
  | solo ON | == 0 | Increment soloCount to 1. Mute all non-soloed channels (gain.value = 0). |
  | solo ON | > 0 | Increment soloCount. Unmute channels with solo == true only. |
  | solo OFF | > 1 after | Decrement soloCount. Mute this channel (gain.value = 0). Non-soloed channels stay muted. |
  | solo OFF | == 0 after | Decrement soloCount to 0. Unmute ALL channels (restore pre-solo gain envelopes via setTargetAtTime(tc=0.02)). |
Implementation rule: every setTargetAtTime call on a gain node MUST go through a helper that checks the above table and reapplies the correct mute/solo state after scheduling. Do not call setTargetAtTime directly on gain nodes outside the helper.
soloCount is a global integer, incremented on solo-on, decremented on solo-off. It must never drop below 0. After source removal, soloCount is recalculated by scanning all remaining channels (as a safety net, not primary mechanism).
```
---
SKIPPED feedback items and rationale:
  - terrain geometry resolution tiers (low/medium/high): 3D-terrain specific, no audio equivalent. Skip.
  - WebGL unsupported environment: 3D-terrain specific. The audio equivalent (Web Audio API unsupported) is already covered in the existing Edge Cases section (lines 86-90).
  - computeVertexNormals dedup: 3D-terrain specific, no audio equivalent. Skip.
  - cache-vs-in-place decision tree for BufferAttribute: 3D-terrain specific. Audio equivalent (cache AudioNode vs create per tick) is already covered by Performance Constraints rule 5 (pre-wire oscillator graph, no disposable AudioNode creation per tick).
---
Final summary:
| Feedback item | Status |
|---|---|
| Data Contract section | ADDED (before Data Ingestion) |
| Error & Edge Case Handling expansion | ADDED (empty dataset, missing fields, NaN/overflow, network failure) |
| Resolution & Responsiveness subsection | SKIPPED — 3D-terrain specific, no audio equivalent |
| Data Loading lifecycle subsection | ADDED (Fetch->Parse->Validate->Render with UI states) |
| Dedup computeVertexNormals | SKIPPED — 3D-terrain specific, no audio equivalent |
| Cache-vs-in-place decision tree | ADAPTED — mute/solo routing consolidated into decision table (replaces raw prose) |
Want me to apply these edits to the file with write_file now, or keep as a review diff?