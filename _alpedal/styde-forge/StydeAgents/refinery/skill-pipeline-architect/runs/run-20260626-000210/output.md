Current forge system skill pipeline analysis:
Primary pipeline entry: forge.py delegate_task() -> hermes_bridge.py build_messages() -> skill_view() load -> skill execution -> result collection.
State contract between skills:
1. Skill view load produces skill dict with name, description, persona, instructions, tools.
2. build_messages() transforms skill dict into message list with system prompt + persona injection.
3. forge.py passes skill name as str, receives raw str result.
Error handling: None. No try/except between skill_view.load and forge.conversation. Error at any stage kills the entire spawn. Bubble-up only.
Parallel execution: None in current pipeline. delegate_task serializes each spawn. Forge could batch multiple delegate_task calls but creates one subprocess per spawn. No shared state between parallel branches.
Major gaps:
- No validation contract between skill_view output and message builder input
- No rollback on mid-pipeline failure
- No timeout per skill stage (only per whole conversation)
- No retry logic for transient skill_load failures
- No parallel fan-out orchestration
Fix: Add PipelineStage class with input_schema, output_schema, max_retries, timeout. Wrap each stage in try/except with fallback. Use asyncio.gather for parallel skill execution when skills are independent.