CROSS CHAIN BRIDGE ARCHITECT — DESIGN OUTPUT
BRIDGE TYPE: Optimistic + External Validator hybrid
SECURITY MODEL: 2-of-3 threshold multisig + fraud proof window
MESSAGE PASSING PROTOCOL
- Source chain: emit event via canonical bridge contract
- Message format: {chainId, sender, targetChain, targetAddr, payload, nonce, timestamp}
- Payload hash committed on-chain; full calldata relayed off-chain via gossip
- Receipt: Merkle proof of inclusion on source block header
TOKEN WRAPPING
- Lock/mint pattern for canonical representation
- Source: user deposits token into Bridge contract -> locked in vault
- Destination: minted as wrappedToken (ERC20) with pausable mint role
- Rate limit: 1% of total supply per epoch across all chains
- Fee: 0.05% split between relayers and protocol treasury
LIGHT CLIENT VERIFICATION
- Solidity implementation of BLS signature aggregation
- Stores source chain block headers: 256 most recent
- Validates Merkle inclusion proof against stored header
- Difficulty check: require N confirmations (varies by chain finality)
- Gas-optimized: batch header updates (max 8 per tx)
RELAY NETWORK
- N validators stake bond (min 100 ETH equivalent)
- Round-robin leader election every 100 blocks
- Leader submits batch of messages + headers
- Validators cast BLS sig share within 50 blocks
- Challenges: any validator can submit fraud proof within 7 days
- Slashing: 10% of stake for invalid message submission; 20% for double-signing
SECURITY VECTORS COVERED
- Replay attack: nonce monotonic per (sourceChain, sender)
- Oracle manipulation: external price feed with TWAP fallback
- Reorg: wait for probabilistic finality (32 blocks Ethereum, 1 epoch Cosmos)
- Griefing: relayer bond slashed for submitting junk headers
- Parition attack: header sync requires 2 independent relayers
CRITICAL PATCHES
- Bridge contract: reentrancy guard on unlock()
- Wrapped token: no rebasing, no fee-on-transfer compat layer
- Validator set: delay of 2 days between vote to add/remove and effect
DEPLOYMENT ORDER
1. Deploy LightClient contract on destination chain
2. Deploy Vault contract on source chain
3. Deploy Bridge contract on both chains
4. Deploy WrappedToken factory
5. Register validator set (genesis: 5 keys)
6. Fund relayer bonds
7. Enable message passing in both directions
99.8% uptime target. Emergency pause by 3-of-5 multi-sig timelock (4h delay).