COMPLETE ARCHITECTURE MAPPED. Key findings from Hermes v0.17.0:
REGISTRY CORE (tools/registry.py, 589 lines)
- Singleton ToolRegistry with RLock, generation counter
- Each tool file self-registers at module import (registry.register(...))
- AST-based discovery: discover_builtin_tools() parses AST looking for top-level registry.register() calls, only imports matching files
- check_fn TTL cache at 30 sec, memoized per callable
- generation counter (_generation int) bumped on every register/deregister/alias change -- external callers memoize against it
- Shadow protection: cross-toolset overwrite rejected unless override=True
- Dynamic schema overrides via zero-arg callable, invoked on every get_definitions()
TOOLSET LAYER (toolsets.py, 928 lines)
- _HERMES_CORE_TOOLS = 38 built-in tool names shared across CLI + messaging platforms
- TOOLSETS dict maps {name: {tools, includes, description}} -- supports composition via includes
- get_toolset()/resolve_toolset() for resolution
EXECUTION PATH (agent/tool_executor.py, 1526 lines)
- Sequential + concurrent dispatch
- Parallel gating: _PARALLEL_SAFE_TOOLS = 12 read-only tools, _PATH_SCOPED_TOOLS = 3 file tools with independent path check, _NEVER_PARALLEL_TOOLS = {"clarify"}
- Tool Search unwrap bypasses bridge into direct dispatch (OpenClaw pattern)
- Pre-tool plugins, guardrails, checkpoint preflight, middleware chain
DISK REGISTRY (tools/process_registry.py)
- Separate process tracking system
Migration path from memory to file: tools/registry.py lines 230-306 for register(), 307-331 for deregister(), 337-384 for get_definitions().
Optimization opportunities identified:
1.  Loading order: _HERMES_CORE_TOOLS hardcodes 38 names in toolsets.py but registry auto-discovers from tools/*.py. No guaranteed loading order leads to potential race at module import. Fix: sorted() in glob + import gives deterministic order via filesystem sort.
2.  check_fn TTL (30s) is fixed. For Styde Forge batch spawning, most check_fns probe static things (Docker, Modal, Playwright). Could lift to 300s in batch mode.
3.  Generation counter serializes all mutations under one lock. MCP refresh + tool registration contend on the same RLock.
4.  No hot-reload hook. Registry has deregister but no filesystem watcher to auto-reload changed tool files.
5.  Tool search scoped names cache is thin -- no per-agent cache invalidation hook.
Send me a specific optimization target (loading order, profile, schema, caching, or hot-reload) and I'll deliver the concrete patch.