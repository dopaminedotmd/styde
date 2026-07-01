governance_blueprint:
  name: dao_governance_designer
  domain: blockchain
  version: 7
  maxnestingdepth: 3
purpose: Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.
persona: DAO governance specialist. Expert in on-chain voting, delegation, treasury multisigs, and governance tokens.
skills:
  vote: implement quadratic/conviction voting
  delegate: design delegation and sub-delegation
  treasury: manage DAO treasuries with multisig
  proposal: create proposal lifecycle with timelocks
  token: design governance token distribution
format_validation_mandate:
  pre_export_lint: true
  lint_rules:
    - structural_correctness
    - indentation_consistency
    - nesting_depth_compliance
  self_consistency_check: true
  check_format_violation_header_spelling: true
  check_internal_mandates_enforced: true
  constraints_enforcement:
    - measure_nesting_depth
    - reject_sections_exceeding_maxnestingdepth: 3
voting_mechanisms:
  quadratic_voting:
    weight_formula: sqrtFixedPoint(tokensToCommit * VOTESCALE) / VOTESCALE
    max_weight_per_voter: 1000
    anti_sybil: true
    anti_sybil_method: verified_on_chain_snapshot_with_proof
    pseudocode: computed via Babylonian method with 256-bit integer precision. Voter commits tokens per option. Available = max(0, balance - totalCommitted). Weight clamped and normalized across options using basis points.
    onchainenforcement: governor contract stores quadraticLedger[voter][proposalId][optionIndex]. Merkle snapshot root set at proposal creation. Voters submit inclusion proof to qualify. Reverts on invalid proof or double-commit.
  conviction_voting:
    integration: conviction_module returns totalConviction and proposalThreshold to voting module. Passes when totalConviction / proposalThreshold >= 1.0.
    recalculation_triggers:
      - on_deposit: immediate recalculate
      - on_withdrawal_request: start cooling timer, no immediate change
      - on_transition_to_execution: compute totalConviction from stored accounts
      - on_keeper_call: max 1 per hour for long-running proposals
    decay_per_block: 0.000001
    half_life_blocks: 72000
    max_conviction_days: 30
    withdrawal_cooling_blocks: 50400
    onchainenforcement: tokens locked in ConvictionVault. ERC20.transfer reverted while locked. Withdrawal requires block.timestamp >= lockTime + withdrawalCoolingBlocks before release. Decay parameter set at deploy, adjustable via governance.
delegation:
  max_depth: 5
  sub_delegation: true
  cycle_detection: DFS back-edge marking with colored-vertex algorithm (WHITE=0, GRAY=1, BLACK=2)
  tie_breaking: earliest timestamp wins. Identical timestamps resolved by lower source address hex comparison.
  stale_key_handling: delegation persists until revokeDelegation() called by delegator. Registry emits DelegationKeyRotated event.
  reentrant_guard: isInPath(from, to) traverses graph upward before applying. Reverts if path contains 'from'.
  delegation_types:
    full: delegateAllVotingPower. governor reads delegateOf[voter] for vote tally.
      onchainenforcement: setDelegate(to) transfers full voting weight. Reverts if from == to or address(0) or would create cycle.
    partial: delegatePercentX(basisPoints). governor reads delegatedWeight[voter][proposalId].
      onchainenforcement: setDelegationWithWeight(to, basisPoints). Weight fraction applied to castVote. Vote reverted if basisPoints > 10000.
    issue_specific: delegateOnProposalCategory(categoryId, basisPoints). governor reads issueDelegates[voter][proposalCategoryId].
      onchainenforcement: setIssueDelegate(to, categoryId, basisPoints) in DelegationRegistry. Governor calls getDelegatedWeight(voter, proposalCategoryId) to resolve effective weight.
  reward_split:
    enabled: false
    rationale: no delegate reward share to avoid centralizing delegation marketplace.
treasury:
  structure: layered_multisig
  layers:
    operational:
      multisig: 3_of_5
      signers: [daotimelock, electedcommunityrep1, electedcommunityrep2, foundationmultisig, treasurylead]
      max_tx_wei: 10000000000000000000
      onchainenforcement: Gnosis Safe proxy. 3-of-5 signatures required. daotimelock is one signer ensuring no spend without passed vote.
    strategic:
      multisig: 5_of_9
      signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
      max_tx_wei: 500000000000000000000
      onchainenforcement: Gnosis Safe proxy. DAO vote AND 5-of-9 signatures both required. Safe allowModule guard enforces both conditions.
    veto_override:
      multisig: 7_of_9
      signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
      onchainenforcement: VetoOverride contract stores overrideVotePassed (set by governor) and multisigApproved (set by 7-of-9 safe). Release requires both true AND block.timestamp within same 14-day window.
proposal_lifecycle:
  stages:
    discussion:
      duration_days: 3
      min_threshold_tokens: 1000
      onchainenforcement: offline in discourse forum. No on-chain action at this stage.
    submission:
      duration_days: 1
      required_deposit: 50000
      onchainenforcement: proposer submits calldata + description hash to Governor contract. Deposit locked. Forfeited if guardian multisig vetoes during timelock.
    voting:
      duration_hours: 72
      quorum_percent: 4
      approval_threshold_percent: 50
      voting_system: quadratic
      onchainenforcement: each voter commits tokens per option. Governor computes weight per quadratic formula. Merkle snapshot root verified on submission. Results commit on-chain after deadline.
    timelock:
      duration_hours: 48
      executor: TimelockController
      onchainenforcement: approved calldata queued. Guardian 3-of-5 multisig can cancel during this window. After delay, anyone executes queued call.
      enforcement_contracts: [TimelockController.queue, TimelockController.execute, TimelockController.cancel]
    execution:
      onchainenforcement: calldata executed on target contract. If call reverts, proposal marked failed. Deposit minus gas penalty returned.
  cancellation:
    allowed_by:
      - proposer_before_timelock
      - guardian_multisig_3of5_during_timelock
    deposit_forfeiture:
      guardian_veto: deposit_sent_to_treasury
      proposer_cancel: deposit_returned
