App Store Optimizer
Domain: app-dev Version: 2
Purpose
Optimizes app store presence across Google Play and App Store. ASO keyword research, screenshot generation, description writing, A/B test management, rating prompts, localization compliance. Designed for production automation with validated schemas, retry-safe execution, and rollback safety.
Persona
ASO specialist. Expert in App Store Optimization, keyword research, and conversion optimization.
Skills
  Keyword: research high-traffic app keywords across 40+ locales with competition scoring
  Screenshot: design and render production screenshot sets for iOS and Android with viewport fallback chains
  Description: write keyword-optimized app descriptions with character budgets per store
  A/B: test listing variants for conversion with statistical significance gates
  Rating: implement strategic rating prompts with timing rules and suppression logic
---
Input Schema
The blueprint accepts the following payload. All fields are required unless marked optional.
yaml
input:
  app:
    name: string                # App display name, max 30 chars
    subtitle: string            # iOS subtitle, max 30 chars
    bundle_id: string           # e.g. com.example.myapp
    platform: string            # "ios" | "android" | "both"
  stores:
    google_play:                # Optional. If omitted, skip Google Play output
      short_description: string # max 80 chars
      full_description: string  # max 4000 chars
      category: string          # Must be valid Google Play category slug
    app_store:                  # Optional. If omitted, skip App Store output
      keywords: string          # Comma-separated, max 100 chars total
      promotional_text: string  # max 170 chars
      description: string       # max 4000 chars
  locales:
    - string                    # BCP-47 locale codes, e.g. en-US, ja-JP, ar-SA
  screenshots:
    count_per_device: integer   # 1-10, default 5
    devices:
      - string                  # "iphone_6.5" | "iphone_5.5" | "ipad_12.9" |
                                # "android_phone_6.7" | "android_tablet_10.5"
    style: string               # "screenshot_only" | "device_frame" | "hero_banner"
  ab_test:
    enabled: boolean            # default false
    variants: integer           # 2-5, number of listing variants
    traffic_split: string       # "even" | "weighted:{variant_1_pct}:{variant_2_pct}:..."
    minimum_sample_size: integer # minimum installs per variant before decision
    metric: string              # "conversion_rate" | "impression_rate" | "retention"
    significance_threshold: float # default 0.95
  rating_prompt:
    enabled: boolean            # default true
    min_days_after_install: integer # default 3
    max_prompts_per_user: integer   # default 2
    suppress_after_review: boolean  # default true
Output Schema
yaml
output:
  metadata:
    blueprint_version: string   # "2"
    generated_at: string        # ISO 8601
    locale_count: integer
    total_screenshots: integer
  listings:
    - locale: string            # BCP-47
      store: string             # "google_play" | "app_store"
      title: string
      subtitle: string          # iOS only
      short_description: string # Google Play only
      full_description: string
      keywords: string[]        # Individual keyword tokens
      category: string          # Google Play category slug
      character_counts:
        title: integer          # Must be <= store limit
        description: integer
        keywords: integer
      status: string            # "valid" | "truncated" | "rejected"
      rejection_reasons: string[] # Empty if valid
  screenshots:
    - locale: string
      device: string
      index: integer            # 1-based display order
      screenshot_path: string   # Relative or CDN URL
      dimensions:
        width: integer
        height: integer
      file_size_bytes: integer
      style: string
      status: string            # "generated" | "fallback" | "failed"
      fallback_used: string|nil # Device fallback chain applied if any
  ab_test_results:
    variant_id: integer
    metric: string
    current_conversion_rate: float
    sample_size: integer
    confidence: float
    is_winner: boolean
    rollback_to_previous: boolean # True if regression detected
  rating_prompt_plan:
    enabled: boolean
    triggers:
      first_prompt: string      # Event name, e.g. "after_3rd_session"
      cooldown_days: integer
      max_lifetime: integer
Rejection Criteria
A listing is rejected if any condition below is true. The rejection_reasons array lists all violations.
- title exceeds store character limit (Google Play: 50, App Store: 30)
- description exceeds 4000 chars on either store
- Google Play short_description exceeds 80 chars
- App Store keywords field exceeds 100 chars
- Google Play category is not in the allowed list (see Compliance & Localization)
- keyword_character_budget exceeded per locale: 5000 chars for Google Play, 100 chars comma-separated for App Store
- keyword_set contains stop words or competitor brand names defined in reject_list
- keyword_set for a locale is empty after deduplication
- screenshot count < minimum_per_device (1) or > maximum_per_device (10)
- screenshot dimensions do not match any supported device resolution for the target store
- screenshot file_size_bytes > 5 MB
- ab_test variants < 2 or > 5
- ab_test traffic_split percentages do not sum to 100
- ab_test minimum_sample_size < 50
Compliance & Localization
Google Play keyword limits:
  Full listing description: 4000 chars
  Short description: 80 chars
  Title: 50 chars
  Keyword field: N/A (keywords embedded in description text; no explicit keyword field)
  Effective keyword character budget: 4000 chars across full_description for ASO
  Keywords beyond 80 chars in short_description are ignored by ranking
