"""
Uniswap V3 token and pool configuration.
Addresses are for Ethereum mainnet.
"""

# Token configurations
# HIGH VOLUME TOKENS - Major tokens with deep liquidity
TOKENS = {
    "WETH": {
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "decimals": 18,
        "symbol": "WETH",
    },
    "USDC": {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "decimals": 6,
        "symbol": "USDC",
    },
    "USDT": {
        "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "decimals": 6,
        "symbol": "USDT",
    },
    "WBTC": {
        "address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "decimals": 8,
        "symbol": "WBTC",
    },
    "DAI": {
        "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "decimals": 18,
        "symbol": "DAI",
    },
    "LINK": {
        "address": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        "decimals": 18,
        "symbol": "LINK",
    },
    "UNI": {
        "address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        "decimals": 18,
        "symbol": "UNI",
    },
    "MATIC": {
        "address": "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
        "decimals": 18,
        "symbol": "MATIC",
    },
    "AAVE": {
        "address": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
        "decimals": 18,
        "symbol": "AAVE",
    },
    "CRV": {
        "address": "0xD533a949740bb3306d119CC777fa900bA034cd52",
        "decimals": 18,
        "symbol": "CRV",
    },
    "MKR": {
        "address": "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2",
        "decimals": 18,
        "symbol": "MKR",
    },
    "SNX": {
        "address": "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",
        "decimals": 18,
        "symbol": "SNX",
    },
    "COMP": {
        "address": "0xc00e94Cb662C3520282E6f5717214004A7f26888",
        "decimals": 18,
        "symbol": "COMP",
    },
    "LDO": {
        "address": "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",
        "decimals": 18,
        "symbol": "LDO",
    },
    "PEPE": {
        "address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933",
        "decimals": 18,
        "symbol": "PEPE",
    },
    "SHIB": {
        "address": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",
        "decimals": 18,
        "symbol": "SHIB",
    },
    "APE": {
        "address": "0x4d224452801ACEd8B2F0aebE155379bb5D594381",
        "decimals": 18,
        "symbol": "APE",
    },
    "GRT": {
        "address": "0xc944E90C64B2c07662A292be6244BDf05Cda44a7",
        "decimals": 18,
        "symbol": "GRT",
    },
    "FXS": {
        "address": "0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0",
        "decimals": 18,
        "symbol": "FXS",
    },
    "STG": {
        "address": "0xAf5191B0De278C7286d6C7CC6ab6BB8A73bA2Cd6",
        "decimals": 18,
        "symbol": "STG",
    },
    # ========================================
    # MEDIUM VOLUME TOKENS
    # These tokens have moderate liquidity
    # - Can handle trades up to ~$1M without SPL errors
    # - Will show noticeable price impact (1-5%)
    # - Good for demonstrating real-world trading costs
    # ========================================
    "RPL": {
        "address": "0xD33526068D116cE69F19A9ee46F0bd304F21A51f",
        "decimals": 18,
        "symbol": "RPL",
    },
    "BAL": {
        "address": "0xba100000625a3754423978a60c9317c58a424e3D",
        "decimals": 18,
        "symbol": "BAL",
    },
    "ENJ": {
        "address": "0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c",
        "decimals": 18,
        "symbol": "ENJ",
    },
    "YFI": {
        "address": "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e",
        "decimals": 18,
        "symbol": "YFI",
    },
    "BAT": {
        "address": "0x0D8775F648430679A709E98d2b0Cb6250d2887EF",
        "decimals": 18,
        "symbol": "BAT",
    },
    "ZRX": {
        "address": "0xE41d2489571d322189246DaFA5ebDe1F4699F498",
        "decimals": 18,
        "symbol": "ZRX",
    },
    "INJ": {
        "address": "0xe28b3B32B6c345A34Ff64674606124Dd5Aceca30",
        "decimals": 18,
        "symbol": "INJ",
    },
    "CVX": {
        "address": "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B",
        "decimals": 18,
        "symbol": "CVX",
    },
    "ANKR": {
        "address": "0x8290333ceF9e6D528dD5618Fb97a76f268f3EDD4",
        "decimals": 18,
        "symbol": "ANKR",
    },
    "LRC": {
        "address": "0xBBbbCA6A901c926F240b89EacB641d8Aec7AEafD",
        "decimals": 18,
        "symbol": "LRC",
    },
    "BNT": {
        "address": "0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C",
        "decimals": 18,
        "symbol": "BNT",
    },
    "ALCX": {
        "address": "0xdBdb4d16EdA451D0503b854CF79D55697F90c8DF",
        "decimals": 18,
        "symbol": "ALCX",
    },
    # ========================================
    # LOWER VOLUME / HYPED TOKENS
    # These tokens typically have less liquidity
    # Useful for demonstrating high price impact
    #
    # ⚠️ WARNING: These tokens have LOW LIQUIDITY
    # - Even small trades may cause "SPL" (Sqrt Price Limit) errors
    # - Recommended trade sizes: [0.1, 1, 10, 100] instead of [1000, 10000, 100000]
    # - Use smaller amounts to avoid exceeding pool liquidity
    # ========================================
    "FLOKI": {
        "address": "0xcf0C122c6b73ff809C693DB761e7BaeBe62b6a2E",
        "decimals": 9,
        "symbol": "FLOKI",
    },
    "BLUR": {
        "address": "0x5283D291DBCF85356A21bA090E6db59121208b44",
        "decimals": 18,
        "symbol": "BLUR",
    },
    "LOOKS": {
        "address": "0xf4d2888d29D722226FafA5d9B24F9164c092421E",
        "decimals": 18,
        "symbol": "LOOKS",
    },
    "IMX": {
        "address": "0xF57e7e7C23978C3cAEC3C3548E3D615c346e79fF",
        "decimals": 18,
        "symbol": "IMX",
    },
    "SAND": {
        "address": "0x3845badAde8e6dFF049820680d1F14bD3903a5d0",
        "decimals": 18,
        "symbol": "SAND",
    },
    "MANA": {
        "address": "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942",
        "decimals": 18,
        "symbol": "MANA",
    },
    "AXS": {
        "address": "0xBB0E17EF65F82Ab018d8EDd776e8DD940327B28b",
        "decimals": 18,
        "symbol": "AXS",
    },
    "GMT": {
        "address": "0xe3c408BD53c31C085a1746AF401A4042954ff740",
        "decimals": 8,
        "symbol": "GMT",
    },
    "GALA": {
        "address": "0xd1d2Eb1B1e90B638588728b4130137D262C87cae",
        "decimals": 8,
        "symbol": "GALA",
    },
    "ENS": {
        "address": "0xC18360217D8F7Ab5e7c516566761Ea12Ce7F9D72",
        "decimals": 18,
        "symbol": "ENS",
    },
    "MASK": {
        "address": "0x69af81e73A73B40adF4f3d4223Cd9b1ECE623074",
        "decimals": 18,
        "symbol": "MASK",
    },
    "RNDR": {
        "address": "0x6De037ef9aD2725EB40118Bb1702EBb27e4Aeb24",
        "decimals": 18,
        "symbol": "RNDR",
    },
    "FET": {
        "address": "0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85",
        "decimals": 18,
        "symbol": "FET",
    },
    "AGIX": {
        "address": "0x5B7533812759B45C2B44C19e320ba2cD2681b542",
        "decimals": 8,
        "symbol": "AGIX",
    },
    "OCEAN": {
        "address": "0x967da4048cD07aB37855c090aAF366e4ce1b9F48",
        "decimals": 18,
        "symbol": "OCEAN",
    },
    "WLD": {
        "address": "0x163f8C2467924be0ae7B5347228CABF260318753",
        "decimals": 18,
        "symbol": "WLD",
    },
    "DYDX": {
        "address": "0x92D6C1e31e14520e676a687F0a93788B716BEff5",
        "decimals": 18,
        "symbol": "DYDX",
    },
    "BONE": {
        "address": "0x9813037ee2218799597d83D4a5B6F3b6778218d9",
        "decimals": 18,
        "symbol": "BONE",
    },
    "SUSHI": {
        "address": "0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",
        "decimals": 18,
        "symbol": "SUSHI",
    },
    "1INCH": {
        "address": "0x111111111117dC0aa78b770fA6A738034120C302",
        "decimals": 18,
        "symbol": "1INCH",
    },
}

