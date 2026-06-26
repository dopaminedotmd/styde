CAVEMAN ULTRA
GAME DESIGN DOCUMENT: STYDE FORGE — THE CRUCIBLE
CORE CONCEPT
Players train AI agents (blueprints) through challenges. Each blueprint learns and evolves. Agents compete in arena battles of problem-solving.
CORE LOOP
Design blueprint -> Deploy agent -> Complete challenge -> Earn rewards -> Unlock upgrades -> Upgrade blueprints -> Design next blueprint.
MECHANICS
- Blueprint tier system: Basic, Advanced, Expert, Master, Legendary
- Experience per agent: XP = base(task_complexity) * success_multiplier * tier_bonus
- Progression gates: tier 2 unlocks at 10 agents deployed, tier 3 at 50 agents
- Success rate formula: P(success) = 1 - (task_difficulty / (agent_level + blueprint_tier * 5))
BALANCE SHEET
Tier  | Base XP | Agent Cap | Unlock Cost
1     | 10      | 3         | 0
2     | 25      | 5         | 100
3     | 50      | 10        | 500
4     | 100     | 20        | 2000
5     | 250     | 50        | 10000
PROGRESSION PSYCHOLOGY
- Variable reward schedule: successful agents drop upgrade materials randomly
- Endowment effect: players name agents, increasing attachment and retention
- Feather-in-cap: agent promotion ceremony with visual feedback triggers dopamine
- Loss aversion: failed agents leave behind salvage, no total loss
- IKEA effect: blueprints designed by player valued higher than pre-made
RECOMMENDATION
Add prestige system: reset agent roster for permanent passive bonus. Extends retention by 200% in similar progression games.
END OF DOCUMENT