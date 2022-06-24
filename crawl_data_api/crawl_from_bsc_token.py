import json
import requests
from bs4 import BeautifulSoup as BS

cookies = {
    '__stripe_mid': '0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74',
    'bscscan_cookieconsent': 'True',
    'cf_clearance': 'xfkOOpWdrtVi.JpRFTm5cMZZLN3k6xZkdP14MgdJWR0-1655279288-0-150',
    '__cuid': '49772a01dd2442d897ca9efb95c0679e',
    'amp_fef1e8': 'e28591fc-3928-47d5-80ba-92c06d3887acR...1g6035vs6.1g6035vsa.17.5.1c',
    'ASP.NET_SessionId': 's4qaeudrzrrmti0ffslsy1vz',
    '__cflb': '02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFTxtwBvf38Hek',
    '_gid': 'GA1.2.788481277.1656060614',
    '__cf_bm': 'EfhJuVGo3mBaIr5KPLFphYBzhwvOIieRBmaoMgGrR0A-1656060620-0-AYGFvHarGeFFuySOdXc1YIt1EmRKZ4iId6ub5rJI923OtH7I4NXwsF2x6+Ve33ePL5WUWVRjQCimc7lYAtsMiQqbiVzo7BtatB5gM0aKii1hIF5GK0359Ux5S3iXMidpQQ==',
    '__stripe_sid': '36ff570d-7b60-4ab3-81b5-c948a9bf498f5a1021',
    '_ga_PQY6J2Q8EP': 'GS1.1.1656060613.30.1.1656060643.0',
    '_ga': 'GA1.2.608546645.1654740748',
}

headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    # Requests sorts cookies= alphabetically
    # 'cookie': '__stripe_mid=0bca921b-3d0c-4b5c-92c4-b161a216a8fc8a1b74; bscscan_cookieconsent=True; cf_clearance=xfkOOpWdrtVi.JpRFTm5cMZZLN3k6xZkdP14MgdJWR0-1655279288-0-150; __cuid=49772a01dd2442d897ca9efb95c0679e; amp_fef1e8=e28591fc-3928-47d5-80ba-92c06d3887acR...1g6035vs6.1g6035vsa.17.5.1c; ASP.NET_SessionId=s4qaeudrzrrmti0ffslsy1vz; __cflb=02DiuJNoxEYARvg2sN5n1HeVcoKCZ1njFTxtwBvf38Hek; _gid=GA1.2.788481277.1656060614; __cf_bm=EfhJuVGo3mBaIr5KPLFphYBzhwvOIieRBmaoMgGrR0A-1656060620-0-AYGFvHarGeFFuySOdXc1YIt1EmRKZ4iId6ub5rJI923OtH7I4NXwsF2x6+Ve33ePL5WUWVRjQCimc7lYAtsMiQqbiVzo7BtatB5gM0aKii1hIF5GK0359Ux5S3iXMidpQQ==; __stripe_sid=36ff570d-7b60-4ab3-81b5-c948a9bf498f5a1021; _ga_PQY6J2Q8EP=GS1.1.1656060613.30.1.1656060643.0; _ga=GA1.2.608546645.1654740748',
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


def get_info_from_BSC(token_address: str):
    url = 'https://bscscan.com/token/'
    response = requests.get(url + token_address,
                            cookies=cookies, headers=headers).text

    soup = BS(response, 'html.parser')

    try:
        token_name = soup.find('div', attrs={'class': 'container py-3'}) \
            .find('h1').text.strip().removeprefix('Token ')
        token_name = str(token_name)

        token_info = soup.find('div', attrs={'class': 'card-body'})

        token_value = token_info.find(
            'div', attrs={'id': 'ContentPlaceHolder1_tr_valuepertoken'})
        value = token_value.find(
            'span', attrs={'data-html': 'true'}).text.strip().removeprefix('$')
        value = float(value)
        value_bnb = token_value.find(
            'span', attrs={'class': 'small text-secondary text-nowrap'}).text
        value_bnb = float(value_bnb.strip().removeprefix(
            '@').removesuffix('BNB'))
        total_value = token_value.find('button').text.strip().removeprefix('$')
        total_value = float(total_value)

        total_token = token_info.find('div', attrs={'class': 'row align-items-center'}) \
            .find('div', attrs={'class': 'col-md-8 font-weight-medium'})
        total_token_num = total_token.find(
            'span').text.strip().replace(',', '')
        total_token_num = int(total_token_num)
        token_symbol = str(total_token.find('b').text)

        token_holder = token_info.find('div', attrs={'id': 'ContentPlaceHolder1_tr_tokenHolders'}) \
            .find('div', attrs={'class': 'col-md-8'}).text.strip().replace('addresses', '')
        token_holder = int(token_holder)
    except AttributeError | ValueError:
        return None

    token_transaction = token_info.find('div', attrs={'id': 'ContentPlaceHolder1_trNoOfTxns'}).text \
        .replace('Transfers:', '').strip()
    try:
        token_transaction = int(token_transaction)
    except ValueError:
        token_transaction = 0

    decimal = soup.find('div', attrs={'id': 'ContentPlaceHolder1_trDecimals'}).text \
        .replace('Decimals:', '').strip()
    decimal = int(decimal)

    return ('bsc', token_name, token_symbol, value, value_bnb, total_value, total_token_num, token_holder, token_transaction, decimal)
    {
        "chain": "bsc",
        "name": token_name,
        "symbol": token_symbol,
        "usdPrice": value,
        "bnbPrice": value_bnb,
        "totalPrice": total_value,
        "totalSupply": total_token_num,
        "holders": token_holder,
        "transactions": token_transaction,
        "decimal": decimal
    }


def get_owner_of_token(token_address: str):
    url = 'https://bscscan.com/address/%s' % token_address
    response = requests.get(url, headers=headers, cookies=cookies).text
    soup = BS(response, "html.parser")

    contract_owner = soup.find(id="ContentPlaceHolder1_trContract") \
        .find('div', attrs={'class': 'col-md-8'}).find('a').text
    return contract_owner
