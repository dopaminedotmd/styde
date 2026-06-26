# Advanced Web Security Engineering Guide — Tier C2

**Generated:** 2026-06-26T02:00:00Z
**Agent:** web-security-engineer (c2)
**Scope:** Supply-chain security (SLSA/SBOM), RASP, ML-driven API abuse detection, subresource integrity automation, real-time threat feed integration
**Predecessor:** run-20260626-000800 (Foundational: CSP, CORS, CSRF, XSS, SQLi, Security Headers, OWASP Top 10)

---

## Table of Contents

1. [Supply-Chain Security with SLSA & SBOM](#1-supply-chain-security-with-slsa--sbom)
2. [Runtime Application Self-Protection (RASP)](#2-runtime-application-self-protection-rasp)
3. [API Abuse Detection with Machine Learning](#3-api-abuse-detection-with-machine-learning)
4. [Subresource Integrity Automation](#4-subresource-integrity-automation)
5. [Real-Time Threat Feed Integration](#5-real-time-threat-feed-integration)

---

## 1. Supply-Chain Security with SLSA & SBOM

### 1.1 Threat Model

Modern web applications ingest hundreds — often thousands — of transitive dependencies. Each is a potential attack vector. The 2020 SolarWinds breach, 2021 Codecov compromise, and 2024 xz-utils backdoor demonstrated that supply-chain attacks bypass traditional perimeter defenses. The defense is **attestation**: proving what went into the build and that the build process itself is tamper-proof.

### 1.2 SLSA Framework (Supply-chain Levels for Software Artifacts)

SLSA defines four levels of increasing rigor. Your goal is **SLSA Level 3** for production artifacts.

| Level | Name | Requirement |
|-------|------|-------------|
| **L0** | None | No guarantees |
| **L1** | Provenance | Build process documented; provenance attestation generated |
| **L2** | Hosted Build + Signed Provenance | Build runs on a hosted CI/CD platform; provenance is signed and verifiable |
| **L3** | Hardened Build | Build runs in an isolated, ephemeral environment; source and build are fully auditable; two-person review required |
| **L4** | Hermetic + Reproducible | Build is fully hermetic (no network access); builds are byte-for-byte reproducible |

#### 1.2.1 SLSA Provenance Generator (GitHub Actions)

```yaml
# .github/workflows/slsa-provenance.yml — Generate SLSA L3 provenance
name: SLSA Provenance Generation
on:
  push:
    tags: ['v*']
  workflow_dispatch:

permissions:
  id-token: write      # Required for OIDC token → Sigstore
  contents: read
  actions: read
  attestations: write

jobs:
  build-and-attest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11  # pin to commit hash

      - name: Setup Node
        uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8
        with:
          node-version: 22

      - name: Install dependencies
        run: npm ci    # strict install from lockfile; no package.json resolution

      - name: Build
        run: npm run build

      # ─── Generate SLSA provenance attestation ────────────
      - name: Generate build provenance
        uses: slsa-framework/slsa-github-generator/.github/actions/generate-provenance@v2.1.0
        with:
          base64-subjects: "${{ needs.build.outputs.hashes }}"

      - name: Upload provenance
        uses: actions/upload-artifact@v4
        with:
          name: slsa-provenance
          path: provenance.intoto.jsonl
```

#### 1.2.2 Verifying SLSA Provenance at Deployment

```javascript
// verify-provenance.js — Gate deployment on valid SLSA provenance
const { execSync } = require('child_process');
const fs = require('fs');
const crypto = require('crypto');

class ProvenanceVerifier {
  constructor({ trustedBuilderIds, policyPath }) {
    this.trustedBuilderIds = trustedBuilderIds;  // e.g. ['https://github.com/slsa-framework/slsa-github-generator/.github/workflows/builder_go_slsa3.yml@refs/tags/v2.1.0']
    this.policyPath = policyPath;
  }

  /** Verify a provenance attestation against the artifact */
  verify(artifactPath, provenancePath) {
    // 1. Extract subject digest from provenance
    const provenance = JSON.parse(fs.readFileSync(provenancePath, 'utf8'));
    const subjects = provenance.subject || [];
    const artifactHash = this._sha256(artifactPath);

    const matched = subjects.find(s => {
      return s.digest && s.digest.sha256 === artifactHash;
    });
    if (!matched) {
      throw new Error(`Artifact hash ${artifactHash} not found in provenance subjects`);
    }

    // 2. Verify builder identity
    const builderId = provenance.predicate?.buildDefinition?.buildType ||
                      provenance.predicate?.builder?.id;
    if (!this.trustedBuilderIds.includes(builderId)) {
      throw new Error(`Untrusted builder: ${builderId}`);
    }

    // 3. Verify signature with Cosign / Sigstore
    try {
      execSync(
        `cosign verify-blob --certificate-identity "${builderId}" ` +
        `--signature <(cat "${provenancePath}" | jq -r '.signatures[0].sig') ` +
        `--bundle "${provenancePath}" "${artifactPath}"`,
        { stdio: 'pipe' }
      );
    } catch (err) {
      throw new Error(`Cosign verification failed: ${err.message}`);
    }

    // 4. Verify against Rego / CEL policy (optional, for custom rules)
    if (this.policyPath) {
      this._verifyPolicy(provenance);
    }

    console.log(`✅ Provenance verified: ${artifactPath}`);
    return true;
  }

  _sha256(filePath) {
    const hash = crypto.createHash('sha256');
    hash.update(fs.readFileSync(filePath));
    return hash.digest('hex');
  }

  _verifyPolicy(provenance) {
    // OPA/Rego policy: e.g. source must match whitelisted repos
    const { execSync } = require('child_process');
    const result = execSync(
      `opa eval --input <(echo '${JSON.stringify(provenance)}') --data "${this.policyPath}" ` +
      `'data.slsa.allow'`,
      { shell: '/bin/bash', encoding: 'utf8' }
    );
    if (!result.includes('true')) {
      throw new Error('Provenance failed policy check');
    }
  }
}

// ── Rego policy (policy.rego) ─────────────────────────────────
// package slsa
// allowed_repos := {"github.com/myorg/frontend", "github.com/myorg/api"}
// allow { input.predicate.materials[0].uri == allowed_repos[_] }

module.exports = ProvenanceVerifier;
```

### 1.3 Software Bill of Materials (SBOM)

An SBOM is a machine-readable inventory of every component in your software. It is the **input** to vulnerability scanning, not the output.

#### 1.3.1 SBOM Standards

| Standard | Ecosystem | Format |
|----------|-----------|--------|
| **SPDX** 2.3+ | Linux Foundation; best for license compliance | JSON, YAML, tag-value |
| **CycloneDX** 1.5+ | OWASP; best for vulnerability analysis | JSON, XML |
| **SWID** | ISO/IEC 19770-2; government compliance | XML |

#### 1.3.2 Generating SBOMs in CI/CD

```yaml
# .github/workflows/sbom.yml
name: SBOM Generation
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'     # Weekly Monday 6AM

jobs:
  generate-sbom:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      # ── Node.js (CycloneDX) ──────────────────────────────
      - name: Generate CycloneDX SBOM (Node)
        uses: CycloneDX/gh-node-module-generatebom@v2
        with:
          path: './'
          output: 'sbom.cyclonedx.json'

      # ── Docker image (Syft) ──────────────────────────────
      - name: Generate SBOM for container image
        uses: anchore/sbom-action@v0
        with:
          image: 'ghcr.io/myorg/app:latest'
          format: 'spdx-json'
          output-file: 'sbom.spdx.json'

      # ── Upload SBOMs as release artifacts ────────────────
      - name: Upload SBOMs
        uses: actions/upload-artifact@v4
        with:
          name: sboms
          path: |
            sbom.cyclonedx.json
            sbom.spdx.json
```

#### 1.3.3 SBOM Ingestion & Vulnerability Correlation

```javascript
// sbom-scanner.js — Ingest SBOM, cross-reference with vulnerability databases
const fs = require('fs');

class SbomScanner {
  constructor({ grypePath = 'grype', osvDevApiKey = null } = {}) {
    this.grypePath = grypePath;
    this.osvDevApiKey = osvDevApiKey;
  }

  /** Scan a CycloneDX SBOM with Grype */
  scanSbom(sbomPath) {
    const { execSync } = require('child_process');
    try {
      const result = execSync(
        `${this.grypePath} sbom:"${sbomPath}" --output json --fail-on high`,
        { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
      );
      const findings = JSON.parse(result);
      return this._categorizeFindings(findings);
    } catch (err) {
      // Grype returns non-zero exit on findings; capture output anyway
      if (err.stdout) {
        const findings = JSON.parse(err.stdout);
        return this._categorizeFindings(findings);
      }
      throw err;
    }
  }

  _categorizeFindings(findings) {
    const categorized = {
      critical: [],
      high: [],
      medium: [],
      low: [],
    };

    for (const match of findings.matches || []) {
      const vuln = match.vulnerability;
      const entry = {
        package: match.artifact.name,
        version: match.artifact.version,
        cve: vuln.id,
        severity: vuln.severity,
        description: vuln.description,
        fixAvailable: vuln.fix?.versions?.join(', ') || 'none',
        url: vuln.dataSource || `https://osv.dev/vulnerability/${vuln.id}`,
      };

      switch (vuln.severity?.toLowerCase()) {
        case 'critical': categorized.critical.push(entry); break;
        case 'high':     categorized.high.push(entry);     break;
        case 'medium':   categorized.medium.push(entry);   break;
        default:         categorized.low.push(entry);
      }
    }
    return categorized;
  }

  /** Block deployment if critical CVEs exist */
  gateDeployment(categorizedFindings) {
    if (categorizedFindings.critical.length > 0) {
      console.error(`❌ ${categorizedFindings.critical.length} critical CVEs found — blocking deploy`);
      for (const cve of categorizedFindings.critical) {
        console.error(`  ${cve.cve}: ${cve.package}@${cve.version} — ${cve.description}`);
      }
      process.exit(1);
    }
    if (categorizedFindings.high.length > 0) {
      console.warn(`⚠️  ${categorizedFindings.high.length} high-severity CVEs — review required`);
    }
    console.log('✅ SBOM scan passed deployment gate');
  }
}

// ── CLI Usage ─────────────────────────────────────────────────
// const scanner = new SbomScanner();
// const findings = scanner.scanSbom('./sbom.cyclonedx.json');
// scanner.gateDeployment(findings);

module.exports = SbomScanner;
```

#### 1.3.4 SBOM Attestation & Signing

```bash
# Sign SBOM with Cosign (Sigstore)
cosign sign-blob \
  --key cosign.key \
  --output-signature sbom.cyclonedx.json.sig \
  sbom.cyclonedx.json

# Or keyless (OIDC-based) signing in CI:
cosign sign-blob \
  --identity-token="$GITHUB_OIDC_TOKEN" \
  --output-signature sbom.cyclonedx.json.sig \
  sbom.cyclonedx.json

# Verify SBOM before deployment:
cosign verify-blob \
  --certificate-identity "https://github.com/myorg/app/.github/workflows/sbom.yml@refs/heads/main" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  --signature sbom.cyclonedx.json.sig \
  sbom.cyclonedx.json
```

### 1.4 Dependency Pinning & Verification

```javascript
// verify-deps.js — Verify that node_modules matches lockfile hashes
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class DependencyVerifier {
  constructor(lockfilePath = 'package-lock.json') {
    this.lockfile = JSON.parse(fs.readFileSync(lockfilePath, 'utf8'));
  }

  /** Verify all installed packages match lockfile integrity hashes */
  verify() {
    const violations = [];
    const packages = this.lockfile.packages || {};

    for (const [packageKey, pkg] of Object.entries(packages)) {
      if (packageKey === '') continue; // root package
      if (!pkg.resolved) continue;     // local or workspace package

      const pkgPath = path.join('node_modules', packageKey);
      if (!fs.existsSync(pkgPath)) {
        violations.push({ package: packageKey, issue: 'MISSING' });
        continue;
      }

      // Verify package.json integrity
      const pkgJsonPath = path.join(pkgPath, 'package.json');
      if (pkg.integrity) {
        const actualIntegrity = this._computeSRI(pkgJsonPath);
        if (actualIntegrity !== pkg.integrity) {
          violations.push({
            package: packageKey,
            issue: 'INTEGRITY_MISMATCH',
            expected: pkg.integrity,
            actual: actualIntegrity,
          });
        }
      }
    }

    if (violations.length > 0) {
      console.error(`❌ ${violations.length} dependency integrity violations:`);
      violations.forEach(v => console.error(`  ${v.package}: ${v.issue}`));
      process.exit(1);
    }
    console.log(`✅ All ${Object.keys(packages).length - 1} dependencies verified`);
  }

  _computeSRI(filePath) {
    const content = fs.readFileSync(filePath);
    const hash = crypto.createHash('sha512').update(content).digest('base64');
    return `sha512-${hash}`;
  }
}

module.exports = DependencyVerifier;
```

### 1.5 Supply-Chain Security Checklist

- [ ] Generate CycloneDX or SPDX SBOM for every release
- [ ] Sign SBOM and provenance attestations with Sigstore/Cosign
- [ ] Pin all GitHub Actions to commit hashes (never use `@main` or `@v1` without hash)
- [ ] Use `npm ci` / `pip install --require-hashes` (strict installs)
- [ ] Verify lockfile integrity before every build
- [ ] Run `grype` or `trivy` against SBOM in CI; block on Critical/High
- [ ] Enforce two-person code review on all changes to build pipelines
- [ ] Use ephemeral, isolated build environments (no cache poisoning)
- [ ] Register with vulnerability disclosure programs (VDP) and subscribe to advisories
- [ ] Rotate signing keys annually; revoke compromised keys immediately

---

## 2. Runtime Application Self-Protection (RASP)

### 2.1 What Is RASP?

RASP embeds security instrumentation directly into the application runtime. Unlike a WAF (which sits at the network edge and operates on HTTP traffic), RASP sees inside the application — it can trace SQL queries, deserialization, file I/O, and reflection calls, and block attacks **in-process** with full context.

### 2.2 RASP Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Application                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  Request │→│  RASP    │→│  Business Logic   │  │
│  │  Handler │  │  Hook    │  │                    │  │
│  └──────────┘  └────┬─────┘  └────────┬───────────┘  │
│                     │                 │               │
│              ┌──────▼─────────────────▼──────┐       │
│              │     Instrumentation Engine     │       │
│              │  • SQL query interception      │       │
│              │  • Command execution hooks      │       │
│              │  • File I/O monitoring          │       │
│              │  • Deserialization guards        │       │
│              │  • Reflection API wrapping       │       │
│              └──────┬─────────────────────────┘       │
│                     │                                 │
│              ┌──────▼─────────┐                       │
│              │  Policy Engine  │                      │
│              │  • Block / Log  │                      │
│              │  • Rate Limit    │                      │
│              │  • Alert         │                      │
│              └────────────────┘                       │
└─────────────────────────────────────────────────────┘
```

### 2.3 Node.js RASP Implementation

```javascript
// rasp-engine.js — In-process RASP for Node.js applications
const { AsyncLocalStorage } = require('async_hooks');
const Module = require('module');
const crypto = require('crypto');

class RaspEngine {
  constructor(options = {}) {
    this.blockMode = options.blockMode ?? true;       // block or log-only
    this.monitorSQL = options.monitorSQL ?? true;
    this.monitorCommands = options.monitorCommands ?? true;
    this.monitorFileIO = options.monitorFileIO ?? true;
    this.monitorDeserialize = options.monitorDeserialize ?? true;
    this.sensitivePaths = options.sensitivePaths ?? [
      '/etc/passwd', '/etc/shadow', '.env', '.git/config',
      'id_rsa', 'id_ed25519',
    ];
    this.alertCallback = options.alertCallback || console.error;
    this.stats = { blocked: 0, alerted: 0, passed: 0 };
    this.als = new AsyncLocalStorage();
  }

  // ── Request-scoped context ────────────────────────────
  middleware() {
    const self = this;
    return (req, res, next) => {
      const requestId = crypto.randomUUID();
      self.als.run({ requestId, ip: req.ip, path: req.path }, () => {
        res.setHeader('X-Request-Id', requestId);
        next();
      });
    };
  }

  getContext() {
    return this.als.getStore() || { requestId: 'unknown' };
  }

  // ── SQL Injection Detection ───────────────────────────
  hookDatabase(driver) {
    if (!this.monitorSQL) return driver;

    const self = this;
    const originalQuery = driver.query.bind(driver);

    driver.query = function (sql, params, callback) {
      const ctx = self.getContext();
      const sqlStr = typeof sql === 'string' ? sql : sql.text || '';

      // Pattern-based detection (supplement, not replace, parameterization)
      const sqliPatterns = [
        /(\bUNION\s+(ALL\s+)?SELECT\b)/i,
        /(\bSELECT\b.*\bFROM\b.*--)/i,
        /(';?\s*(DROP|DELETE|UPDATE|INSERT)\s)/i,
        /(\bEXEC\b\s*[\s(]*[xX]?[pP]?_?\w+)/i,  // EXEC xp_cmdshell
        /(\bSLEEP\s*\(\s*\d+\s*\))/i,
        /(\bBENCHMARK\s*\(\s*\d+\s*,)/i,
      ];

      for (const pattern of sqliPatterns) {
        if (pattern.test(sqlStr)) {
          self._alert('SQL_INJECTION', {
            sql: sqlStr.substring(0, 200),
            params,
            pattern: pattern.source,
          }, ctx);
          self.stats.blocked++;
          if (self.blockMode) {
            const err = new Error('Potential SQL injection blocked by RASP');
            err.code = 'RASP_BLOCKED';
            if (callback) return callback(err);
            throw err;
          }
        }
      }

      self.stats.passed++;
      return originalQuery.call(this, sql, params, callback);
    };

    return driver;
  }

  // ── Command Injection Detection ───────────────────────
  hookChildProcess(childProcess) {
    if (!this.monitorCommands) return;

    const self = this;
    const originalSpawn = childProcess.spawn;
    const originalExec = childProcess.exec;

    childProcess.spawn = function (command, args, options) {
      const ctx = self.getContext();
      const cmdStr = `${command} ${(args || []).join(' ')}`;

      // Block known-dangerous patterns
      const dangerous = [
        /[;&|`$]/,          // command chaining
        /\$\(/,             // command substitution
        /\/dev\/tcp/,       // reverse shell
        /nc\s+\S+\s+\d+/,   // netcat
        /curl.*\|\s*(ba)?sh/,  // curl pipe shell
        /wget.*-O.*\|\s*(ba)?sh/,
        /\/bin\/(ba)?sh\s+-c/,
      ];

      for (const pattern of dangerous) {
        if (pattern.test(cmdStr)) {
          self._alert('COMMAND_INJECTION', {
            command: cmdStr.substring(0, 200),
            pattern: pattern.source,
          }, ctx);
          self.stats.blocked++;
          if (self.blockMode) {
            const err = new Error('Command injection blocked by RASP');
            err.code = 'RASP_BLOCKED';
            throw err;
          }
        }
      }

      return originalSpawn.call(this, command, args, options);
    };

    childProcess.exec = function (command, options, callback) {
      const ctx = self.getContext();
      self._alert('COMMAND_EXEC', {
        command: command.substring(0, 200),
      }, ctx);
      // Always log exec() — it's inherently risky
      self.stats.alerted++;
      return originalExec.call(this, command, options, callback);
    };
  }

  // ── Path Traversal Detection ──────────────────────────
  hookFileSystem(fs) {
    if (!this.monitorFileIO) return;

    const self = this;
    const methods = ['readFile', 'writeFile', 'createReadStream', 'createWriteStream',
                     'open', 'readFileSync', 'writeFileSync', 'openSync', 'accessSync'];

    for (const method of methods) {
      const original = fs[method];
      if (typeof original !== 'function') continue;

      fs[method] = function (filePath, ...args) {
        const ctx = self.getContext();
        const resolved = require('path').resolve(String(filePath));

        // Detect path traversal attempts
        if (resolved.includes('..')) {
          self._alert('PATH_TRAVERSAL', {
            path: String(filePath).substring(0, 200),
            resolved: resolved.substring(0, 200),
          }, ctx);
          self.stats.blocked++;
          if (self.blockMode) {
            const err = new Error('Path traversal blocked by RASP');
            err.code = 'RASP_BLOCKED';
            // For callback-based methods, invoke callback with error
            const cb = args.find(a => typeof a === 'function');
            if (cb) return cb(err);
            throw err;
          }
        }

        // Detect sensitive file access
        for (const sensitive of self.sensitivePaths) {
          if (resolved.includes(sensitive)) {
            self._alert('SENSITIVE_FILE_ACCESS', {
              path: String(filePath).substring(0, 200),
              sensitive,
            }, ctx);
            break;
          }
        }

        return original.call(this, filePath, ...args);
      };
    }
  }

  // ── Deserialization Attack Detection ──────────────────
  hookDeserialization() {
    if (!this.monitorDeserialize) return;

    const self = this;
    const { deserialize } = require('v8');
    const originalParse = JSON.parse;

    // Monitor JSON.parse for excessively large or deeply nested payloads
    JSON.parse = function (text, reviver) {
      const ctx = self.getContext();

      if (text.length > 1_000_000) {  // 1MB JSON — suspicious
        self._alert('LARGE_JSON_PAYLOAD', {
          size: text.length,
        }, ctx);
      }

      // Detect prototype pollution patterns
      if (typeof text === 'string' && /"__proto__"\s*:/i.test(text)) {
        self._alert('PROTOTYPE_POLLUTION', {
          snippet: text.substring(0, 100),
        }, ctx);
        self.stats.blocked++;
        if (self.blockMode) {
          throw new Error('Prototype pollution attempt blocked by RASP');
        }
      }

      return originalParse.call(this, text, reviver);
    };
  }

  // ── Alerting ───────────────────────────────────────────
  _alert(type, payload, ctx = {}) {
    const alert = {
      timestamp: new Date().toISOString(),
      type,
      requestId: ctx.requestId || 'unknown',
      ip: ctx.ip || 'unknown',
      path: ctx.path || 'unknown',
      payload,
      blocked: this.blockMode,
    };
    this.alertCallback(alert);
  }

  /** Enable all hooks */
  enable() {
    this.hookChildProcess(require('child_process'));
    this.hookFileSystem(require('fs'));
    this.hookDeserialization();
    console.log('🛡️  RASP Engine enabled');
    return this;
  }

  /** Get current statistics */
  stats() {
    return { ...this.stats };
  }
}

