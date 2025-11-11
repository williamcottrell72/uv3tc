"""
Utility functions for working with Uniswap V3 contracts.
"""

import requests
import json
from typing import List, Dict, Optional


def get_abi_from_etherscan(contract_address: str, etherscan_api_key: Optional[str] = None, network: str = "mainnet") -> List[Dict]:
    """
    Fetch the ABI for a verified contract from Etherscan.

    Args:
        contract_address: Ethereum contract address
        etherscan_api_key: Etherscan API key (optional, but recommended to avoid rate limits)
        network: Network name ("mainnet", "goerli", "sepolia", etc.)

    Returns:
        List of ABI entries (functions, events, etc.)

    Raises:
        ValueError: If contract is not verified or API request fails

    Example:
        >>> # Get QuoterV2 ABI
        >>> quoter_address = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"
        >>> abi = get_abi_from_etherscan(quoter_address, etherscan_api_key="YOUR_KEY")
        >>> print(f"Found {len(abi)} ABI entries")

    Note:
        - Free Etherscan API keys are available at https://etherscan.io/apis
        - Without an API key, you're limited to 1 request per 5 seconds
        - Etherscan only provides ABIs for verified contracts
    """
    # Map network names to Etherscan API URLs and chain IDs
    network_config = {
        "mainnet": {"url": "https://api.etherscan.io/v2/api", "chainid": "1"},
        "goerli": {"url": "https://api-goerli.etherscan.io/v2/api", "chainid": "5"},
        "sepolia": {"url": "https://api-sepolia.etherscan.io/v2/api", "chainid": "11155111"},
    }

    if network not in network_config:
        raise ValueError(f"Unsupported network: {network}. Supported: {list(network_config.keys())}")

    config = network_config[network]
    api_url = config["url"]

    # Build request parameters for V2 API
    params = {
        "chainid": config["chainid"],
        "module": "contract",
        "action": "getabi",
        "address": contract_address,
    }

    if etherscan_api_key:
        params["apikey"] = etherscan_api_key

    # Note: Without an API key, requests may be rate-limited or blocked

    # Make API request
    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "1":
            raise ValueError(f"Etherscan API error: {data.get('result', 'Unknown error')}")

        # Parse the ABI JSON string
        abi = json.loads(data["result"])
        return abi

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch ABI from Etherscan: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse ABI JSON: {e}")


def extract_function_abi(full_abi: List[Dict], function_name: str) -> Optional[Dict]:
    """
    Extract a specific function's ABI entry from a full contract ABI.

    Args:
        full_abi: Full contract ABI (list of entries)
        function_name: Name of the function to extract

    Returns:
        Dictionary containing the function's ABI entry, or None if not found

    Example:
        >>> abi = get_abi_from_etherscan("0x61fFE014bA17989E743c5F6cB21bF9697530B21e")
        >>> quote_fn = extract_function_abi(abi, "quoteExactInputSingle")
        >>> print(quote_fn["name"])
        quoteExactInputSingle
    """
    for entry in full_abi:
        if entry.get("type") == "function" and entry.get("name") == function_name:
            return entry
    return None


def extract_functions_abi(full_abi: List[Dict], function_names: List[str]) -> List[Dict]:
    """
    Extract multiple functions' ABI entries from a full contract ABI.

    Args:
        full_abi: Full contract ABI (list of entries)
        function_names: List of function names to extract

    Returns:
        List of ABI entries for the requested functions

    Example:
        >>> abi = get_abi_from_etherscan("0x1F98431c8aD98523631AE4a59f267346ea31F984")
        >>> pool_functions = extract_functions_abi(abi, ["getPool", "createPool"])
        >>> print(f"Found {len(pool_functions)} functions")
    """
    result = []
    for function_name in function_names:
        entry = extract_function_abi(full_abi, function_name)
        if entry:
            result.append(entry)
    return result


def get_minimal_abi(contract_address: str, function_names: List[str],
                   etherscan_api_key: Optional[str] = None, network: str = "mainnet") -> List[Dict]:
    """
    Fetch a minimal ABI containing only specific functions from a contract.

    This is useful when you only need a few functions and want to minimize
    the ABI size for efficiency.

    Args:
        contract_address: Ethereum contract address
        function_names: List of function names to include in the minimal ABI
        etherscan_api_key: Etherscan API key (optional)
        network: Network name ("mainnet", "goerli", "sepolia", etc.)

    Returns:
        Minimal ABI containing only the specified functions

    Example:
        >>> # Get minimal QuoterV2 ABI with only quoteExactInputSingle
        >>> quoter_addr = "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"
        >>> minimal_abi = get_minimal_abi(
        ...     quoter_addr,
        ...     ["quoteExactInputSingle"],
        ...     etherscan_api_key="YOUR_KEY"
        ... )
        >>> print(f"Minimal ABI has {len(minimal_abi)} entries")
    """
    full_abi = get_abi_from_etherscan(contract_address, etherscan_api_key, network)
    return extract_functions_abi(full_abi, function_names)


