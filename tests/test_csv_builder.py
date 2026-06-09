import json
import pytest
from qaforge.csv_builder import (
    load_csv,
    load_csv_multiple_lines,
    get_scenario_data_csv,
    get_group_key,
    delete_output_file,
)


@pytest.fixture
def simple_csv(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("id,name,value\n1,alice,100\n2,bob,200\n")
    return str(path)


@pytest.fixture
def scenario_csv(tmp_path):
    path = tmp_path / "scenarios.csv"
    path.write_text("test_scenario_id,name,expected\nscenario_1,alice,pass\nscenario_2,bob,fail\n")
    return str(path)


@pytest.fixture
def multi_line_csv(tmp_path):
    path = tmp_path / "multi.csv"
    path.write_text("order_id,item,qty\n1,apple,2\n1,banana,3\n2,cherry,1\n")
    return str(path)


# --- load_csv ---

def test_load_csv_returns_list_of_json_strings(simple_csv):
    result = load_csv(simple_csv)
    assert len(result) == 2
    assert all(isinstance(r, str) for r in result)


def test_load_csv_parses_correctly(simple_csv):
    result = load_csv(simple_csv)
    first = json.loads(result[0])
    assert first["id"] == "1"
    assert first["name"] == "alice"


def test_load_csv_all_rows_present(simple_csv):
    result = load_csv(simple_csv)
    names = [json.loads(r)["name"] for r in result]
    assert names == ["alice", "bob"]


# --- get_scenario_data_csv ---

def test_get_scenario_data_csv_filters_correctly(scenario_csv):
    result = get_scenario_data_csv(scenario_csv, "scenario_1")
    assert len(result) == 1
    assert json.loads(result[0])["name"] == "alice"


def test_get_scenario_data_csv_no_match_returns_empty(scenario_csv):
    result = get_scenario_data_csv(scenario_csv, "scenario_99")
    assert result == []


def test_get_scenario_data_csv_multiple_matches(tmp_path):
    path = tmp_path / "dup.csv"
    path.write_text("test_scenario_id,val\nscenario_1,a\nscenario_1,b\n")
    result = get_scenario_data_csv(str(path), "scenario_1")
    assert len(result) == 2


# --- load_csv_multiple_lines ---

def test_load_csv_multiple_lines_groups_by_key(multi_line_csv):
    result = load_csv_multiple_lines(multi_line_csv, ["order_id"], "items", ["item", "qty"])
    assert len(result) == 2
    order_1 = json.loads(result[0])
    assert len(order_1["items"]) == 2


# --- get_group_key ---

def test_get_group_key_joins_values():
    row = {"order_id": "1", "name": "alice", "extra": "x"}
    key = get_group_key(row, ["order_id", "name"])
    assert key == "1_alice"


# --- delete_output_file ---

def test_delete_output_file_removes_existing_file(tmp_path):
    path = tmp_path / "to_delete.txt"
    path.write_text("content")
    delete_output_file(str(path))
    assert not path.exists()


def test_delete_output_file_does_not_raise_when_missing(tmp_path):
    delete_output_file(str(tmp_path / "nonexistent.txt"))