// ── Express Integration ────────────────────────────────────
// const rasp = new RaspEngine({
//   blockMode: process.env.NODE_ENV === 'production',
//   alertCallback: (alert) => {
//     console.error('[RASP]', JSON.stringify(alert));
//     // Also ship to your SIEM / alerting pipeline
//   },
// });
// rasp.enable();
// app.use(rasp.middleware());
//
// // Hook database driver
// const pg = require('pg');
// const pool = new pg.Pool({...});
// rasp.hookDatabase(pool);

module.exports = RaspEngine;
```

### 2.4 Java RASP — Key Instrumentation Points

```java
// RaspAgent.java — Java agent-based RASP (premain)
// Add to JVM: -javaagent:rasp-agent.jar
import java.lang.instrument.Instrumentation;
import net.bytebuddy.agent.builder.AgentBuilder;
import net.bytebuddy.asm.Advice;
import static net.bytebuddy.matcher.ElementMatchers.*;

public class RaspAgent {
    public static void premain(String args, Instrumentation inst) {
        new AgentBuilder.Default()
            // Intercept SQL execution
            .type(named("java.sql.Statement"))
            .transform((builder, type, classLoader, module, domain) ->
                builder.visit(Advice.to(SqlInterceptor.class)
                    .on(named("executeQuery").or(named("execute").or(named("executeUpdate"))))
                )
            )
            // Intercept Runtime.exec()
            .type(named("java.lang.Runtime"))
            .transform((builder, type, classLoader, module, domain) ->
                builder.visit(Advice.to(CommandInterceptor.class)
                    .on(named("exec"))
                )
            )
            // Intercept Runtime.exec() via ProcessBuilder
            .type(named("java.lang.ProcessBuilder"))
            .transform((builder, type, classLoader, module, domain) ->
                builder.visit(Advice.to(ProcessBuilderInterceptor.class)
                    .on(named("start"))
                )
            )
            // Intercept deserialization
            .type(named("java.io.ObjectInputStream"))
            .transform((builder, type, classLoader, module, domain) ->
                builder.visit(Advice.to(DeserializationInterceptor.class)
                    .on(named("resolveClass"))
                )
            )
            .installOn(inst);
    }
}