def print_function_signature(abi_entry: Dict):
    """
    Pretty-print a function signature from an ABI entry.

    Args:
        abi_entry: Single ABI entry for a function

    Example:
        >>> abi = get_abi_from_etherscan("0x61fFE014bA17989E743c5F6cB21bF9697530B21e")
        >>> quote_fn = extract_function_abi(abi, "quoteExactInputSingle")
        >>> print_function_signature(quote_fn)
        function quoteExactInputSingle(tuple params) returns (uint256, uint160, uint32, uint256)
    """
    if abi_entry.get("type") != "function":
        print(f"Not a function: {abi_entry.get('type')}")
        return

    name = abi_entry["name"]
    inputs = abi_entry.get("inputs", [])
    outputs = abi_entry.get("outputs", [])
    state_mutability = abi_entry.get("stateMutability", "nonpayable")

    # Format inputs
    input_strs = []
    for inp in inputs:
        if inp["type"] == "tuple":
            components = inp.get("components", [])
            comp_types = [c["type"] for c in components]
            input_strs.append(f"tuple({', '.join(comp_types)}) {inp.get('name', '')}")
        else:
            input_strs.append(f"{inp['type']} {inp.get('name', '')}")

    # Format outputs
    output_strs = []
    for out in outputs:
        if out["type"] == "tuple":
            components = out.get("components", [])
            comp_types = [c["type"] for c in components]
            output_strs.append(f"tuple({', '.join(comp_types)})")
        else:
            output_strs.append(out["type"])

    # Print signature
    inputs_part = ", ".join(input_strs)
    outputs_part = ", ".join(output_strs)

    signature = f"function {name}({inputs_part})"
    if state_mutability in ["pure", "view"]:
        signature += f" {state_mutability}"
    if outputs_part:
        signature += f" returns ({outputs_part})"

    print(signature)


# Known Uniswap V3 contract addresses on Ethereum mainnet
UNISWAP_V3_ADDRESSES = {
    "QuoterV2": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    "Factory": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "Router": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "NFTPositionManager": "0xC36442b4a4522E871399CD717aBDD847Ab11FE88",
}


