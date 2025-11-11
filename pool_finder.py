"""
Helper functions to find Uniswap V3 pool addresses dynamically.
"""

from web3 import Web3

# Uniswap V3 Factory contract address (mainnet)
FACTORY_ADDRESS = Web3.to_checksum_address("0x1F98431c8aD98523631AE4a59f267346ea31F984")

# Factory ABI - just the getPool function
FACTORY_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "tokenA", "type": "address"},
            {"internalType": "address", "name": "tokenB", "type": "address"},
            {"internalType": "uint24", "name": "fee", "type": "uint24"},
        ],
        "name": "getPool",
        "outputs": [{"internalType": "address", "name": "pool", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    }
]


def find_pool_address(w3, token_a, token_b, fee):
    """
    Find the Uniswap V3 pool address for a token pair and fee tier.

    Args:
        w3: Web3 instance
        token_a: Address of first token
        token_b: Address of second token
        fee: Fee tier (100, 500, 3000, 10000)

    Returns:
        Pool address if it exists, otherwise raises an error
    """
    factory = w3.eth.contract(address=FACTORY_ADDRESS, abi=FACTORY_ABI)

    token_a = Web3.to_checksum_address(token_a)
    token_b = Web3.to_checksum_address(token_b)

    pool_address = factory.functions.getPool(token_a, token_b, fee).call()

    # Check if pool exists (non-zero address)
    zero_address = "0x0000000000000000000000000000000000000000"
    if pool_address == zero_address:
        raise ValueError(f"No pool exists for this token pair with fee tier {fee}")

    return pool_address


def find_all_pools_for_pair(w3, token_a, token_b):
    """
    Find all Uniswap V3 pools for a token pair across all fee tiers.

    Args:
        w3: Web3 instance
        token_a: Address of first token
        token_b: Address of second token

    Returns:
        dict mapping fee tiers to pool addresses
    """
    fee_tiers = [100, 500, 3000, 10000]  # 0.01%, 0.05%, 0.3%, 1%
    pools = {}

    for fee in fee_tiers:
        try:
            pool_address = find_pool_address(w3, token_a, token_b, fee)
            pools[fee] = pool_address
        except ValueError:
            # Pool doesn't exist for this fee tier
            continue

    return pools


def discover_pool(w3, token_in_symbol, token_out_symbol, preferred_fee=None):
    """
    Discover the best available pool for a token pair.

    Args:
        w3: Web3 instance
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token
        preferred_fee: Preferred fee tier, or None to find any available

    Returns:
        dict with 'address' and 'fee' keys
    """
    from config import get_token_config

    token_in = get_token_config(token_in_symbol)
    token_out = get_token_config(token_out_symbol)

    # If preferred fee specified, try that first
    if preferred_fee:
        try:
            pool_address = find_pool_address(
                w3, token_in["address"], token_out["address"], preferred_fee
            )
            return {"address": pool_address, "fee": preferred_fee}
        except ValueError:
            pass

    # Try to find any available pool
    all_pools = find_all_pools_for_pair(w3, token_in["address"], token_out["address"])

    if not all_pools:
        raise ValueError(
            f"No Uniswap V3 pools found for {token_in_symbol}/{token_out_symbol}"
        )

    # Prefer 3000 (0.3%) > 500 (0.05%) > 10000 (1%) > 100 (0.01%)
    preferred_order = [3000, 500, 10000, 100]
    for fee in preferred_order:
        if fee in all_pools:
            return {"address": all_pools[fee], "fee": fee}

    # Return first available
    fee = list(all_pools.keys())[0]
    return {"address": all_pools[fee], "fee": fee}