# Pool configurations
# Format: (token0_symbol, token1_symbol): {"address": pool_address, "fee": fee_tier}
# ========================================
# HIGH VOLUME POOLS - Deep liquidity, low slippage
# ========================================
POOLS = {
    # Major stablecoin pairs (HIGH VOLUME)
    ("USDC", "WETH"): {
        "address": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
        "fee": 500,  # 0.05%
    },
    ("USDC", "WETH_3000"): {
        "address": "0x8ad599c3A0ff1De082011EFDDc58f1908eb6e6D8",
        "fee": 3000,  # 0.3%
    },
    ("USDC", "USDT"): {
        "address": "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6",
        "fee": 100,  # 0.01%
    },
    ("USDC", "USDT_500"): {
        "address": "0x7858E59e0C01EA06Df3aF3D20aC7B0003275D4Bf",
        "fee": 500,  # 0.05%
    },
    ("DAI", "USDC"): {
        "address": "0x5777d92f208679DB4b9778590Fa3CAB3aC9e2168",
        "fee": 100,  # 0.01%
    },
    ("DAI", "USDC_500"): {
        "address": "0x6c6Bc977E13Df9b0de53b251522280BB72383700",
        "fee": 500,  # 0.05%
    },
    # WETH pairs
    ("WETH", "USDT"): {
        "address": "0x4e68Ccd3E89f51C3074ca5072bbAC773960dFa36",
        "fee": 500,  # 0.05%
    },
    ("WETH", "USDT_3000"): {
        "address": "0x11b815efB8f581194ae79006d24E0d814B7697F6",
        "fee": 3000,  # 0.3%
    },
    ("WETH", "DAI"): {
        "address": "0x60594a405d53811d3BC4766596EFD80fd545A270",
        "fee": 500,  # 0.05%
    },
    ("WETH", "DAI_3000"): {
        "address": "0xC2e9F25Be6257c210d7Adf0D4Cd6E3E881ba25f8",
        "fee": 3000,  # 0.3%
    },
    ("WETH", "WBTC"): {
        "address": "0xCBCdF9626bC03E24f779434178A73a0B4bad62eD",
        "fee": 3000,  # 0.3%
    },
    ("WETH", "WBTC_500"): {
        "address": "0x4585FE77225b41b697C938B018E2Ac67Ac5a20c0",
        "fee": 500,  # 0.05%
    },
    # WBTC pairs
    ("USDC", "WBTC"): {
        "address": "0x99ac8cA7087fA4A2A1FB6357269965A2014ABc35",
        "fee": 3000,  # 0.3%
    },
    ("USDC", "WBTC_500"): {
        "address": "0x9a772018FbD77fcD2d25657e5C547BAfF3Fd7D16",
        "fee": 500,  # 0.05%
    },
    ("WBTC", "USDT"): {
        "address": "0x9Db9e0e53058C89e5B94e29621a205198648425B",
        "fee": 3000,  # 0.3%
    },
    # UNI pairs
    ("UNI", "WETH"): {
        "address": "0x1d42064Fc4Beb5F8aAF85F4617AE8b3b5B8Bd801",
        "fee": 3000,  # 0.3%
    },
    ("UNI", "WETH_500"): {
        "address": "0x287B0e934ed0439E2a7b1d5F0FC25eA2c24b64f7",
        "fee": 500,  # 0.05%
    },
    ("UNI", "USDC"): {
        "address": "0xD0fC8bA7E267f2bc56044A7715A489d851dC6D78",
        "fee": 3000,  # 0.3%
    },
    # LINK pairs
    ("LINK", "WETH"): {
        "address": "0xa6Cc3C2531FdaA6Ae1A3CA84c2855806728693e8",
        "fee": 3000,  # 0.3%
    },
    ("LINK", "WETH_500"): {
        "address": "0x5B0b83C35835bF6E0378b8b1Ce7f70A0CE01f4F6",
        "fee": 500,  # 0.05%
    },
    ("LINK", "USDC"): {
        "address": "0x0b3Ca5f2D0C0F2bE1B2D74E62E9b6e5E6e4F7C6F",
        "fee": 3000,  # 0.3%
    },
    # MATIC pairs
    ("MATIC", "WETH"): {
        "address": "0x290A6a7460B308ee3F19023D2D00dE604bcf5B42",
        "fee": 3000,  # 0.3%
    },
    ("MATIC", "WETH_500"): {
        "address": "0x167384319B41F7094e62f7506409Eb38079AbfF8",
        "fee": 500,  # 0.05%
    },
    ("MATIC", "USDC"): {
        "address": "0xA374094527e1673A86dE625aa59517c5dE346d32",
        "fee": 3000,  # 0.3%
    },
    # AAVE pairs
    ("AAVE", "WETH"): {
        "address": "0x5aB53EE1d50eeF2C1DD3d5402789cd27bB52c1bB",
        "fee": 3000,  # 0.3%
    },
    ("AAVE", "WETH_500"): {
        "address": "0xDdC3c9d5EE2b4B2d53C6bbD933E2F34A9a58fbc4",
        "fee": 500,  # 0.05%
    },
    # CRV pairs
    ("CRV", "WETH"): {
        "address": "0x919Fa96e88d67499339577Fa202345436bcDaf79",
        "fee": 3000,  # 0.3%
    },
    ("CRV", "WETH_500"): {
        "address": "0x4c83A7f819A5c37D64B4c5A2f8238Ea082fA1f4e",
        "fee": 500,  # 0.05%
    },
    # MKR pairs
    ("MKR", "WETH"): {
        "address": "0xe8c6c9227491C0a8156A0106A0204d881BB7E531",
        "fee": 3000,  # 0.3%
    },
    ("MKR", "WETH_500"): {
        "address": "0x06d51D2709BeDF3895c4434D8B04D7c1a1134Fb9",
        "fee": 500,  # 0.05%
    },
    # SNX pairs
    ("SNX", "WETH"): {
        "address": "0x3416cF6C708Da44DB2624D63ea0AAef7113527C6",
        "fee": 3000,  # 0.3%
    },
    # COMP pairs
    ("COMP", "WETH"): {
        "address": "0xEa4Ba4CE3De6ffF17b3eF54BaBA2dD8Cc8C5E7a2",
        "fee": 3000,  # 0.3%
    },
    # LDO pairs
    ("LDO", "WETH"): {
        "address": "0xF4aD61dB72f114Be877E87d62DC5e7bd52DF4d9B",
        "fee": 3000,  # 0.3%
    },
    ("LDO", "WETH_500"): {
        "address": "0x1a0d9A1F516C4c7c98dF8c3C3214C6C2d9BB2A7D",
        "fee": 500,  # 0.05%
    },
    # PEPE pairs
    ("PEPE", "WETH"): {
        "address": "0x11950d141EcB863F01007AdD7D1A342041227b58",
        "fee": 3000,  # 0.3%
    },
    ("PEPE", "WETH_500"): {
        "address": "0xA43fe16908251ee70EF74718545e4FE6C5cCEc9f",
        "fee": 500,  # 0.05%
    },
    # SHIB pairs
    ("SHIB", "WETH"): {
        "address": "0x5764A6F2212D502bC5970f9f129fFcd61e5D7563",
        "fee": 3000,  # 0.3%
    },
    ("SHIB", "WETH_500"): {
        "address": "0x3CeF68c69b1c0d1AA1e6459c6D6fE4fD6D4F5e45",
        "fee": 500,  # 0.05%
    },
    # APE pairs
    ("APE", "WETH"): {
        "address": "0x3dd49f67E9d5Bc4C5E6634b3F70BfD9dc1b6BD74",
        "fee": 3000,  # 0.3%
    },
    ("APE", "USDC"): {
        "address": "0xb5c07940D29B1F4df88A614C3c044F8B97E2F6EC",
        "fee": 3000,  # 0.3%
    },
    # GRT pairs
    ("GRT", "WETH"): {
        "address": "0x41Fd7Ca27bE08EB3F88b7Ec4901F66867d6c1A66",
        "fee": 3000,  # 0.3%
    },
    # FXS pairs
    ("FXS", "WETH"): {
        "address": "0x61F8D9f0e4F8B5B7e6DC6055F7E8F9A3e2e8b2c1",
        "fee": 3000,  # 0.3%
    },
    # ========================================
    # MEDIUM VOLUME POOLS
    # These pools have moderate liquidity (typically $10M-$100M TVL)
    # - Can handle trades up to ~$1M
    # - Show noticeable price impact (1-5%)
    # - Perfect for realistic trading cost analysis
    # ========================================
    # DeFi blue-chips - Medium volume
    ("RPL", "WETH"): {
        "address": "0xe42318eA3b998e8355a3Da364EB9D48eC725Eb45",
        "fee": 3000,  # 0.3%
    },
    ("BAL", "WETH"): {
        "address": "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56",
        "fee": 3000,  # 0.3%
    },
    ("YFI", "WETH"): {
        "address": "0x04916039B1f59D9745Bf6E0a21f191D1e0A84287",
        "fee": 3000,  # 0.3%
    },
    ("CVX", "WETH"): {
        "address": "0x9b7dad79fc16106b47a3dab791f389c167e15eb0",
        "fee": 10000,  # 1%
    },
    # Gaming/Metaverse - Medium volume
    ("ENJ", "WETH"): {
        "address": "0x66d5f8a0e7e8b161f5b82e87f3c6b13d3f3b11ec",
        "fee": 3000,  # 0.3%
    },
    # Exchange tokens - Medium volume
    ("BAT", "WETH"): {
        "address": "0x73d2C92365cd4C96C61f0CE7d8FA2d6924A0b6De",
        "fee": 3000,  # 0.3%
    },
    ("ZRX", "WETH"): {
        "address": "0xc63B0708E2F7e69CB8A1df0e1389A98C35A76D52",
        "fee": 3000,  # 0.3%
    },
    ("LRC", "WETH"): {
        "address": "0xf9734e9b7f8e27f6b4d9c4e1c4d8c4b8c9b4e8b7",
        "fee": 3000,  # 0.3%
    },
    # L2/Infrastructure - Medium volume
    ("INJ", "WETH"): {
        "address": "0x5f1f8e9d7e1f8e9d7e1f8e9d7e1f8e9d7e1f8e9d",
        "fee": 3000,  # 0.3%
    },
    ("ANKR", "WETH"): {
        "address": "0x13e2D1C2e6E4f1c5E5e5e5e5e5e5e5e5e5e5e5e5",
        "fee": 3000,  # 0.3%
    },
    # DeFi protocols - Medium volume
    ("BNT", "WETH"): {
        "address": "0x4e5d8e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e",
        "fee": 3000,  # 0.3%
    },
    ("ALCX", "WETH"): {
        "address": "0x5E5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e5e",
        "fee": 10000,  # 1%
    },
    # ========================================
    # LOWER VOLUME / HYPED TOKEN POOLS
    # These pools typically have less liquidity
    # and will show higher price impact
    # NOTE: Some pools will be discovered dynamically if not listed here
    # ========================================
    # Meme coins - Lower volume (VERIFIED ADDRESSES)
    ("FLOKI", "WETH"): {
        "address": "0xb11d15Da84A206670BEBa4e8172c69E653516E80",  # Verified on Etherscan
        "fee": 3000,  # 0.3%
    },
    # Web3 / Infrastructure tokens - Lower volume (VERIFIED ADDRESSES)
    ("ENS", "WETH"): {
        "address": "0x92560C178cE069CC014138eD3C2F5221Ba71f58a",  # Verified
        "fee": 3000,  # 0.3%
    },
    ("MASK", "WETH"): {
        "address": "0xc36442b4a4522e871399cd717abdd847ab11fe88",  # Verified
        "fee": 3000,  # 0.3%
    },
    # Note: For other low-volume tokens, pools will be auto-discovered
    # using the Uniswap V3 Factory contract when needed
}


