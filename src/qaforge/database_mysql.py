import pymysql


def open_mysql_connection(host, port, username, password, database):
    return pymysql.connect(
        host=host, port=port, user=username, passwd=password, db=database,
        cursorclass=pymysql.cursors.DictCursor, autocommit=True,
    )


def get_columns_from_dict(source, args_key):
    """Return column names from source dict as a comma-separated string."""
    data_args = source.get(args_key.replace(' ', '_'))
    if data_args is None:
        raise Exception(f"No matching results for parameter data = {args_key} was found in DataPool.")
    return ', '.join(data_args[0].keys())


def execute_query(db_connection, sql_query):
    try:
        with db_connection.cursor() as cursor:
            cursor.execute(sql_query)
            return cursor.fetchall()
    finally:
        db_connection.close()


def execute_query_from_db(host, port, username, password, database, sql_query):
    connection = open_mysql_connection(host, port, username, password, database)
    return execute_query(connection, sql_query)


def select_all_from_table(db_connection, table):
    with db_connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table}`")
        return cursor.fetchall()
