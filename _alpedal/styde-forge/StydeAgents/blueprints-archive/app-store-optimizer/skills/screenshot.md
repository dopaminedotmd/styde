# Screenshot Skill
Generates production-ready app store screenshot sets per store, device, and locale.

## Device Handling

### iOS
| Device              | Resolution       | Aspect ratio | Store              |
|---------------------|------------------|--------------|--------------------|
| iPhone 14 Pro Max   | 1290 x 2796      | 19.5:9       | App Store           |
| iPhone 14 Pro       | 1179 x 2556      | 19.5:9       | App Store           |
| iPhone 14           | 1170 x 2532      | 19.5:9       | App Store           |
| iPhone 13 / 12      | 1170 x 2532      | 19.5:9       | App Store           |
| iPhone SE (3rd gen) | 750 x 1334       | 16:9         | App Store           |
| iPad Pro 12.9"      | 2048 x 2732      | 4:3          | App Store (optional)|
| iPad Pro 11"        | 1668 x 2388      | 4:3          | App Store (optional)|

### Android
| Device              | Resolution       | Aspect ratio | Store              |
|---------------------|------------------|--------------|--------------------|
| Pixel 7 Pro         | 1440 x 3120      | 19.5:9       | Google Play         |
| Pixel 7             | 1080 x 2400      | 20:9         | Google Play         |
| Samsung S23 Ultra   | 1440 x 3088      | 19.3:9       | Google Play         |
| OnePlus 11          | 1440 x 3216      | 20:9         | Google Play         |
| Huawei P60 Pro      | 1224 x 2700      | 19.8:9       | AppGallery          |

### Desktop (for companion/store preview)
| Platform    | Resolution   | Aspect ratio | Use case                    |
|-------------|--------------|--------------|-----------------------------|
| MacBook Pro | 1512 x 982   | 16:10        | App Store Connect preview   |
| Windows     | 1920 x 1080  | 16:9         | promotional materials       |

## Viewport Fallback
When the exact device is unavailable, fall back in this order:
1. Same device family, older model (e.g. iPhone 14 -> iPhone 13)
2. Same aspect ratio, closest resolution
3. Generic template at 1080x1920 (19.5:9 default)
4. No-screenshot placeholder with error logged

## Timeout Per Screenshot Type
| Type            | Timeout | Notes                           |
|-----------------|---------|---------------------------------|
| hero            | 60s     | Full scene render               |
| feature         | 45s     | Feature highlight render        |
| testimonial     | 30s     | Quote overlay on simple bg      |
| demo animation  | 90s     | GIF/APNG generation             |
| localized text  | 15s     | Text overlay only, reusing base |
| placeholder     | 5s      | Minimal fallback asset          |

Total batch timeout = max(individual timeout per type) * (number of screenshots in set). For 10-slot set with 2 heros + 4 features + 4 localized: 60 * 10 = 600s max.

## Retry Counts
Per the canonical retry policy in BLUEPRINT.md:
- Screenshot generation: 2 retries with 5s linear backoff
- Asset upload to store: 3 retries with exponential backoff (2s, 4s, 8s)
- Localization text render: 1 retry, immediate
- 429 (rate limit): follow Retry-After header, up to 3 additional retries

All retries log attempt count, error type, and elapsed time. Exhausted retries fall to error recovery.

## Error Recovery Paths

### Generation Failure
```
render failed -> is file system full? -> yes: alert operator, no
                |                                        |
                ▼                                        ▼
          is fallback device available?          wait 5s, retry
                |                                        |
           yes  |   no                                  |
                ▼                                        ▼
          re-render on           timeout?  --no-->  success
          fallback device         |
                                  ▼
                            use placeholder
                            log full error
                            continue batch
```

### Upload Failure
```
upload failed -> is 5xx? -> yes: retry (3x exponential)
                |         no
                |         -> is 4xx? -> fail terminal, log response body
                ▼
        all retries exhausted -> queue for manual upload
                                 flag in output with upload_status: pending
```

### Localization Failure
```
text render failed -> retry once -> still fail?
                |                                |
                ▼                                ▼
          use English text              start-of-file=English
          tag as fallback: true         region code placeholder
          log locale and string key     flag for human review
```

## Output Contract
Each generated screenshot produces:
```yaml
- slot: 1
  type: hero
  store: ios_app_store
  device: iphone_14_pro_max
  locale: en-US
  asset_path: "screenshots/en-US/iphone/hero.png"
  asset_url: "https://cdn.example.com/screenshots/en-US/iphone/hero.png"  # after upload
  overlay_text: "Focus your mind, anywhere"
  font: SF-Pro-Text-Semibold
  font_size_pt: 32
  text_alignment: center
  text_direction: LTR
  fallback_device: iphone_14
  localization_fallback: false
  upload_status: pending   # pending | uploading | uploaded | failed
  dimensions: {width: 1290, height: 2796}
  aspect_ratio: "19.5:9"
  md5_hash: "a1b2c3d4e5f6..."
```

Rejection criteria:
- Image dimensions within 2px of target resolution (tolerance)
- Text overflows not clipped (auto-reduce font until it fits)
- Aspect ratio mismatch > 0.01 triggers fallback device rerender
- md5_hash must match pre-upload checksum
