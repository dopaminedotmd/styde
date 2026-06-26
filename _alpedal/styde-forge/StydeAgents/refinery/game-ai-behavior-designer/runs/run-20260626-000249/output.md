CAVEMAN ULTRA MODE ACTIVE.
BUILD: Stealth game guard NPC behavior tree.
ROOT: Selector (priority order)
  -- Sequence: ALERT MODE
     -- Condition: IsPlayerDetected?
     -- Action: PlayAlertAnimation
     -- Action: TriggerAlarm
     -- Selector: EngageStrategy
        -- Sequence: CLOSE_COMBAT (utility > 0.8)
           -- Condition: PlayerInMeleeRange?
           -- Action: DrawMeleeWeapon
           -- Action: MeleeAttack
           -- Action: CallForReinforcements
        -- Sequence: RANGED_PURSUIT (utility 0.4-0.8)
           -- Condition: HasLineOfSight?
           -- Action: DrawRangedWeapon
           -- Action: ShootAtPlayer while strafing
           -- Action: MaintainDistance 8m
        -- Sequence: FLANK_ROUTE (utility < 0.4)
           -- Action: CalculateFlankPath (A* to intercept point)
           -- Action: MoveAlongPath
           -- Action: AmbushAtWaypoint
  -- Sequence: SUSPICIOUS MODE
     -- Condition: IsSuspicious?
     -- Action: PlayInvestigateAnimation
     -- Action: MoveToLastKnownNoise (A* path)
     -- Action: LookAround 3s
     -- Action: ResetToPatrol
  -- Sequence: PATROL MODE (default)
     -- Condition: PatrolPathExists?
     -- Action: FollowWaypoints (index + 1 each tick)
     -- Action: ScanEnvironment 60deg every 2s
     -- Action: ListenForNoise
FALLBACK: Idle
DIFFICULTY DYNAMIC ADJUSTMENT:
- Player kills 3+ guards in 30s: guard reaction time -40%, detection radius +25%, call reinforcements on any detection
- Player fails 3 attempts: guard reaction time +60%, detection radius -30%, give audio cues before detection
- Medium skill: baseline values
UTILITY SCORES for EngagementStrategy:
- closeCombatScore = (1 - playerHealthRatio) * 0.5 + distanceFactor(meleeRange) * 0.3 + backupCount * 0.2
- rangedScore = lineOfSight * 0.4 + (1 - coverNearPlayer) * 0.3 + healthAboveHalf * 0.3
- flankScore = (1 - awareOfFlank) * 0.5 + pathExistsToIntercept * 0.3 + surpriseBonus * 0.2
A* COST MODIFIERS:
- Cover tiles: cost 1.5 (preferred by flanking guard)
- Light tiles: cost 3.0 (avoided by sneaking player)
- Noise trigger tiles: cost 2.0
- Default: 1.0
State transitions: PATROL -> SUSPICIOUS on noise event. SUSPICIOUS -> ALERT on player sight. ALERT -> PATROL after 60s with no contact. Each transition has cooldown 1.5s to prevent flicker.
RESULT: 3-tier behavior tree, 9 leaf actions, 3 utility-scored sub-trees, dynamic difficulty with 3 tiers, A* with 4 terrain cost modifiers, FSM guard with 3 states + cooldowns. Ready for engine integration.