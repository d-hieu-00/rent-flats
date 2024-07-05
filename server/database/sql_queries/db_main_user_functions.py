def queries(schema_name):
    return [
        f"""CREATE OR REPLACE FUNCTION {schema_name}.get_user_by_session_id(IN in_session_id text, IN in_extend_min interval default '5 min')
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data jsonb;
            BEGIN
                SELECT  row_to_json(users)::jsonb || jsonb_build_object('session', row_to_json(sessions)) INTO out_data
                FROM    {schema_name}.users users JOIN {schema_name}.sessions sessions ON users.user_id = sessions.user_id
                WHERE   sessions.session_id = in_session_id::uuid AND users.state != 0;

                IF out_data IS NULL THEN
                    RETURN jsonb_build_object('error', 'Not found session');
                END IF;

                IF (out_data->'session'->>'expiration')::timestamp >= CURRENT_TIMESTAMP THEN
                    out_data := out_data || jsonb_build_object('session', jsonb_build_object('expiration', CURRENT_TIMESTAMP + in_extend_min));
                    UPDATE {schema_name}.sessions
                    SET    expiration = (out_data->'session'->>'expiration')::timestamp
                    WHERE  sessions.session_id = in_session_id::uuid;
                ELSE
                    DELETE FROM {schema_name}.sessions WHERE sessions.session_id = in_session_id::uuid;
                    RETURN jsonb_build_object('error', 'Session is expired');
                END IF;
                RETURN out_data;
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.get_user_by_id(IN in_user_id integer)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data jsonb;
            BEGIN
                SELECT  row_to_json(users)::jsonb INTO out_data
                FROM    {schema_name}.users users
                WHERE   users.user_id = in_user_id AND users.state != 0;

                IF out_data IS NULL THEN
                    RETURN jsonb_build_object('error', 'Not found');
                END IF;
                RETURN out_data;
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.new_session(IN in_user_id integer, IN in_login_ip text, IN in_additional JSONB default '{{}}', IN in_extend_min interval default '5 min')
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data        jsonb;
                out_session_id  uuid;
            BEGIN
                SELECT {schema_name}.get_user_by_id(in_user_id) INTO out_data;

                IF out_data ? 'error' THEN
                    RETURN out_data;
                END IF;

                INSERT INTO {schema_name}.sessions(user_id, session_id, login_ip, expiration, additional)
                VALUES (in_user_id, gen_random_uuid(), in_login_ip, CURRENT_TIMESTAMP + in_extend_min, in_additional)
                RETURNING session_id INTO out_session_id;

                IF out_session_id IS NULL THEN
                    RETURN jsonb_build_object('error', 'Internal Error (1)');
                END IF;

                SELECT {schema_name}.get_user_by_session_id(out_session_id::text) INTO out_data;
                RETURN out_data || jsonb_build_object('session_id', out_session_id);
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.end_session(IN in_session_id text)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data        jsonb;
                out_session_id  uuid;
            BEGIN
                SELECT  row_to_json(users)::jsonb || jsonb_build_object('session', row_to_json(sessions)) INTO out_data
                FROM    {schema_name}.users users JOIN {schema_name}.sessions sessions ON users.user_id = sessions.user_id
                WHERE   sessions.session_id = in_session_id::uuid AND users.state != 0;

                IF out_data IS NULL THEN
                    RETURN jsonb_build_object('error', 'Not found session');
                END IF;

                DELETE FROM {schema_name}.sessions WHERE sessions.session_id = in_session_id::uuid;
                RETURN jsonb_build_object('result', 'Success');
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.new_user(IN in_data jsonb)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data        jsonb;
                out_user_id     integer;
            BEGIN
                IF EXISTS (SELECT 1 FROM {schema_name}.users WHERE username = in_data->>'username' AND state != 0 AND admin = 0) THEN
                    RETURN jsonb_build_object('error', 'Username is existed. Please input other username');
                END IF;

                IF EXISTS (SELECT 1 FROM {schema_name}.users WHERE email = in_data->>'email' AND state != 0 AND admin = 1) THEN
                    RETURN jsonb_build_object('error', 'Email is existed. Please choose input other email');
                END IF;

                INSERT INTO {schema_name}.users(username, password, salt, email, additional)
                VALUES (in_data->>'username', in_data->>'password', in_data->>'salt', in_data->>'email', in_data->'additional')
                RETURNING user_id INTO out_user_id;

                IF out_user_id IS NULL THEN
                    RETURN jsonb_build_object('error', 'Internal Error (1)');
                END IF;

                SELECT {schema_name}.get_user_by_id(out_user_id) INTO out_data;
                RETURN out_data;
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.update_user(IN in_data jsonb)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                old_data        jsonb;
                out_data        jsonb;
                out_user_id     integer;
            BEGIN
                SELECT {schema_name}.get_user_by_id(out_user_id) INTO old_data;

                IF old_data ? 'error' THEN
                    RETURN old_data;
                END IF;

                UPDATE  {schema_name}.users
                SET     username = in_data->>'username', password = in_data->>'password', additional = in_data->'additional'
                WHERE   user_id = (in_data->>'user_id')::integer
                RETURNING user_id INTO out_user_id;

                IF out_user_id IS NULL THEN
                    RETURN jsonb_build_object('error', 'Internal Error (1)');
                END IF;

                SELECT {schema_name}.get_user_by_id(out_user_id) INTO out_data;
                RETURN jsonb_build_object('old', old_data, 'new', out_data);
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.new_admin_user(IN in_data jsonb)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data        jsonb;
                out_user_id     integer;
            BEGIN
                IF EXISTS (SELECT 1 FROM {schema_name}.users WHERE username = in_data->>'username' AND state != 0 AND admin = 1) THEN
                    RETURN jsonb_build_object('error', 'Username is existed. Please input other username');
                END IF;

                IF EXISTS (SELECT 1 FROM {schema_name}.users WHERE email = in_data->>'email' AND state != 0 AND admin = 1) THEN
                    RETURN jsonb_build_object('error', 'Email is existed. Please choose input other email');
                END IF;

                INSERT INTO {schema_name}.users(username, password, salt, email, admin, additional)
                VALUES (in_data->>'username', in_data->>'password', in_data->>'salt', in_data->>'email', 1, in_data->'additional')
                RETURNING user_id INTO out_user_id;

                IF out_user_id IS NULL THEN
                    RETURN jsonb_build_object('error', 'Internal Error (1)');
                END IF;

                SELECT {schema_name}.get_user_by_id(out_user_id) INTO out_data;
                RETURN out_data;
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.find_user(IN in_data text, IN in_admin integer)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                out_data        jsonb;
            BEGIN
                SELECT  row_to_json(users)::jsonb INTO out_data
                FROM    {schema_name}.users
                WHERE   username = in_data AND state != 0 AND admin = in_admin;

                IF out_data IS NULL THEN
                    SELECT  row_to_json(users)::jsonb INTO out_data
                    FROM    {schema_name}.users
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
