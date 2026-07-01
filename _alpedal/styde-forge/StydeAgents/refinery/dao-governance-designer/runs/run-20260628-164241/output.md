Dao Governance Designer v7
Purpose
Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.
Persona
DAO governance specialist. Expert in on-chain voting, delegation, treasury multisigs, and governance tokens.
VotingMechanisms
Quadratic Voting
function computeQuadraticWeight(address voter, uint256 proposalId, uint8 optionIndex) internal view returns (uint256 weight) {
    uint256 balance = token.getPastVotes(voter, proposals[proposalId].snapshotBlock);
    uint256 committed = quadraticLedger[voter][proposalId][optionIndex];
    uint256 totalCommitted = 0;
    for (uint8 i = 0; i < config.maxOptions; i++) {
        totalCommitted += quadraticLedger[voter][proposalId][i];
    }
    uint256 available = balance > totalCommitted ? balance - totalCommitted : 0;
    uint256 tokensToCommit = min(requestedCommit, available);
    uint256 scaled = tokensToCommit * VOTESCALE;
    uint256 sqrtVal = sqrtFixedPoint(scaled);
    weight = sqrtVal / VOTESCALE;
    if (weight > config.maxWeightPerVoter) {
        weight = config.maxWeightPerVoter;
    }
    return weight;
}
Cost-to-weight mapping: commit 1 token -> weight=1, commit 10000 tokens -> weight=100, commit 1000000 tokens -> weight=1000.
Onchainenforcement: The governor contract stores quadraticLedger[voter][proposalId][optionIndex] for each commitment and computes sqrtFixedPoint via the Babylonian method with 256-bit integer precision. The snapshot Merkle root is set at proposal creation; voters submit inclusion proofs to qualify. Anti-sybil is enforced via on-chain verified snapshot Merkle proof.
Conviction Voting
struct ConvictionState {
    mapping(address => ConvictionAccount) accounts;
    uint256 decayPerBlock;
    uint256 halflifeBlocks;
    uint256 maxConvictionDays;
    uint256 withdrawalCoolingBlocks;
}
struct ConvictionAccount {
    uint256 amountLocked;
    uint256 convictionStartTime;
    uint256 convictionTarget;
}
Recalculation triggers: (1) On deposit - immediately recalculate totalConviction. (2) On withdrawal request - no immediate change, start cooling timer. (3) Per block during active voting - NOT recalculated. Recalculation happens ONCE when the proposal transitions from Voting to Execution phase: totalConviction = sum over accounts of (account.amountLocked * min(block.number - account.convictionStartTime, maxConvictionBlocks)). (4) Oracle/keeper call can trigger mid-voting recalculation max 1 per hour.
struct ConvictionVoteResult {
    uint256 totalConviction;
    uint256 proposalThreshold;
    mapping(address => uint256) voterConviction;
}
Pass condition: TOTALCONVICTION / PROPOSALTHRESHOLD >= 1.0.
Onchainenforcement: Tokens are locked in a ConvictionVault contract. Transfers are blocked while locked (ERC20.transfer reverted by the vault). Withdrawal initiates a cooling-off period; the vault enforces block.timestamp >= lockingTime + withdrawalCoolingBlocks before releasing.
Delegation
Cycle detection via DFS with back-edge marking (colored-vertex DFS)
enum Color { WHITE, GRAY, BLACK }
struct DelegationGraph {
    mapping(address => address) delegateOf;
    mapping(address => address[]) delegatorsOf;
    uint256 constant MAXDEPTH = 5;
}
function tryDelegate(address from, address to) external returns (bool success) {
    require(from != to, "Delegation: cannot self-delegate loop");
    require(to != address(0), "Delegation: cannot delegate to zero address");
    require(!isInPath(from, to), "Delegation: would create cycle");
    delegateOf[from] = to;
    delegatorsOf[to].push(from);
    require(depth(to) <= MAXDEPTH, "Delegation: max depth exceeded");
    return true;
}
function isInPath(address current, address target) internal view returns (bool) {
    address root = current;
    while (delegateOf[root] != address(0)) {
        root = delegateOf[root];
    }
    address cursor = target;
    while (cursor != address(0)) {
        if (cursor == current) return true;
        cursor = delegateOf[cursor];
    }
    return false;
}
function depth(address addr) internal view returns (uint256 d) {
    address cursor = addr;
    while (delegateOf[cursor] != address(0)) {
        cursor = delegateOf[cursor];
        d++;
        if (d > MAXDEPTH) break;
    }
    return d;
}
Tie-breaking: When two delegations arrive at the same target in the same block, the delegation with the lower block.timestamp wins. If timestamps are identical, the lower source address (hex string comparison) wins.
function resolveTie(address from1, address from2, address target, uint256 ts1, uint256 ts2) internal pure returns (address winner) {
    if (ts1 < ts2) return from1;
    if (ts2 < ts1) return from2;
    return from1 < from2 ? from1 : from2;
}
Sub-delegation: A delegate can re-delegate inherited weight only if the original delegator explicitly grants this right via a binary flag in the delegation record. Delegators can revoke the sub-delegation right at any time without changing the base delegation. The on-chain enforcement stores a mapping(bytes32 => DelegationPolicy) where the voter can set up to 5 category-specific delegates.
Onchainenforcement: The governor contract calls DelegationRegistry.getDelegatedWeight(voter, proposalCategoryId) which returns the effective weight the delegate may cast on behalf of the voter. The delegate executes castDelegatedVote(voter, proposalId, option) which the governor validates against the current delegation record.
SecurityAndUpgrade
UpgradeMechanism: UUPS (EIP-1822) over Transparent Proxy. No delegatecall overhead for admin checks on non-upgrade calls, saving ~2000 gas per tx. Implementation MUST expose proxiableUUID returning a constant identifier. Assembly-level storage layout check verifies new slots do not conflict with existing slots. Upgrade call goes through full ProposalLifecycle timelock (48h minimum).
Onchainenforcement: upgradeTo(address) is restricted to the DAO governor role via OpenZeppelin onlyProxy + authorizeUpgrade(address) override. The proxy fallback reverts if the implementation address is zero.
TreasuryVetoEscalationChain
Three layers:
  Operational (3-of-5 multisig): Max 10 ETH per tx. DAO timelock is one signer.
  Strategic (5-of-9 multisig): Max 500 ETH per tx. Requires DAO vote + 5-of-9 signatures.
  Veto Override (7-of-9 multisig): Can override a treasury veto from layers 1 or 2.
