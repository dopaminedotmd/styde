#!/usr/bin/env node

/**
 * Figma Tokens Plugin Sync
 *
 * Two-way sync between Figma Tokens Studio plugin and the token repository.
 *
 * Direction 1 — Figma → Repo (pull)
 *   Fetches tokens from Figma via REST API, normalizes them into
 *   Style Dictionary-compatible JSON files under tokens/.
 *
 * Direction 2 — Repo → Figma (push)
 *   Pushes transformed tokens back to a Figma Tokens Studio JSON
 *   that can be imported into the plugin.
 *
 * Requirements:
 *   - FIGMA_PERSONAL_ACCESS_TOKEN in environment or .env
 *   - FIGMA_FILE_KEY for the design file
 *
 * Usage:
 *   node figma-tokens/sync.js pull   # pull tokens from Figma
 *   node figma-tokens/sync.js push   # push tokens to Figma-compatible JSON
 *   node figma-tokens/sync.js watch  # watch for changes and auto-sync
 */

import { readFileSync, writeFileSync, existsSync, watch } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '..');

// ─── Configuration ─────────────────────────────────────────────────────

const config = {
  figma: {
    baseUrl: 'https://api.figma.com/v1',
    token: process.env.FIGMA_PERSONAL_ACCESS_TOKEN || process.env.FIGMA_TOKEN || '',
    fileKey: process.env.FIGMA_FILE_KEY || '',
    nodeId: process.env.FIGMA_NODE_ID || '', // optional root node
  },
  tokenSets: [
    'core/colors',
    'core/typography',
    'core/spacing',
    'core/radius',
    'core/sizing',
    'core/shadows',
    'core/motion',
    'core/opacity',
    'semantic/light',
    'semantic/dark',
    'component/button',
    'component/input',
    'component/card',
  ],
  outputDir: resolve(repoRoot, 'tokens'),
  figmaTokensJson: resolve(repoRoot, 'dist', 'figma', 'tokens-figma.json'),
};

// ─── Figma API client ──────────────────────────────────────────────────

class FigmaClient {
  constructor({ token, baseUrl, fileKey }) {
    this.token = token;
    this.baseUrl = baseUrl;
    this.fileKey = fileKey;
  }

  async request(endpoint) {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'X-Figma-Token': this.token,
      },
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`Figma API error ${response.status}: ${body}`);
    }

    return response.json();
  }

  /** Get all local styles in the file */
  async getStyles() {
    const { meta } = await this.request(`/files/${this.fileKey}?depth=1`);
    return meta?.styles || [];
  }

  /** Get all local variables (Figma Variables API) */
  async getVariables() {
    return this.request(`/files/${this.fileKey}/variables/local`);
  }

  /** Get specific nodes with their style references */
  async getNodes(nodeIds) {
    const ids = nodeIds.join(',');
    return this.request(`/files/${this.fileKey}/nodes?ids=${ids}`);
  }
}

// ─── Figma style → Style Dictionary token ─────────────────────────────

function normalizeColorName(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .replace(/--+/g, '-');
}

function parseFigmaColor(paint) {
  if (paint.type === 'SOLID') {
    const { r, g, b } = paint.color;
    const a = paint.opacity ?? 1;
    const toHex = (n) => Math.round(n * 255).toString(16).padStart(2, '0');
    const hex = `#${toHex(r)}${toHex(g)}${toHex(b)}`;
    return a < 1 ? `${hex}${toHex(a)}` : hex;
  }
  return null;
}

function styleToToken(style, paints) {
  switch (style.style_type) {
    case 'FILL': {
      const color = parseFigmaColor(paints[0]);
      return color ? { value: color, type: 'color' } : null;
    }
    case 'TEXT': {
      // Text styles bundle multiple properties
      // In a full implementation, decompose into fontFamily, fontSize, etc.
      return null; // handled separately via getTextStyles
    }
    case 'EFFECT': {
      const shadows = style.effects
        ?.filter(e => e.type === 'DROP_SHADOW' || e.type === 'INNER_SHADOW')
        .map(e => {
          const inner = e.type === 'INNER_SHADOW' ? 'inset ' : '';
          const color = parseFigmaColor({ type: 'SOLID', color: e.color, opacity: e.color.a });
          return `${inner}${e.offset.x}px ${e.offset.y}px ${e.radius}px ${e.spread ?? 0}px ${color}`;
        })
        .join(', ');
      return shadows ? { value: shadows, type: 'boxShadow' } : null;
    }
    default:
      return null;
  }
}

// ─── Two-way sync functions ────────────────────────────────────────────

/**
 * PULL: Fetch tokens from Figma and write to Style Dictionary JSON files.
 */
