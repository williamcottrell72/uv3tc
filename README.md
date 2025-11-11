# Uniswap V3 Trade Cost Analysis

Tools for analyzing trading costs on Uniswap V3, including price impact, slippage, and gas costs.

## Installation

### Requirements

- Python 3.8+
- Required packages:
  ```bash
  pip install web3 pandas plotly requests
  ```

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/uv3tc.git
   cd uv3tc
   ```

2. Set your Infura API key (required for Ethereum RPC access):
   ```bash
   export INFURA_API_KEY="your_infura_api_key"
   ```
   Get a free Infura key at [https://infura.io](https://infura.io)

3. (Optional) Set Etherscan API key for ABI fetching:
   ```bash
   export ETHERSCAN_API_KEY="your_etherscan_api_key"
   ```
   Get a free key at [https://etherscan.io/apis](https://etherscan.io/apis)

## Quick Start

```python
from web3 import Web3
from tradecost import analyze_trade_costs
from plots import plot_combined_analysis
from config import get_recommended_amounts

# Connect to Ethereum
w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"))

# Analyze trade costs with recommended amounts for the token
token_in = "USDC"
token_out = "WBTC"
amounts = get_recommended_amounts(token_in)  # Auto-selects appropriate sizes

df = analyze_trade_costs(
    w3=w3,
    token_in_symbol=token_in,
    token_out_symbol=token_out,
    amounts_in=amounts
)

# Visualize results
fig = plot_combined_analysis(df, token_in, token_out)
fig.show()
```

## Features

- **Automatic Pool Discovery**: Finds Uniswap V3 pools dynamically via the Factory contract
- **Price Impact Analysis**: Calculate real-world slippage for various trade sizes
- **Gas Cost Estimation**: Uses Chainlink oracle for accurate ETH price, converts gas to USD
- **Chainlink Price Oracles**: ETH/USD price from Chainlink oracle (manipulation-resistant, no DEX impact)
- **Interactive Plots**: Plotly visualizations for analysis
- **52 Tokens Across 3 Liquidity Tiers**: Pre-configured high, medium, and low liquidity tokens
- **Smart Trade Sizing**: Helper functions automatically recommend appropriate trade amounts based on pool liquidity

## File Structure

The project uses a simple flat module structure (not a package):

```
uv3tc/
├── tradecost.py          # Core analysis functions (analyze_trade_costs, quote_with_price_impact)
├── config.py             # Token and pool configurations, liquidity helper functions
├── pool_finder.py        # Automatic pool discovery via Uniswap V3 Factory
├── plots.py              # Plotly visualization functions
├── utils.py              # ABI fetching utilities for Etherscan
├── __init__.py           # Module exports (for reference, but use direct imports)
├── UniswapTradeCosts.ipynb   # Interactive Jupyter notebook
├── examples/             # Example scripts
├── test/                 # Test scripts
└── README.md
```


## Working with Low-Liquidity Pools

### The "SPL" Error

When trading low-liquidity tokens (like FLOKI, SHIB, etc.), you may encounter:

```
Error: execution reverted: SPL
```

**SPL = "Sqrt Price Limit"** - This means the trade would move the price too far given the available liquidity.

### Solution: Use Smaller Trade Amounts

For low-liquidity pools, use **much smaller** trade amounts:

```python
# ❌ DON'T - Too large for low-liquidity pools
amounts_in = [1000, 10000, 100000, 1000000]

# ✅ DO - Appropriate for low-liquidity pools
amounts_in = [0.1, 1, 10, 100]
```

### Example: Comparing High vs Low Liquidity

```python
# High-liquidity pool (large amounts work)
df_btc = analyze_trade_costs(w3, "USDC", "WBTC", [1000, 10000, 100000])

# Low-liquidity pool (need small amounts)
df_floki = analyze_trade_costs(w3, "FLOKI", "WETH", [0.1, 1, 10, 100])
```

Run the comparison script:
```bash
python examples/compare_liquidity.py
```

## Pool Discovery

Pools are automatically discovered if not in the config:

```python
from pool_finder import find_all_pools_for_pair, discover_pool

# Find all pools for a pair
pools = find_all_pools_for_pair(w3, token_a_address, token_b_address)
# Returns: {500: pool_address, 3000: pool_address, ...}

