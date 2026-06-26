# Web Security Implementation Guide

**Generated:** 2026-06-26  
**Agent:** web-security-engineer  
**Scope:** Production web application hardening — CSP, CORS, CSRF, XSS, SQLi, Security Headers, OWASP Top 10

---

## Table of Contents

1. [Content Security Policy (CSP) Builder](#1-content-security-policy-csp-builder)
2. [CORS Configuration Per Endpoint](#2-cors-configuration-per-endpoint)
3. [CSRF Token Implementation](#3-csrf-token-implementation)
4. [XSS Prevention with DOMPurify](#4-xss-prevention-with-dompurify)
5. [SQL Injection Prevention with Parameterized Queries](#5-sql-injection-prevention-with-parameterized-queries)
6. [Security Headers](#6-security-headers)
7. [OWASP Top 10 Checklist](#7-owasp-top-10-checklist)

---

## 1. Content Security Policy (CSP) Builder

### 1.1 What Is CSP?

Content Security Policy is a browser defense-in-depth mechanism that restricts which resources (scripts, styles, images, fonts, etc.) a page can load and execute. A well-crafted CSP is the single most effective mitigation against XSS and data-injection attacks.

### 1.2 CSP Directive Reference

| Directive | Controls |
|-----------|----------|
| `default-src` | Fallback for all `*-src` directives |
| `script-src` | JavaScript sources and execution contexts |
| `style-src` | CSS sources |
| `img-src` | Image sources |
| `font-src` | Web font sources |
| `connect-src` | XHR, WebSocket, EventSource fetches |
| `frame-src` | Nested browsing contexts (`<iframe>`) |
| `frame-ancestors` | Who can embed this page (replaces `X-Frame-Options`) |
| `form-action` | Allowed destinations for `<form>` submissions |
| `base-uri` | Allowed `<base>` element values |
| `object-src` | Plugin sources (Flash, Java; lock down to `'none'`) |
| `report-uri` / `report-to` | Violation-report endpoint |

### 1.3 CSP Builder — Production-Grade Policy

```javascript
// csp-builder.js — Dynamic CSP builder for Express/Fastify/Koa
class CspBuilder {
  constructor() {
    this.directives = {
      'default-src':  ["'self'"],
      'script-src':   ["'self'"],
      'style-src':    ["'self'"],
      'img-src':      ["'self'", 'data:', 'https:'],
      'font-src':     ["'self'"],
      'connect-src':  ["'self'"],
      'frame-src':    ["'none'"],
      'frame-ancestors': ["'none'"],
      'form-action':  ["'self'"],
      'base-uri':     ["'self'"],
      'object-src':   ["'none'"],
      'upgrade-insecure-requests': [],
    };
    this.reportUri = null;
    this.reportTo = null;
  }

  // ── Fluent API ────────────────────────────────────────────
  add( directive, ...sources ) { this.directives[directive].push(...sources); return this; }
  set( directive, ...sources ) { this.directives[directive] = [...sources];  return this; }

  /** Hash an inline script so it survives CSP */
  static hashScript(code, algo = 'sha256') {
    const hash = require('crypto').createHash(algo).update(code).digest('base64');
    return `'${algo}-${hash}'`;
  }

  /** Generate a nonce value (regenerate per-request in production!) */
  static nonce() {
    return require('crypto').randomBytes(16).toString('base64');
  }

  /** Allow a specific CDN / third-party domain */
  allowCdn(domain) {
    ['script-src','style-src','img-src','font-src','connect-src'].forEach(d => {
      if (d === 'img-src' && this.directives[d]?.includes('https:')) return; // already wide open
      this.directives[d].push(domain);
    });
    return this;
  }

  /** Allow Google Tag Manager + Analytics */
  allowGoogleAnalytics() {
    this.directives['script-src'].push('https://www.googletagmanager.com',
                                       'https://www.google-analytics.com');
    this.directives['connect-src'].push('https://www.google-analytics.com');
    this.directives['img-src'].push('https://www.google-analytics.com');
    return this;
  }

  /** Allow Stripe */
  allowStripe() {
    this.directives['script-src'].push('https://js.stripe.com');
    this.directives['frame-src'].push('https://js.stripe.com');
    this.directives['connect-src'].push('https://api.stripe.com');
    return this;
  }

  /** Enable violation reports */
  reportToEndpoint(uri) { this.reportUri = uri; return this; }
  reportToGroup(group)  { this.reportTo  = group; return this; }

  /** Compose the final header value */
  toString() {
    const parts = [];
    for (const [key, values] of Object.entries(this.directives)) {
      if (values.length === 0 && key === 'upgrade-insecure-requests') {
        parts.push('upgrade-insecure-requests');
        continue;
      }
      if (values.length > 0) parts.push(`${key} ${values.join(' ')}`);
    }
    if (this.reportUri) parts.push(`report-uri ${this.reportUri}`);
    if (this.reportTo)  parts.push(`report-to ${this.reportTo}`);
    return parts.join('; ');
  }
}

// ── Usage Example ──────────────────────────────────────────
const csp = new CspBuilder()
  .allowCdn('https://cdn.example.com')
  .allowGoogleAnalytics()
  .allowStripe()
  .reportToEndpoint('/csp-violation-report');

console.log(csp.toString());
// default-src 'self'; script-src 'self' https://cdn.example.com https://www.googletagmanager.com https://www.google-analytics.com https://js.stripe.com; ...

// Apply as middleware (Express)
function cspMiddleware(req, res, next) {
  const policy = new CspBuilder()
    .allowCdn('https://cdn.example.com')
    .reportToEndpoint('/csp-violation-report');
  // Per-request nonce for inline scripts
  const nonce = CspBuilder.nonce();
  policy.add('script-src', `'nonce-${nonce}'`);
  res.locals.cspNonce = nonce;
  res.setHeader('Content-Security-Policy', policy.toString());
  next();
}
```

### 1.4 CSP in Different Frameworks

**Express (Node.js) — Helmet Middleware:**
```javascript
const helmet = require('helmet');
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc:          ["'self'"],
    scriptSrc:           ["'self'", "'unsafe-inline'"], // prefer nonces over unsafe-inline
    styleSrc:            ["'self'", 'https://fonts.googleapis.com'],
    fontSrc:             ["'self'", 'https://fonts.gstatic.com'],
    imgSrc:              ["'self'", 'data:', 'https:'],
    connectSrc:          ["'self'", 'https://api.example.com'],
    frameAncestors:      ["'none'"],
    formAction:          ["'self'"],
    upgradeInsecureRequests: [],
  },
  reportOnly: false,             // set true during rollout
}));
```

**Django (Python):**
```python
# settings.py
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC  = ("'self'", 'https://cdn.example.com')
CSP_STYLE_SRC   = ("'self'", "'unsafe-inline'", 'https://fonts.googleapis.com')
CSP_IMG_SRC     = ("'self'", 'data:', 'https:')
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_REPORT_URI  = '/csp-violation-report/'
```

**Nginx (reverse-proxy):**
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; frame-ancestors 'none';" always;
```

### 1.5 CSP Violation Report Endpoint

```javascript
// POST /csp-violation-report
app.post('/csp-violation-report', express.json({ type: 'application/csp-report' }), (req, res) => {
  const report = req.body['csp-report'];
  console.warn('CSP Violation:', {
    blockedUri:    report['blocked-uri'],
    violatedDirective: report['violated-directive'],
    documentUri:   report['document-uri'],
    originalPolicy: report['original-policy'],
    timestamp:     new Date().toISOString(),
  });
  // Ship to your observability stack
  metrics.increment('csp.violation', { directive: report['violated-directive'] });
  res.status(204).end();
});
```

---

## 2. CORS Configuration Per Endpoint

### 2.1 Understanding CORS

Cross-Origin Resource Sharing (CORS) controls which origins may access your API from a browser context. Wildcard (`*`) configurations are dangerous — every endpoint should declare the narrowest possible policy.

### 2.2 CORS Policy Builder

```javascript
// cors-builder.js — Endpoint-scoped CORS configuration
class CorsPolicy {
  constructor() {
    this.allowedOrigins      = [];    // exact origins, not regex unless manually checked
    this.allowedMethods      = ['GET', 'HEAD'];
    this.allowedHeaders      = ['Content-Type', 'Authorization'];
    this.exposedHeaders      = [];
    this.maxAge              = 86400; // 24h preflight cache
    this.credentials         = false;
  }

  allowOrigin(...origins)        { this.allowedOrigins = origins;     return this; }
  allowMethods(...methods)       { this.allowedMethods = methods;      return this; }
  allowHeaders(...headers)       { this.allowedHeaders = headers;      return this; }
  exposeHeaders(...headers)      { this.exposedHeaders = headers;      return this; }
  withCredentials()              { this.credentials    = true;         return this; }
  maxAge(seconds)               { this.maxAge         = seconds;      return this; }

  /** Build middleware for a single route group */
  middleware() {
    const policy = this;
    return (req, res, next) => {
      const origin = req.headers.origin;
      if (!origin) return next(); // same-origin request, no CORS needed

      if (!policy.allowedOrigins.includes(origin)) {
        return res.status(403).json({ error: 'Origin not allowed' });
      }

      res.setHeader('Access-Control-Allow-Origin',      policy.credentials ? origin : '*');
      if (policy.credentials) res.setHeader('Access-Control-Allow-Credentials', 'true');
      res.setHeader('Access-Control-Expose-Headers',    policy.exposedHeaders.join(', '));
      res.setHeader('Access-Control-Max-Age',           String(policy.maxAge));
      res.setHeader('Vary',                             'Origin');

      if (req.method === 'OPTIONS') {
        res.setHeader('Access-Control-Allow-Methods',   policy.allowedMethods.join(', '));
        res.setHeader('Access-Control-Allow-Headers',   policy.allowedHeaders.join(', '));
        return res.status(204).end();
      }
      next();
    };
  }
}
```

### 2.3 Per-Endpoint Configuration (Express Router)

```javascript
const express = require('express');
const router  = express.Router();

// ── Public endpoints: allow known web-app origins ──────────
const publicCors = new CorsPolicy()
  .allowOrigin('https://app.example.com', 'https://staging.example.com')
  .allowMethods('GET', 'POST', 'OPTIONS')
  .allowHeaders('Content-Type')
  .maxAge(86400);

router.use('/api/public',  publicCors.middleware());

// ── Authenticated endpoints: with credentials ─────────────
const authCors = new CorsPolicy()
  .allowOrigin('https://app.example.com')
  .allowMethods('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS')
  .allowHeaders('Content-Type', 'Authorization', 'X-CSRF-Token')
  .exposeHeaders('X-Request-Id')
  .withCredentials();

router.use('/api/user',    authCors.middleware());
router.use('/api/orders',  authCors.middleware());

// ── Webhook endpoints: ONLY from a single partner origin ──
const webhookCors = new CorsPolicy()
  .allowOrigin('https://partner.example.com')
  .allowMethods('POST', 'OPTIONS')
  .allowHeaders('Content-Type', 'X-Webhook-Signature');

router.use('/api/webhooks/stripe', webhookCors.middleware());

// ── Admin endpoints: internal-origin only ──────────────────
const adminCors = new CorsPolicy()
  .allowOrigin('https://admin.internal.example.com')
  .allowMethods('GET', 'POST', 'PUT', 'DELETE', 'OPTIONS')
  .allowHeaders('Content-Type', 'Authorization')
  .withCredentials();

router.use('/api/admin', adminCors.middleware());

module.exports = router;
```

### 2.4 CORS Quick Reference

| Risk Level | Configuration | When to Use |
|------------|--------------|-------------|
| 🔴 Critical | `Access-Control-Allow-Origin: *` + credentials | **Never** — browsers reject this combo, but never try |
| 🟠 High | `Access-Control-Allow-Origin: *` | Public CDN assets only (no credentials) |
| 🟡 Medium | Dynamic origin reflection | Ensure origin is validated against an allowlist |
| 🟢 Safe | Static allowlist + credentials | All authenticated API endpoints |

---

## 3. CSRF Token Implementation

### 3.1 Approach: Double-Submit Cookie Pattern

The server sets a cryptographically random token both as a cookie **and** requires it in a custom request header. Browsers enforce that a cross-origin page cannot read the cookie (SameSite) nor set the custom header, so CSRF is blocked.

### 3.2 Node.js Implementation (Express)

```javascript
// csrf.js — Production CSRF middleware using double-submit cookie pattern
const crypto = require('crypto');

const CSRF_COOKIE = 'csrf-token';
const CSRF_HEADER = 'x-csrf-token';

function generateToken() {
  return crypto.randomBytes(32).toString('hex');
}

// ── Middleware: sets CSRF token on GET requests ────────────
function csrfTokenProvider(req, res, next) {
  if (!req.cookies?.[CSRF_COOKIE]) {
    const token = generateToken();
    res.cookie(CSRF_COOKIE, token, {
      httpOnly: false,     // JS must read it to set the header
      secure: true,        // HTTPS only
      sameSite: 'strict',  // Blocks cross-origin cookie send
      path: '/',
      maxAge: 86400 * 1000, // 24h
    });
    res.locals.csrfToken = token;
  } else {
    res.locals.csrfToken = req.cookies[CSRF_COOKIE];
  }
  next();
}

// ── Middleware: validate CSRF token on mutating requests ───
function csrfProtection(req, res, next) {
  const safeMethods = ['GET', 'HEAD', 'OPTIONS'];
  if (safeMethods.includes(req.method)) return next();

  const cookieToken = req.cookies?.[CSRF_COOKIE];
  const headerToken = req.headers[CSRF_HEADER];

  if (!cookieToken || !headerToken) {
    return res.status(403).json({ error: 'CSRF token missing' });
  }

  // Constant-time comparison to prevent timing attacks
  try {
    if (!crypto.timingSafeEqual(
          Buffer.from(cookieToken, 'utf8'),
          Buffer.from(headerToken, 'utf8'))) {
      return res.status(403).json({ error: 'CSRF token mismatch' });
    }
  } catch {
    return res.status(403).json({ error: 'CSRF token invalid' });
  }

  next();
}

// ── Usage ──────────────────────────────────────────────────
app.use(cookieParser());           // cookie-parser middleware
app.use(csrfTokenProvider);        // runs on every request
app.use('/api', csrfProtection);   // protect all API mutating calls
```

### 3.3 Frontend Integration

```javascript
// csrf-client.js — Client-side CSRF helper
const CSRF_COOKIE = 'csrf-token';
const CSRF_HEADER = 'x-csrf-token';

// Read token from cookie and attach to every mutating request
function getCsrfToken() {
  const match = document.cookie.match(new RegExp(`(?:^|;\\s*)${CSRF_COOKIE}=([^;]*)`));
  return match ? match[1] : null;
}

async function apiFetch(url, options = {}) {
  const method = (options.method || 'GET').toUpperCase();
  const headers = { ...options.headers };

  if (!['GET', 'HEAD', 'OPTIONS'].includes(method)) {
    headers[CSRF_HEADER] = getCsrfToken();
  }
  headers['Content-Type'] = headers['Content-Type'] || 'application/json';

  return fetch(url, { ...options, method, headers, credentials: 'include' });
}

// Usage:
// apiFetch('/api/user/profile', { method: 'PUT', body: JSON.stringify({ name: 'Alice' }) });
```

### 3.4 CSRF in Other Frameworks

**Django:**
```python
# Enabled by default via CsrfViewMiddleware
# Frontend reads token from cookie 'csrftoken' and sends in header 'X-CSRFToken'
# settings.py
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False      # JS must read it
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = ['https://app.example.com']
```

**Laravel (PHP):**
```php
// VerifyCsrfToken middleware is auto-applied
// Blade template:
// <meta name="csrf-token" content="{{ csrf_token() }}">
// axios.defaults.headers.common['X-CSRF-TOKEN'] = document.querySelector('meta[name="csrf-token"]').content;
```

### 3.5 CSRF Checklist

- [ ] Use `SameSite=Strict` or `SameSite=Lax` on session cookies
- [ ] Require custom header (`X-CSRF-Token`) for all state-changing requests
- [ ] Use constant-time comparison for token validation
- [ ] Regenerate token after login / privilege escalation
- [ ] Set `httpOnly: false` on the CSRF cookie (JS needs access) — **only for CSRF token, not session cookie**
- [ ] Enforce HTTPS for cookie delivery (`secure: true`)

---

## 4. XSS Prevention with DOMPurify

### 4.1 The Golden Rule

> **Never insert unsanitized data into the DOM.** Use DOMPurify for HTML sanitization and always context-encode output.

### 4.2 DOMPurify Setup

```html
<!-- Install via npm: npm install dompurify -->
<!-- Or CDN: -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.0/purify.min.js"></script>
```

### 4.3 Sanitization Patterns

```javascript
// xss-prevention.js — DOMPurify-driven XSS defense
import DOMPurify from 'dompurify';

// ── 1. Sanitize user HTML (rich-text comments, etc.) ───────
function sanitizeHtml(dirty) {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: [
      'b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre',
      'img', 'span', 'div', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    ],
    ALLOWED_ATTR: [
      'href', 'target', 'rel', 'src', 'alt', 'width', 'height',
      'class', 'id', 'style',
    ],
    ALLOW_DATA_ATTR: false,         // block data-* attributes
    ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto|tel):|[^a-z]|[a-z+.-]+(?:[^a-z+.-:]|$))/i,
    // Block javascript: and data: URIs except data:image/*
  });
}

// ── 2. Strip ALL HTML (plain text only) ────────────────────
function stripAllHtml(dirty) {
  return DOMPurify.sanitize(dirty, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
}

// ── 3. Sanitize for an attribute context ───────────────────
function sanitizeAttr(dirty) {
  // Use when inserting into href, src, etc.
  return DOMPurify.sanitize(dirty, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
}

// ── 4. DOM insertion helpers ───────────────────────────────
function safeSetInnerHTML(element, html) {
  element.innerHTML = DOMPurify.sanitize(html);
}

function safeSetTextContent(element, text) {
  // No sanitization needed — textContent auto-escapes
  element.textContent = text;
}

// ── 5. Trusted Types integration ──────────────────────────
if (window.trustedTypes?.createPolicy) {
  window.trustedTypes.createPolicy('default', {
    createHTML: (input) => DOMPurify.sanitize(input),
    createScriptURL: (input) => {
      const allowed = ['https://cdn.example.com', 'https://www.googletagmanager.com'];
      return allowed.some(origin => input.startsWith(origin)) ? input : '';
    },
  });
}
```

### 4.4 Context-Specific Output Encoding

```javascript
// escape-utils.js — Output encoding for every context
const entityMap = {
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;',
  "'": '&#x27;', '/': '&#x2F;', '`': '&#x60;', '=': '&#x3D;',
};

function escapeHtml(str) {
  return String(str).replace(/[&<>"'`=/]/g, char => entityMap[char]);
}

function escapeAttribute(str) {
  // Use for HTML attributes: <div data-x="...">
  return escapeHtml(str);
}

function escapeJavaScript(str) {
  return JSON.stringify(str).slice(1, -1); // encodes \n, \t, \", etc.
}

function escapeCss(str) {
  return String(str).replace(/[^a-zA-Z0-9-_.]/g, ''); // CSS identifier safe
}

function escapeUrl(str) {
  return encodeURIComponent(str);
}
```

### 4.5 Template Engine Hardening

**Handlebars:**
```javascript
// Always use triple-brace {{{ }}} ONLY with sanitized input
Handlebars.registerHelper('sanitize', (text) => {
  return new Handlebars.SafeString(DOMPurify.sanitize(text));
});
// In templates: {{{sanitize userBio}}} — never raw {{{userBio}}}
```

**React (JSX):**
```jsx
// JSX auto-escapes by default — safe
<div>{userInput}</div>

// DANGEROUS: dangerouslySetInnerHTML — ALWAYS sanitize
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userHtml) }} />
```

---

## 5. SQL Injection Prevention with Parameterized Queries

### 5.1 The Rule

> **Never concatenate user input into SQL strings.** Use parameterized queries (prepared statements) 100% of the time. No exceptions.

### 5.2 Node.js / PostgreSQL (pg / node-postgres)

```javascript
// ✅ CORRECT — Parameterized query with pg
const { Pool } = require('pg');
const pool = new Pool({ /* config */ });

async function getUserById(userId) {
  const result = await pool.query(
    'SELECT id, name, email FROM users WHERE id = $1',
    [userId]                              // parameter binding
  );
  return result.rows[0];
}

async function searchProducts(filters) {
  let query = 'SELECT * FROM products WHERE 1=1';
  const params = [];
  let paramIndex = 1;

  if (filters.category) {
    query += ` AND category = $${paramIndex++}`;
    params.push(filters.category);
  }
  if (filters.minPrice) {
    query += ` AND price >= $${paramIndex++}`;
    params.push(filters.minPrice);
  }
  // ✅ Safe: dynamic column names must be whitelisted
  if (filters.sortBy && ['name','price','created_at'].includes(filters.sortBy)) {
    const direction = filters.order === 'desc' ? 'DESC' : 'ASC';
    query += ` ORDER BY ${filters.sortBy} ${direction}`; // whitelist-checked
  }
  return pool.query(query, params);
}

// ❌ WRONG — String interpolation (SQLi vulnerable)
// const query = `SELECT * FROM users WHERE id = ${userId}`; // NEVER DO THIS
```

### 5.3 Node.js / MySQL (mysql2)

```javascript
const mysql = require('mysql2/promise');
const conn  = await mysql.createConnection({ /* config */ });

// ✅ Named placeholders
const [rows] = await conn.execute(
  'SELECT * FROM users WHERE email = :email AND status = :status',
  { email: userEmail, status: 'active' }
);

// ✅ Positional placeholders
const [rows2] = await conn.execute(
  'INSERT INTO orders (user_id, total) VALUES (?, ?)',
  [userId, total]
);
```

### 5.4 Python / SQLAlchemy

```python
from sqlalchemy import text
from sqlalchemy.orm import Session

# ✅ ORM query — auto-escaped
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# ✅ Raw SQL with bind parameters
def get_user_raw(db: Session, user_id: int):
    result = db.execute(
        text("SELECT id, name FROM users WHERE id = :uid"),
        {"uid": user_id}
    )
    return result.fetchone()

# ❌ WRONG — f-string in SQL
# db.execute(text(f"SELECT * FROM users WHERE id = {user_id}"))  # SQLi!
```

### 5.5 Python / Django ORM

```python
# ✅ ORM filter — auto-escaped
User.objects.filter(id=user_id).first()

# ✅ Raw SQL with params
User.objects.raw('SELECT * FROM users WHERE id = %s', [user_id])

# ✅ Custom SQL via cursor
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
    rows = cursor.fetchall()

# ❌ NEVER use .extra() with user-supplied strings in select/where
```

### 5.6 Handling Dynamic Table/Column Names

Dynamic identifiers **cannot be parameterized**. You must whitelist:

```javascript
// ✅ Whitelist approach for dynamic column/table names
const ALLOWED_TABLES = new Set(['users', 'orders', 'products']);
const ALLOWED_COLUMNS = new Set(['id', 'name', 'email', 'created_at']);
const ALLOWED_DIRECTIONS = new Set(['ASC', 'DESC']);

function buildDynamicQuery(table, column, direction) {
  if (!ALLOWED_TABLES.has(table))   throw new Error('Invalid table');
  if (!ALLOWED_COLUMNS.has(column)) throw new Error('Invalid column');
  if (!ALLOWED_DIRECTIONS.has(direction.toUpperCase())) throw new Error('Invalid direction');

  // Now safe to interpolate
  return `SELECT * FROM ${table} ORDER BY ${column} ${direction.toUpperCase()} LIMIT $1`;
}
```

### 5.7 ORM Considerations

ORMs protect against SQLi for simple queries, but **raw/execute methods are still dangerous** if you interpolate user input. Audit every `.raw()`, `.execute()`, and `.query()` call.

---

## 6. Security Headers

### 6.1 Complete Security-Header Middleware

```javascript
// security-headers.js — One middleware to set all critical headers
function securityHeaders(req, res, next) {

  // ── HTTP Strict Transport Security (HSTS) ─────────────────
  // Forces HTTPS for the entire domain. max-age in seconds.
  res.setHeader(
    'Strict-Transport-Security',
    'max-age=63072000; includeSubDomains; preload'
    // 2 years, all subdomains, eligible for browser preload list
  );

  // ── X-Frame-Options ───────────────────────────────────────
  // Prevents clickjacking. Use CSP frame-ancestors instead if CSP is set.
  res.setHeader('X-Frame-Options', 'DENY'); // or 'SAMEORIGIN'

  // ── X-Content-Type-Options ────────────────────────────────
  // Prevents MIME-type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // ── Referrer-Policy ───────────────────────────────────────
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');

  // ── Permissions-Policy ────────────────────────────────────
  // Disables browser features you don't use
  res.setHeader(
    'Permissions-Policy',
    [
      'camera=()',                // block camera access
      'microphone=()',            // block microphone
      'geolocation=(self)',       // allow on own origin
      'payment=()',               // block Payment Request API
      'usb=()',                   // block WebUSB
      'fullscreen=(self)',        // allow fullscreen on own origin
      'accelerometer=()',
      'autoplay=()',
      'clipboard-read=(self)',    // allow clipboard read on own origin
      'clipboard-write=(self)',
      'display-capture=()',       // block screen capture
      'interest-cohort=()',       // opt out of FLoC
    ].join(', ')
  );

  // ── Cross-Origin-Embedder-Policy ──────────────────────────
  // Set only if you need SharedArrayBuffer / high-res timers
  // res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');

  // ── Cross-Origin-Opener-Policy ────────────────────────────
  res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');

  // ── Cross-Origin-Resource-Policy ──────────────────────────
  res.setHeader('Cross-Origin-Resource-Policy', 'same-origin');

  // ── Cache-Control for sensitive pages ─────────────────────
  if (req.path.startsWith('/api/') || req.path.startsWith('/dashboard')) {
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, private');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
  }

  next();
}

module.exports = securityHeaders;
```

### 6.2 Header Reference Table

| Header | Recommended Value | Purpose |
|--------|-------------------|---------|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` | Force HTTPS |
| `X-Frame-Options` | `DENY` | Block clickjacking |
| `X-Content-Type-Options` | `nosniff` | Block MIME sniffing |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Limit referrer leakage |
| `Permissions-Policy` | See above | Disable unused browser APIs |
| `Cross-Origin-Opener-Policy` | `same-origin` | Process isolation |
| `Cross-Origin-Resource-Policy` | `same-origin` | Block cross-origin resource reads |
| `X-XSS-Protection` | `0` | **Deprecated** — rely on CSP instead |
| `X-Powered-By` | Remove it | Don't leak server technology |
| `Server` | Remove it | Don't leak server version |

### 6.3 Nginx Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    # Remove server tokens
    server_tokens off;
    proxy_hide_header X-Powered-By;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # Anti-clickjacking
    add_header X-Frame-Options "DENY" always;

    # Anti-MIME sniffing
    add_header X-Content-Type-Options "nosniff" always;

    # Referrer policy
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Permissions policy
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=(self), payment=()" always;

    # Cross-origin isolation
    add_header Cross-Origin-Opener-Policy "same-origin" always;
    add_header Cross-Origin-Resource-Policy "same-origin" always;

    # Content Security Policy
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self'" always;
}
```

### 6.4 Testing Security Headers

```bash
# Test with curl
curl -I https://example.com

# Use Mozilla Observatory
# https://observatory.mozilla.org/

# Use securityheaders.com
# https://securityheaders.com/
```

---

## 7. OWASP Top 10 Checklist (2021)

### A01: Broken Access Control

- [ ] Enforce deny-by-default for all resources
- [ ] Implement role-based access control (RBAC) with server-side enforcement
- [ ] Never rely on client-side hiding of UI elements
- [ ] Validate object-level authorization (can user X access record Y?)
- [ ] Rate-limit API endpoints to prevent enumeration
- [ ] Invalidate JWT tokens on logout / password change
- [ ] Use UUIDs or opaque IDs instead of sequential integers in URLs

```javascript
// Example: Object-level authorization middleware
async function authorizeOwnership(model, paramName = 'id') {
  return async (req, res, next) => {
    const record = await model.findByPk(req.params[paramName]);
    if (!record) return res.status(404).json({ error: 'Not found' });
    if (record.userId !== req.user.id) return res.status(403).json({ error: 'Forbidden' });
    req.record = record;
    next();
  };
}
router.put('/api/orders/:id', authorizeOwnership(Order), updateOrder);
```

### A02: Cryptographic Failures

- [ ] Encrypt data in transit (TLS 1.3 minimum, TLS 1.2 acceptable)
- [ ] Encrypt sensitive data at rest (AES-256-GCM, not ECB)
- [ ] Never write your own crypto — use well-vetted libraries (libsodium, Node crypto)
- [ ] Hash passwords with bcrypt, scrypt, or Argon2id (NEVER MD5/SHA1/SHA256 directly)
- [ ] Use secure, random token generation (`crypto.randomBytes`, not `Math.random()`)
- [ ] Rotate keys regularly; never hardcode secrets

```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

async function hashPassword(plain) {
  return bcrypt.hash(plain, SALT_ROUNDS);
}
async function verifyPassword(plain, hash) {
  return bcrypt.compare(plain, hash);
}
```

### A03: Injection

- [ ] Use parameterized queries 100% of the time (see [Section 5](#5-sql-injection-prevention-with-parameterized-queries))
- [ ] Sanitize HTML with DOMPurify (see [Section 4](#4-xss-prevention-with-dompurify))
- [ ] Validate and escape all user input in shell commands — avoid `exec()` with user data
- [ ] Use an allowlist for ORM operators and dynamic field names
- [ ] Disable LDAP/OS command execution in DB if not needed

### A04: Insecure Design

- [ ] Threat-model every feature before coding
- [ ] Limit input sizes and types (validate on server, not just client)
- [ ] Implement rate-limiting on login, password reset, and API endpoints
- [ ] Use proper error handling that doesn't leak stack traces to clients
- [ ] Segregate tenants in multi-tenant apps at the data layer

### A05: Security Misconfiguration

- [ ] Set all security headers (see [Section 6](#6-security-headers))
- [ ] Disable directory listing on web server
- [ ] Remove default credentials, sample apps, and debug endpoints in production
- [ ] Set `NODE_ENV=production` (or equivalent)
- [ ] Disable verbose error messages
- [ ] Keep dependencies updated (run `npm audit` / `pip audit` regularly)
- [ ] Use security.txt and CORS policies to report vulnerabilities

### A06: Vulnerable and Outdated Components

- [ ] Inventory all dependencies (SBOM)
- [ ] Run automated vulnerability scanning in CI/CD (`npm audit`, `snyk`, `dependabot`)
- [ ] Subscribe to security advisories for your stack
- [ ] Remove unused dependencies
- [ ] Pin dependency versions; use lockfiles

```bash
# Quick audit scripts
npm audit --production        # Node.js
pip-audit                     # Python
bundle audit                  # Ruby
```

### A07: Identification and Authentication Failures

- [ ] Enforce MFA for all privileged accounts
- [ ] Prevent credential stuffing with rate-limiting and breach-password detection
- [ ] Enforce strong password policies (min 12 chars, check against haveibeenpwned API)
- [ ] Use secure session management: `httpOnly`, `secure`, `SameSite` cookies
- [ ] Implement account lockout after N failed attempts (with cooldown, not permanent)
- [ ] Session IDs must be regenerated after login, privilege change, and logout
- [ ] Never expose session IDs in URLs

```javascript
// Session configuration (express-session)
app.use(session({
  name: 'sessionId',               // don't use default 'connect.sid'
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,                 // block JS access
    secure: true,                   // HTTPS only
    sameSite: 'strict',             // block cross-origin
    maxAge: 3600000,                // 1 hour
  },
}));

// Regenerate session after login
req.session.regenerate((err) => {
  req.session.userId = user.id;
});
```

### A08: Software and Data Integrity Failures

- [ ] Verify integrity of third-party scripts with Subresource Integrity (SRI)
- [ ] Sign and verify serialized objects (JWT signatures, not just decode)
- [ ] Use checksums for CI/CD pipeline artifacts
- [ ] Never `eval()` or `require()` dynamic code from untrusted sources
- [ ] Pin CI/CD actions to commit hashes, not branch names

```html
<!-- SRI: Subresource Integrity -->
<script src="https://cdn.example.com/lib.js"
        integrity="sha384-abc123..."
        crossorigin="anonymous"></script>
```

### A09: Security Logging and Monitoring Failures

- [ ] Log all authentication events (login, logout, password change, MFA)
- [ ] Log all access-control failures (403s)
- [ ] Log input validation failures
- [ ] Never log credentials, tokens, or PII in cleartext
- [ ] Use structured logging with correlation IDs
- [ ] Set up real-time alerting for suspicious patterns
- [ ] Retain logs per compliance requirements (GDPR: 30-90 days typical)

```javascript
// Structured security event logging
function logSecurityEvent(event) {
  const entry = {
    timestamp: new Date().toISOString(),
    correlationId: event.correlationId || crypto.randomUUID(),
    event: event.type,
    userId: event.userId || null,
    ip: event.ip,
    userAgent: event.userAgent,
    metadata: event.metadata,
  };
  // Redact sensitive fields
  delete entry.metadata?.password;
  delete entry.metadata?.token;
  console.log(JSON.stringify(entry)); // ship to SIEM
}
```

### A10: Server-Side Request Forgery (SSRF)

- [ ] Validate and sanitize all user-supplied URLs before fetching
- [ ] Use an allowlist of permitted domains/protocols
- [ ] Block requests to internal IP ranges (10.x, 172.16-31.x, 192.168.x, 127.x, 169.254.x)
- [ ] Disable HTTP redirect following or validate redirect targets
- [ ] Use a separate egress proxy with network segmentation

```javascript
const dns = require('dns').promises;
const BLOCKED_RANGES = [
  /^10\./, /^172\.(1[6-9]|2\d|3[01])\./, /^192\.168\./,
  /^127\./, /^169\.254\./, /^0\./, /^fc00:/, /^fe80:/,
];

async function validateUrl(url) {
  const parsed = new URL(url);
  if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('Protocol not allowed');

  const addresses = await dns.resolve(parsed.hostname);
  for (const addr of addresses) {
    if (BLOCKED_RANGES.some(r => r.test(addr))) {
      throw new Error(`Blocked internal IP: ${addr}`);
    }
  }
  return parsed;
}
```

### OWASP Top 10 — Quick-Audit Script

```bash
#!/bin/bash
# security-audit.sh — Quick OWASP Top 10 compliance check
echo "=== OWASP Top 10 Quick Audit ==="

echo -n "[A01] Access Control: grep for 'admin' routes... "
grep -r "admin" routes/ controllers/ | wc -l

echo -n "[A02] Crypto: checking for bcrypt/scrypt/argon2... "
grep -r "bcrypt\|scrypt\|argon2" . 2>/dev/null | head -1 || echo "MISSING!"

echo -n "[A03] Injection: checking for string concat in SQL... "
grep -r "SELECT.*\${" . 2>/dev/null | wc -l || echo "0 (good)"

echo -n "[A05] Misconfig: checking NODE_ENV... "
echo $NODE_ENV

echo -n "[A06] Dependencies: running npm audit... "
npm audit --audit-level=high 2>/dev/null || echo "not a Node project"

echo "=== Done ==="
```

---

## Appendix: Quick-Reference Security Cheatsheet

### Headers Checklist

| Header | Set? | Value |
|--------|------|-------|
| `Content-Security-Policy` | ☐ | Nonce-based or strict-dynamic |
| `Strict-Transport-Security` | ☐ | `max-age=63072000; includeSubDomains` |
| `X-Frame-Options` | ☐ | `DENY` |
| `X-Content-Type-Options` | ☐ | `nosniff` |
| `Referrer-Policy` | ☐ | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | ☐ | Camera/Mic disabled, minimal grants |
| `Cross-Origin-Opener-Policy` | ☐ | `same-origin` |
| `Cross-Origin-Resource-Policy` | ☐ | `same-origin` |

### Input Validation By Context

| Context | Defense |
|---------|---------|
| SQL query | Parameterized queries / prepared statements |
| HTML body | DOMPurify sanitization |
| HTML attribute | `escapeHtml()` + quotes |
| JavaScript string | `JSON.stringify()` or `escapeJavaScript()` |
| CSS value | `escapeCss()` |
| URL parameter | `encodeURIComponent()` |
| Shell command | Avoid entirely; use spawn with argument arrays |
| File path | Resolve + validate against allowed directory |

### Never Do This

```javascript
// ❌❌❌ Anti-patterns — NEVER copy these ❌❌❌

// SQLi
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// XSS
element.innerHTML = userInput;

// CSRF vulnerable
app.use(cors({ origin: '*' }));  // with credentials

// Crypto
const token = Math.random().toString(36);  // NOT cryptographically secure

// Password hashing
const hash = md5(password);  // MD5 is broken

// Secrets
const apiKey = 'sk_live_abc123';  // never hardcode secrets in code

// SSRF
fetch(userSuppliedUrl);  // without validation

// Eval
eval(userSuppliedCode);  // remote code execution
```

---

*End of Web Security Implementation Guide. Review and adapt each section to your stack and threat model.*
