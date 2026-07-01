teacher-agent-chicken-check skill design
purpose:
  Inspects agent's own trace before summary emission. Counts write_file, patch, terminal (modifying ops) calls. If zero, blocks summary and emits WARNING.
implementation approach:
  Two hooks needed in the runtime or skill lifecycle:
    pre_summary: examine tool_call history in session
    block: set a flag that prevents summary formatting
skill file structure:
  skills/teacher-agent-chicken-check/
    SKILL.md
    chicken_check.py
SKILL.md content:
name: teacher-agent-chicken-check
version: 1
domain: meta / quality
trigger: lifecycle:pre_summary
action: run chicken_check.py
failure_mode: block_summary + emit WARNING
description: |
  Before summary, count write_file/patch/terminal calls in current turn.
  If count=0 and the turn contained a user request that expects a file change or action,
  block summary emission and emit WARNING: "Zero tool calls with file effect detected.
  Teacher analysis produces diagnostics-only output. Structural enforcement required."
chicken_check.py logic:
def chicken_check(session):
    tool_calls = session.get_tool_calls(current_turn=True)
    actionable = ['write_file', 'patch', 'terminal']
    count = sum(1 for tc in tool_calls if tc.name in actionable)
    if count == 0:
        turn_requests = session.get_user_requests(current_turn=True)
        # heuristic: if user asked for a change, file, fix, implement, create, build
        action_keywords = ['create', 'change', 'fix', 'implement', 'write', 'build', 'make', 'patch', 'add']
        if any(kw in turn_requests[-1].lower() for kw in action_keywords):
            session.block_summary()
            session.emit_warning(
                "WARNING: Zero tool calls with file effect. "
                "Teacher analysis reproduces the analysis-without-action failure mode. "
                "Structural enforcement engaged: summary blocked."
            )
            return False
    return True
integration:
  hook into the summary pipeline before the final emit call
  if block_summary flag is set, the agent MUST NOT produce any output — return instead
failure mode:
  if chicken_check itself crashes, fail open (allow summary) and log error
  if chicken_check blocks, agent receives WARNING and turn ends without summary
resonance with teacher feedback:
  The irony the teacher diagnosed — diagnosing actionlessness by producing more analysis — is structurally prevented by this skill. No summary = no analysis to emit. The agent has no choice but to execute tool calls.
estimated token overhead:
  <10 tokens per tool call inspected
  <50 tokens for the pre_summary hook call
  negligible at any scale
contingency:
  if the runtime does not expose tool_call history at pre_summary time, fall back to post-hoc check: append WARNING to summary stats without blocking emission ("chicken-check: 0 file ops detected — this turn may be analysis-only")