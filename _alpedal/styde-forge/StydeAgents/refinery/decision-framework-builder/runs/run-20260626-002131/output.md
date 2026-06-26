DECISION RECORD: Agent orchestration model for Styde Forge
DECISION: Orchestration model — hierarchical supervisor vs flat event bus
CONTEXT: 149 blueprints, ~188 concurrent agents, max_children=5
WEIGHTED DECISION MATRIX
Criterion                          Weight    Supervisor    Event Bus
Scalability to 500+ agents          0.30     7 (2.10)      9 (2.70)
Debugging / traceability            0.20     9 (1.80)      4 (0.80)
Latency per decision hop            0.15     5 (0.75)      8 (1.20)
Implementation complexity           0.10     4 (0.40)      7 (0.70)
Existing codebase alignment         0.15     8 (1.20)      6 (0.90)
Failure isolation                   0.10     9 (0.90)      5 (0.50)
                                    1.00     7.15          6.80
SUPERVISOR WINS by 0.35 points. Margin: 5%.
RACI MATRIX (Supervisor model)
Activity                     R              A             C            I
Define agent hierarchy       Architect      Lead dev     Team         PM
Route delegation rules       Lead dev       Architect    QA           PM
Error escalation policy      Architect      Lead dev     Security     PM
Child timeout handling       Lead dev       Lead dev     Architect    PM
Dead agent reaping           DevOps         Lead dev     Architect    PM
TRADEOFF ANALYSIS
Supervisor pros:
+ Clear parent-child lineage for debugging
+ Failure isolation per subtree — one child crash does not cascade
+ Natural fit with existing delegate_task + max_children=5
+ Traceable decision path: root → supervisor → worker → result
Supervisor cons:
- Linear latency: each delegation hop adds round-trip to Hermes bridge
- Root supervisor becomes single-point bottleneck at scale
- Tree rebalancing needed when depth exceeds 3 levels
Event bus pros:
+ Horizontal scale: add more workers by subscribing to topics
+ Lower average latency per message: one fan-out instead of tree walk
+ No single bottleneck
Event bus cons:
+ No built-in lineage tracing — "which agent caused this?"
+ Cascade failures: one bad actor floods all subscribers
+ Requires new infrastructure (Redis pub/sub or NATS)
RECOMMENDATION
Keep hierarchical supervisor for phase 1 (current scale 188 agents).
Prepare event bus migration path at 500+ agents.
Add telemetry hooks on supervisor delegation now to ease future migration.
Document the switch point: when avg delegation depth exceeds 3, or when agent count > 500, move to event bus.