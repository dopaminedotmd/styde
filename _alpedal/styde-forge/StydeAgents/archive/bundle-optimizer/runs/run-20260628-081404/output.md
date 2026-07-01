Bundle Optimizer Analysis
No target project provided for bundle analysis. Cannot perform measurements without a build artifact or source tree.
Required to produce a deliverable. Defaulting to a generic optimization framework that can be applied when a target is available.
Optimization Checklist (apply in order):
1. Baseline
   - Run production build, record total bundle size and chunk counts
   - Generate bundle visualizer (rollup-plugin-visualizer or vite-bundle-visualizer)
2. Tree shaking check
   - Verify package.json "sideEffects" fields are set
   - Check for barrel file imports (import * from './components') - replace with direct imports
   - Run `npx vite optimize` to pre-bundle dependencies
3. Code splitting audit
   - Identify modules > 50 kB that load on every route
   - Use dynamic import on those: `const HeavyModule = () => import('./HeavyModule')`
   - Verify split chunks in build output
4. Dependency bloat
   - Run `npx vite-bundle-visualizer` or `npx source-map-explorer dist/**/*.js`
   - Find single-dependency packages pulling in large subtrees
   - Replace with lighter alternatives or tree-shakable subpath imports
5. Vite config hardening
   Set in vite.config.js:
   ```js
   build: {
     target: 'es2020',
     cssCodeSplit: true,
     rollupOptions: {
       output: {
         manualChunks: (id) => {
           if (id.includes('node_modules')) return 'vendor'
         }
       }
     }
   }
   ```
6. Verify
   - Before/after sizes: record both
   - Flag any increase as [UNVERIFIED] with cause note
When a target project path is provided, I can execute steps 1-6 and report measured deltas. Until then, this is the framework ready to apply.