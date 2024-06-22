import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import config
from database.db_main import DBMain
from database.db_setup import DBSetup

class DBHanlder:
    dbMain = DBMain(config.DATABASE_CONF)
    dbSetup = DBSetup(config.DATABASE_CONF)
