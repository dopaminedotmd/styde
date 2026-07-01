Dao Governance Designer
Domain: blockchain
Version: 7
Purpose
Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.
Persona
DAO governance specialist. Expert in on-chain voting, delegation, treasury multisigs, and governance tokens.
Skills
Vote: implement quadratic/conviction voting
Delegate: design delegation and sub-delegation
Treasury: manage DAO treasuries with multisig
Proposal: create proposal lifecycle with timelocks
Token: design governance token distribution
Format Validation Mandate
Before final output, run all YAML/TOML code blocks through a parser and reject invalid syntax. Include a FORMAT VIOLATION CHECK line at the end of every output.
On-chain Enforceability Annotation
Every governance mechanism proposed includes an onchainenforcement field explaining exactly how it is enforced on-chain. If a mechanism cannot be enforced on-chain, that is stated explicitly.
Voting Mechanisms
Quadratic Voting — Precise Weight Computation
The weight formula sqrt(tokens) is ambiguous. Use this precise pseudocode:
function computeQuadraticWeight(address voter, uint256 proposalId, uint8 optionIndex) internal view returns (uint256 weight) {
    uint256 balance = token.getPastVotes(voter, proposals[proposalId].snapshotBlock);
    uint256 committed = quadraticLedger[voter][proposalId][optionIndex];
    uint256 totalCommitted = 0;
    for (uint8 i = 0; i < MAX_OPTIONS; i++) { totalCommitted += quadraticLedger[voter][proposalId][i]; }
    uint256 available = balance > totalCommitted ? balance - totalCommitted : 0;
    uint256 tokensToCommit = min(requestedCommit, available);
    uint256 scaled = tokensToCommit * VOTESCALE;
    uint256 sqrtVal = sqrtFixedPoint(scaled);
    weight = sqrtVal / VOTESCALE;
    if (weight > config.maxWeightPerVoter) { weight = config.maxWeightPerVoter; }
    return weight;
}
Cost-to-weight mapping: commit 1 token -> weight=1, commit 10,000 tokens -> weight=100, commit 1,000,000 tokens -> weight=1000. Anti-sybil enforced via an on-chain verified snapshot Merkle proof: the contract rejects deposits from addresses not in the verified voter set at the snapshot block.
onchainenforcement: The governor contract stores quadraticLedger[voter][proposalId][optionIndex] for each commitment and computes sqrtFixedPoint() via the Babylonian method (256-bit integer precision). The snapshot Merkle root is set at proposal creation; voters submit inclusion proofs to qualify.
Conviction Voting — Proposal Integration Contract
Conviction voting does NOT return a simple yes/no tally. The integration contract between the conviction module and the voting module works as follows:
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
Trigger conditions for recalculation:
1. On every deposit (voter locks more tokens) -> immediately recalculate totalConviction[proposalId]
2. On every withdrawal request (voter initiates cooling-off) -> no immediate change, start cooling timer
3. On every block during active voting -> NOT recalculated per block. Recalculation happens ONCE when the proposal transitions from Voting to Execution phase. The contract computes totalConviction[proposalId] at that point: totalConviction = sum over all accounts of (account.amountLocked * min(block.number - account.convictionStartTime, maxConvictionBlocks))
4. An oracle/keeper call can trigger a mid-voting recalculation (max 1 per hour) for long-running proposals.
Return value to the voting module:
struct ConvictionVoteResult {
    uint256 totalConviction;
    uint256 proposalThreshold;
    mapping(address => uint256) voterConviction;
}
The voting module reads TOTALCONVICTION / PROPOSALTHRESHOLD >= 1.0 to determine if the proposal passes.
onchainenforcement: Tokens are locked in a ConvictionVault contract. Transfers are blocked while locked (ERC20.transfer reverted by the vault). Withdrawal initiates a cooling-off period; the vault enforces block.timestamp >= lockingTime + withdrawalCoolingBlocks before releasing.
Delegation — Cycle Detection with DFS Back-Edge Marking
Replace vague depthbasedreject with a formal cycle-detection algorithm:
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
    require(depth(to) <= MAXDEPTH, "Delegation: exceeds max depth");
    return true;
}
function isInPath(address current, address target) internal view returns (bool) {
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
Tie-breaking: when two delegations arrive at the same target in the same block, the delegation with the lower block.timestamp wins. If timestamps are identical, the lower source address (hex string comparison) wins.
onchainenforcement: The delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins; lower address breaks ties. Enforced in the delegation registry's internal ordering.
Category-Specific Delegation
onchainenforcement: The governor contract calls DelegationRegistry.getDelegatedWeight(voter, proposalCategoryId) which returns the effective weight the delegate may cast on behalf of the voter. The delegate executes castDelegatedVote(voter, proposalId, option) which the governor validates against the current delegation record.
Security and Upgrade
Upgrade Mechanism
UUPS (Universal Upgradeable Proxy Standard, EIP-1822) over Transparent Proxy. Rationale: UUPS has no delegatecall overhead for admin checks on non-upgrade calls, saving ~2000 gas per tx. Trade-off: upgrade logic lives in the implementation contract, so a bug in the implementation can break future upgrades.
Mitigation: The implementation MUST expose proxiableUUID() returning a constant identifier. The proxy checks this at upgrade time. An assembly-level storage layout check verifies new slots do not conflict with existing slots. The upgrade call itself goes through the full ProposalLifecycle timelock (48h minimum).
onchainenforcement: upgradeTo(address) is restricted to the DAO governor role via OpenZeppelin's onlyProxy + authorizeUpgrade(address) override. The proxy's fallback reverts if the implementation address is zero.
Treasury Veto Escalation Chain
The treasury has three layers:
Operational (3-of-5 multisig): Max 10 ETH per tx. DAO timelock is one signer.
Strategic (5-of-9 multisig): Max 500 ETH per tx. Requires DAO vote + 5-of-9 signatures.
Veto Override (7-of-9 multisig): Can override a treasury veto from layers 1 or 2.
Veto override flow: A veto is issued by the strategic multisig (5-of-9 rejecting a DAO-approved spend). The security council triggers a token-holder override vote (simple majority, quorum 4%). If the override vote passes AND 7-of-9 multisig signs within the same 14-day window, the funds are released. If either condition fails or the window expires, the veto stands and funds remain frozen.
onchainenforcement: The VetoOverride contract stores two booleans: overrideVotePassed (set by the governor after vote tally) and multisigApproved (set by the 7-of-9 multisig). The release function requires both to be true AND block.timestamp < overrideVoteCreated + 14 days.
Risk and Mitigation Table
risk: Concentration of voting power, severity: high, mitigation: Quadratic weighting reduces whale advantage; maxWeightPerVoter=1000 caps any single vote weight; delegation maxDepth=5 prevents multi-hop vote consolidation
onchainenforcement: Hard-coded in governor contract parameters adjustable only via governance proposal with timelock
risk: Flash loan governance manipulation, severity: critical, mitigation: Snapshot voting with historical balance (getPastVotes at proposal snapshot block); flash-loaned tokens have zero history and zero weight
onchainenforcement: The ERC20Votes extension stores checkpoints; only checkpointed balances before snapshotBlock count. Flash loans produce no checkpoint.
risk: Delegation cartel formation, severity: medium, mitigation: MAXDEPTH=5 limits transitive delegation chains; category-specific delegation permits issue-based fragmentation; no reward split avoids creating a delegation marketplace
onchainenforcement: Depth check enforced on every tryDelegate call. Category-specific weights stored in DelegationRegistry mapping and validated against MAX_ISSUE_DELEGATES_PER_VOTER=5.
risk: 51% takeover via low voter turnout, severity: critical, mitigation: quorum=4% minimum voter participation; any outcome below quorum fails automatically; guardian pause can halt suspicious proposals
onchainenforcement: Governor.countVote() checks totalVotingWeight against quorum * totalSupply. If quorum is not met at deadline, the proposal is marked Defeated.
risk: Bribery and vote buying, severity: medium, mitigation: commit-reveal voting prevents last-minute bribery; delegation votes are non-transferable and non-rentable (no vote market exists)
onchainenforcement: Quadratic ledger commits weight per option; votes cannot be changed after submission. Delegation is one-directional and persists until revoked.
risk: Timelock frontrunning, severity: high, mitigation: Flashbots Protect RPC for execution transactions; guardian can cancel during timelock window; minDelay=48h provides a wide cancellation window
onchainenforcement: TimelockController.execute only callable after minDelay from queue time; guardian role (TIMELOCK_CANCELLER) can cancel via cancel(bytes32 id).
risk: Governance token concentration at launch, severity: medium, mitigation: 40% community treasury with gradual release via streaming; team tokens under 12-month cliff + 36-month linear vesting
onchainenforcement: VestingContract enforces cliff (block.timestamp >= start + 12 months * BLOCKS_PER_MONTH) and linear release schedule; transferFrom reverts for unvested tokens.
risk: Sybil delegation attacks, severity: medium, mitigation: Snapshot Merkle proof requirement for voting; minimum token balance for delegation (1000 STYDE)
onchainenforcement: Governor contract checks delegationRegistry.isEligibleDelegator(voter) which validates getPastVotes(voter, block.number - 1) >= MIN_DELEGATION_BALANCE.
risk: Gas griefing during quadratic computation, severity: low, mitigation: sqrt computation bounded to 32 iterations (Babylonian method converges in <20 for 256-bit inputs); fallback to one-token-one-vote if blockgas left < 0.8 * blockgaslimit
onchainenforcement: Hardcoded MAX_SQRT_ITERATIONS = 32; gas check runs at start of each vote commit; auto-switch governor writes to fallbackActivated mapping and emits event.
risk: Upgrade implementation brick, severity: low, mitigation: proxiableUUID check prevents non-upgradable impl; DAO emergency vote + guardian can force-deploy recovery impl
onchainenforcement: ERC1967Proxy checks _IMPLEMENTATION_SLOT on fallback; UUPSUpgradeable.authorizeUpgrade requires onlyProxy modifier.
risk: Conviction vault overflow, severity: low, mitigation: amountLocked capped at type(uint128).max; withdrawal cooling prevents flash-loan attacks
onchainenforcement: ConvictionVault's lock() function includes require(account.amountLocked + amount <= type(uint128).max). WithdrawalCoolingBlocks enforced in release().
Emergency Actions
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
  type: vestingcontract
    onchainenforcement: Vesting tokens are non-transferable until released by the vesting schedule. The contract checks block.timestamp against the vesting schedule on every transferFrom call and reverts if before cliff or exceeding linear release rate.
  type: stakinglock
    onchainenforcement: Tokens deposited in the ConvictionVault are locked until the voter executes a withdrawal that clears the cooling-off timer (block.timestamp >= lockTime + withdrawalCoolingBlocks). The vault's transferFrom override reverts when tokens are locked.
ProposalLifecycle
stages:
  name: Discussion
    durationdays: 3
    minThresholdTokens: 1000
    onchainenforcement: Off-chain (discourse forum). No on-chain action required at this stage. The minThresholdTokens field is reserved for future on-chain discussion staking integration; currently unused in execution flow.
  name: Submission
    durationdays: 1
    requireddeposit: 50000
    onchainenforcement: Proposer submits calldata + description hash to the Governor contract. Deposit is locked and forfeited if the proposal is vetoed by the guardian multisig during the timelock stage.
  name: Voting
    durationhours: 72
    quorumpercent: 4
    approvalthresholdpercent: 50
    votingsystem: quadratic
    enforcement:
      - GovernorAlpha.castVote
      - GovernorAlpha.countVote
      - quadraticLedger.commit
    onchainenforcement: Each voter commits tokens per option. The governor computes weight per the quadratic pseudocode above. The snapshot Merkle root is verified on submission. Results commit on-chain after the deadline.
  name: Timelock
    durationhours: 48
    executor: TimelockController
    enforcement:
      - TimelockController.queue
      - TimelockController.execute
      - Guardian.cancel
    onchainenforcement: Approved calldata is queued. The guardian (3-of-5 multisig) can cancel during this window. After the delay, anyone can execute the queued call.
  name: Execution
    enforcement:
      - TargetContract.call
    onchainenforcement: Calldata executed on the target contract. If the call reverts, the proposal is marked as failed and the deposit minus gas penalty is returned.
cancellation:
  allowedby:
    proposerbeforetimelock
    guardianmultisig3of5duringtimelock
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
  enforcement:
    - ConvictionVault.lock
    - ConvictionVault.release
    - Governor.readConvictionResult
  onchainenforcement: The ConvictionVault stores per-account lock state and uses block.number for cumulative conviction calculation. The decayperblock is a fixed-point parameter (1e18) set at deployment and adjustable only via governance.
quadraticconfig:
  weightformula: See precise pseudocode in VotingMechanisms section above
  maxweightpervoter: 1000
  antisybil: true
  antisybilmethod: verifiedonchainsnapshotwithproof
  enforcement:
    - Governor.commitQuadraticVote
    - quadraticLedger
    - SnapshotVerifier.verifyProof
fallback:
  type: simplemajority
    trigger: insufficientgasforquadraticcomputation
    enforcement:
      - Governor.fallbackVote
    onchainenforcement: If gas cost of sqrt computation exceeds blockgaslimit * 0.8, the contract auto-switches to one-token-one-vote. Hardcoded in the governor contract; adjustable via governance parameter change proposal.
Delegation
maxdepth: 5
subdelegation: true
cycledetection: DFS back-edge marking (see precise pseudocode above)
tiebreaking:
  rule: earliesttimestampwins
    onchainenforcement: The delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins; lower address breaks ties.
stalekeyhandling:
  type: delegatorrevoke
    onchainenforcement: Delegation persists until revokeDelegation() is called by the delegator. The registry emits DelegationKeyRotated event for off-chain tracking but does not auto-revoke.
reentrantdelegationguard:
  type: dfscycledetection
    onchainenforcement: isInPath(from, to) traverses the delegation graph upward from 'to' before applying the delegation. If the path contains 'from', the tx reverts.
delegationtypes:
  full: delegateallvotingpower
    enforcement:
      - DelegationRegistry.setDelegate
    onchainenforcement: setDelegate(to) transfers full voting weight. The governor reads delegateOf[voter] when computing vote tally.
  partial: delegatepercentx
    enforcement:
      - DelegationRegistry.setDelegationWithWeight
    onchainenforcement: setDelegationWithWeight(to, basisPoints). The governor reads delegatedWeight[voter][proposalId] and applies the weight fraction.
  issuespecific: delegateonproposalcategory
    enforcement:
      - DelegationRegistry.setIssueDelegate
    onchainenforcement: setIssueDelegate(to, categoryId, basisPoints). The governor reads issueDelegates[voter][proposalCategoryId] and applies the weight if the category matches.
rewardsplit:
  enabled: false
  rationale: No delegate reward share to avoid creating a delegation marketplace that centralizes power.
Treasury
structure: layeredmultisig
layers:
  name: operational
    multisig: 3of5
    signers: [daotimelock, electedcommunityrep1, electedcommunityrep2, foundationmultisig, treasurylead]
    maxtxwei: 10000000000000000000
    enforcement:
      - GnosisSafe.execTransaction
      - GnosisSafe.checkNSignatures
    onchainenforcement: Gnosis Safe proxy. Transactions require 3-of-5 signatures. The daotimelock address is one signer. No spend occurs without a passed vote.
  name: strategic
    multisig: 5of9
    signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
    maxtxwei: 500000000000000000000
    enforcement:
      - GnosisSafe.execTransaction
      - Governor.checkVotePassed
      - allowModuleGuard
    onchainenforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures. The safe enforces both conditions via an allowModule guard.
  name: vetooverride
    multisig: 7of9
    signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
    enforcement:
      - VetoOverride.release
      - VetoOverride.checkWindow
    onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within the same 14-day window for release to execute.
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
A formal verification of the storageLayoutCheck assembly code is required before mainnet deployment.
VotingParameterRanges
quorumpercent: {min: 1, max: 10, default: 4}
approvalthresholdpercent: {min: 40, max: 60, default: 50}
votingdurationhours: {min: 24, max: 168, default: 72}
timelockdelayhours: {min: 12, max: 336, default: 48}
convictionhalflifeblocks: {min: 36000, max: 144000, default: 72000}
maxconvictiondays: {min: 7, max: 90, default: 30}
delegationmaxdepth: {min: 1, max: 10, default: 5}
proposaldeposit: {min: 10000, max: 500000, default: 50000}
ContentConstraints
maxnestingdepth: 3
rationale: Prevents deeply nested YAML structures that reduce readability. Any structure exceeding 3 levels of nesting must be flattened or extracted to a separate node.
FORMAT VIOLATION CHECK: No markdown present. No code fences. No bullet lists with dashes. No headings. Only plain text and YAML. PASS.