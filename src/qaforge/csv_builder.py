import json
import csv
import os


def delete_output_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def load_csv(csv_file_path):
    with open(csv_file_path, mode='r') as csv_file:
        return [json.dumps(row, sort_keys=True) for row in csv.DictReader(csv_file)]


def load_csv_multiple_lines(csv_file, group_key, output_list_name, list_fields):
    result = {}
    with open(csv_file, 'r') as fh:
        for row in csv.DictReader(fh):
            key = get_group_key(row, group_key)
            if key not in result:
                result[key] = row.copy()
                result[key][output_list_name] = []
            result[key][output_list_name].append({field: row[field] for field in list_fields})
    return [json.dumps(data) for data in result.values()]


def get_group_key(row, group_key):
    return "_".join(str(row[r]) for r in row if r in group_key)


def get_scenario_data_csv(csv_file_path, test_scenario_id):
    with open(csv_file_path, mode='r') as csv_file:
        return [
            json.dumps(row, sort_keys=True)
            for row in csv.DictReader(csv_file)
            if test_scenario_id == row["test_scenario_id"]
        ]


def converter_pandas_csv_json(data_path):
    with open(data_path, 'r') as f:
        return json.dumps(list(csv.DictReader(f)))
