import database.cmc_db as cmc_db
import datetime
import sys
sys.path.append('./database')

loop = cmc_db.loop


async def init_total_token_table(loop):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)
    # delete the table if it exists
    # create a new ones
    async with con.cursor() as cursor:
        await cursor.execute("DROP TABLE IF EXISTS total_token")
        await cursor.execute('''
            CREATE TABLE total_token (
                token_address varchar(255),
                token_name varchar(255),
                chain VARCHAR(255),
                lastest_result VARCHAR(255),
                timestamp VARCHAR(255)''')
        await con.commit()
    con.close()


async def init_value(loop):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO total_token
            SELECT token_address, name, chain, NULL, NULL FROM cmc_metadata ''')
        await con.commit()
    con.close()


async def update_value(loop, lastest_result: str, token_address: str):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            UPDATE total_token
            SET lastest_result = %s, timestamp = %s
            WHERE token_address = %s''',
            (lastest_result, datetime.datetime.now(), token_address))
        await con.commit()
    con.close()

async def insert_value(loop, data: dict):
    # Connect to the database
    con = await cmc_db.get_connection_to_database(loop)

    async with con.cursor() as cursor:
        await cursor.execute('''
            INSERT INTO total_token
            VALUES (%s, %s, %s, %s, %s)''',
            (data['token_address'], data['token_name'], data['chain'], data['lastest_result'], datetime.datetime.now()))
        await con.commit()
    con.close()