class SqlInterceptor {
    @Advice.OnMethodEnter
    public static void onEnter(@Advice.Argument(0) String sql) {
        if (sql != null && RaspPolicy.isBlocked(sql)) {
            throw new SecurityException("SQL blocked by RASP: " + RaspPolicy.reason(sql));
        }
    }
}

class CommandInterceptor {
    @Advice.OnMethodEnter
    public static void onEnter(@Advice.Argument(0) String command) {
        if (RaspPolicy.containsDangerousChars(command)) {
            throw new SecurityException("Command exec blocked by RASP");
        }
    }
}

class DeserializationInterceptor {
    @Advice.OnMethodEnter
    public static void onEnter(@Advice.Argument(0) java.io.ObjectStreamClass desc) {
        if (RaspPolicy.isDangerousGadget(desc.getName())) {
            throw new SecurityException("Dangerous deserialization blocked: " + desc.getName());
        }
    }
}
```

### 2.5 RASP Deployment Checklist

- [ ] Deploy RASP in **monitor-only mode** first (1-2 weeks) to establish baseline
- [ ] Tune false-positive sensitivity before enabling block mode
- [ ] Integrate RASP alerts with your SIEM/SOAR pipeline
- [ ] Hook all data-access layers (database drivers, ORM query builders)
- [ ] Hook `child_process` and `fs` modules; add whitelist for legitimate usage
- [ ] Monitor deserialization entry points (JSON.parse, `ObjectInputStream`, `pickle.loads`)
- [ ] Add health-check endpoint that reports RASP status and block stats
- [ ] Test RASP coverage with automated attack simulation (OWASP ZAP, sqlmap in safe mode)
- [ ] Performance-budget: acceptable overhead < 3% p99 latency increase

---

## 3. API Abuse Detection with Machine Learning

### 3.1 Problem Statement

Traditional rate limiting (fixed-window, token bucket) catches naive scraping but misses sophisticated abuse: credential stuffing with distributed IPs, slow data exfiltration, account enumeration with jittered timing, and business-logic abuse that stays *within* rate limits. ML-based detection analyzes behavioral patterns across multiple dimensions.

### 3.2 Feature Engineering for API Abuse

```javascript
// feature-extractor.js — Extract behavioral features from API request stream
class ApiFeatureExtractor {
  constructor() {
    this.sessions = new Map();  // sessionId → feature buffer
    this.windowMs = 300_000;    // 5-minute sliding window
    this.cleanupInterval = null;
  }

