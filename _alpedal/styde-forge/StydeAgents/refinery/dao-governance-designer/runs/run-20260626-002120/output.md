DAO GOVERNANCE FRAMEWORK v1
VOTING: QUADRATIC + CONVICTION HYBRID
Quadratic voting floor: cost = votes^2 * base_fee. Prevents whale dominance. Minimum quorum 4% of total supply.
Conviction voting for capital allocation: voting power grows linearly over time up to 365-day max. Higher conviction = more influence on treasury grants. Exit penalty: withdrawing conviction resets timer with 50% decay on first withdrawal.
Gas-optimized: batch verify Merkle proofs for off-chain tally on L2. Use zk-SNARK for private voting option.
DELEGATION: FOUR-TIER HIERARCHY
Level 1: Token holder delegates to any address. Full voting power transferred.
Level 2: Delegates can sub-delegate to max 5 specialists per governance area (treasury, protocol, grants, operations, emergency).
Level 3: Sub-delegates can re-delegate specific proposal categories to domain experts. Max depth 3.
Level 4: Zero-knowledge delegation — delegate without revealing voting preference. Commit-reveal scheme with 48h reveal window.
Auto-deactivation: delegate inactive for 90 days loses delegation. Delegated tokens return to holders. Re-delegation cooldown 7 days.
TREASURY: 3/5 MULTISIG WITH MODULAR GUARDS
Primary treasury: 3/5 Gnosis Safe on Base L2. Signers rotated quarterly by governance vote.
Timelock controller: all treasury transactions >= 50 ETH require 7-day timelock + public veto period. Emergency multisig (2/3) bypasses timelock for hacks only.
Streaming: token streaming for contributor payments via Sablier. Max 6-month streams approved by governance.
Yield: treasury assets deposited in diversified strategy vaults (50% stables LP, 30% blue-chip staking, 20% protocol-owned liquidity). Monthly rebalance triggers governance vote if outside tolerance bands.
PROPOSAL LIFECYCLE: 6-STAGE PIPELINE
Stage 1 — Temperature check: forum poll. 3 days. 50% majority.
Stage 2 — Formal draft: on-chain proposal submitted. 100k token deposit bond. Bond slashed if proposal fails quorum.
Stage 3 — Discussion period: 5 days. Delegate chat mandatory.
Stage 4 — Voting: 7 days. Quadratic weights. Quorum: 4% supply.
Stage 5 — Timelock: 48h on execution. Cancelable by guardian multisig during timelock.
Stage 6 — Execution: automated via Gelato keeper. Gas sponsored by treasury.
Emergency proposals: 24h voting. Requires 2/3 supermajority. Max one per 30 days.
TOKEN DISTRIBUTION: MERITOCRATIC LAUNCH
Total supply: 100,000,000 GOV tokens
30% — Community treasury. Vested linearly over 4 years. Unlocks via conviction voting.
20% — Initial airdrop. Proof-of-personhood gated (WorldID + Gitcoin Passport). Sybil resistance score >= 0.7. Claim 12-month linear vesting.
20% — Protocol contributors. 3-year cliff + 2-year linear vesting. Non-transferable until TGE+12m.
15% — Liquidity bootstrapping. Balancer LBP over 72h. Starting weight 90/10 GOV/USDC, ending 50/50.
10% — Strategic partners. 1-year cliff. 2-year vesting. Governance-nominated.
5% — Retroactive public goods funding. Distributed quarterly via conviction voting.
Airdrop formula: base = 100 tokens. Multipliers: early supporter (2x), active voter (1.5x), GitHub contributor (1.3x), Discord rank (1.2x). Cap at 5x.
VeToken: lock GOV for MAX 4 years. Get veGOV. veGOV voting power = lock_amount * (lock_duration / 4yr). veGOV decays linearly. 5% early exit fee burned.