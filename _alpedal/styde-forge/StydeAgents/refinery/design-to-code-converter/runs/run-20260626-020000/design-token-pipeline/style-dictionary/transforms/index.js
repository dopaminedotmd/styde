/**
 * Style Dictionary Custom Transforms
 *
 * Transforms applied during the token build pipeline:
 *  1. px_to_rem     — Convert pixel values to rem (base 16px)
 *  2. hex_to_oklch  — Convert hex colors to OKLCH color space
 *  3. px_to_rem_font — Font-size specific px→rem (preserves comments)
 */

// ─── px → rem transform ───────────────────────────────────────────────

/**
 * Converts px values to rem units (1rem = 16px).
 * Only transforms values that end with 'px', leaving other values untouched.
 * If the value contains multiple px values (e.g., shadows), each is converted.
 */
function pxToRem(token) {
  const value = token.value;

  // String values (e.g., "16px", "0 4px 16px rgba(...)")
  if (typeof value === 'string') {
    // Match all px values in the string
    return value.replace(
      /(\d+(?:\.\d+)?)px\b/g,
      (_match, digits) => {
        const rem = parseFloat(digits) / 16;
        // Round to 4 decimal places to avoid floating-point noise
        // Special case: 1px → 0.0625rem, keep it
        return `${Number(rem.toFixed(4))}rem`;
      }
    );
  }

  // Numeric values — treat as px
  if (typeof value === 'number') {
    const rem = value / 16;
    return `${Number(rem.toFixed(4))}rem`;
  }

  return value;
}

/**
 * Matcher: only apply to tokens with category "size" or value containing "px".
 * Skips breakpoints (they should stay as px for media queries).
 */
function pxToRemMatcher(token) {
  // Skip breakpoints
  if (token.path.includes('breakpoint')) return false;

  const cat = token.attributes?.category;
  if (cat === 'size') return true;

  const val = token.value;
  if (typeof val === 'string' && /px/.test(val) && !/shadow|blur/.test(token.path.join('/'))) return true;

  return false;
}

// ─── hex → oklch transform ────────────────────────────────────────────

/**
 * Converts hex color values to OKLCH format: oklch(L C H)
 * This is a pure JS implementation — no external dependencies required.
 *
 * OKLCH advantages over hex/RGB:
 *  - Perceptually uniform (equal changes look equal to the human eye)
 *  - Wide gamut support (P3, Rec.2020)
 *  - Accessible contrast calculations are more reliable
 *
 * Color pipeline: hex → sRGB → linear RGB → LMS → OKLab → OKLCH
 */

// sRGB to linear (gamma decode)
function srgbToLinear(c) {
  const abs = Math.abs(c);
  if (abs <= 0.04045) return c / 12.92;
  return (c < 0 ? -1 : 1) * Math.pow((abs + 0.055) / 1.055, 2.4);
}

function linearToSrgb(c) {
  const abs = Math.abs(c);
  if (abs <= 0.0031308) return c * 12.92;
  return (c < 0 ? -1 : 1) * (1.055 * Math.pow(abs, 1 / 2.4) - 0.055);
}

