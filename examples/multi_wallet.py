#!/usr/bin/env python3
"""
Example: Monitor multiple wallets simultaneously

This example shows how to track multiple wallet addresses
across different chains using OM1 Universal Wallet.
"""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)


class SensorConfig:
    pass


async def monitor_single_wallet(name, address, chains):
    """Monitor a single wallet."""

    config = SensorConfig()
    config.wallet_address = address
    config.chains = chains
    config.poll_interval = 20
    config.mock_mode = True

    print(f"\n[{name}] Monitoring {address[:10]}... on {', '.join(chains)}")

    # In real usage:
    # from inputs.plugins.wallet_universal import WalletUniversal
    # wallet = WalletUniversal(config)
    # await wallet.connect()

    # Simulate monitoring
    iteration = 0
    while True:
        await asyncio.sleep(20)
        iteration += 1

        # Simulate occasional updates
        if iteration % 3 == 0:
            print(f"[{name}] Balance update detected")
        else:
            print(f"[{name}] No changes")


async def monitor_multiple_wallets():
    """Monitor multiple wallets concurrently."""

    print("\n" + "="*60)
    print("Multi-Wallet Monitoring Example")
    print("="*60)

    # Define wallets to monitor
    wallets = [
        {
            "name": "Main EVM Wallet",
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "chains": ["ethereum", "polygon", "arbitrum"]
        },
        {
            "name": "DeFi Wallet",
            "address": "0x8888888888888888888888888888888888888888",
            "chains": ["ethereum", "optimism"]
        },
        {
            "name": "Solana Wallet",
            "address": "DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK",
            "chains": ["solana"]
        },
        {
            "name": "BSC Trading Wallet",
            "address": "0x9999999999999999999999999999999999999999",
            "chains": ["bsc"]
        }
    ]

    print(f"\nMonitoring {len(wallets)} wallets:\n")
    for wallet in wallets:
        print(f"  • {wallet['name']}")
        print(f"    {wallet['address'][:20]}...")
        print(f"    Chains: {', '.join(wallet['chains'])}\n")

    print("Starting concurrent monitoring (press Ctrl+C to stop)...\n")

    # Create monitoring tasks for each wallet
    tasks = [
        monitor_single_wallet(w["name"], w["address"], w["chains"])
        for w in wallets
    ]

    try:
        # Run all monitoring tasks concurrently
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\n\nStopping all monitors...")


if __name__ == "__main__":
    print("""
    MULTI-WALLET MONITORING
    =======================

    This example demonstrates monitoring multiple wallet addresses
    simultaneously across different blockchains.

    Use cases:
    - Portfolio tracking across multiple wallets
    - Family wallet monitoring
    - Business treasury management
    - Cross-chain asset tracking

    The Universal Wallet efficiently monitors multiple addresses
    by using shared chain adapters and concurrent async operations.

    Each wallet can monitor different chains independently.
    """)

    asyncio.run(monitor_multiple_wallets())
