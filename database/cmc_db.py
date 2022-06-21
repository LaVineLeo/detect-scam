import asyncio
import aiomysql

import sys
sys.path.append('./')

import coin_marketcap.metadata_api as cmc_api

loop = asyncio.get_event_loop()
result = []

#########################################################################
# get the async connection to the database
# @param loop: the event loop
#
async def get_connection_to_database(loop):

    # Connect to the database
    connection = await aiomysql.connect(
        host='localhost',
        user='root',
        password='wewemaylalong2A!',
        loop=loop,
    )
    async with connection.cursor() as cursor:
        await cursor.execute("CREATE DATABASE IF NOT EXISTS cmc_token")
        await cursor.execute("USE cmc_token")
        await connection.commit()
    return connection

#
# get the async connection POOL to the database
#
async def get_pool_connection(loop):
    pool = await aiomysql.create_pool(
        host='localhost',
        user='root',
        password='wewemaylalong2A!',
        loop=loop,
        db='cmc_token',
    )

    return pool

#########################################################################

# init database
async def cmc_init_database(loop, name=None):
    # Connect to the database
    con = await get_connection_to_database(loop)
    if name == None:
        name = 'cmc_metadata'
    # delete the table if it exists
    # create a new ones
    async with con.cursor() as cursor:
        await cursor.execute("DROP TABLE IF EXISTS cmc_metadata")
        await cursor.execute('''
            CREATE TABLE %s (
                id INT PRIMARY KEY, 
                name VARCHAR(255), 
                symbol VARCHAR(255), 
                slug VARCHAR(255), 
                cmc_rank INT, 
                is_active INT, 
                first_historical_data VARCHAR(255),
                last_historical_data VARCHAR(255),
                platform INT,
                token_address VARCHAR(255)
                )
            ''' %(name,))
        await con.commit()

    con.close()


# fill data from the API to the database
async def fill_to_metadata(loop):
    pool = await get_pool_connection(loop)
    # Get the data from the API
    data = cmc_api.get_metadata_from_cmc()

    async with pool.acquire() as con:
        print('\n\n', len(data), '\n')
        for token in data:
            cursor = await con.cursor()
            # Get the data from the API
            id = token['id']
            name = token['name']
            symbol = token['symbol']
            slug = token['slug']    
            cmc_rank = token['rank']
            is_active = token['is_active']
            first_historical_data = token['first_historical_data']
            last_historical_data = token['last_historical_data']
            if token['platform'] is None:
                platform = -1
                token_address = None
            else:
                platform = token['platform']['id']
                token_address = token['platform']['token_address']
            
            # Insert the data into the database
            await cursor.execute('''
                INSERT INTO cmc_metadata VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                (id, name, symbol, slug, cmc_rank, is_active, 
                first_historical_data, last_historical_data, platform, token_address,))
            await con.commit()
    pool.close()
    await pool.wait_closed()


# run SELECT query on the database
# return something based on the params 
async def get_metadata(loop, id=None, token_address=None):
    global result
    con = await get_connection_to_database(loop)
    async with con.cursor() as cursor:
        if id is not None:
            await cursor.execute('''
                SELECT * FROM cmc_metadata WHERE id = %s''', (id,))
        elif token_address is not None: 
            await cursor.execute('''
                SELECT * FROM cmc_metadata WHERE token_address = %s''', (token_address,))
        else:
            await cursor.execute('''
                SELECT * FROM cmc_metadata''')
        result = await cursor.fetchall()
        await con.commit()
    con.close()

# update the database with the new data  
async def update_metadata(loop, token_metadata):
    con = get_connection_to_database(loop)
    async with con.cursor() as cursor:
        await cursor.execute('''
            UPDATE cmc_metadata SET name = %s, symbol = %s, slug = %s, cmc_rank = %s, is_active = %s, first_historical_data = %s, last_historical_data = %s, platform = %s, token_address = %s WHERE id = %s''',
            (token_metadata['name'], token_metadata['symbol'], token_metadata['slug'], token_metadata['cmc_rank'], token_metadata['is_active'], token_metadata['first_historical_data'], token_metadata['last_historical_data'], token_metadata['platform'], token_metadata['token_address'], token_metadata['id']))
        await con.commit()
    con.close()


    
        