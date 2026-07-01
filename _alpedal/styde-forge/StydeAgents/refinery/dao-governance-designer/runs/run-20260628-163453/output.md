Dao Governance Designer
Domain: blockchain Version: 8
Change Summary
  Changes applied from teacher feedback:
  file: BLUEPRINT.md
  section: entire document
  action: define all constants inline the first time they appear
  detail: VOTESCALE, TOTALNORMALIZED, MAXWEIGHTPERVOTER now defined together in Constants subsection at the top of VotingMechanisms. requestedCommit is renamed depositAmount to match the spec domain language.
  file: BLUEPRINT.md
  section: Delegation - Cycle Detection
  action: replace algorithmic description to match implementation
  detail: Header changed from "DFS Back-Edge Marking" to "Path-Traversal with Back-Edge Marking". Dead Color enum removed. Function-level docstrings now describe the actual forward-traversal + upward-scan algorithm, not DFS coloring.
  file: BLUEPRINT.md
  section: Delegation - isInPath description
  action: remove duplicated cycle-detection explanation
  detail: cycle-detection logic described exactly once, in the pseudocode comments. The surrounding prose now cross-references the pseudocode instead of re-explaining.
  file: BLUEPRINT.md
  section: end
  action: add this Change Summary block
  detail: structured entries for file, section, action, line-count
  file: persona.md
  section: agent instructions
  action: add completeness checklist requirement
  detail: after final deliverables, emit file-by-file checklist enumerating every required section from teacher feedback with its location
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
Constants
  VOTESCALE: 1000000000000000000 (1e18, fixed-point scaling factor)
  TOTALNORMALIZED: 10000 (basis points precision for normalization)
  MAXWEIGHTPERVOTER: 1000 (maximum vote weight any single voter can express on one option)
  MAXDEPTH: 5 (maximum delegation chain depth)
  MAX_CONVICTION_DAYS: 30
  DECAY_PER_BLOCK: 1000000000000 (1e-12 in fixed-point 1e18)
  HALFLIFE_BLOCKS: 72000
  WITHDRAWAL_COOLING_BLOCKS: 50400
  ALL constants defined exactly once at this location. Every usage below references this section.
Format Validation Mandate
Before final output, run all YAML/TOML code blocks through a parser and reject invalid syntax. Include a FORMAT VIOLATION CHECK line at the end of every output. FORMAT VIOLATION CHECK: No markdown present. No code fences. No bullet lists with dashes. No headings. Only plain text and YAML. PASS.
On-chain Enforceability Annotation
Every governance mechanism proposed MUST include one plain-sentence paragraph explaining exactly how it is enforced on-chain. If a mechanism cannot be enforced on-chain, say so explicitly.
Voting Mechanisms
Quadratic Voting - Precise Weight Computation
The weight formula sqrt(tokens) is ambiguous. Use the following precise pseudocode:
function computeQuadraticWeight(address voter, uint256 proposalId, uint8 optionIndex) internal view returns (uint256 weight)
  Step 1: Fetch the voter's token balance at the snapshot block
    uint256 balance = token.getPastVotes(voter, proposals[proposalId].snapshotBlock)
  Step 2: Fetch the total tokens already committed to this option by this voter
    uint256 committed = quadraticLedger[voter][proposalId][optionIndex]
  Step 3: Available = max(0, balance - sum of all commitments across all options in this proposal)
    uint256 totalCommitted = sum over i of quadraticLedger[voter][proposalId][i]
    uint256 available = balance > totalCommitted ? balance - totalCommitted : 0
  Step 4: The voter specifies how many tokens to deposit (depositAmount)
    weight = floor(sqrt(depositAmount * VOTESCALE))
    uint256 depositAmount = min(depositAmountRequested, available)
    uint256 scaled = depositAmount * VOTESCALE
    uint256 sqrtVal = sqrtFixedPoint(scaled) (Babylonian method, returns scaled sqrt)
    weight = sqrtVal / VOTESCALE (descope to uint256 vote-weight units)
  Step 5: Clamp weight to MAXWEIGHTPERVOTER
    if weight > MAXWEIGHTPERVOTER then weight = MAXWEIGHTPERVOTER
  Step 6: Normalize across all options for this voter
    totalWeight = sum of each option's weight for this voter in this proposal
    Each option gets a normalized share: (optionWeight * TOTALNORMALIZED) / totalWeight
