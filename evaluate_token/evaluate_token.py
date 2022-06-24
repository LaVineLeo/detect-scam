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

def jsonify_latest_result(result: tuple):
    if result == None: 
        return None
    if result[3] == None:
        return None
    return_value = {
        'token_name': result[0],
        'token_address': result[1],
        'symbol': result[2],
        'category': result[3][0],
        'possibility': int(result[3][1:]),
        'timestamp': result[4]
    }
    return return_value


def evaluate_token(token_address: str = None, name: str = None, symbol: str = None):
    data = get_latest_result(token_address, name, symbol)
    data = jsonify_latest_result(data)

    if data == None:
        data = get_info.get_info_for_validator(token_address)
        """
        data = {
            'token_address': token_address,
            'name': name,
            'symbol': symbol,
            'cmc_metadata': {},
            'moralis': {},
            'bsc'/'eth': {}
        }
        """
        # stage 01: check no value token
        result = validator.evaluate(data)

        if result['status'] != 'OK':
            return {
                'token_name': data['name'],
                'token_address': data['token_address'],
                'symbol': data['symbol'],
                'category': 'no value token',
                'possibility': 100
            }
        
        # stage 02: check simple scam token

        """
        there will be some code here in future
        """

        # stage 03: check complex scam token
        
        """
        there will be some code here in future
        """

    else:
        return data, 'OK'