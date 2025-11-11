#!/usr/bin/env python3
"""
Test script for Uniswap V3 trade cost estimation.

Usage:
    python test_tradecost.py
    python test_tradecost.py --amount 2000 --token-in USDC --token-out WETH
"""

import os
import sys
import argparse
from web3 import Web3

# Add parent directory to path to import tradecost
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tradecost import quote_exact_input_single, quote_with_price_impact

# Token addresses (mainnet)
TOKENS = {
    "USDC": {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "decimals": 6,
        "symbol": "USDC"
    },
    "WETH": {
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "decimals": 18,
        "symbol": "WETH"
    },
    "WBTC": {
        "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "decimals": 8,
        "symbol": "WBTC"
    },
    "DAI": {
        "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "decimals": 18,
        "symbol": "DAI"
    }
}

# Common pool addresses (mainnet)
POOLS = {
    ("USDC", "WBTC"): "0x99ac8cA7087fA4A2A1FB6357269965A2014ABc35",  # 0.3% fee
    ("USDC", "WETH"): "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",  # 0.05% fee
    ("WETH", "WBTC"): "0xCBCdF9626bC03E24f779434178A73a0B4bad62eD",  # 0.3% fee
    ("DAI", "USDC"): "0x5777d92f208679DB4b9778590Fa3CAB3aC9e2168",  # 0.01% fee
}

# Fee tiers
FEE_TIERS = {
    ("USDC", "WBTC"): 3000,  # 0.3%
    ("USDC", "WETH"): 500,   # 0.05%
    ("WETH", "WBTC"): 3000,  # 0.3%
    ("DAI", "USDC"): 100,    # 0.01%
}


def get_pool_and_fee(token_in_symbol, token_out_symbol):
    """Get pool address and fee tier for a token pair."""
    pair = (token_in_symbol, token_out_symbol)
    reverse_pair = (token_out_symbol, token_in_symbol)

    if pair in POOLS:
        return POOLS[pair], FEE_TIERS[pair]
    elif reverse_pair in POOLS:
        return POOLS[reverse_pair], FEE_TIERS[reverse_pair]
    else:
        # Default to 0.3% fee if pool not found
        return None, 3000


def main():
    parser = argparse.ArgumentParser(description="Test Uniswap V3 trade cost estimation")
    parser.add_argument("--token-in", default="USDC", choices=TOKENS.keys(),
                        help="Input token symbol (default: USDC)")
    parser.add_argument("--token-out", default="WBTC", choices=TOKENS.keys(),
                        help="Output token symbol (default: WBTC)")
    parser.add_argument("--amount", type=float, default=1000.0,
                        help="Input amount in human-readable units (default: 1000)")
    parser.add_argument("--fee", type=int, choices=[100, 500, 3000, 10000],
                        help="Fee tier in bps (100=0.01%%, 500=0.05%%, 3000=0.3%%, 10000=1%%)")
    parser.add_argument("--with-impact", action="store_true",
                        help="Calculate price impact (requires pool address)")

    args = parser.parse_args()

    # Check for Infura API key
    infura_api_key = os.environ.get("INFURA_API_KEY")
    if not infura_api_key:
        print("Error: INFURA_API_KEY environment variable not set")
        print("Please set it with: export INFURA_API_KEY=your_api_key")
        sys.exit(1)

    # Set up Web3
    rpc_url = f"https://mainnet.infura.io/v3/{infura_api_key}"
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    if not w3.is_connected():
        print("Error: Failed to connect to Ethereum node")
        sys.exit(1)

    print(f"Connected to Ethereum mainnet via Infura")
    print(f"Latest block: {w3.eth.block_number}\n")

    # Get token info
    token_in = TOKENS[args.token_in]
    token_out = TOKENS[args.token_out]

    # Convert amount to smallest unit
    amount_in = int(args.amount * 10 ** token_in["decimals"])

    # Get pool and fee
    pool_addr, default_fee = get_pool_and_fee(args.token_in, args.token_out)
    fee = args.fee if args.fee else default_fee

    print(f"Trade Parameters:")
    print(f"  Input: {args.amount} {args.token_in}")
    print(f"  Output: {args.token_out}")
    print(f"  Fee tier: {fee / 10000}%")
    if pool_addr:
        print(f"  Pool: {pool_addr}")
    print()

    try:
        if args.with_impact and pool_addr:
            # Quote with price impact
            print("Querying Uniswap V3 QuoterV2 with price impact calculation...")
            result = quote_with_price_impact(
                w3,
                token_in["address"],
                token_out["address"],
                fee,
                amount_in,
                pool_addr,
                token_in["decimals"],
                token_out["decimals"]
            )

            amount_out_human = result["amountOut"] / 10 ** token_out["decimals"]

            print(f"\nResults:")
            print(f"  Output amount: {amount_out_human:.8f} {args.token_out}")
            print(f"  Execution price: {result['execPrice']:.8f} {args.token_out}/{args.token_in}")
            print(f"  Mid price: {result['midPrice']:.8f} {args.token_out}/{args.token_in}")
            print(f"  Price impact: {result['priceImpactBps']:.2f} bps ({result['priceImpactBps']/100:.2f}%)")
            print(f"  Ticks crossed: {result['ticksCrossed']}")
            print(f"  Gas estimate: {result['gasEstimate']:,}")

        else:
            # Basic quote
            print("Querying Uniswap V3 QuoterV2...")
            result = quote_exact_input_single(
                w3,
                token_in["address"],
                token_out["address"],
                fee,
                amount_in
            )

            amount_out_human = result["amountOut"] / 10 ** token_out["decimals"]

            print(f"\nResults:")
            print(f"  Output amount: {amount_out_human:.8f} {args.token_out}")
            print(f"  Ticks crossed: {result['ticksCrossed']}")
            print(f"  Gas estimate: {result['gasEstimate']:,}")

            # Calculate simple execution price
            exec_price = amount_out_human / args.amount
            print(f"  Execution price: {exec_price:.8f} {args.token_out}/{args.token_in}")

        if not args.with_impact and pool_addr:
            print(f"\nTip: Use --with-impact flag to see price impact analysis")

    except Exception as e:
        print(f"Error querying Uniswap: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
