domain: gaming
version: 1
purpose: patrol-and-combat NPC AI combining behavior trees, pathfinding, FSM states, utility scoring, and dynamic difficulty
persona: game AI designer
blueprint: npc_guardian_ai
behavior_tree: npc_root
  selector:
    - sequence: combat_priority
      - condition: enemy_in_range
      - action: face_target
      - selector: combat_action
        - condition: hp_low
        - action: flee_to_cover
        - condition: ammo_low
        - action: retreat_reload
        - utility_scorer: best_attack
          - option: burst_fire
            weight: 0.35
          - option: flank_throw_grenade
            weight: 0.30
          - option: suppress_advance
            weight: 0.20
          - option: charge_melee
            weight: 0.15
    - sequence: alert_state
      - condition: suspicious_noise
      - action: investigate_point
      - timer: 8s
      - action: return_to_patrol
    - sequence: patrol_state
      - action: traverse_path
        - nodes: patrol_waypoints
        - mode: loop
      - action: idle_scan
        - duration: random(2,5)
fsm: npc_state_machine
  states:
    idle:
      entry: play_animation idle
      update: check_threats
      exit: reset_awareness
    patrol:
      entry: set_destination nearest_waypoint
      update: move_along_path, spawn_random_comment
      transition_to_alert: on_sound_detected
      transition_to_combat: on_enemy_visible
    investigate:
      entry: lock_destination noise_origin
      update: move_toward, scan_on_arrival
      transition_to_patrol: after_investigate_complete
      transition_to_combat: on_enemy_found
    combat:
      entry: draw_weapon, enter_cover
      update: utility_decide_action
      transition_to_patrol: enemy_lost + cooldown_expired(15s)
      transition_to_flee: hp_below(25%)
pathfinding: improved_a_star
  grid: 0.5m x 0.5m cell
  heuristic: octile_distance
  optimisation:
    - jump_point_search: true
    - dynamic_obstacle_repulsion: 1.5m radius
    - corridor_smoothing: 3-iteration string_pulling
  navmesh:
    - generation: auto_voxel_agent_radius_0.4m
    - rasterisation: walkable_slope_under_45_deg
    - links: jump_links_max_2m, climb_links_max_3m
dynamic_difficulty: player_skill_matcher
  metrics:
    - ttk_ratio: observed_time_to_kill / expected_ttk
    - hit_rate: player_accuracy_baseline_70% +- 20%
    - death_count: deaths_per_encounter
  adjustments:
    ttk_ratio < 0.6: amplify_aggression
      - perception_multiplier: 1.4x
      - combat_reaction_delay_ms: 100 (was 400)
      - cover_use_frequency: 80% (was 40%)
    ttk_ratio between 0.6 and 1.2: balanced
      - default_params
    ttk_ratio > 1.2: handicap_npc
      - aim_noise_degrees: 2.5 (was 0)
      - attack_cooldown_bonus_ms: +500
      - telegraph_intensity: high (telegraphed tells on heavy attacks)
    death_count > 3_in_last_5_minutes: mercy_mode
      - spawn_health_packs_on_npc_death: true
      - reduce_flanking: true
      - increase_reaction_ms: +200
utility_scorer: best_attack
  considerations:
    burst_fire:
      distance_to_target:
        curve: bell_peak_at_10m
        score: 0.8 at 8-15m
      cover_quality:
        curve: inverse_linear
        score: 0.9 when exposed
    flank_throw_grenade:
      allies_near_target:
        curve: step_0_above_2
        score: 1.0 if allies >= 3
      own_hp:
        curve: above_0.5
        score: 0.7 when hp > 50%
    suppress_advance:
      target_moving_toward:
        curve: linear_rising
        score: 1.0 when closing distance
      ammo_count:
        curve: above_10
        score: 0.8 when ammo > 10
    charge_melee:
      distance_to_target:
        curve: under_5m
        score: 0.9 at melee range
      own_hp:
        curve: above_0.7
        score: 0.6 when hp > 70%
implementation_notes:
  language: C++ with Unreal Engine 5 Behavior Tree / C# with Unity NavMesh
  patterns: observer for difficulty adjustments, strategy pattern for utility options, composite pattern for BT nodes
  edge_cases:
    - if navmesh fails to generate on dynamic obstacle: fallback to A* on 2D grid
    - if utility_scorer returns all scores below 0.15: default to flee
    - if player is invisible but making noise: investigate state, not combat
    - if multiple enemies share target: spread utility noise to prevent all choosing flank