  start() {
    this.cleanupInterval = setInterval(() => this._cleanup(), 60_000);
  }

  /** Extract a feature vector from a single request */
  extract(sessionId, req) {
    const now = Date.now();
    let session = this.sessions.get(sessionId);

    if (!session) {
      session = {
        sessionId,
        createdAt: now,
        requests: [],
        endpoints: new Map(),
        userAgents: new Set(),
        ips: new Set(),
        statusCodes: new Map(),
        errorCount: 0,
        payloadSizes: [],
        timeDeltas: [],
        firstTimestamp: now,
      };
      this.sessions.set(sessionId, session);
    }

    const timeDelta = session.requests.length > 0
      ? now - session.requests[session.requests.length - 1].timestamp
      : 0;

    session.requests.push({
      timestamp: now,
      endpoint: req.path,
      method: req.method,
      statusCode: 200,  // filled after response
      payloadSize: JSON.stringify(req.body || '').length,
    });

    // Track endpoint frequency
    const endpointKey = `${req.method}:${req.path}`;
    session.endpoints.set(endpointKey, (session.endpoints.get(endpointKey) || 0) + 1);

    if (req.headers['user-agent']) session.userAgents.add(req.headers['user-agent']);
    session.ips.add(req.ip);
    if (timeDelta > 0) session.timeDeltas.push(timeDelta);
    session.payloadSizes.push(JSON.stringify(req.body || '').length);

    // Prune old requests outside window
    session.requests = session.requests.filter(r => now - r.timestamp < this.windowMs);

    return this._computeFeatures(session);
  }

  /** After response: update status code */
  updateResponse(sessionId, statusCode) {
    const session = this.sessions.get(sessionId);
    if (!session) return;
    session.statusCodes.set(statusCode, (session.statusCodes.get(statusCode) || 0) + 1);
    if (statusCode >= 400) session.errorCount++;
    if (session.requests.length > 0) {
      session.requests[session.requests.length - 1].statusCode = statusCode;
    }
  }

  /** Compute the 30+ dimensional feature vector */
  _computeFeatures(session) {
    const now = Date.now();
    const windowRequests = session.requests;
    const windowDuration = now - session.firstTimestamp;
    const count = windowRequests.length;

    // ── Rate features ──────────────────────────
    const rpm = count / Math.max(windowDuration / 60000, 0.001);

    // ── Entropy features ───────────────────────
    const endpointEntropy = this._entropy(Array.from(session.endpoints.values()));
    const uniqueEndpoints = session.endpoints.size;
    const uniqueUserAgents = session.userAgents.size;
    const uniqueIps = session.ips.size;

    // ── Timing features ────────────────────────
    const timeStats = this._stats(session.timeDeltas);
    const jitter = timeStats.stdDev / Math.max(timeStats.mean, 0.001); // CV of inter-request time

    // ── Payload features ──────────────────────
    const payloadStats = this._stats(session.payloadSizes);
    const totalPayload = session.payloadSizes.reduce((a, b) => a + b, 0);

    // ── Error rate ────────────────────────────
    const errorRate = count > 0 ? session.errorCount / count : 0;

    // ── Burst features ────────────────────────
    const burstRatio = this._burstRatio(session.requests);

    // ── Sequential scanning ───────────────────
    const sequentialPattern = this._detectSequentialEndpoints(session.requests);

    return {
      // Rate
      request_count: count,
      requests_per_minute: rpm,
      unique_endpoints: uniqueEndpoints,
      unique_user_agents: uniqueUserAgents,
      unique_ips: uniqueIps,

      // Entropy / diversity
      endpoint_entropy: endpointEntropy,
      endpoint_diversity: uniqueEndpoints / Math.max(count, 1),

      // Timing
      mean_inter_request_ms: timeStats.mean,
      stddev_inter_request_ms: timeStats.stdDev,
      timing_jitter_cv: jitter,
      burst_ratio: burstRatio,

      // Payload
      mean_payload_size: payloadStats.mean,
      max_payload_size: payloadStats.max,
      total_payload: totalPayload,

      // Errors
      error_rate: errorRate,
      status_4xx_rate: (session.statusCodes.get(400) + session.statusCodes.get(401) +
                        session.statusCodes.get(403) + session.statusCodes.get(404) || 0) / Math.max(count, 1),
      status_5xx_rate: (session.statusCodes.get(500) + session.statusCodes.get(502) +
                        session.statusCodes.get(503) || 0) / Math.max(count, 1),

      // Abuse indicators
      sequential_endpoint_pattern: sequentialPattern,
      session_age_ms: now - session.createdAt,
    };
  }

  _entropy(values) {
    const total = values.reduce((a, b) => a + b, 0);
    if (total === 0) return 0;
    let entropy = 0;
    for (const v of values) {
      const p = v / total;
      if (p > 0) entropy -= p * Math.log2(p);
    }
    return entropy;
  }

  _stats(arr) {
    if (arr.length === 0) return { mean: 0, stdDev: 0, max: 0, min: 0 };
    const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
    const variance = arr.reduce((a, b) => a + (b - mean) ** 2, 0) / arr.length;
    return {
      mean,
      stdDev: Math.sqrt(variance),
      max: Math.max(...arr),
      min: Math.min(...arr),
    };
  }

  _burstRatio(requests) {
    if (requests.length < 3) return 0;
    // Count requests that occur within 1 second of each other
    let burstCount = 0;
    for (let i = 1; i < requests.length; i++) {
      if (requests[i].timestamp - requests[i - 1].timestamp < 1000) burstCount++;
    }
    return burstCount / requests.length;
  }

  _detectSequentialEndpoints(requests) {
    // Detect sequential ID enumeration: /users/1, /users/2, /users/3...
    const patterns = [];
    const seqRegex = /\/\d+$/;
    let consecutive = 0;

    for (let i = 1; i < requests.length; i++) {
      const prevPath = requests[i - 1].endpoint;
      const currPath = requests[i].endpoint;
      const prevMatch = prevPath.match(seqRegex);
      const currMatch = currPath.match(seqRegex);

      if (prevMatch && currMatch && prevPath.replace(seqRegex, '') === currPath.replace(seqRegex, '')) {
        const prevId = parseInt(prevMatch[0].slice(1));
        const currId = parseInt(currMatch[0].slice(1));
        if (currId === prevId + 1) {
          consecutive++;
        }
      }
    }

    return consecutive;
  }

  _cleanup() {
    const now = Date.now();
    for (const [key, session] of this.sessions) {
      if (now - session.createdAt > this.windowMs * 2) {
        this.sessions.delete(key);
      }
    }
  }
}

module.exports = ApiFeatureExtractor;
```

### 3.3 Anomaly Detection Model — Isolation Forest

```python
# api_abuse_model.py — Train and serve an Isolation Forest for API abuse detection
import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

FEATURE_NAMES = [
    'request_count', 'requests_per_minute', 'unique_endpoints',
    'endpoint_entropy', 'endpoint_diversity',
    'mean_inter_request_ms', 'stddev_inter_request_ms', 'timing_jitter_cv',
    'burst_ratio',
    'mean_payload_size', 'max_payload_size', 'total_payload',
    'error_rate', 'status_4xx_rate', 'status_5xx_rate',
    'sequential_endpoint_pattern', 'session_age_ms',
]

class ApiAbuseDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=200,
            contamination=0.05,          # Expect ~5% of traffic to be anomalous
            max_samples='auto',
            random_state=42,
            n_jobs=-1,
        )
        self.fitted = False
        if model_path:
            self.load(model_path)

    def train(self, feature_vectors: List[Dict], labels: Optional[List[int]] = None):
        """Train on historical feature vectors. Labels optional (unsupervised)."""
        X = self._dicts_to_matrix(feature_vectors)
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.fitted = True

        # Compute anomaly score thresholds from training data
        scores = self.model.decision_function(X_scaled)
        self.threshold_high = np.percentile(scores, 1)   # bottom 1% = high anomaly
        self.threshold_low  = np.percentile(scores, 5)   # bottom 5% = low anomaly

        return self

    def predict(self, feature_dict: Dict) -> Dict:
        """Returns anomaly prediction with score and reasoning."""
        if not self.fitted:
            raise RuntimeError('Model not fitted')

        X = self._dicts_to_matrix([feature_dict])
        X_scaled = self.scaler.transform(X)
        score = float(self.model.decision_function(X_scaled)[0])
        prediction = int(self.model.predict(X_scaled)[0])  # 1 = normal, -1 = anomaly

        # Determine severity
        if score < self.threshold_high:
            severity = 'high'
            action = 'block'
        elif score < self.threshold_low:
            severity = 'medium'
            action = 'challenge'  # e.g., require CAPTCHA
        elif prediction == -1:
            severity = 'low'
            action = 'log'
        else:
            severity = 'normal'
            action = 'allow'

        # Explain which features contributed to anomaly
        feature_contributions = self._explain_anomaly(feature_dict, X_scaled[0])

        return {
            'is_anomaly': prediction == -1,
            'anomaly_score': score,
            'severity': severity,
            'action': action,
            'top_contributors': feature_contributions,
        }

    def _dicts_to_matrix(self, feature_dicts: List[Dict]) -> np.ndarray:
        rows = []
        for fd in feature_dicts:
            rows.append([float(fd.get(name, 0)) for name in FEATURE_NAMES])
        return np.array(rows)

    def _explain_anomaly(self, feature_dict: Dict, scaled_row: np.ndarray) -> List[Dict]:
        """Identify which features deviate most from the training distribution."""
        contributions = []
        for i, name in enumerate(FEATURE_NAMES):
            mean_val = self.scaler.mean_[i]
            std_val = self.scaler.scale_[i] if self.scaler.scale_[i] > 0 else 1
            deviation = abs(scaled_row[i])  # how many std devs from mean
            if deviation > 1.5:  # >1.5σ from mean
                contributions.append({
                    'feature': name,
                    'value': feature_dict.get(name, 0),
                    'z_score': float(deviation),
                })
        contributions.sort(key=lambda x: x['z_score'], reverse=True)
        return contributions[:5]  # top 5 contributors

    def save(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'model': self.model,
                'fitted': self.fitted,
                'threshold_high': self.threshold_high,
                'threshold_low': self.threshold_low,
            }, f)

    def load(self, path: str):
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.scaler = data['scaler']
        self.model = data['model']
        self.fitted = data['fitted']
        self.threshold_high = data.get('threshold_high', -0.5)
        self.threshold_low = data.get('threshold_low', -0.3)
        return self

# ── Training Script ──────────────────────────────────────────
# with open('training_features.jsonl') as f:
#     features = [json.loads(line) for line in f]
# detector = ApiAbuseDetector()
# detector.train(features)
# detector.save('models/api_abuse_model.pkl')
```

### 3.4 Real-Time Inference Middleware

```javascript
// abuse-detection-middleware.js — Real-time ML inference on every API request
const { spawn } = require('child_process');
const path = require('path');
const ApiFeatureExtractor = require('./feature-extractor');

class AbuseDetectionMiddleware {
  constructor({ modelPath, blockThreshold = 'high', pythonPath = 'python3' } = {}) {
    this.modelPath = modelPath;
    this.blockThreshold = blockThreshold;
    this.pythonPath = pythonPath;
    this.extractor = new ApiFeatureExtractor();
    this.cache = new Map();  // sessionId → last prediction (TTL: 10s)

    this.extractor.start();
  }

  middleware() {
    const self = this;
    return async (req, res, next) => {
      const sessionId = req.user?.id || req.ip || 'anonymous';
      const features = self.extractor.extract(sessionId, req);

      // Check cache to avoid redundant predictions
      const cached = self.cache.get(sessionId);
      if (cached && Date.now() - cached.timestamp < 10_000) {
        if (cached.action === 'block') {
          return res.status(429).json({
            error: 'Request blocked by abuse detection',
            retryAfter: 60,
          });
        }
        // Update response tracker
        res.on('finish', () => self.extractor.updateResponse(sessionId, res.statusCode));
        return next();
      }

      // Only run ML on enough data
      if (features.request_count < 5) {
        res.on('finish', () => self.extractor.updateResponse(sessionId, res.statusCode));
        return next();
      }

      try {
        const result = await self._predictPython(features);

        self.cache.set(sessionId, {
          ...result,
          timestamp: Date.now(),
        });

        if (result.action === 'block') {
          console.warn('[ABUSE] Blocked session:', sessionId, result.top_contributors);
          return res.status(429).json({
            error: 'Suspicious activity detected',
            retryAfter: 60,
          });
        }

        if (result.action === 'challenge') {
          // Inject CAPTCHA requirement header
          res.setHeader('X-Challenge-Required', 'true');
        }
      } catch (err) {
        // Fail open if model is unavailable — log but don't block
        console.error('[ABUSE] Model inference failed:', err.message);
      }

      res.on('finish', () => self.extractor.updateResponse(sessionId, res.statusCode));
      next();
    };
  }

  /** Call Python model process for inference */
  _predictPython(features) {
    return new Promise((resolve, reject) => {
      const proc = spawn(this.pythonPath, [
        path.join(__dirname, 'predict_abuse.py'),
        '--model', this.modelPath,
        '--features', JSON.stringify(features),
      ], { stdio: ['pipe', 'pipe', 'pipe'] });

      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', d => stdout += d);
      proc.stderr.on('data', d => stderr += d);

      proc.on('close', code => {
        if (code !== 0) return reject(new Error(stderr));
        try {
          resolve(JSON.parse(stdout));
        } catch (e) {
          reject(new Error(`Parse error: ${stdout}`));
        }
      });

      proc.on('error', reject);
    });
  }
}

// Python inference script: predict_abuse.py
// import json, sys, argparse
// from api_abuse_model import ApiAbuseDetector
// parser = argparse.ArgumentParser()
// parser.add_argument('--model', required=True)
// parser.add_argument('--features', required=True)
// args = parser.parse_args()
// detector = ApiAbuseDetector(args.model)
// features = json.loads(args.features)
// result = detector.predict(features)
// print(json.dumps(result))

module.exports = AbuseDetectionMiddleware;
```

### 3.5 ML Abuse Detection Checklist

- [ ] Collect and label training data: 2+ weeks of real traffic with known abuse labels
- [ ] Feature-engineer 20+ dimensions: rate, entropy, timing, payload, error patterns
- [ ] Train Isolation Forest (unsupervised) or XGBoost (supervised if you have labels)
- [ ] Deploy in **shadow mode** first: predict but don't block; compare against manual review
- [ ] Calibrate contamination rate (start at 0.05, tune based on false-positive rate)
- [ ] Add per-endpoint sensitivity: authentication endpoints need stricter detection
- [ ] Implement graduated response: log → CAPTCHA → 429 rate limit → block
- [ ] Monitor model drift: retrain weekly or when alert rate deviates >20% from baseline
- [ ] Keep model inference < 10ms; use caching for repeat requests within TTL
- [ ] Integrate feature extractor with existing logging pipeline for continuous data collection

---

## 4. Subresource Integrity Automation

### 4.1 What Is SRI?

Subresource Integrity (SRI) allows browsers to verify that third-party assets (scripts, stylesheets) haven't been tampered with. The `integrity` attribute contains a cryptographic hash; if the fetched resource doesn't match, the browser refuses to execute it.

### 4.2 Why Automate?

Manually updating SRI hashes across hundreds of pages every time a CDN library updates is error-prone. Outdated hashes cause silent breakage; missing hashes leave supply-chain gaps. Automation ensures every third-party asset is pinned and verified on every deploy.

### 4.3 SRI Hash Generator & Injector

```javascript
// sri-automation.js — Automated SRI hash generation for static HTML
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { JSDOM } = require('jsdom');

class SriAutomator {
  constructor({ cacheFile = '.sri-cache.json', algorithms = ['sha384'] } = {}) {
    this.cacheFile = cacheFile;
    this.algorithms = algorithms;
    this.cache = this._loadCache();
    this.fetchedHashes = new Map();
  }

  // ── Generate SRI hash for a remote resource ────────────
  async generateIntegrity(url) {
    // Check cache first
    const cached = this.cache[url];
    if (cached && Date.now() - cached.timestamp < 86400_000) {
      return cached.integrity;
    }

    // Fetch resource
    let content;
    try {
      const response = await fetch(url, { timeout: 10_000 });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      content = await response.arrayBuffer();
    } catch (err) {
      console.error(`Failed to fetch ${url}: ${err.message}`);
      return null;
    }

    const buffer = Buffer.from(content);
    const hashes = this.algorithms.map(algo => {
      const hash = crypto.createHash(algo).update(buffer).digest('base64');
      return `${algo}-${hash}`;
    });

    const integrity = hashes.join(' ');
    this.cache[url] = { integrity, timestamp: Date.now(), size: buffer.length };
    this._saveCache();

    return integrity;
  }

