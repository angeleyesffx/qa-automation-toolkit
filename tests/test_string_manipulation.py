import pytest
from qaforge.string_manipulation import (
    empty_string_to_none_string,
    generate_unique_id,
    generate_unique_lowercase_id,
    generate_unique_uppercase_id,
    generate_unique_email,
    generate_random_number,
    split_string_between,
    split_string_before,
    split_string_after,
    remove_chars_from_string,
    replace_string_with,
)

# --- empty_string_to_none ---

def test_empty_string_returns_none():
    assert empty_string_to_none_string("") is None


def test_none_input_returns_none():
    assert empty_string_to_none_string(None) is None


def test_non_empty_string_returned_unchanged():
    assert empty_string_to_none_string("hello") == "hello"


def test_whitespace_not_treated_as_empty():
    assert empty_string_to_none_string(" ") == " "


# --- generate ids ---

def test_generate_unique_id_correct_length():
    assert len(generate_unique_id(10)) == 10


def test_generate_unique_id_is_alphanumeric():
    result = generate_unique_id(50)
    assert result.isalnum()


def test_generate_unique_lowercase_id_is_lowercase():
    result = generate_unique_lowercase_id(20)
    assert result == result.lower()
    assert len(result) == 20


def test_generate_unique_uppercase_id_is_uppercase():
    result = generate_unique_uppercase_id(20)
    assert result == result.upper()
    assert len(result) == 20


def test_generate_unique_id_produces_different_values():
    assert generate_unique_id(16) != generate_unique_id(16)


# --- generate_unique_email ---

def test_generate_unique_email_contains_at_symbol():
    result = generate_unique_email("user", "abc123", ["@gmail.com"])
    assert "@" in result


def test_generate_unique_email_starts_with_username():
    result = generate_unique_email("priscilla", "xyz", ["@test.com"])
    assert result.startswith("priscilla.xyz")


def test_generate_unique_email_uses_domain_from_list():
    domains = ["@gmail.com", "@yahoo.com"]
    result = generate_unique_email("user", "id", domains)
    assert any(result.endswith(d) for d in domains)


# --- generate_random_number ---

def test_generate_random_number_correct_digit_count():
    result = generate_random_number(5)
    assert len(result) == 5
    assert result.isdigit()


def test_generate_random_number_does_not_start_with_zero():
    for _ in range(20):
        assert generate_random_number(4)[0] != "0"


# --- split_string_between ---

def test_split_string_between_returns_middle():
    assert split_string_between("start[middle]end", "[", "]") == "middle"


def test_split_string_between_returns_empty_when_not_found():
    assert split_string_between("no brackets here", "[", "]") == ""


def test_split_string_between_returns_empty_when_only_open():
    assert split_string_between("hello[world", "[", "]") == ""


def test_split_string_between_returns_empty_when_adjacent():
    assert split_string_between("[]", "[", "]") == ""


# --- split_string_before ---

def test_split_string_before_returns_prefix():
    assert split_string_before("hello world", " ") == "hello"


def test_split_string_before_returns_empty_when_not_found():
    assert split_string_before("hello", " ") == ""


# --- split_string_after ---

def test_split_string_after_returns_suffix():
    assert split_string_after("hello world", " ") == "world"


def test_split_string_after_returns_empty_when_not_found():
    assert split_string_after("hello", " ") == ""


def test_split_string_after_uses_last_occurrence():
    assert split_string_after("a/b/c", "/") == "c"


def test_split_string_after_returns_empty_when_delimiter_is_at_end():
    assert split_string_after("hello/", "/") == ""


# --- remove_chars_from_string ---

def test_remove_chars_from_string():
    assert remove_chars_from_string("hello world", ["l", "o"]) == "he wrd"


def test_remove_chars_empty_list_returns_unchanged():
    assert remove_chars_from_string("hello", []) == "hello"


# --- replace_string_with ---

def test_replace_string_with():
    assert replace_string_with("foo bar foo", "foo", "baz") == "baz bar baz"