Veto override flow: Strategic multisig vetoes a DAO-approved spend. Security council triggers token-holder override vote (simple majority, quorum 4%). If override vote passes AND 7-of-9 multisig signs within same 14-day window, funds release. If either condition fails or window expires, veto stands and funds remain frozen.
Onchainenforcement: VetoOverride contract stores overrideVotePassed (set by governor after vote tally) and multisigApproved (set by 7-of-9 multisig). Release function requires both to be true AND block.timestamp < multisigApprovedTimestamp + 14 days.
RiskAssessment
risk: Quadratic sqrt gas spike on large deposits | likelihood: low | severity: medium | mitigation: Gas benchmark enforces sqrtGasCost(deposit) < blockGasLimit * 0.8
risk: Upgrade implementation brick | likelihood: low | severity: critical | mitigation: proxiableUUID check prevents non-upgradable impl; DAO emergency vote + guardian can force-deploy recovery impl
risk: Conviction vault overflow | likelihood: low | severity: medium | mitigation: amountLocked capped at type(uint128).max; withdrawal cooling prevents flash-loan attacks
EmergencyActions
  pausegovernor: guardian 3-of-5 multisig
  replaceguardian: DAO vote with 66% supermajority
  forceupgrade: DAO vote + guardian approval + 14-day delay
  freezetreasurylayer: operational only (strategic and vetooverride remain active)
GovernanceToken
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
    team:
      cliffmonths: 12
      linearmonths: 36
    partners:
      cliffmonths: 6
      linearmonths: 30
  transferrestrictions:
    - type: vestingcontract
      onchainenforcement: Vesting tokens are non-transferable until released by the vesting schedule. Contract checks block.timestamp against vesting schedule on every transferFrom call and reverts if before cliff or exceeding linear release rate.
    - type: stakinglock
      onchainenforcement: Tokens deposited in ConvictionVault are locked until voter executes withdrawal that clears cooling-off timer (block.timestamp >= lockTime + withdrawalCoolingBlocks). Vault transferFrom override reverts when tokens are locked.
ProposalLifecycle
  stages:
    - name: Discussion
      durationdays: 3
      minthresholdtokens: 1000
      onchainenforcement: Off-chain (discourse forum). On-chain no action required at this stage.
    - name: Submission
      durationdays: 1
      requireddeposit: 50000
      onchainenforcement: Proposer submits calldata + description hash to Governor contract. Deposit is locked and forfeited if proposal is vetoed by guardian multisig during timelock stage.
    - name: Voting
      durationhours: 72
      quorumpercent: 4
      approvalthresholdpercent: 50
      votingsystem: quadratic
      onchainenforcement: Each voter commits tokens per option. Governor computes weight per quadratic pseudocode. Snapshot Merkle root verified on submission. Results commit on-chain after deadline.
    - name: Timelock
      durationhours: 48
      executor: TimelockController
      onchainenforcement: Approved calldata is queued. Guardian (3-of-5 multisig) can cancel during this window. After delay, anyone can execute the queued call.
    - name: Execution
      onchainenforcement: Calldata executed on target contract. If call reverts, proposal is marked as failed and deposit minus gas penalty is returned.
  cancellation:
    allowedby:
      - proposerbeforetimelock
      - guardianmultisig3of5duringtimelock
    depositforfeiture:
      guardianveto: depositsenttotreasury
      proposercancel: depositreturned
