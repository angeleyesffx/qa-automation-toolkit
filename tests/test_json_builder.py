import json
import pytest
from qaforge.json_builder import (
    load_json_as_string,
    load_json_as_dict,
    get_json_keys,
    get_json_values,
    write_json_file,
    find_key_and_replace_value_json,
    convert_to_dict,
    edit_json,
)


@pytest.fixture
def json_file(tmp_path):
    data = {"name": "alice", "value": 42, "nested": {"inner": "old"}}
    path = tmp_path / "test.json"
    path.write_text(json.dumps(data))
    return str(path)


@pytest.fixture
def json_list_file(tmp_path):
    data = [{"name": "alice"}, {"name": "bob"}]
    path = tmp_path / "list.json"
    path.write_text(json.dumps(data))
    return str(path)


# --- load ---

def test_load_json_as_string_returns_raw_content(json_file):
    result = load_json_as_string(json_file)
    assert isinstance(result, str)
    assert '"name"' in result


def test_load_json_as_dict_returns_dict(json_file):
    result = load_json_as_dict(json_file)
    assert isinstance(result, dict)
    assert result["name"] == "alice"
    assert result["value"] == 42


def test_get_json_keys(json_file):
    keys = list(get_json_keys(json_file))
    assert set(keys) == {"name", "value", "nested"}


def test_get_json_values(json_file):
    values = list(get_json_values(json_file))
    assert "alice" in values
    assert 42 in values


# --- write ---

def test_write_json_file_creates_file(tmp_path):
    path = tmp_path / "output.json"
    write_json_file({"key": "value"}, file_path=str(path))
    assert json.loads(path.read_text()) == {"key": "value"}


def test_write_json_file_sorts_keys(tmp_path):
    path = tmp_path / "out.json"
    write_json_file({"b": 2, "a": 1}, file_path=str(path))
    content = path.read_text()
    assert content.index('"a"') < content.index('"b"')


# --- find_key_and_replace ---

def test_find_key_and_replace_in_flat_dict():
    obj = {"a": 1, "b": 2}
    find_key_and_replace_value_json(obj, "a", 99)
    assert obj["a"] == 99


def test_find_key_and_replace_in_nested_dict():
    obj = {"outer": {"inner": "old"}}
    find_key_and_replace_value_json(obj, "inner", "new")
    assert obj["outer"]["inner"] == "new"


def test_find_key_and_replace_in_list():
    obj = {"items": [{"key": "old"}]}
    find_key_and_replace_value_json(obj, "key", "new")
    assert obj["items"][0]["key"] == "new"


def test_find_key_and_replace_returns_none_when_not_found():
    result = find_key_and_replace_value_json({"a": 1}, "z", 99)
    assert result is None


# --- convert_to_dict ---

def test_convert_to_dict_from_dict():
    assert convert_to_dict({"k": "v"}) == {"k": "v"}


def test_convert_to_dict_from_list_returns_first_element():
    result = convert_to_dict([{"k": "v1"}, {"k": "v2"}])
    assert result == {"k": "v1"}


def test_convert_to_dict_from_empty_list_returns_none():
    assert convert_to_dict([]) is None


def test_convert_to_dict_from_other_type_returns_none(capsys):
    result = convert_to_dict("not a dict or list")
    assert result is None
    assert "Type is different" in capsys.readouterr().out


# --- edit_json ---

def test_edit_json_replaces_top_level_key():
    data = {"name": "old", "value": 1}
    result = edit_json(data, {"name": "new"})
    assert result[0]["name"] == "new"
    assert result[0]["value"] == 1


def test_edit_json_replaces_nested_key():
    data = {"outer": {"inner": "old"}}
    result = edit_json(data, {"inner": "new"})
    assert result[0]["outer"]["inner"] == "new"


def test_edit_json_returns_list():
    result = edit_json({"k": "v"}, {"k": "new"})
    assert isinstance(result, list)
