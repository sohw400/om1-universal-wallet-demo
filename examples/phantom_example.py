#!/usr/bin/env python3
"""
Example: Phantom wallet monitoring with OM1 Universal Wallet

This example shows how to monitor a Phantom wallet on Solana.
"""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)


class SensorConfig:
    pass


async def monitor_phantom():
    """Monitor Phantom wallet on Solana."""

    print("\n" + "="*60)
    print("Phantom Wallet Monitoring Example")
    print("="*60 + "\n")

    # Configure wallet
    config = SensorConfig()
    config.wallet_address = "DYw8jCTfwHNRJhhmFcbXvVDTqWMEVFBX6ZKUmG5CNSKK"  # Solana address
    config.chains = ["solana"]
    config.poll_interval = 15  # Check every 15 seconds
    config.mock_mode = True  # Set to False for real wallet

    print(f"Wallet Address: {config.wallet_address}")
    print(f"Monitoring Chain: Solana")
    print(f"Poll Interval: {config.poll_interval}s")
    print(f"Mock Mode: {config.mock_mode}\n")

    # In real usage:
    # from inputs.plugins.wallet_universal import WalletUniversal
    # wallet = WalletUniversal(config)

    # For demo, we'll simulate
    print("Connecting to Phantom wallet...")
    await asyncio.sleep(1)
    print("✓ Connected\n")

    print("Fetching SOL balance...\n")
    await asyncio.sleep(1)

    # Simulated balance
    sol_balance = 12.5483

    print("Current Balance:")
    print("-" * 60)
    print(f"  Solana        {sol_balance:>12.4f} SOL")
    print("-" * 60 + "\n")

    print("Monitoring for changes (press Ctrl+C to stop)...")
    print("Phantom wallet activity (NFT transfers, SOL transactions) will be detected.\n")

    # Simulate monitoring with occasional balance changes
    try:
        iteration = 0
        while True:
            await asyncio.sleep(config.poll_interval)
            iteration += 1

            # Simulate a transaction every 5 iterations
            if iteration % 5 == 0:
                change = 0.5
                sol_balance += change
                print(f"[CHANGE DETECTED] Received {change:.4f} SOL")
                print(f"[NEW BALANCE] {sol_balance:.4f} SOL\n")
            else:
                print(f"[{iteration}] Checked - No changes detected")

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")


if __name__ == "__main__":
    print("""
    PHANTOM WALLET MONITORING
    =========================

    This example demonstrates monitoring a Phantom wallet on Solana
    using OM1's Universal Wallet.

    Phantom is the leading Solana wallet with support for:
    - SOL (native Solana token)
    - SPL tokens (Solana's token standard)
    - NFT collections
    - Solana DeFi protocols

    The Universal Wallet works seamlessly with Phantom and
    any other Solana wallet that supports RPC connections.

    Note: Solana implementation is in progress. Currently shows
    mock data for demonstration purposes.
    """)

    asyncio.run(monitor_phantom())