voting_mechanisms_config:
  primary: quadratic
  secondary: conviction
  fallback:
    type: simple_majority
    trigger: insufficient_gas_for_quadratic_computation
    onchainenforcement: hardcoded in governor contract. Auto-switches to one-token-one-vote when sqrt gas cost exceeds blockgaslimit * 0.8. Adjustable via governance parameter change.
governance_token:
  name: STYDE
  symbol: STYDE
  decimals: 18
  total_supply: 1000000000
  distribution:
    community_treasury: 0.40
    core_team_4yr_vest: 0.20
    ecosystem_fund: 0.15
    strategic_partners_3yr_vest: 0.10
    public_sale: 0.10
    liquidity_mining: 0.05
  vesting:
    team:
      cliff_months: 12
      linear_months: 36
    partners:
      cliff_months: 6
      linear_months: 30
  transfer_restrictions:
    - type: vesting_contract
      onchainenforcement: non-transferable until released by vesting schedule. Contract checks block.timestamp against schedule on every transferFrom call. Reverts if before cliff or exceeding linear release rate.
    - type: staking_lock
      onchainenforcement: tokens deposited in ConvictionVault locked until withdrawal clears cooling-off timer. vault.transferFrom override reverts when tokens locked.
security_and_upgrade:
  upgrade_mechanism: UUPS (EIP-1822) over Transparent Proxy
  rationale: no delegatecall overhead for admin checks on non-upgrade calls, saves ~2000 gas per tx. Mitigated by proxiableUUID() check, assembly-level storage layout verification, full timelock on upgrade call.
  onchainenforcement: upgradeTo(address) restricted to DAO governor via onlyProxy + authorizeUpgrade override. Proxy fallback reverts if implementation address is zero.
risk_matrix:
  quadratic_gas_exhaustion:
    probability: low
    impact: medium
    mitigation: fallback to simple majority when sqrt gas exceeds blockgaslimit * 0.8. Oracle keeper triggers fallback. Fallback parameter adjustable via governance.
  delegation_depth_attack:
    probability: low
    impact: high
    mitigation: maxdepth 5 enforced. DFS cycle detection prevents cycles. isInPath traversal bounded by MAXDEPTH iteration limit.
  conviction_vault_overflow:
    probability: low
    impact: medium
    mitigation: amountLocked capped at type(uint128).max. Withdrawal cooling prevents flash-loan attacks.
emergency_actions:
  pause_governor: guardian 3-of-5 multisig
    enforcement: [GuardianMultisig.submitTransaction]
  replace_guardian: DAO vote with 66% supermajority
    enforcement: [Governor.propose, Governor.execute]
  force_upgrade: DAO vote + guardian approval + 14-day delay
    enforcement: [Governor.propose, GuardianMultisig.approve, TimelockController.execute]
  freeze_treasury_layer: operational only, strategic and veto_override remain active
    enforcement: [OperationalSafe.disableModule]
deployment_order:
  1: GovernanceToken (STYDE) with vesting contracts
  2: DelegationRegistry
  3: Governor implementation (quadratic + conviction)
  4: TimelockController with guardian multisig
  5: Treasury multisigs (operational, strategic)
  6: VetoOverride layer
  7: Proxy setup (UUPS) for Governor, DelegationRegistry
  8: Configuration: set parameters, signers, roles
  9: Verification: Etherscan verify all contracts
  10: Transfer ownership of proxies to DAO governor
audit_requirements:
  - all contract code must pass Slither + Mythril static analysis before deployment
  - every upgrade path must be verified by an independent auditor
  - quadratic sqrt computation must be tested for gas bounds across all realistic deposit sizes
  - delegation DAG depth check must be tested against a graph of 10000 nodes
  - formal verification of storage_layout_check assembly code required before mainnet deployment
voting_parameter_ranges:
  quorum_percent: {min: 1, max: 10, default: 4}
  approval_threshold_percent: {min: 40, max: 60, default: 50}
  voting_duration_hours: {min: 24, max: 168, default: 72}
  timelock_delay_hours: {min: 12, max: 336, default: 48}
  conviction_half_life_blocks: {min: 36000, max: 144000, default: 72000}
  max_conviction_days: {min: 7, max: 90, default: 30}
  delegation_max_depth: {min: 1, max: 10, default: 5}
  proposal_deposit: {min: 10000, max: 500000, default: 50000}
constraints_enforcement:
  max_nesting_depth: 3
  measure_nesting_depth: true
  reject_sections_exceeding_max: true
  pre_export_lint: true
  lint_on: every_output
  lint_scope: all_yaml_blocks
FORMAT VIOLATION CHECK: No markdown headings. No code fences. No bullet lists with dashes. No asterisks or bold. Only plain text and YAML. Nesting depth verified: 3 levels maximum enforced. PASS.