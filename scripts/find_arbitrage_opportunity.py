from web3 import Web3, HTTPProvider
import json

# Connect to Ethereum node
web3 = Web3(HTTPProvider("http://localhost:8545"))

# Address of Uniswap
# Define ABI for Pair contract to fetch reserves
pair_abi = '[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Define pair addresses of token pairs on Uniswap and Sushiswap
uniswap_pair_address = web3.toChecksumAddress('0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11') # Replace with actual address
sushiswap_pair_address = web3.toChecksumAddress('0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852') # Replace with actual address

# Instantiate pair contracts
uniswap_pair = web3.eth.contract(address=uniswap_pair_address, abi=pair_abi)
sushiswap_pair = web3.eth.contract(address=sushiswap_pair_address, abi=pair_abi)

def get_price(pair_contract, token0, token1):
    # Get reserves of token pair
    reserves = pair_contract.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]

    # Calculate price: price = reserve1 / reserve0
    price = reserve1 / reserve0 if token0 < token1 else reserve0 / reserve1
    return price

def find_arbitrage_opportunity():
    # Define tokens
    token0 = web3.toChecksumAddress('0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48') # USDC
    token1 = web3.toChecksumAddress('0xdac17f958d2ee523a2206206994597c13d831ec7') # USDT

    # Get current price at Uniswap and Sushiswap
    uniswap_price = get_price(uniswap_pair, token0, token1)
    sushiswap_price = get_price(sushiswap_pair, token0, token1)

    # Check for arbitrage opportunity
    if uniswap_price > sushiswap_price:
        return ('uniswap', 'sushiswap', uniswap_price - sushiswap_price)
    elif sushiswap_price > uniswap_price:
        return ('sushiswap', 'uniswap', sushiswap_price - uniswap_price)
    else:
        return None

# Find arbitrage opportunity
opportunity = find_arbitrage_opportunity()
if opportunity is not None:
    print(f'Arbitrage opportunity: buy on {opportunity[0]}, sell on {opportunity[1]} for profit of {opportunity[2]}')
else:
    print('No arbitrage opportunity found')
