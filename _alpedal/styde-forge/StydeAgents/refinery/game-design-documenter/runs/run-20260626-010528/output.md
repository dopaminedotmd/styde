CAVEMAN ULTRA MODE ACTIVE
No task specified beyond loading blueprint. Providing GDD framework and sample design.
SAMPLE GAME CONCEPT: ECHO CORE
GDD HEADER
title: Echo Core
genre: Action Roguelite / Rhythm
platform: PC (Steam)
target audience: 25-40, roguelite veterans, rhythm game enjoyers
core hook: Movement and attacks are bound to music beat. Every run generates a unique procedural soundtrack.
CORE MECHANICS LOOP
player state:
- health pool
- stamina pool (recharges on beat)
- rhythm sync meter (0-100%)
- equipped abilities (max 4)
game loop:
  1. enter floor -> music track generated from seed
  2. enemies spawn on beat intervals
  3. player actions cost stamina (recharges every beat)
  4. perfect timing (on-beat) deals 2x damage + restores rhythm meter
  5. off-beat actions cost 50% more stamina, deal 0.5x damage
  6. rhythm meter full -> trigger crescendo (screen clear AoE)
  7. clear room -> choose reward (3 cards)
  8. repeat until boss floor -> defeat boss -> progress or die -> restart
BALANCE SPREADSHEET (values per difficulty tier)
difficulty: Normal
enemy_hp_multiplier: 1.0
enemy_damage_multiplier: 1.0
stamina_regen_rate: 30
rhythm_window_ms: 200
floor_count: 4
heal_per_room: 20
difficulty: Hard
enemy_hp_multiplier: 1.5
enemy_damage_multiplier: 1.3
stamina_regen_rate: 25
rhythm_window_ms: 150
floor_count: 6
heal_per_room: 15
difficulty: Echo
enemy_hp_multiplier: 2.5
enemy_damage_multiplier: 2.0
stamina_regen_rate: 20
rhythm_window_ms: 100
floor_count: 8
heal_per_room: 10
PROGRESSION SYSTEM
meta-progression (persistent across runs):
- shards earned per run (spent in hub)
- unlockable characters (5 base, 3 secret)
- ability pool grows with shard purchases
- difficulty tiers unlocked by clearing previous tier
- echo resonance: permanent stat bonuses (capped)
per-run progression:
- floor 1-2: basic enemies, 2 reward choices
- floor 3-4: elite enemies, 3 reward choices
- floor 5-6: mixed elites + mini-boss, 4 reward choices
- boss floors: unique boss mechanics synced to music
reward pool (card draft after each room):
- common (60%): stat boosts, single-use items
- rare (30%): new abilities, passive modifiers
- legendary (10%): game-changing effects, extra ability slot
PLAYER PSYCHOLOGY
extrinsic motivators:
- shard economy with visible progress bar
- unlockable cosmetics (skins, sound packs, visualizers)
- achievement system (50 achievements)
- leaderboards (score = damage dealt * rhythm accuracy multiplier)
intrinsic motivators:
- flow state via beat-synced gameplay
- mastery through rhythm precision
- discovery via procedural music generation
- autonomy via build customization
retention hooks:
- daily challenge (fixed seed, leaderboard)
- weekly mutation (modifiers change rules)
- endless mode (survive as long as possible, increasing BPM)
engagement patterns:
- loss aversion: 50% shard retention on death
- variable rewards: room completion lottery (bonus shards)
- sunk cost: meta-progression is per-character
- curiosity gap: next ability card face-down until selection