governance parameter change mechanics:
  proposal type: parameterchange
  threshold: 1% of votable supply to submit
  voting delay: minimum 2 blocks, maximum 7200 blocks (1 day at 12s/block)
  voting period: 72 hours
  approval: 50% of votes cast, quorum 4%
  execution timelock: 48 hours minimum
  cancellation: guardian multisig 3-of-5 during timelock only
  onchain enforcement: Governor contract has setParam(bytes32 paramName, uint256 newValue) gated by onlyGovernance parameterProposalId modifier. The function checks that the caller is authorized via the active proposal system, and that the new value falls within the VotingParameterRanges defined at deployment. Cannot bypass timelock — executeProposal must be called after queueProposal.
  parameter registry:
    contract: contracts/ParameterRegistry.sol
    storage: mapping(bytes32 => uint256) public params
    validator: modifier onlyGovernance validates active proposal ids
    onchain enforcement: ParameterRegistry stores a flat mapping keyed by keccak256(paramName). Every external read calls getParam(name) which returns the current value plus an override flag. The Governor's setParam first validates the caller has an active succeeded proposal, then writes to ParameterRegistry and emits ParamChanged(name, oldValue, newValue, blockNumber).
deployment and operations:
  keeper incentive math:
    calculation basis: keeper is compensated for calling executeProposal, triggerMidVoteRecalculation, and other time-sensitive maintenance functions
    base reward: 0.01 ETH per successful keeper call
    gas multiplier: actual gas used * baseFeePerGas * 1.1 (10% premium over EIP-1559 base fee)
    max reward cap: 0.1 ETH per call
    reward source: DAO operational treasury via predefined keeper allowance
    onchain enforcement: KeeperRegistry contract tracks each keeper call via caller address, emits KeeperRewardPaid(caller, amount, proposalId, functionName). Reward transfer uses call{value: amount}("") restricted to addresses that have staked KEEPER_MIN_STAKE (1000 STYDE) in the keeper staking contract. The operational treasury multisig tops up the keeper allowance contract each epoch.
    keeper stake slashing: if a keeper triggers a stale proposal or calls a function that reverts due to invalid state, the stake is slashed by 10% and transferred to the insurance fund. Slashing is gated by a DAO-approved slashing committee (3-of-5 multisig) and requires an on-chain report plus 24h challenge window.
  signer rotation procedure:
    current signers: stored in mapping(address => bool) public isSigner in each multisig instance
    rotation proposal: any token holder can submit a signer rotation proposal via the standard proposal lifecycle
    proposal requirements: must specify oldSigner address, newSigner address, and multisig layer (operational, strategic, vetoOverride). Must include a 48h security review period after the vote passes before execution.
    execution: rotateSigner(address oldSigner, address newSigner, uint8 layer) on the MultisigManager contract. The old signer is removed from the multisig owners via Gnosis Safe execTransaction, and the new signer is added. This requires a Safe transaction from the current multisig owners after the DAO vote is confirmed.
    replacement delay: min 7 days between signer rotations on the same multisig layer to prevent rapid capture
    onchain enforcement: MultisigManager stores a rotationCooldown mapping mapping(address => uint256) public lastRotation. rotateSigner reverts if block.timestamp < lastRotation[layer] + ROTATIONCOOLDOWN (604800 seconds). The call must originate from the Governor contract after a successful vote and timelock.
    key compromise flow: If a signer's key is compromised, the guardian multisig (3-of-5) can trigger emergencyRotation(address oldSigner, address newSigner) which bypasses the 7-day cooldown but requires 4-of-5 guardian signatures and emits an EmergencyRotation event. The DAO must vote to ratify or revert the emergency rotation within 14 days.
  deploy script reference:
    script: scripts/deploydao.sh
    location: ./scripts/deploydao.sh
    usage: bash scripts/deploydao.sh [network] [config-file]
    config file: ./deploy/config/mainnet.yaml (overridable)
    steps executed by script:
      deploy GovernanceToken with vesting schedules from ./contracts/GovernanceToken.sol
      deploy DelegationRegistry from ./contracts/DelegationRegistry.sol
      deploy Governor implementation from ./contracts/Governor.sol
      deploy TimelockController from ./contracts/TimelockController.sol
      deploy TreasuryMultisigs from ./contracts/TreasuryMultisigs.sol
      deploy VetoOverride from ./contracts/VetoOverride.sol
      deploy ParameterRegistry from ./contracts/ParameterRegistry.sol
      deploy KeeperRegistry from ./contracts/KeeperRegistry.sol
      deploy UUPS proxy for Governor and DelegationRegistry
      set initial params from config file
      transfer proxy ownership to DAO governor address
      run post-deploy verification (Slither, Mythril)
    script dependencies: forge (foundry), jq, curl for API calls
    onchain enforcement: The deploy script is off-chain tooling. Each contract has an initializer modifier that prevents re-initialization. The script verifies initialization by calling isInitialized() on each contract after deployment and reverts the entire deployment if any contract reports uninitialized state.