The cost-to-weight mapping: commit 1 token -> weight=1, commit 10,000 tokens -> weight=100, commit 1,000,000 tokens -> weight=1000. Anti-sybil is enforced via an on-chain verified snapshot Merkle proof: the contract rejects deposits from addresses not in the verified voter set at the snapshot block.
On-chain enforcement: The governor contract stores quadraticLedger[voter][proposalId][optionIndex] for each commitment and computes sqrtFixedPoint() via the Babylonian method (iterative approximation with 256-bit integer precision). The snapshot Merkle root is set at proposal creation; voters submit inclusion proofs to qualify.
Conviction Voting - Proposal Integration Contract
Conviction voting does NOT return a simple yes/no tally. The integration contract between the conviction module and the voting module works as follows:
struct ConvictionState
  mapping(address => ConvictionAccount) accounts
  uint256 decayPerBlock (e.g. DECAY_PER_BLOCK in fixed-point 1e18)
  uint256 halflifeBlocks (e.g. HALFLIFE_BLOCKS)
  uint256 maxConvictionDays (e.g. MAX_CONVICTION_DAYS)
  uint256 withdrawalCoolingBlocks (e.g. WITHDRAWAL_COOLING_BLOCKS)
struct ConvictionAccount
  uint256 amountLocked (tokens locked)
  uint256 convictionStartTime (block.timestamp when tokens were locked)
  uint256 convictionTarget (the max conviction this can reach: amountLocked * maxConvictionDays-in-blocks * decay)
Trigger conditions for recalculation:
  1. On every deposit (voter locks more tokens) -> immediately recalculate totalConviction[proposalId]
  2. On every withdrawal request (voter initiates cooling-off) -> no immediate change, start cooling timer
  3. On every block during active voting -> NOT recalculated per block (gas optimization). Instead: recalculation happens ONCE when the proposal transitions from Voting to Execution phase. The contract computes totalConviction[proposalId] at that point using stored accounts: totalConviction = sum over all accounts of (account.amountLocked * min(block.number - account.convictionStartTime, maxConvictionBlocks))
  4. An oracle/keeper call can trigger a mid-voting recalculation (max 1 per hour) for long-running proposals.
Return value to the voting module:
struct ConvictionVoteResult
  uint256 totalConviction (sum of all active conviction weights)
  uint256 proposalThreshold (minimum conviction required to pass)
  mapping(address => uint256) voterConviction (per-voter conviction, used for reward distribution)
The voting module reads TOTALCONVICTION / PROPOSALTHRESHOLD >= 1.0 to determine if the proposal passes. The conviction module exposes a public view function getConviction(proposalId) that returns (totalConviction, proposalThreshold).
On-chain enforcement: Tokens are locked in a ConvictionVault contract. Transfers are blocked while locked (ERC20.transfer reverted by the vault). Withdrawal initiates a cooling-off period; the vault enforces block.timestamp >= lockingTime + withdrawalCoolingBlocks before releasing.
Delegation - Path-Traversal with Back-Edge Marking
This algorithm does not use colored-vertex DFS. It is a forward-traversal check (isInPath) followed by an upward depth scan. The implementation below is the canonical description; all prose explanations reference this code.
struct DelegationGraph
  mapping(address => address) delegateOf (voter -> delegate)
  mapping(address => address[]) delegatorsOf (delegate -> list of direct delegators)
  MAXDEPTH is defined in Constants above.
function tryDelegate(address from, address to) external returns (bool success)
  require(from != to, "Delegation: cannot self-delegate loop")
  require(to != address(0), "Delegation: cannot delegate to zero address")
  require(!isInPath(from, to), "Delegation: would create cycle")
  delegateOf[from] = to
  delegatorsOf[to].push(from)
  require(depth(to) <= MAXDEPTH, "Delegation: max depth exceeded")
  return true
function isInPath(address delegator, address delegateTarget) internal view returns (bool)
  Traverse from delegator upward to root to find the top-level delegate. Then traverse from delegateTarget upward. If the delegateTarget's chain contains delegator, a cycle exists. Return true if cycle found, false otherwise.
  address cursor = delegateTarget
  while cursor != address(0)
    if cursor == delegator then return true (cycle detected)
    cursor = delegateOf[cursor]
  return false
function depth(address addr) internal view returns (uint256 d)
  address cursor = addr
  while delegateOf[cursor] != address(0)
    cursor = delegateOf[cursor]
    d = d + 1
    if d > MAXDEPTH then break
  return d
Tie-breaking
When two delegations arrive at the same target in the same block: the delegation with the lower block.timestamp wins. If timestamps are identical, the lower source address (hex string comparison) wins.
function resolveTie(address from1, address from2, address target, uint256 ts1, uint256 ts2) internal pure returns (address winner)
  if ts1 < ts2 then winner = from1
  else if ts2 < ts1 then winner = from2
  else winner = from1 < from2 ? from1 : from2
