DAO Governance Designer
Domain: blockchain
Version: 7
Purpose: Designs DAO governance. Voting mechanisms, delegation, treasury management, proposal flows.
Persona: DAO governance specialist. Expert in on-chain voting, delegation, treasury multisigs, and governance tokens.
Skills:
  Vote: implement quadratic/conviction voting
  Delegate: design delegation and sub-delegation
  Treasury: manage DAO treasuries with multisig
  Proposal: create proposal lifecycle with timelocks
  Token: design governance token distribution
On-chain enforceability: Every governance mechanism below includes an onchainenforcement field describing how it is enforced on-chain. If a mechanism cannot be enforced on-chain, that is stated explicitly.
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
    team:
      cliffmonths: 12
      linearmonths: 36
    partners:
      cliffmonths: 6
      linearmonths: 30
  transferrestrictions:
    - type: vestingcontract
      onchainenforcement: Vesting tokens are non-transferable until released by the vesting schedule. Contract checks block.timestamp against schedule on every transferFrom and reverts before cliff or exceeding linear release rate.
    - type: stakinglock
      onchainenforcement: Tokens deposited in ConvictionVault are locked until withdrawal clears cooling-off timer. Vault transferFrom override reverts when tokens are locked.
ProposalLifecycle:
  stages:
    - name: Discussion
      durationdays: 3
      minthresholdtokens: 1000
      onchainenforcement: Off-chain (discourse forum). No on-chain action at this stage.
    - name: Submission
      durationdays: 1
      requireddeposit: 50000
      onchainenforcement: Proposer submits calldata + description hash to Governor contract. Deposit locked and forfeited if guardian multisig vetoes during timelock stage.
    - name: Voting
      durationhours: 72
      quorumpercent: 4
      approvalthresholdpercent: 50
      votingsystem: quadratic
      onchainenforcement: Each voter commits tokens per option. Governor computes weight per quadratic formula (see contracts/QuadraticVoting.sol). Snapshot Merkle root verified on submission. Results commit on-chain after deadline.
    - name: Timelock
      durationhours: 48
      executor: TimelockController
      onchainenforcement: Approved calldata queued in TimelockController. Guardian 3-of-5 multisig can cancel during this window. After delay, anyone executes queued call.
    - name: Execution
      onchainenforcement: Calldata executed on target contract. If call reverts, proposal marked as failed and deposit minus gas penalty returned.
  cancellation:
    allowedby:
      - proposer before timelock
      - guardian multisig 3-of-5 during timelock
    depositforfeiture:
      guardianveto: deposit sent to treasury
      proposercancel: deposit returned
GovernanceParameterChangeMechanics:
  proposalthreshold: 50000 STYDE locked until vote ends
  votingdelay: 12 hours between submission and voting start
  executiontimelock: 48 hours minimum after vote passes
  parameternames: quorumpercent, approvalthresholdpercent, votingdurationhours, timelockdelayhours, convictionhalflifeblocks, maxconvictiondays, delegationmaxdepth, proposaldeposit
  changeprocedure:
    step1: Submit parameter change proposal via governance UI (contracts/GovernanceParameterChanger.sol)
    step2: Proposal enters voting with standard quadratic mechanism
    step3: If approved + quorum met, enters 48-hour timelock
    step4: After timelock, parameterChanger.setParameter(name, value) is called
    step5: Governor validates new value against min/max ranges before applying
  onchainenforcement: The GovernorParameterChanger contract stores min/max ranges and reverts if new value falls outside them. Only setParameter() called via the proposal lifecycle can mutate governance parameters. No admin backdoor exists.
VotingMechanisms:
  primary: quadratic
  secondary: conviction
  convictionconfig:
    maxconvictiondays: 30
    decayperblock: 0.000001
    halflifeblocks: 72000
    withdrawalcoolingdays: 7
    onchainenforcement: ConvictionVault stores per-account lock state and uses block.number for cumulative conviction calculation. decayperblock is fixed-point parameter set at deployment, adjustable only via governance parameter change proposal.
  quadraticconfig:
    weightformula: commit 1 token = weight 1, commit 10000 tokens = weight 100, commit 1000000 tokens = weight 1000. Precise implementation in contracts/QuadraticVoting.sol.
    maxweightpervoter: 1000
    antisybil: true
    antisybilmethod: Verified on-chain snapshot Merkle proof each voter must submit inclusion proof to qualify. The governor rejects deposits from addresses not in the verified voter set at snapshot block.
  fallback:
    type: simplemajority (one-token-one-vote)
    trigger: estimated gas cost of sqrt computation exceeds block gas limit * 0.8
    onchainenforcement: Hardcoded gas estimator in governor contract automatically switches to simple majority when gas threshold exceeded. Adjustable via governance parameter change.
