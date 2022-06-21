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

def get_latest_result(token_address: str = None, name: str = None, symbol: str = None):
    data = None
    if token_address != None:
        data = total_token.find_by_address(token_address)
    if name != None:
        data = total_token.find_by_name(name)
    if symbol != None:
        data = total_token.find_by_symbol(symbol)
    return data

def get_info_for_validator(token_address: str):
    # step 1: find in database
    loop = cmc_db.loop
    loop.run_until_complete(cmc_db.get_metadata(
        loop, token_address=token_address))
    result = cmc_db.result

    def get_bsc_info(token_address: str):
    # get bsc data
        bsc_data = bsc_crawl.get_info_from_BSC(token_address)
        more_info = _bsc.get_more_info_from_bsc(token_address)
        return bsc_data, more_info
    def get_eth_info(token_address: str):
    # get eth data
        eth_data = eth_crawl.get_info_from_ETH(token_address)
        more_info = _eth.get_more_info_from_eth(token_address)
        return eth_data, more_info
    def get_moralis_info(token_address: str):
    # get moralis data
        moralis_data = moralis.get_info_from_moralis(token_address)
        return moralis_data

    # step 1: data found, use the data in database
    if len(result) == 1:
        json_data = {
            "name": result[0][1],
            "symbol": result[0][2],
            "token_address": token_address,
            "cmc_rank": result[0][4],
            "slug": result[0][3],
            "is_active": result[0][5],
            "first_historical_data": result[0][6],
            "last_historical_data": result[0][7],
            "platform": result[0][8],
            "id": result[0][0],
        }

         #
        # this token is in database
        # we need some code to retrive more info
        # from bsc/eth database
        #
        if json_data['platform'] == ETH_PLATFORM_ID:
            # get eth data
            eth_data, more_info = get_eth_info(token_address)
            json_data.update(eth_data)
            json_data.update(more_info)
        if json_data['platform'] == BSC_PLATFORM_ID:
            # get bsc data
            bsc_data, more_info = get_bsc_info(token_address)
            json_data.update(bsc_data)
            json_data.update(more_info)
        json_data.update(get_moralis_info(token_address))
        return json_data
    # step 2: if not found, get info from another source
    if len(result) == 0:

        # 2a. get infor from eth/bsc scan
        chain = 'bsc'
        token_info = bsc_crawl.get_info_from_BSC(token_address)
        # bsc:
        # name, symbol, usd-bnb price, totalvalue, total supply
        # holders, transactions, decimal
        if token_info == None:
            chain = 'eth'
            # eth:
            # name, symbol, total supply
            # holders, transactions
            token_info = eth_crawl.get_info_from_ETH(token_address)
            if token_info == None:
                chain = None

        # more info:
        # total supply, circulating supply, liquidity
        # owner, contract abi
        if chain == 'eth':
            more_info = _eth.get_more_info_from_eth(token_address)
        if chain == 'bsc':
            more_info = _bsc.get_more_info_from_bsc(token_address)
        if chain != None:
            token_info.update(more_info)

        # 2b. get info from moralis
        # chain, name, symbol, created_at
        # usd price, transaction, decimal
        moralis_info = moralis.get_moralis_metadata_erc20(token_address)
        if moralis_info == None and chain == None:
            return None

        token_info.update(moralis_info)

        # token_info:
        # chain, name, symbol
        # create_at
        # total_supply, circulating_supply, liquidity, owner, contract_abi
        # usd_price, holders, transactions, decimal
        return token_info

    # step 3: if not found, get info from coinmarketcap
    if len(result) == 0:
        token_info = cmc_api.get_metadata_by_address(token_address)
        if token_info == None:
            return None
        return token_info


print(get_info_for_validator('0x0d8775f648430679a709e98d2b0cb6250d2887ef'))
