import psycopg2


def open_postgresql_connection(host, dbname, user, password, ssl_mode="require"):
    conn_string = f"host={host} user={user} dbname={dbname} password={password} sslmode={ssl_mode}"
    return psycopg2.connect(conn_string)


def execute_query(host, dbname, user, password, sql_query, ssl_mode="require"):
    conn = open_postgresql_connection(host, dbname, user, password, ssl_mode)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query)
            return cursor.fetchall()
    finally:
        conn.close()
