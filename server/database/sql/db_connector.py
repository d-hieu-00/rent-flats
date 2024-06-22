import sys, pathlib
import json
import copy
import sqlite3
import psycopg2

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
from utils.utils import logger
from utils.utils import safe_execute

class DBConnector:
    SQLite3    = "SQLite3"
    PostgreSQL = "PostgreSQL"

    @property
    def class_name(self): return self.__class__.__name__

    @property
    def db_type(self): return self.__db_type

    @property
    def db_config(self):
        if self.__db_config is None: return "{}"
        return json.dumps(self.__db_config)

    def __init__(self, db, config):
        self.__db_config = config
        self.__db_type = db
        logger.debug(f"[{self.class_name}] Init db '{self.db_type}'", config)
        self.__verify_config()
        self.__test_connection()

    def __del__(self):
        logger.debug(f"[{self.class_name}] Deinit db '{self.db_type}', config: '{self.db_config}'")

    def __new_connection(self):
        if self.__db_type == self.SQLite3:
            return sqlite3.connect(self.__db_config["path"], check_same_thread=False)
        if self.__db_type == self.PostgreSQL:
            return psycopg2.connect(**self.__db_config)
        raise Exception(f"[{self.class_name}] Not support db '{self.db_type}'")

    def __verify_config(self):
        ok = type(self.__db_config) == type({})
        if self.__db_type == self.SQLite3:
            ok = ok and self.__db_config.keys().__contains__("path")
        elif self.__db_type == self.PostgreSQL:
            ok = ok \
             and self.__db_config.keys().__contains__("host") \
             and self.__db_config.keys().__contains__("port") \
             and self.__db_config.keys().__contains__("user") \
             and self.__db_config.keys().__contains__("password") \
             and self.__db_config.keys().__contains__("database")
        else:
            raise Exception(f"[{self.class_name}] Not support db type '{self.db_type}'")
        if ok == False:
            raise Exception(f"[{self.class_name}] Invalid config for db '{self.db_type}'")

    def __create_database(self):
        if self.__db_type == self.PostgreSQL:
            logger.debug(f"[{self.class_name}] Creating database")
            _config   = copy.deepcopy(self.__db_config); del _config['database']
            db_name   = self.__db_config["database"]
            db_conn   = psycopg2.connect(**_config)
            db_cursor = db_conn.cursor()
            db_cursor.execute(f"""
            CREATE EXTENSION IF NOT EXISTS dblink;
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '{db_name}') THEN
                    PERFORM dblink_exec('{self.connection_str()}', 'CREATE DATABASE {db_name}');
                END IF;
            END $$;
            """)
            db_conn.commit()
            db_conn.close()
        return True

    def __test_connection(self):
        isOk = False; times = 1
        while isOk == False and times < 5:
            logger.debug("Try connect to database", times); times += 1
            if self.__db_type == self.SQLite3:
                isOk = safe_execute(False, self.__new_connection)
            elif self.__db_type == self.PostgreSQL:
                isOk = safe_execute(False, self.__create_database)
        if isOk == False:
            raise Exception("Test connection failed")
        logger.debug("Test connection successfully")

    def connection_str(self):
        if self.__db_type == self.PostgreSQL:
            __host = self.__db_config['host']
            __port = self.__db_config['port']
            __user = self.__db_config['user']
            __pass = self.__db_config['password']
            return f"postgresql://{__user}:{__pass}@{__host}:{__port}/"
        return ""

    def new_connection(self):
        return self.__new_connection()
