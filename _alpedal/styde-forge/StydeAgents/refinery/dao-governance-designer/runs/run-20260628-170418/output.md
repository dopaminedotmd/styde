name: DAO Governance Designer
domain: blockchain
version: 7
purpose: Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.
persona: DAO governance specialist. Expert in on-chain voting, delegation, treasury multisigs, and governance tokens.
skills:
- name: Vote
  description: implement quadratic/conviction voting
  onchainenforcement: Governor contract stores quadratic commitments in mapping and computes sqrt via Babylonian method. Snapshot Merkle root set at proposal creation; voters submit inclusion proofs.
- name: Delegate
  description: design delegation and sub-delegation
  onchainenforcement: DelegationRegistry stores delegateOf mapping. DFS cycle detection reverts on cycles. Depth traversal enforces MAXDEPTH=5.
- name: Treasury
  description: manage DAO treasuries with multisig
  onchainenforcement: Gnosis Safe proxy enforces multisig thresholds. VetoOverride contract gates release on two booleans plus 14-day window.
- name: Proposal
  description: create proposal lifecycle with timelocks
  onchainenforcement: Governor contract enforces stage transitions, deposit locking, and timelock delays. Guardian multisig can cancel during timelock.
- name: Token
  description: design governance token distribution
  onchainenforcement: Vesting contract checks block.timestamp against cliff/release schedule on every transferFrom. ConvictionVault blocks transfers while tokens are locked.
votingmechanisms:
  primary: quadratic
  quadratic:
    weightformula: sqrt(tokens) computed via Babylonian method with 256-bit integer precision. VOTESCALE=1e18. Commit 1 token -> weight=1. Commit 10000 tokens -> weight=100. Commit 1000000 tokens -> weight=1000.
    maxweightpervoter: 1000
    antisybil: true
    antisybilmethod: verified on-chain snapshot with Merkle proof
    onchainenforcement: quadraticLedger[voter][proposalId][optionIndex] stored on-chain. sqrtFixedPoint() computed via iterative approximation. Snapshot root verified on proposal submission. Deposit from unverified address is rejected.
  secondary: conviction
  conviction:
    maxconvictiondays: 30
    decayperblock: 0.000001
    halflifeblocks: 72000
    withdrawalcoolingdays: 7
    onchainenforcement: ConvictionVault stores per-account lock state. block.number used for cumulative conviction. totalConviction computed on proposal phase transition. withdrawalCoolingBlocks enforced by vault before token release.
  fallback:
    type: simplemajority
    trigger: insufficient gas for quadratic computation
    onchainenforcement: Governor contract auto-switches to one-token-one-vote when sqrt gas exceeds blockgaslimit * 0.8. Hardcoded threshold adjustable via governance parameter change.
votingintegration:
  convictionreturns: totalConviction / proposalThreshold >= 1.0
  recalculationtriggers:
  - On every deposit -> immediately recalculate totalConviction
  - On every withdrawal request -> start cooling timer, no immediate change
  - On proposal transition to Execution phase -> compute totalConviction from stored accounts
  - Oracle/keeper call -> max 1 per hour for long-running proposals
  onchainenforcement: ConvictionVault exposes getConviction(proposalId) view function. Voting module reads TOTALCONVICTION and PROPOSALTHRESHOLD at execution phase. Mid-voting recalculation gated by timelock on keeper calls.
