import pytest
from qaforge.yaml_manipulation import read_yml_file, select_the_keys_from_yml


@pytest.fixture
def flat_yml(tmp_path):
    path = tmp_path / "flat.yml"
    path.write_text("key_a: value1\nkey_b: value2\nkey_c: value3\n")
    return str(path)


@pytest.fixture
def nested_yml(tmp_path):
    path = tmp_path / "nested.yml"
    path.write_text("group_a:\n  sub_1: v1\n  sub_2: v2\ngroup_b:\n  sub_3: v3\n")
    return str(path)


# --- read_yml_file ---

def test_read_yml_file_returns_dict(flat_yml):
    result = read_yml_file(flat_yml)
    assert isinstance(result, dict)


def test_read_yml_file_parses_values(flat_yml):
    result = read_yml_file(flat_yml)
    assert result["key_a"] == "value1"
    assert result["key_b"] == "value2"


# --- select_the_keys_from_yml ---

def test_select_keys_environment_returns_top_level_keys(flat_yml):
    result = select_the_keys_from_yml(flat_yml, "environment")
    assert set(result) == {"key_a", "key_b", "key_c"}


def test_select_keys_environment_returns_sorted_list(flat_yml):
    result = select_the_keys_from_yml(flat_yml, "environment")
    assert result == sorted(result)


def test_select_keys_nested_returns_all_sub_keys(nested_yml):
    result = select_the_keys_from_yml(nested_yml, "other")
    assert "sub_1" in result
    assert "sub_2" in result
    assert "sub_3" in result


def test_select_keys_nested_processes_all_groups(nested_yml):
    result = select_the_keys_from_yml(nested_yml, "other")
    assert len(result) == 3
