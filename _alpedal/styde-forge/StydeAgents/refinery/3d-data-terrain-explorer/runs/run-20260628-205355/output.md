┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\blueprints\std\3D Data Terrain Explorer\BLUEPRINT.md → b/E:\Stryde\_alpedal\styde-forge\blueprints\std\3D Data Terrain Explorer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -52,6 +52,34 @@[0m
[38;2;184;134;11m - Zero computeVertexNormals() calls during hot-path playback (cached geometry swap)[0m
[38;2;184;134;11m - One getHeightData() call per frame max (memoized, shared across terrain + rivers + particles)[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+## Error and Edge Cases[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### WebGL Unsupported[0m
[38;2;255;255;255;48;2;19;87;20m+- Detect via canvas.getContext('webgl2') at init; if null, try webgl fallback[0m
[38;2;255;255;255;48;2;19;87;20m+- If both fail, render a DOM-based fallback message panel: "3D terrain requires WebGL. Please use Chrome, Firefox, or Edge."[0m
[38;2;255;255;255;48;2;19;87;20m+- Fallback panel must match dark theme styling and include a browser download link[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Zero-Area Heightfield (Flat Terrain)[0m
[38;2;255;255;255;48;2;19;87;20m+- If max(heightData) - min(heightData) < 0.001, terrain is flat — no peaks or valleys to visualize[0m
[38;2;255;255;255;48;2;19;87;20m+- Add a subtle wave displacement in the fragment shader (sin-based, 0.02 units amplitude) so the surface is not invisible[0m
[38;2;255;255;255;48;2;19;87;20m+- Display an info toast: "Metrics are constant — terrain flattened. Inject variance for 3D relief."[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### NaN or Infinity in Height Data[0m
[38;2;255;255;255;48;2;19;87;20m+- Pre-process heightData with Number.isFinite() check before BufferGeometry attribute upload[0m
[38;2;255;255;255;48;2;19;87;20m+- Clamp non-finite values to 0.0 and log count to console as a warning: "NaN/Inf found in height data: N values clamped to 0"[0m
[38;2;255;255;255;48;2;19;87;20m+- Prevent corrupted vertex positions that would break normal computation or produce rendering artifacts[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Non-Power-of-Two Heightfield Resolution[0m
[38;2;255;255;255;48;2;19;87;20m+- Grid dimensions (GRID x GRID) do not need to be power-of-two — BufferGeometry accepts any vertex count[0m
[38;2;255;255;255;48;2;19;87;20m+- However, avoid prime-number grid sizes where normal computation becomes numerically unstable; prefer even dimensions[0m
[38;2;255;255;255;48;2;19;87;20m+- If the input resolution is very large (e.g. 1000x1000), down-sample via nearest-neighbor sampling to the configured GRID before building geometry[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Memory Bounds for Large Heightfield Arrays[0m
[38;2;255;255;255;48;2;19;87;20m+- Hard cap: GRID maxes at 200x200 (40,000 vertices, ~80k triangles). Above this, warn and clamp[0m
[38;2;255;255;255;48;2;19;87;20m+- If input data exceeds GRID^2 elements, truncate silently with a console warning showing truncated count[0m
[38;2;255;255;255;48;2;19;87;20m+- GEO_CACHE_BUDGET * vertices * (position + normal + color attributes + index) must not exceed 250MB system memory[0m
[38;2;255;255;255;48;2;19;87;20m+- Defensive check at cache insert: reject geometry sizes > 30MB and log a warning[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;184;134;11m ## Compatibility Requirements[0m
[38;2;184;134;11m - importmap must specify Three.js v0.170.0 ESM via jsdelivr CDN[0m
[38;2;184;134;11m - CDN import style matches Three.js build target: use `three.module.js` (ESM) + `examples/jsm/` for addons[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-sections.ps1 → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-blueprint-sections.ps1[0m
[38;2;139;134;130m@@ -0,0 +1,90 @@[0m
[38;2;255;255;255;48;2;19;87;20m+param([string]$Path)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+$errors = @()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check file exists[0m
[38;2;255;255;255;48;2;19;87;20m+if (-not (Test-Path $Path)) {[0m
[38;2;255;255;255;48;2;19;87;20m+    Write-Host "FAIL: Blueprint file not found at $Path"[0m
[38;2;255;255;255;48;2;19;87;20m+    exit 1[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+$content = Get-Content $Path -Raw[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Expected sections in order[0m
[38;2;255;255;255;48;2;19;87;20m+$sections = @([0m
[38;2;255;255;255;48;2;19;87;20m+    'Purpose',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Persona',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Skills',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Performance',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Error and Edge Cases',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Compatibility Requirements',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Validation Criteria',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Output'[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Write-Host "Checking section order..."[0m
[38;2;255;255;255;48;2;19;87;20m+$prevIdx = -1[0m
[38;2;255;255;255;48;2;19;87;20m+foreach ($sec in $sections) {[0m
[38;2;255;255;255;48;2;19;87;20m+    $idx = $content.IndexOf("## $sec")[0m
[38;2;255;255;255;48;2;19;87;20m+    if ($idx -eq -1) {[0m
[38;2;255;255;255;48;2;19;87;20m+        $errors += "MISSING: Section '## $sec' not found"[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    elseif ($idx -le $prevIdx) {[0m
[38;2;255;255;255;48;2;19;87;20m+        $errors += "ORDER: Section '$sec' appears out of order (at $idx, previous at $prevIdx)"[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+    $prevIdx = $idx[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Write-Host "Checking Error sub-sections..."[0m
[38;2;255;255;255;48;2;19;87;20m+$errorSubs = @([0m
[38;2;255;255;255;48;2;19;87;20m+    'WebGL Unsupported',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Zero-Area Heightfield',[0m
[38;2;255;255;255;48;2;19;87;20m+    'NaN or Infinity in Height Data',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Non-Power-of-Two Heightfield Resolution',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Memory Bounds for Large Heightfield Arrays'[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+foreach ($sub in $errorSubs) {[0m
[38;2;255;255;255;48;2;19;87;20m+    if ($content -notmatch [regex]::Escape("### $sub")) {[0m
[38;2;255;255;255;48;2;19;87;20m+        $errors += "MISSING: Error sub-section '### $sub'"[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Write-Host "Checking keywords..."[0m
[38;2;255;255;255;48;2;19;87;20m+$keywords = @([0m
[38;2;255;255;255;48;2;19;87;20m+    'canvas.getContext',[0m
[38;2;255;255;255;48;2;19;87;20m+    'Number.isFinite',[0m
[38;2;255;255;255;48;2;19;87;20m+    'max(heightData) - min(heightData)',[0m
[38;2;255;255;255;48;2;19;87;20m+    'GEO_CACHE_BUDGET',[0m
[38;2;255;255;255;48;2;19;87;20m+    'GRID maxes at 200'[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+foreach ($kw in $keywords) {[0m
[38;2;255;255;255;48;2;19;87;20m+    if ($content -notmatch [regex]::Escape($kw)) {[0m
[38;2;255;255;255;48;2;19;87;20m+        $errors += "MISSING keyword: '$kw'"[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Check no unwanted artifacts from old feedback[0m
[38;2;255;255;255;48;2;19;87;20m+Write-Host "Checking for removed artifacts..."[0m
[38;2;255;255;255;48;2;19;87;20m+$unwanted = @([0m
[38;2;255;255;255;48;2;19;87;20m+    'Quality Standards',[0m
[38;2;255;255;255;48;2;19;87;20m+    'DO NOT extract',[0m
[38;2;255;255;255;48;2;19;87;20m+    'omit-list',[0m
[38;2;255;255;255;48;2;19;87;20m+    'persona.md'[0m
[38;2;255;255;255;48;2;19;87;20m+)[0m
[38;2;255;255;255;48;2;19;87;20m+foreach ($bad in $unwanted) {[0m
[38;2;255;255;255;48;2;19;87;20m+    if ($content -match [regex]::Escape($bad)) {[0m
[38;2;255;255;255;48;2;19;87;20m+        $errors += "STALE ARTIFACT FOUND: '$bad' should not appear"[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;139;134;130m… omitted 12 diff line(s) across 1 additional file(s)/section(s)[0m
Direktläsning bekräftar att ändringen sitter korrekt. Error & Edge Cases-sektionen (raderna 55-81) är intakt med alla 5 sub-sektioner, rätt placerad mellan Performance och Compatibility Requirements. Inga ytterligare verifieringssteg behövs — blueprint.md är en dokumentationsfil utan bygg/test-kedja.