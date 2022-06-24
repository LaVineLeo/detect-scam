import json
from fastapi import FastAPI

app = FastAPI()

# validate input from user
def validate_input(token_address: str):
    for i in range(len(token_address)):
        if token_address[i].isalnum() is False:
            return False
    return True

# input: /address/0x1234567890123456789012345678901234567890
@app.get("/address/{token_address}")
async def is_scam(token_address: str):
    
    if validate_input(token_address) is False:
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