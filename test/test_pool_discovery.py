#!/usr/bin/env python3
"""
Test script for dynamic pool discovery.
Shows how pools are automatically discovered if not in config.
"""

import os
import sys
from web3 import Web3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from uniswap import find_all_pools_for_pair, get_token_config, discover_pool

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

print(f"Connected to Ethereum mainnet")
print(f"Latest block: {w3.eth.block_number}\n")

# Test discovering pools for various token pairs
test_pairs = [
    ("FLOKI", "WETH"),
    ("SHIB", "WETH"),
    ("PEPE", "WETH"),
    ("BLUR", "WETH"),
    ("DYDX", "WETH"),
]

print("Discovering Uniswap V3 Pools")
print("=" * 70)

for token_in, token_out in test_pairs:
    try:
        token_in_config = get_token_config(token_in)
        token_out_config = get_token_config(token_out)

        print(f"\n{token_in}/{token_out}:")
        print(f"  Token In:  {token_in_config['address']}")
        print(f"  Token Out: {token_out_config['address']}")

        # Find all pools for this pair
        pools = find_all_pools_for_pair(
            w3, token_in_config["address"], token_out_config["address"]
        )

        if pools:
            print(f"  Found {len(pools)} pool(s):")
            for fee, address in pools.items():
                fee_pct = fee / 10000
                print(f"    - {fee_pct}% fee: {address}")
        else:
            print(f"  No pools found")

        # Test auto-discover (picks best pool)
        try:
            best_pool = discover_pool(w3, token_in, token_out)
            print(
                f"  Best pool: {best_pool['address']} ({best_pool['fee'] / 10000}% fee)"
            )
        except Exception as e:
            print(f"  Auto-discover failed: {e}")

    except Exception as e:
        print(f"\n{token_in}/{token_out}: Error - {e}")

print("\n" + "=" * 70)
print("Pool discovery complete!")
