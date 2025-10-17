#!/usr/bin/env python3
"""
OM1 Universal Wallet - Web Demo

FastAPI-based web interface demonstrating Universal Wallet functionality.
"""

import asyncio
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="OM1 Universal Wallet Demo")


# Models
class WalletConfig(BaseModel):
    wallet_address: str
    chains: List[str] = ["ethereum"]
    poll_interval: int = 10
    mock_mode: bool = False


class BalanceResponse(BaseModel):
    chain: str
    asset: str
    amount: float
    usd_value: Optional[float] = None


class SupportedWalletsResponse(BaseModel):
    wallets: List[str]


class SupportedChainsResponse(BaseModel):
    chains: List[str]


# Mock implementation for demo
class SensorConfig:
    pass


class MockWalletUniversal:
    """Simplified wallet for demo."""

    SUPPORTED_CHAINS = ["ethereum", "polygon", "bsc", "arbitrum", "optimism", "solana"]
    SUPPORTED_WALLETS = [
        "MetaMask", "Trust Wallet", "Phantom", "Ledger",
        "Coinbase Wallet", "Rainbow", "Argent", "Safe",
        "WalletConnect (300+ wallets)",
        "Any wallet with blockchain RPC support"
    ]

    def __init__(self, config):
        self.wallet_address = getattr(config, "wallet_address", None)
        self.enabled_chains = getattr(config, "chains", ["ethereum"])
        self.mock_mode = getattr(config, "mock_mode", False)
        self.connected = False

    async def connect(self):
        self.connected = True
        return True

    async def get_all_balances(self):
        if not self.connected:
            return []

        balances = []
        for chain in self.enabled_chains:
            balance = self._generate_mock_balance(chain)
            if balance:
                balances.append(balance)
        return balances

    def _generate_mock_balance(self, chain):
        import random

        amounts = {
            "ethereum": 1.5,
            "polygon": 500.0,
            "bsc": 0.5,
            "solana": 10.0,
            "arbitrum": 0.8,
            "optimism": 0.6,
        }

        assets = {
            "ethereum": "ETH",
            "polygon": "MATIC",
            "bsc": "BNB",
            "solana": "SOL",
            "arbitrum": "ETH",
            "optimism": "ETH",
        }

        base = amounts.get(chain, 1.0)
        amount = base + random.uniform(-0.05, 0.05)

        return {
            "chain": chain,
            "asset": assets.get(chain, "TOKEN"),
            "amount": amount
        }


