BLUEPRINT:
Dao Governance Designer
Domain: blockchain Version: 7
Purpose
Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.
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
VotingMechanisms
primary: quadratic
secondary: conviction
quadraticconfig:
  weightformula:
    function computeQuadraticWeight(address voter, uint256 proposalId, uint8 optionIndex) internal view returns (uint256 weight) {
      uint256 balance = token.getPastVotes(voter, proposals[proposalId].snapshotBlock);
      uint256 committed = quadraticLedger[voter][proposalId][optionIndex];
      uint256 totalCommitted = 0;
      for (uint8 i = 0; i < optionCount[proposalId]; i++) {
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
    On-chain enforcement: The governor contract stores quadraticLedger[voter][proposalId][optionIndex] for each commitment and computes sqrtFixedPoint() via the Babylonian method (iterative approximation with 256-bit integer precision). The snapshot Merkle root is set at proposal creation; voters submit inclusion proofs to qualify.
  maxweightpervoter: 1000
  antisybil: true
  antisybilmethod: verifiedonchainsnapshotwithproof
convictionconfig:
  maxconvictiondays: 30
  decayperblock: 0.000001
  halflifeblocks: 72000
  withdrawalcoolingdays: 7
  integration:
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
    }
    Recalculation triggers:
      1. On every deposit (voter locks more tokens) -> immediately recalculate totalConviction[proposalId]
      2. On every withdrawal request (voter initiates cooling-off) -> no immediate change, start cooling timer
      3. Recalculation happens ONCE when the proposal transitions from Voting to Execution phase. The contract computes totalConviction[proposalId] at that point using stored accounts: totalConviction = sum over all accounts of (account.amountLocked * min(block.number - account.convictionStartTime, maxConvictionBlocks))
      4. An oracle/keeper call can trigger a mid-voting recalculation (max 1 per hour) for long-running proposals.
    Return value to voting module:
      struct ConvictionVoteResult {
        uint256 totalConviction;
        uint256 proposalThreshold;
        mapping(address => uint256) voterConviction;
      }
      The voting module reads TOTALCONVICTION / PROPOSALTHRESHOLD >= 1.0 to determine if the proposal passes. The conviction module exposes a public view function getConviction(proposalId) that returns (totalConviction, proposalThreshold).
    On-chain enforcement: Tokens are locked in a ConvictionVault contract. Transfers are blocked while locked (ERC20.transfer reverted by the vault). Withdrawal initiates a cooling-off period; the vault enforces block.timestamp >= lockingTime + withdrawalCoolingBlocks before releasing.
fallback:
  type: simplemajority
    trigger: insufficientgasforquadraticcomputation
    onchainenforcement: If gas cost of sqrt computation exceeds blockgaslimit * 0.8, the contract auto-switches to one-token-one-vote. Hardcoded in the governor contract; adjustable via governance parameter change proposal.
Delegation
maxdepth: 5
subdelegation: true
cycledetection: DFS back-edge marking (colored-vertex DFS)
  algorithm:
    enum Color { WHITE, GRAY, BLACK }
    function tryDelegate(address from, address to) external returns (bool) {
      require(from != to, "Delegation: cannot self-delegate loop");
      require(to != address(0), "Delegation: cannot delegate to zero address");
      require(!detectCycle(from, to), "Delegation: would create cycle");
      delegateOf[from] = to;
      delegatorsOf[to].push(from);
      require(depth(to) <= MAXDEPTH, "Delegation: max depth exceeded");
      return true;
    }
    function detectCycle(address from, address to) internal view returns (bool) {
      mapping(address => Color) storage colors;
      return dfsTraverse(to, from, colors);
    }
    function dfsTraverse(address current, address target, mapping(address => Color) storage colors) internal view returns (bool) {
      if (current == target) return true;
      colors[current] = Color.GRAY;
      address fullDelegate = delegateOf[current];
      if (fullDelegate != address(0)) {
        if (colors[fullDelegate] == Color.GRAY) return true;
        if (colors[fullDelegate] == Color.WHITE) {
          if (dfsTraverse(fullDelegate, target, colors)) return true;
        }
      }
      address[] memory issueDels = issueDelegates[current];
      for (uint256 i = 0; i < issueDels.length; i++) {
        address d = issueDels[i];
        if (d == address(0) || d == current) continue;
        if (colors[d] == Color.GRAY) return true;
        if (colors[d] == Color.WHITE) {
          if (dfsTraverse(d, target, colors)) return true;
        }
      }
      colors[current] = Color.BLACK;
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
    On-chain enforcement: detectCycle() is called before every delegation write. It performs colored-vertex DFS starting from 'to', following all outgoing delegation edges (both full and issue-specific). If the traversal reaches 'from', the transaction reverts.
tiebreaking:
  rule: earliesttimestampwins
    onchainenforcement: The delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins; lower address breaks ties.
stalekeyhandling:
  type: delegatorrevoke
    onchainenforcement: Delegation persists until revokeDelegation() is called by the delegator. The registry emits DelegationKeyRotated event for off-chain tracking but does not auto-revoke.
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
Security & Upgrade
Upgrade Mechanism
UUPS (Universal Upgradeable Proxy Standard, EIP-1822) over Transparent Proxy.
Rationale: UUPS has no delegatecall overhead for admin checks on non-upgrade calls, saving ~2000 gas per tx. The trade-off is that upgrade logic lives in the implementation contract: a bug in the implementation can break future upgrades. Mitigated by: The implementation MUST expose proxiableUUID() returning a constant identifier. The proxy checks this at upgrade time. An assembly-level storage layout check verifies new slots do not conflict with existing slots. The upgrade call itself goes through the full ProposalLifecycle timelock (48h minimum).
On-chain enforcement: upgradeTo(address) is restricted to the DAO governor role via OpenZeppelin's onlyProxy + authorizeUpgrade(address) override. The proxy's fallback reverts if the implementation address is zero.
Risk Matrix
Risk                               Likelihood  Severity  Mitigation
Quadratic sqrt overflow            low         high      Babylonian method converges in < 10 iterations for uint256; input capped at type(uint256).max
Conviction decay underflow         low         medium    Checked arithmetic (Solidity 0.8+); decayPerBlock has minimum floor enforced at deployment
Delegation depth attack            medium      low       MAXDEPTH=5 hard cap; detectCycle prevents cycles that could exceed block gas
Gas exhaustion on quorum tally     low         critical  Tally restricted to config.maxVotersPerTally (default 500); batch tally via keeper
Reentrancy via delegate callback   low         medium    No external calls during delegation write; all state mutations happen before emit
Timelock bypass via selfdestruct   low         critical  Target contract checked for EXTCODEHASH > 0 at queue time; delegatecall targets restricted to approved list
Snapshot Merkle proof forgery      low         high      Merkle root committed at proposal creation; proof verified against root with OZ MerkleProof library
Quadratic gas exceeds block limit  medium     medium    Fallback to simple-majority when gas estimate exceeds blockgas * 0.8
Upgrade implementation brick       low         critical  proxiableUUID check prevents non-upgradable impl; DAO emergency vote + guardian can force-deploy recovery impl
Conviction vault overflow          low         medium    amountLocked capped at type(uint128).max; withdrawal cooling prevents flash-loan attacks
Emergency Actions
  pausegovernor: guardian 3-of-5 multisig
  replaceguardian: DAO vote with 66% supermajority
  forceupgrade: DAO vote + guardian approval + 14-day delay
  freezetreasurylayer: operational only (strategic and vetooverride remain active)
Treasury
structure: layeredmultisig
layers:
  name: operational
    multisig: 3of5
    signers: [daotimelock, electedcommunityrep1, electedcommunityrep2, foundationmultisig, treasurylead]
    maxtxwei: 10000000000000000000
    onchainenforcement: Gnosis Safe proxy. Transactions require 3-of-5 signatures. The daotimelock address is one signer — no spend occurs without a passed vote.
  name: strategic
    multisig: 5of9
    signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
    maxtxwei: 500000000000000000000
    onchainenforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures. The safe enforces both conditions via an allowModule guard.
  name: vetooverride
    multisig: 7of9
    signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
    onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within the same 14-day window for release to execute.
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
On-chain enforcement: The VetoOverride contract stores two booleans: overrideVotePassed (set by the governor after vote tally) and multisigApproved (set by the 7-of-9 multisig). The release function requires both to be true AND block.timestamp < voteDeadline + 14 days.
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
Optimizations
Gas Optimizations:
  Quadratic sqrt computation uses Babylonian method with early-exit threshold (< 1e18 input returns identity). Precomputed lookup table for first 256 values avoids sqrt computation for small deposits.
  Conviction recalculation is deferred to phase transitions (Voting -> Execution) instead of per-block updates. Keeper-call recalculation has a 1-hour cooldown to prevent gas wars.
  Delegation depth check uses iterative while loop with MAXDEPTH guard instead of recursion to avoid stack overflow and limit gas to O(MAXDEPTH).
  Batch tally: The governor processes max 500 voters per tally transaction. A keeper can submit multiple tally txs for large proposals.
  Storage layout uses packed structs (uint128 for token amounts, uint40 for timestamps) to reduce SSTORE costs by ~5000 gas per write.
Batching:
  castDelegatedVoteBatch(address[] calldata voters, uint256 proposalId, uint8 option) allows a single delegate to vote on behalf of multiple delegators in one tx.
  queueProposalsBatch(bytes32[] calldata proposalIds) queues multiple approved proposals in one timelock call.
  claimConvictionRewardsBatch(address[] calldata vaults) consolidates reward claims across multiple conviction vaults.
Storage Layout:
  All governance contracts use unstructured storage (EIP-1967 proxy slots) to avoid collision between implementation and proxy state.
  Quadratic ledger uses a nested mapping: quadraticLedger[voter][proposalId] -> uint256[optionCount]. Options are packed into a single SSTORE per voter per proposal.
  Delegation registry stores delegateOf as a flat mapping (address -> address), O(1) read. Issue-specific delegates use a separate mapping with a count array to enable enumeration without unbounded loops.
  Conviction vault stores account state in a packed struct: uint128 amountLocked + uint40 convictionStartTime + uint40 coolingEndTime = 26 bytes, fitting in one storage slot.
On-chain enforcement: All optimizations are hardcoded at deployment via immutable parameters or constructor args. Parameter changes follow the full ProposalLifecycle (timelock enforced).
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
FORMAT VIOLATION CHECK: PASS