from fastapi import FastAPI

app = FastAPI()

# validate input from user
def validate_input(token_address: str):
    if len(token_address) != 42:
        return False
    if token_address[0] != '0':
        return False
    if token_address[1] != 'x':
        return False
    for i in range(2, len(token_address)):
        if token_address[i] not in '0123456789abcdefABCDEF':
            return False
    return True

@app.get("/{token_address}")
async def is_scam(token_address: str):
    
    if validate_input(token_address) is False:
        return {
            "status_code": 400,
            "message": "Invalid token_address value",
            "result": []
        }

    # 
    # this code for database find its data
    # and return if it have
    #
    
    

    return {
        "status_code": 200,
        "message": "OK",
        "result": {
            "token_address": token_address, 
            "scam": False, 
            "explain": "Token is not scam",
            "point": 100
        }}