App Store keyword limits:
  Title: 30 chars
  Subtitle: 30 chars
  Keyword field: 100 chars comma-separated (no spaces between commas)
  Promotional text: 170 chars
  Description: 4000 chars
Store category constraints:
  Google Play category must match one of: GAME, APPLICATION, GAME_ACTION, GAME_ADVENTURE, GAME_ARCADE, GAME_BOARD, GAME_CARD, GAME_CASINO, GAME_CASUAL, GAME_EDUCATIONAL, GAME_MUSIC, GAME_PUZZLE, GAME_RACING, GAME_ROLE_PLAYING, GAME_SIMULATION, GAME_SPORTS, GAME_STRATEGY, GAME_TRIVIA, GAME_WORD, APPLICATION_BUSINESS, APPLICATION_COMICS, APPLICATION_COMMUNICATION, APPLICATION_EDUCATION, APPLICATION_ENTERTAINMENT, APPLICATION_FINANCE, APPLICATION_HEALTH_AND_FITNESS, APPLICATION_LIBRARIES_AND_DEMO, APPLICATION_LIFESTYLE, APPLICATION_MEDIA_AND_VIDEO, APPLICATION_MEDICAL, APPLICATION_MUSIC_AND_AUDIO, APPLICATION_NEWS_AND_MAGAZINES, APPLICATION_PERSONALIZATION, APPLICATION_PHOTOGRAPHY, APPLICATION_PRODUCTIVITY, APPLICATION_SHOPPING, APPLICATION_SOCIAL, APPLICATION_SPORTS, APPLICATION_TOOLS, APPLICATION_TRAVEL_AND_LOCAL, APPLICATION_VIDEO_PLAYERS, APPLICATION_WEATHER
  App Store category derived from bundle_id primary category in App Store Connect; no category string in listing payload
Per-locale keyword deduplication:
  For each locale, keyword tokens are:
  1. Lowercased and stripped of punctuation
  2. Deduplicated (each unique word appears once)
  3. Filtered against a reject_list per locale (brand names, generic stop words, competitor terms)
  4. Sorted by estimated traffic volume descending
  5. Truncated to fit character budget (5000 for Google Play, 100 char comma-string for App Store)
Right-to-left text handling:
  When locale is ar-SA, he-IL, fa-IR, ur-PK, or other RTL BCP-47 codes:
    All description and title text is stored as-is (Unicode bidirectional)
    Display direction metadata set to "rtl" in output listing
    Screenshot text overlay renders with right-alignment
    Keyword analysis uses RTL-aware tokenization (break on whitespace, not leading/trailing)
Character Density Specification
All length constraints use characters (Unicode code points) as the canonical unit. Tokens are counted as individual characters, not tokens.
Conversion table for token-limited channels:
  Channel               Token budget   Equivalent characters (approx)
  Google Play title     50 chars       50 characters
  Google Play short     80 chars       80 characters
  Google Play full      4000 chars     4000 characters
  App Store title       30 chars       30 characters
  App Store subtitle    30 chars       30 characters
  App Store keywords    100 chars      100 characters (as comma-separated string)
  App Store promo text  170 chars      170 characters
  App Store description 4000 chars     4000 characters
  SMS/MMS               ~160 chars     Target 140 to leave room for URL (approx 120-150 chars)
  Twitter/X post        280 chars      280 characters (hard limit)
  Push notification     120 chars      120 characters (iOS), 80 (Android summary)
Character budget supersedes token budget when both apply. No token-level truncation is performed; character-level count is the gate.
A/B Testing & Rollback
Traffic splitting:
  evenly across variants. Example with 3 variants: 33.3% each.
  Option for weighted split defined in input: "weighted:50:30:20" for 50%/30%/20%.
Minimum sample size calculation:
  sample_size = (Z^2 * p * (1-p)) / E^2
  where:
    Z = 1.96 (for 95% confidence)
    p = estimated baseline conversion rate (from input or last known)
    E = desired margin of error (default 0.02)
  Minimum enforced at 50 installs per variant regardless of formula result.
Decision rules:
  Wait until every variant meets minimum_sample_size.
  Compute two-tailed p-value between each variant and control (variant 0).
  Declare winner if p < 0.05 AND conversion rate > control by > E.
  If no variant meets both criteria, extend test. If test runs 30 days without winner, declare inconclusive and keep control.
