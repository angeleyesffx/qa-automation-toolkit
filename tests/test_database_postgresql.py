import pytest
from unittest.mock import MagicMock, patch
from qaforge.database_postgresql import open_postgresql_connection, execute_query


@patch("qaforge.database_postgresql.psycopg2.connect")
def test_open_postgresql_connection_returns_connection(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    result = open_postgresql_connection("host", "db", "user", "pass")
    assert result is mock_conn


@patch("qaforge.database_postgresql.psycopg2.connect")
def test_open_postgresql_connection_uses_ssl_require_by_default(mock_connect):
    open_postgresql_connection("host", "db", "user", "pass")
    conn_string = mock_connect.call_args[0][0]
    assert "sslmode=require" in conn_string


@patch("qaforge.database_postgresql.psycopg2.connect")
def test_execute_query_returns_rows(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "alice")]
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    mock_connect.return_value = mock_conn

    result = execute_query("host", "db", "user", "pass", "SELECT 1")
    assert result == [(1, "alice")]


@patch("qaforge.database_postgresql.psycopg2.connect")
def test_execute_query_closes_connection(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
    mock_connect.return_value = mock_conn

    execute_query("host", "db", "user", "pass", "SELECT 1")
    mock_conn.close.assert_called_once()


@patch("qaforge.database_postgresql.psycopg2.connect")
def test_execute_query_closes_connection_on_error(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.side_effect = Exception("connection failed")

    with pytest.raises(Exception, match="connection failed"):
        execute_query("host", "db", "user", "pass", "SELECT 1")
    mock_conn.close.assert_called_once()
