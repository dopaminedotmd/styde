┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\app-store-optimizer\BLUEPRINT.md → b/StydeAgents\blueprints\app-store-optimizer\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,15 +1,229 @@[0m
[38;2;184;134;11m # App Store Optimizer[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** app-dev **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+**Domain:** app-dev **Version:** 2[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Optimizes app store presence. ASO, screenshots, keywords, A/B testing listings.[0m
[38;2;255;255;255;48;2;19;87;20m+Optimizes app store presence across Google Play and Apple App Store via keyword research, screenshot generation, A/B testing, and strategic rating prompts.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Persona[0m
[38;2;184;134;11m ASO specialist. Expert in App Store Optimization, keyword research, and conversion optimization.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Keyword: research high-traffic app keywords[0m
[38;2;255;255;255;48;2;119;20;20m-- Screenshot: design compelling screenshot sets[0m
[38;2;255;255;255;48;2;119;20;20m-- Description: write optimized app descriptions[0m
[38;2;255;255;255;48;2;119;20;20m-- A/B: test listing variants for conversion[0m
[38;2;255;255;255;48;2;119;20;20m-- Rating: implement rating prompts strategically[0m
[38;2;255;255;255;48;2;19;87;20m+- Keyword: research high-traffic app keywords with locale-specific volume and difficulty scores[0m
[38;2;255;255;255;48;2;19;87;20m+- Screenshot: design compelling screenshot sets per store, device type, and locale[0m
[38;2;255;255;255;48;2;19;87;20m+- Description: write optimized app descriptions with keyword density < 3.5% per locale[0m
[38;2;255;255;255;48;2;19;87;20m+- A/B: test listing variants for conversion with minimum sample size of 1000 impressions per variant[0m
[38;2;255;255;255;48;2;19;87;20m+- Rating: implement rating prompts strategically with per-platform rate-limit rules[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Input / Output Schema[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Input (JSON)[0m
[38;2;255;255;255;48;2;19;87;20m+```json[0m
[38;2;255;255;255;48;2;19;87;20m+{[0m
[38;2;255;255;255;48;2;19;87;20m+  "app": {[0m
[38;2;255;255;255;48;2;19;87;20m+    "name": {"type": "string", "required": true, "max_length": 30},[0m
[38;2;255;255;255;48;2;19;87;20m+    "bundle_id": {"type": "string", "required": true, "pattern": "^com\\.[a-z0-9]+\\.[a-z0-9]+$"},[0m
[38;2;255;255;255;48;2;19;87;20m+    "category": {"type": "string", "enum": ["games", "productivity", "utilities", "finance", "health", "education", "social", "entertainment"]},[0m
[38;2;255;255;255;48;2;19;87;20m+    "primary_language": {"type": "string", "pattern": "^[a-z]{2}(-[A-Z]{2})?$", "default": "en-US"}[0m
[38;2;255;255;255;48;2;19;87;20m+  },[0m
[38;2;255;255;255;48;2;19;87;20m+  "locales": {[0m
[38;2;255;255;255;48;2;19;87;20m+    "type": "array",[0m
[38;2;255;255;255;48;2;19;87;20m+    "items": {"type": "string", "pattern": "^[a-z]{2}(-[A-Z]{2})?$"},[0m
[38;2;255;255;255;48;2;19;87;20m+    "min_items": 1,[0m
[38;2;255;255;255;48;2;19;87;20m+    "max_items": 50,[0m
[38;2;255;255;255;48;2;19;87;20m+    "default": ["en-US"][0m
[38;2;255;255;255;48;2;19;87;20m+  },[0m
[38;2;255;255;255;48;2;19;87;20m+  "keywords": {[0m
[38;2;255;255;255;48;2;19;87;20m+    "type": "array",[0m
[38;2;255;255;255;48;2;19;87;20m+    "items": {"type": "string", "max_length": 100},[0m
[38;2;255;255;255;48;2;19;87;20m+    "min_items": 0,[0m
[38;2;255;255;255;48;2;19;87;20m+    "max_items": 100,[0m
[38;2;255;255;255;48;2;19;87;20m+    "description": "Optional seed keywords. If empty, auto-generate from app metadata."[0m
[38;2;255;255;255;48;2;19;87;20m+  },[0m
[38;2;255;255;255;48;2;19;87;20m+  "competitors": {[0m
[38;2;255;255;255;48;2;19;87;20m+    "type": "array",[0m
[38;2;255;255;255;48;2;19;87;20m+    "items": {"type": "string"},[0m
[38;2;255;255;255;48;2;19;87;20m+    "max_items": 10,[0m
[38;2;255;255;255;48;2;19;87;20m+    "description": "Optional competitor bundle IDs for keyword gap analysis."[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Output[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+keywords:[0m
[38;2;255;255;255;48;2;19;87;20m+  recommended:[0m
[38;2;255;255;255;48;2;19;87;20m+    - term: "meditation timer"[0m
[38;2;255;255;255;48;2;19;87;20m+      locale: en-US[0m
[38;2;255;255;255;48;2;19;87;20m+      volume: 42000[0m
[38;2;255;255;255;48;2;19;87;20m+      difficulty: 0.65[0m
[38;2;255;255;255;48;2;19;87;20m+      priority: high[0m
[38;2;255;255;255;48;2;19;87;20m+      source: seed_expansion[0m
[38;2;255;255;255;48;2;19;87;20m+    # ... up to 100 per locale[0m
[38;2;255;255;255;48;2;19;87;20m+screenshots:[0m
[38;2;255;255;255;48;2;19;87;20m+  generated:[0m
[38;2;255;255;255;48;2;19;87;20m+    - store: ios_app_store[0m
[38;2;255;255;255;48;2;19;87;20m+      device: iphone_14_pro_max[0m
[38;2;255;255;255;48;2;19;87;20m+      locale: en-US[0m
[38;2;255;255;255;48;2;19;87;20m+      set:[0m
[38;2;255;255;255;48;2;19;87;20m+        - slot: 1[0m
[38;2;255;255;255;48;2;19;87;20m+          type: hero[0m
[38;2;255;255;255;48;2;19;87;20m+          asset_url: "screenshots/en-US/iphone/hero.png"[0m
[38;2;255;255;255;48;2;19;87;20m+          overlay_text: "Focus your mind, anywhere"[0m
[38;2;139;134;130m… omitted 158 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\app-store-optimizer\skills\screenshot.md → b/StydeAgents\blueprints\app-store-optimizer\skills\screenshot.md[0m
[38;2;139;134;130m@@ -0,0 +1,126 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# Screenshot Skill[0m
[38;2;255;255;255;48;2;19;87;20m+Generates production-ready app store screenshot sets per store, device, and locale.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Device Handling[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### iOS[0m
[38;2;255;255;255;48;2;19;87;20m+| Device              | Resolution       | Aspect ratio | Store              |[0m
[38;2;255;255;255;48;2;19;87;20m+|---------------------|------------------|--------------|--------------------|[0m
[38;2;255;255;255;48;2;19;87;20m+| iPhone 14 Pro Max   | 1290 x 2796      | 19.5:9       | App Store           |[0m
[38;2;255;255;255;48;2;19;87;20m+| iPhone 14 Pro       | 1179 x 2556      | 19.5:9       | App Store           |[0m
[38;2;255;255;255;48;2;19;87;20m+| iPhone 14           | 1170 x 2532      | 19.5:9       | App Store           |[0m
[38;2;255;255;255;48;2;19;87;20m+| iPhone 13 / 12      | 1170 x 2532      | 19.5:9       | App Store           |[0m
[38;2;255;255;255;48;2;19;87;20m+| iPhone SE (3rd gen) | 750 x 1334       | 16:9         | App Store           |[0m
[38;2;255;255;255;48;2;19;87;20m+| iPad Pro 12.9"      | 2048 x 2732      | 4:3          | App Store (optional)|[0m
[38;2;255;255;255;48;2;19;87;20m+| iPad Pro 11"        | 1668 x 2388      | 4:3          | App Store (optional)|[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Android[0m
[38;2;255;255;255;48;2;19;87;20m+| Device              | Resolution       | Aspect ratio | Store              |[0m
[38;2;255;255;255;48;2;19;87;20m+|---------------------|------------------|--------------|--------------------|[0m
[38;2;255;255;255;48;2;19;87;20m+| Pixel 7 Pro         | 1440 x 3120      | 19.5:9       | Google Play         |[0m
[38;2;255;255;255;48;2;19;87;20m+| Pixel 7             | 1080 x 2400      | 20:9         | Google Play         |[0m
[38;2;255;255;255;48;2;19;87;20m+| Samsung S23 Ultra   | 1440 x 3088      | 19.3:9       | Google Play         |[0m
[38;2;255;255;255;48;2;19;87;20m+| OnePlus 11          | 1440 x 3216      | 20:9         | Google Play         |[0m
[38;2;255;255;255;48;2;19;87;20m+| Huawei P60 Pro      | 1224 x 2700      | 19.8:9       | AppGallery          |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Desktop (for companion/store preview)[0m
[38;2;255;255;255;48;2;19;87;20m+| Platform    | Resolution   | Aspect ratio | Use case                    |[0m
[38;2;255;255;255;48;2;19;87;20m+|-------------|--------------|--------------|-----------------------------|[0m
[38;2;255;255;255;48;2;19;87;20m+| MacBook Pro | 1512 x 982   | 16:10        | App Store Connect preview   |[0m
[38;2;255;255;255;48;2;19;87;20m+| Windows     | 1920 x 1080  | 16:9         | promotional materials       |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Viewport Fallback[0m
[38;2;255;255;255;48;2;19;87;20m+When the exact device is unavailable, fall back in this order:[0m
[38;2;255;255;255;48;2;19;87;20m+1. Same device family, older model (e.g. iPhone 14 -> iPhone 13)[0m
[38;2;255;255;255;48;2;19;87;20m+2. Same aspect ratio, closest resolution[0m
[38;2;255;255;255;48;2;19;87;20m+3. Generic template at 1080x1920 (19.5:9 default)[0m
[38;2;255;255;255;48;2;19;87;20m+4. No-screenshot placeholder with error logged[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Timeout Per Screenshot Type[0m
[38;2;255;255;255;48;2;19;87;20m+| Type            | Timeout | Notes                           |[0m
[38;2;255;255;255;48;2;19;87;20m+|-----------------|---------|---------------------------------|[0m
[38;2;255;255;255;48;2;19;87;20m+| hero            | 60s     | Full scene render               |[0m
[38;2;255;255;255;48;2;19;87;20m+| feature         | 45s     | Feature highlight render        |[0m
[38;2;255;255;255;48;2;19;87;20m+| testimonial     | 30s     | Quote overlay on simple bg      |[0m
[38;2;255;255;255;48;2;19;87;20m+| demo animation  | 90s     | GIF/APNG generation             |[0m
[38;2;255;255;255;48;2;19;87;20m+| localized text  | 15s     | Text overlay only, reusing base |[0m
[38;2;255;255;255;48;2;19;87;20m+| placeholder     | 5s      | Minimal fallback asset          |[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Total batch timeout = max(individual timeout per type) * (number of screenshots in set). For 10-slot set with 2 heros + 4 features + 4 localized: 60 * 10 = 600s max.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Retry Counts[0m
[38;2;255;255;255;48;2;19;87;20m+Per the canonical retry policy in BLUEPRINT.md:[0m
[38;2;255;255;255;48;2;19;87;20m+- Screenshot generation: 2 retries with 5s linear backoff[0m
[38;2;255;255;255;48;2;19;87;20m+- Asset upload to store: 3 retries with exponential backoff (2s, 4s, 8s)[0m
[38;2;255;255;255;48;2;19;87;20m+- Localization text render: 1 retry, immediate[0m
[38;2;255;255;255;48;2;19;87;20m+- 429 (rate limit): follow Retry-After header, up to 3 additional retries[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+All retries log attempt count, error type, and elapsed time. Exhausted retries fall to error recovery.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Error Recovery Paths[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Generation Failure[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+render failed -> is file system full? -> yes: alert operator, no[0m
[38;2;255;255;255;48;2;19;87;20m+                |                                        |[0m
[38;2;255;255;255;48;2;19;87;20m+                ▼                                        ▼[0m
[38;2;255;255;255;48;2;19;87;20m+          is fallback device available?          wait 5s, retry[0m
[38;2;255;255;255;48;2;19;87;20m+                |                                        |[0m
[38;2;255;255;255;48;2;19;87;20m+           yes  |   no                                  |[0m
[38;2;255;255;255;48;2;19;87;20m+                ▼                                        ▼[0m
[38;2;255;255;255;48;2;19;87;20m+          re-render on           timeout?  --no-->  success[0m
[38;2;255;255;255;48;2;19;87;20m+          fallback device         |[0m
[38;2;255;255;255;48;2;19;87;20m+                                  ▼[0m
[38;2;255;255;255;48;2;19;87;20m+                            use placeholder[0m
[38;2;255;255;255;48;2;19;87;20m+                            log full error[0m
[38;2;255;255;255;48;2;19;87;20m+                            continue batch[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 48 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\app-store-optimizer\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\app-store-optimizer\config.yaml[0m
[38;2;139;134;130m@@ -11,7 +11,7 @@[0m
[38;2;184;134;11m   domain: app-dev[0m
[38;2;184;134;11m   last_reviewed: '2026-06-26'[0m
[38;2;184;134;11m   name: app-store-optimizer[0m
[38;2;255;255;255;48;2;119;20;20m-  version: 5.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 5.1.0[0m
[38;2;184;134;11m   version_history:[0m
[38;2;184;134;11m   - from: 1.0.0[0m
[38;2;184;134;11m     to: 1.0.1[0m
[38;2;139;134;130m@@ -97,6 +97,12 @@[0m
[38;2;184;134;11m     score: 87.2[0m
[38;2;184;134;11m     previous_score: 77.4[0m
[38;2;184;134;11m     timestamp: '2026-06-26T07:04:36Z'[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 5.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 5.1.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MINOR: input/output schema, retry consolidation, keyword refresh cadence, localization expansion, screenshot skill with production edge cases'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 87.2[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T09:09:00Z'[0m
[38;2;184;134;11m eval:[0m
[38;2;184;134;11m   benchmarks: [][0m
[38;2;184;134;11m   judge_model: deepseek-v4-pro[0m
All changes applied. Summary of v5.0.0 -> v5.1.0:
BLUEPRINT.md -- 15 lines -> 230 lines
- Input schema: JSON template with field types, constraints, required flags, regex patterns, enums, and defaults
- Output contract: YAML spec for keywords, screenshots, descriptions, A/B test variants with full field definitions
- Retry & Resilience: single canonical table covering all 5 operations with per-operation max retries, backoff strategy, timeout, and fallback behavior. HTTP 4xx/5xx/429 distinction specified.
- Keyword Refresh Cadence: 4-tier schedule (weekly/bi-weekly/monthly/on-demand) with source data logic, fallback thresholds, and step-by-step refresh pipeline
- Localization expansion: transliteration rules (ISO-15919/ICU, 0.8x weight for transliterated), character inflation per language group (CJK 0.35x, Arabic 1.2x, etc.), screenshot-text overlay strategy per store (Apple/Google/Huawei/Samsung with max chars, font ranges, language-aware wrap)
- RTL handling: auto-detect from locale, override support, text flip rules for overlays
- Decision tree: full ASCII flowchart from seed keywords through scoring, difficulty gates, competitor gap scan, to per-locale output
- Locale-to-ASO table: 16 locales with per-row keyword max, description max, screenshot slots, text direction, rating prompt policy
skills/screenshot.md -- new file
- Device resolution tables: iOS (7 devices), Android (5 devices), Desktop (2 platforms)
- Viewport fallback chain: exact device -> same family -> same aspect ratio -> generic 1080x1920 -> placeholder
- Timeout per type: hero 60s, feature 45s, testimonial 30s, demo animation 90s, localized text 15s, placeholder 5s, with batch timeout formula
- Retry counts: references canonical retry policy, adds 429 Retry-After handling
- Error recovery paths: three full flowcharts (generation failure, upload failure, localization failure) with decision nodes and terminal states
- Output contract: YAML field spec with rejection criteria (2px tolerance, overflow clipping, aspect ratio mismatch, checksum)