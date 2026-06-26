teacher feedback parsed. blueprint loaded. three fixes already incorporated in steps 5, 7, 10, and reporting rules.
remaining gaps from 184201 feedback:
gap 1: efficiency constraints section missing from blueprint
  fix: add section between skills and integration context with max tool calls per phase
  file: BLUEPRINT.md
  location: after Skills block, before Integration Context
  add: |-
    Efficiency Constraints
      toolcallbudget:
        generation: 15 calls
        evaluation: 10 calls
        gate: 5 calls
        promotion: 3 calls
      failfast: true
      maxretrysamepattern: 1
gap 2: verificationstyle: compact config parameter missing
  fix: add to config section or persona as inline trait
  implement as field: verificationstyle: compact
  effect: strips ANSI color codes from diff output, uses plain text assertions
gap 3: persona trait 'optimizes for minimal tool calls' missing
  fix: add to persona traits as second bullet after the dr y css rule
  text: 'optimises for minimal tool calls — prefers batch verification over single-assertion-at-a-time loops. uses fail-fast: stops verification after first failed assertion on the same pattern.'
these three patches close all three feedback gaps. no mockup task given yet — waiting for a dashboard brief to produce the 3+ spatial interface artifacts.