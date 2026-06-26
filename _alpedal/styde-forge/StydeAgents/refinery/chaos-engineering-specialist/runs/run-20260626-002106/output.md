TARGET: styde-forge codebase
STEADY STATE: 149 blueprints, ~188 agents, Caveman Ultra ON. Default model deepseek-v4-flash. delegation.max_concurrent_children=5.
FAULT INJECTION CANDIDATES:
1. Concurrency fault: raise max_concurrent_children from 5 to 50. Observe agent spawn behavior under load.
2. Network fault: inject 2000ms latency on delegate_task calls. Verify timeout handling.
3. Pod fault: kill hermes_bridge subprocess mid-spawn. Verify recovery.
4. Resource fault: memory limit to 256MB during blueprint compilation. Verify OOM handling.
5. Config fault: swap default model to nonexistent model name. Verify fallback chain.
BLAST RADIUS: start with single blueprint (web-dev-01). Isolate to one agent session.
RECOVERY VERIFICATION: expect automatic retry (3 attempts), fallback model selection, and session isolation timeout (60s max per child). If no recovery, circuit breaker activates.
REPORT: ready to execute experiment 1-5. Which fault first?