#!/usr/bin/env python3
"""
Example: Fetch ABIs from Etherscan programmatically.

This shows how the ABIs in tradecost.py were originally obtained.
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from uniswap import (
    get_abi_from_etherscan,
    extract_function_abi,
    get_minimal_abi,
    print_function_signature,
    UNISWAP_V3_ADDRESSES,
)

# Check for Etherscan API key
etherscan_api_key = os.environ.get("ETHERSCAN_API_KEY")

if not etherscan_api_key:
    print("=" * 70)
    print("ERROR: ETHERSCAN_API_KEY environment variable not set")
    print("=" * 70)
    print("\nEtherscan's API requires an API key for programmatic access.")
    print("\nTo get started:")
    print("  1. Get a free API key at: https://etherscan.io/apis")
    print("  2. Set the environment variable:")
    print("     export ETHERSCAN_API_KEY='your_key_here'")
    print("  3. Run this script again")
    print("\n" + "=" * 70)
    print("Alternatively, view ABIs on Etherscan without an API key:")
    print("=" * 70)
    for name, address in UNISWAP_V3_ADDRESSES.items():
        print(f"{name}:")
        print(f"  https://etherscan.io/address/{address}#code")
    print("=" * 70)
    sys.exit(1)

print("=" * 70)
print("Fetching ABIs from Etherscan")
print("=" * 70)

# Example 1: Fetch QuoterV2 ABI
print("\n1. Fetching QuoterV2 full ABI...")
quoter_address = UNISWAP_V3_ADDRESSES["QuoterV2"]
print(f"   Address: {quoter_address}")

try:
    quoter_abi = get_abi_from_etherscan(quoter_address, etherscan_api_key)
    print(f"   ✓ Retrieved {len(quoter_abi)} ABI entries")

    # Extract the specific function we need
    print("\n2. Extracting 'quoteExactInputSingle' function...")
    quote_fn = extract_function_abi(quoter_abi, "quoteExactInputSingle")

    if quote_fn:
        print("   ✓ Found function!")
        print("\n   Function signature:")
        print("   ", end="")
        print_function_signature(quote_fn)

        print("\n   Full ABI entry (formatted):")
        print(json.dumps(quote_fn, indent=2))
    else:
        print("   ✗ Function not found in ABI")

except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Example 2: Get minimal ABI
print("\n" + "=" * 70)
print("3. Creating minimal ABI with only required functions...")
print("=" * 70)

try:
    minimal_quoter_abi = get_minimal_abi(
        quoter_address, ["quoteExactInputSingle"], etherscan_api_key
    )

    print(f"✓ Minimal ABI created with {len(minimal_quoter_abi)} entry")
    print("\nMinimal ABI structure:")
    print(json.dumps(minimal_quoter_abi, indent=2))

    print("\n" + "=" * 70)
    print("Comparison:")
    print(f"  Full QuoterV2 ABI:    {len(quoter_abi)} entries")
    print(f"  Minimal ABI:          {len(minimal_quoter_abi)} entry")
    print(
        f"  Size reduction:       {(1 - len(minimal_quoter_abi)/len(quoter_abi))*100:.1f}%"
    )
    print("=" * 70)

except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Example 3: Fetch Pool ABI
print("\n" + "=" * 70)
print("4. Fetching Uniswap V3 Pool ABI...")
print("=" * 70)

# Use the USDC/WETH 0.05% pool as example
example_pool = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
print(f"   Example pool: USDC/WETH (0.05% fee)")
print(f"   Address: {example_pool}")

try:
    pool_abi = get_abi_from_etherscan(example_pool, etherscan_api_key)
    print(f"   ✓ Retrieved {len(pool_abi)} ABI entries")

    # Extract functions we need for the toolkit
    functions_needed = ["slot0", "token0", "token1"]
    print(f"\n   Extracting required functions: {', '.join(functions_needed)}")

    for fn_name in functions_needed:
        fn = extract_function_abi(pool_abi, fn_name)
        if fn:
            print(f"   ✓ {fn_name}: ", end="")
            print_function_signature(fn)
        else:
            print(f"   ✗ {fn_name}: Not found")

except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("Success!")
print("=" * 70)
print("\nThese ABIs can be used in web3.py like this:")
print(
    """
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_KEY"))

# Create contract instance with the minimal ABI
quoter = w3.eth.contract(address=quoter_address, abi=minimal_quoter_abi)

# Call the function
result = quoter.functions.quoteExactInputSingle(params).call()
"""
)
print("=" * 70)
