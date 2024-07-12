def queries(schema_name):
    return [
        f"""CREATE OR REPLACE FUNCTION {schema_name}.find_house(IN in_data text, IN in_capacity integer, IN in_lower_price integer, IN in_upper_price integer, IN in_states jsonb, IN in_others jsonb)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                exec_sql        text;
                exec_count_sql  text;
                out_houses      jsonb;
                out_count       integer;
            BEGIN
                exec_sql := 'FROM    {schema_name}.__houses __houses
                    WHERE   $5 @> jsonb_build_array(state)
                            AND ($1 = '''' OR POSITION($1 in (additional)::text) > 0)
                            AND ($1 = '''' OR POSITION($1 in address) > 0)
                            AND ($2 <= 0 OR capacity = $2)
                            AND ($3 <= 0 OR base_price >= $3)
                            AND ($4 <= 0 OR base_price <= $4)
                    ';
                exec_count_sql := 'SELECT COUNT(1) ' || exec_sql;
                --
                IF in_others->>'order' = 'lower_price' THEN
                    -- exec_sql := exec_sql || 'ORDER BY base_price ASC ';
                    exec_sql := 'SELECT  jsonb_agg(row_to_json(__houses) ORDER BY base_price ASC ) ' || exec_sql || 'LIMIT 20 OFFSET 0';
                ELSIF in_others->>'order' = 'higher_price' THEN
                    -- exec_sql := exec_sql || 'ORDER BY base_price DESC ';
                    exec_sql := 'SELECT  jsonb_agg(row_to_json(__houses) ORDER BY base_price DESC ) ' || exec_sql || 'LIMIT 20 OFFSET 0';
                ELSE
                    -- exec_sql := exec_sql || 'ORDER BY house_id DESC ';
                    exec_sql := 'SELECT  jsonb_agg(row_to_json(__houses) ORDER BY __houses.house_id DESC ) ' || exec_sql || 'LIMIT 20 OFFSET 0';
                END IF;
                --
                -- exec_sql := 'SELECT  jsonb_agg(row_to_json(__houses)) ' || exec_sql || 'LIMIT 20 OFFSET 0';
                -- EXEC
                EXECUTE exec_sql INTO out_houses USING in_data, in_capacity, in_lower_price, in_upper_price, in_states, in_others;
                EXECUTE exec_count_sql INTO out_count USING in_data, in_capacity, in_lower_price, in_upper_price, in_states;

                RETURN jsonb_build_object(
                    'houses', out_houses,
                    'total', out_count
                );
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.get_rented_house(IN in_session_id text)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                exec_sql        text;
                exec_count_sql  text;
                out_houses      jsonb;
                out_count       integer;
                user_data       jsonb;
            BEGIN
                SELECT {schema_name}.get_user_by_session_id(in_session_id) INTO user_data;
                IF user_data ? 'error' THEN
                    RETURN user_data;
                END IF;

                exec_sql := 'FROM    {schema_name}.__houses __houses
                    WHERE   house_id IN (
                        SELECT house_id
                        FROM    {schema_name}.__house_bills
                        WHERE   user_id = $1
                    )
                    ';
                exec_count_sql := 'SELECT COUNT(1) ' || exec_sql;
                --
                exec_sql := 'SELECT  jsonb_agg(row_to_json(__houses) ORDER BY house_id DESC) ' || exec_sql || 'LIMIT 20 OFFSET 0';
                -- EXEC
                EXECUTE exec_sql INTO out_houses USING (user_data->>'user_id')::integer;
                EXECUTE exec_count_sql INTO out_count USING (user_data->>'user_id')::integer;

                RETURN jsonb_build_object(
                    'houses', out_houses,
                    'total', out_count
                );
            END;
            $$;
        """,
        f"""CREATE OR REPLACE FUNCTION {schema_name}.get_bills(IN in_session_id text, IN in_house_id integer)
                RETURNS jsonb
                LANGUAGE plpgsql
            AS $$
            DECLARE
                exec_sql        text;
                exec_count_sql  text;
                out_houses      jsonb;
                out_count       integer;
                user_data       jsonb;
            BEGIN
                SELECT {schema_name}.get_user_by_session_id(in_session_id) INTO user_data;
                IF user_data ? 'error' THEN
                    RETURN user_data;
                END IF;

                exec_sql := 'FROM    {schema_name}.__house_bills __house_bills
                    WHERE   house_id = $1 AND user_id = $2
                    ';
                exec_count_sql := 'SELECT COUNT(1) ' || exec_sql;
                --
                exec_sql := 'SELECT  jsonb_agg(row_to_json(__house_bills) ORDER BY house_id DESC) ' || exec_sql;
                -- EXEC
                EXECUTE exec_sql INTO out_houses USING in_house_id, (user_data->>'user_id')::integer;
                EXECUTE exec_count_sql INTO out_count USING in_house_id, (user_data->>'user_id')::integer;

                RETURN jsonb_build_object(
                    'bills', out_houses,
                    'total', out_count
                );
            END;
            $$;
        """,
    ]
