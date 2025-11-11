import pandas as pd
from web3 import Web3
from config import get_token_config, get_pool_config

# Uniswap V3 Quoter V2 contract address (mainnet)
QUOTER_V2 = Web3.to_checksum_address("0x61fFE014bA17989E743c5F6cB21bF9697530B21e")

# ABI for QuoterV2 quoteExactInputSingle function
# Note: QuoterV2 uses a struct parameter
QUOTER_ABI = [
    {
        "name": "quoteExactInputSingle",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "params",
                "type": "tuple",
                "components": [
                    {"name": "tokenIn", "type": "address"},
                    {"name": "tokenOut", "type": "address"},
                    {"name": "amountIn", "type": "uint256"},
                    {"name": "fee", "type": "uint24"},
                    {"name": "sqrtPriceLimitX96", "type": "uint160"},
                ],
            }
        ],
        "outputs": [
            {"name": "amountOut", "type": "uint256"},
            {"name": "sqrtPriceX96After", "type": "uint160"},
            {"name": "initializedTicksCrossed", "type": "uint32"},
            {"name": "gasEstimate", "type": "uint256"},
        ],
    }
]

# ABI for Uniswap V3 Pool functions
POOL_ABI = [
    {
        "name": "slot0",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [
            {"name": "sqrtPriceX96", "type": "uint160"},
            {"name": "tick", "type": "int24"},
            {"name": "", "type": "uint16"},
            {"name": "", "type": "uint16"},
            {"name": "", "type": "uint16"},
            {"name": "", "type": "uint8"},
            {"name": "", "type": "bool"},
        ],
    },
    {
        "name": "token0",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    },
    {
        "name": "token1",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "address"}],
    },
]

Q96 = 2**96

# Chainlink ETH/USD Price Feed (Mainnet)
CHAINLINK_ETH_USD = Web3.to_checksum_address(
    "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"
)

# Chainlink Price Feed ABI (minimal - just latestRoundData)
CHAINLINK_ABI = [
    {
        "name": "latestRoundData",
        "type": "function",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [
            {"name": "roundId", "type": "uint80"},
            {"name": "answer", "type": "int256"},
            {"name": "startedAt", "type": "uint256"},
            {"name": "updatedAt", "type": "uint256"},
            {"name": "answeredInRound", "type": "uint80"},
        ],
    }
]


def get_quoter_contract(w3):
    """Get the Uniswap V3 QuoterV2 contract instance."""
    return w3.eth.contract(address=QUOTER_V2, abi=QUOTER_ABI)


def quote_exact_input_single(w3, token_in, token_out, fee, amount_in):
    """
    Get a quote for an exact input swap on Uniswap V3.

    Args:
        w3: Web3 instance
        token_in: Address of the input token
        token_out: Address of the output token
        fee: Pool fee tier (e.g., 500 for 0.05%, 3000 for 0.3%, 10000 for 1%)
        amount_in: Amount of input tokens (in smallest unit)

    Returns:
        dict: Contains amountOut, sqrtPriceX96After, ticksCrossed, gasEstimate
    """
    quoter = get_quoter_contract(w3)
    token_in = Web3.to_checksum_address(token_in)
    token_out = Web3.to_checksum_address(token_out)

    # QuoterV2 requires parameters as a struct (tuple in Python)
    # sqrtPriceLimitX96 = 0 means "no limit" (let the price move as needed)
    params = (token_in, token_out, amount_in, fee, 0)

    amount_out, sqrt_after, ticks_crossed, gas_est = (
        quoter.functions.quoteExactInputSingle(params).call()
    )

    return {
        "amountOut": amount_out,
        "sqrtPriceX96After": sqrt_after,
        "ticksCrossed": ticks_crossed,
        "gasEstimate": gas_est,
    }


def check_pool_liquidity(w3, pool_addr):
    """
    Check if a pool has sufficient liquidity.

    Args:
        w3: Web3 instance
        pool_addr: Address of the Uniswap V3 pool

    Returns:
        dict with liquidity info
    """
    pool = w3.eth.contract(address=Web3.to_checksum_address(pool_addr), abi=POOL_ABI)

    try:
        slot0 = pool.functions.slot0().call()
        sqrt_price_x96 = slot0[0]

        # If sqrt price is 0, pool is not initialized
        if sqrt_price_x96 == 0:
            return {"initialized": False, "has_liquidity": False}

        return {
            "initialized": True,
            "has_liquidity": True,
            "sqrt_price_x96": sqrt_price_x96,
        }
    except Exception as e:
        return {"initialized": False, "has_liquidity": False, "error": str(e)}