solidity contract references:
  GovernanceToken: contracts/GovernanceToken.sol
  DelegationRegistry: contracts/DelegationRegistry.sol
  Governor: contracts/Governor.sol
  TimelockController: contracts/TimelockController.sol
  TreasuryMultisigs: contracts/TreasuryMultisigs.sol
  VetoOverride: contracts/VetoOverride.sol
  ConvictionVault: contracts/ConvictionVault.sol
  ParameterRegistry: contracts/ParameterRegistry.sol
  KeeperRegistry: contracts/KeeperRegistry.sol
  QuadraticLedger: contracts/QuadraticLedger.sol
  RiskRegistry: contracts/RiskRegistry.sol
  DelegationPolicy: contracts/DelegationPolicy.sol
TransferRestrictions normalized:
- type: vestingcontract
  onchainenforcement: Vesting tokens are non-transferable until released by the vesting schedule. Contract checks block.timestamp against schedule on every transferFrom call and reverts if before cliff or exceeding linear release rate. See contracts/VestingContract.sol.
- type: stakinglock
  onchainenforcement: Tokens deposited in ConvictionVault are locked until withdrawal clears cooling-off timer (block.timestamp >= lockTime + withdrawalCoolingBlocks). Vault transferFrom override reverts when locked. See contracts/ConvictionVault.sol.
DelegationTypes normalized:
- name: full
  description: delegate all voting power
  onchainenforcement: setDelegate(to) transfers full voting weight. Governor reads delegateOf[voter] when tallying. See contracts/DelegationRegistry.sol.
- name: partial
  description: delegate percent X
  onchainenforcement: setDelegationWithWeight(to, basisPoints). Governor reads delegatedWeight[voter][proposalId] and applies fraction. See contracts/DelegationRegistry.sol.
- name: issuespecific
  description: delegate on proposal category
  onchainenforcement: setIssueDelegate(to, categoryId, basisPoints). Governor reads issueDelegates[voter][proposalCategoryId] if category matches. See contracts/DelegationRegistry.sol.
ProposalLifecycle stages normalized:
- name: Discussion
  durationdays: 3
  minthresholdtokens: 1000
  note: Field is reserved for future on-chain discussion weighting. Currently off-chain via discourse forum. No on-chain action at this stage.
  onchainenforcement: Off-chain. Reserved field — not enforced on-chain in v1.
- name: Submission
  durationdays: 1
  requireddeposit: 50000
  onchainenforcement: Proposer submits calldata + description hash to Governor. Deposit locked and forfeited if guardian vetoes during timelock.
- name: Voting
  durationhours: 72
  quorumpercent: 4
  approvalthresholdpercent: 50
  votingsystem: quadratic
  onchainenforcement: Each voter commits tokens per option. Governor computes weight per quadratic pseudocode in VotingMechanisms section. Snapshot Merkle root verified on submission. Results commit on-chain after deadline.
- name: Timelock
  durationhours: 48
  executor: TimelockController
  onchainenforcement: Approved calldata queued. Guardian 3-of-5 multisig can cancel during window. Anyone can execute after delay.
- name: Execution
  onchainenforcement: Calldata executed on target contract. If call reverts, proposal marked failed and deposit minus gas penalty returned.
FORMAT VIOLATION CHECK: PASS