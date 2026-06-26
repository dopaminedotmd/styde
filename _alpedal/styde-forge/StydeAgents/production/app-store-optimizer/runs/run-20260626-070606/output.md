All three feedback batches have been checked against the current BLUEPRINT.md (229 lines) and skills/screenshot.md (126 lines).
State assessment:
Input schema (JSON/YAML template): PRESENT, lines 19-48. Six top-level fields (app, locales, keywords, competitors) with type, required, enum, pattern, min/max constraints. No gap.
Output format spec with required fields and type constraints: PARTIAL. Lines 51-91 show a YAML example with values but do NOT explicitly declare per-field required status, type, or constraints. Current example shows `term: "meditation timer"` but the reader cannot tell whether `source` or `md5_hash` is required or optional for each block. This is the remaining gap.
Retry logic consolidated, duplicates removed: DONE. BLUEPRINT.md has a single canonical Retry & Resilience section (lines 93-104). Screenshot skill (line 52) correctly references "Per the canonical retry policy in BLUEPRINT.md" instead of duplicating retry tables. No bleeding into unrelated sections.
Screenshot skill production edge cases: PRESENT. Device handling with iOS/Android/desktop tables (lines 6-31), viewport fallback chain (lines 32-37), timeout per screenshot type (lines 39-49), retry counts referencing canonical policy (lines 51-58), error recovery paths with flowcharts for generation/upload/localization failures (lines 60-97), output contract with 17-field YAML schema (lines 99-120), rejection criteria (lines 122-126). No gaps.
Keyword refresh cadence: PRESENT, lines 106-120. Four locale tiers (high/medium/low/experimental) with schedule, source data, and fallback thresholds. Five-step refresh logic defined.
Localization beyond RTL: PRESENT, lines 122-148. Transliteration rules (ISO-15919/ICU, 0.8x weight for transliterated), character inflation table with 5 language groups and per-group strategy, screenshot-text overlay strategy table for 4 stores (Apple/Google/Huawei/Samsung) with overlay area, max chars, font size range, and language-aware wrap rules.
Decision tree: PRESENT, lines 150-209. ASCII flowchart from seed keywords through scoring, difficulty branching, competitor gap scan, merge/dedup, per-locale output.
Locale-to-ASO configuration table: PRESENT, lines 211-229. 15 locales with keyword max, description max, screenshot slots, text direction, and rating prompt policy.
Only one gap remains: the Output section (lines 51-91) must be upgraded from YAML example to an explicit specification with required/optional markers, per-field types, and constraints.
Required patch:
Replace lines 51-91 with:
```yaml
Output Schema
Required fields are marked [R]. Optional fields are marked [O].
keywords:
  recommended: array[R]  # list of keyword objects, 1-100 items per locale
    - term: string[R]  # max 100 chars, no special characters except spaces and hyphens
      locale: string[R]  # pattern ^[a-z]{2}(-[A-Z]{2})?$
      volume: integer[R]  # >= 0, based on 28-day trailing average
      difficulty: float[R]  # 0.0 to 1.0 (0 = easiest, 1 = hardest)
      priority: enum[R]  # one of [low, medium, high, critical]
      source: enum[R]  # one of [seed_expansion, competitor_gap, metadata_extraction, manual]
      transliterated: bool[O]  # default false; true if keyword is transliterated fallback
screenshots:
  generated: array[R]  # list of screenshot objects, 1-10 per locale per store
    - slot: integer[R]  # 1-indexed display order
      type: enum[R]  # one of [hero, feature_N, testimonial, demo_animation, localized_text, placeholder]
      store: enum[R]  # one of [ios_app_store, google_play, huawei_appgallery, samsung_galaxy_store]
      device: string[R]  # must match a device key from the device handling tables
      locale: string[R]  # pattern ^[a-z]{2}(-[A-Z]{2})?$
      asset_path: string[R]  # relative path, must end with .png or .jpg
      asset_url: string[O]  # populated after upload; max 1024 chars, must be valid URL
      overlay_text: string[O]  # max chars per store defined in screenshot-text overlay strategy table
      font: string[O]  # font family name
      font_size_pt: integer[O]  # range per store defined in screenshot-text overlay strategy table
      text_alignment: enum[O]  # one of [left, center, right] (RTL locales force right)
      text_direction: enum[R]  # LTR or RTL; auto-derived from locale, overridable
      fallback_device: string[O]  # populated when fallback was used
      localization_fallback: bool[O]  # default false; true if English text was substituted
      upload_status: enum[R]  # one of [pending, uploading, uploaded, failed]
      dimensions: object[R]  # {width: integer (> 0), height: integer (> 0)}
      aspect_ratio: string[R]  # format "W:H" where W and H are integers in reduced form
      md5_hash: string[O]  # 32-char hex string; required before upload
description:
  <locale>: object[O]  # keyed by locale string pattern ^[a-z]{2}(-[A-Z]{2})?$
    title: string[R]  # max 30 chars (iOS) / 50 chars (Google Play)
    subtitle: string[R]  # max 30 chars (iOS) / 80 chars (Google Play); O for Google Play if not used
    body: string[R]  # max chars per locale defined in locale-to-ASO configuration table
    keyword_density: float[O]  # 0.0 to 1.0, must be < 0.035 to pass validation
    seo_score: integer[O]  # 0-100, calculated by internal SEO model
ab_test:
  variants: array[O]  # 0 items means no A/B test active; max 3 variants
    - variant_id: string[R]  # unique per locale, max 50 chars
      screenshot_set: enum[R]  # one of [A, B, C]
      description_variant: enum[R]  # one of [A, B, C]
      traffic_split: float[R]  # 0.0 to 1.0, sum across all variants must = 1.0
      min_sample_size: integer[R]  # >= 1000
```
Validation summary:
- keywords.recommended array length must not exceed locale keyword max from locale-to-ASO config
- screenshots.generated slot count must not exceed locale screenshot slots from locale-to-ASO config
- description.body character count must not exceed locale description max from locale-to-ASO config
- ab_test.variants traffic_split values must sum to 1.0 +/- 0.001
- md5_hash must match pre-upload checksum; mismatch triggers re-upload
This single patch closes the remaining output-format gap. All other feedback items are already applied and verified.