function hexToSrgb(hex) {
  hex = hex.replace(/^#/, '');
  const r = parseInt(hex.substring(0, 2), 16) / 255;
  const g = parseInt(hex.substring(2, 4), 16) / 255;
  const b = parseInt(hex.substring(4, 6), 16) / 255;
  const a = hex.length === 8 ? parseInt(hex.substring(6, 8), 16) / 255 : undefined;
  return { r, g, b, a };
}

function srgbToOklch({ r, g, b, a }) {
  // sRGB → linear
  const lr = srgbToLinear(r);
  const lg = srgbToLinear(g);
  const lb = srgbToLinear(b);

  // linear sRGB → LMS
  const l = 0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb;
  const m = 0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb;
  const s = 0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb;

  // LMS → OKLab (cube roots)
  const l_ = Math.cbrt(l);
  const m_ = Math.cbrt(m);
  const s_ = Math.cbrt(s);

  const L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_;
  const A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_;
  const B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_;

  // OKLab → OKLCH
  const C = Math.sqrt(A * A + B * B);
  let H = Math.atan2(B, A) * (180 / Math.PI);
  if (H < 0) H += 360;

  if (a !== undefined && a < 1) {
    return `oklch(${L.toFixed(4)} ${C.toFixed(4)} ${H.toFixed(1)} / ${a})`;
  }
  return `oklch(${L.toFixed(4)} ${C.toFixed(4)} ${H.toFixed(1)})`;
}

function hexToOklch(token) {
  const value = token.value;

  if (typeof value !== 'string') return value;

  // Match hex colors (#RGB, #RRGGBB, #RRGGBBAA)
  const hexRegex = /#([0-9a-fA-F]{3,8})\b/g;

  return value.replace(hexRegex, (hex) => {
    // Normalize shorthand hex
    let expanded = hex.replace(/^#/, '');
    if (expanded.length === 3) {
      expanded = expanded[0] + expanded[0] + expanded[1] + expanded[1] + expanded[2] + expanded[2];
      hex = '#' + expanded;
    }
    try {
      const srgb = hexToSrgb(hex);
      // Only convert if it looks like a color, not a transparency-only hex
      if (srgb.r === 0 && srgb.g === 0 && srgb.b === 0) return hex; // pure black stays
      return srgbToOklch(srgb);
    } catch {
      return value; // fallback
    }
  });
}

function hexToOklchMatcher(token) {
  const val = token.value;
  if (typeof val !== 'string') return false;
  return /#[0-9a-fA-F]/.test(val);
}

// ─── Font-specific px → rem ───────────────────────────────────────────

const fontSizeToRem = {
  type: 'value',
  name: 'fontSizes/pxToRem',
  transitive: true,
  matcher: (token) => {
    return token.path.includes('fontSize') || token.path.includes('font-size');
  },
  transformer: (token) => {
    const val = token.value;
    if (typeof val === 'string' && val.endsWith('px')) {
      const px = parseFloat(val);
      return `${parseFloat((px / 16).toFixed(4))}rem`;
    }
    return val;
  }
};

// ─── Export ────────────────────────────────────────────────────────────

export const transforms = {
  pxToRem,
  pxToRemMatcher,
  hexToOklch,
  hexToOklchMatcher,
  fontSizeToRem,
};

export function registerTransforms(StyleDictionary) {
  StyleDictionary.registerTransform({
    name: 'size/pxToRem',
    type: 'value',
    transitive: true,
    matcher: pxToRemMatcher,
    transformer: pxToRem,
  });

  StyleDictionary.registerTransform({
    name: 'color/hexToOklch',
    type: 'value',
    transitive: true,
    matcher: hexToOklchMatcher,
    transformer: hexToOklch,
  });

  StyleDictionary.registerTransform(fontSizeToRem);

  // Register custom transform groups
  StyleDictionary.registerTransformGroup({
    name: 'custom/css',
    transforms: [
      'attribute/cti',
      'name/cti/kebab',
      'color/hexToOklch',
      'size/pxToRem',
      'time/ms',
    ],
  });

  StyleDictionary.registerTransformGroup({
    name: 'custom/json',
    transforms: [
      'attribute/cti',
      'name/cti/kebab',
      'color/hexToOklch',
      'size/pxToRem',
      'time/ms',
    ],
  });

  StyleDictionary.registerTransformGroup({
    name: 'custom/ts',
    transforms: [
      'attribute/cti',
      'name/cti/camel',
      'color/hexToOklch',
      'size/pxToRem',
      'time/ms',
    ],
  });

  StyleDictionary.registerTransformGroup({
    name: 'custom/figma',
    transforms: [
      'attribute/cti',
      'name/cti/kebab',
      // Figma consumes raw hex values — no oklch conversion for Figma tokens
      'size/pxToRem',
    ],
  });
}