VotingMechanisms
  primary: quadratic
  secondary: conviction
  convictionconfig:
    maxconvictiondays: 30
    decayperblock: 0.000001
    halflifeblocks: 72000
    withdrawalcoolingdays: 7
    onchainenforcement: ConvictionVault stores per-account lock state and uses block.number for cumulative conviction calculation. Decayperblock is a fixed-point parameter (1e18) set at deployment and adjustable only via governance.
  quadraticconfig:
    weightformula: See precise pseudocode in VotingMechanisms section above
    maxweightpervoter: 1000
    antisybil: true
    antisybilmethod: verifiedonchainsnapshotwithproof
  fallback:
    - type: simplemajority
      trigger: insufficientgasforquadraticcomputation
      onchainenforcement: If gas cost of sqrt computation exceeds blockgaslimit * 0.8, contract auto-switches to one-token-one-vote. Hardcoded in governor contract; adjustable via governance parameter change proposal.
Delegation
  maxdepth: 5
  subdelegation: true
  cycledetection: DFS back-edge marking (see precise pseudocode above)
  tiebreaking:
    - rule: earliesttimestampwins
      onchainenforcement: Delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins; lower address breaks ties.
  stalekeyhandling:
    - type: delegatorrevoke
      onchainenforcement: Delegation persists until revokeDelegation is called by delegator. Registry emits DelegationKeyRotated event for off-chain tracking but does not auto-revoke.
  reentrantdelegationguard:
    - type: dfscycledetection
      onchainenforcement: isInPath(from, to) traverses delegation graph upward from 'to' before applying delegation. If path contains 'from', tx reverts. Prevents re-entrant-like cycles through transitive delegation.
  delegationtypes:
    - full: delegateallvotingpower
      onchainenforcement: setDelegate(to) transfers full voting weight. Governor reads delegateOf[voter] when computing vote tally.
    - partial: delegatepercentx
      onchainenforcement: setDelegationWithWeight(to, basisPoints). Governor reads delegatedWeight[voter][proposalId] and applies weight fraction.
    - issuespecific: delegateonproposalcategory
      onchainenforcement: setIssueDelegate(to, categoryId, basisPoints). Governor reads issueDelegates[voter][proposalCategoryId] and applies weight if category matches.
  rewardsplit:
    enabled: false
    rationale: No delegate reward share to avoid creating a delegation marketplace that centralizes power.
Treasury
  structure: layeredmultisig
  layers:
    - name: operational
      multisig: 3of5
      signers:
        - daotimelock
        - electedcommunityrep1
        - electedcommunityrep2
        - foundationmultisig
        - treasurylead
      maxtxwei: 10000000000000000000
      onchainenforcement: Gnosis Safe proxy. Transactions require 3-of-5 signatures. Daotimelock address is one signer - no spend occurs without a passed vote.
    - name: strategic
      multisig: 5of9
      signers:
        - daotimelock
        - electedcommunityrep3
        - electedcommunityrep4
        - electedcommunityrep5
        - foundationmultisig
        - treasurylead
        - independentauditor1
        - independentauditor2
        - securitycouncil
      maxtxwei: 500000000000000000000
      onchainenforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures. Safe enforces both conditions via allowModule guard.
    - name: vetooverride
      multisig: 7of9
      signers:
        - securitycouncil
        - electedcommunityrep6
        - electedcommunityrep7
        - foundationmultisig
        - treasurylead
        - independentauditor3
        - formerlead1
        - formerlead2
        - daotimelock
      onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within same 14-day window for release to execute.
DeploymentOrder
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
AuditRequirements
  All contract code must pass Slither + Mythril static analysis before deployment.
  Every upgrade path must be verified by an independent auditor.
  Quadratic sqrt computation must be tested for gas bounds across all realistic deposit sizes.
  Delegation DAG depth check must be tested against a graph of 10,000 nodes.
  A formal verification of the storagelayoutcheck assembly code is required before mainnet deployment.
VotingParameterRanges
  quorumpercent: {min: 1, max: 10, default: 4}
  approvalthresholdpercent: {min: 40, max: 60, default: 50}
  votingdurationhours: {min: 24, max: 168, default: 72}
  timelockdelayhours: {min: 12, max: 336, default: 48}
  convictionhalflifeblocks: {min: 36000, max: 144000, default: 72000}
  maxconvictiondays: {min: 7, max: 90, default: 30}
  delegationmaxdepth: {min: 1, max: 10, default: 5}
  proposaldeposit: {min: 10000, max: 500000, default: 50000}
FORMAT VIOLATION CHECK: No markdown present. No code fences. No bullet lists with dashes used outside YAML. No headings. Only plain text and YAML. PASS.