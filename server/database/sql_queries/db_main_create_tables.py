def queries(schema_name):
    return [
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.users (
            user_id     SERIAL NOT NULL PRIMARY KEY,
            username    VARCHAR(256) NOT NULL,
            password    TEXT NOT NULL,
            salt        VARCHAR(32) NOT NULL,
            email       VARCHAR(320) NOT NULL,
            admin       INTEGER NOT NULL DEFAULT 0,
            state       INTEGER NOT NULL DEFAULT 1,
            additional  JSONB DEFAULT '{{}}'
        )""",
        f"""CREATE UNIQUE INDEX IF NOT EXISTS user_name_idx ON {schema_name}.users(username, email) WHERE state != 0 AND admin = 0
        """,
        f"""CREATE UNIQUE INDEX IF NOT EXISTS admin_name_idx ON {schema_name}.users(username, email) WHERE state != 0 AND admin = 1
        """,
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.sessions (
            user_id     INTEGER NOT NULL REFERENCES {schema_name}.users(user_id),
            session_id  UUID NOT NULL PRIMARY KEY,
            login_ip    VARCHAR(128) NOT NULL,
            expiration  TIMESTAMP NOT NULL,
            additional  JSONB NOT NULL DEFAULT '{{}}'
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.user_logs (
            user_id     INTEGER NOT NULL REFERENCES {schema_name}.users(user_id),
            key_data    TEXT NOT NULL,
            old_data    TEXT NOT NULL,
            new_data    TEXT NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.admin_logs (
            user_id     INTEGER NOT NULL REFERENCES {schema_name}.users(user_id),
            key_data    TEXT NOT NULL,
            old_data    TEXT NOT NULL,
            new_data    TEXT NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.__houses (
            house_id    SERIAL NOT NULL PRIMARY KEY,
            address     TEXT NOT NULL,
            capacity    INTEGER NOT NULL,
            base_price  INTEGER NOT NULL,
            state       INTEGER NOT NULL DEFAULT 1,
            additional  JSONB DEFAULT '{{}}'
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.__house_discounts (
            house_id    INTEGER NOT NULL REFERENCES {schema_name}.__houses(house_id),
            discount    JSONB DEFAULT '{{}}',
            start       DATE NOT NULL,
            expiration  DATE NOT NULL
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.__house_feedbacks (
            user_id     INTEGER NOT NULL REFERENCES {schema_name}.users(user_id),
            house_id    INTEGER NOT NULL REFERENCES {schema_name}.__houses(house_id),
            feedback_id SERIAL NOT NULL PRIMARY KEY,
            feedback    JSONB DEFAULT '{{}}',
            send_date   TIMESTAMP NOT NULL,
            state       INTEGER NOT NULL DEFAULT 1
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.__house_bills (
            house_id    INTEGER NOT NULL REFERENCES {schema_name}.__houses(house_id),
            bill_data   JSONB DEFAULT '{{}}',
            init_date   TIMESTAMP NOT NULL,
            pay_date    TIMESTAMP DEFAULT NULL,
            state       INTEGER NOT NULL DEFAULT 1,
            additional  JSONB DEFAULT '{{}}'
        )""",
        f"""CREATE TABLE IF NOT EXISTS {schema_name}.__feedbacks (
            user_id     INTEGER NOT NULL REFERENCES {schema_name}.users(user_id),
            feedback_id SERIAL NOT NULL PRIMARY KEY,
            feedback    JSONB DEFAULT '{{}}',
            send_date   TIMESTAMP NOT NULL,
            state       INTEGER NOT NULL DEFAULT 1
        )""",
    ]