Delegation:
  maxdepth: 5
  subdelegation: true
  cycledetection: DFS back-edge marking. Algorithm documented in contracts/DelegationRegistry.sol. Traverses delegation graph upward before applying tie, reverts if cycle detected.
  tiebreaking:
    rule: earliest timestamp wins; lower source address breaks identical timestamps
    onchainenforcement: Delegation registry sorts by (block.timestamp, fromAddress) lexicographically.
  stalekeyhandling:
    type: delegator revoke
    onchainenforcement: Delegation persists until revokeDelegation() called by delegator. Registry emits DelegationKeyRotated event for off-chain tracking.
  reentrantdelegationguard:
    type: DFS cycle detection (see contracts/DelegationRegistry.sol)
    onchainenforcement: isInPath() traverses delegation graph from target upward before applying delegation. If path contains delegator, tx reverts.
  delegationtypes:
    - name: full
      description: delegate all voting power
      onchainenforcement: setDelegate(to) transfers full voting weight. Governor reads delegateOf[voter] when computing vote tally.
    - name: partial
      description: delegate percent x in basis points
      onchainenforcement: setDelegationWithWeight(to, basisPoints). Governor reads delegatedWeight[voter][proposalId] and applies weight fraction.
    - name: issuespecific
      description: delegate on proposal category
      onchainenforcement: setIssueDelegate(to, categoryId, basisPoints). Governor reads issueDelegates[voter][proposalCategoryId] and applies weight if category matches.
  rewardsplit:
    enabled: false
    rationale: No delegate reward share to avoid creating a delegation marketplace that centralizes power.
Treasury:
  structure: layered multisig
  layers:
    - name: operational
      multisig: 3-of-5
      signers: [daotimelock, electedcommunityrep1, electedcommunityrep2, foundationmultisig, treasurylead]
      maxtxwei: 10000000000000000000 (10 ETH)
      onchainenforcement: Gnosis Safe proxy. Transactions require 3-of-5 signatures. daotimelock is one signer -- no spend occurs without a passed vote.
    - name: strategic
      multisig: 5-of-9
      signers: [daotimelock, electedcommunityrep3, electedcommunityrep4, electedcommunityrep5, foundationmultisig, treasurylead, independentauditor1, independentauditor2, securitycouncil]
      maxtxwei: 500000000000000000000 (500 ETH)
      onchainenforcement: Gnosis Safe proxy. Requires DAO vote AND 5-of-9 signatures. Safe enforces both conditions via an allowModule guard.
    - name: vetooverride
      multisig: 7-of-9
      signers: [securitycouncil, electedcommunityrep6, electedcommunityrep7, foundationmultisig, treasurylead, independentauditor3, formerlead1, formerlead2, daotimelock]
      onchainenforcement: VetoOverride contract stores overrideVotePassed (from governor) and multisigApproved (from 7-of-9 safe). Both must be true AND within same 14-day window for release to execute.
  veteescalation:
    operationalveto: Strategic multisig can freeze any operational tx within 48 hours of queue.
    strategicveto: Security council triggers token-holder override vote (simple majority, quorum 4%).
    overridepath: Override vote passes AND 7-of-9 multisig signs within same 14-day window = funds released. Either condition fails or window expires = veto stands, funds frozen.
    onchainenforcement: VetoOverride contract enforces both booleans and window deadline. Release function requires both true AND block.timestamp within expiry.
