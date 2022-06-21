import json
import moralis
import requests
import crawl_data_api.crawl_from_eth_token as crawl

ETHER_KEY = '92KN8VPM8UFJW2CP6PR6G4S9DJBDBM1TA5'

# get total number of tokens
def get_total_supply(token_address: str):
    url = 'https://api.etherscan.io/api?module=stats&action=tokensupply' \
        + '&contractaddress=%s&apikey=%s' % (token_address,ETHER_KEY)
    
    response = requests.get(url).json()
    if response['status'] == '0':
        return 0
    else:
        return int(response['result'])


def get_contract_abi(token_address: str):
    url = 'https://api.etherscan.io/api?module=contract&action=getabi' \
     +'&address=%s&apikey=%s' %(token_address, ETHER_KEY)

    response = requests.get(url).json()
    if response['status'] == '0':
        return None
    else:
        return response['result']

# get the liquidity of the token by USD or BNB
def get_liquidity_of_token(token: str):
    url = 'https://api.pancakeswap.info/api/v2/tokens/' + token
    response = requests.get(url).json()
    try:
        data = response['data']
        price_USD = data['price']
    except:
        return 0
    return float(price_USD)

def get_total_circulating_supply(token_address: str):
    url = 'https://api.etherscan.io/api?module=stats&action=tokenCsupply' \
        + '&contractaddress=%s&apikey=%s' % (token_address,ETHER_KEY)
    
    response = requests.get(url).json()
    if response['status'] == '0':
        return 0
    else:
        return int(response['result'])

def get_more_info_from_eth(token_address: str):
    total_supply = get_total_supply(token_address)
    circulating_supply = get_total_circulating_supply(token_address)
    liquidity = get_liquidity_of_token(token_address)

    contract_abi = get_contract_abi(token_address)
    if contract_abi is None:
        token_owner = None
    else:
        token_owner = moralis.call_contract_function(
                token_address, 'owner', contract_abi, 1)
        if token_owner is None:
            token_owner = moralis.call_contract_function(
                token_address, 'getOwner', contract_abi, 1)
        if token_owner is None:
            token_owner = crawl.get_owner_of_token(token_address)

    return {
        "total_supply": total_supply,
        "circulating_supply": circulating_supply,
        "liquidity": liquidity,
        "owner": token_owner,
        "contract_abi": contract_abi
    } 