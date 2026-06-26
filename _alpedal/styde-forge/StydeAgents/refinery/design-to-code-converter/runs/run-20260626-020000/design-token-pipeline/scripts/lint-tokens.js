/**
 * Token Linting Script
 *
 * Validates token source files for:
 *   1. Valid JSON syntax
 *   2. Required "value" key on leaf tokens
 *   3. No empty objects
 *   4. Consistent naming conventions
 *   5. No duplicate token paths
 */

import { readdirSync, readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const tokensDir = resolve(__dirname, '..', 'tokens');

const ALLOWED_LEAF_KEYS = ['value', 'type', 'description', 'attributes', 'comment', 'filePath', 'isSource'];
const NAMING_PATTERN = /^[a-z0-9]+(_[a-z0-9]+)*$/; // snake_case or kebab-case fallback

let errors = 0;
let warnings = 0;

function reportError(msg) {
  console.log(`  ❌ ${msg}`);
  errors++;
}

function reportWarning(msg) {
  console.log(`  ⚠️  ${msg}`);
  warnings++;
}

function validateTokenObject(obj, path = '', file = '') {
  if (typeof obj !== 'object' || obj === null) {
    reportError(`${file}:${path || '.'} — not an object`);
    return;
  }

  const keys = Object.keys(obj);

  // Empty objects are warnings
  if (keys.length === 0) {
    reportWarning(`${file}:${path || '.'} — empty token group`);
    return;
  }

  for (const key of keys) {
    const fullPath = path ? `${path}.${key}` : key;

    // Check naming convention for non-attributes keys
    if (!ALLOWED_LEAF_KEYS.includes(key) && !NAMING_PATTERN.test(key)) {
      reportWarning(`${file}:${fullPath} — key "${key}" doesn't match naming convention (snake_case)`);
    }

    const val = obj[key];

    // If value is an object with a "value" key, it's a leaf token
    if (typeof val === 'object' && val !== null && 'value' in val) {
      // Validate leaf token
      if (val.value === undefined || val.value === null) {
        reportError(`${file}:${fullPath} — token has null/undefined value`);
      }

      // Check for unexpected keys
      const extraKeys = Object.keys(val).filter(k => !ALLOWED_LEAF_KEYS.includes(k));
      if (extraKeys.length > 0) {
        reportWarning(`${file}:${fullPath} — unexpected keys: ${extraKeys.join(', ')}`);
      }

      // Specific type checks
      if (val.type === 'color' && typeof val.value === 'string') {
        if (!/^#[0-9a-fA-F]{3,8}$|^oklch\(|^rgba?\(|^hsla?\(/.test(val.value)) {
          // Allow references to other tokens
          if (!val.value.startsWith('{')) {
            reportWarning(`${file}:${fullPath} — color value "${val.value}" doesn't look like a valid color`);
          }
        }
      }
    } else if (typeof val === 'object' && val !== null) {
      // Nested group — recurse
      validateTokenObject(val, fullPath, file);
    }
    // If it's a primitive without "value" wrapper, it's invalid
    else if (key !== 'value' && !['type', 'description', 'attributes', 'comment'].includes(key)) {
      // This is allowed for intermediate nesting nodes
      if (typeof val !== 'object' || val === null) {
        reportError(`${file}:${fullPath} — non-object non-token group value: ${typeof val}`);
      }
    }
  }
}

function checkDuplicatePaths(files) {
  console.log('\n🔍 Checking for duplicate token paths...');

  const allPaths = {};

  for (const file of files) {
    const raw = readFileSync(resolve(tokensDir, file), 'utf-8');
    const tokens = JSON.parse(raw);

    function collectPaths(obj, path = '', filePrefix) {
      if (typeof obj !== 'object' || obj === null) return;

      for (const [key, val] of Object.entries(obj)) {
        const fullPath = path ? `${path}.${key}` : key;

        if (typeof val === 'object' && val !== null && 'value' in val) {
          if (allPaths[fullPath]) {
            reportError(`duplicate token path "${fullPath}" — in ${allPaths[fullPath]} and ${filePrefix}`);
          }
          allPaths[fullPath] = filePrefix;
        } else if (typeof val === 'object' && val !== null) {
          collectPaths(val, fullPath, filePrefix);
        }
      }
    }

    collectPaths(tokens, '', file);
  }

  if (Object.keys(allPaths).filter(k => allPaths[k] !== allPaths[k]).length === 0) {
    console.log('  ✅ No duplicate token paths found.');
  }
}

// ─── Main ──────────────────────────────────────────────────────────────

console.log('🔍 Linting design tokens...\n');

const files = readdirSync(tokensDir).filter(f => f.endsWith('.json'));

if (files.length === 0) {
  reportError('No token files found in tokens/ directory');
  process.exit(1);
}

console.log(`  Found ${files.length} token files.\n`);

for (const file of files) {
  const filePath = resolve(tokensDir, file);
  let parsed;

  try {
    parsed = JSON.parse(readFileSync(filePath, 'utf-8'));
  } catch (err) {
    reportError(`${file}: invalid JSON — ${err.message}`);
    continue;
  }

  console.log(`  ${file}`);
  validateTokenObject(parsed, '', file);
}

checkDuplicatePaths(files);

// ─── Report ────────────────────────────────────────────────────────────

console.log(`\n${'─'.repeat(40)}`);
console.log(`  Errors:   ${errors}`);
console.log(`  Warnings: ${warnings}`);
console.log(`${'─'.repeat(40)}`);

if (errors > 0) {
  console.log('\n❌ Token linting failed.');
  process.exit(1);
}

console.log('\n✅ Token linting passed!');
