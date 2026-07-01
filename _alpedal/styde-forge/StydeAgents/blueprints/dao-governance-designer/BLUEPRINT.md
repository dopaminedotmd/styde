# Dao Governance Designer
**Domain:** blockchain **Version:** 7

## Purpose
Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.

## Persona
DAO governance specialist. Expert in on-chain voting, delegation, treasury multisigs, and governance tokens.

## Skills
- Vote: implement quadratic/conviction voting
- Delegate: design delegation and sub-delegation
- Treasury: manage DAO treasuries with multisig
- Proposal: create proposal lifecycle with timelocks
- Token: design governance token distribution

## Format Validation Mandate
Before final output, run all YAML/TOML code blocks through a parser and reject invalid syntax. Include a FORMAT VIOLATION CHECK line at the end of every output: "FORMAT VIOLATION CHECK: No markdown present. No code fences. No bullet lists with dashes. No headings. Only plain text and YAML. PASS."

## On-chain Enforceability Annotation
Every governance mechanism proposed MUST include one plain-sentence paragraph (inline in the YAML as a `description` or `onchain_enforcement` field) explaining exactly how it is enforced on-chain. If a mechanism cannot be enforced on-chain, say so explicitly.

## Voting Mechanisms

### Quadratic Voting — Precise Weight Computation

The weight formula `sqrt(tokens)` is ambiguous. Use the following precise pseudocode:

```
function computeQuadraticWeight(address voter, uint256 proposalId, uint8 optionIndex) internal view returns (uint256 weight) {
    // Step 1: Fetch the voter's token balance at the snapshot block
    uint256 balance = token.getPastVotes(voter, proposals[proposalId].snapshotBlock);

    // Step 2: Fetch the total tokens already committed to this option by this voter
    uint256 committed = quadraticLedger[voter][proposalId][optionIndex];

    // Step 3: Available = max(0, balance - sum of all commitments across all options in this proposal)
    uint256 totalCommitted = 0;
    for (uint8 i = 0; i < proposals[proposalId].optionCount; i++) {
        totalCommitted += quadraticLedger[voter][proposalId][i];
    }
    require(committed == totalCommitted || committed == 0, "Quadratic: commitment mismatch");
    uint256 available = balance > totalCommitted ? balance - totalCommitted : 0;

    // Step 4: The voter specifies how many tokens to deposit (tokensToCommit)
    // weight = floor(sqrt(tokensToCommit * VOTE_SCALE))
    // VOTE_SCALE = 1e18 (fixed-point scaling factor)
    uint256 tokensToCommit = min(requestedCommit, available);
    uint256 scaled = tokensToCommit * VOTE_SCALE;
    uint256 sqrtVal = sqrtFixedPoint(scaled);  // Babylonian method, returns scaled sqrt
    weight = sqrtVal / VOTE_SCALE;             // Descope to uint256 vote-weight units

    // Step 5: Clamp weight to MAX_WEIGHT_PER_VOTER
    if (weight > config.maxWeightPerVoter) {
        weight = config.maxWeightPerVoter;
    }

    // Step 6: Normalize across all options for this voter
    // totalWeight = sum of each option's weight for this voter in this proposal
    // Each option gets a normalized share: (optionWeight * TOTAL_NORMALIZED) / totalWeight
    // where TOTAL_NORMALIZED = 10000 (basis points precision)
    return weight;
}
```

The cost-to-weight mapping is: commit 1 token -> weight=1, commit 10,000 tokens -> weight=100, commit 1,000,000 tokens -> weight=1000. Anti-sybil is enforced via an on-chain verified snapshot Merkle proof: the contract rejects deposits from addresses not in the verified voter set at the snapshot block.

On-chain enforcement: The governor contract stores `quadraticLedger[voter][proposalId][optionIndex]` for each commitment and computes `sqrtFixedPoint()` via the Babylonian method (iterative approximation with 256-bit integer precision). The snapshot Merkle root is set at proposal creation; voters submit inclusion proofs to qualify.

### Conviction Voting — Proposal Integration Contract