# Global wallet instance
current_wallet: Optional[MockWalletUniversal] = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the web interface."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OM1 Universal Wallet Demo</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #555;
                font-weight: 500;
            }
            input, select {
                width: 100%;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            button {
                background: #667eea;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                width: 100%;
                margin-top: 10px;
            }
            button:hover {
                background: #5568d3;
            }
            .balances {
                margin-top: 30px;
            }
            .balance-item {
                background: #f8f9fa;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }
            .chain {
                font-weight: 600;
                color: #667eea;
                text-transform: capitalize;
            }
            .amount {
                font-size: 24px;
                color: #333;
                margin: 5px 0;
            }
            .info {
                background: #e7f3ff;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                border-left: 4px solid #2196F3;
            }
            .checkbox-group {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-top: 10px;
            }
            .checkbox-label {
                display: flex;
                align-items: center;
                font-weight: normal;
            }
            .checkbox-label input {
                width: auto;
                margin-right: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 OM1 Universal Wallet</h1>
            <p class="subtitle">Support for 300+ Wallets Across Multiple Blockchains</p>

            <div class="info">
                <strong>Demo Mode:</strong> This demo uses mock data.
                For real wallet integration, install OM1 from
                <a href="https://github.com/OpenMind/OM1" target="_blank">GitHub</a>.
            </div>

            <div class="form-group">
                <label for="address">Wallet Address:</label>
                <input type="text" id="address" placeholder="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb" />
            </div>

            <div class="form-group">
                <label>Select Blockchains:</label>
                <div class="checkbox-group">
                    <label class="checkbox-label">
                        <input type="checkbox" name="chain" value="ethereum" checked> Ethereum
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" name="chain" value="polygon" checked> Polygon
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" name="chain" value="bsc"> BSC
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" name="chain" value="arbitrum"> Arbitrum
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" name="chain" value="optimism"> Optimism
                    </label>
                    <label class="checkbox-label">
                        <input type="checkbox" name="chain" value="solana"> Solana
                    </label>
                </div>
            </div>

            <button onclick="connectWallet()">Connect & Get Balances</button>
            <button onclick="listWallets()" style="background: #28a745; margin-top: 5px;">
                View Supported Wallets (300+)
            </button>

            <div id="balances" class="balances"></div>
        </div>

        <script>
            async function connectWallet() {
                const address = document.getElementById('address').value || '0xMOCK_ADDRESS';
                const checkboxes = document.querySelectorAll('input[name="chain"]:checked');
                const chains = Array.from(checkboxes).map(cb => cb.value);

                if (chains.length === 0) {
                    alert('Please select at least one blockchain');
                    return;
                }

                const balancesDiv = document.getElementById('balances');
                balancesDiv.innerHTML = '<p>Fetching balances...</p>';

                try {
                    const response = await fetch('/api/balances', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            wallet_address: address,
                            chains: chains,
                            mock_mode: true
                        })
                    });

                    const data = await response.json();

                    if (data.length === 0) {
                        balancesDiv.innerHTML = '<p>No balances found</p>';
                        return;
                    }

                    let html = '<h2>Your Balances</h2>';
                    data.forEach(balance => {
                        html += `
                            <div class="balance-item">
                                <div class="chain">${balance.chain}</div>
                                <div class="amount">${balance.amount.toFixed(4)} ${balance.asset}</div>
                            </div>
                        `;
                    });
                    balancesDiv.innerHTML = html;
                } catch (error) {
                    balancesDiv.innerHTML = '<p>Error fetching balances</p>';
                    console.error(error);
                }
            }

            async function listWallets() {
                const balancesDiv = document.getElementById('balances');

                try {
                    const response = await fetch('/api/wallets');
                    const data = await response.json();

                    let html = '<h2>Supported Wallets</h2>';
                    html += '<div style="columns: 2; column-gap: 20px;">';
                    data.wallets.forEach(wallet => {
                        html += `<p>✓ ${wallet}</p>`;
                    });
                    html += '</div>';
                    balancesDiv.innerHTML = html;
                } catch (error) {
                    console.error(error);
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content


@app.post("/api/balances", response_model=List[BalanceResponse])
async def get_balances(config: WalletConfig):
    """Get wallet balances for configured chains."""
    try:
        # Create config object
        sensor_config = SensorConfig()
        sensor_config.wallet_address = config.wallet_address
        sensor_config.chains = config.chains
        sensor_config.poll_interval = config.poll_interval
        sensor_config.mock_mode = config.mock_mode

        # Create wallet and get balances
        wallet = MockWalletUniversal(sensor_config)
        await wallet.connect()
        balances = await wallet.get_all_balances()

        return [BalanceResponse(**b) for b in balances]

    except Exception as e:
        logging.error(f"Error fetching balances: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/wallets", response_model=SupportedWalletsResponse)
async def get_supported_wallets():
    """Get list of all supported wallets."""
    return SupportedWalletsResponse(wallets=MockWalletUniversal.SUPPORTED_WALLETS)


@app.get("/api/chains", response_model=SupportedChainsResponse)
async def get_supported_chains():
    """Get list of all supported blockchains."""
    return SupportedChainsResponse(chains=MockWalletUniversal.SUPPORTED_CHAINS)


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("OM1 Universal Wallet Web Demo")
    print("="*60)
    print("\nStarting server at http://localhost:8000")
    print("Press Ctrl+C to stop\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
