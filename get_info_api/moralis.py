import json
import requests

headers = {
    'accept': 'application/json',
    'X-API-Key': 'ML5nx3bP0hScC1assNgG8nsYTRCkk5yAwvTOKJaYc6WHZdDpKPRMKazn5K9jLju8',
}

chains = [
            'eth', 'bsc', 'bsc testnet', '0x1', 'ropsten', 
            '0x3', 'rinkeby', '0x4', 'goerli', '0x5', '0x38',
            'kovan', '0x2a', 'polygon', '0x89', 'mumbai', '0x13881',
            '0x61', 'avalanche','0xa86a', 'avalanche testnet', 
            '0xa869', 'fantom', '0xfa', 'cronos', '0x19'
        ]

# network, name, symbol, decimal, create_at
def get_meta_data_erc20(token_address: str, chain_index = 0):
    url = 'https://deep-index.moralis.io/api/v2/erc20/metadata'
    params = {
        'chain': chains[chain_index],
        'addresses': token_address
    }

    response = requests.get(url, params=params, headers=headers).json()
    if response[0]['name'] != '':
        data = response[0]
        return (chain_index, data['name'], data['symbol'], data['decimals'], data['created_at'])
    elif chain_index == len(chains) - 1:
        return None
    else:
        return get_meta_data_erc20(token_address, chain_index+1)

# usdPrice
def get_price_erc20(token_address: str, chain_index = 0):
    url = 'https://deep-index.moralis.io/api/v2/erc20/%s/price' %token_address
    params = {
        'chain': chains[chain_index],
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()['usdPrice']
    else:
        return None

# erc20 token transactions
def get_transactions_erc20(token_address: str, chain:str=None):
    url = 'https://deep-index.moralis.io/api/v2/erc20/%s/transfers' %token_address
    def get_next_page(cursor: str):
        if cursor == None:
            params = {
                'chain': chain,
            }
        else:
            params = {
                'chain': chain,
                'cursor': cursor
            }
        response = requests.get(url, params=params, headers=headers).json()
        return response['cursor'], response['result']

    cursor, transactions = get_next_page(None)
    while cursor != None:
        cursor, transactions_next = get_next_page(cursor)
        transactions.append(transactions_next)
    
    return transactions

# numbers of erc20 token transactions
def get_numbers_of_transactions(token_address: str, chain: str=None):
    url = 'https://deep-index.moralis.io/api/v2/erc20/%s/transfers' %token_address
    params = {
        'chain': chain,
    }
    response = requests.get(url=url, params=params, headers=headers).json()
    return response['total']

# call to a contract funtion
def call_contract_function(token_address: str, function_name: str,
     contract_abi: str, chain_index = 0):
    params = {
        'chain' : chains[chain_index],
        'function_name' : function_name
    }
    json_data = {
        'abi' : contract_abi,
        'params' : {}
    }
    url = 'https://deep-index.moralis.io/api/v2/%s/function' %token_address
    response = requests.post(url=url, data=json_data, headers=headers, params=params)
    if response.json['message'] is not None:
        return None
    return response


# get the liquidity of the token by USD or BNB
def get_liquidity_of_token(token: str):
    url = 'https://api.pancakeswap.info/api/v2/tokens/' + token
    response = requests.get(url).json()
    try:
        data = response['data']
        name = data['name']
        symbol = data['symbol']
        price_USD = data['price']
        price_BNB = data['price_BNB']
    except:
        return('Not Found', 'Not Found', '0', '0.0')
    return (name, symbol, price_USD, price_BNB)

# call to this function to retrieve from Moralis tokens metadata
def get_moralis_metadata_erc20(token_address: str):
    metadata = get_meta_data_erc20(token_address)
    if metadata == None:
        return None
    
    chain_index, name, symbol, decimal, create_at = metadata
    price = get_price_erc20(token_address, chain_index)
    numbers_transaction = get_numbers_of_transactions(token_address, chains[chain_index])
    
    return (chains[chain_index], name, symbol, decimal, create_at, price, numbers_transaction)


