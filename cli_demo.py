#!/usr/bin/env python3
"""
OM1 Universal Wallet - Command Line Demo

This demonstrates the Universal Wallet functionality with support for
300+ wallets across multiple blockchains.
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class SensorConfig:
    """Simple config object for demo purposes."""
    pass


class WalletBalance:
    """Mock WalletBalance for demo."""
    def __init__(self, chain, asset, amount, usd_value=None):
        self.chain = chain
        self.asset = asset
        self.amount = amount
        self.usd_value = usd_value


class MockWalletUniversal:
    """
    Simplified version of WalletUniversal for demo purposes.

    In real usage, import from OM1:
    from inputs.plugins.wallet_universal import WalletUniversal
    """

    SUPPORTED_CHAINS = ["ethereum", "polygon", "bsc", "arbitrum", "optimism", "solana"]

    def __init__(self, config):
        self.wallet_address = getattr(config, "wallet_address", None)
        self.enabled_chains = getattr(config, "chains", ["ethereum"])
        self.poll_interval = getattr(config, "poll_interval", 10)
        self.mock_mode = getattr(config, "mock_mode", False)
        self.connected = False

        if self.mock_mode:
            self.wallet_address = "0xMOCK_ADDRESS"
            logging.info("Running in MOCK MODE - no real blockchain connections")

        logging.info(f"Initialized Universal Wallet for chains: {', '.join(self.enabled_chains)}")

    async def connect(self):
        """Connect to wallet."""
        if not self.wallet_address:
            logging.error("No wallet address provided")
            return False

        logging.info(f"Connecting to wallet: {self.wallet_address}")
        self.connected = True
        return True

    async def get_balance(self, chain, asset="native"):
        """Get balance for a specific chain."""
        if not self.connected:
            return None

        if self.mock_mode:
            return self._generate_mock_balance(chain)

        # In real implementation, this would query blockchain
        logging.warning("Real blockchain queries require OM1 installation")
        return None

    async def get_all_balances(self):
        """Get balances for all configured chains."""
        balances = []

        for chain in self.enabled_chains:
            balance = await self.get_balance(chain)
            if balance and balance.amount > 0:
                balances.append(balance)

        return balances

    def _generate_mock_balance(self, chain):
        """Generate realistic mock balance data."""
        import random

        base_amounts = {
            "ethereum": 1.5,
            "polygon": 500.0,
            "bsc": 0.5,
            "solana": 10.0,
            "arbitrum": 0.8,
            "optimism": 0.6,
        }

        asset_symbols = {
            "ethereum": "ETH",
            "polygon": "MATIC",
            "bsc": "BNB",
            "solana": "SOL",
            "arbitrum": "ETH",
            "optimism": "ETH",
        }

        base = base_amounts.get(chain, 1.0)
        variation = random.uniform(-0.05, 0.05)
        amount = base + variation

        return WalletBalance(
            chain=chain,
            asset=asset_symbols.get(chain, "TOKEN"),
            amount=amount
        )

    def get_supported_chains(self):
        """Get list of supported blockchains."""
        return self.SUPPORTED_CHAINS

    def get_supported_wallets(self):
        """Get list of supported wallet types."""
        return [
            "MetaMask",
            "Trust Wallet",
            "Phantom",
            "Ledger",
            "Coinbase Wallet",
            "Rainbow",
            "Argent",
            "Safe",
            "WalletConnect (300+ wallets)",
            "Any wallet with blockchain RPC support",
        ]


async def run_demo(args):
    """Run the wallet demo."""

    # Create configuration
    config = SensorConfig()

    if args.config:
        # Load from config file
        with open(args.config) as f:
            config_data = json.load(f)
            config.wallet_address = config_data.get("wallet_address")
            config.chains = config_data.get("chains", ["ethereum"])
            config.poll_interval = config_data.get("poll_interval", 10)
            config.mock_mode = config_data.get("mock_mode", False)
    else:
        # Use command line arguments
        config.wallet_address = args.address
        config.chains = args.chains
        config.poll_interval = args.interval
        config.mock_mode = args.mock

    # Create wallet instance
    print("\n" + "="*60)
    print("OM1 UNIVERSAL WALLET DEMO")
    print("="*60 + "\n")

    wallet = MockWalletUniversal(config)

    # Show supported wallets
    if args.list_wallets:
        print("Supported Wallets:")
        for wallet_name in wallet.get_supported_wallets():
            print(f"  • {wallet_name}")
        return

    # Show supported chains
    if args.list_chains:
        print("Supported Blockchains:")
        for chain in wallet.get_supported_chains():
            print(f"  • {chain}")
        return

    # Connect to wallet
    connected = await wallet.connect()
    if not connected:
        print("Failed to connect to wallet")
        return

    print(f"✓ Connected to wallet: {wallet.wallet_address}\n")

    # Get balances
    print(f"Fetching balances for {len(config.chains)} chain(s)...\n")
    balances = await wallet.get_all_balances()

    if not balances:
        print("No balances found or all balances are zero")
        return

    # Display balances
    print("Current Balances:")
    print("-" * 60)

    for balance in balances:
        print(f"  {balance.chain:12} {balance.amount:>12.4f} {balance.asset}")

    print("-" * 60)
    print(f"Total: {len(balances)} non-zero balance(s)\n")

    # Monitor mode
    if args.monitor:
        print("Monitoring for balance changes (Ctrl+C to stop)...")
        print("Checking every {} seconds\n".format(config.poll_interval))

        try:
            while True:
                await asyncio.sleep(config.poll_interval)
                new_balances = await wallet.get_all_balances()

                for new_bal in new_balances:
                    for old_bal in balances:
                        if new_bal.chain == old_bal.chain:
                            if new_bal.amount != old_bal.amount:
                                change = new_bal.amount - old_bal.amount
                                print(f"[{new_bal.chain}] Balance changed: "
                                      f"{old_bal.amount:.4f} → {new_bal.amount:.4f} "
                                      f"({change:+.4f} {new_bal.asset})")

                balances = new_balances

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped")


def main():
    parser = argparse.ArgumentParser(
        description="OM1 Universal Wallet Demo - Support for 300+ wallets"
    )

    parser.add_argument(
        "--address",
        help="Wallet address to monitor"
    )

    parser.add_argument(
        "--chains",
        nargs="+",
        default=["ethereum"],
        help="Blockchains to monitor (ethereum, polygon, bsc, etc.)"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Poll interval in seconds (default: 10)"
    )

    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock mode (no real blockchain connections)"
    )

    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor for balance changes"
    )

    parser.add_argument(
        "--config",
        help="Load configuration from JSON file"
    )

    parser.add_argument(
        "--list-wallets",
        action="store_true",
        help="List all supported wallets"
    )

    parser.add_argument(
        "--list-chains",
        action="store_true",
        help="List all supported blockchains"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.mock and not args.address and not args.config and not args.list_wallets and not args.list_chains:
        parser.error("Either --address, --mock, --config, --list-wallets, or --list-chains is required")

    # Run demo
    try:
        asyncio.run(run_demo(args))
    except KeyboardInterrupt:
        print("\n\nDemo terminated")


if __name__ == "__main__":
    main()