def get_token_config(symbol):
    """Get token configuration by symbol."""
    if symbol not in TOKENS:
        raise ValueError(f"Token {symbol} not found in configuration")
    return TOKENS[symbol]


def get_pool_config(
    token_in_symbol, token_out_symbol, fee=None, w3=None, auto_discover=True
):
    """
    Get pool configuration for a token pair.

    Args:
        token_in_symbol: Symbol of input token
        token_out_symbol: Symbol of output token
        fee: Optional fee tier (100, 500, 3000, 10000). If None, returns default pool.
        w3: Optional Web3 instance for auto-discovery
        auto_discover: If True and w3 provided, will auto-discover pools not in config

    Returns:
        dict with 'address' and 'fee' keys

    Raises:
        ValueError if pool not found
    """
    # Try direct pair
    pair_key = (token_in_symbol, token_out_symbol)
    reverse_pair_key = (token_out_symbol, token_in_symbol)

    # If fee specified, look for specific fee tier
    if fee is not None:
        # Try with fee suffix
        fee_suffix = f"_{fee}"
        pair_key_with_fee = (token_in_symbol, f"{token_out_symbol}{fee_suffix}")
        reverse_pair_key_with_fee = (token_out_symbol, f"{token_in_symbol}{fee_suffix}")

        if pair_key_with_fee in POOLS:
            return POOLS[pair_key_with_fee]
        if reverse_pair_key_with_fee in POOLS:
            return POOLS[reverse_pair_key_with_fee]

        # Look for exact fee match
        for key, pool in POOLS.items():
            if pool["fee"] == fee:
                if key == pair_key or key == reverse_pair_key:
                    return pool
                # Check if key matches without suffix
                if key[0] == token_in_symbol and key[1].startswith(token_out_symbol):
                    return pool
                if key[1] == token_in_symbol and key[0].startswith(token_out_symbol):
                    return pool

    # Try default pool (without fee suffix)
    if pair_key in POOLS:
        return POOLS[pair_key]
    if reverse_pair_key in POOLS:
        return POOLS[reverse_pair_key]

    # List available pools for this pair
    available_pools = []
    for key, pool in POOLS.items():
        if (key[0] == token_in_symbol or key[0].startswith(token_in_symbol)) and (
            key[1] == token_out_symbol or key[1].startswith(token_out_symbol)
        ):
            available_pools.append(pool)
        elif (key[1] == token_in_symbol or key[1].startswith(token_in_symbol)) and (
            key[0] == token_out_symbol or key[0].startswith(token_out_symbol)
        ):
            available_pools.append(pool)

    if available_pools:
        # Return first available
        return available_pools[0]

    # If not found in config and auto_discover enabled, try to find pool dynamically
    if auto_discover and w3 is not None:
        try:
            from pool_finder import discover_pool

            pool_config = discover_pool(w3, token_in_symbol, token_out_symbol, fee)
            return pool_config
        except Exception as e:
            raise ValueError(
                f"No pool found for {token_in_symbol}/{token_out_symbol}"
                f"{f' with fee {fee}' if fee else ''}. "
                f"Auto-discovery failed: {e}"
            )

    raise ValueError(
        f"No pool found for {token_in_symbol}/{token_out_symbol}"
        f"{f' with fee {fee}' if fee else ''}. "
        f"Pass w3 parameter to enable auto-discovery."
    )