Rollback:
  On metric regression exceeding 10% relative drop from pre-test baseline:
    Stop test immediately
    Revert all listings to pre-test state (stored in output.metadata.previous_blueprint_hash)
    Flag ab_test_results.rollback_to_previous = true
  The previous_blueprint_hash is captured at the start of each ab_test run and stored alongside the output.
  Rollback auto-triggers a webhook notification if a webhook_url is configured in input (optional field).
Retry Logic
All operations that make network calls or generate external assets follow this canonical retry pattern.
  retry:
    max_attempts: 3
    base_delay_seconds: 1
    backoff_multiplier: 2
    max_delay_seconds: 30
    retryable_statuses:
      - 429                   # Rate limited
      - 502                   # Bad gateway
      - 503                   # Service unavailable
      - 504                   # Gateway timeout
    retryable_exceptions:
      - ConnectionError
      - TimeoutError
      - SSLError
    non_retryable:
      - 400                   # Bad request (schema validation failure)
      - 401                   # Unauthorized
      - 403                   # Forbidden
      - 404                   # Not found
      - 422                   # Unprocessable entity (schema violation)
    jitter: true              # Add random 0-1000ms jitter to each delay
Implementation contract: every function that hits an external API or renders a screenshot MUST wrap the call in this retry logic. Functions that catch a non-retryable error MUST surface the full error payload in output.
There is no other retry specification anywhere in this blueprint. The screenshot skill, keyword lookup, description generation, and A/B test data fetching all reference this single section.
Localization note: All project documentation, this blueprint included, is in English per convention. No Swedish in any outputs.
Screenplay specification (skills/screenshot.md)
Screenshot skill
Purpose
Generate production-ready screenshot sets for iOS and Android app store listings. Supports device framing, raw screenshots, and hero banner styles. Handles viewport fallback, per-type timeouts, retry via canonical retry logic, and error recovery.
Device handling
Supported devices and their required resolutions:
  iPhone 6.5 (iOS):            1248 x 2688  (portrait), 2688 x 1248 (landscape)
  iPhone 5.5 (iOS):            1242 x 2208  (portrait), 2208 x 1242 (landscape)
  iPad 12.9 (iOS):             2048 x 2732  (portrait), 2732 x 2048 (landscape)
  Android phone 6.7 (Android): 1080 x 2400  (portrait)
  Android tablet 10.5 (Android): 1600 x 2560 (landscape)
Input must specify device strings exactly as listed above. Unknown device string causes immediate rejection with rejection_reason "unsupported_device".
Viewport fallback chain
When the exact device resolution cannot be served (e.g. test environment lacks that device profile), apply the following fallback in order:
  iPhone 6.5 -> iPhone 5.5 (scale up, crop to fit) -> iPad 12.9 (letterbox to fill) -> reject
  iPhone 5.5 -> iPhone 6.5 (scale down, crop to fit) -> reject
  iPad 12.9 -> iPhone 6.5 (scale down) -> reject
  Android phone 6.7 -> Android tablet 10.5 (letterbox) -> reject
  Android tablet 10.5 -> Android phone 6.7 (crop center) -> reject
Each fallback step logs the fallback_used field in the output screenshot entry. If all fallbacks fail, status="failed" and rejection_reason includes "viewport_fallback_exhausted".
Timeout per screenshot type
  screenshot_only:   30 seconds per screenshot
  device_frame:      60 seconds per screenshot  (includes device rendering)
  hero_banner:       45 seconds per screenshot
If a screenshot exceeds its timeout, the retry function fires (see canonical Retry Logic section). After max_attempts=3, the screenshot is marked status="failed" and the error type recorded in failure_reason.
Retry counts (canonical)
  max_attempts: 3
  base_delay_seconds: 1
  backoff: exponential, multiplier 2
  jitter: enabled
  Only retries on transient errors (timeout, 503, connection reset). 400/401/403/422 errors are not retried.
Error recovery paths
  Device not available:       fallback chain as above. If all fail -> status="failed"
  Rendering engine crash:     retry once (counts as attempt 2). If crash repeats -> status="failed"
  Disk full during write:     try alternate temp directory (configurable in input as screenshots.alt_temp_dir). If also full -> status="failed"
  Network timeout (CDN upload): canonical retry. If still fails after 3 attempts -> status="failed", img stored locally and path returned in local_fallback_path
  Locale font missing:        fall back to Noto Sans CJK for CJK locales, Noto Sans Arabic for RTL. If still missing -> render with system sans-serif and flag warning in screenshot output
  GPU unavailable:            fall back to CPU rendering. If CPU render exceeds 2x the screenshot_type timeout -> status="failed"
All failed screenshots include:
  failure_reason: string      # Machine-readable error code
  failure_detail: string      # Human-readable explanation
  attempt_count: integer      # How many retry attempts were made
  final_error: string         # The error message of the last attempt
There are no duplicate retry references elsewhere. All retry behavior is governed by the single canonical Retry Logic section in the blueprint.