  // ── Inject SRI into HTML file ──────────────────────────
  async injectSriInHtml(htmlPath) {
    const html = fs.readFileSync(htmlPath, 'utf8');
    const dom = new JSDOM(html);
    const document = dom.window.document;

    // Process <script> tags with external src
    const scripts = document.querySelectorAll('script[src]');
    for (const script of scripts) {
      const src = script.getAttribute('src');
      if (!src || src.startsWith('/') || src.startsWith('data:')) continue;
      if (script.hasAttribute('integrity')) continue;  // already has SRI

      const integrity = await this.generateIntegrity(src);
      if (integrity) {
        script.setAttribute('integrity', integrity);
        script.setAttribute('crossorigin', 'anonymous');
        console.log(`  ✅ SRI: ${src}`);
      }
    }

    // Process <link rel="stylesheet"> with external href
    const links = document.querySelectorAll('link[rel="stylesheet"][href]');
    for (const link of links) {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('/') || href.startsWith('data:')) continue;
      if (link.hasAttribute('integrity')) continue;

      const integrity = await this.generateIntegrity(href);
      if (integrity) {
        link.setAttribute('integrity', integrity);
        link.setAttribute('crossorigin', 'anonymous');
        console.log(`  ✅ SRI: ${href}`);
      }
    }

    // Write back
    fs.writeFileSync(htmlPath, dom.serialize());
    return htmlPath;
  }

  // ── Scan directory for HTML files and inject SRI ───────
  async injectAllInDirectory(dirPath) {
    const files = this._findHtmlFiles(dirPath);
    console.log(`Found ${files.length} HTML files in ${dirPath}`);

    for (const file of files) {
      console.log(`Processing: ${file}`);
      await this.injectSriInHtml(file);
    }
  }

  // ── Verify all SRIs in an HTML file ────────────────────
  async verifySri(htmlPath, { failOnMissing = true } = {}) {
    const html = fs.readFileSync(htmlPath, 'utf8');
    const dom = new JSDOM(html);
    const document = dom.window.document;
    const results = { passed: [], failed: [], missing: [] };

    const elements = [
      ...document.querySelectorAll('script[src][integrity]'),
      ...document.querySelectorAll('link[rel="stylesheet"][href][integrity]'),
    ];

    for (const el of elements) {
      const url = el.getAttribute('src') || el.getAttribute('href');
      const expectedIntegrity = el.getAttribute('integrity');

      if (!url.startsWith('http')) continue;

      const actualIntegrity = await this.generateIntegrity(url);
      if (!actualIntegrity) {
        results.missing.push({ url, expected: expectedIntegrity });
        continue;
      }

      if (actualIntegrity === expectedIntegrity) {
        results.passed.push({ url, integrity: actualIntegrity });
      } else {
        results.failed.push({
          url,
          expected: expectedIntegrity,
          actual: actualIntegrity,
        });
      }
    }

    return results;
  }

  // ── Cache management ───────────────────────────────────
  _loadCache() {
    try {
      return JSON.parse(fs.readFileSync(this.cacheFile, 'utf8'));
    } catch {
      return {};
    }
  }

  _saveCache() {
    fs.writeFileSync(this.cacheFile, JSON.stringify(this.cache, null, 2));
  }

  _findHtmlFiles(dirPath) {
    const results = [];
    function walk(dir) {
      for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory() && !entry.name.startsWith('.') && entry.name !== 'node_modules') {
          walk(fullPath);
        } else if (entry.isFile() && /\.(html|htm|svelte|vue|jsx|tsx)$/.test(entry.name)) {
          results.push(fullPath);
        }
      }
    }
    walk(dirPath);
    return results;
  }
}

// ── CLI Usage ────────────────────────────────────────────────
// const automator = new SriAutomator();
// await automator.injectAllInDirectory('./dist');
// const results = await automator.verifySri('./dist/index.html');
// console.log(results);

module.exports = SriAutomator;
```

### 4.4 SRI in CI/CD Pipeline

```yaml
# .github/workflows/sri-check.yml
name: SRI Integrity Check
on:
  pull_request:
    paths:
      - '**.html'
      - '**.svelte'
      - '**.vue'
      - '**.jsx'
      - '**.tsx'

jobs:
  sri-verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11

      - uses: actions/setup-node@60edb5dd545a775178f52524783378180af0d1f8
        with:
          node-version: 22

      - run: npm ci

      - name: Verify SRI integrity
        run: |
          node scripts/sri-verify.js --dir ./dist --fail-on-missing --fail-on-mismatch
        # Fails CI if any <script> or <link> is missing or has wrong SRI hash
```

### 4.5 Webpack / Vite Plugin for SRI

```javascript
// vite-plugin-sri.js — Vite plugin to auto-inject SRI at build time
import crypto from 'crypto';
import fs from 'fs';

export function viteSRI(options = {}) {
  const {
    algorithms = ['sha384'],
    include = /\.(js|css)$/,
    exclude = /\.map$/,
    crossorigin = 'anonymous',
  } = options;

  return {
    name: 'vite-plugin-sri',
    enforce: 'post',

    generateBundle(_, bundle) {
      for (const [fileName, chunk] of Object.entries(bundle)) {
        if (chunk.type !== 'chunk' && chunk.type !== 'asset') continue;
        if (exclude && exclude.test(fileName)) continue;
        if (include && !include.test(fileName)) continue;

        const content = chunk.type === 'chunk' ? chunk.code : chunk.source;
        const source = typeof content === 'string' ? content : Buffer.from(content);

        const hashes = algorithms.map(algo => {
          const hash = crypto.createHash(algo).update(source).digest('base64');
          return `${algo}-${hash}`;
        });
        chunk.integrity = hashes.join(' ');
      }
    },

    transformIndexHtml(html) {
      // Inject crossorigin attribute on script/link tags that have integrity
      // Vite's manifest handles the actual integrity attribute injection
      return html;
    },
  };
}
```

### 4.6 SRI for Dynamic CDN Loads (Script Tag Builder)

```javascript
// safe-cdn-loader.js — Dynamically create <script> tags with known SRI hashes
const KNOWN_CDN_HASHES = {
  'react@18.3.1': {
    url: 'https://unpkg.com/react@18.3.1/umd/react.production.min.js',
    integrity: 'sha384-...',
  },
  'lodash@4.17.21': {
    url: 'https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js',
    integrity: 'sha384-...',
  },
  'alpinejs@3.13.5': {
    url: 'https://cdn.jsdelivr.net/npm/alpinejs@3.13.5/dist/cdn.min.js',
    integrity: 'sha384-...',
  },
};

class SafeCdnLoader {
  /** Load a script with SRI, only if not already loaded */
  static load(packageId) {
    const entry = KNOWN_CDN_HASHES[packageId];
    if (!entry) throw new Error(`No SRI hash registered for: ${packageId}`);

    // Check if already loaded
    const existing = document.querySelector(`script[src="${entry.url}"]`);
    if (existing) return Promise.resolve();

    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = entry.url;
      script.integrity = entry.integrity;
      script.crossOrigin = 'anonymous';
      script.async = true;

      script.onload = () => resolve();
      script.onerror = () => {
        // SRI mismatch — resource tampered or CDN changed content
        reject(new Error(`SRI verification failed for ${packageId}`));
        script.remove();
      };

      document.head.appendChild(script);
    });
  }

  /** Register a new CDN resource with its verified SRI hash */
  static register(packageId, url, integrity) {
    KNOWN_CDN_HASHES[packageId] = { url, integrity };
  }
}

module.exports = SafeCdnLoader;
```

### 4.7 SRI Checklist

- [ ] Every third-party `<script>` and `<link>` has an `integrity` attribute
- [ ] Every integrity-bearing element has `crossorigin="anonymous"`
- [ ] CI pipeline fails on missing or stale SRI hashes
- [ ] SRI cache is version-controlled and reviewed after dependency updates
- [ ] CDN resources are verified against at least SHA-384 (SHA-256 is acceptable; SHA-512 preferred)
- [ ] Dynamic script loaders use SRI (don't create elements without it)
- [ ] Monitor CSP violation reports for SRI-blocked resources (indicates CDN compromise or stale hash)
- [ ] Bundle analyzer validates SRI for lazily-loaded chunks

---

## 5. Real-Time Threat Feed Integration

### 5.1 Architecture Overview

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  AlienVault  │    │  AbuseIPDB   │    │  CrowdSec    │
│     OTX      │    │              │    │     CTI      │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │ (poll / webhook)
                  ┌────────▼────────┐
                  │  Threat Feed    │
                  │   Aggregator    │
                  │                 │
                  │ • Dedup & merge │
                  │ • Expire stale  │
                  │ • Score compute │
                  └────────┬────────┘
                           │
                  ┌────────▼────────┐
                  │  In-Memory      │
                  │  Reputation DB  │
                  │  (Redis/Node)   │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼──┐  ┌─────▼─────┐  ┌───▼──────┐
       │ WAF/RASP│  │ API Gateway│  │ Auth     │
       │  Block  │  │  Rate Limit│  │ Challenge│
       └─────────┘  └───────────┘  └──────────┘
```

### 5.2 Threat Feed Aggregator

