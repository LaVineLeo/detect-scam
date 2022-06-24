import sys
sys.path.append('./')
import database.cmc_db as cmc_db
import database.total_token as total_token


# init coin marketcap db
def init_cmc_db():
    loop = cmc_db.loop

    loop.run_until_complete(cmc_db.cmc_init_database(loop))
    loop.run_until_complete(total_token.init_total_token_table(loop))

    loop.run_until_complete(cmc_db.call_fill_to_metadata(loop))
    loop.run_until_complete(cmc_db.fill_to_price(loop))
    loop.run_until_complete(total_token.init_value(loop))

# update the coin marketcap db
def update_cmc_db():
    loop = cmc_db.loop

    loop.run_until_complete(cmc_db.cmc_init_database(loop, name='new_'))

    loop.run_until_complete(cmc_db.fill_to_metadata(loop, name='new_'))
    loop.run_until_complete(cmc_db.fill_to_price(loop, name='new_'))

    cmc_db.change_name(loop)

init_cmc_db()