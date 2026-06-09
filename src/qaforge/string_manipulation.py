import string
import random


def generate_unique_id(chars_number):
    """Generate N chars random string with Lowercase and Uppercase."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(chars_number))


def generate_unique_lowercase_id(chars_number):
    """Generate N chars random string with Lowercase."""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(chars_number))


def generate_unique_uppercase_id(chars_number):
    """Generate N chars random string with Uppercase."""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(chars_number))


def generate_unique_email(username, unique_id, domain_list):
    """Generate random email from username, unique_id, and a random domain from domain_list."""
    return username + '.' + unique_id + random.choice(domain_list)


def split_string_between(string_value, slice_a, slice_b):
    """Return the substring between slice_a and slice_b, or empty string if not found."""
    pos_a = string_value.find(slice_a)
    if pos_a == -1:
        return ""
    pos_b = string_value.rfind(slice_b)
    if pos_b == -1:
        return ""
    adjusted_pos_a = pos_a + len(slice_a)
    if adjusted_pos_a >= pos_b:
        return ""
    return string_value[adjusted_pos_a:pos_b]


def split_string_before(string_value, slice_a):
    """Return the substring before slice_a, or empty string if not found."""
    pos_a = string_value.find(slice_a)
    if pos_a == -1:
        return ""
    return string_value[0:pos_a]


def split_string_after(string_value, slice_a):
    """Return the substring after the last occurrence of slice_a, or empty string if not found."""
    pos_a = string_value.rfind(slice_a)
    if pos_a == -1:
        return ""
    adjusted_pos_a = pos_a + len(slice_a)
    if adjusted_pos_a >= len(string_value):
        return ""
    return string_value[adjusted_pos_a:]


def remove_chars_from_string(string_value, char_list):
    """Remove all characters in char_list from string_value."""
    for char in char_list:
        string_value = string_value.replace(char, "")
    return string_value


def replace_string_with(string_value, old_string, new_string):
    return string_value.replace(old_string, new_string)


def empty_string_to_none_string(string_value):
    """Return None if string_value is empty or None, otherwise return the original value."""
    return None if not string_value else string_value


def generate_random_number(number_of_digits):
    begin = int('1' + '0' * (number_of_digits - 1))
    end = int('9' * number_of_digits)
    return str(random.randrange(begin, end))
