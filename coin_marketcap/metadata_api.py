import requests
import json

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '3f5a70b1-52d2-4f67-8a1e-22d935f25c05',
}

api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/'

def get_token_price_from_cmc():
    def get_info_from_cmc(start=1, limit=5000):
        url = api_url + 'listings/latest'

        parameters = {
            'start': str(start),
            'limit': str(limit),
            'convert': 'USD'
        }

        response = requests.get(url, headers=headers, params=parameters).json()
        if response['status']['error_code'] != 0:
            return None
        if len(response['data']) == 0:
            return None
        return response['data']
    result_list = []
    error_code = 0
    start = 1
    while error_code == 0:
        print('start: ', start)
        response = get_info_from_cmc(start=start, limit=5000)
        if response != None:
            result_list.extend(response)
            start += 5000
        else:
            error_code = 1
    return result_list

# get metadata of the token -> fill to the database
# json: id, rank, name, symbol, slug, cmc_rank, is_active,
#       first_historical_data, last_historical_data, platform, token_address


def get_metadata_from_cmc_(start: int, limit: int, listing_status: str = 'active'):
    url = api_url + 'map'
    params = {
        'listing_status': listing_status,
        'start': str(start),
        'limit': str(limit),
        'sort': 'id',
    }
    response = requests.get(url, headers=headers, params=params).json()
    if response['status']['error_code'] != 0:
        print(response['status']['error_code'])
        return None
    if len(response['data']) == 0:
        return None

    return response['data']

print(json.dumps(get_metadata_from_cmc_(1,1, 'inactive'), indent=4))

def get_metadata_from_cmc(listing_status: str = 'active'):
    result_list = []
    error_code = 0
    start = 1
    while error_code == 0:
        print('start: ', start)
        response = get_metadata_from_cmc_(start=start, limit=5000, listing_status=listing_status)
        if response != None:
            result_list.extend(response)
            start += 5000
        else:
            error_code = 1
    return result_list

def get_active_token_metadata():
    return get_metadata_from_cmc(listing_status='active')
def get_inactive_token_metadata():
    return get_metadata_from_cmc(listing_status='inactive')
def get_untracked_token_metadata():
    return get_metadata_from_cmc(listing_status='untracked')


def get_metadata_by_address(token_address: str):
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info'
    params = {
        'address': token_address,
    }

    response = requests.get(url, headers=headers, params=params).json()
    if response['status']['error_code'] != 0:
        return None
    return response['data']

# print(json.dumps(get_metadata_by_address('0xc40af1e4fecfa05ce6bab79dcd8b373d2e436c4e'), indent=4))
