from web3 import Web3

# Connect to Ethereum node via Infura
web3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/API'))

# Define ABI for Pair contract to fetch reserves
pair_abi = '[{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Define pair addresses of token pairs on Uniswap and Sushiswap
uniswap_pair_address = web3.toChecksumAddress('0x75e48c9ae6183c862bc9ea0e3a9a8e11f76808b4') # Replace with actual address
sushiswap_pair_address = web3.toChecksumAddress('0xc76225124f3caabc0c048378bf7d728aeede344d') # Replace with actual address

# Instantiate pair contracts
uniswap_pair = web3.eth.contract(address=uniswap_pair_address, abi=pair_abi)
sushiswap_pair = web3.eth.contract(address=sushiswap_pair_address, abi=pair_abi)

def get_price(pair_contract):
    # Get reserves of token pair
    reserves = pair_contract.functions.getReserves().call()
    reserve0 = reserves[0]
    reserve1 = reserves[1]

    # Calculate price: price = reserve1 / reserve0
    price = reserve1 / reserve0
    return price

def find_arbitrage_opportunity():
    # Get current price at Uniswap and Sushiswap
    uniswap_price = get_price(uniswap_pair)
    sushiswap_price = get_price(sushiswap_pair)

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
