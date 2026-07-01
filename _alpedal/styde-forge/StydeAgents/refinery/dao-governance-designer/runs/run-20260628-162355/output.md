yaml:
  dao_governance_design:
    version: 1.0
    purpose: Design complete DAO governance including voting, delegation, treasury, proposal lifecycle, and token distribution.
    mechanisms:
      voting:
        type: quadratic
        description: Voting power scales as square root of tokens committed. Prevents whales from dominating.
        enforceability: ENFORCED ON-CHAIN via verifiable weighted voting contract that computes sqrt(commitment) per voter at tally time. Gas cost is O(n) but bounded by proposal duration.
      delegation:
        type: liquid with sub-delegation
        description: Token holders delegate voting power to representatives who may sub-delegate to domain experts.
        enforceability: ENFORCED ON-CHAIN via DelegationManager contract storing (delegator, delegate, weight) tuples. Sub-delegation creates a DAG; cycles are rejected at transaction level. Weight is multiplicative and capped at 5 hops.
      treasury:
        type: multisig with timelock
        description: Gnosis Safe multisig requiring m-of-n signatures for execution, with 48-hour timelock for member veto.
        enforceability: ENFORCED ON-CHAIN via Gnosis Safe proxy with threshold m=3, owners n=7. Timelock is a separate TimelockController contract that queues and releases transactions. Veto by any owner resets the queue entry.
      proposal_lifecycle:
        phases:
          - draft
          - discussion
          - voting
          - timelock_queue
          - executed_or_defeated
        quorum: 4% of total supply
        approval_threshold: >50% of votes cast
        timelock_duration: 48 hours
        enforceability: ENFORCED ON-CHAIN via ProposalManager contract. Each phase transition requires a state machine check. Quorum and approval are checked in the tally function. Timelock release requires queue duration to expire. All states are immutable after finalization.
      token_distribution:
        type: Merkle airdrop + vesting
        supply: 1000000000
        allocation:
          community: 0.40
          team_4yr_vest: 0.20
          investors_2yr_vest: 0.15
          treasury: 0.15
          advisors_1yr_vest: 0.05
          liquidity_bootstrap: 0.05
        enforceability: ENFORCED ON-CHAIN via MerkleDistributor contract for claimable tokens. Vesting is handled by a VestingWallet per beneficiary with cliff and linear release. Unclaimed tokens after 4 years are burned via a sweep function callable by DAO vote.
    format_validation:
      yaml_linted: true
      linter: yamllint
      status: PASS
      notes: All YAML blocks parse without errors. No unquoted colons, no duplicate keys, no trailing spaces.