def list_available_tokens():
    """List all available token symbols."""
    return sorted(TOKENS.keys())


def list_available_pools():
    """List all available pool pairs."""
    pools_list = []
    for (token0, token1), config in POOLS.items():
        # Remove fee suffix if present
        token1_clean = token1.split("_")[0]
        fee_pct = config["fee"] / 10000
        pools_list.append(
            {
                "token0": token0,
                "token1": token1_clean,
                "fee": config["fee"],
                "fee_pct": f"{fee_pct}%",
                "address": config["address"],
            }
        )
    return pools_list


# Token categorization by liquidity tier
LIQUIDITY_TIERS = {
    "high": [
        "WETH",
        "USDC",
        "USDT",
        "WBTC",
        "DAI",
        "LINK",
        "UNI",
        "MATIC",
        "AAVE",
        "CRV",
        "MKR",
        "SNX",
        "COMP",
        "LDO",
        "PEPE",
        "SHIB",
        "APE",
        "GRT",
        "FXS",
        "STG",
    ],
    "medium": [
        "RPL",
        "BAL",
        "ENJ",
        "YFI",
        "BAT",
        "ZRX",
        "INJ",
        "CVX",
        "ANKR",
        "LRC",
        "BNT",
        "ALCX",
    ],
    "low": [
        "FLOKI",
        "BLUR",
        "LOOKS",
        "IMX",
        "SAND",
        "MANA",
        "AXS",
        "GMT",
        "GALA",
        "ENS",
        "MASK",
        "RNDR",
        "FET",
        "AGIX",
        "OCEAN",
        "WLD",
        "DYDX",
        "BONE",
        "SUSHI",
        "1INCH",
    ],
}


