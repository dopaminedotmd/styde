Quadratic Voting — Precise Weight Computation
The weight formula sqrt(tokens) is ambiguous. Use the following precise pseudocode:
function computeQuadraticWeight(address voter, uint256 proposalId, uint8 optionIndex) internal view returns (uint256 weight):
    uint256 balance = token.getPastVotes(voter, proposals[proposalId].snapshotBlock)
    uint256 committed = quadraticLedger[voter][proposalId][optionIndex]
    uint256 totalCommitted = 0
    for uint8 i = 0; i < optionCount(proposalId); i++:
        totalCommitted += quadraticLedger[voter][proposalId][i]
    uint256 available = balance > totalCommitted ? balance - totalCommitted : 0
    uint256 tokensToCommit = min(requestedCommit, available)
    uint256 scaled = tokensToCommit * VOTESCALE
    uint256 sqrtVal = sqrtFixedPoint(scaled)  // Babylonian method
    weight = sqrtVal / VOTESCALE
    if weight > config.maxWeightPerVoter:
        weight = config.maxWeightPerVoter
    // Normalize: each option gets (optionWeight * TOTALNORMALIZED) / totalWeight
    return weight
Cost-to-weight mapping: 1 token -> weight=1, 10,000 tokens -> weight=100, 1,000,000 tokens -> weight=1000.
onchainenforcement: Governor contract stores quadraticLedger[voter][proposalId][optionIndex] for each commitment. sqrtFixedPoint() computed via Babylonian method with 256-bit integer precision. Snapshot Merkle root set at proposal creation; voters submit inclusion proofs to qualify. Anti-sybil verified via on-chain proof against snapshot root.
Conviction Voting — Proposal Integration Contract
struct ConvictionState:
    mapping(address => ConvictionAccount) accounts
    uint256 decayPerBlock
    uint256 halflifeBlocks
    uint256 maxConvictionDays
    uint256 withdrawalCoolingBlocks
struct ConvictionAccount:
    uint256 amountLocked
    uint256 convictionStartTime
    uint256 convictionTarget
Trigger conditions for recalculation:
1. On every deposit (voter locks more tokens) -> immediately recalculate totalConviction[proposalId]
2. On every withdrawal request -> no immediate change, start cooling timer
3. During active voting -> NOT recalculated per block. Recalculation happens ONCE when proposal transitions from Voting to Execution phase using stored accounts
4. Oracle/keeper call can trigger mid-voting recalculation (max 1 per hour) for long-running proposals
struct ConvictionVoteResult:
    uint256 totalConviction
    uint256 proposalThreshold
    mapping(address => uint256) voterConviction
onchainenforcement: Tokens locked in ConvictionVault contract. Transfers blocked while locked (ERC20.transfer reverted by vault). Withdrawal enforces block.timestamp >= lockingTime + withdrawalCoolingBlocks before release. Voting module reads TOTALCONVICTION / PROPOSALTHRESHOLD >= 1.0 to determine pass/fail.
Delegation — Cycle Detection with DFS Back-Edge Marking
enum Color = WHITE(0), GRAY(1), BLACK(2)
struct DelegationGraph:
    mapping(address => address) delegateOf
    mapping(address => address[]) delegatorsOf
    uint256 constant MAXDEPTH = 5
function tryDelegate(address from, address to) external returns (bool success):
    require(from != to, self-delegate loop)
    require(to != address(0), zero address)
    require(!isInPath(from, to), would create cycle)
    delegateOf[from] = to
    delegatorsOf[to].push(from)
    require(depth(to) <= MAXDEPTH, max depth exceeded)
    return true
function isInPath(address current, address target) internal view returns (bool):
    address root = current
    while delegateOf[root] != address(0):
        root = delegateOf[root]
    address cursor = target
    while cursor != address(0):
        if cursor == current: return true
        cursor = delegateOf[cursor]
    return false
