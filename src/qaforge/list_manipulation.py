import random


def union_list_without_duplicate_item(list_a, list_b):
    result = list(list_a)
    result.extend(x for x in list_b if x not in result)
    return result


def intersection_list(list_a, list_b):
    return [list(filter(lambda x: x in list_a, sublist)) for sublist in list_b]


def remove_item_from_list(items, item):
    result = list(items)
    result.remove(item)
    return result


def get_random_item_from_list(items):
    return random.choice(items)


def get_different_random_item_from_list(items, item):
    remaining = [x for x in items if x != item]
    return random.choice(remaining)


def get_list_from_source(source, data):
    """Get a list of arguments named as 'data' on the 'source'."""
    data_args = source.get(data.replace(' ', '_'))
    if data_args is not None:
        return data_args[0]
    raise Exception(f"No matching results for parameter data = {data} was found in DataPool.")


def datapool_read(source, data, key):
    """Get the value of 'key' from the list named 'data' inside 'source'."""
    data_args = source.get(data.replace(' ', '_'))
    dt_key = key.replace(' ', '_')
    if data_args is None:
        raise Exception(f"No matching results for data = {data}, key = {key} in DataPool.")
    value = data_args[0].get(dt_key)
    if value is None:
        raise Exception(f"No matching results for data = {data}, key = {key} in DataPool.")
    return value


def get_data_from_dict(dict_args, key):
    """Search 'key' in 'dict_args' and return its value."""
    value = dict_args.get(key)
    if value is None:
        raise Exception(f"No matching results for parameter key = {key} was found in Dictionary.")
    return value