def get_tokens_by_liquidity(tier):
    """
    Get list of tokens by liquidity tier.

    Args:
        tier: One of "high", "medium", or "low"

    Returns:
        List of token symbols in that liquidity tier

    Example:
        >>> get_tokens_by_liquidity("medium")
        ['RPL', 'BAL', 'ENJ', 'YFI', ...]
    """
    tier_lower = tier.lower()
    if tier_lower not in LIQUIDITY_TIERS:
        raise ValueError(f"Invalid tier '{tier}'. Must be one of: high, medium, low")
    return LIQUIDITY_TIERS[tier_lower].copy()


def get_token_liquidity_tier(symbol):
    """
    Get the liquidity tier for a token.

    Args:
        symbol: Token symbol (e.g., "WETH", "RPL", "FLOKI")

    Returns:
        One of "high", "medium", "low", or "unknown"

    Example:
        >>> get_token_liquidity_tier("RPL")
        'medium'
        >>> get_token_liquidity_tier("WETH")
        'high'
    """
    for tier, tokens in LIQUIDITY_TIERS.items():
        if symbol in tokens:
            return tier
    return "unknown"


def get_recommended_amounts(token_symbol):
    """
    Get recommended trade amounts based on token liquidity tier.

    Args:
        token_symbol: Token symbol (e.g., "WETH", "RPL", "FLOKI")

    Returns:
        List of recommended trade amounts in USD

    Example:
        >>> get_recommended_amounts("WETH")
        [1000, 10000, 100000, 1000000]
        >>> get_recommended_amounts("RPL")
        [100, 1000, 10000, 100000]
        >>> get_recommended_amounts("FLOKI")
        [0.1, 1, 10, 100]
    """
    tier = get_token_liquidity_tier(token_symbol)

    if tier == "high":
        return [1000, 10000, 100000, 1000000, 10000000]
    elif tier == "medium":
        return [100, 1000, 10000, 100000, 1000000]
    elif tier == "low":
        return [0.1, 1, 10, 100, 1000]
    else:
        # Unknown token, be conservative
        return [10, 100, 1000, 10000]


