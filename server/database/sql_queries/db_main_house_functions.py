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
                exec_sql := 'FROM    __houses
                    WHERE   $5 @> jsonb_agg(state)
                            AND ($1 = '''' OR POSITION($1, addtional->>''search'') > 0)
                            AND ($2 <= 0 OR capacity = $2)
                            AND ($3 <= 0 OR base_price >= $3)
                            AND ($4 <= 0 OR base_price <= $4)
                    ';
                exec_count_sql := 'SELECT COUNT(1) ' || exec_sql;
                --
                IF in_others->>'order' = 'lower_price' THEN
                    exec_sql := exec_sql || 'ORDER BY base_price ASC ';
                ELSIF in_others->>'order' = 'higher_price' THEN
                    exec_sql := exec_sql || 'ORDER BY base_price DESC ';
                ELSE
                    exec_sql := exec_sql || 'ORDER BY __houses.house_id DESC ';
                END IF;
                --
                exec_sql := 'SELECT  jsonb_agg(row_to_json(__houses)) ' || exec_sql || 'LIMIT ($6->>''size'')::integer OFFSET ($6->>''first'')::integer';
                -- EXEC
                EXECUTE exec_sql INTO out_houses USING in_data, in_capacity, in_lower_price, in_upper_price, in_states, in_others;
                EXECUTE exec_count_sql INTO out_count USING in_data, in_capacity, in_lower_price, in_upper_price, in_states;

                RETURN jsonb_build_jsonb(
                    'houses', out_houses,
                    'total', out_count
                );
            END;
            $$;
        """,
    ]
