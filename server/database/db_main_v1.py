import sys, pathlib
import threading
import faiss
import numpy as np

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import config
from utils.utils import logger
from utils.utils import safe_execute
from database.db_connector import DBConnector

class Indexer:
    Dimension = 170

    @property
    def class_name(self): return self.__class__.__name__

    def __init__(self):
        self.__index   = faiss.IndexLSH(Indexer.Dimension, 8)
        self.__map_idx = []

    def add(self, data, id):
        datas = np.array([data[Indexer.Dimension:Indexer.Dimension*2]]).astype("float32")
        self.__index.train(datas)
        self.__index.add(datas)
        self.__map_idx.append(id)

    def query(self, data, size):
        datas = np.array([data[Indexer.Dimension:Indexer.Dimension*2]]).astype("float32")
        _, indices = self.__index.search(datas, k=size)
        # print(_)
        ids = [self.__map_idx[it] for it in indices[0]]
        ids = list(dict.fromkeys(ids)) # remove duplicates
        return ids

    def remove_ids(self, ids):
        ids_to_remove = [_idx for _idx, _val in enumerate(self.__map_idx) if _val in ids]
        self.__index.remove_ids(np.array(ids_to_remove))

class DBMainV1:
    __threshold = config.THRESHOLD

    @property
    def class_name(self): return self.__class__.__name__

    def __init__(self, db_config = config.DATABASE_CONF):
        self.__database_name   = config.DATABASE_NAME
        self.__database_schema = config.DATABASE_SCHEMA
        self.__index           = Indexer()

        # Wait for connect to DB
        isOk  = False
        times = 0
        while isOk == False:
            times += 1
            logger.info("Try connect to database", times)
            isOk = safe_execute(False, self.__create_database, db_config)

        # Setup connection
        db_config["database"]  = self.__database_name
        self.__connector = DBConnector(DBConnector.PostgreSQL, db_config)
        self.__rconn = self.__connector.new_connection()
        self.__wconn = self.__connector.new_connection()
        self.__wlock = threading.Lock()
        self.__create_tables()
        logger.info(f"[{self.class_name}] Started database", db_config)

        # Build index
        ids = self.__read(f"SELECT img_idx FROM {self.__database_schema}.flowers_img").fetchall()
        logger.info(f"[{self.class_name}] Building LSH index, size={len(ids)}")
        for id in ids:
            features = self.__read(f"SELECT image_features FROM {self.__database_schema}.flowers_img WHERE img_idx = %s", id).fetchone()[0]
            self.__index.add(features, id[0])

    def __del__(self):
        if self.__wconn: self.__wconn.close()
        if self.__rconn: self.__rconn.close()

    def __write(self, query: str, *args):
        logger.debug(f"[{self.class_name}] Excute write query", query, *args)
        with self.__wlock:
            cursor = self.__wconn.cursor()
            cursor.execute(query, [*args])
            self.__wconn.commit()
            return cursor

    def __read(self, query: str, *args):
        logger.debug(f"[{self.class_name}] Excute read query", query, *args)
        cursor = self.__rconn.cursor()
        cursor.execute(query, [*args])
        return cursor

    def __create_database(self, db_config):
        logger.debug(f"[{self.class_name}] Create database")
        db_conn   = DBConnector(DBConnector.PostgreSQL, db_config).new_connection()
        db_cursor = db_conn.cursor()
        db_cursor.execute(
        f"""
        CREATE EXTENSION IF NOT EXISTS dblink;
        DO
        $do$
        BEGIN
            IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '{self.__database_name}') THEN
                PERFORM dblink_exec('', 'CREATE DATABASE {self.__database_name}');
            END IF;
        END
        $do$;
        """)
        db_conn.commit()
        db_conn.close()
        return True

    def __create_tables(self):
        logger.debug(f"[{self.class_name}] Create tables")
        queries = [
            f"CREATE SCHEMA IF NOT EXISTS {self.__database_schema}",
            f"""CREATE TABLE IF NOT EXISTS {self.__database_schema}.flowers_img(
                img_idx SERIAL PRIMARY KEY,
                filename TEXT,
                image_features FLOAT[]
            )
            """,
            f"""CREATE TABLE IF NOT EXISTS {self.__database_schema}.config (
                key  TEXT NOT NULL PRIMARY KEY,
                data TEXT DEFAULT '{{}}'
            )
            """,
            f""" INSERT INTO {self.__database_schema}.config
                (
                    SELECT  *
                    FROM    (VALUES('base','{{}}')) as tmp (key, data)
                    WHERE   NOT EXISTS ( SELECT 1 FROM {self.__database_schema}.config m where m.key = tmp.key )
                )
            """,
            "CREATE EXTENSION IF NOT EXISTS pg_trgm",
            """
            CREATE OR REPLACE FUNCTION cosine_similarity(a double precision[], b double precision[])
            RETURNS double precision AS $body$
            DECLARE
                dot_product double precision;
                norm_a double precision;
                norm_b double precision;
            BEGIN
                dot_product := 0;
                norm_a := 0;
                norm_b := 0;

                FOR i IN 1..array_length(a, 1) LOOP
                    dot_product := dot_product + a[i] * b[i];
                    norm_a := norm_a + a[i] * a[i];
                    norm_b := norm_b + b[i] * b[i];
                END LOOP;

                norm_a := sqrt(norm_a);
                norm_b := sqrt(norm_b);

                IF norm_a = 0 OR norm_b = 0 THEN
                    RETURN 0;
                ELSE
                    RETURN dot_product / (norm_a * norm_b);
                END IF;
            END;
            $body$ LANGUAGE plpgsql;
            """
        ]

        for query in queries:
            safe_execute(None, self.__write, query)

    ### IMAGE HANDLER ####
    def save_img(self, filename, features):
        err_msg   = ""
        lastrowid = None
        try:
            lastrowid = self.__write(f"INSERT INTO {self.__database_schema}.flowers_img(filename, image_features) VALUES (%s, %s) RETURNING img_idx",
                                     filename, features).fetchone()[0]
            self.__index.add(features, lastrowid)
        except Exception as e:
            err_msg = f"Failed to save. Error occur: {str(e)}"
        except:
            err_msg = "Failed to save. Unknow Error"
        if err_msg != "":
            logger.error(f"[{self.class_name}] Err: {err_msg}")
            return err_msg
        return lastrowid

    def delete_img(self, img_idx):
        err_msg = ""
        try:
            # Delete and check it
            if self.__write(f"DELETE FROM {self.__database_schema}.flowers_img WHERE img_idx = %s", img_idx).rowcount < 1:
                raise Exception("item not found")
            self.__index.remove_ids([img_idx])
        except Exception as e:
            err_msg = f"Failed to delete. Error: {str(e)}"
        except:
            err_msg = "Failed to delete. Unknow Error"
        if err_msg != "":
            logger.error(err_msg)
            return err_msg
        return True

    def query_img_by_id(self, img_idx: int):
        query = f"SELECT img_idx as id, filename as path FROM {self.__database_schema}.flowers_img WHERE img_idx = %s"
        return self.__read(query, img_idx).fetchall()

    def query_img(self, txt_features, first: int, size: int, type: int):
        print(first, size, type)
        if type == 1:
            base_query  = f"""
                SELECT * FROM (
                    SELECT  fi.img_idx, fi.filename, image_features @@ %s as similarity
                    FROM    {self.__database_schema}.flowers_img fi
                ) 
            """
            txt_features = " ".join([str(i) for i in txt_features])
        elif type == 2:
            base_query = f"""
                SELECT * FROM (
                    SELECT  fi.img_idx, fi.filename, '-' as similarity
                    FROM    {self.__database_schema}.flowers_img fi
                    WHERE   fi.img_idx IN %s
                )
            """
            img_idxs = self.__index.query(txt_features, size if size is not None else 10)
            # txt_features = ', '.join([str(i) for i in img_idxs])
            txt_features = tuple(img_idxs)
        else:
            base_query  = f"""
                SELECT * FROM (
                    SELECT  fi.img_idx, fi.filename, cosine_similarity(image_features, %s) as similarity
                    FROM    {self.__database_schema}.flowers_img fi
                ) WHERE similarity > {self.__threshold}
            """

        count_query = f"SELECT COUNT(1) FROM ({ base_query })"
        sel_query   = f"{ base_query } ORDER BY similarity DESC LIMIT { size if size is not None else 10 }"

        if first is not None:
            sel_query += f" OFFSET {first}"

        data    = None
        count   = None
        err_msg = ""
        try:
            cursor   = self.__read(count_query, txt_features)
            count    = cursor.fetchall()[0][0]

            cursor   = self.__read(sel_query, txt_features)
            data     = cursor.fetchall()
        except Exception as e:
            err_msg = f"Failed to select. Error: {str(e)}"
        except:
            err_msg = "Failed to select. Unknow Error"

        if err_msg != "":
            logger.error(err_msg)
            return err_msg

        out_data = []
        for it in data:
            out_it = {
                "id":       it[0],
                "path":     it[1],
                "simi":     it[2],
            }
            out_data.append(out_it)
        if len(out_data) == 0:
            return f"Not found any images have similarity above {self.__threshold}"
        return count, out_data
    ### END OF [IMAGE HANDLER] ####

    ### BASE CONFIG ####
    def save_conf(self, data):
        query = f"UPDATE {self.__database_schema}.config SET data = %s WHERE key = %s"
        return safe_execute(None, self.__write, query, data, 'base')

    def query_conf(self):
        query = f"SELECT data FROM {self.__database_schema}.config where key = %s"
        cursor = self.__rconn.cursor()
        cursor.execute(query, ['base'])
        _rows = cursor.fetchall()

        if len(_rows) == 0:
            return '{}'
        return _rows[0][0]
    ### END OF [BASE CONFIG] ####