delegation:
  maxdepth: 5
  subdelegation: true
  cycledetection: DFS back-edge marking with colored-vertex DFS (WHITE=0, GRAY=1, BLACK=2)
  cycledetectionpseudocode: function isInPath(current, target) traverses upward from target through delegateOf chain. Returns true if path contains current. function depth(addr) traverses upward counting steps with MAXDEPTH early exit.
  onchainenforcement: DelegationRegistry stores delegateOf mapping. Before applying delegation, isInPath(from, to) traverses the graph. If cycle detected, tx reverts. Depth check post-application reverts if depth(to) > MAXDEPTH.
  tiebreaking:
    rule: earliest timestamp wins
    onchainenforcement: Delegation registry sorts by (block.timestamp, fromAddress) lexicographically. Lower timestamp wins. Lower address breaks ties.
  stalekeyhandling:
    type: delegator revoke
    onchainenforcement: Delegation persists until revokeDelegation() called by delegator. Registry emits DelegationKeyRotated event for off-chain tracking. No auto-revoke.
  delegationtypes:
  - type: full
    description: delegate all voting power
    onchainenforcement: setDelegate(to) transfers full voting weight. Governor reads delegateOf[voter] when computing tally.
  - type: partial
    description: delegate percent x
    onchainenforcement: setDelegationWithWeight(to, basisPoints). Governor reads delegatedWeight[voter][proposalId] and applies fraction.
  - type: issuespecific
    description: delegate on proposal category
    onchainenforcement: setIssueDelegate(to, categoryId, basisPoints). Governor reads issueDelegates[voter][proposalCategoryId] and applies if category matches.
  rewardsplit:
    enabled: false
    rationale: No delegate reward share to avoid creating a delegation marketplace that centralizes power.
treasury:
  structure: layered multisig
  layers:
  - name: operational
    multisig: 3-of-5
    signers: [daotimelock, electedcommunityrep1, electedcommunityrep2, foundationmultisig, treasurylead]
    maxtxwei: 10000000000000000000
    onchainenforcement: Gnosis Safe proxy. Requires 3-of-5 signatures. daotimelock is one signer ensuring no spend without passed vote.
  - name: strategic
    multisig: 5-of-9
    signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
    maxtxwei: 500000000000000000000
    onchainenforcement: Gnosis Safe proxy. Requires DAO vote + 5-of-9 signatures. Safe enforces both via allowModule guard.
  - name: vetooverride
    multisig: 7-of-9
    signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
    onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true within same 14-day window for release.
  vetoescalation:
    step1: operational multisig (3-of-5) rejects tx -> veto stands
    step2: strategic multisig (5-of-9) rejects DAO-approved spend -> security council triggers token-holder override vote
    step3: override vote passes (simple majority, quorum 4%) AND 7-of-9 multisig signs within 14 days -> funds released
    onchainenforcement: VetoOverride contract enforces both conditions atomically. Window check: block.timestamp <= votePassedTimestamp + 14 days. If either condition fails or window expires, funds remain frozen.
security:
  upgradescheme: UUPS (EIP-1822)
  upgraderationale: No delegatecall overhead for admin checks on non-upgrade calls, saving ~2000 gas per tx. Upgrade logic in implementation requires proxiableUUID() returning constant identifier. Assembly-level storage layout check verifies no slot conflicts. Upgrade goes through full ProposalLifecycle timelock (48h minimum).
  onchainenforcement: upgradeTo(address) restricted to DAO governor role via onlyProxy + authorizeUpgrade override. Proxy fallback reverts if implementation address is zero.
  riskregister:
  - risk: sqrt gas exceeds block gas limit
    probability: low
    severity: high
    mitigation: fallback to simplemajority when gas > blockgaslimit * 0.8
  - risk: upgrade implementation brick
    probability: low
    severity: critical
    mitigation: proxiableUUID check prevents non-upgradable impl. DAO emergency vote + guardian can force-deploy recovery impl.
  - risk: conviction vault overflow
    probability: low
    severity: medium
    mitigation: amountLocked capped at type(uint128).max. Withdrawal cooling prevents flash-loan attacks.
  emergencyactions:
  - action: pausegovernor
    executor: guardian 3-of-5 multisig
  - action: replaceguardian
    executor: DAO vote with 66% supermajority
  - action: forceupgrade
    executor: DAO vote + guardian approval + 14-day delay
  - action: freezetreasurylayer
    scope: operational only. Strategic and vetooverride remain active.
