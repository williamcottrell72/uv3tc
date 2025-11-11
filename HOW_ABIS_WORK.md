# How ABIs Work and Were Obtained

This document explains how the ABIs (Application Binary Interfaces) in this toolkit were obtained and how you can fetch ABIs for other contracts.

## What is an ABI?

An **ABI (Application Binary Interface)** is a JSON description of a smart contract's interface. It tells your code:

- What functions the contract has
- What parameters each function takes
- What types those parameters are
- What the function returns
- Whether the function is read-only (`view`/`pure`) or can modify state

Without an ABI, you can't interact with a smart contract - you wouldn't know which functions exist or how to call them.

## Example: QuoterV2 ABI

Here's the minimal ABI for the `quoteExactInputSingle` function in Uniswap V3's QuoterV2:

```python
QUOTER_ABI = [{
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
                {"name": "sqrtPriceLimitX96", "type": "uint160"}
            ]
        }
    ],
    "outputs": [
        {"name": "amountOut", "type": "uint256"},
        {"name": "sqrtPriceX96After", "type": "uint160"},
        {"name": "initializedTicksCrossed", "type": "uint32"},
        {"name": "gasEstimate", "type": "uint256"}
    ]
}]
```

This tells us:
- Function name: `quoteExactInputSingle`
- Takes 1 parameter: a `tuple` (struct) with 5 fields
- Returns 4 values: `amountOut`, `sqrtPriceX96After`, `initializedTicksCrossed`, and `gasEstimate`
- Marked as `nonpayable` (doesn't accept ETH, but modifies state for the quote calculation)

## How ABIs Were Obtained for This Toolkit

### Method 1: Etherscan API (Programmatic)

The ABIs in `tradecost.py` were obtained using Etherscan's API:

```python
from uniswap import get_abi_from_etherscan, UNISWAP_V3_ADDRESSES

# Fetch full ABI from Etherscan
quoter_address = UNISWAP_V3_ADDRESSES["QuoterV2"]
full_abi = get_abi_from_etherscan(quoter_address, "YOUR_ETHERSCAN_API_KEY")

# The full QuoterV2 ABI has ~50 entries (functions, events, errors)
print(f"Full ABI has {len(full_abi)} entries")
```

**Steps:**
1. Get a free API key from [Etherscan](https://etherscan.io/apis)
2. Use the `get_abi_from_etherscan()` function
3. Extract only the functions you need
4. Create a minimal ABI with just those functions

**Benefits:**
- Automated and scriptable
- Get the exact, verified ABI
- Can be integrated into build processes

### Method 2: Etherscan Website (Manual)

You can also view ABIs directly on Etherscan's website (no API key needed):

1. Go to the contract address on Etherscan
   - QuoterV2: https://etherscan.io/address/0x61fFE014bA17989E743c5F6cB21bF9697530B21e#code
2. Click the "Contract" tab
3. Scroll to "Contract ABI"
4. Copy the JSON

**Benefits:**
- No API key needed
- Quick for one-off lookups
- See the full contract source code

### Method 3: Official Documentation

Uniswap provides ABIs in their documentation:
- https://docs.uniswap.org/contracts/v3/reference/deployments
- https://docs.uniswap.org/contracts/v3/reference/periphery/interfaces/IQuoterV2

### Method 4: npm Packages

Install Uniswap's official packages:
```bash
npm install @uniswap/v3-core @uniswap/v3-periphery
```

The ABIs are in the package artifacts:
```javascript
const QuoterV2 = require('@uniswap/v3-periphery/artifacts/contracts/lens/QuoterV2.sol/QuoterV2.json')
const abi = QuoterV2.abi
```

## Why Minimal ABIs?

This toolkit uses **minimal ABIs** - containing only the functions we need. Compare:

### Full QuoterV2 ABI (~50 entries)
```python
[
    {"name": "quoteExactInputSingle", ...},
    {"name": "quoteExactInput", ...},
    {"name": "quoteExactOutputSingle", ...},
    {"name": "quoteExactOutput", ...},
    # ... 40+ more functions, events, errors
]
```

### Minimal ABI (1 entry)
```python
[
    {"name": "quoteExactInputSingle", ...}
]
```

**Benefits:**
1. **Smaller code**: Only include what you use
2. **Faster**: Less JSON to parse
3. **Clearer**: See exactly which functions you depend on
4. **No dependencies**: Don't need npm or external files
5. **Version stable**: Less likely to break with contract upgrades

## Creating Your Own Minimal ABI

### Step 1: Get the Full ABI

```python
from uniswap import get_abi_from_etherscan

contract_address = "0xYourContractAddress"
full_abi = get_abi_from_etherscan(contract_address, "YOUR_API_KEY")
```

### Step 2: Extract Functions You Need

```python
from uniswap import extract_functions_abi

minimal_abi = extract_functions_abi(
    full_abi,
    ["functionName1", "functionName2"]
)
```

### Step 3: Save to Your Code

```python
import json

print(json.dumps(minimal_abi, indent=2))
# Copy this output to your Python file
```

## Using ABIs with web3.py

Once you have an ABI, use it to interact with the contract:

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR_KEY"))

# Create contract instance
contract = w3.eth.contract(
    address="0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    abi=QUOTER_ABI
)

# Call a function
params = (token_in, token_out, amount_in, fee, 0)
result = contract.functions.quoteExactInputSingle(params).call()
```

## Known Uniswap V3 Contract Addresses

The toolkit includes these addresses in `UNISWAP_V3_ADDRESSES`:

| Contract | Address | Etherscan |
|----------|---------|-----------|
| QuoterV2 | `0x61fFE014bA17989E743c5F6cB21bF9697530B21e` | [View](https://etherscan.io/address/0x61fFE014bA17989E743c5F6cB21bF9697530B21e#code) |
| Factory | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | [View](https://etherscan.io/address/0x1F98431c8aD98523631AE4a59f267346ea31F984#code) |
| Router | `0xE592427A0AEce92De3Edee1F18E0157C05861564` | [View](https://etherscan.io/address/0xE592427A0AEce92De3Edee1F18E0157C05861564#code) |
| NFTPositionManager | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | [View](https://etherscan.io/address/0xC36442b4a4522E871399CD717aBDD847Ab11FE88#code) |

## Tools in This Toolkit

The `uniswap.utils` module provides:

- **`get_abi_from_etherscan(address, api_key, network)`** - Fetch full ABI
- **`extract_function_abi(full_abi, function_name)`** - Extract single function
- **`extract_functions_abi(full_abi, function_names)`** - Extract multiple functions
- **`get_minimal_abi(address, function_names, api_key, network)`** - One-step minimal ABI
- **`print_function_signature(abi_entry)`** - Pretty-print function signature
- **`demonstrate_abi_fetching(api_key)`** - Interactive demo

## Running the Examples

### View the ABI demonstration:
```bash
export ETHERSCAN_API_KEY="your_key_here"
python -m uniswap.utils
```

### Fetch ABIs programmatically:
```bash
export ETHERSCAN_API_KEY="your_key_here"
python uniswap/examples/fetch_abis.py
```

## Further Reading

- [Ethereum ABI Specification](https://docs.soliditylang.org/en/latest/abi-spec.html)
- [web3.py Contract Documentation](https://web3py.readthedocs.io/en/stable/contracts.html)
- [Uniswap V3 Documentation](https://docs.uniswap.org/)
- [Etherscan API Documentation](https://docs.etherscan.io/)

## Summary

The ABIs in this toolkit were obtained by:

1. ✅ Fetching full ABIs from Etherscan using their API
2. ✅ Extracting only the functions needed (`quoteExactInputSingle`, `slot0`, etc.)
3. ✅ Formatting them as clean, minimal ABIs in the code

This approach gives you:
- ✅ Verified, correct ABIs from Etherscan
- ✅ Minimal code footprint
- ✅ No external dependencies
- ✅ Easy to maintain and understand

You can use the same process for any Ethereum contract!
