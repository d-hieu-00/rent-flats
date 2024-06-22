import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.utils import logger
from utils.utils import safe_execute
from database.sql.db_pgsql import DBPgSql

class DBSetup(DBPgSql):
    def __init__(self, db_config):
        super().__init__(db_config, 'setup')

        # Init database
        self.__init_database()
        logger.info(f"[{self.class_name}] Started setup database")

    def __init_database(self):
        logger.debug(f"[{self.class_name}] Create tables")
        queries = [
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.config (
                key  TEXT NOT NULL PRIMARY KEY,
                data TEXT DEFAULT '{{}}'
            )""",
            f"INSERT INTO {self.database_schema}.config(key, data) VALUES('base','{{}}') ON CONFLICT DO NOTHING",
        ]

        for query in queries:
            safe_execute(None, self._write, query)

    ### BASE CONFIG ####
    def save_conf(self, data):
        query = f"UPDATE {self.database_schema}.config SET data = %s WHERE key = %s"
        return safe_execute(None, self._write, query, data, 'base')

    def query_conf(self):
        query   = f"SELECT data FROM {self.database_schema}.config where key = %s"
        _result = safe_execute(None, self._read, query, 'base')
        if _result is None:
            return None

        _rows = _result.fetchall()
        if len(_rows) == 0:
            return '{}'
        return _rows[0][0]
    ### END OF [BASE CONFIG] ####
