import sys, pathlib
import json

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.utils import logger
from utils.utils import safe_execute
from database.sql.db_pgsql import DBPgSql

from database.sql_queries.db_main_create_tables import queries as create_table_queries
from database.sql_queries.db_main_user_functions import queries as user_queries
from database.sql_queries.db_main_house_functions import queries as house_queries

class DBMain(DBPgSql):
    def __init__(self, db_config):
        super().__init__(db_config, 'main')

        # Init database
        self.__init_database()
        logger.info(f"[{self.class_name}] Started main database")

    def __del__(self):
        super().__del__()

    def __create_table_queries(self):
        return create_table_queries(self.database_schema)

    def __create_function_queries(self):
        _queries = []
        _queries.extend(user_queries(self.database_schema))
        _queries.extend(house_queries(self.database_schema))
        return _queries

    def __init_database(self):
        for query in self.__create_table_queries():
            safe_execute(None, self._write, query)
        for query in self.__create_function_queries():
            safe_execute(None, self._write, query)
    
    def __call_db_fn(self, fn, *args):
        _bind_args = "%s," * len(args)
        _call_fn = f"SELECT {fn}({_bind_args[:-1]})"
        print(_call_fn, args)
        return self._read(_call_fn, *args)

    def get_user_by_session_id(self, session_id):
        cur = self.__call_db_fn(f'{self.database_schema}.get_user_by_session_id', session_id)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])

    def get_user_by_id(self, user_id):
        cur = self.__call_db_fn(f'{self.database_schema}.get_user_by_id', user_id)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])

    def new_session(self, user_id, login_ip):
        cur = self.__call_db_fn(f'{self.database_schema}.new_session', user_id, login_ip)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])

    def new_user(self, new_user):
        cur = self.__call_db_fn(f'{self.database_schema}.new_user', new_user)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])

    def update_user(self, upd_user):
        cur = self.__call_db_fn(f'{self.database_schema}.update_user', upd_user)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])

    def new_admin_user(self, new_user):
        cur = self.__call_db_fn(f'{self.database_schema}.new_admin_user', new_user)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])

    def find_user(self, data, is_admin):
        cur = self.__call_db_fn(f'{self.database_schema}.find_user', data, is_admin)
        res = cur.fetchall()
        if len(res) != 1:
            return json.dumps({"error": "Unknow Error"})
        else:
            return json.dumps(res[0][0])
