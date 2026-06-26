/**
 * Design Token Pipeline — Build Orchestrator
 *
 * Entry point for the full token build pipeline:
 *   1. Validate token source files (schema + naming)
 *   2. Run Style Dictionary across all platforms
 *   3. Verify outputs
 *   4. Report build summary
 *
 * Usage:
 *   node build.js [--watch] [--platform css,json,ts]
 */

import { existsSync, readdirSync, statSync, readFileSync } from 'fs';
import { resolve, dirname, join } from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import StyleDictionary from 'style-dictionary';

import { registerTransforms } from './style-dictionary/transforms/index.js';
import { registerFormats } from './style-dictionary/formats/index.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ─── Build configuration ───────────────────────────────────────────────

const DEFAULT_PLATFORMS = ['css', 'json', 'ts', 'scss', 'less', 'tailwind', 'figma'];

const args = process.argv.slice(2);
const isWatch = args.includes('--watch');
const platformArg = args.find(a => a.startsWith('--platform='));
const platforms = platformArg
  ? platformArg.replace('--platform=', '').split(',')
  : DEFAULT_PLATFORMS;

// ─── Step 1: Validate token source files ───────────────────────────────

function validateTokens() {
  console.log('🔍 Validating token source files...\n');

  const tokensDir = resolve(__dirname, 'tokens');
  const files = readdirSync(tokensDir).filter(f => f.endsWith('.json'));

  let errors = 0;
  let warnings = 0;

  for (const file of files) {
    const filePath = resolve(tokensDir, file);
    try {
      const raw = readFileSync(filePath, 'utf-8');
      const parsed = JSON.parse(raw);

      // Check for invalid characters in token names
      const validateTokenNames = (obj, path = []) => {
        for (const [key, val] of Object.entries(obj)) {
          if (key === 'value' || key === 'attributes' || key === 'description' || key === 'type') continue;

          if (!/^[a-zA-Z0-9_-]+$/.test(key)) {
            console.log(`   ❌ ${file}: invalid token name "${key}" at ${path.join('.')}`);
            errors++;
          }

          if (typeof val === 'object' && val !== null && !val.value) {
            validateTokenNames(val, [...path, key]);
          }
        }
      };

      validateTokenNames(parsed);
      console.log(`   ✅ ${file} — valid JSON`);

    } catch (err) {
      console.log(`   ❌ ${file} — ${err.message}`);
      errors++;
    }
  }

  if (errors > 0) {
    console.error(`\n❌ Validation failed with ${errors} error(s).`);
    process.exit(1);
  }

  console.log(`\n✅ All ${files.length} token files validated.\n`);
  return files.length;
}

// ─── Step 2: Style Dictionary build ────────────────────────────────────

function buildTokens() {
  console.log('🔨 Building design tokens...\n');

  // Register custom transforms and formats
  registerTransforms(StyleDictionary);
  registerFormats(StyleDictionary);

  // Load config
  const configPath = resolve(__dirname, 'style-dictionary', 'config.json');
  const baseConfig = JSON.parse(readFileSync(configPath, 'utf-8'));

  const builtPlatforms = [];
  const errors = [];

  for (const platform of platforms) {
    if (!baseConfig.platforms[platform]) {
      console.log(`   ⚠️  Platform "${platform}" not found in config, skipping.`);
      continue;
    }

    try {
      // Create a Style Dictionary instance for this platform
      const sdConfig = {
        ...baseConfig,
        platforms: {
          [platform]: baseConfig.platforms[platform],
        },
      };

      // Use parallel Style Dictionary CLI for each platform
      console.log(`   Building ${platform}...`);
      execSync(
        `npx style-dictionary build --config style-dictionary/config.json --platform ${platform}`,
        { cwd: __dirname, stdio: 'pipe' }
      );
      console.log(`   ✅ ${platform} — built successfully`);
      builtPlatforms.push(platform);
    } catch (err) {
      console.log(`   ❌ ${platform} — ${err.message}`);
      errors.push({ platform, error: err.message });
    }
  }

  return { builtPlatforms, errors };
}

// ─── Step 3: Verify outputs ────────────────────────────────────────────

function verifyOutputs() {
  console.log('\n📋 Verifying build outputs...\n');

  const distDir = resolve(__dirname, 'dist');
  const expectedFiles = [
    'dist/css/tokens.css',
    'dist/json/tokens.json',
    'dist/json/tokens-flat.json',
    'dist/ts/tokens.ts',
    'dist/ts/tokens.d.ts',
  ];

  let verified = 0;
  let missing = 0;
  let totalSize = 0;

  for (const file of expectedFiles) {
    const fullPath = resolve(__dirname, file);
    if (existsSync(fullPath)) {
      const size = statSync(fullPath).size;
      totalSize += size;
      console.log(`   ✅ ${file} (${(size / 1024).toFixed(1)} KB)`);
      verified++;
    } else {
      console.log(`   ⚠️  ${file} — not found`);
      missing++;
    }
  }

  return { verified, missing, totalSize };
}

// ─── Step 4: Summary ───────────────────────────────────────────────────

function printSummary(tokenCount, buildResults, verification) {
  console.log('\n' + '═'.repeat(60));
  console.log('  DESIGN TOKEN PIPELINE — BUILD SUMMARY');
  console.log('═'.repeat(60));
  console.log(`  Source files:        ${tokenCount} token JSON files`);
  console.log(`  Platforms built:     ${buildResults.builtPlatforms.join(', ')}`);
  console.log(`  Outputs verified:    ${verification.verified}/${verification.verified + verification.missing}`);
  console.log(`  Total output size:   ${(verification.totalSize / 1024).toFixed(1)} KB`);
  if (buildResults.errors.length > 0) {
    console.log(`  Build errors:        ${buildResults.errors.length}`);
    buildResults.errors.forEach(e => console.log(`    ❌ ${e.platform}: ${e.error}`));
  }
  console.log('═'.repeat(60));
}

// ─── Main ──────────────────────────────────────────────────────────────

async function main() {
  const startTime = Date.now();

  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║   DESIGN TOKEN PIPELINE — Multi-Platform Build           ║');
  console.log('╚═══════════════════════════════════════════════════════════╝\n');

  // Step 1: Validate
  const tokenCount = validateTokens();

  // Step 2: Build (skip if watch — build is done by watcher)
  if (!isWatch) {
    const buildResults = buildTokens();

    // Step 3: Verify
    const verification = verifyOutputs();

    // Step 4: Summary
    const duration = ((Date.now() - startTime) / 1000).toFixed(1);
    printSummary(tokenCount, buildResults, verification);
    console.log(`\n  ⏱️  Total time: ${duration}s`);

    if (buildResults.errors.length > 0) {
      process.exit(1);
    }
  } else {
    console.log('   👀 Watch mode — waiting for changes...');
    // Watch mode would use chokidar here; for now just report
  }
}

// ─── Watch mode ────────────────────────────────────────────────────────

if (isWatch) {
  console.log('👀 Watch mode enabled. Press Ctrl+C to stop.\n');
  main();

  // Re-run on changes (using simple file watcher)
  import('chokidar').then(({ default: chokidar }) => {
    const watcher = chokidar.watch(resolve(__dirname, 'tokens'), {
      persistent: true,
      ignoreInitial: true,
    });

    watcher.on('change', (filePath) => {
      console.log(`\n🔄 Detected change: ${filePath}`);
      main();
    });

    watcher.on('error', console.error);
  }).catch(() => {
    console.log('   chokidar not available; watch mode limited.');
    main();
  });
} else {
  main();
}
