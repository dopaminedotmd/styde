# DCE and Constant Propagation Skill
This skill defines dead code elimination and constant propagation procedures. Load with skill_view(name='dce-skill').

## Dead Code Elimination

Eliminate variables and instructions that have no observable effect on program output.

Algorithm:
1. Mark all variables used in return statements, exports, or side-effect-producing calls (I/O, writes, function calls with observable effects) as live.
2. Walk backward through the AST: any variable that feeds into a live variable is also live.
3. Any variable not reachable from a live root is dead and can be removed.
4. Remove dead variable declarations and their associated assignment instructions.
5. Remove unreachable basic blocks (blocks with no incoming edges after variable removal).

Edge cases:
-- Variables assigned but never read: remove declaration and assignment. Example: let x = 5; followed by no read of x before scope exit.
-- Variables assigned, read only by a now-dead variable: transitive removal. Example: let x = computeExpensive(); let y = x + 2; console.log(z); -- if z is undefined and y is only read by z, both y and x are dead.
-- Function parameters that are never used inside the function body: can be dropped from call sites if the callee signature allows.

## Constant Propagation and Folding

Replace variables whose values are known at compile time with their literal values.

Algorithm:
1. Identify variables assigned exactly once with a literal value (number, string, boolean, null, undefined).
2. Trace all references to that variable through the AST.
3. Replace each reference with the literal value.
4. After replacement, re-run DCE if the variable is now unreferenced.
5. Fold constant expressions: replace 2 + 3 with 5, "hello " + "world" with "hello world", true && false with false, etc.

Edge cases:
-- Conditional branch folding: if (true) { ... } else { ... } -> keep only the true branch.
-- Ternary folding: false ? a : b -> b.
-- String concatenation with mixed types: if one side is non-constant, do not fold the concatenation.
-- Object property access through a constant chain: const PATH = 'a.b.c'; obj[PATH] -- do NOT fold PATH into the access unless the full chain is also constant.

## Transitive Dead Code Detection

Detect and eliminate chains where a variable becomes dead only after constant propagation removes dependent variables.

Example chain: let x = 10; let y = x + 5; let z = y * 2; console.log("done");

Step-by-step treatment:
1. Constant propagation identifies x=10, folds y=10+5 -> y=15, folds z=15*2 -> z=30.
2. After folding, console.log("done") does not reference x, y, or z.
3. DCE pass marks x, y, z as dead because no live root reaches them.
4. All three declarations and assignments are removed.
5. Output: console.log("done");

Test this chain explicitly in the self-checking harness below.

Another transitive chain: function f() { let a = allocate(); let b = transform(a); return b; } g(f()); where g discards its argument.

Treatment:
1. If g(...) discards its argument (no reference to param inside g), then the return value of f() is dead.
2. If the return is dead, b is dead.
3. If b is dead, a is dead.
4. If a is dead, the call to allocate() is dead.
5. The entire call f() and the function body can be eliminated (if f has no other side effects).

## Self-Checking Test Harness

The following test cases MUST pass after every change to the DCE or constant propagation logic. Run them with the self_check action.

Test case 1 - basic DCE:
Input:
  let dead = 42;
  let live = 10;
  console.log(live);
Expected: console.log(10); (dead removed; live folded from 10)

Test case 2 - transitive dead code:
Input:
  let x = 10;
  let y = x + 5;
  let z = y * 2;
  console.log("done");
Expected: console.log("done"); (x, y, z all removed after constant propagation)

Test case 3 - constant folding in branches:
Input:
  const DEBUG = false;
  if (DEBUG) { console.log("debug"); }
  console.log("running");
Expected: console.log("running"); (DEBUG=false, if block dead)

Test case 4 - transitive function deadness:
Input:
  function helper() { let a = malloc(1024); let b = process(a); return b; }
  function discard(x) { return null; }
  discard(helper());
Expected: empty output or only side-effect-free no-ops (both functions dead if no side effects)

Test case 5 - source map conformance:
After any optimization, generate a source map. Assert:
- sourceMap.version === 3
- sourceMap.mappings is a non-empty string of VLQ characters
- sourceMap.names is an Array
- sourceMap.sources is an Array
- All mappings decode to valid (generatedLine, generatedColumn, sourceIndex, sourceLine, sourceColumn, nameIndex) tuples

Test case 6 - report matches reality:
After any optimization pass, assert:
- The count of reported removed variables equals the actual difference in variable declarations between pre-pass and post-pass AST.
- The count of reported removed instructions equals the actual difference in instruction nodes.
- If mismatch > 0, emit FAIL with detailed diff output. Do not silently accept.

Usage:
  self_check action=run test=<test_number>
  self_check action=run_all
