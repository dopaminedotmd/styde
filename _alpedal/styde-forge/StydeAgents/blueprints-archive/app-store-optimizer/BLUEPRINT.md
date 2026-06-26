# App Store Optimizer
**Domain:** app-dev **Version:** 2

## Purpose
Optimizes app store presence across Google Play and Apple App Store via keyword research, screenshot generation, A/B testing, and strategic rating prompts.

## Persona
ASO specialist. Expert in App Store Optimization, keyword research, and conversion optimization.

## Skills
- Keyword: research high-traffic app keywords with locale-specific volume and difficulty scores
- Screenshot: design compelling screenshot sets per store, device type, and locale
- Description: write optimized app descriptions with keyword density < 3.5% per locale
- A/B: test listing variants for conversion with minimum sample size of 1000 impressions per variant
- Rating: implement rating prompts strategically with per-platform rate-limit rules

## Input / Output Schema

### Input (JSON)
```json
{
  "app": {
    "name": {"type": "string", "required": true, "max_length": 30},
    "bundle_id": {"type": "string", "required": true, "pattern": "^com\\.[a-z0-9]+\\.[a-z0-9]+$"},
    "category": {"type": "string", "enum": ["games", "productivity", "utilities", "finance", "health", "education", "social", "entertainment"]},
    "primary_language": {"type": "string", "pattern": "^[a-z]{2}(-[A-Z]{2})?$", "default": "en-US"}
  },
  "locales": {
    "type": "array",
    "items": {"type": "string", "pattern": "^[a-z]{2}(-[A-Z]{2})?$"},
    "min_items": 1,
    "max_items": 50,
    "default": ["en-US"]
  },
  "keywords": {
    "type": "array",
    "items": {"type": "string", "max_length": 100},
    "min_items": 0,
    "max_items": 100,
    "description": "Optional seed keywords. If empty, auto-generate from app metadata."
  },
  "competitors": {
    "type": "array",
    "items": {"type": "string"},
    "max_items": 10,
    "description": "Optional competitor bundle IDs for keyword gap analysis."
  }
}
```

### Output
```yaml
keywords:
  recommended:
    - term: "meditation timer"
      locale: en-US
      volume: 42000
      difficulty: 0.65
      priority: high
      source: seed_expansion
    # ... up to 100 per locale
screenshots:
  generated:
    - store: ios_app_store
      device: iphone_14_pro_max
      locale: en-US
      set:
        - slot: 1
          type: hero
          asset_url: "screenshots/en-US/iphone/hero.png"
          overlay_text: "Focus your mind, anywhere"
          fallback_device: iphone_14
        - slot: 2
          type: feature_1
          asset_url: "screenshots/en-US/iphone/feature_1.png"
          fallback_device: iphone_14
description:
  en-US:
    title: "Meditation Timer & Focus"
    subtitle: "Guided sessions for calm"
    body: "body_text_here"  # max 4000 chars
    keyword_density: 0.032
    seo_score: 88
ab_test:
  variants:
    - variant_id: v1
      screenshot_set: A
      description_variant: A
      traffic_split: 0.5
      min_sample_size: 1000
```

## Retry & Resilience
Single canonical retry policy applied to all external calls:

| Operation              | Max Retries | Backoff          | Timeout    | Fallback                      |
|------------------------|-------------|------------------|------------|-------------------------------|
| keyword fetch          | 3           | exponential 2x   | 10s/call   | cached keyword pool (7d TTL)  |
| screenshot generation  | 2           | linear 5s        | 60s/call   | no-screenshot template asset  |
| description publish    | 3           | exponential 2x   | 15s/call   | fail with error report        |
| competitor gap scan    | 2           | exponential 2x   | 30s/call   | skip competitor, log warning  |
| rating prompt send     | 1           | none             | 5s/call    | queue for retry on next cycle |

Retry condition: HTTP 5xx, timeout, or network error. HTTP 4xx (except 429) are terminal and not retried. 429 follows Retry-After header.

## Keyword Refresh Cadence

| Locale type   | Refresh schedule | Source data                    | Fallback threshold                    |
|---------------|------------------|--------------------------------|---------------------------------------|
| high-volume   | weekly (Mon 00:00 UTC) | Apple Search Ads + Google Play Console | no refresh if previous score > 80     |
| medium-volume | bi-weekly (1st, 15th)  | API keyword volume snapshots   | keep previous set if new volume < 50% |
| low-volume    | monthly          | cached competitor gap scan     | manual override only                  |
| experimental  | on-demand / A/B trigger | zero-volume seed expansion     | reject if difficulty > 0.85           |

Refresh logic:
1. Fetch current keyword performance (impressions, conversion, rank).
2. Run gap analysis against competitor bundles.
3. Score each candidate: volume * (1 - difficulty) + conversion_bonus.
4. Replace bottom 20% of current set with top candidates from scoring.
5. If new set conversion confidence < 80%, revert to previous set and log.

