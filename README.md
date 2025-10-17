# OM1 Universal Wallet Demo

Demo application for OM1's Universal Wallet implementation - supports 300+ cryptocurrency wallets.

## Features

- **300+ Wallet Support**: MetaMask, Coinbase Wallet, Trust Wallet, Rainbow, Ledger, Phantom, and more via WalletConnect
- **Multi-Chain**: Ethereum, Polygon, Sepolia testnet
- **Full Functionality**: Connect, sign messages, send transactions, switch networks

## Quick Start

1. **Install dependencies**

```bash
cd wallet-demo
npm install
```

2. **Run the demo**

```bash
npm run dev
```

3. **Open browser**

Navigate to `http://localhost:3000`

## Demo Features

- **Connect Wallet**: Click to see 300+ wallet options
- **Sign Message**: Test cryptographic message signing
- **Send Transaction**: Send test transaction (0.001 ETH to self)
- **Network Switch**: Change between Ethereum, Polygon, Sepolia
- **Disconnect**: Safely disconnect wallet

## Technology Stack

- React + Vite
- WalletConnect Web3Modal
- Wagmi hooks
- Viem

## Main Repository

This demo is part of the OM1 Universal Wallet implementation:

- **PR**: https://github.com/OpenMind/OM1/pull/463
- **Docs**: https://github.com/OpenMind/OM1/blob/feat/universal-wallet-support/docs/UNIVERSAL_WALLET.md

## Implementation Details

The OM1 Universal Wallet uses a modular chain adapter architecture:

- `WalletBase`: Abstract base class for wallet implementations
- `ChainAdapter`: Blockchain-specific adapters (Ethereum, Solana)
- `WalletUniversal`: Main implementation supporting 300+ wallets

See the main PR for full implementation and 87 unit tests.

## License

MIT License
