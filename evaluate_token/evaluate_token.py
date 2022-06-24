import sys
sys.path.append('./')
import database.total_token as total_token
import evaluate_token.group_1 as validator
import get_info_interface as get_info

def get_latest_result(token_address: str = None, name: str = None, symbol: str = None):
    data = None
    if token_address != None:
        data = total_token.find_by_address(token_address)
    if name != None:
        data = total_token.find_by_name(name)
    if symbol != None:
        data = total_token.find_by_symbol(symbol)
    return data

def evaluate_token(token_address: str = None, name: str = None, symbol: str = None):
    data = get_latest_result(token_address, name, symbol)
    if data == None:
        data = get_info.get_info_for_validator(token_address)
        
        result = validator.evaluate(data)

        if result['status'] != 'OK':
            return {
                'token_name': data['name'],
                'token_address': data['token_address'],
                'symbol': data['symbol'],
                'category': 'no value token',
                'possibility': 100
            }
        
        

        return_value = {
            'token_name': token_name,
            'token_address': token_address,
            'symbol': token_symbol,
            'category': category,
            'possibility': possibility,
        }
    else:
        token_name = data['name']
        token_address = data['token_address']
        token_symbol = data['symbol']
        category = data['latest_result'][0]
        if category == '0':
            category = 'no value token'
            possibility = 100
        elif category == '1':
            category = 'a simple scam token'
            possibility = 100
        elif category == '2':
            category = 'a complicated scam token'
            possibility = int(data['latest_result'][1:])
        else:
            category = 'an OK token'
            possibility = int(data['latest_result'][1:])
        return_value = {
            'token_name': token_name,
            'token_address': token_address,
            'symbol': token_symbol,
            'category': category,
            'possibility': possibility,
        }
        return return_value