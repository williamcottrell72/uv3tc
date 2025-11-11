"""Uniswap V3 trade cost estimation tools."""

from .tradecost import (
    quote_exact_input_single,
    quote_with_price_impact,
    get_quoter_contract,
    analyze_trade_costs,
    get_eth_price_usd
)
from .config import (
    get_token_config,
    get_pool_config,
    list_available_tokens,
    list_available_pools,
    get_tokens_by_liquidity,
    get_token_liquidity_tier,
    get_recommended_amounts,
    print_liquidity_summary,
    TOKENS,
    POOLS,
    LIQUIDITY_TIERS
)
from .pool_finder import (
    find_pool_address,
    find_all_pools_for_pair,
    discover_pool
)
from .plots import (
    plot_amount_in_vs_out,
    plot_price_impact,
    plot_cost_of_impact,
    plot_combined_analysis,
    print_summary_stats
)
from .utils import (
    get_abi_from_etherscan,
    extract_function_abi,
    extract_functions_abi,
    get_minimal_abi,
    print_function_signature,
    demonstrate_abi_fetching,
    UNISWAP_V3_ADDRESSES
)

__all__ = [
    # Core functions
    'quote_exact_input_single',
    'quote_with_price_impact',
    'get_quoter_contract',
    'analyze_trade_costs',
    'get_eth_price_usd',
    # Config functions
    'get_token_config',
    'get_pool_config',
    'list_available_tokens',
    'list_available_pools',
    'get_tokens_by_liquidity',
    'get_token_liquidity_tier',
    'get_recommended_amounts',
    'print_liquidity_summary',
    'TOKENS',
    'POOLS',
    'LIQUIDITY_TIERS',
    # Pool discovery functions
    'find_pool_address',
    'find_all_pools_for_pair',
    'discover_pool',
    # Plotting functions
    'plot_amount_in_vs_out',
    'plot_price_impact',
    'plot_cost_of_impact',
    'plot_combined_analysis',
    'print_summary_stats',
    # Utility functions
    'get_abi_from_etherscan',
    'extract_function_abi',
    'extract_functions_abi',
    'get_minimal_abi',
    'print_function_signature',
    'demonstrate_abi_fetching',
    'UNISWAP_V3_ADDRESSES'
]