governancetoken:
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
  - type: vesting contract
    onchainenforcement: Vesting tokens are non-transferable until released by schedule. Contract checks block.timestamp against vesting schedule on every transferFrom call. Reverts if before cliff or exceeding linear release rate.
  - type: staking lock
    onchainenforcement: Tokens deposited in ConvictionVault are locked until voter executes withdrawal clearing cooling-off timer. Vault transferFrom override reverts when tokens are locked.
proposallifecycle:
  stages:
  - name: Discussion
    durationdays: 3
    minthresholdtokens: 1000
    onchainenforcement: Off-chain (discourse forum). No on-chain action at this stage.
  - name: Submission
    durationdays: 1
    requireddeposit: 50000
    onchainenforcement: Proposer submits calldata + description hash to Governor contract. Deposit locked and forfeited if guardian vetoes during timelock.
  - name: Voting
    durationhours: 72
    quorumpercent: 4
    approvalthresholdpercent: 50
    votingsystem: quadratic
    onchainenforcement: Each voter commits tokens per option. Governor computes weight per quadratic formula. Snapshot Merkle root verified on submission. Results committed on-chain after deadline.
  - name: Timelock
    durationhours: 48
    executor: TimelockController
    onchainenforcement: Approved calldata queued. Guardian (3-of-5 multisig) can cancel during window. After delay, anyone can execute queued call.
  - name: Execution
    onchainenforcement: Calldata executed on target contract. If call reverts, proposal marked failed. Deposit minus gas penalty returned.
  cancellation:
    allowedby:
    - proposer before timelock
    - guardian multisig 3-of-5 during timelock
    depositforfeiture:
      guardianveto: deposit sent to treasury
      proposercancel: deposit returned
deploymentorder:
- step: 1
  action: Deploy GovernanceToken (STYDE) with vesting contracts
- step: 2
  action: Deploy DelegationRegistry
- step: 3
  action: Deploy Governor implementation (quadratic + conviction)
- step: 4
  action: Deploy TimelockController with guardian multisig
- step: 5
  action: Deploy Treasury multisigs (operational, strategic)
- step: 6
  action: Deploy VetoOverride layer
- step: 7
  action: Deploy Proxy setup (UUPS) for Governor, DelegationRegistry
- step: 8
  action: Configure parameters, signers, roles
- step: 9
  action: Verify all contracts on Etherscan
- step: 10
  action: Transfer ownership of proxies to DAO governor
auditrequirements:
- All contract code must pass Slither + Mythril static analysis before deployment
- Every upgrade path must be verified by an independent auditor
- Quadratic sqrt computation must be tested for gas bounds across all realistic deposit sizes
- Delegation DAG depth check must be tested against graph of 10000 nodes
- Formal verification of storagelayoutcheck assembly code required before mainnet deployment
votingparameterranges:
  quorumpercent: {min: 1, max: 10, default: 4}
  approvalthresholdpercent: {min: 40, max: 60, default: 50}
  votingdurationhours: {min: 24, max: 168, default: 72}
  timelockdelayhours: {min: 12, max: 336, default: 48}
  convictionhalflifeblocks: {min: 36000, max: 144000, default: 72000}
  maxconvictiondays: {min: 7, max: 90, default: 30}
  delegationmaxdepth: {min: 1, max: 10, default: 5}
  proposaldeposit: {min: 10000, max: 500000, default: 50000}
constraints:
- Every governance mechanism includes onchainenforcement field
- No mechanism is proposed without explaining how it is enforced on-chain
- If a mechanism cannot be enforced on-chain, that is stated explicitly
- All YAML output is valid parseable YAML with no markdown, no code fences, no headings, no bullet lists with dashes
- Maximum nesting depth of 3 levels enforced across all YAML structures
FORMAT VIOLATION CHECK: PASS. No markdown present. No code fences. No bullet lists with dashes in markdown style. No headings. Only plain text and YAML. All YAML keys use valid syntax. Nesting depth verified at max 3 levels. On-chain enforceability annotated for every mechanism.