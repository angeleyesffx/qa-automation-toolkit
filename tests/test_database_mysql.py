import pytest
from unittest.mock import MagicMock, patch
from qaforge.database_mysql import (
    get_columns_from_dict,
    execute_query,
    execute_query_from_db,
    select_all_from_table,
)


def make_mock_connection(rows=None):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = rows or []
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor


# --- get_columns_from_dict ---

def test_get_columns_from_dict_returns_column_string():
    source = {"users": [{"id": 1, "name": "alice", "email": "a@b.com"}]}
    result = get_columns_from_dict(source, "users")
    assert result == "id, name, email"


def test_get_columns_from_dict_raises_when_key_missing():
    with pytest.raises(Exception, match="No matching results"):
        get_columns_from_dict({}, "missing")


def test_get_columns_from_dict_handles_spaces_in_key():
    # function converts spaces to underscores when looking up source keys
    source = {"valid_data": [{"col": "v"}]}
    result = get_columns_from_dict(source, "valid data")
    assert result == "col"


# --- execute_query ---

def test_execute_query_returns_fetchall_result():
    mock_conn, mock_cursor = make_mock_connection(rows=[{"id": 1}])
    result = execute_query(mock_conn, "SELECT 1")
    assert result == [{"id": 1}]


def test_execute_query_closes_connection():
    mock_conn, _ = make_mock_connection()
    execute_query(mock_conn, "SELECT 1")
    mock_conn.close.assert_called_once()


def test_execute_query_closes_connection_even_on_error():
    mock_conn = MagicMock()
    mock_conn.cursor.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        execute_query(mock_conn, "SELECT 1")
    mock_conn.close.assert_called_once()


# --- execute_query_from_db ---

@patch("qaforge.database_mysql.open_mysql_connection")
def test_execute_query_from_db_opens_and_closes_connection(mock_open):
    mock_conn, mock_cursor = make_mock_connection(rows=[{"id": 1}])
    mock_open.return_value = mock_conn

    result = execute_query_from_db("host", 3306, "user", "pass", "db", "SELECT 1")
    assert result == [{"id": 1}]
    mock_conn.close.assert_called_once()


# --- select_all_from_table ---

def test_select_all_from_table_uses_cursor():
    mock_conn, mock_cursor = make_mock_connection(rows=[{"id": 1, "name": "test"}])
    result = select_all_from_table(mock_conn, "users")
    mock_cursor.execute.assert_called_once_with("SELECT * FROM `users`")
    assert result == [{"id": 1, "name": "test"}]


def test_select_all_from_table_quotes_table_name():
    mock_conn, mock_cursor = make_mock_connection()
    select_all_from_table(mock_conn, "my_table")
    call_args = mock_cursor.execute.call_args[0][0]
    assert "`my_table`" in call_args
