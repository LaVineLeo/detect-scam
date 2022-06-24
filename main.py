import evaluate_token.evaluate_token as evaluate_token
import json
from fastapi import FastAPI
import sys
sys.path.append('./')

app = FastAPI()

# validate input from user


def validate_input(token_address: str):
    if token_address is None:
        return False
    if token_address.startswith('0x') is False:
        return False
    if len(token_address) != 42:
        return False
    for i in range(len(2, token_address)):
        if token_address[i] not in '1234567890abcdefABCDEF':
            return False
    return True

# input: /address/0x1234567890123456789012345678901234567890


@app.get("/address/{token_address}")
async def is_scam(token_address: str):

    if validate_input(token_address) is False:
        return json.dumps({
            "status": "ERR",
            "developer_message": "Only accept ETH/BSC/BNB token address",
            "result": []
        }, indent=4)

    #
    # this code will process the data
    #

    # get the result from evaluate_token
    result = evaluate_token.evaluate_token(token_address)

    #
    # this above code just process for ETH/BSC/BNB token address
    # other platform will be processed in the future
    #

    return json.dumps({
        "status": "OK",
        "result": result
    }, indent=4)


@app.get('/name/{token_name}')
async def is_scam(token_name: str):
    if validate_input(token_name) == False:
        return json.dumps({
            "status": "ERR",
            "result": []
        }, indent=4)

    #
    # this code will process the data
    #

    return json.dumps({
        "status": "OK",
        "result": {
            "token_address": "0x1234567890123456789012345678901234567890",
            "token_name": "Bitcoin",
            "symbol": "BTC",
            "category": "an OK token",
            "possibility": 20
        }}, indent=4)


@app.get('/symbol/{symbol}')
async def is_scam(symbol: str):
    if validate_input(symbol) == False:
        return json.dumps({
            "status": "ERR",
            "result": []
        }, indent=4)
    #
    # this code will process the data
    #

    return json.dumps({
        "status": "OK",
        "result": {
            "token_address": "0x1234567890123456789012345678901234567890",
            "token_name": "Bitcoin",
            "symbol": "BTC",
            "category": "an OK token",
            "possibility": 20
        }}, indent=4)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
