import sys, pathlib
import threading

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
from utils.utils import logger
from utils.utils import safe_execute
from database.sql.db_connector import DBConnector

class DBPgSql:
    @property
    def class_name(self):       return self.__class__.__name__

    @property
    def database_schema(self):  return self._database_schema

    def __init__(self, db_config, db_schema):
        self._database_schema = db_schema

        # Setup connection
        self.__connector = DBConnector(DBConnector.PostgreSQL, db_config)
        self.__rconn = self.__connector.new_connection()
        self.__wconn = self.__connector.new_connection()
        self.__wlock = threading.Lock()
        self.__init_schema()

        logger.debug(f"[{self.class_name}] Inited {self.database_schema} database")

    def __del__(self):
        if self.__wconn: self.__wconn.close()
        if self.__rconn: self.__rconn.close()

    def __init_schema(self):
        logger.debug(f"[{self.class_name}] Create schema")
        if safe_execute(None, self._write, f"CREATE SCHEMA IF NOT EXISTS {self.database_schema}") is None:
            raise Exception(f"Failed to create schema {self.database_schema}")

    def _write(self, query: str, *args):
        logger.debug(f"[{self.class_name}] Excute write query", query, *args)
        with self.__wlock:
            cursor = self.__wconn.cursor()
            cursor.execute(query, [*args])
            self.__wconn.commit()
            return cursor

    def _read(self, query: str, *args):
        logger.debug(f"[{self.class_name}] Excute read query", query, *args)
        cursor = self.__rconn.cursor()
        cursor.execute(query, [*args])
        return cursor