async function pullFromFigma() {
  console.log('📥 Pulling tokens from Figma...');

  if (!config.figma.token) {
    console.error('❌ FIGMA_PERSONAL_ACCESS_TOKEN not set. Skipping Figma pull.');
    console.log('   Set the environment variable and retry.');
    return;
  }

  if (!config.figma.fileKey) {
    console.error('❌ FIGMA_FILE_KEY not set. Skipping Figma pull.');
    return;
  }

  const client = new FigmaClient(config.figma);

  try {
    // 1. Fetch local variables (new Figma Variables API)
    console.log('   Fetching variables...');
    const variables = await client.getVariables();
    console.log(`   Found ${variables?.meta?.variableCollections?.length || 0} variable collections.`);

    // 2. Fetch local styles (legacy paint/text/effect styles)
    console.log('   Fetching styles...');
    const styles = await client.getStyles();
    console.log(`   Found ${styles?.length || 0} local styles.`);

    // 3. Process into tokens
    const tokens = {
      color: {},
      typography: {},
      shadow: {},
    };

    // Process variables into color tokens
    if (variables?.meta?.variableCollections) {
      for (const collection of variables.meta.variableCollections) {
        for (const variable of collection.variables || []) {
          if (variable.resolvedType === 'COLOR') {
            const name = normalizeColorName(variable.name);
            const color = parseFigmaColor({
              type: 'SOLID',
              color: variable.valuesByMode?.[Object.keys(variable.valuesByMode || {})[0]],
              opacity: 1,
            });
            if (color) {
              tokens.color[name] = { value: color };
            }
          }
        }
      }
    }

    // 4. Write Style Dictionary-compatible JSON files
    // Merge into existing tokens (preserves hand-written tokens not in Figma)
    const colorPath = resolve(config.outputDir, 'color.json');
    const existingColors = existsSync(colorPath)
      ? JSON.parse(readFileSync(colorPath, 'utf-8'))
      : {};
    const merged = {
      ...existingColors,
      figma: tokens.color,
    };
    writeFileSync(colorPath, JSON.stringify(merged, null, 2), 'utf-8');
    console.log(`   ✅ Wrote ${Object.keys(tokens.color).length} color tokens to color.json`);

    // 5. Rebuild
    console.log('\n   Rebuilding tokens...');
    execSync('npm run build:all', { cwd: repoRoot, stdio: 'inherit' });

    console.log('\n✅ Figma pull complete!');
  } catch (err) {
    console.error('❌ Figma pull failed:', err.message);
    process.exit(1);
  }
}

/**
 * PUSH: Generate Figma Tokens Studio-compatible JSON.
 * This runs Style Dictionary with the 'figma' platform, then
 * outputs a JSON file importable into the Figma Tokens Studio plugin.
 */
function pushToFigma() {
  console.log('📤 Pushing tokens to Figma Tokens Studio format...');

  try {
    // Run the Style Dictionary figma platform build
    execSync(
      'npx style-dictionary build --config style-dictionary/config.json --platform figma',
      { cwd: repoRoot, stdio: 'inherit' }
    );

    const outputPath = config.figmaTokensJson;
    if (existsSync(outputPath)) {
      const tokens = JSON.parse(readFileSync(outputPath, 'utf-8'));
      const setCount = Object.keys(tokens).length;
      console.log(`\n✅ Generated Figma Tokens Studio JSON: ${outputPath}`);
      console.log(`   ${setCount} token sets ready for import`);
      console.log('\n   To import into Figma:');
      console.log('   1. Open Figma Tokens Studio plugin');
      console.log('   2. Go to Settings → Import');
      console.log(`   3. Select: ${outputPath}`);
    } else {
      console.error('❌ Figma tokens file not generated.');
    }
  } catch (err) {
    console.error('❌ Figma push failed:', err.message);
    process.exit(1);
  }
}

/**
 * WATCH: Watch token files for changes and auto-regenerate.
 * Useful during development when iterating on token values.
 */
function watchTokens() {
  const tokensDir = config.outputDir;
  console.log(`👀 Watching for token changes in ${tokensDir}...`);

  let debounceTimer;

  const rebuild = () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      console.log('\n🔄 Change detected, rebuilding...');
      try {
        execSync('npm run build:all', { cwd: repoRoot, stdio: 'inherit' });
        console.log('✅ Rebuild complete. Watching for changes...');
      } catch (err) {
        console.error('❌ Rebuild failed:', err.message);
      }
    }, 300); // 300ms debounce
  };

  watch(tokensDir, { recursive: true }, (eventType, filename) => {
    if (filename && filename.endsWith('.json')) {
      console.log(`   Modified: ${filename}`);
      rebuild();
    }
  });

  // Keep process alive
  process.stdin.resume();
}

// ─── CLI ───────────────────────────────────────────────────────────────

const command = process.argv[2];

switch (command) {
  case 'pull':
    pullFromFigma();
    break;
  case 'push':
    pushToFigma();
    break;
  case 'watch':
    watchTokens();
    break;
  default:
    console.log(`
Design Token Pipeline — Figma Sync

Usage:
  node figma-tokens/sync.js pull    Pull tokens from Figma → repo
  node figma-tokens/sync.js push    Push tokens from repo → Figma Tokens Studio JSON
  node figma-tokens/sync.js watch   Watch token files and auto-rebuild

Environment:
  FIGMA_PERSONAL_ACCESS_TOKEN    Figma personal access token
  FIGMA_FILE_KEY                 Figma file key (from URL)
  FIGMA_NODE_ID                  Optional root node/ frame ID
`);
    process.exit(1);
}