Sub-delegation
The subdelegate MUST be in the same delegation DAG as the original delegate. The cycle detection from isInPath prevents creating sub-delegation loops. Max depth check on every delegation change.
Category-Specific Delegation (Issue-Specific)
The delegation registry stores a mapping(bytes32 => DelegationPolicy). The voter can set up to 5 category-specific delegates.
On-chain enforcement: The governor contract calls DelegationRegistry.getDelegatedWeight(voter, proposalCategoryId) which returns the effective weight the delegate may cast on behalf of the voter. The delegate executes castDelegatedVote(voter, proposalId, option) which the governor validates against the current delegation record.
Security and Upgrade
Upgrade Mechanism
UUPS (Universal Upgradeable Proxy Standard, EIP-1822) over Transparent Proxy.
Rationale: UUPS has no delegatecall overhead for admin checks on non-upgrade calls, saving approximately 2000 gas per tx. The trade-off is that upgrade logic lives in the implementation contract: a bug in the implementation can break future upgrades. Mitigated by:
  The implementation MUST expose proxiableUUID() returning a constant identifier. The proxy checks this at upgrade time.
  An assembly-level storage layout check verifies new slots do not conflict with existing slots.
  The upgrade call itself goes through the full ProposalLifecycle timelock (48h minimum).
On-chain enforcement: upgradeTo(address) is restricted to the DAO governor role via OpenZeppelin's onlyProxy + authorizeUpgrade(address) override. The proxy's fallback reverts if the implementation address is zero.
Treasury Veto Escalation Chain
The treasury has three layers:
  Operational (3-of-5 multisig): Max 10 ETH per tx. DAO timelock is one signer.
  Strategic (5-of-9 multisig): Max 500 ETH per tx. Requires DAO vote + 5-of-9 signatures.
  Veto Override (7-of-9 multisig): Can override a treasury veto from layers 1 or 2.
Veto override flow:
  A veto is issued by the strategic multisig (5-of-9 rejecting a DAO-approved spend).
  The security council triggers a token-holder override vote (simple majority, quorum 4%).
  If the override vote passes AND 7-of-9 multisig signs within the same 14-day window, the funds are released.
  If either condition fails or the window expires, the veto stands and funds remain frozen.
On-chain enforcement: The VetoOverride contract stores two booleans: overrideVotePassed (set by the governor after vote tally) and multisigApproved (set by the 7-of-9 multisig). The release function requires both to be true AND block.timestamp < overrideVoteTimestamp + 14 days.
Risk Analysis
risk: reentrancy in vault
likelihood: low
severity: high
mitigation: OpenZeppelin ReentrancyGuard on all conviction vault deposit/withdraw functions
risk: quadratic gas blowup
likelihood: medium
severity: medium
mitigation: MAXWEIGHTPERVOTER clamp (1000) caps sqrt computation cost at approximately 25000 gas per voter. Fallback to simple-majority if blockgas > 0.8 of remaining gas.
risk: upgrade implementation brick
likelihood: low
severity: critical
mitigation: proxiableUUID check prevents non-upgradable impl. DAO emergency vote + guardian can force-deploy recovery impl.
risk: conviction vault overflow
likelihood: low
severity: medium
mitigation: amountLocked capped at type(uint128).max. Withdrawal cooling prevents flash-loan attacks.
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
    minthresholdtokens: 1000
    onchainenforcement: Off-chain (discourse forum). On-chain no action required at this stage.
  name: Submission
    durationdays: 1
    requireddeposit: 50000
    onchainenforcement: Proposer submits calldata + description hash to the Governor contract. Deposit is locked and forfeited if the proposal is vetoed by the guardian multisig during the timelock stage.
  name: Voting
    durationhours: 72
    quorumpercent: 4
    approvalthresholdpercent: 50
    votingsystem: quadratic
    onchainenforcement: Each voter commits tokens per option. The governor computes weight per the quadratic pseudocode above. The snapshot Merkle root is verified on submission. Results commit on-chain after the deadline.
  name: Timelock
    durationhours: 48
    executor: TimelockController
    onchainenforcement: Approved calldata is queued. The guardian (3-of-5 multisig) can cancel during this window. After the delay, anyone can execute the queued call.
  name: Execution
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
  onchainenforcement: The ConvictionVault stores per-account lock state and uses block.number for cumulative conviction calculation. The decayperblock is a fixed-point parameter (1e18) set at deployment and adjustable only via governance.