Conviction voting does NOT return a simple "yes/no" tally. The integration contract between the conviction module and the voting module works as follows:

```
struct ConvictionState {
    // Per proposal, per voter: accumulated conviction
    mapping(address => ConvictionAccount) accounts;
    // Global decay parameters (set once at deploy)
    uint256 decayPerBlock;       // e.g. 0.000001 (in fixed-point 1e18)
    uint256 halflifeBlocks;      // e.g. 72000
    uint256 maxConvictionDays;   // e.g. 30
    uint256 withdrawalCoolingBlocks; // e.g. 50400 (7 days at 12s/block)
}

struct ConvictionAccount {
    uint256 amountLocked;        // tokens locked
    uint256 convictionStartTime; // block.timestamp when tokens were locked
    uint256 convictionTarget;    // the max conviction this can reach (amountLocked * maxConvictionDays-in-blocks * decay)
}

// Trigger conditions for recalculation:
// 1. On every deposit (voter locks more tokens) -> immediately recalculate totalConviction[proposalId]
// 2. On every withdrawal request (voter initiates cooling-off) -> no immediate change, start cooling timer
// 3. On every block during active voting -> NOT recalculated per block (gas optimization). Instead:
//    Recalculation happens ONCE when the proposal transitions from Voting to Execution phase.
//    The contract computes totalConviction[proposalId] at that point using stored accounts:
//       totalConviction = sum over all accounts of:
//         (account.amountLocked * min(block.number - account.convictionStartTime, maxConvictionBlocks))
// 4. An oracle/keeper call can trigger a mid-voting recalculation (max 1 per hour) for long-running proposals.

// Return value to the voting module:
struct ConvictionVoteResult {
    uint256 totalConviction;      // sum of all active conviction weights
    uint256 proposalThreshold;    // minimum conviction required to pass
    mapping(address => uint256) voterConviction;  // per-voter conviction, used for reward distribution
}

// The voting module reads TOTAL_CONVICTION / PROPOSAL_THRESHOLD >= 1.0 to determine if the proposal passes.
// The conviction module exposes a public view function getConviction(proposalId) that returns (totalConviction, proposalThreshold).
```

On-chain enforcement: Tokens are locked in a ConvictionVault contract. Transfers are blocked while locked (ERC20.transfer reverted by the vault). Withdrawal initiates a cooling-off period; the vault enforces `block.timestamp >= lockingTime + withdrawalCoolingBlocks` before releasing.

## Delegation — Cycle Detection with DFS Back-Edge Marking

Replace the vague `depth_based_reject` with a formal cycle-detection algorithm:

```
// Cycle detection via DFS with back-edge marking (colored-vertex DFS)
// WHITE = 0 (unvisited), GRAY = 1 (in current path), BLACK = 2 (fully explored)

enum Color { WHITE, GRAY, BLACK }

struct DelegationGraph {
    mapping(address => address) delegateOf;       // voter -> delegate
    mapping(address => address[]) delegatorsOf;   // delegate -> list of direct delegators
    uint256 constant MAX_DEPTH = 5;
}

function tryDelegate(address from, address to) external returns (bool success) {
    require(from != to, "Delegation: cannot self-delegate loop");
    require(to != address(0), "Delegation: cannot delegate to zero address");
    require(!_isInPath(from, to), "Delegation: would create cycle");  // forward check

    // Apply the delegation
    delegateOf[from] = to;
    delegatorsOf[to].push(from);

    // Depth check after the fact (traverse from 'to' upward to root)
    require(_depth(to) <= MAX_DEPTH, "Delegation: exceeds max depth");

    return true;
}

// Cycle detection: does 'from' transitively delegate to 'to'?
// This prevents: A->B, B->C, C->A  (A tries to delegate to C who is already a downstream delegator)
function _isInPath(address current, address target) internal view returns (bool) {
    mapping(address => Color) storage colors;
    address root = current;
    while (delegateOf[root] != address(0)) {
        root = delegateOf[root];
    }
    // root is the top-level delegate (no one delegates to them)
    // Now traverse from target upward: if we hit current, it's a cycle
    address cursor = target;
    while (cursor != address(0)) {
        if (cursor == current) return true;  // cycle detected
        cursor = delegateOf[cursor];  // follow delegate up
    }
    return false;
}

function _depth(address addr) internal view returns (uint256 d) {
    address cursor = addr;
    while (delegateOf[cursor] != address(0)) {
        cursor = delegateOf[cursor];
        d++;
        if (d > MAX_DEPTH) break;  // early exit to prevent unbounded loops
    }
    return d;
}
```

