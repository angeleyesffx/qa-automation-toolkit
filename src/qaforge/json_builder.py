import json
import os
import jinja2


def load_json_as_string(json_file_path):
    with open(json_file_path, 'r') as file:
        return file.read()


def load_json_as_dict(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)


def get_json_keys(json_file_path):
    return load_json_as_dict(json_file_path).keys()


def get_json_values(json_file_path):
    return load_json_as_dict(json_file_path).values()


def write_json_file(json_string, file_path="new_json.json"):
    with open(file_path, "w") as f:
        f.write(json.dumps(json_string, sort_keys=True))


def find_key_and_replace_value_json(obj, key, value):
    if isinstance(obj, dict):
        if key in obj:
            obj[key] = value
            return json.dumps(obj, indent=2, sort_keys=True)
        for v in obj.values():
            result = find_key_and_replace_value_json(v, key, value)
            if result is not None:
                return json.dumps(obj, indent=2, sort_keys=True)
    elif isinstance(obj, list):
        for item in obj:
            result = find_key_and_replace_value_json(item, key, value)
            if result is not None:
                return json.dumps(obj, indent=2, sort_keys=True)
    return None


def convert_to_dict(data):
    if isinstance(data, list):
        return data[0] if data else None
    if isinstance(data, dict):
        return data
    print("\nType is different from 'list' or 'dict'")
    return None


def edit_json(json_data, args):
    for args_key, args_value in args.items():
        if args_key in json_data:
            json_data[args_key] = args_value
        else:
            for val in json_data.values():
                if isinstance(val, (dict, list)):
                    find_key_and_replace_value_json(val, args_key, args_value)
    return [json_data]


def edit_template_json(json_file_path, args_data):
    new_json = []
    if isinstance(args_data, list):
        for item in args_data:
            args = json.loads(item)
            with open(json_file_path, 'r') as file:
                json_data = convert_to_dict(json.load(file))
            edited = edit_json(json_data, args)
            new_json.append(json.dumps(edited, sort_keys=True))
    elif isinstance(args_data, dict):
        with open(json_file_path, 'r') as file:
            json_data = convert_to_dict(json.load(file))
        edited = edit_json(json_data, args_data)
        new_json.append(json.dumps(edited, sort_keys=True))
    return new_json


def create_payload(json_template_name, data, multiple_request):
    edited_json = template_editor(json_template_name, data, multiple_request)
    return get_beautified_payload(json_template_name, edited_json)


def get_template_from_folder(folder_path, template_name):
    loader = jinja2.FileSystemLoader(searchpath=folder_path)
    return jinja2.Environment(loader=loader).get_template(template_name)


def template_editor(json_template_name, data, multiple_request):
    if json_template_name and json_template_name.lower() != "none" and data is not None:
        template = get_template_from_folder(
            os.path.join(os.getcwd(), "templates"),
            json_template_name + ".json",
        )
        if multiple_request and isinstance(data, list):
            return [template.render(dict_list=[d]) for d in data]
        return template.render(dict_list=data)
    return data


def get_beautified_payload(json_template_name, payload):
    if not isinstance(payload, list):
        body = payload.replace('\n', '').replace('"[', '[').replace(']"', ']').replace(
            '"{ ', '{').replace('}"', '}')
        return beautify_json(json_template_name, body)
    return [beautify_json(json_template_name, body) for body in payload]


def beautify_json(json_template_name, json_string):
    try:
        return json.dumps(json.loads(json_string), indent=4, ensure_ascii=False).encode('utf8')
    except json.decoder.JSONDecodeError as err:
        body = json_string.replace('"[', '[').replace(']"', ']').replace(
            '"{ ', '{').replace('}"', '}').replace(' ', '')
        raise Exception(
            f"Check if the template {json_template_name} is malformed and try again."
            f"\nError: {err}\nBody: {body}"
        )