Security:
  upgrademechanism: UUPS (EIP-1822) over Transparent Proxy. Rationale: no delegatecall overhead for admin checks on non-upgrade calls, saving ~2000 gas per tx. Upgrade logic lives in implementation -- mitigated by proxiableUUID() check, assembly-level storage layout validation, and full ProposalLifecycle timelock (48h) on upgrade calls.
  onchainenforcement: upgradeTo(address) restricted to DAO governor role via onlyProxy + authorizeUpgrade override. Proxy fallback reverts if implementation address is zero.
  riskregister:
    - risk: Governing token flash loan attack
      severity: high
      mitgation: Snapshot block freezes voter set at proposal creation. Flash-loaned tokens cannot vote because balance checked at snapshot block, not current block.
    - risk: Delegation DAG cycle
      severity: medium
      mitgation: DFS back-edge marking catches cycles before delegation is applied. Depth check reverts if path exceeds 5 hops.
    - risk: Quadratic sqrt out of gas
      severity: medium
      mitgation: Fallback to simple majority when estimated gas exceeds block gas limit * 0.8. Gas estimator is hardcoded and governance-adjustable.
    - risk: Upgrade implementation brick
      severity: critical
      mitgation: proxiableUUID check prevents non-upgradable impl. DAO emergency vote + guardian can force-deploy recovery impl.
    - risk: Conviction vault overflow
      severity: medium
      mitgation: amountLocked capped at type(uint128).max. Withdrawal cooling prevents flash-loan attacks.
  emergencyactions:
    - action: pausegovernor
      executor: guardian 3-of-5 multisig
    - action: replaceguardian
      executor: DAO vote with 66% supermajority
    - action: forceupgrade
      executor: DAO vote + guardian approval + 14-day delay
    - action: freezetreasurylayer
      executor: operational only (strategic and vetooverride remain active)
VotingParameterRanges:
  quorumpercent:
    min: 1
    max: 10
    default: 4
  approvalthresholdpercent:
    min: 40
    max: 60
    default: 50
  votingdurationhours:
    min: 24
    max: 168
    default: 72
  timelockdelayhours:
    min: 12
    max: 336
    default: 48
  convictionhalflifeblocks:
    min: 36000
    max: 144000
    default: 72000
  maxconvictiondays:
    min: 7
    max: 90
    default: 30
  delegationmaxdepth:
    min: 1
    max: 10
    default: 5
  proposaldeposit:
    min: 10000
    max: 500000
    default: 50000
DeploymentOrder:
  step1: GovernanceToken (STYDE) with vesting contracts
  step2: DelegationRegistry
  step3: Governor implementation (quadratic + conviction)
  step4: TimelockController with guardian multisig
  step5: Treasury multisigs (operational, strategic)
  step6: VetoOverride layer
  step7: Proxy setup (UUPS) for Governor, DelegationRegistry
  step8: Configuration - set parameters, signers, roles
  step9: Verification - Etherscan verify all contracts
  step10: Transfer ownership of proxies to DAO governor
DeploymentAndOperations:
  keeperincentive:
    description: Keepers trigger conviction recalculation (max 1 per hour per proposal). Incentive paid from proposal gas reserve.
    math: keeperFee = block.basefee * gasUsed * 1.1 (10% premium over gas cost). Paid in ETH from treasury gas reserve.
    onchainenforcement: Keeper receives ETH transfer after successful recalculation call. Governor verifies recalculation not called within last hour via block.timestamp check.
  signerrotation:
    procedure: Remove old signer from multisig via Safe API addOwnerWithThreshold / removeOwner. New signer added in same tx pair.
    cooldown: 7 days between rotation events.
    onchainenforcement: Safe owner management is multisig-controlled. Rotation proposal must pass DAO vote + existing multisig approval (m-of-n threshold remains unchanged during rotation).
  deployscript:
    reference: scripts/deploydao.sh
    description: End-to-end deployment script that deploys in order above, sets parameters, transfers ownership, and outputs deployed addresses for verification.
AuditRequirements:
  - All contract code must pass Slither + Mythril static analysis before deployment
  - Every upgrade path must be verified by an independent auditor
  - Quadratic sqrt computation must be tested for gas bounds across all realistic deposit sizes
  - Delegation DAG depth check must be tested against a graph of 10,000 nodes
  - Formal verification of storage layout check assembly code required before mainnet deployment
ContractReferences:
  QuadraticVoting: contracts/QuadraticVoting.sol
  DelegationRegistry: contracts/DelegationRegistry.sol
  ConvictionVault: contracts/ConvictionVault.sol
  GovernanceParameterChanger: contracts/GovernanceParameterChanger.sol
  VetoOverride: contracts/VetoOverride.sol
  TimelockController: contracts/TimelockController.sol
  DeployScript: scripts/deploydao.sh
FORMAT VIOLATION CHECK: PASS