```javascript
// threat-feed-aggregator.js — Aggregate, deduplicate, and score threat intelligence
const EventEmitter = require('events');
const crypto = require('crypto');

class ThreatFeedAggregator extends EventEmitter {
  constructor({ redis, refreshIntervalMs = 300_000 } = {}) {
    super();
    this.redis = redis;
    this.refreshIntervalMs = refreshIntervalMs;
    this.feeds = new Map();
    this.reputationCache = new Map();  // ip/domain → ReputationEntry
    this.refreshTimer = null;
  }

  /** Register a threat feed source */
  registerFeed(name, fetcher, { weight = 1.0, category = 'generic' } = {}) {
    this.feeds.set(name, { fetcher, weight, category });
    return this;
  }

  /** Start periodic refresh */
  start() {
    this._refreshAll();
    this.refreshTimer = setInterval(() => this._refreshAll(), this.refreshIntervalMs);
    console.log(`🔄 Threat feed aggregator started with ${this.feeds.size} feeds`);
  }

  async stop() {
    if (this.refreshTimer) clearInterval(this.refreshTimer);
  }

  /** Check reputation of an IP address */
  checkIp(ip) {
    const entry = this.reputationCache.get(ip);
    if (!entry) return { score: 0, categories: [], sources: [], verdict: 'unknown' };

    const now = Date.now();
    if (now - entry.timestamp > entry.ttlMs) {
      this.reputationCache.delete(ip);
      return { score: 0, categories: [], sources: [], verdict: 'unknown' };
    }

    // Map score to verdict
    let verdict = 'safe';
    if (entry.score >= 0.8) verdict = 'malicious';
    else if (entry.score >= 0.5) verdict = 'suspicious';
    else if (entry.score >= 0.2) verdict = 'low_risk';

    return {
      score: entry.score,
      categories: [...entry.categories],
      sources: [...entry.sources],
      verdict,
      lastSeen: new Date(entry.timestamp).toISOString(),
    };
  }

  // ── Internal ────────────────────────────────────────────
  async _refreshAll() {
    console.log(`[${new Date().toISOString()}] Refreshing threat feeds...`);
    const allEntries = [];

    for (const [name, feed] of this.feeds) {
      try {
        const entries = await feed.fetcher();
        // Weight each entry by feed reliability
        for (const entry of entries) {
          allEntries.push({
            ...entry,
            sourceWeight: feed.weight,
            sourceCategory: feed.category,
            sourceName: name,
          });
        }
        console.log(`  ${name}: ${entries.length} entries`);
      } catch (err) {
        console.error(`  ${name}: FAILED — ${err.message}`);
        this.emit('feed-error', { feed: name, error: err.message });
      }
    }

    // Merge and deduplicate by indicator
    const merged = this._mergeIndicators(allEntries);
    this.reputationCache = merged;

    // Persist to Redis if available
    if (this.redis) {
      await this._persistToRedis(merged);
    }

    console.log(`✅ Aggregated ${allEntries.length} raw entries → ${merged.size} unique indicators`);
    this.emit('refresh-complete', { count: merged.size });
  }

  _mergeIndicators(entries) {
    const merged = new Map();

    for (const entry of entries) {
      const existing = merged.get(entry.indicator);

      if (existing) {
        // Merge categories
        entry.categories?.forEach(c => existing.categories.add(c));
        // Add source
        existing.sources.add(entry.sourceName);
        // Weighted score: max + contribution from each new source
        existing.score = Math.min(
          1.0,
          existing.score + entry.sourceWeight * entry.confidence * 0.1
        );
        existing.ttlMs = Math.max(existing.ttlMs, entry.ttlMs || 86400000);
        existing.timestamp = Math.max(existing.timestamp, entry.timestamp || Date.now());
      } else {
        merged.set(entry.indicator, {
          score: entry.sourceWeight * (entry.confidence || 0.7),
          categories: new Set(entry.categories || [entry.sourceCategory || 'unknown']),
          sources: new Set([entry.sourceName]),
          timestamp: entry.timestamp || Date.now(),
          ttlMs: entry.ttlMs || 86400000,
          metadata: entry.metadata || {},
        });
      }
    }

    return merged;
  }

  async _persistToRedis(merged) {
    const pipeline = this.redis.pipeline();
    for (const [indicator, entry] of merged) {
      const key = `threat:rep:${indicator}`;
      pipeline.set(key, JSON.stringify({
        score: entry.score,
        categories: [...entry.categories],
        sources: [...entry.sources],
        timestamp: entry.timestamp,
        ttlMs: entry.ttlMs,
      }));
      pipeline.expire(key, Math.ceil(entry.ttlMs / 1000));
    }
    await pipeline.exec();
  }
}

module.exports = ThreatFeedAggregator;
```

### 5.3 Feed Connectors

```javascript
// feed-connectors.js — Fetchers for major threat intelligence sources

/**
 * AbuseIPDB — Community-driven IP reputation
 * Requires API key: https://www.abuseipdb.com/api
 */
async function fetchAbuseIPDB(apiKey, { confidenceMinimum = 90, limit = 10000 } = {}) {
  const response = await fetch(
    `https://api.abuseipdb.com/api/v2/blacklist?confidenceMinimum=${confidenceMinimum}&limit=${limit}`,
    {
      headers: {
        'Key': apiKey,
        'Accept': 'application/json',
      },
      timeout: 30000,
    }
  );

  if (!response.ok) throw new Error(`AbuseIPDB: HTTP ${response.status}`);

  const data = await response.json();
  return (data.data || []).map(entry => ({
    indicator: entry.ipAddress,
    categories: entry.categories?.map(c => c.name) || ['abuse'],
    confidence: entry.abuseConfidenceScore / 100,
    ttlMs: 24 * 3600 * 1000,  // 24h
    metadata: {
      totalReports: entry.totalReports,
      lastReportedAt: entry.lastReportedAt,
      country: entry.countryCode,
    },
  }));
}

/**
 * AlienVault OTX — Open Threat Exchange
 * Requires API key: https://otx.alienvault.com/api
 */
async function fetchAlienVaultOTX(apiKey, { pulseTypes = ['ip', 'domain'] } = {}) {
  const indicators = [];

  for (const type of pulseTypes) {
    const response = await fetch(
      `https://otx.alienvault.com/api/v1/pulses/subscribed?types=${type}&limit=100`,
      { headers: { 'X-OTX-API-KEY': apiKey }, timeout: 30000 }
    );

    if (!response.ok) {
      console.warn(`AlienVault OTX (${type}): HTTP ${response.status}`);
      continue;
    }

    const data = await response.json();
    for (const pulse of data.results || []) {
      for (const ind of pulse.indicators || []) {
        indicators.push({
          indicator: ind.indicator,
          categories: pulse.tags || ['threat'],
          confidence: pulse.adversary ? 0.9 : 0.6,
          ttlMs: 7 * 24 * 3600 * 1000,  // 7 days
          metadata: {
            pulseName: pulse.name,
            pulseId: pulse.id,
            created: pulse.created,
          },
        });
      }
    }
  }

  return indicators;
}

/**
 * CrowdSec CTI — Crowd-sourced IP reputation
 * Free tier: https://www.crowdsec.net/
 */
async function fetchCrowdSecCTI(apiKey) {
  // CrowdSec provides a blocklist
  const response = await fetch(
    'https://api.crowdsec.net/v2/decisions/stream?startup=false',
    {
      headers: {
        'X-Api-Key': apiKey,
        'Accept': 'application/json',
      },
      timeout: 30000,
    }
  );

  if (!response.ok) throw new Error(`CrowdSec: HTTP ${response.status}`);

  const data = await response.json();
  // CrowdSec format: { new: [...decisions], deleted: [...] }

  const entries = [];
  for (const decision of data.new || []) {
    if (decision.scope === 'Ip') {
      entries.push({
        indicator: decision.value,
        categories: [decision.scenario || 'attack'],
        confidence: 0.85,
        ttlMs: Date.parse(decision.until) - Date.now(),
        metadata: {
          scenario: decision.scenario,
          origin: decision.origin,
          type: decision.type,
        },
      });
    }
  }

  return entries;
}

/**
 * URLhaus — Malware URL database (Abuse.ch)
 * Free, no API key required
 */
async function fetchURLhaus() {
  const response = await fetch(
    'https://urlhaus-api.abuse.ch/v1/urls/recent/limit/1000/',
    { timeout: 30000 }
  );

  if (!response.ok) throw new Error(`URLhaus: HTTP ${response.status}`);

  const data = await response.json();
  if (data.query_status !== 'ok') throw new Error(`URLhaus: ${data.query_status}`);

  return (data.urls || []).map(entry => ({
    indicator: entry.url,
    categories: ['malware_distribution'],
    confidence: 0.9,
    ttlMs: 7 * 24 * 3600 * 1000,
    metadata: {
      threat: entry.threat,
      urlStatus: entry.url_status,
      tags: entry.tags,
    },
  }));
}

/**
 * Emerging Threats (Proofpoint) — Open ruleset
 * Free: https://rules.emergingthreats.net/
 */