# Auto-discover best pool
pool = discover_pool(w3, "FLOKI", "WETH")
# Returns: {"address": "0x...", "fee": 3000}
```

## Available Tokens

The toolkit includes 52 tokens across three liquidity tiers:

### High-Liquidity Tokens (20 tokens)
Deep liquidity pools that can handle large trades ($1M+) with minimal slippage (<0.5%)
- Stablecoins: USDC, USDT, DAI
- Major: WETH, WBTC, LINK, UNI, AAVE
- DeFi: CRV, MKR, SNX, COMP, LDO, MATIC, FXS, FRAX
- Other: WSTETH, RETH, OP, ARB

**Recommended trade sizes**: $1K - $10M

### Medium-Liquidity Tokens (12 tokens)
Moderate liquidity pools showing significant price impact (1-5%) on larger trades
- DeFi: RPL, BAL, ENJ, YFI, BAT, ZRX, INJ, CVX, ANKR, LRC, BNT, ALCX

**Recommended trade sizes**: $100 - $1M

### Low-Liquidity Tokens (20 tokens)
Shallow liquidity pools with high price impact (5-50%) even on small trades
- Meme: FLOKI, SHIB, PEPE, BONE
- NFT: BLUR, LOOKS
- Gaming: SAND, MANA, AXS, GMT, GALA, IMX
- AI: RNDR, FET, AGIX, OCEAN, WLD
- DeFi: DYDX, SUSHI, 1INCH
- Web3: ENS, MASK

**Recommended trade sizes**: $0.10 - $1K

## Liquidity Helper Functions

Use these functions to work with liquidity tiers:

```python
from config import (
    get_tokens_by_liquidity,
    get_token_liquidity_tier,
    get_recommended_amounts,
    print_liquidity_summary
)

# Get all tokens in a specific tier
high_liq_tokens = get_tokens_by_liquidity("high")
medium_liq_tokens = get_tokens_by_liquidity("medium")
low_liq_tokens = get_tokens_by_liquidity("low")

# Check a token's liquidity tier
tier = get_token_liquidity_tier("RPL")  # Returns "medium"

# Get recommended trade sizes for a token
amounts = get_recommended_amounts("WBTC")  # Returns [1000, 10000, 100000, 1000000, 10000000]
amounts = get_recommended_amounts("RPL")   # Returns [100, 1000, 10000, 100000, 1000000]
amounts = get_recommended_amounts("FLOKI") # Returns [0.1, 1, 10, 100, 1000]

# Print a summary of all tokens by tier
print_liquidity_summary()
```

## Price Data: Chainlink Oracle

This toolkit uses **Chainlink price oracles** for ETH/USD pricing to ensure accurate, manipulation-resistant price data.


### Implementation

```python
from tradecost import get_eth_price_usd, CHAINLINK_ETH_USD

# Get current ETH price from Chainlink oracle
eth_price = get_eth_price_usd(w3)
print(f"ETH Price: ${eth_price:,.2f}")

# Oracle contract address (for reference)
print(f"Using Chainlink ETH/USD feed: {CHAINLINK_ETH_USD}")
# 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
```

The Chainlink ETH/USD price feed on Ethereum mainnet is located at `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` and provides prices with 8 decimals of precision.

## Understanding Price Impact

Price impact varies dramatically by liquidity:

| Pool Type | Trade Size | Price Impact |
|-----------|------------|--------------|
| High-liquidity (USDC/WBTC) | $100,000 | ~0.3% |
| Medium-liquidity (RPL/WETH) | $100,000 | ~2-5% |
| Low-liquidity (FLOKI/WETH) | $100 | ~5-10% |

**Key Insights**:
- High-liquidity pools can handle multi-million dollar trades with <1% impact
- Medium-liquidity pools show 1-5% impact on $100K+ trades
- Low-liquidity pools can have 10-100x higher price impact even on small trades

## API Reference

### Main Functions

- `analyze_trade_costs(w3, token_in, token_out, amounts_in, fee=None)` - Complete analysis
- `quote_with_price_impact(w3, ...)` - Single quote with price impact
- `get_eth_price_usd(w3)` - Current ETH price from Chainlink oracle (manipulation-resistant)

### Pool Discovery

- `find_pool_address(w3, token_a, token_b, fee)` - Find specific pool
- `find_all_pools_for_pair(w3, token_a, token_b)` - Find all fee tiers
- `discover_pool(w3, token_in_symbol, token_out_symbol, fee=None)` - Auto-discover best pool

### Liquidity Helpers

- `get_tokens_by_liquidity(tier)` - Get list of tokens in "high", "medium", or "low" tier
- `get_token_liquidity_tier(symbol)` - Get liquidity tier for a token
- `get_recommended_amounts(token_symbol)` - Get appropriate trade sizes for a token
- `print_liquidity_summary()` - Print formatted summary of all tokens by tier

### Plotting

- `plot_amount_in_vs_out(df, token_in, token_out)` - Actual vs ideal output
- `plot_price_impact(df, token_in, token_out)` - Price impact vs size
- `plot_cost_of_impact(df, token_in, token_out)` - Tokens lost due to slippage
- `plot_combined_analysis(df, token_in, token_out)` - 2x2 dashboard
- `print_summary_stats(df, ...)` - Text summary

### ABI Utilities

- `get_abi_from_etherscan(address, api_key, network)` - Fetch full ABI from Etherscan
- `extract_function_abi(full_abi, function_name)` - Extract single function from ABI
- `extract_functions_abi(full_abi, function_names)` - Extract multiple functions
- `get_minimal_abi(address, function_names, api_key, network)` - Get minimal ABI
- `print_function_signature(abi_entry)` - Pretty-print function signature
- `demonstrate_abi_fetching(api_key)` - Show how ABIs were obtained
- `UNISWAP_V3_ADDRESSES` - Dict of known Uniswap V3 contract addresses

## Working with ABIs

> 📖 **For a comprehensive guide**, see [HOW_ABIS_WORK.md](HOW_ABIS_WORK.md) or read about [Ethereum ABIs on the official docs](https://docs.soliditylang.org/en/latest/abi-spec.html)

### How ABIs Were Obtained

The ABIs used in this toolkit (QuoterV2, Pool, Factory) were obtained from Etherscan. You can fetch ABIs programmatically or view them on Etherscan's website.

#### Fetch ABIs Programmatically

```python
from utils import get_abi_from_etherscan, get_minimal_abi, UNISWAP_V3_ADDRESSES

