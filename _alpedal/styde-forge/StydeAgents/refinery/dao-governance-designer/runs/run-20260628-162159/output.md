Dao Governance Design — Complete Specification
governance_design:
  name: Stryde DAO Framework
  chain: EVM-compatible (Ethereum, Polygon, Arbitrum)
  framework: OpenZeppelin Governor + custom extensions
token:
  name: STRYDE
  supply: 100,000,000
  distribution:
    - category: Community Treasury
      allocation: 40,000,000
      mechanism: vesting over 48 months, linear unlock
    - category: Core Contributors
      allocation: 20,000,000
      mechanism: 12-month cliff, 36-month linear vest
    - category: Strategic Investors
      allocation: 15,000,000
      mechanism: 6-month cliff, 24-month linear vest
    - category: Ecosystem / Grants
      allocation: 15,000,000
      mechanism: DAO-controlled, milestone-based via governance
    - category: Liquidity Provision
      allocation: 10,000,000
      mechanism: deployed to DEX pools, managed by treasury
  governance_role: ERC20Votes — each token = 1 voting power
  anti_concentration:
    - whalecap: votes beyond 4% of total supply are discounted exponentially
    - cooldown: tokens must be held 7 days before voting
voting:
  primary: quadratic voting
    formula: cost_in_vp = (votes_cast)^2
      - cast 1 vote = pay 1 VP
      - cast 10 votes = pay 100 VP
      - cast 100 votes = pay 10,000 VP
    implementation: merkle-tree snapshot of token holdings at proposal creation
    gas_optimization: allow batch signature verification
  secondary: conviction voting (for treasury allocation proposals only)
    formula: voting_power = tokens_staked * sqrt(time_staked_days / 90)
    - conviction builds over 90 days to max
    - withdrawal during active conviction resets timer
    - conviction decays passively if no new vote cast within 30 days
  threshold:
    quorum: 4% of circulating supply must vote
    approval: majority wins (simple majority for standard, supermajority 66% for treasury/pause)
    min_voting_period: 3 days
    max_voting_period: 7 days
delegation:
  model: liquid delegation with sub-delegation chains
  delegator_action:
    - delegate to any address (EOA or contract)
    - split delegation: allocate % to different delegates
    - override: delegator always can override delegate's vote on specific proposal
  sub_delegation:
    - depth: max 3 hops (A -> B -> C -> D votes)
    - power_passthrough: 100% of original VP passes through each hop
    - revocable: any node can revoke delegation to their sub-delegate at any time
  delegation_expiry:
    - auto-expire after 180 days of inactivity
    - must re-delegate or vote to renew
    - expiry does not affect past votes — only future
  reputation_staking:
    - delegates can stake STRYDE tokens to signal commitment
    - staked delegates appear higher in discovery UI
    - slashing: delegate who votes against their stated platform loses reputation score
proposal_lifecycle:
  stages:
    - stage: Draft
      condition: proposer holds >= 100,000 STRYDE (0.1%)
      action: submit proposal text + parameters on-chain
      gas: proposer pays
    - stage: SigCheck
      condition: 5 community members sign supporting signature
      action: proposal moves to discussion queue
      deadline: 7 days to collect sigs, else expired
    - stage: Discussion
      duration: minimum 48 hours on-chain discussion period
      action: forum link mandatory, on-chain comments optional
    - stage: Voting
      duration: 3-7 days (set at proposal creation)
      action: token holders cast votes via quadratic mechanism
    - stage: Timelock
      duration: 48 hours
      action: after vote passes, queued in TimelockController
      cancel_window: first 24 hours of timelock — cancel by governance vote (66%)
    - stage: Executed
      action: anyone can call execute() after timelock expires
    - stage: Failed
      condition: quorum not met OR majority against OR defeated in timelock
      proposer_penalty: 1% of stake slashed for spam proposals (below 10% quorum)
  proposal_categories:
    - type: Standard
      threshold: 100,000 tokens
      quorum: 4%
      approval: majority
      timelock: 48h
    - type: Treasury
      threshold: 500,000 tokens
      quorum: 6%
      approval: 66% supermajority
      timelock: 72h
    - type: Emergency
      threshold: 1,000,000 tokens
      quorum: 8%
      approval: 75% supermajority
      timelock: 0h (immediate)
      restriction: only pause/unpause, no treasury drain
    - type: Parameter
      threshold: 50,000 tokens
      quorum: 3%
      approval: majority
      timelock: 24h
      scope: voting params, thresholds, quorum only
treasury_multisig:
  signers: 7
  threshold: 4 of 7
  signer_rotation:
    - DAO votes to add/remove signers via Standard proposal
    - timelock applies before signer change executes
  spending_limits:
    - tier1 (no vote): up to 10,000 STRYDE — any 2 multisig signers
    - tier2 (rapid): up to 100,000 STRYDE — 4 of 7 multisig + on-chain vote waiver (emergency)
    - tier3 (governance): any amount — requires standard governance proposal + timelock
  treasury_assets: STRYDE tokens, stablecoins, LP tokens, NFTs
  streaming: integrate Superfluid or Sablier for continuous grants
  safety_valve:
    - circuit_breaker: if 3 signers call pause, treasury freezes for 48 hours
    - unpause: requires governance vote or 6 of 7 signers
security:
  timelock_controller:
    min_delay: 24 hours (standard operations)
    max_delay: 30 days (critical upgrades)
    executor_role: anyone can call execute after delay
    canceller_role: governance (66% vote)
    proposer_role: governance (Standard proposal)
  upgradeability:
    - proxy pattern with explicit upgrade delay (7 days)
    - upgrade must pass Standard proposal + timelock
    - emergency upgrades require 75% supermajority + 4 of 7 multisig ratify
  emergency_pause:
    - governor and multisig both can pause
    - pause_duration: max 7 days
    - auto-resume: paused execution resumes automatically after expiry
user_flow:
  1. User acquires STRYDE tokens (DEX, vesting, or grant)
  2. User delegates voting power to a delegate or self
  3. Delegated VP accumulates: 100 tokens held for 7 days = 100 VP
  4. Proposal creation: hold 0.1% supply -> write proposal -> submit with stake
  5. Voting phase: user votes — quadratic cost applies
     - vote YES once = 1 VP consumed (casts 1 unit of voting power)
     - vote YES 10 times = 100 VP consumed (casts 10 units)
     - casting more votes = exponentially costlier
  6. Proposal passes -> enters timelock -> anyone executes after delay
  7. Treasury spend goes through conviction voting or standard vote
  8. Multisig monitors and can pause in emergency
contract_stack:
  - StrydeToken.sol: ERC20 + ERC20Votes + whalecap
  - StrydeGovernor.sol: OpenZeppelin Governor + quadratic extension
  - StrydeQuadraticVote.sol: custom module for quadratic cost function
  - StrydeDelegation.sol: liquid delegation with sub-delegation chain
  - StrydeConvictionVault.sol: time-weighted voting for treasury
  - StrydeTimelockController.sol: OpenZeppelin TimelockController
  - StrydeTreasury.sol: multisig + DAO-controlled streaming
  - StrydeCircuitBreaker.sol: pause/resume guardian
metrics_to_track:
  - voter_participation_rate (% of supply voting per proposal)
  - delegate_health_score (active delegates vs zombie delegates)
  - proposal_pass_rate (% of proposals passing)
  - treasury_utilization (% of treasury deployed vs idle)
  - quadratic_efficiency (are whales still dominating? measure gini of voting power)
  - delegation_depth_distribution (% direct vs 1-hop vs 2-hop vs 3-hop)
  - timelock_bypass_rate (how many emergency proposals bypass full timelock)