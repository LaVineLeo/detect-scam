import requests
import json

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '3f5a70b1-52d2-4f67-8a1e-22d935f25c05',
}

api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/'


def get_info_from_cmc():
    url = api_url + 'listings/latest'

    parameters = {
        'start': '1',
        'limit': '5',
        'convert': 'USD'
    }

    response = requests.get(url, headers=headers, params=parameters).json()
    if response['status']['error_code'] != 0:
        return None

    return response['data']

# get metadata of the token -> fill to the database
# json: id, rank, name, symbol, slug, cmc_rank, is_active,
#       first_historical_data, last_historical_data, platform, token_address


def get_metadata_from_cmc():

    def get_metadata_from_cmc(start: int, limit: int):
        url = api_url + 'map'
        params = {
            'listing_status': 'active',
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

    result_list = []
    error_code = 0
    start = 1
    while error_code == 0:
        print('start: ', start)
        response = get_metadata_from_cmc(start=start, limit=5000)
        if response != None:
            result_list.extend(response)
            start += 5000
        else:
            error_code = 1
    return result_list


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
