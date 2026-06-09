import pytest
from qaforge.list_manipulation import (
    union_list_without_duplicate_item,
    intersection_list,
    remove_item_from_list,
    get_random_item_from_list,
    get_different_random_item_from_list,
    get_list_from_source,
    datapool_read,
    get_data_from_dict,
)

SOURCE = {
    "valid_data": [{"key_1": "value1", "key_2": "value2"}],
}


# --- union ---

def test_union_returns_merged_without_duplicates():
    assert union_list_without_duplicate_item([1, 2], [2, 3]) == [1, 2, 3]


def test_union_returns_list():
    result = union_list_without_duplicate_item([1], [2])
    assert isinstance(result, list)


def test_union_does_not_mutate_original():
    a = [1, 2]
    union_list_without_duplicate_item(a, [3])
    assert a == [1, 2]


def test_union_empty_lists():
    assert union_list_without_duplicate_item([], []) == []


# --- remove ---

def test_remove_item_returns_list_without_item():
    assert remove_item_from_list([1, 2, 3], 2) == [1, 3]


def test_remove_item_does_not_mutate_original():
    original = [1, 2, 3]
    remove_item_from_list(original, 2)
    assert original == [1, 2, 3]


def test_remove_item_raises_when_not_present():
    with pytest.raises(ValueError):
        remove_item_from_list([1, 2], 99)


# --- random ---

def test_get_random_item_returns_element_from_list():
    items = [10, 20, 30]
    assert get_random_item_from_list(items) in items


def test_get_different_random_item_excludes_given_item():
    items = [1, 2, 3, 4, 5]
    for _ in range(20):
        assert get_different_random_item_from_list(items, 1) != 1


def test_get_different_random_item_returns_from_list():
    items = [1, 2, 3]
    assert get_different_random_item_from_list(items, 1) in items


# --- get_list_from_source ---

def test_get_list_from_source_returns_first_entry():
    result = get_list_from_source(SOURCE, "valid_data")
    assert result == {"key_1": "value1", "key_2": "value2"}


def test_get_list_from_source_handles_spaces_in_key():
    # function converts spaces to underscores when looking up source keys
    source = {"valid_data": [{"k": "v"}]}
    assert get_list_from_source(source, "valid data") == {"k": "v"}


def test_get_list_from_source_raises_when_missing():
    with pytest.raises(Exception, match="No matching results"):
        get_list_from_source({}, "missing_key")


# --- datapool_read ---

def test_datapool_read_returns_correct_value():
    assert datapool_read(SOURCE, "valid_data", "key_1") == "value1"


def test_datapool_read_raises_on_missing_data():
    with pytest.raises(Exception, match="No matching results"):
        datapool_read({}, "missing", "key_1")


def test_datapool_read_raises_on_missing_key():
    with pytest.raises(Exception, match="No matching results"):
        datapool_read(SOURCE, "valid_data", "key_99")


# --- get_data_from_dict ---

def test_get_data_from_dict_returns_value():
    assert get_data_from_dict({"k": "v"}, "k") == "v"


def test_get_data_from_dict_raises_on_missing_key():
    with pytest.raises(Exception, match="No matching results"):
        get_data_from_dict({"k": "v"}, "missing")


# --- intersection ---

def test_intersection_list():
    result = intersection_list([1, 2, 3], [[1, 4], [2, 5]])
    assert result == [[1], [2]]