def quote_with_price_impact(
    w3, token_in, token_out, fee, amount_in, pool_addr, decimals_in, decimals_out
):
    """
    Get a quote with price impact calculation for Uniswap V3.

    Args:
        w3: Web3 instance
        token_in: Address of the input token
        token_out: Address of the output token
        fee: Pool fee tier (e.g., 500 for 0.05%, 3000 for 0.3%, 10000 for 1%)
        amount_in: Amount of input tokens (in smallest unit)
        pool_addr: Address of the Uniswap V3 pool
        decimals_in: Decimals of input token
        decimals_out: Decimals of output token

    Returns:
        dict: Contains amountOut, execPrice, midPrice, priceAfter, priceImpactBps, ticksCrossed, gasEstimate
            - amountOut: Output amount in smallest unit
            - execPrice: Average execution price (tokenOut per tokenIn)
            - midPrice: Mid market price before trade (tokenOut per tokenIn)
            - priceAfter: Pool price after trade execution (tokenOut per tokenIn)
            - priceImpactBps: Price impact in basis points
            - ticksCrossed: Number of ticks crossed
            - gasEstimate: Estimated gas cost

    Raises:
        ValueError: If pool has insufficient liquidity for the trade
    """
    quoter = get_quoter_contract(w3)
    token_in = Web3.to_checksum_address(token_in)
    token_out = Web3.to_checksum_address(token_out)
    pool = w3.eth.contract(address=Web3.to_checksum_address(pool_addr), abi=POOL_ABI)

    # Check pool liquidity first
    liquidity_check = check_pool_liquidity(w3, pool_addr)
    if not liquidity_check.get("has_liquidity"):
        raise ValueError(
            f"Pool at {pool_addr} does not have sufficient liquidity or is not initialized"
        )

    # Get pool token ordering
    token0 = pool.functions.token0().call()
    token1 = pool.functions.token1().call()

    # Get current pool price from slot0
    slot0 = pool.functions.slot0().call()
    sqrt_price_x96 = slot0[0]

    # sqrtPriceX96 represents sqrt(token1/token0) in raw units (no decimal adjustment)
    # Calculate the raw price as token1 per token0
    price_token1_per_token0_raw = (sqrt_price_x96 / Q96) ** 2

    # Determine which token is token0 and token1, and adjust for decimals
    if token_in.lower() == token0.lower():
        # Buying token1 (tokenOut) with token0 (tokenIn)
        # Price = (token1/token0)_raw * 10^(decimals_in) / 10^(decimals_out)
        mid_price = price_token1_per_token0_raw * (10**decimals_in) / (10**decimals_out)
    else:
        # Buying token0 (tokenOut) with token1 (tokenIn)
        # Price = (token0/token1)_raw * 10^(decimals_in) / 10^(decimals_out)
        mid_price = (
            (1 / price_token1_per_token0_raw) * (10**decimals_in) / (10**decimals_out)
        )

    # Get quote - QuoterV2 requires parameters as a struct (tuple in Python)
    params = (token_in, token_out, amount_in, fee, 0)
    amount_out, sqrt_after, ticks_crossed, gas_est = (
        quoter.functions.quoteExactInputSingle(params).call()
    )

    # Calculate execution price (tokenOut per tokenIn)
    amount_in_human = amount_in / 10**decimals_in
    amount_out_human = amount_out / 10**decimals_out
    exec_price = amount_out_human / amount_in_human

    # Calculate price after the swap from sqrtPriceX96After
    # This represents the pool's price after the trade is executed
    price_token1_per_token0_after_raw = (sqrt_after / Q96) ** 2

    # Convert to human-readable price (tokenOut per tokenIn) based on token ordering
    if token_in.lower() == token0.lower():
        # Buying token1 (tokenOut) with token0 (tokenIn)
        price_after = (
            price_token1_per_token0_after_raw * (10**decimals_in) / (10**decimals_out)
        )
    else:
        # Buying token0 (tokenOut) with token1 (tokenIn)
        price_after = (
            (1 / price_token1_per_token0_after_raw)
            * (10**decimals_in)
            / (10**decimals_out)
        )

    # Calculate price impact in basis points
    # Price impact = (mid_price - exec_price) / mid_price * 10000
    price_impact_bps = ((mid_price - exec_price) / mid_price) * 1e4

    return {
        "amountOut": amount_out,
        "execPrice": exec_price,
        "midPrice": mid_price,
        "priceAfter": price_after,
        "priceImpactBps": price_impact_bps,
        "ticksCrossed": ticks_crossed,
        "gasEstimate": gas_est,
    }


