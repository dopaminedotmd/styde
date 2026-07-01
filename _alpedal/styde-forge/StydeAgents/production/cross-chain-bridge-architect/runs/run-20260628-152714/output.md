Message passing design:
LAYER 0: CONSENSUS ABSTRACTION
Each chain exposes a block header format with validator set.
Light client on destination chain verifies source chain consensus.
No trusted third party. Only cryptographic verification.
MESSAGE FORMAT:
source_chain_id: u32
destination_chain_id: u32
nonce: u64
sender: bytes32
receiver: bytes32
payload: bytes
signature_threshold: u8
MESSAGE FLOW:
1. User calls send() on source chain contract
2. Event emitted with message hash
3. Relayer picks up event from source chain log
4. Relayer submits message + Merkle proof to destination
5. Light client verifies proof against stored source chain state
6. Destination contract executes payload or mints wrapped tokens
TOKEN WRAPPING:
Lock on source -> Mint on destination
Burn on destination -> Unlock on source
Canonical token contract on each chain tracks total supply.
Native assets locked in bridge contract. Wrapped assets are 1:1 representation.
Rebalancing: relayer nodes maintain liquidity pools for fast swaps.
Slow path: always revert to lock/mint for security.
VALIDATOR NETWORK:
PoS validator set with bonded stake.
2/3 majority required for message approval.
Slashing conditions:
- Double-signing: 100% slash
- False message relay: 100% slash
- Downtime: gradual unbonding
Validator rotation every epoch (100 blocks).
Dynamic set: new validators can join by bonding minimum stake.
SECURITY VECTORS:
Replay attack: nonce prevents. Each message consumed once.
Phantom message: Merkle proof ties message to real source chain event.
Validator collusion: threshold 2/3+1, economic security from bonded stake.
Bridge drain: rate limiter per asset per epoch (max 1% of TVL).
Oracle manipulation: use TWAP not spot price for any valuation.
Cross-chain reorg: finality delay before message acceptance.
- Ethereum L1: 12 block confirmations
- Cosmos: 1 block (instant finality)
- Solana: 32 block confirmations
Upgrade: multi-sig timelock (7 day delay, 3/5 signers).
RELAY NETWORK:
P2P gossip layer for message discovery.
Relayer nodes subscribe to source chain events.
Message mempool: pending messages awaiting verification.
Competitive relayer fee market. Lowest fee wins.
Redundancy: N relayers pick up same message. First valid submission wins.
Latency target: block time + 2 seconds for finality check.
Fallback: anyone can relay. Permissionless.
LIGHT CLIENT VERIFICATION:
Store source chain block headers on destination.
Verify validator set signatures on each header.
Efficient: store only header, not full block.
Merkle proof verifies message inclusion in source chain block.
Gas optimization: batch header updates, verify once per N messages.
ZK option: generate zkSNARK of entire subchain for 10x gas reduction.
IMPLEMENTATION PRIORITY:
1. Single message passing between two EVM chains
2. Token wrapping contract (lock/mint, burn/unlock)
3. Light client with header sync
4. Relayer daemon in Rust
5. Validator set with staking
6. Rate limiters and emergency pause
7. ZK proof integration
SECURITY AUDIT CHECKLIST:
- Reentrancy on unlock functions
- Integer overflow in total supply tracking
- Signature replay across chains
- Timestamp manipulation in time-locks
- Front-running of relay submissions
- Denial of service via invalid message spam
- Cross-chain reorg handling
- Upgrade proxy patterns (UUPS vs transparent)