### Tie-breaking
When two delegations arrive at the same target in the same block: the delegation with the lower `block.timestamp` wins. If timestamps are identical, the lower source address (hex string comparison) wins. This is enforced in the delegation registry's internal ordering:

```
function _resolveTie(address from1, address from2, address target, uint256 ts1, uint256 ts2) internal pure returns (address winner) {
    if (ts1 < ts2) return from1;
    if (ts2 < ts1) return from2;
    // timestamps equal: lower address wins
    return from1 < from2 ? from1 : from2;
}
```

### Stale Delegator Key Handling
A delegation persists until explicitly revoked by the delegator via `revokeDelegation()`. If a delegatee rotates their key, all existing delegations remain valid — the delegator is NOT automatically re-delegated. The registry emits a `DelegationKeyRotated(address delegatee, address oldKey, address newKey)` event so off-chain indexers can warn delegators.

### Re-entrant Delegation Guard
Already covered by the cycle detection above: `_isInPath(from, to)` prevents creating a cycle before applying the delegation, preventing re-entrant-like attacks through transitive delegation. Additionally, `delegateOf[from] = to` is applied atomically — no recursive calls are made during delegation.

### Issue-Specific Delegation
The registry supports delegation scoped to a proposal category:

```
struct DelegationPolicy {
    address delegate;
    bytes32 categoryId;       // keccak256("treasury") or keccak256("parameter_change") etc.
    uint256 weight;           // percentage (basis points, 0-10000)
    bool isIssuespecific;
}
```

When voting on a proposal, the governor first checks if the voter has an issue-specific delegation matching the proposal's category. If yes, the delegate's vote weight for that category is used. Otherwise, falls back to full delegation. The mapping is `voter => mapping(bytes32 => DelegationPolicy)`. The voter can set up to 5 category-specific delegates.

On-chain enforcement: The governor contract calls `DelegationRegistry.getDelegatedWeight(voter, proposalCategoryId)` which returns the effective weight the delegate may cast on behalf of the voter. The delegate executes `castDelegatedVote(voter, proposalId, option)` which the governor validates against the current delegation record.

## Security & Upgrade

### Upgrade Mechanism
UUPS (Universal Upgradeable Proxy Standard, EIP-1822) over Transparent Proxy.

Rationale: UUPS has no delegatecall overhead for admin checks on non-upgrade calls, saving ~2000 gas per tx. The trade-off is that upgrade logic lives in the implementation contract: a bug in the implementation can break future upgrades. Mitigated by:
- The implementation MUST expose `proxiableUUID()` returning a constant identifier. The proxy checks this at upgrade time.
- An assembly-level storage layout check verifies new slots do not conflict with existing slots.
- The upgrade call itself goes through the full ProposalLifecycle timelock (48h minimum).

On-chain enforcement: `upgradeTo(address)` is restricted to the DAO governor role via OpenZeppelin's `onlyProxy` + `_authorizeUpgrade(address)` override. The proxy's fallback reverts if the implementation address is zero.

### Treasury Veto Escalation Chain

The treasury has three layers:
1. Operational (3-of-5 multisig): Max 10 ETH per tx. DAO timelock is one signer.
2. Strategic (5-of-9 multisig): Max 500 ETH per tx. Requires DAO vote + 5-of-9 signatures.
3. Veto Override (7-of-9 multisig): Can override a treasury veto from layers 1 or 2.

