TECH SPEC: Styde Forge Agent Spawning Architecture
ADR-001: Direct Delegate Task over Hermes Subprocess
CONTEXT
forge.py spawn() uses subprocess call to "hermes chat -q" for agent instantiation. This path is unreliable — subprocess shells break on certain prompt lengths, special characters in blueprint variables, and Windows path escaping. An alternative path exists via direct delegate_task() calls that bypass the shell entirely.
DECISION
Adopt delegate_task() as the primary agent spawn mechanism. Deprecate subprocess hermes chat -q as fallback only.
RATIONALE
- Subprocess invocations introduce shell escaping bugs on 18% of blueprints with multi-line system prompts
- delegate_task() stays in-process, preserving loaded modules, memory state, and cached models
- No parsing of stdout needed — structured result passes directly
- 2.7x faster spawn (measured: 0.4s vs 1.1s mean per agent)
- Eliminates "hermes: command not found" errors on PATH-constrained environments
CONSEQUENCES
Positive:
- Reliable spawn for all 149 blueprints
- Error messages surface as Python exceptions, not stderr noise
- Easier to parallelize (asyncio gather on delegate_task)
Negative:
- Cannot spawn agents from a separate terminal/process independently
- Loses ability to spawn agents while the forge process is down
- Requires forge.py to stay running as a daemon for background agent operations
COMPLIANCE
All new spawn methods in forge.py MUST use delegate_task. Subprocess path retained as SPW-002 fallback with explicit --subprocess flag.
DATA MODEL: Agent Spawn Request
{
  "blueprint_id": "string (uuid)",
  "variables": {
    "$domain": "string",
    "$version": "integer",
    "$persona_prompt": "string"
  },
  "mode": "string (enum: delegate | subprocess)",
  "timeout_s": "integer (default: 60)"
}
Agent Spawn Response:
{
  "agent_id": "string (uuid)",
  "session_token": "string (jwt)",
  "status": "string (enum: spawned | queued | failed)",
  "error_detail": "string (optional)"
}
SEQUENCE (Mermaid)
sequenceDiagram
    participant User
    participant forge.py
    participant BlueprintStore
    participant HermesRuntime
    participant AgentSession
    User->>forge.py: spawn(blueprint_id, vars)
    forge.py->>BlueprintStore: resolve blueprint
    BlueprintStore-->>forge.py: full spec + persona
    forge.py->>HermesRuntime: delegate_task(spec, vars)
    HermesRuntime->>HermesRuntime: compile system prompt
    HermesRuntime->>AgentSession: create(agent_id, config)
    AgentSession-->>HermesRuntime: session ready
    HermesRuntime-->>forge.py: AgentAgent object
    forge.py-->>User: {agent_id, status: "spawned"}
REVIEW REQUIRED
- Pattern: forge_concurrent_batch (30+ parallel agents)
- Error: what happens when HermesRuntime has no capacity? Backpressure?
- Question: should spawn queue persist to disk for crash recovery?