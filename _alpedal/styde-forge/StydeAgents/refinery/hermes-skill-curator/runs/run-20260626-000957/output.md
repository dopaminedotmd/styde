## SKILL CURATION ANALYSIS - default profile
### Current state
Zero skills installed. Profile is bare.
### Gap assessment
Design gap: no skill exists. Every agent spawn inherits only the base system prompt. No behavioral shaping, no domain expertise injection.
Compose gap: no skill chains possible. Cannot build multi-step workflows.
Deps gap: no dependency graph exists. No conflicts, also no synergy.
Reuse gap: no pattern extraction. Every agent learns from scratch.
Test gap: no benchmark harness. Cannot measure if skills improve outcomes.
### Recommended skill architecture
Core skills to create for Styde Forge context:
1.  **forge-core.skill.md**
    Purpose: Mission Control context. Injects Blueprint ID, agent role, caveat flags, spawn type. Every spawned agent gets forge awareness without manual instruction.
    Deps: none.
2.  **swedish-svar.skill.md**
    Purpose: Swedish response mode. Sets language preference, avoids English boilerplate. Structured directives for conciseness.
    Deps: none. Compose: loads before forge-core to set language.
3.  **agent-spawn.skill.md**
    Purpose: Delegate task protocol. Standardizes how agents spawn sub-agents. Shared channel, task packing, result format.
    Deps: forge-core (needs to know spawn context).
4.  **blueprint-loader.skill.md**
    Purpose: Loads blueprint YAML from forge repo, extracts purpose/persona/skills, sets task constraints.
    Deps: forge-core (needs repo path). Compose: runs after swedish-svar.
5.  **eval-harness.skill.md**
    Purpose: Post-task evaluation. Grades agent output against blueprint criteria. Stores results.
    Deps: forge-core.
### Dependency graph
swedish-svar (root)
  |
forge-core (root)
  |
  +-- agent-spawn
  |
  +-- blueprint-loader
  |
  +-- eval-harness
### Potential conflicts
None expected - skills are additive, no overlapping directives. Risk if two skills both set `language` variable or both define `delegate_task` - but forge-core owns spawn, swedish-svar owns language, clear separation.
### Reuse patterns
agent-spawn.skill.md is reusable across any multi-agent system outside Styde Forge. Extract as standalone and import as dep.
swedish-svar.skill.md is reusable for any Swedish-speaking user on any project.
### Optimization recommendation
Create 5 files. Priority order: forge-core > swedish-svar > blueprint-loader > agent-spawn > eval-harness. Install via skill_view(name='...') or place in ~/.hermes/profiles/default/skills/. Each 50-100 lines of SKILL.md. Total time: ~20 minutes.
Want me to write them out with write_file?