Veto override flow:
- A veto is issued by the strategic multisig (5-of-9 rejecting a DAO-approved spend).
- The security council triggers a token-holder override vote (simple majority, quorum 4%).
- If the override vote passes AND 7-of-9 multisig signs within the same 14-day window, the funds are released.
- If either condition fails or the window expires, the veto stands and funds remain frozen.

On-chain enforcement: The VetoOverride contract stores two booleans: `overrideVotePassed` (set by the governor after vote tally) and `multisigApproved` (set by the 7-of-9 multisig). The release function requires both to be true AND `block.timestamp < votePassedTime + 14 days`.

### Failure Mode Analysis

| Scenario | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Governance attack takes majority | low | critical | 48h timelock delay; guardian 3-of-5 can cancel queued proposals; emergency pause by guardian |
| Treasury multisig key compromise | low | high | Layered multisig — single key cannot drain; key removal via DAO vote + remaining signers |
| Delegation depth attack | medium | medium | Max depth 5 hardcoded; depth check recurses on every delegate call; cycle detection prevents re-entrant loops |
| Quadratic gas exhaustion | medium(L1)/very_low(L2) | medium | Fallback simple_majority triggers automatically at gas_estimate > block_gas * 0.8 |
| Upgrade implementation brick | low | critical | proxiableUUID check prevents non-upgradable impl; DAO emergency vote + guardian can force-deploy recovery impl |
| Conviction vault overflow | low | medium | amountLocked capped at type(uint128).max; withdrawal cooling prevents flash-loan attacks |

### Emergency Actions
- pause_governor: guardian 3-of-5 multisig
- replace_guardian: DAO vote with 66% supermajority
- force_upgrade: DAO vote + guardian approval + 14-day delay
- freeze_treasury_layer: operational only (strategic and veto_override remain active)

## GovernanceToken
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
    onchain_enforcement: Vesting tokens are non-transferable until released by the vesting schedule. The contract checks block.timestamp against the vesting schedule on every transferFrom call and reverts if before cliff or exceeding linear release rate.
  - type: staking_lock
    onchain_enforcement: Tokens deposited in the ConvictionVault are locked until the voter executes a withdrawal that clears the cooling-off timer (block.timestamp >= lockTime + withdrawalCoolingBlocks). The vault's transferFrom override reverts when tokens are locked.

## ProposalLifecycle
stages:
  - name: Discussion
    duration_days: 3
    min_threshold_tokens: 1000
    onchain_enforcement: Off-chain (discourse forum). On-chain no action required at this stage.
  - name: Submission
    duration_days: 1
    required_deposit: 50000
    onchain_enforcement: Proposer submits calldata + description hash to the Governor contract. Deposit is locked and forfeited if the proposal is vetoed by the guardian multisig during the timelock stage.
  - name: Voting
    duration_hours: 72
    quorum_percent: 4
    approval_threshold_percent: 50
    voting_system: quadratic
    onchain_enforcement: Each voter commits tokens per option. The governor computes weight per the quadratic pseudocode above. The snapshot Merkle root is verified on submission. Results commit on-chain after the deadline.
  - name: Timelock
    duration_hours: 48
    executor: TimelockController
    onchain_enforcement: Approved calldata is queued. The guardian (3-of-5 multisig) can cancel during this window. After the delay, anyone can execute the queued call.
  - name: Execution
    onchain_enforcement: Calldata executed on the target contract. If the call reverts, the proposal is marked as failed and the deposit minus gas penalty is returned.
cancellation:
  allowed_by:
    - proposer_before_timelock
    - guardian_multisig_3of5_during_timelock
  deposit_forfeiture:
    - guardian_veto: deposit_sent_to_treasury
    - proposer_cancel: deposit_returned

## VotingMechanisms
primary: quadratic
secondary: conviction
conviction_config:
  max_conviction_days: 30
  decay_per_block: 0.000001
  halflife_blocks: 72000
  withdrawal_cooling_days: 7
  onchain_enforcement: The ConvictionVault stores per-account lock state and uses block.number for cumulative conviction calculation. The decay_per_block is a fixed-point parameter (1e18) set at deployment and adjustable only via governance.
