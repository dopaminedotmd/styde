# Design Token Pipeline

> **Multi-platform design token pipeline** — Style Dictionary + Figma sync + GitHub Actions CI
>
> Transforms design tokens from a single source of truth into CSS, JSON, TypeScript, SCSS, Less,
> Tailwind, Android, iOS, and Figma Tokens Studio formats with automatic px→rem and hex→oklch conversion.

## ⚡ Quick Start

```bash
npm install
npm run build        # Build all platforms
npm run build:all    # Alternative: build every format
npm run sync:figma   # Pull tokens from Figma
npm test             # Validate outputs
```

## 🗂 Token Architecture

```
tokens/
├── color.json         # Primitives + semantic + dark theme colors
├── typography.json    # Font families, sizes, weights, line heights, letter spacing
├── spacing.json       # 4px-grid spacing scale (0.5–96)
├── size.json          # Containers, breakpoints, icons, avatars
├── radius.json        # Border radius scale (none → full)
├── shadow.json        # Elevation shadow scale + focus rings
├── motion.json        # Animation durations + easing curves
└── z-index.json       # Z-index scale
```

## 🔄 Transformation Pipeline

1. **px → rem** — All pixel values (sizes, spacing, radii) converted to rem units at 16px base
2. **hex → oklch** — All hex colors converted to perceptually-uniform OKLCH color space
3. **Alias resolution** — `{color.primitives.gray.100}` references resolved transitively
4. **Platform transforms** — CSS custom properties, camelCase JS, Android XML resources, iOS ObjC

## 📦 Output Formats

| Format | Output | Platforms |
|--------|--------|-----------|
| CSS | `dist/css/tokens.css` | Web, any |
| CSS Dark | `dist/css/tokens-dark.css` | Web (dark mode) |
| JSON Nested | `dist/json/tokens.json` | Universal |
| JSON Flat | `dist/json/tokens-flat.json` | Style processors |
| TypeScript | `dist/ts/tokens.ts` | React, Next.js, Node |
| TypeScript Types | `dist/ts/tokens.d.ts` | TypeScript type safety |
| SCSS | `dist/scss/_tokens.scss` | SCSS projects |
| Less | `dist/less/_tokens.less` | Less projects |
| Tailwind | `dist/tailwind/tokens.tailwind.js` | Tailwind CSS |
| Android | `dist/android/*.xml` | Android apps |
| iOS | `dist/ios/*.h`, `dist/ios/*.m` | iOS apps |
| Figma Tokens | `dist/figma/tokens-figma.json` | Figma Tokens Studio |

## 🔌 Figma Integration

### Pull from Figma

```bash
# Set environment variables
export FIGMA_PERSONAL_ACCESS_TOKEN=figd_xxxx
export FIGMA_FILE_KEY=abc123

# Pull tokens
npm run sync:figma
```

### Push to Figma Tokens Studio

```bash
# Build Figma-compatible JSON
npm run build -- --platform=figma

# Import into Figma:
#   1. Open Figma Tokens Studio plugin
#   2. Settings → Import
#   3. Select dist/figma/tokens-figma.json
```

## 🤖 GitHub Actions CI

Automated on push to tokens/**, PRs, daily schedule, and manual dispatch.

### Workflow Steps

1. **Validate** — Lint token files, check JSON schema, verify naming conventions, detect duplicates
2. **Build** — Matrix build across all platforms (CSS, JSON, TS, SCSS, Less, Tailwind, Figma)
3. **Sync Figma** (optional) — Pull latest tokens from Figma and auto-create PR
4. **Test** — Validate CSS (OKLCH + rem presence), JSON (parse check), TS (type assertion check)
5. **Release** — Create GitHub release with `design-tokens.zip` artifact on main push

### Manual Dispatch

```bash
# Trigger via GitHub UI or GitHub CLI:
gh workflow run token-ci.yml \
  -f platforms=css,json,ts \
  -f sync_figma=true \
  -f release=true
```

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `FIGMA_PERSONAL_ACCESS_TOKEN` | Figma API authentication for token sync |
| `FIGMA_FILE_KEY` | Target Figma file key |
| `FIGMA_NODE_ID` | Optional root frame/node ID |

## 🧬 OKLCH Color Pipeline

Colors flow through a pure-JS transformation:

```
hex → sRGB [0-1] → linear RGB → LMS → OKLab → OKLCH
```

**Why OKLCH?**
- Perceptually uniform — equal numeric changes look equally different to humans
- Wide gamut — supports P3 and Rec.2020 beyond sRGB
- Better interpolation — gradient midpoint colors aren't muddy
- Accessibility-friendly — L (lightness) maps directly to perceived lightness

**Example conversion:**
```
#3b82f6 → oklch(0.6320 0.1955 264.1)
#22c55e → oklch(0.6940 0.1861 142.5)
#ef4444 → oklch(0.6192 0.2387 29.6)
```

## Available Scripts

```bash
npm run build          # Full pipeline: validate + build + verify
npm run build:all      # Build all platforms via native style-dictionary
npm run build:css      # CSS only
npm run build:json     # JSON only
npm run build:ts       # TypeScript only
npm run sync:figma     # Pull tokens from Figma
npm run lint:tokens    # Validate token source files
npm test               # Verify build outputs
npm run ci             # Full CI pipeline (lint + build + test)
```

## Dependencies

- **style-dictionary** (^4.3) — Core token engine, manages platforms, transforms, formats
- **culori** (^4.0) — Optional: provides additional color space conversions (used for advanced cases)
- **chokidar** (^4.0) — File watcher for development mode

## 🚀 Design Token CI/CD Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Designers   │     │  Token Repo  │     │  Developers │
│  (Figma)     │     │  (GitHub)    │     │  (Apps)     │
└──────┬───────┘     └──────┬───────┘     └──────┬──────┘
       │                    │                    │
       │  Update tokens     │                    │
       │  in Figma plugin   │                    │
       │───────────────────►│                    │
       │                    │  CI: validate      │
       │                    │  CI: build all     │
       │                    │  CI: test outputs  │
       │                    │───────────────────►│
       │                    │  npm publish /     │
       │                    │  GitHub Release    │
       │                    │                    │
       │  ← Sync PR         │                    │
       │  (if Figma sync    │                    │
       │   is configured)   │                    │
       │                    │                    │
       │                    │  PR for token      │
       │                    │  changes from devs │◄───┘
       │                    │  (reviewed by      │
       │                    │   designers)       │
```

## 🔧 Configuration

The Style Dictionary configuration (`style-dictionary/config.json`) defines:

- **source**: `tokens/**/*.json` — all JSON files in the tokens directory
- **platforms**: 8 output platforms with their transforms, build paths, and format options
- **filtering**: Per-format filters ensure only relevant tokens land in each output (e.g., Android `colors.xml` gets only color tokens)

## 📁 File Structure

```
design-token-pipeline/
├── .github/workflows/token-ci.yml    # GitHub Actions CI/CD
├── build.js                          # Pipeline orchestrator
├── figma-tokens/sync.js              # Figma two-way sync
├── package.json                      # Dependencies & scripts
├── scripts/
│   └── lint-tokens.js                # Token validation
├── style-dictionary/
│   ├── config.json                   # Multi-platform SD config
│   ├── transforms/index.js           # px→rem, hex→oklch transforms
│   └── formats/index.js              # Custom output formats
└── tokens/
    ├── color.json
    ├── typography.json
    ├── spacing.json
    ├── size.json
    ├── radius.json
    ├── shadow.json
    ├── motion.json
    └── z-index.json
```
