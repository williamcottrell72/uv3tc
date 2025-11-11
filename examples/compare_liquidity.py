#!/usr/bin/env python3
"""
Example: Compare high-liquidity vs low-liquidity pools.

This demonstrates the dramatic difference in trading costs between
pools with deep liquidity (like USDC/WBTC) and those with shallow
liquidity (like FLOKI/WETH).
"""

import os
import sys
from web3 import Web3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from uniswap import analyze_trade_costs, plot_price_impact

# Check for Infura API key
infura_api_key = os.environ.get("INFURA_API_KEY")
if not infura_api_key:
    print("Error: INFURA_API_KEY environment variable not set")
    sys.exit(1)

# Set up Web3
rpc_url = f"https://mainnet.infura.io/v3/{infura_api_key}"
w3 = Web3(Web3.HTTPProvider(rpc_url))

if not w3.is_connected():
    print("Error: Failed to connect to Ethereum node")
    sys.exit(1)

print("=" * 70)
print("Comparing High-Liquidity vs Low-Liquidity Pools")
print("=" * 70)

# ========================================
# High-Liquidity Pool: USDC/WBTC
# ========================================
print("\n\n1️⃣  HIGH-LIQUIDITY POOL: USDC → WBTC")
print("-" * 70)
print("This is a major pool with deep liquidity.\n")

df_high_liquidity = analyze_trade_costs(
    w3=w3,
    token_in_symbol="USDC",
    token_out_symbol="WBTC",
    amounts_in=[1000, 10000, 100000, 1000000],  # Large trades work fine
    verbose=True,
)

print("\n💡 Notice: All trades succeed with low price impact (<1%)")

# ========================================
# Low-Liquidity Pool: FLOKI/WETH
# ========================================
print("\n\n2️⃣  LOW-LIQUIDITY POOL: FLOKI → WETH")
print("-" * 70)
print("This is a low-volume pool with shallow liquidity.\n")

df_low_liquidity = analyze_trade_costs(
    w3=w3,
    token_in_symbol="FLOKI",
    token_out_symbol="WETH",
    amounts_in=[0.1, 1, 10, 100],  # Much smaller amounts!
    verbose=True,
)

print("\n💡 Notice: Even small trades may fail due to insufficient liquidity")

# ========================================
# Compare Results
# ========================================
print("\n\n📊 COMPARISON")
print("=" * 70)

if len(df_high_liquidity) > 0:
    avg_impact_high = df_high_liquidity["price_impact_bps"].mean()
    print(f"High-Liquidity (USDC/WBTC):")
    print(
        f"  Average Price Impact: {avg_impact_high:.2f} bps ({avg_impact_high/100:.2f}%)"
    )
    print(f"  Successful trades: {len(df_high_liquidity)}/4")

if len(df_low_liquidity) > 0:
    avg_impact_low = df_low_liquidity["price_impact_bps"].mean()
    print(f"\nLow-Liquidity (FLOKI/WETH):")
    print(
        f"  Average Price Impact: {avg_impact_low:.2f} bps ({avg_impact_low/100:.2f}%)"
    )
    print(f"  Successful trades: {len(df_low_liquidity)}/4")

    if len(df_high_liquidity) > 0:
        ratio = avg_impact_low / avg_impact_high
        print(f"\n📈 Price impact is {ratio:.1f}x higher in the low-liquidity pool!")

print("\n" + "=" * 70)
print("Key Takeaway:")
print("- High-liquidity pools: Can handle large trades with minimal slippage")
print("- Low-liquidity pools: Even small trades cause significant price impact")
print("=" * 70)