def get_eth_price_usd(w3):
    """
    Get current ETH price in USD from Chainlink oracle.

    Uses the Chainlink ETH/USD price feed to get accurate, manipulation-resistant
    price data without any DEX price impact.

    Args:
        w3: Web3 instance connected to Ethereum node

    Returns:
        float: ETH price in USD

    Note:
        Chainlink price feeds return prices with 8 decimals of precision.
        Feed address: 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419 (Mainnet)
    """
    try:
        # Get Chainlink price feed contract
        price_feed = w3.eth.contract(address=CHAINLINK_ETH_USD, abi=CHAINLINK_ABI)

        # Get latest price data
        round_id, answer, started_at, updated_at, answered_in_round = (
            price_feed.functions.latestRoundData().call()
        )

        # Chainlink returns price with 8 decimals
        eth_price_usd = answer / 10**8

        return eth_price_usd

    except Exception as e:
        # Fallback to a reasonable default if oracle query fails
        print(
            f"Warning: Could not fetch ETH price from Chainlink oracle, using default: {e}"
        )
        return 3500.0  # Reasonable fallback


def analyze_trade_costs(
    w3, token_in_symbol, token_out_symbol, amounts_in, fee=None, verbose=True
):
    """
    Analyze trade costs for a token pair across multiple trade sizes.

    Args:
        w3: Web3 instance connected to Ethereum node
        token_in_symbol: Symbol of input token (e.g., "USDC")
        token_out_symbol: Symbol of output token (e.g., "WBTC")
        amounts_in: List of input amounts in human-readable units (e.g., [1, 10, 100, 1000])
        fee: Optional fee tier (100, 500, 3000, 10000). If None, uses default pool.
        verbose: If True, prints progress messages

    Returns:
        pandas.DataFrame with columns:
            - amount_in: Input amount
            - amount_out: Actual output amount
            - ideal_amount_out: Theoretical output at mid price with no slippage
            - cost_of_impact: Tokens lost due to price impact
            - cost_of_impact_usd: Dollar value of tokens lost
            - exec_price: Execution price (token_out per token_in)
            - exec_price_inv: Inverted execution price (token_in per token_out)
            - mid_price: Mid market price before trade (token_out per token_in)
            - mid_price_inv: Inverted mid price (token_in per token_out)
            - price_after: Pool price after trade execution (token_out per token_in)
            - price_after_inv: Inverted price after trade (token_in per token_out)
            - price_impact_bps: Price impact in basis points
            - price_impact_pct: Price impact in percent
            - ticks_crossed: Number of ticks crossed
            - gas_estimate: Estimated gas cost in gas units
            - eth_price_usd: ETH price in USD
            - gas_cost_usd: Estimated gas cost in USD

    Raises:
        ValueError: If token or pool not found in configuration
        ConnectionError: If Web3 connection fails
    """
    # Get token configurations
    token_in = get_token_config(token_in_symbol)
    token_out = get_token_config(token_out_symbol)

    # Get pool configuration (with auto-discovery enabled)
    pool_config = get_pool_config(
        token_in_symbol, token_out_symbol, fee, w3=w3, auto_discover=True
    )

    # Get current ETH price for gas cost calculations
    eth_price_usd = get_eth_price_usd(w3)

    # Assume average gas price of 20 gwei for cost estimation
    # User can adjust this externally if needed
    gas_price_gwei = 20

    if verbose:
        print(f"Analyzing trade costs for {token_in_symbol} → {token_out_symbol}")
        print(f"Pool: {pool_config['address']}")
        print(f"Fee tier: {pool_config['fee'] / 10000}%")
        print(f"ETH Price: ${eth_price_usd:,.2f}")

        # Check pool liquidity and warn if it might be low
        liquidity_info = check_pool_liquidity(w3, pool_config["address"])
        if not liquidity_info.get("has_liquidity"):
            print(f"⚠️  WARNING: Pool may have insufficient liquidity")

        print(f"\nQuerying {len(amounts_in)} different trade sizes...")
        print(
            "Note: Low-liquidity pools may fail for larger trade sizes due to high price impact"
        )

    # Collect results
    results = []

    for amount_in_human in amounts_in:
        # Convert to smallest unit
        amount_in = int(amount_in_human * 10 ** token_in["decimals"])

        try:
            # Get quote with price impact
            result = quote_with_price_impact(
                w3,
                token_in["address"],
                token_out["address"],
                pool_config["fee"],
                amount_in,
                pool_config["address"],
                token_in["decimals"],
                token_out["decimals"],
            )

            # Convert amountOut to human-readable
            amount_out_human = result["amountOut"] / 10 ** token_out["decimals"]

            # Calculate ideal amount out (at mid price with no slippage/impact)
            ideal_amount_out = amount_in_human * result["midPrice"]

            # Calculate cost of impact
            cost_of_impact = ideal_amount_out - amount_out_human
            cost_of_impact_usd = cost_of_impact / result["midPrice"]

            # Calculate inverted prices (token_in per token_out)
            exec_price_inv = 1 / result["execPrice"] if result["execPrice"] > 0 else 0
            mid_price_inv = 1 / result["midPrice"] if result["midPrice"] > 0 else 0
            price_after_inv = (
                1 / result["priceAfter"] if result["priceAfter"] > 0 else 0
            )

            # Calculate gas cost in USD
            # gas_estimate (in gas units) * gas_price (in gwei) * 1e-9 (gwei to ETH) * eth_price_usd
            gas_cost_usd = result["gasEstimate"] * gas_price_gwei * 1e-9 * eth_price_usd

            # Store results
            results.append(
                {
                    "amount_in": amount_in_human,
                    "amount_out": amount_out_human,
                    "ideal_amount_out": ideal_amount_out,
                    "cost_of_impact": cost_of_impact,
                    "cost_of_impact_usd": cost_of_impact_usd,
                    "exec_price": result["execPrice"],
                    "exec_price_inv": exec_price_inv,
                    "mid_price": result["midPrice"],
                    "mid_price_inv": mid_price_inv,
                    "price_after": result["priceAfter"],
                    "price_after_inv": price_after_inv,
                    "price_impact_bps": result["priceImpactBps"],
                    "price_impact_pct": result["priceImpactBps"] / 100,
                    "ticks_crossed": result["ticksCrossed"],
                    "gas_estimate": result["gasEstimate"],
                    "eth_price_usd": eth_price_usd,
                    "gas_cost_usd": gas_cost_usd,
                }
            )

            if verbose:
                print(
                    f"✓ ${amount_in_human:,.0f} {token_in_symbol} → "
                    f"{amount_out_human:.8f} {token_out_symbol} "
                    f"(Impact: {result['priceImpactBps']:.2f} bps)"
                )

        except Exception as e:
            error_str = str(e)
            if verbose:
                # Provide helpful error messages for common issues
                if "SPL" in error_str or "Sqrt Price Limit" in error_str:
                    print(
                        f"✗ ${amount_in_human:,.0f}: Trade too large for available liquidity (price impact too high)"
                    )
                elif "STF" in error_str:
                    print(f"✗ ${amount_in_human:,.0f}: Insufficient liquidity in pool")
                elif "TLU" in error_str or "Too little" in error_str:
                    print(f"✗ ${amount_in_human:,.0f}: Amount too small for this pool")
                else:
                    print(f"✗ ${amount_in_human:,.0f}: {error_str[:100]}")

    if verbose:
        success_count = len(results)
        total_count = len(amounts_in)
        failed_count = total_count - success_count

        print(f"\nSuccessfully collected {success_count}/{total_count} quotes")

        if failed_count > 0:
            print(f"\n⚠️  {failed_count} trade(s) failed due to insufficient liquidity")
            print("Recommendation: For low-liquidity pools, try:")
            print("  - Smaller trade amounts (e.g., [0.1, 1, 10, 100])")
            print("  - Different fee tiers (try 10000 for 1% fee pools)")

        if success_count == 0:
            raise ValueError(
                f"No successful quotes obtained for {token_in_symbol}/{token_out_symbol}. "
                f"This pool may have extremely low liquidity or the trade sizes are too large. "
                f"Try much smaller amounts or a different token pair."
            )

    # Create DataFrame
    df = pd.DataFrame(results)
    return df
