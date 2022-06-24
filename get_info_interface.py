import crawl_data_api.crawl_from_eth_token as eth_crawl
import crawl_data_api.crawl_from_bsc_token as bsc_crawl
import get_info_api.metadata_eth as _eth
import get_info_api.metadata_bsc as _bsc
import get_info_api.moralis as moralis
import coin_marketcap.metadata_api as cmc_api
import database.cmc_db as cmc_db
import database.total_token as total_token
import sys
sys.path.append('./')

ETH_PLATFORM_ID = 1027
BSC_PLATFORM_ID = 1839

METADATA_FIELDS = ['id', 'name', 'symbol', 'slug', 'cmc_rank', 'is_active',
                   'first_historical_data', 'last_historical_data', 'platform', 'token_address']
PRICE_FIELDS = ['id', 'num_market_pair', 'circulating_supply', 'total_supply',
                'max_supply', 'last_updated', 'date_added', 'usd_price', 'usd_volume_24h',
                'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap',
                'fully_diluted_market_cap']
BSC_FIELDS = ['chain', 'name', 'symbol', 'usdPrice', 'bnbPrice', 'totalPrice',
              'totalSupply', 'holders', 'transactions', 'decimal']
ETH_FIELDS = ['chain', 'name', 'symbol',
              'totalSupply', 'holders', 'transactions']
MORE_INFO_FIELDS = ['total_supply', 'circulating_supply', 'liquidity',
                    'contract_owner', 'contract_abi']
MORALIS_FIELDS = ['chain', 'name', 'symbol', 'decimal',
                  'create_at', 'price', 'numberTransaction']

MODE = ['metadata', 'price', 'bsc', 'eth',
        'more_info', 'moralis', 'transaction']

# return the result by the dict/json format


def jsonify_result(result, kind: str):
    if result is None:
        return None
    result_json = {}
    if kind == 'metadata':
        for i in range(len(result)):
            result_json[METADATA_FIELDS[i]] = result[i]
    if kind == 'price':
        for i in range(len(result)):
            result_json[PRICE_FIELDS[i]] = result[i]
    if kind == 'bsc':
        for i in range(len(result)):
            result_json[BSC_FIELDS[i]] = result[i]
    if kind == 'eth':
        for i in range(len(result)):
            result_json[ETH_FIELDS[i]] = result[i]
    if kind == 'more_info':
        for i in range(len(result)):
            result_json[MORE_INFO_FIELDS[i]] = result[i]
    if kind == 'moralis':
        for i in range(len(result)):
            result_json[MORALIS_FIELDS[i]] = result[i]
    return result_json


def get_info_for_validator(token_address: str = None, name: str = None, symbol: str = None):

    result = {
        'token_address': token_address,
        'name': name,
        'symbol': symbol
    }

    # step 1: find in database-coinmarketcap
    def find_in_database(token_address: str = None, name: str = None, symbol: str = None):
        loop = cmc_db.loop
        loop.run_until_complete(cmc_db.get_metadata(
            loop, token_address=token_address, name=name, symbol=symbol))
        database_result = jsonify_result(cmc_db.get_result, 'metadata')
        cmc_db.clear_result()
        return database_result

    # step pre-2,3: check if the token is valid bsc/eth token
    def is_valid_eth_or_bsc_token(token_address: str):
        if token_address is None:
            return False
        if token_address.startswith('0x') is False:
            return False
        if len(token_address) != 42:
            return False
        for i in range(len(token_address)):
            if token_address[i] not in '1234567890abcdefABCDEF':
                return False
        return True

    # step 2: find in bsc scan
    def get_bsc_info(token_address: str):
        bsc_data = jsonify_result(
            bsc_crawl.get_info_from_BSC(token_address), 'bsc')
        more_info = jsonify_result(
            _bsc.get_more_info_from_bsc(token_address), 'more_info')
        return bsc_data.update(more_info)

    # step 3: find in eth scan
    def get_eth_info(token_address: str):
        eth_data = jsonify_result(
            eth_crawl.get_info_from_ETH(token_address), 'eth')
        more_info = jsonify_result(
            _eth.get_more_info_from_eth(token_address), 'more_info')
        return eth_data.update(more_info)

    # step 4: find in moralis
    def get_moralis_info(token_address: str):
        moralis_data = jsonify_result(
            moralis.get_moralis_metadata_erc20(token_address), 'moralis')
        return moralis_data

    result['cmc_metadata'] = jsonify_result(
        find_in_database(token_address, name, symbol), 'metadata')
    result['name'] = result['cmc_metadata']['name']
    result['symbol'] = result['cmc_metadata']['symbol']
    result['token_address'] = result['cmc_metadata']['token_address']

    if result['token_address'] is not None and is_valid_eth_or_bsc_token(result['token_address']):
        result['moralis'] = jsonify_result(
            get_moralis_info(token_address), 'moralis')
        chain = result['moralis']['chain']
        if chain == 'bsc':
            result['bsc'] = get_bsc_info(token_address)
        elif chain == 'eth':
            result['eth'] = get_eth_info(token_address)

    return result


def get_list_of_transaction(token_address: str = None, name: str = None, chain: str = None):
    if token_address is not None:
        return moralis.get_transactions_erc20(token_address, chain)
    else:
        return None


print(get_info_for_validator('0x0d8775f648430679a709e98d2b0cb6250d2887ef'))