# Get your free API key at https://etherscan.io/apis
ETHERSCAN_API_KEY = "YOUR_KEY_HERE"

# Fetch full QuoterV2 ABI
quoter_address = UNISWAP_V3_ADDRESSES["QuoterV2"]
full_abi = get_abi_from_etherscan(quoter_address, ETHERSCAN_API_KEY)
print(f"QuoterV2 has {len(full_abi)} ABI entries")

# Get minimal ABI with only the functions you need
minimal_abi = get_minimal_abi(
    quoter_address,
    ["quoteExactInputSingle"],
    ETHERSCAN_API_KEY
)
print(f"Minimal ABI has {len(minimal_abi)} entries")
```

#### View on Etherscan (No API Key Required)

You can also view ABIs directly on Etherscan:

- **QuoterV2**: https://etherscan.io/address/0x61fFE014bA17989E743c5F6cB21bF9697530B21e#code
- **Factory**: https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984#code
- **Any Pool**: Find pool address using `find_pool_address()`, then view on Etherscan

#### Run the ABI Demonstration

```bash
# Set your Etherscan API key (optional but recommended)
export ETHERSCAN_API_KEY="your_key_here"

# Run the demonstration
python utils.py
```

This will show:
- How to fetch ABIs from Etherscan
- How to extract specific functions
- How minimal ABIs were created for this toolkit
- Alternative methods for obtaining ABIs

### Why Minimal ABIs?

The toolkit uses "minimal ABIs" - containing only the functions needed rather than the full contract ABI. Benefits:

- **Smaller code size**: Only include what you need
- **Faster**: Less data to parse and process
- **Clearer**: Easy to see exactly which functions are used
- **No dependencies**: Don't need npm packages or external files

Example:
```python
# Full QuoterV2 ABI: ~50 entries (functions, events, errors)
# Minimal ABI in tradecost.py: 1 entry (just quoteExactInputSingle)
```

## Troubleshooting

### "SPL" Error (Sqrt Price Limit)
- **Cause**: Trade too large for pool liquidity
- **Fix**: Use smaller trade amounts (divide by 10-1000x)

### "No pool found"
- **Cause**: Token pair doesn't have a Uniswap V3 pool
- **Fix**: Check token addresses, try different fee tiers

### "Could not transact with/call contract function"
- **Cause**: Invalid pool address or network issue
- **Fix**: Check RPC connection, verify pool exists on Etherscan

## Examples

### Example Scripts

**Compare High vs Low Liquidity:**
```bash
python examples/compare_liquidity.py
```
Demonstrates the dramatic difference between high-liquidity (USDC/WBTC) and low-liquidity (FLOKI/WETH) pools.

**Compare All Liquidity Tiers:**
```bash
python examples/compare_all_liquidity_tiers.py
```
Comprehensive comparison of high, medium, and low liquidity pools showing how trade costs scale with pool depth.

**Pool Discovery:**
```bash
python test/test_pool_discovery.py
```
Shows how pools are automatically discovered via the Uniswap V3 Factory contract.

**Fetch ABIs from Etherscan:**
```bash
export ETHERSCAN_API_KEY="your_key_here"
python examples/fetch_abis.py
```
Demonstrates how to programmatically fetch ABIs from Etherscan and create minimal ABIs. Shows how the ABIs in tradecost.py were originally obtained.

### Jupyter Notebooks

See `UniswapTradeCosts.ipynb` for an interactive analysis with visualizations.
