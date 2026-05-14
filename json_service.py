import os
import json
from datetime import datetime

def save_to_json(new_data, filename):
    new_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        DATA_DIR = "data"
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        with open(f"data/{filename}", "r") as file:
            data_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_list = []
    data_list.append(new_data)

    with open(f"data/{filename}", "w") as file:
        json.dump(data_list, file, indent=4)

def get_all_logs(filename):
    try:
        with open(f"data/{filename}", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []