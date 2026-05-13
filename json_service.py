import json
from datetime import datetime

def save_to_json(new_data, filename):
    new_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(filename, "r") as file:
            data_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_list = []
    data_list.append(new_data)

    with open(filename, "w") as file:
        json.dump(data_list, file, indent=4)

def get_all_logs(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []