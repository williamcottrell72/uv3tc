#!/usr/bin/env python3
"""
Example: Compare high, medium, and low liquidity pools.

This demonstrates how trading costs vary dramatically across
the three liquidity tiers available in the toolkit.
"""

import os
import sys
from web3 import Web3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from uniswap import (
    analyze_trade_costs,
    get_recommended_amounts,
    get_token_liquidity_tier,
    print_liquidity_summary
)

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
print("Comparing High, Medium, and Low Liquidity Pools")
print("=" * 70)

# Show all available tokens by tier
print("\n")
print_liquidity_summary()

# Test cases for each liquidity tier
test_cases = [
    ("USDC", "WBTC", "high"),      # High liquidity
    ("RPL", "WETH", "medium"),     # Medium liquidity
    ("FLOKI", "WETH", "low")       # Low liquidity
]

results_summary = []

for token_in, token_out, expected_tier in test_cases:
    # Verify the tier
    tier = get_token_liquidity_tier(token_in)

    print("\n" + "=" * 70)
    print(f"{expected_tier.upper()}-LIQUIDITY POOL: {token_in} → {token_out}")
    print("=" * 70)
    print(f"Token tier: {tier}")

    # Get recommended amounts for this token
    amounts = get_recommended_amounts(token_in)
    print(f"Recommended trade sizes: {amounts}")
    print("")

    try:
        df = analyze_trade_costs(
            w3=w3,
            token_in_symbol=token_in,
            token_out_symbol=token_out,
            amounts_in=amounts,
            verbose=True
        )

        if len(df) > 0:
            avg_impact = df['price_impact_bps'].mean()
            max_impact = df['price_impact_bps'].max()
            success_rate = len(df) / len(amounts)

            results_summary.append({
                "pair": f"{token_in}/{token_out}",
                "tier": expected_tier,
                "avg_impact_bps": avg_impact,
                "max_impact_bps": max_impact,
                "success_rate": success_rate,
                "num_successful": len(df),
                "num_total": len(amounts)
            })

            print(f"\nSummary:")
            print(f"  Average Price Impact: {avg_impact:.2f} bps ({avg_impact/100:.2f}%)")
            print(f"  Maximum Price Impact: {max_impact:.2f} bps ({max_impact/100:.2f}%)")
            print(f"  Successful trades: {len(df)}/{len(amounts)}")
        else:
            print(f"\n  No successful trades for {token_in}/{token_out}")
            results_summary.append({
                "pair": f"{token_in}/{token_out}",
                "tier": expected_tier,
                "avg_impact_bps": None,
                "max_impact_bps": None,
                "success_rate": 0,
                "num_successful": 0,
                "num_total": len(amounts)
            })

    except Exception as e:
        print(f"\nError analyzing {token_in}/{token_out}: {e}")
        results_summary.append({
            "pair": f"{token_in}/{token_out}",
            "tier": expected_tier,
            "avg_impact_bps": None,
            "max_impact_bps": None,
            "success_rate": 0,
            "num_successful": 0,
            "num_total": len(amounts)
        })

# ========================================
# Final Comparison
# ========================================
print("\n\n" + "=" * 70)
print("FINAL COMPARISON")
print("=" * 70)

for result in results_summary:
    print(f"\n{result['tier'].upper()}-LIQUIDITY ({result['pair']}):")
    if result['avg_impact_bps'] is not None:
        print(f"  Avg Impact: {result['avg_impact_bps']:.2f} bps ({result['avg_impact_bps']/100:.2f}%)")
        print(f"  Max Impact: {result['max_impact_bps']:.2f} bps ({result['max_impact_bps']/100:.2f}%)")
    print(f"  Success Rate: {result['num_successful']}/{result['num_total']} ({result['success_rate']*100:.0f}%)")

print("\n" + "=" * 70)
print("Key Takeaways:")
print("=" * 70)
print("High-Liquidity Pools:")
print("  - Handle large trades ($1M+) with minimal slippage (<1%)")
print("  - Ideal for institutional trading and large swaps")
print("  - Nearly 100% success rate across all trade sizes")
print("\nMedium-Liquidity Pools:")
print("  - Show 1-5% price impact on $100K+ trades")
print("  - Suitable for medium-sized trades ($100 - $1M)")
print("  - Good balance between availability and cost")
print("\nLow-Liquidity Pools:")
print("  - High price impact (5-50%) even on small trades")
print("  - Only suitable for small trades (<$1K)")
print("  - Many large trades fail due to insufficient liquidity")
print("=" * 70)