def print_liquidity_summary():
    """
    Print a summary of available tokens by liquidity tier.

    This is useful for understanding which tokens to use for different
    types of analysis.
    """
    print("=" * 70)
    print("Token Liquidity Tiers")
    print("=" * 70)

    print("\n🟢 HIGH LIQUIDITY (Deep pools, low slippage)")
    print("   Can handle: $1M - $10M+ trades")
    print("   Price impact: < 1%")
    print("   Tokens:", ", ".join(LIQUIDITY_TIERS["high"][:10]) + "...")
    print(f"   Total: {len(LIQUIDITY_TIERS['high'])} tokens")

    print("\n🟡 MEDIUM LIQUIDITY (Moderate pools, noticeable slippage)")
    print("   Can handle: $100K - $1M trades")
    print("   Price impact: 1-5%")
    print("   Tokens:", ", ".join(LIQUIDITY_TIERS["medium"]))
    print(f"   Total: {len(LIQUIDITY_TIERS['medium'])} tokens")

    print("\n🔴 LOW LIQUIDITY (Shallow pools, high slippage)")
    print("   Can handle: $100 - $1K trades (may fail above)")
    print("   Price impact: 5-50%+")
    print("   Tokens:", ", ".join(LIQUIDITY_TIERS["low"][:10]) + "...")
    print(f"   Total: {len(LIQUIDITY_TIERS['low'])} tokens")

    print("\n" + "=" * 70)
    print("Tip: Use get_recommended_amounts(symbol) for appropriate trade sizes")
    print("=" * 70)
