#!/usr/bin/env python3
"""
Example: MetaMask wallet monitoring with OM1 Universal Wallet

This example shows how to monitor a MetaMask wallet across
multiple EVM chains (Ethereum, Polygon, BSC, Arbitrum, Optimism).
"""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)


class SensorConfig:
    pass


# In real usage, import from OM1:
# from inputs.plugins.wallet_universal import WalletUniversal


async def monitor_metamask():
    """Monitor MetaMask wallet across multiple chains."""

    print("\n" + "="*60)
    print("MetaMask Multi-Chain Monitoring Example")
    print("="*60 + "\n")

    # Configure wallet
    config = SensorConfig()
    config.wallet_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"  # Replace with your address
    config.chains = ["ethereum", "polygon", "bsc", "arbitrum", "optimism"]
    config.poll_interval = 30  # Check every 30 seconds
    config.mock_mode = True  # Set to False for real wallet

    print(f"Wallet Address: {config.wallet_address}")
    print(f"Monitoring Chains: {', '.join(config.chains)}")
    print(f"Poll Interval: {config.poll_interval}s")
    print(f"Mock Mode: {config.mock_mode}\n")

    # In real usage:
    # from inputs.plugins.wallet_universal import WalletUniversal
    # wallet = WalletUniversal(config)

    # For demo, we'll simulate
    print("Connecting to wallet...")
    await asyncio.sleep(1)
    print("✓ Connected\n")

    print("Fetching balances across all chains...\n")
    await asyncio.sleep(1)

    # Simulated balances
    balances = [
        {"chain": "ethereum", "asset": "ETH", "amount": 1.5432},
        {"chain": "polygon", "asset": "MATIC", "amount": 523.45},
        {"chain": "arbitrum", "asset": "ETH", "amount": 0.8721},
        {"chain": "optimism", "asset": "ETH", "amount": 0.6543},
    ]

    print("Current Balances:")
    print("-" * 60)
    for balance in balances:
        print(f"  {balance['chain']:12} {balance['amount']:>12.4f} {balance['asset']}")
    print("-" * 60 + "\n")

    print("Monitoring for changes (press Ctrl+C to stop)...")
    print("In real mode, this would detect deposits, withdrawals, and transfers.\n")

    # Simulate monitoring
    try:
        while True:
            await asyncio.sleep(config.poll_interval)
            print(f"[{asyncio.get_event_loop().time():.0f}] Checked - No changes detected")
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")


if __name__ == "__main__":
    print("""
    METAMASK MULTI-CHAIN MONITORING
    ================================

    This example demonstrates monitoring a MetaMask wallet across
    multiple EVM-compatible chains using OM1's Universal Wallet.

    MetaMask supports:
    - Ethereum mainnet
    - Polygon (MATIC)
    - Binance Smart Chain (BSC)
    - Arbitrum (Layer 2)
    - Optimism (Layer 2)
    - And many more EVM chains

    The Universal Wallet automatically works with MetaMask and
    any other wallet that supports blockchain RPCs.
    """)

    asyncio.run(monitor_metamask())
