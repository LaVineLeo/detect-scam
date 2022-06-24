
def evaluate(data: dict):
    """
    data = {
        'token_address': token_address,
        'name': name,
        'symbol': symbol,
        'cmc_metadata': {
            'id', 'name', 'symbol', 'slug', 'cmc_rank', 'is_active',
            'first_historical_data', 'last_historical_data', 'platform', 'token_address'
        },
        'moralis': {
            'chain', 'name', 'symbol', 'decimal',
            'create_at', 'price', 'numberTransaction'
        },
        'bsc'/'eth': {
            
            ----------
            'total_supply', 'circulating_supply', 'liquidity',
                    'contract_owner', 'contract_abi'
        }
    }
    """
    if data['token_address'] is None or data['name'] is None or data['symbol'] is None:
        return {
            'status': 'NOT OK',
            'developer_message': 'token_address, name, symbol is required'
        }
    if data.get('bsc', None) is None and data.get('eth', None) is None:
        return {
            'status': 'NOT OK',
            'developer_message': 'bsc or eth is required'
        }
    
    if data.get('bsc', None) is not None:
        result = validator_for_bsc(data)
        return result

    if data.get('eth', None) is not None:
        result = validator_for_eth(data)
        return result

    return {
        'status': 'OK',
        'developer_message': 'OK - pass the validator check'
    }


def validator_for_bsc(data):
    return {
        'status': 'OK',
        'developer_message': 'OK - pass the validator check'
    }

def validator_for_eth(data):
    return {
        'status': 'OK',
        'developer_message': 'OK - pass the validator check'
    }