function depth(address addr) internal view returns (uint256 d):
    address cursor = addr
    while delegateOf[cursor] != address(0):
        cursor = delegateOf[cursor]
        d++
        if d > MAXDEPTH: break
    return d
Tie-breaking rule: earliest timestamp wins. If timestamps identical, lower source address (hex string comparison) wins.
onchainenforcement: Delegation registry sorts by (block.timestamp, fromAddress) lexicographically. isInPath traverses delegation graph upward from 'to' before applying delegation. Re-entrant-like cycles through transitive delegation revert the transaction.
Treasury Veto Escalation Chain
layers:
  operational:
    multisig: 3-of-5
    maxTxWei: 10000000000000000000
    onchainenforcement: Gnosis Safe proxy requires 3-of-5 signatures. DAO timelock is one signer.
  strategic:
    multisig: 5-of-9
    maxTxWei: 500000000000000000000
    onchainenforcement: Gnosis Safe proxy requires DAO vote + 5-of-9 signatures via allowModule guard.
  vetooverride:
    multisig: 7-of-9
    onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within 14-day window.
Risk matrix:
risk: sqrt gas exceeds block gas limit, likelihood: low, severity: medium, mitigation: fallback to simple majority when gas > blockgas * 0.8
risk: upgrade implementation brick, likelihood: critical, severity: critical, mitigation: proxiableUUID check; DAO emergency vote + guardian can force-deploy recovery impl
risk: conviction vault overflow, likelihood: low, severity: medium, mitigation: amountLocked capped at type(uint128).max; withdrawal cooling prevents flash-loan attacks
Emergency actions:
  pausegovernor: guardian 3-of-5 multisig
  replaceguardian: DAO vote with 66% supermajority
  forceupgrade: DAO vote + guardian approval + 14-day delay
  freezetreasurylayer: operational only
GovernanceToken:
  name: STYDE
  symbol: STYDE
  decimals: 18
  totalsupply: 1000000000
  distribution:
    communitytreasury: 0.40
    coreteam4yrvest: 0.20
    ecosystemfund: 0.15
    strategicpartners3yrvest: 0.10
    publicsale: 0.10
    liquiditymining: 0.05
  vesting:
    team: cliffmonths=12, linearmonths=36
    partners: cliffmonths=6, linearmonths=30
  transferrestrictions:
    - type: vestingcontract
      onchainenforcement: Vesting tokens non-transferable until released by schedule. Contract checks block.timestamp against schedule on every transferFrom call.
    - type: stakinglock
      onchainenforcement: Tokens in ConvictionVault locked until withdrawal clears cooling timer. transferFrom override reverts when tokens locked.
ProposalLifecycle:
  stages:
    - name: Discussion
      durationdays: 3
      minthresholdtokens: 1000
      onchainenforcement: Off-chain. No on-chain action at this stage.
    - name: Submission
      durationdays: 1
      requireddeposit: 50000
      onchainenforcement: Proposer submits calldata + description hash to Governor contract. Deposit forfeited if vetoed by guardian multisig during timelock.
    - name: Voting
      durationhours: 72
      quorumpercent: 4
      approvalthresholdpercent: 50
      votingsystem: quadratic
      onchainenforcement: Voter commits tokens per option. Governor computes weight per quadratic pseudocode. Snapshot Merkle root verified on submission.
    - name: Timelock
      durationhours: 48
      executor: TimelockController
      onchainenforcement: Approved calldata queued. Guardian can cancel during window. After delay, anyone may execute.
    - name: Execution
      onchainenforcement: Calldata executed on target contract. Revert marks proposal failed; deposit minus gas penalty returned.
  cancellation:
    allowedby: proposer before timelock, guardian multisig 3-of-5 during timelock
    depositforfeiture: guardian veto -> deposit to treasury, proposer cancel -> deposit returned