async function fetchEmergingThreatsIPs() {
  const response = await fetch(
    'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
    { timeout: 30000 }
  );

  if (!response.ok) throw new Error(`EmergingThreats: HTTP ${response.status}`);

  const text = await response.text();
  return text.split('\n')
    .filter(line => line.trim() && !line.startsWith('#'))
    .map(ip => ({
      indicator: ip.trim(),
      categories: ['compromised', 'c2'],
      confidence: 0.8,
      ttlMs: 24 * 3600 * 1000,
    }));
}

/**
 * Tor Exit Nodes — List of known Tor exit nodes
 */
async function fetchTorExitNodes() {
  const response = await fetch(
    'https://check.torproject.org/torbulkexitlist',
    { timeout: 30000 }
  );

  if (!response.ok) throw new Error(`Tor exit list: HTTP ${response.status}`);

  const text = await response.text();
  return text.split('\n')
    .filter(line => line.trim())
    .map(ip => ({
      indicator: ip.trim(),
      categories: ['anonymizer', 'tor'],
      confidence: 0.5,   // Tor is not inherently malicious but high-risk
      ttlMs: 3600 * 1000,  // 1h — list changes frequently
    }));
}

module.exports = {
  fetchAbuseIPDB,
  fetchAlienVaultOTX,
  fetchCrowdSecCTI,
  fetchURLhaus,
  fetchEmergingThreatsIPs,
  fetchTorExitNodes,
};
```

### 5.4 Real-Time Reputation Middleware

```javascript
// reputation-middleware.js — Block requests from known malicious IPs/domains
class ReputationMiddleware {
  constructor(aggregator, { blockThreshold = 0.7, torPolicy = 'challenge' } = {}) {
    this.aggregator = aggregator;
    this.blockThreshold = blockThreshold;
    this.torPolicy = torPolicy;
  }

  middleware() {
    const self = this;
    return (req, res, next) => {
      const ip = req.ip || req.connection.remoteAddress;
      const result = self.aggregator.checkIp(ip);

      // Attach reputation to request for downstream use
      req.threatReputation = result;

      if (result.verdict === 'malicious') {
        console.warn(`🛑 Blocked malicious IP: ${ip} (score: ${result.score.toFixed(2)}, categories: ${result.categories.join(', ')})`);
        return res.status(403).json({
          error: 'Access denied',
          reason: 'security_reputation',
        });
      }

      if (result.categories.includes('tor') && self.torPolicy === 'challenge') {
        // Require additional verification for Tor users
        res.setHeader('X-Tor-Detected', 'true');
        res.setHeader('X-Challenge-Required', 'true');
      }

      if (result.verdict === 'suspicious') {
        // Apply stricter rate limiting
        res.setHeader('X-RateLimit-Scope', 'suspicious');
        req.rateLimitMultiplier = 0.25;  // 25% of normal rate limit
      }

      next();
    };
  }
}

module.exports = ReputationMiddleware;
```

### 5.5 Complete Application Integration

```javascript
// server.js — Full threat-feed-aware Express application
const express = require('express');
const ThreatFeedAggregator = require('./threat-feed-aggregator');
const {
  fetchAbuseIPDB,
  fetchAlienVaultOTX,
  fetchCrowdSecCTI,
  fetchTorExitNodes,
} = require('./feed-connectors');
const ReputationMiddleware = require('./reputation-middleware');

const app = express();

// ── Initialize threat feed aggregator ─────────────────────
const aggregator = new ThreatFeedAggregator({
  refreshIntervalMs: 300_000,  // 5 minutes
});

aggregator
  .registerFeed('abuseipdb', () =>
    fetchAbuseIPDB(process.env.ABUSEIPDB_API_KEY, { confidenceMinimum: 90 }),
    { weight: 0.9, category: 'abuse' }
  )
  .registerFeed('alienvault', () =>
    fetchAlienVaultOTX(process.env.OTX_API_KEY),
    { weight: 0.7, category: 'threat' }
  )
  .registerFeed('crowdsec', () =>
    fetchCrowdSecCTI(process.env.CROWDSEC_API_KEY),
    { weight: 0.8, category: 'attack' }
  )
  .registerFeed('tor', () =>
    fetchTorExitNodes(),
    { weight: 0.4, category: 'anonymizer' }
  );

aggregator.on('refresh-complete', ({ count }) => {
  console.log(`Threat DB: ${count} active indicators`);
});

aggregator.on('feed-error', ({ feed, error }) => {
  // Alert monitoring: feed X is failing
  console.error(`⚠️  Feed "${feed}" error: ${error}`);
});

aggregator.start();

// ── Mount reputation middleware ────────────────────────────
const reputation = new ReputationMiddleware(aggregator, {
  blockThreshold: 0.7,
  torPolicy: 'challenge',
});

app.use(reputation.middleware());

// ── Additional security middleware (from previous guides) ──
// app.use(cspMiddleware);
// app.use(csrfProtection);
// etc.

// ── Health check including threat feed status ─────────────
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    threatFeeds: aggregator.feeds.size,
    reputationScore: req.threatReputation?.score || 0,
  });
});

app.listen(3000);
```

### 5.6 Threat Feed Integration Checklist

- [ ] Integrate 3+ threat intelligence sources (AbuseIPDB, AlienVault OTX, CrowdSec are a good baseline)
- [ ] Apply source-specific weights: premium feeds weigh higher than freely available lists
- [ ] Implement TTL-based expiration: stale intelligence is worse than none
- [ ] Cache reputation lookups in-memory (Map/Redis) for sub-millisecond access
- [ ] Fail open: if all feeds are down, don't block legitimate traffic
- [ ] Log all blocks with full context (IP, score, categories, sources) for SIEM correlation
- [ ] Add `/health` endpoint that reports feed status and indicator count
- [ ] Apply graduated response: Tor → challenge, suspicious → stricter rate limit, malicious → block
- [ ] Monitor false-positive rate: allow internal test IPs to bypass reputation checks
- [ ] Regularly audit which feeds are providing unique value; prune stale feeds

---

## Appendix A: End-to-End Security Pipeline

```
 ┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
 │   Developer  │────▶│   CI/CD       │────▶│  Artifact     │────▶│  Production  │
 │   git push   │     │               │     │  Registry     │     │  Deployment  │
 └─────────────┘     │ • SAST scan   │     └──────┬────────┘     └──────┬──────┘
                     │ • SCA scan    │            │                     │
                     │ • SBOM gen    │            │ SBOM + Provenance   │
                     │ • SLSA attest │            │ verification        │
                     │ • SRI verify  │            │                     │
                     │ • npm audit   │     ┌──────▼────────┐     ┌──────▼──────┐
                     └──────────────┘     │  Artifact      │     │  Runtime     │
                                          │  Signing       │     │  Protection  │
                                          │  (Cosign)      │     │              │
                                          └───────────────┘     │ • RASP       │
                                                                 │ • ML Abuse   │
                                                                 │   Detection  │
                                                                 │ • Threat Feed│
                                                                 │   Reputation │
                                                                 │ • SRI (CDN)  │
                                                                 └──────────────┘
```

## Appendix B: Quick-Reference Cheatsheet

### Tier C2 — What's Covered

| Domain | Technique | Tooling |
|--------|-----------|---------|
| **Supply Chain** | SLSA L3 builds, CycloneDX SBOM, signed provenance | SLSA GitHub Generator, Syft/Grype, Cosign |
| **RASP** | In-process SQLi/CMDi/path-traversal/deserialization hooks | Custom Node.js agent, ByteBuddy (Java) |
| **API Abuse Detection** | Isolation Forest on 17-dim behavioral features | Python scikit-learn, Node feature extractor |
| **SRI** | Auto-generation, CI enforcement, cache management | jsdom + crypto, Vite plugin |
| **Threat Feeds** | Multi-source aggregation, weighted scoring, TTL expiry | AbuseIPDB, AlienVault OTX, CrowdSec CTI, Tor exit nodes |

### Maturity Model

| Level | Supply Chain | RASP | Abuse Detection | SRI | Threat Feeds |
|-------|-------------|------|-----------------|-----|-------------|
| **L1** | `npm audit` in CI | None | Basic rate limiting | Manual hashes on key pages | None |
| **L2** | SBOM generated; pinned deps | Log-only mode | Rule-based heuristics | SRI in CI for all pages | Single feed (e.g., AbuseIPDB) |
| **L3** | Signed SBOM + provenance; SLSA L3 | Block mode on critical paths | ML anomaly detection, shadow mode | Auto-injected SRI at build time | 3+ aggregated feeds, weighted scores |
| **L4** | Hermetic builds; reproducible; SLSA L4 | Full coverage, zero FPs, performance <2% | Real-time blocking, adaptive thresholds | Cryptographic verification of all third-party assets | Curated threat intel, custom IOCs, STIX/TAXII |

---

*End of Advanced Web Security Engineering Guide — Tier C2. Each section builds incrementally on the foundational OWASP and web security defenses covered in the Tier C1 guide (run-20260626-000800).*
