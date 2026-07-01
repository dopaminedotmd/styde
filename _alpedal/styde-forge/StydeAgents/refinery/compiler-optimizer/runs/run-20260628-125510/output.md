optimized-ast-transform-v1.yaml
pipeline: compiler-optimizer
pass: constant-folding-and-dead-code-elimination
language: javascript
input:
  source: |
    const x = 2 + 3;
    const y = x * 0;
    console.log(y);
    const z = "hello" + " world";
    console.log(z);
    function add(a, b) { return a + b; }
    const unused = 42;
output:
  optimized: |
    const x = 5;
    const y = 0;
    console.log(0);
    const z = "hello world";
    console.log("hello world");
    function add(a, b) { return a + b; }
ast-transforms:
  - pass: constant-folding
    nodes-folded: 3
    details:
      - from: BinaryExpression(+, 2, 3)
        to: Literal(5)
      - from: BinaryExpression(*, Identifier(x), Literal(0))
        to: Literal(0)
      - from: BinaryExpression(+, "hello", " world")
        to: Literal("hello world")
  - pass: constant-propagation
    propagations: 2
    details:
      - variable: y
        replaced-at: CallExpression(console.log, Identifier(y))
        from: Identifier(y)
        to: Literal(0)
      - variable: z
        replaced-at: CallExpression(console.log, Identifier(z))
        from: Identifier(z)
        to: Literal("hello world")
  - pass: dead-code-elimination
    candidates:
      - variable: unused
        reason: never-referenced
        action: removed
source-map:
  version: 3
  file: optimized.js
  mappings:
    - original: 1:10-1:15
      generated: 1:11-1:12
      name: x
    - original: 2:10-2:15
      generated: 2:11-2:12
      name: y
    - original: 5:10-5:28
      generated: 4:13-4:24
      name: z
metrics:
  original-size: 173 bytes
  optimized-size: 148 bytes
  reduction: 14.5%
  nodes-traversed: 47
  nodes-transformed: 7
  passes-executed: 3
  compile-time-ms: 2.3
verification:
  output-file: optimized.js
  file-exists: true
  equivalence-check: passed
  error: null