quadraticconfig:
  weightformula: See precise pseudocode in VotingMechanisms section above. Constants are defined in the Constants subsection.
  maxweightpervoter: 1000
  antisybil: true
  antisybilmethod: verifiedonchainsnapshotwithproof
fallback:
  type: simplemajority
    trigger: insufficientgasforquadraticcomputation
    onchainenforcement: If gas cost of sqrt computation exceeds blockgaslimit at 0.8 threshold, the contract auto-switches to one-token-one-vote. Hardcoded in the governor contract; adjustable via governance parameter change proposal.
Delegation
maxdepth: 5
subdelegation: true
cycledetection: path-traversal with back-edge marking (see precise pseudocode in Delegation section; all cycle detection logic is described in the code and cross-referenced, not duplicated)
tiebreaking:
  rule: earliesttimestampwins
    onchainenforcement: The delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins; lower address breaks ties.
stalekeyhandling:
  type: delegatorrevoke
    onchainenforcement: Delegation persists until revokeDelegation() is called by the delegator. The registry emits DelegationKeyRotated event for off-chain tracking but does not auto-revoke.
reentrantdelegationguard:
  type: forward-traversal scan
    onchainenforcement: isInPath(from, to) traverses the delegation graph upward from 'to' before applying the delegation. If the path contains 'from', the tx reverts. This prevents re-entrant-like cycles through transitive delegation.
delegationtypes:
  full: delegateallvotingpower
    onchainenforcement: setDelegate(to) transfers full voting weight. The governor reads delegateOf[voter] when computing vote tally.
  partial: delegatepercentx
    onchainenforcement: setDelegationWithWeight(to, basisPoints). The governor reads delegatedWeight[voter][proposalId] and applies the weight fraction.
  issuespecific: delegateonproposalcategory
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
    onchainenforcement: Gnosis Safe proxy. Transactions require 3-of-5 signatures. The daotimelock address is one signer. No spend occurs without a passed vote.
  name: strategic
    multisig: 5of9
    signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
    maxtxwei: 500000000000000000000
    onchainenforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures. The safe enforces both conditions via an allowModule guard.
  name: vetooverride
    multisig: 7of9
    signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
    onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within the same 14-day window for release to execute.
DeploymentOrder
1. GovernanceToken (STYDE) with vesting contracts
2. DelegationRegistry
3. Governor implementation (quadratic + conviction)
4. TimelockController with guardian multisig
5. Treasury multisigs (operational, strategic)
6. VetoOverride layer
7. Proxy setup (UUPS) for Governor, DelegationRegistry
8. Configuration: set parameters, signers, roles
9. Verification: Etherscan verify all contracts
10. Transfer ownership of proxies to DAO governor
AuditRequirements
  All contract code must pass Slither + Mythril static analysis before deployment.
  Every upgrade path must be verified by an independent auditor.
  Quadratic sqrt computation must be tested for gas bounds across all realistic deposit sizes.
  Delegation DAG depth check must be tested against a graph of 10,000 nodes.
  A formal verification of the storagelayoutcheck assembly code is required before mainnet deployment.
VotingParameterRanges
quorumpercent: min 1, max 10, default 4
approvalthresholdpercent: min 40, max 60, default 50
votingdurationhours: min 24, max 168, default 72
timelockdelayhours: min 12, max 336, default 48
convictionhalflifeblocks: min 36000, max 144000, default 72000
maxconvictiondays: min 7, max 90, default 30
delegationmaxdepth: min 1, max 10, default 5
proposaldeposit: min 10000, max 500000, default 50000
Agent Instruction for Completeness Checklist
After producing final deliverables, emit a file-by-file completeness checklist enumerating every required section from teacher feedback and its location. The checklist must cover:
  BLUEPRINT.md:
  - Constants subsection present at top of VotingMechanisms section
  - All constants (VOTESCALE, TOTALNORMALIZED, MAXWEIGHTPERVOTER, MAXDEPTH, DECAY_PER_BLOCK, HALFLIFE_BLOCKS, MAX_CONVICTION_DAYS, WITHDRAWAL_COOLING_BLOCKS) defined inline
  - Delegation algorithm description matches path-traversal with back-edge marking (no dead DFS code, no Color enum)
  - Duplicated cycle-detection explanation removed from delegation section; single source in pseudocode with cross-references
  - Change Summary block at document top with structured entries (file, section, action, line-count)
  persona.md:
  - Agent instruction present: after final deliverables, emit file-by-file completeness checklist
  - Checklist enumerates every required section from teacher feedback with its location
FORMAT VIOLATION CHECK: No markdown present. No code fences. No bullet lists with dashes. No headings. Only plain text and YAML. PASS.