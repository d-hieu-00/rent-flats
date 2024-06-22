import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.utils import logger
from utils.utils import safe_execute
from database.sql.db_pgsql import DBPgSql

class DBMain(DBPgSql):
    def __init__(self, db_config):
        super().__init__(db_config, 'main')

        # Init database
        self.__init_database()
        logger.info(f"[{self.class_name}] Started main database")

    def __del__(self):
        super().__del__()

    def __create_table_queries(self):
        return [
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.users (
                user_id     SERIAL NOT NULL PRIMARY KEY,
                username    VARCHAR(256) NOT NULL,
                password    TEXT NOT NULL,
                salt        VARCHAR(32) NOT NULL,
                email       VARCHAR(320) NOT NULL,
                admin       INTEGER NOT NULL DEFAULT 0,
                state       INTEGER NOT NULL DEFAULT 1,
                additional  JSONB DEFAULT '{{}}'
            )""",
            f"""CREATE UNIQUE INDEX IF NOT EXISTS user_name_idx ON {self.database_schema}.users(username, email) WHERE state != 0 AND admin = 0
            """,
            f"""CREATE UNIQUE INDEX IF NOT EXISTS admin_name_idx ON {self.database_schema}.users(username, email) WHERE state != 0 AND admin = 1
            """,
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.sessions (
                user_id     INTEGER NOT NULL REFERENCES {self.database_schema}.users(user_id),
                session_id  UUID NOT NULL PRIMARY KEY,
                login_ip    VARCHAR(128) NOT NULL,
                expiration  TIMESTAMP NOT NULL,
                additional  JSONB NOT NULL DEFAULT '{{}}'
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.user_logs (
                user_id     INTEGER NOT NULL REFERENCES {self.database_schema}.users(user_id),
                key_data    TEXT NOT NULL,
                old_data    TEXT NOT NULL,
                new_data    TEXT NOT NULL
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.admin_logs (
                user_id     INTEGER NOT NULL REFERENCES {self.database_schema}.users(user_id),
                key_data    TEXT NOT NULL,
                old_data    TEXT NOT NULL,
                new_data    TEXT NOT NULL
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.__houses (
                house_id    SERIAL NOT NULL PRIMARY KEY,
                address     TEXT NOT NULL,
                capacity    INTEGER NOT NULL,
                base_price  INTEGER NOT NULL,
                state       INTEGER NOT NULL DEFAULT 1,
                additional  JSONB DEFAULT '{{}}'
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.__house_discounts (
                house_id    INTEGER NOT NULL REFERENCES {self.database_schema}.__houses(house_id),
                discount    JSONB DEFAULT '{{}}',
                start       DATE NOT NULL,
                expiration  DATE NOT NULL
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.__house_feedbacks (
                user_id     INTEGER NOT NULL REFERENCES {self.database_schema}.users(user_id),
                house_id    INTEGER NOT NULL REFERENCES {self.database_schema}.__houses(house_id),
                feedback_id SERIAL NOT NULL PRIMARY KEY,
                feedback    JSONB DEFAULT '{{}}',
                send_date   TIMESTAMP NOT NULL,
                state       INTEGER NOT NULL DEFAULT 1
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.__house_bills (
                house_id    INTEGER NOT NULL REFERENCES {self.database_schema}.__houses(house_id),
                bill_data   JSONB DEFAULT '{{}}',
                init_date   TIMESTAMP NOT NULL,
                pay_date    TIMESTAMP DEFAULT NULL,
                state       INTEGER NOT NULL DEFAULT 1,
                additional  JSONB DEFAULT '{{}}'
            )""",
            f"""CREATE TABLE IF NOT EXISTS {self.database_schema}.__feedbacks (
                user_id     INTEGER NOT NULL REFERENCES {self.database_schema}.users(user_id),
                feedback_id SERIAL NOT NULL PRIMARY KEY,
                feedback    JSONB DEFAULT '{{}}',
                send_date   TIMESTAMP NOT NULL,
                state       INTEGER NOT NULL DEFAULT 1
            )""",
        ]

    def __create_function_queries(self):
        return [
            f"""CREATE OR REPLACE {self.database_schema}.get_user_by_session_id(IN in_session_id text, IN in_extend_min interval default '5 min')
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data jsonb;
                BEGIN
                    SELECT  row_to_json(users)::jsonb || jsonb_build_object('session', row_to_json(sessions)) INTO out_data
                    FROM    {self.database_schema}.users users JOIN {self.database_schema}.sessions sessions ON users.user_id = sessions.user_id
                    WHERE   sessions.session_id = in_session_id::uuid AND users.state != 0;

                    IF out_data IS NULL THEN
                        RETURN jsonb_build_object('error', 'Not found session');
                    END IF;

                    IF out_data->'session'->'expiration'::timestamp >= CURRENT_TIMESTAMP THEN
                        out_data := out_data || jsonb_build_object('session', jsonb_build_object('expiration', CURRENT_TIMESTAMP + in_extend_min));
                        UPDATE {self.database_schema}.sessions
                        SET    expiration = out_data->'session'->'expiration'::timestamp
                        WHERE  sessions.session_id = in_session_id::uuid;
                    ELSE
                        DELETE FROM {self.database_schema}.sessions WHERE sessions.session_id = in_session_id::uuid;
                        RETURN jsonb_build_object('error', 'Session is expired');
                    END IF;
                    RETURN out_data;
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.get_user_by_id(IN in_user_id integer)
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data jsonb;
                BEGIN
                    SELECT  row_to_json(users)::jsonb INTO out_data
                    FROM    {self.database_schema}.users users
                    WHERE   users.user_id = in_user_id AND users.state != 0;

                    IF out_data IS NULL THEN
                        RETURN jsonb_build_object('error', 'Not found');
                    END IF;
                    RETURN out_data;
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.new_session(IN in_user_id integer, IN in_login_ip text, IN in_additional JSONB default '{{}}', IN in_extend_min interval default '5 min')
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data        jsonb;
                    out_session_id  uuid;
                BEGIN
                    SELECT {self.database_schema}.get_user_by_id(in_user_id) INTO out_data;

                    IF out_data ? 'error' THEN
                        RETURN out_data;
                    END IF;

                    INSERT {self.database_schema}.sessions(user_id, session_id, login_ip, expiration, additional)
                    VALUES (in_user_id, gen_random_uuid(), in_login_ip, CURRENT_TIMESTAMP + in_extend_min, in_additional)
                    RETURNING session_id INTO out_session_id;

                    IF out_session_id IS NULL THEN
                        RETURN jsonb_build_object('error', 'Internal Error (1)');
                    END IF;

                    SELECT {self.database_schema}.get_user_by_session_id(out_session_id) INTO out_data;
                    RETURN out_data;
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.new_user(IN in_data jsonb)
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data        jsonb;
                    out_user_id     integer;
                BEGIN
                    IF EXISTS (SELECT 1 FROM {self.database_schema}.users WHERE username = in_data->>'username' AND state != 0 AND admin = 0) THEN
                        RETURN jsonb_build_object('error', 'Username is existed. Please input other username');
                    END IF;

                    IF EXISTS (SELECT 1 FROM {self.database_schema}.users WHERE email = in_data->>'email' AND state != 0 AND admin = 1) THEN
                        RETURN jsonb_build_object('error', 'Email is existed. Please choose input other email');
                    END IF;

                    INSERT {self.database_schema}.users(username, password, salt, email, additional)
                    VALUES (in_data->>'username', in_data->>'password', in_data->>'salt', in_data->>'email', in_data->'additional')
                    RETURNING user_id INTO out_user_id;

                    IF out_user_id IS NULL THEN
                        RETURN jsonb_build_object('error', 'Internal Error (1)');
                    END IF;

                    SELECT {self.database_schema}.get_user_by_id(out_user_id) INTO out_data;
                    RETURN out_data;
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.update_user(IN in_data jsonb)
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    old_data        jsonb;
                    out_data        jsonb;
                    out_user_id     integer;
                BEGIN
                    SELECT {self.database_schema}.get_user_by_id(out_user_id) INTO old_data;

                    IF old_data ? 'error' THEN
                        RETURN old_data;
                    END IF;

                    UPDATE  {self.database_schema}.users(username, password, salt, email, additional)
                    SET     username = in_data->>'username', password = in_data->>'password', additional = in_data->'additional'
                    WHERE   user_id = (in_data->>'user_id')::integer
                    RETURNING user_id INTO out_user_id;

                    IF out_user_id IS NULL THEN
                        RETURN jsonb_build_object('error', 'Internal Error (1)');
                    END IF;

                    SELECT {self.database_schema}.get_user_by_id(out_user_id) INTO out_data;
                    RETURN jsonb_build_object('old', old_data, 'new', out_data);
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.new_admin_user(IN in_data jsonb)
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data        jsonb;
                    out_user_id     integer;
                BEGIN
                    IF EXISTS (SELECT 1 FROM {self.database_schema}.users WHERE username = in_data->>'username' AND state != 0 AND admin = 1) THEN
                        RETURN jsonb_build_object('error', 'Username is existed. Please input other username');
                    END IF;

                    IF EXISTS (SELECT 1 FROM {self.database_schema}.users WHERE email = in_data->>'email' AND state != 0 AND admin = 1) THEN
                        RETURN jsonb_build_object('error', 'Email is existed. Please choose input other email');
                    END IF;

                    INSERT {self.database_schema}.users(username, password, salt, email, admin, additional)
                    VALUES (in_data->>'username', in_data->>'password', in_data->>'salt', in_data->>'email', 1, in_data->'additional')
                    RETURNING user_id INTO out_user_id;

                    IF out_user_id IS NULL THEN
                        RETURN jsonb_build_object('error', 'Internal Error (1)');
                    END IF;

                    SELECT {self.database_schema}.get_user_by_id(out_user_id) INTO out_data;
                    RETURN out_data;
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.find_user(IN in_data text, IN in_admin integer)
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data        jsonb;
                BEGIN
                    SELECT  row_to_json(users)::jsonb INTO out_data
                    FROM    {self.database_schema}.users
                    WHERE   username = in_data AND state != 0 AND admin = in_admin;

                    IF out_data IS NULL THEN
                        SELECT  row_to_json(users)::jsonb INTO out_data
                        FROM    {self.database_schema}.users
                        WHERE   email = in_data AND state != 0 AND admin = in_admin;
                    END IF;

                    IF out_data IS NULL THEN
                        RETURN jsonb_build_object('error', 'Not found user');
                    END IF;

                    RETURN out_data;
                END;
                $$;
            """,
            f"""CREATE OR REPLACE {self.database_schema}.find_house(IN in_data text)
                    RETURNS jsonb
                    LANGUAGE plpgsql
                AS $$
                DECLARE
                    out_data        jsonb;
                BEGIN
                    IF in_data = '' THEN
                        SELECT  
                    END IF;



                    SELECT  row_to_json(users)::jsonb INTO out_data
                    FROM    {self.database_schema}.__houses
                    WHERE   username = in_data AND state != 0 AND admin = in_admin;

                    IF out_data IS NULL THEN
                        SELECT  row_to_json(users)::jsonb INTO out_data
                        FROM    {self.database_schema}.users
                        WHERE   email = in_data AND state != 0 AND admin = in_admin;
                    END IF;

                    IF out_data IS NULL THEN
                        RETURN jsonb_build_object('error', 'Not found user');
                    END IF;

                    RETURN out_data;
                END;
                $$;
            """,
        ]

    def __init_database(self):
        for query in self.__create_table_queries():
            safe_execute(None, self._write, query)
        for query in self.__create_function_queries():
            safe_execute(None, self._write, query)
