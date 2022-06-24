import sys
import requests
import datetime

sys.path.append('./get_info_api')
import moralis
sys.path.append('./')
import crawl_data_api.crawl_from_bsc_token as crawl

BSC_KEY = 'EV41IX58376FTWQM37PW9T3ADJV18HSPZN'

# get total supply of token by ContractAddress
def get_total_supply(contract_address: str):
    url = 'https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=' +\
         contract_address + '&apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    try:
        rs = int(data)
    except ValueError:
        rs = 0
    return rs

# get total circulating supply 
# -> the numbers of cryptocurrencies coins publicly available in the market
def get_total_circulating_supply(contract_address: str):
    url = 'https://api.bscscan.com/api?module=stats&\
        action=tokenCsupply&contractaddress=' +\
        contract_address + '&apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    return int(data)


# get token account balance from token address & account address
def get_account_balance(token_address: str, account_address: str):
    url = 'https://api.bscscan.com/api?module=account&action=tokenbalance' +\
        '&contractaddress=' + token_address + '&address=' + account_address +\
        '&tag=latest&apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    return int(data)


# get a list of normal transaction by address
# contain timestamp, [blocknumber, hash, nonce, blockHash, transactionindex]
# from - to - value - gas - gas price - isError
# contractAddress - cumulativeGasUsed

def get_list_transactions(address: str):
    url = 'https://api.bscscan.com/api?module=account&action=txlist&address=' +\
    address + '&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&' +\
    'apikey=' + BSC_KEY
    
    data = requests.get(url).json()['result']
    result = []
    for transaction in data:
        time = datetime.utcfromtimestamp(int(transaction['timeStamp'])) \
                    .strftime('%Y-%m-%d %H:%M:%S')
        sender = transaction['from']
        receiver = transaction['to']
        value = int(transaction['value']) / 10**18
        result.append((time, sender, receiver, value))
    
    return result

# get infor about the creator of the token
def get_creator_of_token(address: str):
    transaction = get_list_transactions(address)[-1]
    (time, creator, _, _) = transaction
    explain = "Token Address: " + address + "\nCreator: " + creator + "\n" +\
        "Time create: "+ time 
    
    return (explain, creator)

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

# get contract abi if the contract is verified
def get_contract_abi(token_address: str):
    url = 'https://api.bscscan.com/api?module=contract&action=getabi' \
     + '&address=%s&apikey=%s' % (token_address, BSC_KEY)
    response = requests.get(url=url).json()
    if response['status'] == '0':
        return None
    return response['result']

# call this function for more infomation about the BSC token
def get_more_info_from_bsc(token_address: str):
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

    return (total_supply, circulating_supply, liquidity, token_owner, contract_abi)
    {
        "total_supply": total_supply,
        "circulating_supply": circulating_supply,
        "liquidity": liquidity,
        "owner": token_owner,
        "contract_abi": contract_abi
    } 

