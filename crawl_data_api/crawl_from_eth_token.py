import json
import requests
from bs4 import BeautifulSoup


cookies = {
    '_ga': 'GA1.2.229927880.1653624028',
    '__stripe_mid': '65d18ee4-509f-44f4-94e2-6e6d18c3909b286f00',
    'etherscan_userid': 'truongtnn404',
    'etherscan_pwd': '4792:Qdxb:Mnm3/nYXYI305UrNi2QRSEb+AvCt2Q+mqBrMiHY2TUg=',
    'etherscan_autologin': 'True',
    '__cuid': '2582bae2bbc1439aa5a5cce7d59bb44f',
    'amp_fef1e8': 'e28591fc-3928-47d5-80ba-92c06d3887acR...1g5o9dsfc.1g5ocor35.v.6.15',
}

headers = {
    'authority': 'etherscan.io',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.229927880.1653624028; __stripe_mid=65d18ee4-509f-44f4-94e2-6e6d18c3909b286f00; etherscan_userid=truongtnn404; etherscan_pwd=4792:Qdxb:Mnm3/nYXYI305UrNi2QRSEb+AvCt2Q+mqBrMiHY2TUg=; etherscan_autologin=True; __cuid=2582bae2bbc1439aa5a5cce7d59bb44f; amp_fef1e8=e28591fc-3928-47d5-80ba-92c06d3887acR...1g5o9dsfc.1g5ocor35.v.6.15',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Microsoft Edge";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
}


def get_transaction_info(token_address: str):
    params = {
        'm': 'normal',
        'contractAddress': token_address,
        'a': '',
        'sid': 'bf11ccdf0bed7fe62a1d1ed2be7563c6',
        'p': '1',
    }

    response = requests.get('https://etherscan.io/token/generic-tokentxns2', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    useful_string = soup.find('p').text.strip().removeprefix('A total of ') \
            .removesuffix('transactions found')
    return int(useful_string)

def get_info_from_ETH(token_address: str):
    url = 'https://etherscan.io/token/'
    
    response = requests.get(url + token_address, headers=headers, cookies=cookies).text
    soup = BeautifulSoup(response, 'html.parser')

    token_name = soup.find('div', attrs={'class': 'container py-3'}) \
                        .find('h1').text.strip().removeprefix('Token ')
    token_name = str(token_name)
    
    token_info = soup.find('div', attrs={'class': 'card-body'})

    total_token = token_info.find('div', attrs={'class': 'row align-items-center'}) \
            .find('div', attrs={'class': 'col-md-8 font-weight-medium'})
    total_token_num = total_token.find('span').text
    token_symbol = str(total_token.text.replace(total_token_num, '').strip())
    total_token_num = int(total_token_num.strip().replace(',', ''))
    token_holder = token_info.find('div', attrs={'id': 'ContentPlaceHolder1_tr_tokenHolders'}) \
            .find('div', attrs={'class': 'col-md-8'}).text.strip().replace('addresses', '')
    token_holder = int(token_holder)

    token_transaction = get_transaction_info(token_address)
    return ('eth', token_name, token_symbol, total_token_num, token_holder, token_transaction)
    {
        "chain": "eth",
        "name": token_name,
        "symbol": token_symbol,
        "token_supply": total_token_num,
        "holders": token_holder,
        "transactions": token_transaction,
    } 

def get_owner_of_token(token_address: str):
    url = 'https://etherscan.io/token/'
    
    response = requests.get(url + token_address, headers=headers, cookies=cookies).text
    soup = BeautifulSoup(response, 'html.parser')

    contract_owner = soup.find(id="ContentPlaceHolder1_trContract") \
        .find('div', attrs={'class': 'col-md-8'}).find('a').text

    return contract_owner