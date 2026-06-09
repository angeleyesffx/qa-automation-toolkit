import yaml


def read_yml_file(file_path):
    with open(file_path) as file:
        return yaml.full_load(file)


def select_the_keys_from_yml(yml_path, parent_reference):
    environments = read_yml_file(yml_path)
    params = set()
    if parent_reference == "environment":
        params.update(environments)
    else:
        for key in environments.keys():
            params.update(environments[key])
    return sorted(params)
