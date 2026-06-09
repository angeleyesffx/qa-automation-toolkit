import pytest
from unittest.mock import MagicMock, patch
from qaforge.request_builder import (
    response_from_auth,
    get_access_token,
    zip_payload,
    select_request,
    split,
)


# --- zip_payload ---

def test_zip_payload_returns_bytes():
    result = zip_payload("hello world")
    assert isinstance(result, bytes)


def test_zip_payload_accepts_string():
    result = zip_payload("test payload")
    assert len(result) > 0


def test_zip_payload_accepts_bytes():
    result = zip_payload(b"raw bytes")
    assert isinstance(result, bytes)


# --- split ---

def test_split_chunks_list():
    result = list(split([1, 2, 3, 4, 5], 2))
    assert result == [[1, 2], [3, 4], [5]]


def test_split_chunk_size_larger_than_list():
    result = list(split([1, 2], 10))
    assert result == [[1, 2]]


# --- response_from_auth ---

def test_response_from_auth_returns_none_when_method_is_none():
    result = response_from_auth(None, "http://example.com", {})
    assert result is None


@patch("qaforge.request_builder.select_request")
def test_response_from_auth_returns_json_data(mock_select):
    mock_response = MagicMock()
    mock_response.json.return_value = {"token": "abc123"}
    mock_select.return_value = mock_response

    result = response_from_auth("post", "http://example.com", {})
    assert result == {"token": "abc123"}


@patch("qaforge.request_builder.select_request")
def test_response_from_auth_returns_none_when_response_is_none(mock_select):
    mock_select.return_value = None
    result = response_from_auth("post", "http://example.com", {})
    assert result is None


# --- get_access_token ---

@patch("qaforge.request_builder.response_from_auth")
def test_get_access_token_returns_token(mock_auth):
    mock_auth.return_value = {"access_token": "mytoken123"}
    result = get_access_token("access_token", "post", "http://example.com", {})
    assert result == "mytoken123"


@patch("qaforge.request_builder.response_from_auth")
def test_get_access_token_returns_none_when_key_missing(mock_auth):
    mock_auth.return_value = {"other_key": "value"}
    result = get_access_token("access_token", "post", "http://example.com", {})
    assert result is None


# --- select_request ---

@patch("qaforge.request_builder.requests.request")
def test_select_request_post(mock_request):
    mock_request.return_value = MagicMock(status_code=200)
    result = select_request("post", "http://example.com", {}, {})
    assert result is not None
    mock_request.assert_called_once()


@patch("qaforge.request_builder.requests.request")
def test_select_request_put(mock_request):
    mock_request.return_value = MagicMock(status_code=200)
    select_request("put", "http://example.com", {}, {})
    mock_request.assert_called_once()


@patch("qaforge.request_builder.requests.request")
def test_select_request_delete(mock_request):
    mock_request.return_value = MagicMock(status_code=200)
    select_request("delete", "http://example.com", {}, {})
    mock_request.assert_called_once()


@patch("qaforge.request_builder.requests.get")
def test_select_request_get_iterates_payload(mock_get):
    mock_get.return_value = MagicMock(status_code=200)
    payloads = [{"p": 1}, {"p": 2}]
    result = select_request("get", "http://example.com", payloads, {})
    assert len(result) == 2
    assert mock_get.call_count == 2


def test_select_request_unknown_method_returns_none():
    result = select_request("patch", "http://example.com", {}, {})
    assert result is None
