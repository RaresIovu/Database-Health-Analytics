import json
from datetime import datetime

def save_to_json(new_data):
    filename = "db_log.json"
    
    new_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Saving...")
    try:
        with open(filename, "r") as file:
            data_list = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_list = []
    data_list.append(new_data)

    with open(filename, "w") as file:
        json.dump(data_list, file, indent=4)
    
    print(f"Metrics saved to {filename}")

def get_all_logs():
    filename = 'db_log.json'
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []