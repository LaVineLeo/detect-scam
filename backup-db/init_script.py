import sys
sys.path.append('./')
import database.cmc_db as cmc_db


# init coin marketcap db
loop = cmc_db.loop

loop.run_until_complete(cmc_db.cmc_init_database(loop))
loop.run_until_complete(cmc_db.fill_to_metadata(loop))