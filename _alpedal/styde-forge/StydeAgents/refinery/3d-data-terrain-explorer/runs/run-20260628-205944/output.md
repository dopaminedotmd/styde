Teacher feedback analysis:
Changes required with priority ordering:
1. persona.md: delete entirely
   impact: high
   reason: Principles section duplicates blueprint Persona section. Agent already has blueprint in context. Wastes tokens on every generation pass.
2. BLUEPRINT.md: remove 'Quality Standards' section
   impact: high
   reason: Generic quality rules bolted on at end. Each rule belongs inline at the step it governs. Script consolidation goes inside build script step, verification rule goes inside final step, etc.
3. BLUEPRINT.md: inline each quality rule into relevant step
   impact: high
   rules to relocate:
     'run verification' -> final required action in task structure. Task not complete until verification output is presented.
     'Script consolidation' -> inside build script step
     remaining quality rules -> respective steps
4. BLUEPRINT.md: strip all meta-extraction directives
   impact: medium
   targets: 'DO NOT extract', omit-lists, any instruction targeting eval harness instead of agent builder. These confuse the agent's primary goal (terrain dashboard generation).
5. persona.md replacement (if kept): add completion checklist rule
   impact: high
   text: 'After every edit, you MUST run the corresponding verification/test command and include its output in your response. An edit without verification is not a finished task.'
Blueprint current state:
  score: 77.6/100
  completeness: weakest dimension
  accuracy: 90/95 (good judgment)
  failure mode: stops after edit, skips verification execution
  result: completeness and usefulness dragged below production threshold
Revised task structure for BLUEPRINT.md:
  Step 1: Parse input data shape and metric mappings
  Step 2: Generate Three.js BufferGeometry heightfield terrain
  Step 3: Map secondary metric to vertex colors (vegetation gradient)
  Step 4: Trace error/anomaly paths as river geometry
  Step 5: Build particle system for data flow trails
  Step 6: Wire OrbitControls with damping + auto-rotation + bookmarks
  Step 7: Implement time slider terrain reshape
  Step 8: Export interactive HTML dashboard panel
  Step 9: RUN VERIFICATION - execute the output HTML, confirm terrain renders, controls work, particles flow, time slider reshapes geometry. Present verification output in response. Task is not complete until this step outputs results.
No write_file used as instructed. Above is the actionable diff.