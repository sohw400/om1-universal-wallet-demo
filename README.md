# OM1 Universal Wallet Demo

This repository demonstrates the Universal Wallet functionality of OM1, showcasing support for 300+ cryptocurrency wallets through a unified interface.

## Features

- **300+ Wallet Support**: Works with MetaMask, Phantom, Trust Wallet, Ledger, and any wallet supporting blockchain RPCs
- **Multi-Chain**: Supports Ethereum, Polygon, BSC, Arbitrum, Optimism, and Solana
- **Web Interface**: Interactive demo with wallet connection and balance monitoring
- **Mock Mode**: Test without real wallets or blockchain connections

## Quick Start

### Interactive Demo (Recommended) ⭐

**Real wallet connections - MetaMask, WalletConnect, 300+ wallets**

1. Clone and navigate:
```bash
git clone https://github.com/sohw400/om1-universal-wallet-demo
cd om1-universal-wallet-demo
```

2. Start the server:
```bash
npm start
```

3. Open http://localhost:3000 in your browser with MetaMask installed

4. Click "Connect Wallet" to interact with real wallets!

**What you can do:**
- Connect any Web3 wallet (MetaMask, WalletConnect, etc.)
- Sign messages with cryptographic proof
- Send real transactions
- Switch between networks
- Works on Mainnet, Sepolia, Polygon, etc.

### Alternative Options

**Option 1: HTML Demo (No Server)**

Just open `interactive-demo.html` or `demo.html` in your browser

**Option 2: Python Web Demo**

```bash
pip install -r requirements.txt
python web_demo.py
```

**Option 3: Command Line Demo**

```bash
# With a real wallet address
python cli_demo.py --address 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --chains ethereum polygon

# With mock mode (no real wallet needed)
python cli_demo.py --mock
```

## Examples

### Basic Usage

```python
from wallet_universal import WalletUniversal
from inputs.base import SensorConfig

# Configure wallet
config = SensorConfig()
config.wallet_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
config.chains = ["ethereum", "polygon"]
config.poll_interval = 10

# Create wallet instance
wallet = WalletUniversal(config)

# Connect and get balances
await wallet.connect()
balances = await wallet.get_all_balances()

for balance in balances:
    print(f"{balance.chain}: {balance.amount} {balance.asset}")
```

### Mock Mode for Testing

```python
config = SensorConfig()
config.mock_mode = True
config.chains = ["ethereum", "polygon", "solana"]

wallet = WalletUniversal(config)
await wallet.connect()
balances = await wallet.get_all_balances()
```

### Monitor Balance Changes

```python
while True:
    changes = await wallet._poll()
    if changes:
        await wallet.raw_to_text(changes)
        message = wallet.formatted_latest_buffer()
        if message:
            print(message)
```

## Supported Wallets

### Ethereum & EVM Chains
- MetaMask
- Trust Wallet
- Coinbase Wallet
- Rainbow Wallet
- Argent
- Safe (Gnosis Safe)
- Ledger (hardware)
- Trezor (hardware)
- 200+ more via WalletConnect

### Solana
- Phantom
- Solflare
- Backpack
- Ledger (hardware)
- 50+ more

## Supported Blockchains

- Ethereum (ETH)
- Polygon (MATIC)
- Binance Smart Chain (BNB)
- Arbitrum (ETH L2)
- Optimism (ETH L2)
- Solana (SOL)

## Architecture

```
WalletUniversal
    ↓
ChainAdapters
    ↓
RPC Endpoints
    ↓
Any Wallet (300+)
```

The Universal Wallet uses chain adapters instead of wallet-specific connectors. This means:
- New wallets work automatically
- No code changes needed for new wallets
- Easy to add new blockchains
- Maintainable and extensible

## Demo Files

- `web_demo.py` - FastAPI web interface with wallet connection
- `cli_demo.py` - Command-line demonstration
- `examples/metamask_example.py` - MetaMask specific example
- `examples/phantom_example.py` - Phantom wallet example
- `examples/multi_wallet.py` - Monitor multiple wallets

## Configuration

Create a `config.json` file:

```json
{
  "wallet_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "chains": ["ethereum", "polygon", "arbitrum"],
  "poll_interval": 15,
  "mock_mode": false
}
```

Then run:

```bash
python cli_demo.py --config config.json
```

## Testing

```bash
# Run mock mode tests
python cli_demo.py --mock --test

# Test all supported chains
python cli_demo.py --mock --chains ethereum polygon bsc arbitrum optimism solana
```

## Main Repository

This demo is part of the OM1 project:
https://github.com/OpenMind/OM1

See the full Universal Wallet documentation:
https://github.com/OpenMind/OM1/blob/main/docs/UNIVERSAL_WALLET.md

## Related PR

Universal Wallet Implementation PR: https://github.com/OpenMind/OM1/pull/XXX

## License

MIT License - Same as OM1 project
