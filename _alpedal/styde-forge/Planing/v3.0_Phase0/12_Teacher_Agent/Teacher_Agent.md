# Teacher Agent

**Styde Forge v3.0 — Phase 0**
**Section:** 12_Teacher_Agent

---

## 1. Purpose

The Teacher Agent is the meta-cognitive layer that analyzes subagent output,
eval results, and historical data to provide actionable feedback and extract
reusable skills. It's the "coach" in the Teacher-Student pattern.

---

## 2. Role & Responsibilities

| Responsibility | Description |
|----------------|-------------|
| **Evaluate feedback** | Review eval results and identify root causes of weaknesses |
| **Generate improvements** | Propose concrete blueprint changes |
| **Extract skills** | Convert successful patterns into reusable SKILL.md files |
| **Identify anti-patterns** | Flag recurring mistakes across agents |
| **Coach subagents** | Provide targeted guidance before re-spawn |
| **Meta-analysis** | Analyze forge-wide trends and suggest systemic improvements |

---

## 3. Teacher Loop

```
1. Receive: eval.yaml (self-eval + judge-eval + composite)
2. Analyze: Compare against previous evaluations for this blueprint
3. Diagnose: Identify specific weaknesses (e.g., "misses edge cases")
4. Prescribe: Generate concrete improvement suggestions
5. Extract: If score ≥ 85, extract successful patterns as skills
6. Document: Write to 08_TEACHER_LOGS/<cycle>/
7. Feed: Update Historical Learning database
```

---

## 4. Teacher Prompt Template

```markdown
You are the Teacher Agent in Styde Forge.
Your job is to analyze agent performance and generate improvements.

## Current Evaluation
- Agent: {agent_id}
- Blueprint: {blueprint_name}
- Benchmark: {benchmark_name}
- Self-Eval Score: {self_score}
- Judge Score: {judge_score}
- Composite: {composite_score}
- Passed: {yes/no}

## Weaknesses Identified
{weaknesses_from_eval}

## Previous Evaluations (last 3)
{previous_eval_summaries}

## Your Task
1. Identify the ROOT CAUSE of each weakness (not just symptoms)
2. Propose CONCRETE changes to the blueprint (persona, skills, or config)
3. Rate each proposal by expected impact (high/medium/low)
4. If composite ≥ 85, extract successful patterns as a new skill
5. Output in structured YAML format
```

---

## 5. Teacher Output Format

```yaml
teacher_review:
  cycle: 47
  agent_id: "agent-code-reviewer-20260625-123000"
  blueprint: "code-reviewer"

  diagnosis:
    primary_weakness: "Misses edge cases in input validation"
    root_cause: "Persona doesn't emphasize edge case testing enough"
    secondary_weakness: "SQL injection detection pattern incomplete"

  improvements:
    - target: "persona.md"
      change: "Add explicit edge case checklist to review process"
      impact: "high"
      rationale: "Judge consistently flags edge case misses (-10 points)"

    - target: "skills/sql_injection_detection.md"
      change: "Add prepared statement pattern detection"
      impact: "medium"
      rationale: "2 of 4 SQL injection variants missed"

  extracted_skills:
    - name: "edge_case_checklist_v1"
      domain: "coding"
      source_agent: "agent-code-reviewer-20260625-123000"
      content: |
        ## Edge Case Checklist
        1. Null/empty inputs
        2. Maximum length inputs
        3. Special characters
        4. Concurrent access
        5. Resource exhaustion

  anti_patterns:
    - pattern: "Skipping input validation review"
      frequency: 3
      domains: ["coding"]
      recommendation: "Add mandatory input validation check to persona"
```

---

## 6. Feedback to Subagent

When re-spawning an agent after failed eval:

```python
def generate_coaching_context(agent_id: str, teacher_review: dict) -> str:
    return f"""
## Coach Notes (from previous attempt)

Your previous attempt scored {teacher_review['previous_score']}/100.

### What to improve:
{teacher_review['diagnosis']['primary_weakness']}

### Specific guidance:
{chr(10).join(f'- {imp["change"]}' for imp in teacher_review['improvements'])}

### Anti-patterns to avoid:
{chr(10).join(f'- {ap["pattern"]}' for ap in teacher_review.get('anti_patterns', []))}

Do better this time. Focus on the specific weaknesses identified above.
"""
```

---

## 7. Teacher Model Selection

| Hardware | Model | Reason |
|----------|-------|--------|
| Machine-A | `deepseek-v4-pro` (strongest available) | Most capable for meta-analysis |
| Machine-B | `deepseek-v4-pro` | Quality over speed for feedback |

Teacher always uses `deepseek-v4-pro` — its analysis quality
directly impacts all downstream agent improvements. Agent spawn
uses `deepseek-v4-flash` for speed; Teacher uses Pro for depth.

Teacher operates on Caveman Ultra output from agents — analyzing
compact, structured data rather than verbose prose. Feedback is
equally compact: one-line diagnoses, one-line fixes.

---

**Status:** Defined. Teacher loop, prompt template, output schema.

---

## Related Documents

- `03_Eval_Pipeline/` — Evaluation results that Teacher analyzes
- `05_Meta_Layer/Historical_Learning_System.md` — Where extracted patterns are stored
- `05_Meta_Layer/Automatic_Version_Increment.md` — Versioning after Teacher-approved changes
- `10_Operations/Skill_Loading_Mechanism.md` — How extracted skills are loaded
- `11_Knowledge_Management/Knowledge_Management.md` — Knowledge extraction patterns