def demonstrate_abi_fetching(etherscan_api_key: Optional[str] = None):
    """
    Demonstrate how to fetch and work with ABIs from Etherscan.

    This function shows how the ABIs in tradecost.py were obtained.

    Args:
        etherscan_api_key: Optional Etherscan API key (REQUIRED for API access)

    Example:
        >>> demonstrate_abi_fetching(etherscan_api_key="YOUR_KEY")
    """
    print("=" * 70)
    print("How ABIs Were Obtained for Uniswap V3 Trade Cost Analysis")
    print("=" * 70)

    if not etherscan_api_key:
        print("\n⚠️  NOTE: ETHERSCAN_API_KEY not provided!")
        print("   Etherscan V2 API requires an API key for programmatic access.")
        print("   Get a free API key at: https://etherscan.io/apis")
        print("   Then run: export ETHERSCAN_API_KEY='your_key_here'")
        print("\n   This demo will show URLs to view ABIs manually on Etherscan.\n")

    print("\n1. QuoterV2 Contract ABI")
    print("-" * 70)
    quoter_address = UNISWAP_V3_ADDRESSES["QuoterV2"]
    print(f"Contract: QuoterV2")
    print(f"Address: {quoter_address}")
    print(f"Etherscan: https://etherscan.io/address/{quoter_address}#code")

    try:
        print("\nFetching full ABI from Etherscan...")
        quoter_abi = get_abi_from_etherscan(quoter_address, etherscan_api_key)
        print(f"✓ Retrieved {len(quoter_abi)} ABI entries")

        # Extract the function we need
        print("\nExtracting 'quoteExactInputSingle' function...")
        quote_fn = extract_function_abi(quoter_abi, "quoteExactInputSingle")
        if quote_fn:
            print("✓ Found function signature:")
            print_function_signature(quote_fn)
            print("\nFull ABI entry:")
            print(json.dumps(quote_fn, indent=2))

    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nNote: You can view the ABI on Etherscan without an API key:")
        print(f"      https://etherscan.io/address/{quoter_address}#code")

    print("\n\n2. Uniswap V3 Pool Contract ABI")
    print("-" * 70)
    print("Pool contracts are created by the Factory.")
    print("Example pool: USDC/WETH (0.05% fee)")
    example_pool = "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640"
    print(f"Address: {example_pool}")
    print(f"Etherscan: https://etherscan.io/address/{example_pool}#code")

    try:
        print("\nFetching pool ABI from Etherscan...")
        pool_abi = get_abi_from_etherscan(example_pool, etherscan_api_key)
        print(f"✓ Retrieved {len(pool_abi)} ABI entries")

        # Extract functions we need
        print("\nExtracting required functions...")
        functions_needed = ["slot0", "token0", "token1"]
        for fn_name in functions_needed:
            fn = extract_function_abi(pool_abi, fn_name)
            if fn:
                print(f"✓ {fn_name}:")
                print(f"  ", end="")
                print_function_signature(fn)

    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nNote: You can view the ABI on Etherscan without an API key:")
        print(f"      https://etherscan.io/address/{example_pool}#code")

    print("\n\n3. Creating Minimal ABIs")
    print("-" * 70)
    print("The ABIs in tradecost.py are 'minimal ABIs' containing only the")
    print("functions we need. This reduces code size and improves readability.")
    print("\nBenefits of minimal ABIs:")
    print("  • Smaller code size")
    print("  • Faster contract instantiation")
    print("  • Easier to read and maintain")
    print("  • No external dependencies (don't need npm packages)")

    print("\n\n4. Alternative Methods")
    print("-" * 70)
    print("ABIs can also be obtained from:")
    print("  • Uniswap documentation: https://docs.uniswap.org/")
    print("  • npm packages: @uniswap/v3-core, @uniswap/v3-periphery")
    print("  • Contract source code on GitHub")
    print("  • Etherscan web interface (no API key needed)")

    print("\n\n5. Example: Minimal ABI Structure")
    print("-" * 70)
    print("Here's what the minimal QuoterV2 ABI looks like in tradecost.py:")
    print("\nQUOTER_ABI = [")
    print("    {")
    print("        'name': 'quoteExactInputSingle',")
    print("        'type': 'function',")
    print("        'stateMutability': 'nonpayable',")
    print("        'inputs': [")
    print("            {")
    print("                'name': 'params',")
    print("                'type': 'tuple',")
    print("                'components': [")
    print("                    {'name': 'tokenIn', 'type': 'address'},")
    print("                    {'name': 'tokenOut', 'type': 'address'},")
    print("                    {'name': 'amountIn', 'type': 'uint256'},")
    print("                    {'name': 'fee', 'type': 'uint24'},")
    print("                    {'name': 'sqrtPriceLimitX96', 'type': 'uint160'}")
    print("                ]")
    print("            }")
    print("        ],")
    print("        'outputs': [")
    print("            {'name': 'amountOut', 'type': 'uint256'},")
    print("            {'name': 'sqrtPriceX96After', 'type': 'uint160'},")
    print("            {'name': 'initializedTicksCrossed', 'type': 'uint32'},")
    print("            {'name': 'gasEstimate', 'type': 'uint256'}")
    print("        ]")
    print("    }")
    print("]")
    print("\nThis minimal ABI contains just 1 function entry,")
    print("compared to ~50 entries in the full QuoterV2 ABI.")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print("The ABIs in tradecost.py were created by:")
    print("1. Fetching full ABIs from Etherscan (with API key)")
    print("2. Extracting only the functions we need")
    print("3. Manually formatting them as minimal ABIs in the code")
    print("\nThis approach works well for production code where you want")
    print("minimal dependencies and maximum clarity.")
    print("\n" + "=" * 70)
    print("Get started:")
    print("  1. Get free API key: https://etherscan.io/apis")
    print("  2. Set environment: export ETHERSCAN_API_KEY='your_key'")
    print("  3. Run this demo again to see live API fetching")
    print("=" * 70)


if __name__ == "__main__":
    import os
    import sys

    # Get API key from environment
    etherscan_api_key = os.environ.get("ETHERSCAN_API_KEY")

    if not etherscan_api_key:
        print("WARNING: ETHERSCAN_API_KEY not set. Using rate-limited API.")
        print("Get a free API key at: https://etherscan.io/apis\n")

    demonstrate_abi_fetching(etherscan_api_key)