## Localization Strategy

### RTL Handling
- Arabic and Hebrew locales force right-to-left layout in description body and screenshot overlays.
- Text direction auto-detected from locale code (ar-*, he-*). Overridable per locale.
- Screenshot text overlays mirror on RTL layouts: alignment flips to right, reading order reversed.

### Transliteration Rules
- Non-Latin scripts (Cyrillic, Arabic, CJK, Devanagari) use ISO-15919 or ICU transliteration for keyword fallback when native search volume is unavailable.
- Transliterated keywords are flagged in output with `transliterated: true` and scored at 0.8x native weight.

### Character Inflation Handling
| Language group | Avg char inflation factor | Max description chars | Strategy                              |
|----------------|--------------------------|-----------------------|---------------------------------------|
| CJK            | 0.35x                    | 4000 (Google) / 4000 (Apple) | pack 2.8x more semantic density |
| Arabic         | 1.2x                     | 4000                  | shorten descriptions; rely on visuals |
| Cyrillic       | 1.1x                     | 4000                  | standard compression                  |
| Latin          | 1.0x                     | 4000                  | standard                              |
| Thai           | 0.8x                     | 4000                  | moderate compression                  |

### Screenshot-Text Overlay Strategy per Store
| Store        | Overlay area  | Max chars per overlay | Font size range | Language-aware wrap |
|--------------|---------------|-----------------------|-----------------|---------------------|
| Apple App Store | top 20%, bottom 15% | 120             | 24-36pt         | yes (CJK break any) |
| Google Play  | top 25%, bottom 20% | 140             | 22-34pt         | yes (no mid-word for CJK) |
| Huawei AppGallery | top 20%, bottom 15% | 100         | 20-32pt         | yes                 |
| Samsung Galaxy Store | top 25%, bottom 20% | 110      | 22-34pt         | yes                 |

## Keyword Selection Decision Tree
```
                      ┌──────────────┐
                      │ Seed keywords │
                      │ provided?     │
                      └──┬───────┬───┘
                      Yes│       │No
                         ▼       ▼
                   ┌────────┐ ┌──────────────┐
                   │ Use    │ │ Extract from  │
                   │ seeds  │ │ app metadata │
                   └───┬────┘ └──────┬───────┘
                       │             │
                       ▼             ▼
                  ┌────────────────────────┐
                  │ Fetch volume +         │
                  │ difficulty per locale   │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Score = volume *        │
                  │ (1 - difficulty)        │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Rank by score;         │
                  │ keep top 50 per locale  │
                  └───────────┬────────────┘
                              │
                  ┌───────────┴──────────┐
                  ▼                      ▼
          ┌──────────────┐    ┌───────────────────┐
          │ difficulty   │    │ difficulty ≥ 0.85  │
          │ < 0.85       │    │                   │
          │ Add to set   │    │ Add only if        │
          │              │    │ brand_name match   │
          └──────┬───────┘    └────────┬──────────┘
                 │                     │
                 └──────────┬──────────┘
                            ▼
                  ┌────────────────────────┐
                  │ Run competitor gap scan │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Merge, deduplicate,     │
                  │ tag source              │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Output per locale       │
                  │ keyword set with        │
                  │ volume, difficulty,     │
                  │ priority field          │
                  └────────────────────────┘
```

## Locale-to-ASO Dimension Configuration

| Locale        | Keyword max | Description max | Screenshot slots | Text direction | Rating prompt allowed |
|---------------|-------------|-----------------|------------------|----------------|-----------------------|
| en-US         | 100         | 4000 chars      | 10               | LTR            | yes                   |
| en-GB         | 100         | 4000 chars      | 10               | LTR            | yes                   |
| ja-JP         | 100         | 4000 chars      | 10               | LTR            | yes (opt-in only)     |
| ko-KR         | 100         | 4000 chars      | 10               | LTR            | no                    |
| zh-CN         | 100         | 4000 chars      | 8                | LTR            | no                    |
| zh-TW         | 100         | 4000 chars      | 8                | LTR            | no                    |
| ar-SA         | 100         | 4000 chars      | 10               | RTL            | yes (opt-in only)     |
| he-IL         | 100         | 4000 chars      | 10               | RTL            | no                    |
| ru-RU         | 100         | 4000 chars      | 10               | LTR            | no                    |
| pt-BR         | 100         | 4000 chars      | 10               | LTR            | yes                   |
| es-MX         | 100         | 4000 chars      | 10               | LTR            | yes                   |
| de-DE         | 100         | 4000 chars      | 10               | LTR            | yes (opt-in only)     |
| fr-FR         | 100         | 4000 chars      | 10               | LTR            | yes                   |
| it-IT         | 100         | 4000 chars      | 10               | LTR            | yes                   |
| th-TH         | 100         | 4000 chars      | 10               | LTR            | no                    |