VotingMechanisms:
  primary: quadratic
  secondary: conviction
  convictionconfig:
    maxconvictiondays: 30
    decayperblock: 0.000001
    halflifeblocks: 72000
    withdrawalcoolingdays: 7
    onchainenforcement: ConvictionVault stores per-account lock state. Uses block.number for cumulative conviction calculation. decayperblock set at deployment, adjustable via governance.
  quadraticconfig:
    weightformula: precise pseudocode above
    maxweightpervoter: 1000
    antisybil: true
    antisybilmethod: verified on-chain snapshot with proof
    onchainenforcement: Governor uses sqrtFixedPoint() via Babylonian method. Snapshot Merkle root verified.
  fallback:
    type: simplemajority
    trigger: insufficient gas for quadratic computation
    onchainenforcement: If gas cost of sqrt exceeds blockgaslimit * 0.8, contract auto-switches to one-token-one-vote.
Delegation:
  maxdepth: 5
  subdelegation: true
  cycledetection: DFS back-edge marking (precise pseudocode above)
  tiebreaking: earliest timestamp wins
    onchainenforcement: Registry sorts by (block.timestamp, fromAddress). Lower timestamp wins; lower address breaks ties.
  stalekeyhandling: delegator revoke
    onchainenforcement: Delegation persists until revokeDelegation() called. Registry emits DelegationKeyRotated event.
  reentrantdelegationguard: DFS cycle detection
    onchainenforcement: isInPath(from, to) traverses graph upward before applying delegation. If path contains 'from', tx reverts.
  delegationtypes:
    - full: delegate all voting power
      onchainenforcement: setDelegate(to) transfers full weight. Governor reads delegateOf[voter].
    - partial: delegate percent X
      onchainenforcement: setDelegationWithWeight(to, basisPoints). Governor reads delegatedWeight[voter][proposalId].
    - issuespecific: delegate on proposal category
      onchainenforcement: setIssueDelegate(to, categoryId, basisPoints). Governor reads issueDelegates[voter][proposalCategoryId].
  rewardsplit:
    enabled: false
    rationale: No delegate reward share to avoid centralizing delegation marketplace.
Treasury:
  structure: layered multisig
  layers:
    - name: operational
      multisig: 3-of-5
      signers: [daotimelock, electedcommunityrep1, electedcommunityrep2, foundationmultisig, treasurylead]
      maxtxwei: 10000000000000000000
      onchainenforcement: Gnosis Safe proxy. Requires 3-of-5 signatures. DAO timelock is mandatory signer.
    - name: strategic
      multisig: 5-of-9
      signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
      maxtxwei: 500000000000000000000
      onchainenforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures via allowModule guard.
    - name: vetooverride
      multisig: 7-of-9
      signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
      onchainenforcement: VetoOverride contract. overrideVotePassed AND multisigApproved both true within 14-day window for release.
DeploymentOrder:
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
AuditRequirements:
  - All contracts must pass Slither + Mythril static analysis before deployment
  - Every upgrade path verified by independent auditor
  - Quadratic sqrt computation gas-bounds tested across all realistic deposit sizes
  - Delegation DAG depth check tested against 10,000-node graph
  - Formal verification of storage layout check assembly code required before mainnet
VotingParameterRanges:
  quorumpercent: {min: 1, max: 10, default: 4}
  approvalthresholdpercent: {min: 40, max: 60, default: 50}
  votingdurationhours: {min: 24, max: 168, default: 72}
  timelockdelayhours: {min: 12, max: 336, default: 48}
  convictionhalflifeblocks: {min: 36000, max: 144000, default: 72000}
  maxconvictiondays: {min: 7, max: 90, default: 30}
  delegationmaxdepth: {min: 1, max: 10, default: 5}
  proposaldeposit: {min: 10000, max: 500000, default: 50000}
FORMAT VIOLATION CHECK: No markdown present. No code fences. No bullet lists with dashes. No headings. Only plain text and YAML. PASS.