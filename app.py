from db_metrics import get_con_metrics, get_db_size
from system_metrics import get_sys_metrics
from service import save_to_json

if(__name__ == "__main__"):
    metrics = {
        "connections": get_con_metrics(),
        "system": get_sys_metrics(),
        "db_size": get_db_size()
    }
    save_to_json(metrics)