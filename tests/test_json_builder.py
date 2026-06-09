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
    edit_template_json,
    beautify_json,
    get_beautified_payload,
    template_editor,
    create_payload,
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


def test_find_key_and_replace_in_list_of_dicts():
    obj = [{"key": "old"}, {"other": "value"}]
    find_key_and_replace_value_json(obj, "key", "new")
    assert obj[0]["key"] == "new"


def test_find_key_and_replace_in_list_not_found():
    obj = [{"a": 1}, {"b": 2}]
    result = find_key_and_replace_value_json(obj, "missing", "new")
    assert result is None


# --- convert_to_dict ---

def test_convert_to_dict_from_dict():
    assert convert_to_dict({"k": "v"}) == {"k": "v"}


def test_convert_to_dict_from_list_returns_first_element():
    result = convert_to_dict([{"k": "v1"}, {"k": "v2"}])
    assert result == {"k": "v1"}


def test_convert_to_dict_from_empty_list_returns_none():
    assert convert_to_dict([]) is None


def test_convert_to_dict_from_other_type_raises():
    with pytest.raises(TypeError):
        convert_to_dict("not a dict or list")


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


def test_edit_json_skips_primitive_values_when_key_missing():
    data = {"name": "old", "count": 5}
    result = edit_json(data, {"missing_key": "new"})
    assert result[0]["count"] == 5


# --- edit_template_json ---

def test_edit_template_json_with_list_of_json_strings(tmp_path):
    json_file = tmp_path / "template.json"
    json_file.write_text(json.dumps({"name": "old", "value": 1}))

    result = edit_template_json(str(json_file), [json.dumps({"name": "new"})])

    assert len(result) == 1
    assert json.loads(result[0])[0]["name"] == "new"


def test_edit_template_json_with_dict(tmp_path):
    json_file = tmp_path / "template.json"
    json_file.write_text(json.dumps({"name": "old", "value": 1}))

    result = edit_template_json(str(json_file), {"name": "new"})

    assert len(result) == 1
    assert json.loads(result[0])[0]["name"] == "new"


def test_edit_template_json_with_empty_args_returns_empty(tmp_path):
    json_file = tmp_path / "template.json"
    json_file.write_text(json.dumps({"name": "old"}))

    result = edit_template_json(str(json_file), "not a list or dict")
    assert result == []


# --- beautify_json ---

def test_beautify_json_returns_formatted_bytes():
    result = beautify_json("template", '{"key": "value"}')
    assert isinstance(result, bytes)
    assert b'"key"' in result


def test_beautify_json_raises_on_malformed_json():
    with pytest.raises(Exception, match="malformed"):
        beautify_json("template", "not valid {{ json }}")


# --- get_beautified_payload ---

def test_get_beautified_payload_with_string():
    result = get_beautified_payload("template", '{"key": "value"}')
    assert isinstance(result, bytes)


def test_get_beautified_payload_with_list():
    result = get_beautified_payload("template", ['{"a": 1}', '{"b": 2}'])
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(r, bytes) for r in result)


# --- template_editor ---

def test_template_editor_returns_data_when_name_is_none():
    data = {"key": "value"}
    assert template_editor(None, data, False) == data


def test_template_editor_returns_data_when_name_is_none_string():
    data = {"key": "value"}
    assert template_editor("none", data, False) == data


def test_template_editor_returns_data_when_data_is_none():
    assert template_editor("some_template", None, False) is None


def test_template_editor_renders_single_request(tmp_path, monkeypatch):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "user.json").write_text('{"name": "{{ dict_list.name }}"}')
    monkeypatch.chdir(tmp_path)

    result = template_editor("user", {"name": "alice"}, False)
    assert "alice" in result


def test_template_editor_renders_multiple_requests(tmp_path, monkeypatch):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "user.json").write_text('{"name": "{{ dict_list[0].name }}"}')
    monkeypatch.chdir(tmp_path)

    result = template_editor("user", [{"name": "alice"}, {"name": "bob"}], True)
    assert isinstance(result, list)
    assert len(result) == 2
    assert "alice" in result[0]
    assert "bob" in result[1]


# --- create_payload ---

def test_create_payload_with_none_template():
    result = create_payload(None, '{"key": "value"}', False)
    assert isinstance(result, bytes)
    assert b'"key"' in result