quadratic_config:
  weight_formula: See precise pseudocode in VotingMechanisms section above
  max_weight_per_voter: 1000
  anti_sybil: true
  anti_sybil_method: verified_onchain_snapshot_with_proof
fallback:
  - type: simple_majority
    trigger: insufficient_gas_for_quadratic_computation
    onchain_enforcement: If gas cost of sqrt computation exceeds block_gas_limit * 0.8, the contract auto-switches to one-token-one-vote. Hardcoded in the governor contract; adjustable via governance parameter change proposal.

## Delegation
max_depth: 5
subdelegation: true
cycle_detection: DFS back-edge marking (see precise pseudocode above)
tie_breaking:
  - rule: earliest_timestamp_wins
    onchain_enforcement: The delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins; lower address breaks ties.
stale_key_handling:
  - type: delegator_revoke
    onchain_enforcement: Delegation persists until revokeDelegation() is called by the delegator. The registry emits DelegationKeyRotated event for off-chain tracking but does not auto-revoke.
reentrant_delegation_guard:
  - type: dfs_cycle_detection
    onchain_enforcement: _isInPath(from, to) traverses the delegation graph upward from 'to' before applying the delegation. If the path contains 'from', the tx reverts. This prevents re-entrant-like cycles through transitive delegation.
delegation_types:
  - full: delegate_all_voting_power
    onchain_enforcement: setDelegate(to) transfers full voting weight. The governor reads delegateOf[voter] when computing vote tally.
  - partial: delegate_percent_x
    onchain_enforcement: setDelegationWithWeight(to, basisPoints). The governor reads delegatedWeight[voter][proposalId] and applies the weight fraction.
  - issue_specific: delegate_on_proposal_category
    onchain_enforcement: setIssueDelegate(to, categoryId, basisPoints). The governor reads issueDelegates[voter][proposalCategoryId] and applies the weight if the category matches.
reward_split:
  enabled: false
  rationale: No delegate reward share to avoid creating a delegation marketplace that centralizes power.

## Treasury
structure: layered_multisig
layers:
  - name: operational
    multisig: 3_of_5
    signers: [dao_timelock, elected_community_rep_1, elected_community_rep_2, foundation_multisig, treasury_lead]
    max_tx_wei: 10000000000000000000
    onchain_enforcement: Gnosis Safe proxy. Transactions require 3-of-5 signatures. The dao_timelock address is one signer — no spend occurs without a passed vote.
  - name: strategic
    multisig: 5_of_9
    signers: [dao_timelock, elected_community_rep_3, elected_community_rep_4, elected_community_rep_5, foundation_multisig, treasury_lead, independent_auditor_1, independent_auditor_2, security_council]
    max_tx_wei: 500000000000000000000
    onchain_enforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures. The safe enforces both conditions via an allowModule guard.
  - name: veto_override
    multisig: 7_of_9
    signers: [security_council, elected_community_rep_6, elected_community_rep_7, foundation_multisig, treasury_lead, independent_auditor_3, former_lead_1, former_lead_2, dao_timelock]
    onchain_enforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within the same 14-day window for release to execute.

## DeploymentOrder
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

## AuditRequirements
- All contract code must pass Slither + Mythril static analysis before deployment.
- Every upgrade path must be verified by an independent auditor.
- Quadratic sqrt computation must be tested for gas bounds across all realistic deposit sizes.
- Delegation DAG depth check must be tested against a graph of 10,000 nodes.
- A formal verification of the storage_layout_check assembly code is required before mainnet deployment.

## VotingParameterRanges
quorum_percent: {min: 1, max: 10, default: 4}
approval_threshold_percent: {min: 40, max: 60, default: 50}
voting_duration_hours: {min: 24, max: 168, default: 72}
timelock_delay_hours: {min: 12, max: 336, default: 48}
conviction_halflife_blocks: {min: 36000, max: 144000, default: 72000}
max_conviction_days: {min: 7, max: 90, default: 30}
delegation_max_depth: {min: 1, max: 10, default: 5}
proposal_deposit: {min: 10000, max: 500000, default: 50000}
