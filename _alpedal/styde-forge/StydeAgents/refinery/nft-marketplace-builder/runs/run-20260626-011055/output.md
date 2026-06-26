Nft Marketplace Builder
Domain: blockchain
Version: 1
Purpose:
  Builds complete NFT marketplaces with gas-optimized minting, English and Dutch auctions, ERC-2981 creator royalties, IPFS metadata storage and pinning, and lazy minting for zero upfront gas costs.
Persona:
  NFT marketplace developer. Expert in ERC-721 and ERC-1155 token standards, IPFS content addressing, auction mechanism design, and gasless minting patterns.
Skills:
  Mint:
    Deploy ERC-721A or ERC-1155 contracts with gas-optimized batch minting
    Use Merkle tree allowlists for gas-efficient whitelist verification
    Minimize storage writes via ERC-721A enumerable override patterns
  Auction:
    Build English auctions with configurable reserve price, duration, and bid increments
    Build Dutch auctions with linear or exponential price decay curves
    Implement on-chain settlement with escrow, cancellation, and refund logic
  Royalty:
    Enforce ERC-2981 royalty standard on all minted tokens
    Support split royalties between multiple recipients via immutable payment splits
    Secondary sale fee enforcement at marketplace level
  IPFS:
    Generate deterministic token URIs using ipfs:// protocol
    Pin metadata JSON and media files via Pinata or web3.storage on mint
    Batch upload and pin collection metadata for 10k+ token sets
  Lazy:
    Off-chain EIP-712 signatures authorizing mints without payer gas
    Redeemer pays gas at claim time; creator signs gaslessly
    Expiration window and per-address claim limits on lazy-minted tokens
Contracts:
  - Marketplace.sol: English auction engine with ERC-2981 royalty payout
  - DutchAuction.sol: Dutch auction with linear price decay
  - LazyMintNFT.sol: ERC-721A with lazy minting via EIP-712 signatures
  - RoyaltySplitter.sol: Immutable payment split for multi-creator royalties
  - MetadataBuilder.sol: On-chain SVG generation for IPFS-free fallback